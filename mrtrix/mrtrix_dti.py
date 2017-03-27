#!/om/user/ksitek/envs/ksitek_env/bin/python

import os
import nipype.interfaces.mrtrix3 as mrt

n_threads = 4
bvecs = os.path.join('/om/user/ksitek/exvivo/data/','camino_120_RAS_T.bvecs')
bvals = os.path.join('/om/user/ksitek/exvivo/data/','camino_120_RAS_T.bvals')

dwi_file = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dwi.mif')
dti_file = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dti/dti.mif')
mask_file = os.path.join('/om/user/ksitek/exvivo/data/','Reg_S64550_nii_b0-slice_mask.nii.gz')

'''
tsr = mrt.FitTensor()
tsr.inputs.in_file = os.path.join('/om/user/ksitek/exvivo/mrtrix/','dwi.mif')
tsr.inputs.in_mask = os.path.join('/om/user/ksitek/exvivo/data/','Reg_S64550_nii_b0-slice_mask.nii.gz')
tsr.inputs.grad_fsl = (bvecs, bvals)
tsr.inputs.nthreads = n_threads
tsr.inputs.out_file = dti_file
tsr.cmdline                               
tsr.run()
'''

tk = mrt.Tractography()
tk.inputs.in_file = dwi_file
tk.inputs.algorithm = 'Tensor_Det'
tk.inputs.seed_image = mask_file
tk.inputs.grad_fsl = (bvecs, bvals)
tk.inputs.n_tracks = 1000000
tk.inputs.out_file = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dti/tensor_det_1m.tck')
tk.inputs.nthreads = n_threads
tk.run()

'''
import nipype.interfaces.mrtrix
tck2trk = mrtrix.MRTrix2TrackVis()
tck2trk.inputs.out_filename = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dti/mrtrix_detDTI.trk')
tck2trk.run()
'''

tk_prob = mrt.Tractography()
tk_prob.inputs.in_file = dwi_file
tk_prob.inputs.algorithm = 'Tensor_Det'
tk_prob.inputs.seed_image = mask_file
tk_prob.inputs.grad_fsl = (bvecs, bvals)
tk_prob.inputs.n_tracks = 1000000
tk_prob.inputs.out_file = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dti/tensor_prob_1m.tck')
tk_prob.inputs.nthreads = n_threads
tk_prob.run()

'''
import nipype.interfaces.mrtrix
tck2trk = mrtrix.MRTrix2TrackVis()
tck2trk.inputs.out_filename = os.path.abspath('/om/user/ksitek/exvivo/mrtrix/dti/mrtrix_probDTI.trk')
tck2trk.run()
'''

