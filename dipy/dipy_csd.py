from nipype import config
config.enable_provenance()

from nipype import Node, Function, Workflow, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink

import os
from glob import glob

data_dir = '/om/user/ksitek/exvivo/data'
out_dir = '/om/user/ksitek/exvivo/analysis/dipy_csd'
sids = ['Reg_S64550']

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

work_dir = os.path.abspath('/om/scratch/Fri/ksitek/dipy_csd')

def dmri_recon(sid, data_dir, out_dir, recon='csd', num_threads=1):
    import tempfile
    #tempfile.tempdir = '/om/scratch/Fri/ksitek/'

    import os
    oldval = None
    if 'MKL_NUM_THREADS' in os.environ:
        oldval = os.environ['MKL_NUM_THREADS']
    os.environ['MKL_NUM_THREADS'] = '%d' % num_threads
    ompoldval = None
    if 'OMP_NUM_THREADS' in os.environ:
        ompoldval = os.environ['OMP_NUM_THREADS']
    os.environ['OMP_NUM_THREADS'] = '%d' % num_threads
    import nibabel as nib
    import numpy as np
    from glob import glob


    fimg = os.path.abspath(glob(os.path.join(data_dir,
                                             'Reg_S64550_nii4d.nii.gz'))[0])
    print "dwi file = %s"%fimg
    fbvec = os.path.abspath(glob(os.path.join(data_dir,
                                              'camino_120_RAS.bvecs'))[0])
    print "bvec file = %s"%fbvec
    fbval = os.path.abspath(glob(os.path.join(data_dir,
                                              'camino_120_RAS.bvals'))[0])
    print "bval file = %s"%fbval
    img = nib.load(fimg)
    data = img.get_data()

    prefix = sid

    from dipy.io import read_bvals_bvecs
    from dipy.core.gradients import vector_norm
    bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
    print "bvals.shape:"
    print bvals.shape
    print "bvecs.shape:"
    print bvecs.shape

    b0idx = []
    for idx, val in enumerate(bvals):
        if val < 1:
            pass
            #bvecs[idx] = [1, 0, 0]
        else:
            b0idx.append(idx)
            print "b0idx=%d"%idx
    print "input bvecs:"
    print bvecs
    bvecs[b0idx, :] = bvecs[b0idx, :]/vector_norm(bvecs[b0idx])[:, None]
    print "bvecs after normalization:"
    print bvecs


    from dipy.core.gradients import gradient_table
    gtab = gradient_table(bvals, bvecs)
    print "bvecs shape?"
    gtab.bvecs.shape == bvecs.shape
    gtab.bvecs
    print "bvals shape?"
    gtab.bvals.shape == bvals.shape
    gtab.bvals


    from dipy.reconst.csdeconv import auto_response
    response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)
    print "response:"
    print response
    print "ratio:"
    print ratio

    #from dipy.segment.mask import median_otsu
    #b0_mask, mask = median_otsu(data[:, :, :, b0idx].mean(axis=3).squeeze(), 4, 4)

    fmask1 = os.path.join(data_dir, 'Reg_S64550_nii_b0-slice_mask.nii.gz')
    print "fmask file = %s"%fmask1
    mask = nib.load(fmask1).get_data()

    useFA = True
    print "creating model"
    if recon == 'csd':
        from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
        model = ConstrainedSphericalDeconvModel(gtab, response)
        useFA = True
    elif recon == 'csa':
        from dipy.reconst.shm import CsaOdfModel, normalize_data
        model = CsaOdfModel(gtab, 4)
        useFA = False
    else:
        raise ValueError('only csd, csa supported currently')
        from dipy.reconst.dsi import (DiffusionSpectrumDeconvModel,
                                      DiffusionSpectrumModel)
        model = DiffusionSpectrumDeconvModel(gtab)
    #fit = model.fit(data)

    from dipy.data import get_sphere
    sphere = get_sphere('symmetric724')
    #odfs = fit.odf(sphere)

    from dipy.reconst.peaks import peaks_from_model
    print "running peaks_from_model"
    peaks = peaks_from_model(model=model,
                             data=data,
                             sphere=sphere,
                             mask=mask,
                             return_sh=True,
                             return_odf=False,
                             normalize_peaks=True,
                             npeaks=5,
                             relative_peak_threshold=.5,
                             min_separation_angle=25,
                             parallel=num_threads > 1,
                             nbr_processes=num_threads)

    from dipy.reconst.dti import TensorModel
    print "running tensor model"
    tenmodel = TensorModel(gtab)
    tenfit = tenmodel.fit(data, mask)

    from dipy.reconst.dti import fractional_anisotropy
    print "running FA"
    FA = fractional_anisotropy(tenfit.evals)
    FA[np.isnan(FA)] = 0
    fa_img = nib.Nifti1Image(FA, img.get_affine())
    tensor_fa_file = os.path.abspath('%s_tensor_fa.nii.gz' % (prefix))
    nib.save(fa_img, tensor_fa_file)

    evecs = tenfit.evecs
    evec_img = nib.Nifti1Image(evecs, img.get_affine())
    tensor_evec_file = os.path.abspath('%s_tensor_evec.nii.gz' % (prefix))
    nib.save(evec_img, tensor_evec_file)

    #from dipy.reconst.dti import quantize_evecs
    #peak_indices = quantize_evecs(tenfit.evecs, sphere.vertices)
    #eu = EuDX(FA, peak_indices, odf_vertices = sphere.vertices,
               #a_low=0.2, seeds=10**6, ang_thr=35)

    fa_img = nib.Nifti1Image(peaks.gfa, img.get_affine())
    model_gfa_file = os.path.abspath('%s_%s_gfa.nii.gz' % (prefix, recon))
    nib.save(fa_img, model_gfa_file)

    from dipy.tracking.eudx import EuDX
    print "reconstructing with EuDX"
    if useFA:
        eu = EuDX(FA, peaks.peak_indices[..., 0],
                  odf_vertices = sphere.vertices,
                  a_low=0.1, seeds=10**6, ang_thr=35)
    else:
        eu = EuDX(peaks.gfa, peaks.peak_indices[..., 0],
                  odf_vertices = sphere.vertices,
                  a_low=0.1, seeds=10**6, ang_thr=35)

    #import dipy.tracking.metrics as dmetrics
    streamlines = ((sl, None, None) for sl in eu) # if dmetrics.length(sl) > 15)

    hdr = nib.trackvis.empty_header()
    hdr['voxel_size'] = fa_img.get_header().get_zooms()[:3]
    hdr['voxel_order'] = 'LAS'
    hdr['dim'] = FA.shape[:3]

    sl_fname = os.path.abspath('%s_%s_streamline.trk' % (prefix, recon))

    nib.trackvis.write(sl_fname, streamlines, hdr, points_space='voxel')
    if oldval:
        os.environ['MKL_NUM_THREADS'] = oldval
    else:
        del os.environ['MKL_NUM_THREADS']
    if ompoldval:
        os.environ['OMP_NUM_THREADS'] = ompoldval
    else:
        del os.environ['OMP_NUM_THREADS']
    return tensor_fa_file, tensor_evec_file, model_gfa_file, sl_fname

infosource = Node(IdentityInterface(fields=['subject_id']), name='infosource')
infosource.iterables = ('subject_id', sids)

tracker = Node(Function(input_names=['sid', 'data_dir', 'out_dir',
                                     'recon', 'num_threads'],
                        output_names=['tensor_fa_file', 'tensor_evec_file',
                                      'model_gfa_file',
                                      'model_track_file'],
                        function=dmri_recon), name='tracker')
tracker.inputs.data_dir = data_dir
tracker.inputs.out_dir = out_dir
tracker.inputs.recon = 'csd'
num_threads = 2 # 20
tracker.inputs.num_threads = num_threads
tracker.plugin_args = {'sbatch_args': '--time=6:00:00 --mem=%dG -N 1 -c %d --qos=gablab' % (20 * num_threads, num_threads),
                       'overwrite': True}

ds = Node(DataSink(parameterization=False), name='sinker')
ds.inputs.base_directory = out_dir
ds.plugin_args = {'overwrite': True}

wf = Workflow(name='exvivo')

wf.connect(infosource, 'subject_id', tracker, 'sid')
#wf.connect(tracker, 'sid', ds, 'container')

wf.connect(tracker, 'tensor_fa_file', ds, 'recon.@fa')
wf.connect(tracker, 'tensor_evec_file', ds, 'recon.@evec')
wf.connect(tracker, 'model_gfa_file', ds, 'recon.@gfa')
wf.connect(tracker, 'model_track_file', ds, 'recon.@track')

wf.base_dir = work_dir

wf.run(plugin='SLURM',
       plugin_args={'sbatch_args': '--time=23:59:59 --mem=10G -N1 -c2 --qos=gablab'})
