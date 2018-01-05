#from nipype import config
#config.enable_provenance()
#
from nipype import Node, Function, Workflow, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink

import os
from glob import glob

resolution = '0.8mm'

data_dir = '/om/user/ksitek/exvivo/data'
out_dir = '/om/user/ksitek/exvivo/analysis/dipy_csd/%s_fa_thresh_0.3_ang_thresh_45/'%resolution
sids = ['Reg_S64550']

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

work_dir = os.path.abspath('/om/scratch/Thu/ksitek/dipy_csd/%s'%resolution)

# if you want to run tractography from specific regions of interest
atlas_file = os.path.join('/om/user/ksitek/exvivo/maastricht/',
                          'atlas/maas-atlas2exvivo_ants_Linear.nii.gz')
atlas_labels = [x+1 for x in range(8)] # labels 1-8

def dmri_recon(sid, data_dir, out_dir, resolution, recon='csd', num_threads=1):
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

    if resolution = '0.2mm':
        filename = 'Reg_S64550_nii4d.nii.gz'
    else:
        filename = 'Reg_S64550_nii4d_resamp-%s.nii.gz'%(resolution)
    fimg = os.path.abspath(glob(os.path.join(data_dir, 'resample', filename))[0])
    print "dwi file = %s"%fimg
    fbvec = os.path.abspath(glob(os.path.join(data_dir, 'bvecs',
                                              'camino_120_RAS_flipped-xy.bvecs'))[0])
    print "bvec file = %s"%fbvec
    fbval = os.path.abspath(glob(os.path.join(data_dir, 'bvecs',
                                              'camino_120_RAS.bvals'))[0])
    print "bval file = %s"%fbval
    img = nib.load(fimg)
    data = img.get_data()

    affine = img.get_affine()

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
    response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.3) # 0.7
    print "response:"
    print response
    print "ratio:"
    print ratio

    #from dipy.segment.mask import median_otsu
    #b0_mask, mask = median_otsu(data[:, :, :, b0idx].mean(axis=3).squeeze(), 4, 4)

    if resolution = '0.2mm':
        mask_name = 'Reg_S64550_nii_b0-slice_mask.nii.gz'
        fmask1 = os.path.join(data_dir, mask_name)
    else:
        mask_name = 'Reg_S64550_nii_b0-slice_mask_resamp-%s.nii.gz'%(resolution)
        fmask1 = os.path.join(data_dir, 'resample', mask_name)
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
                  #a_low=0.1,
                  seeds=10**6,
                  ang_thr=45)
    else:
        eu = EuDX(peaks.gfa, peaks.peak_indices[..., 0],
                  odf_vertices = sphere.vertices,
                  #a_low=0.1,
                  seeds=10**6,
                  ang_thr=45)

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
    return tensor_fa_file, tensor_evec_file, model_gfa_file, sl_fname, affine

# extract targets from an atlas file
# see nilearn example 8.5.4. Regions Extraction of Default Mode Networks using Smith Atlas
def extract_region(atlas_file, label):
    from nipype.interfaces.base import CommandLine
    from nipype.pipeline.engine import Node
    node = Node(CommandLine('fslmaths %s -thr %s -uthr %s region_%s.nii.gz'%(atlas_file, label, label, label)),
                name = 'extract_roi')
    node.base_dir = os.getcwd()
    node.run()

    return single_region

region_extracter = Node(Function(input_names = ['atlas_file','label'],
                                 output_names = ['single_region'],
                                 function = extract_region,
                                 name = 'region_extracter'))

# filter streamlines by region of interest
def sl_filter(streamlines, target_mask, affine, include=True):
    from dipy.tracking.utils import target

    target(streamlines, target_mask, affine, include=True)

    return target_streamlines

filter_streamlines = Node(Function(input_names = ['streamlines', 'target_mask',
                                                  'affine'],
                                   output_names = ['target_streamlines'],
                                   function = sl_filter,
                                   name = 'filter_streamlines'))

infosource = Node(IdentityInterface(fields=['subject_id',
                                            'atlas_file', 'region_label']),
                                    name='infosource')
infosource.iterables = ('subject_id', sids)
infosource.iterables = ('region_label', atlas_labels)
infosource.inputs.atlas_file = atlas_file

tracker = Node(Function(input_names=['sid', 'data_dir', 'out_dir', 'resolution',
                                     'recon', 'num_threads'],
                        output_names=['tensor_fa_file', 'tensor_evec_file',
                                      'model_gfa_file',
                                      'model_track_file',
                                      'affine'],
                        function=dmri_recon), name='tracker')
tracker.inputs.data_dir = data_dir
tracker.inputs.out_dir = out_dir
tracker.inputs.resolution = resolution
tracker.inputs.recon = 'csd'
num_threads =  10
tracker.inputs.num_threads = num_threads
tracker.plugin_args = {'sbatch_args': '--qos=gablab --time=2-00:00:00 --mem=%dG -N 1 -c %d' % (20 * num_threads, num_threads),
                       'overwrite': True}

ds = Node(DataSink(parameterization=False), name='sinker')
ds.inputs.base_directory = out_dir
ds.plugin_args = {'overwrite': True}

wf = Workflow(name='exvivo')

wf.connect(infosource, 'subject_id', tracker, 'sid')
#wf.connect(tracker, 'sid', ds, 'container')

# atlas target filtering
wf.connect(infosource, 'atlas_file', region_extracter, 'atlas_file')
wf.connect(infosource, 'region_label', region_extracter, 'label')

wf.connect(tracker, 'model_track_file', filter_streamlines, 'streamlines')
wf.connect(region_extracter, 'single_region', filter_streamlines, 'target_mask')
wf.connect(tracker, 'affine', filter_streamlines, 'affine')

wf.connect(tracker, 'tensor_fa_file', ds, 'recon.@fa')
wf.connect(tracker, 'tensor_evec_file', ds, 'recon.@evec')
wf.connect(tracker, 'model_gfa_file', ds, 'recon.@gfa')
wf.connect(tracker, 'model_track_file', ds, 'recon.@track')

wf.base_dir = work_dir

wf.run(plugin='SLURM',
       plugin_args={'sbatch_args': '--time=3-00:00:00 --mem=80G -N1 -c2 --qos=gablab'})
