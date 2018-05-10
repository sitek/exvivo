
# run one of a few models
# KRS 2018.02.26

import numpy as np
import nibabel as nb
import os

n_jobs = 16

project_dir = os.path.abspath('/om2/user/ksitek/exvivo')
resolution = '0.4mm'

infile_basenames = ['Reg_S64550_tensor_fa',
                    'Reg_S64550_tensor_ad',
                    'Reg_S64550_tensor_rd',
                    'Reg_S64550_tensor_md'
                    ]
infile_basenames = ['Reg_S64550_shm_coeff']

data_dir = os.path.join(project_dir,
                        'analysis','dipy_csd',
                        'Mar30_%s'%resolution,'recon')
data_files = [os.path.join(data_dir, '%s.nii.gz'%x) for x in infile_basenames]

out_dir = os.path.join(project_dir, 'analysis', 'cluster', 'diff_%s'%resolution)
out_basename = 'fa_ad_rd_md'

for ix, data_file in enumerate(data_files):
    # load the data
    print("loading data: %s"%(os.path.basename(data_file)), flush=True)
    data_img = nb.load(data_file)

    if data_img.get_data().ndim == 4: # if spherical harmonics
        print('4-D data not yet supported')
        X_4D = data_img.get_data()
        for shm in range(X_4D.shape[3]): # for each dimension of the metric
            X_3D = X_4D[:,:,:,shm].reshape(X_4D.shape[0],
                                           X_4D.shape[1],
                                           X_4D.shape[2])
            if shm == 0:
                X_1D = X_3D.reshape(-1, 1)
            else:
                X_1D = np.hstack((X_1D, X_3D.reshape(-1, 1)))
            # not technically "1D", but it works
    elif data_img.get_data().ndim == 3: # if 3D map, like FA or RD
        X_3D = data_img.get_data()
        #X_3D = X_3D[50:150, 50:150, 50:150] # use a subset of data
        print('data shape: ', X_3D.shape)

        print('masking data')
        mask_data = X_3D.astype(bool)

        # reshape data to a single feature column
        X_1D = X_3D.reshape(-1, 1)

    """
            # get rid of zeros in the data but remember the ordering
            nonzero_indices = np.where(X_1D!=0)
            X_nonzero = X_1D[nonzero_indices].reshape(-1, 1)
            print('nonzero voxels: ', X_nonzero.shape)
    """

    # save 3D indices to 3 columns
    XX, YY, ZZ = np.meshgrid(np.arange(X_3D.shape[2]),
                             np.arange(X_3D.shape[1]),
                             np.arange(X_3D.shape[0]))
    coord_3D = np.vstack((XX, YY, ZZ)).reshape(3,-1).T
    print('coord_3D.shape = ', coord_3D.shape)

    # add in spatial features
    if ix==0:
        spatial_feature = ''
        if spatial_feature == 'coordinates':
            # combine data + coordinates
            #X_raw = np.hstack((coord_3D[nonzero_indices[0],:], X_1D))
            X_raw = np.hstack((coord_3D, X_1D))

        elif spatial_feature == 'euclidean_distance':
            # alternatively, use Euclidean distance of coordinates from centroid
            centroid = np.array([int(X_3D.shape[0]/2),
                                 int(X_3D.shape[1]/2),
                                 int(X_3D.shape[2]/2)])
            #dist = np.linalg.norm(coord_3D - centroid)
            from scipy.spatial.distance import cdist
            dist = cdist(coord_3D, centroid.reshape(1,-1))
            print('dist.shape = ', dist.shape)
            print(dist)

            #X_raw = np.hstack((dist[nonzero_indices[0]], X_1D))
            X_raw = np.hstack((dist, X_1D))
        else:
            X_raw = X_1D
    else:
        print('X_raw shape = ', X_raw.shape)
        X_raw = np.hstack((X_raw, X_1D))

# normalize data across features
from sklearn.preprocessing import normalize
X = normalize(X_raw)

# check the data
print("normalized data:")
print(X[:10,:])

# run the model
clustering = 'kmeans'
for clust_val in [10, 20]:#[10, 20, 50, 100, 200]:
    if clustering == 'spectral':
        from sklearn.feature_extraction import image
        from sklearn.cluster import spectral_clustering

        # spectral clustering runs on a symmetric graph, not feature space
        print('creating a graph', flush=True)
        graph = image.img_to_graph(X_3D,mask=mask_data)

        # only outputs labels, not a full model
        print('running spectral clustering')
        labels = spectral_clustering(graph,
                                     n_clusters=clust_val,
                                     eigen_solver='arpack',
                                     assign_labels='discretize')

    else:
        if clustering == 'hdbscan':
            from hdbscan import HDBSCAN
            clusters = clust_val # min_cluster_size
            print("running %s with min_samples = %d"%(clustering, clusters))
            model = HDBSCAN(min_cluster_size=clusters,
                            core_dist_n_jobs=n_jobs).fit(X)
        elif clustering == 'dbscan':
            from sklearn.cluster import DBSCAN
            clusters = clust_val
            print("running %s with min_samples = %d"%(clustering, clusters),
                  flush=True)
            model = DBSCAN(min_samples=clusters, n_jobs=n_jobs).fit(X)
        elif clustering == 'kmeans':
            from sklearn.cluster import KMeans
            clusters = clust_val # number of clusters (k)
            print("running %s with %d clusters"%(clustering, clusters))
            model = KMeans(n_clusters=clusters, n_jobs=n_jobs).fit(X)

        # save entire model to explore later
        print("saving model")
        from sklearn.externals import joblib
        out_pkl = os.path.join(out_dir,'%s_%s_%s_%d.pkl'%(out_basename,
                                                          spatial_feature,
                                                          clustering,
                                                          clusters))
        joblib.dump(model, out_pkl)

        # convert labels back to 3D and save labels to nifti
        print("saving labels")
        labels = model.labels_

        labels_withzeros = np.zeros(X_1D.shape, dtype=int)
        #labels_withzeros[nonzero_indices] = labels
        labels_withzeros = labels
        labels_3D = labels_withzeros.reshape(X_3D.shape)

    label_img = nb.Nifti1Image(labels_3D, data_img.affine, data_img.header)

    out_img = os.path.join(out_dir, '%s_%s_%s_labels_%d.nii.gz'%(out_basename,
                                                                 spatial_feature,
                                                                 clustering,
                                                                 clusters))
    nb.save(label_img, out_img)
