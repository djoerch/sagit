#!/usr/bin/python

from optparse import OptionParser
import numpy as np
import nibabel as nib
import sys
from mayavi import mlab
from scipy import interpolate as sinterp

def run(options, args):
	vol2iso_viz(args[0], options.bg, show_label=options.show_label, slice_index=options.slice_index, plane_orientation=options.orientation, save_fig=options.output)

def vol2iso_viz(vol_file, bg_file, bgcolor=(0,0,0), bgslice='', auto_slice=True, show_label=1, force_show_fig=False, save_fig=None, show_outline=False, 
	plane_orientation='z_axes', slice_index=0,
	size=(1024,768),vmin=0,nb_labels=10,nb_colors=10,label_orientation='vertical'):
	def getNiftiAsScalarField(filename):
		fimg = nib.load(filename)
		hdr = fimg.get_header()
		data = fimg.get_data()

		print data.shape

		af = fimg.get_affine()
		origin = af[:3,3]
		stride = [af[0,0],af[1,1],af[2,2]]
		print stride

		if stride[0] < 0:
			print 'flipX'
			data = data[::-1,:,:]
			#data = np.flipud(data)
		if stride[1] < 0:
			print 'flipY'			
			data = data[:,::-1,:]
		if stride[2] < 0:
			print 'flipZ'			
			data = data[:,:,::-1]			

		src = mlab.pipeline.scalar_field(data)
		src.spacing = hdr.get_zooms()
		src.origin = origin

		src.update_image_data = True	
		return src, data

	if save_fig:
		mlab.options.offscreen=True
	mlab.figure(bgcolor=bgcolor, size=size)

	# try tp turn on depth peeling
	# https://dl.dropboxusercontent.com/u/1200872/mayavi/depth_peeling.py

	scene = mlab.gcf().scene
	scene.renderer.render_window.set(alpha_bit_planes=1,multi_samples=0)
	scene.renderer.set(use_depth_peeling=True,maximum_number_of_peels=4,occlusion_ratio=0.1)

	# print "Traits for the renderer"
	# scene.renderer.print_traits()
	# print "Traits for the render window"
	# scene.renderer.render_window.print_traits()

	_plasma_data = [[0.050383, 0.029803, 0.527975, 1.0],
                [0.063536, 0.028426, 0.533124, 1.0],
                [0.075353, 0.027206, 0.538007, 1.0],
                [0.086222, 0.026125, 0.542658, 1.0],
                [0.096379, 0.025165, 0.547103, 1.0],
                [0.105980, 0.024309, 0.551368, 1.0],
                [0.115124, 0.023556, 0.555468, 1.0],
                [0.123903, 0.022878, 0.559423, 1.0],
                [0.132381, 0.022258, 0.563250, 1.0],
                [0.140603, 0.021687, 0.566959, 1.0],
                [0.148607, 0.021154, 0.570562, 1.0],
                [0.156421, 0.020651, 0.574065, 1.0],
                [0.164070, 0.020171, 0.577478, 1.0],
                [0.171574, 0.019706, 0.580806, 1.0],
                [0.178950, 0.019252, 0.584054, 1.0],
                [0.186213, 0.018803, 0.587228, 1.0],
                [0.193374, 0.018354, 0.590330, 1.0],
                [0.200445, 0.017902, 0.593364, 1.0],
                [0.207435, 0.017442, 0.596333, 1.0],
                [0.214350, 0.016973, 0.599239, 1.0],
                [0.221197, 0.016497, 0.602083, 1.0],
                [0.227983, 0.016007, 0.604867, 1.0],
                [0.234715, 0.015502, 0.607592, 1.0],
                [0.241396, 0.014979, 0.610259, 1.0],
                [0.248032, 0.014439, 0.612868, 1.0],
                [0.254627, 0.013882, 0.615419, 1.0],
                [0.261183, 0.013308, 0.617911, 1.0],
                [0.267703, 0.012716, 0.620346, 1.0],
                [0.274191, 0.012109, 0.622722, 1.0],
                [0.280648, 0.011488, 0.625038, 1.0],
                [0.287076, 0.010855, 0.627295, 1.0],
                [0.293478, 0.010213, 0.629490, 1.0],
                [0.299855, 0.009561, 0.631624, 1.0],
                [0.306210, 0.008902, 0.633694, 1.0],
                [0.312543, 0.008239, 0.635700, 1.0],
                [0.318856, 0.007576, 0.637640, 1.0],
                [0.325150, 0.006915, 0.639512, 1.0],
                [0.331426, 0.006261, 0.641316, 1.0],
                [0.337683, 0.005618, 0.643049, 1.0],
                [0.343925, 0.004991, 0.644710, 1.0],
                [0.350150, 0.004382, 0.646298, 1.0],
                [0.356359, 0.003798, 0.647810, 1.0],
                [0.362553, 0.003243, 0.649245, 1.0],
                [0.368733, 0.002724, 0.650601, 1.0],
                [0.374897, 0.002245, 0.651876, 1.0],
                [0.381047, 0.001814, 0.653068, 1.0],
                [0.387183, 0.001434, 0.654177, 1.0],
                [0.393304, 0.001114, 0.655199, 1.0],
                [0.399411, 0.000859, 0.656133, 1.0],
                [0.405503, 0.000678, 0.656977, 1.0],
                [0.411580, 0.000577, 0.657730, 1.0],
                [0.417642, 0.000564, 0.658390, 1.0],
                [0.423689, 0.000646, 0.658956, 1.0],
                [0.429719, 0.000831, 0.659425, 1.0],
                [0.435734, 0.001127, 0.659797, 1.0],
                [0.441732, 0.001540, 0.660069, 1.0],
                [0.447714, 0.002080, 0.660240, 1.0],
                [0.453677, 0.002755, 0.660310, 1.0],
                [0.459623, 0.003574, 0.660277, 1.0],
                [0.465550, 0.004545, 0.660139, 1.0],
                [0.471457, 0.005678, 0.659897, 1.0],
                [0.477344, 0.006980, 0.659549, 1.0],
                [0.483210, 0.008460, 0.659095, 1.0],
                [0.489055, 0.010127, 0.658534, 1.0],
                [0.494877, 0.011990, 0.657865, 1.0],
                [0.500678, 0.014055, 0.657088, 1.0],
                [0.506454, 0.016333, 0.656202, 1.0],
                [0.512206, 0.018833, 0.655209, 1.0],
                [0.517933, 0.021563, 0.654109, 1.0],
                [0.523633, 0.024532, 0.652901, 1.0],
                [0.529306, 0.027747, 0.651586, 1.0],
                [0.534952, 0.031217, 0.650165, 1.0],
                [0.540570, 0.034950, 0.648640, 1.0],
                [0.546157, 0.038954, 0.647010, 1.0],
                [0.551715, 0.043136, 0.645277, 1.0],
                [0.557243, 0.047331, 0.643443, 1.0],
                [0.562738, 0.051545, 0.641509, 1.0],
                [0.568201, 0.055778, 0.639477, 1.0],
                [0.573632, 0.060028, 0.637349, 1.0],
                [0.579029, 0.064296, 0.635126, 1.0],
                [0.584391, 0.068579, 0.632812, 1.0],
                [0.589719, 0.072878, 0.630408, 1.0],
                [0.595011, 0.077190, 0.627917, 1.0],
                [0.600266, 0.081516, 0.625342, 1.0],
                [0.605485, 0.085854, 0.622686, 1.0],
                [0.610667, 0.090204, 0.619951, 1.0],
                [0.615812, 0.094564, 0.617140, 1.0],
                [0.620919, 0.098934, 0.614257, 1.0],
                [0.625987, 0.103312, 0.611305, 1.0],
                [0.631017, 0.107699, 0.608287, 1.0],
                [0.636008, 0.112092, 0.605205, 1.0],
                [0.640959, 0.116492, 0.602065, 1.0],
                [0.645872, 0.120898, 0.598867, 1.0],
                [0.650746, 0.125309, 0.595617, 1.0],
                [0.655580, 0.129725, 0.592317, 1.0],
                [0.660374, 0.134144, 0.588971, 1.0],
                [0.665129, 0.138566, 0.585582, 1.0],
                [0.669845, 0.142992, 0.582154, 1.0],
                [0.674522, 0.147419, 0.578688, 1.0],
                [0.679160, 0.151848, 0.575189, 1.0],
                [0.683758, 0.156278, 0.571660, 1.0],
                [0.688318, 0.160709, 0.568103, 1.0],
                [0.692840, 0.165141, 0.564522, 1.0],
                [0.697324, 0.169573, 0.560919, 1.0],
                [0.701769, 0.174005, 0.557296, 1.0],
                [0.706178, 0.178437, 0.553657, 1.0],
                [0.710549, 0.182868, 0.550004, 1.0],
                [0.714883, 0.187299, 0.546338, 1.0],
                [0.719181, 0.191729, 0.542663, 1.0],
                [0.723444, 0.196158, 0.538981, 1.0],
                [0.727670, 0.200586, 0.535293, 1.0],
                [0.731862, 0.205013, 0.531601, 1.0],
                [0.736019, 0.209439, 0.527908, 1.0],
                [0.740143, 0.213864, 0.524216, 1.0],
                [0.744232, 0.218288, 0.520524, 1.0],
                [0.748289, 0.222711, 0.516834, 1.0],
                [0.752312, 0.227133, 0.513149, 1.0],
                [0.756304, 0.231555, 0.509468, 1.0],
                [0.760264, 0.235976, 0.505794, 1.0],
                [0.764193, 0.240396, 0.502126, 1.0],
                [0.768090, 0.244817, 0.498465, 1.0],
                [0.771958, 0.249237, 0.494813, 1.0],
                [0.775796, 0.253658, 0.491171, 1.0],
                [0.779604, 0.258078, 0.487539, 1.0],
                [0.783383, 0.262500, 0.483918, 1.0],
                [0.787133, 0.266922, 0.480307, 1.0],
                [0.790855, 0.271345, 0.476706, 1.0],
                [0.794549, 0.275770, 0.473117, 1.0],
                [0.798216, 0.280197, 0.469538, 1.0],
                [0.801855, 0.284626, 0.465971, 1.0],
                [0.805467, 0.289057, 0.462415, 1.0],
                [0.809052, 0.293491, 0.458870, 1.0],
                [0.812612, 0.297928, 0.455338, 1.0],
                [0.816144, 0.302368, 0.451816, 1.0],
                [0.819651, 0.306812, 0.448306, 1.0],
                [0.823132, 0.311261, 0.444806, 1.0],
                [0.826588, 0.315714, 0.441316, 1.0],
                [0.830018, 0.320172, 0.437836, 1.0],
                [0.833422, 0.324635, 0.434366, 1.0],
                [0.836801, 0.329105, 0.430905, 1.0],
                [0.840155, 0.333580, 0.427455, 1.0],
                [0.843484, 0.338062, 0.424013, 1.0],
                [0.846788, 0.342551, 0.420579, 1.0],
                [0.850066, 0.347048, 0.417153, 1.0],
                [0.853319, 0.351553, 0.413734, 1.0],
                [0.856547, 0.356066, 0.410322, 1.0],
                [0.859750, 0.360588, 0.406917, 1.0],
                [0.862927, 0.365119, 0.403519, 1.0],
                [0.866078, 0.369660, 0.400126, 1.0],
                [0.869203, 0.374212, 0.396738, 1.0],
                [0.872303, 0.378774, 0.393355, 1.0],
                [0.875376, 0.383347, 0.389976, 1.0],
                [0.878423, 0.387932, 0.386600, 1.0],
                [0.881443, 0.392529, 0.383229, 1.0],
                [0.884436, 0.397139, 0.379860, 1.0],
                [0.887402, 0.401762, 0.376494, 1.0],
                [0.890340, 0.406398, 0.373130, 1.0],
                [0.893250, 0.411048, 0.369768, 1.0],
                [0.896131, 0.415712, 0.366407, 1.0],
                [0.898984, 0.420392, 0.363047, 1.0],
                [0.901807, 0.425087, 0.359688, 1.0],
                [0.904601, 0.429797, 0.356329, 1.0],
                [0.907365, 0.434524, 0.352970, 1.0],
                [0.910098, 0.439268, 0.349610, 1.0],
                [0.912800, 0.444029, 0.346251, 1.0],
                [0.915471, 0.448807, 0.342890, 1.0],
                [0.918109, 0.453603, 0.339529, 1.0],
                [0.920714, 0.458417, 0.336166, 1.0],
                [0.923287, 0.463251, 0.332801, 1.0],
                [0.925825, 0.468103, 0.329435, 1.0],
                [0.928329, 0.472975, 0.326067, 1.0],
                [0.930798, 0.477867, 0.322697, 1.0],
                [0.933232, 0.482780, 0.319325, 1.0],
                [0.935630, 0.487712, 0.315952, 1.0],
                [0.937990, 0.492667, 0.312575, 1.0],
                [0.940313, 0.497642, 0.309197, 1.0],
                [0.942598, 0.502639, 0.305816, 1.0],
                [0.944844, 0.507658, 0.302433, 1.0],
                [0.947051, 0.512699, 0.299049, 1.0],
                [0.949217, 0.517763, 0.295662, 1.0],
                [0.951344, 0.522850, 0.292275, 1.0],
                [0.953428, 0.527960, 0.288883, 1.0],
                [0.955470, 0.533093, 0.285490, 1.0],
                [0.957469, 0.538250, 0.282096, 1.0],
                [0.959424, 0.543431, 0.278701, 1.0],
                [0.961336, 0.548636, 0.275305, 1.0],
                [0.963203, 0.553865, 0.271909, 1.0],
                [0.965024, 0.559118, 0.268513, 1.0],
                [0.966798, 0.564396, 0.265118, 1.0],
                [0.968526, 0.569700, 0.261721, 1.0],
                [0.970205, 0.575028, 0.258325, 1.0],
                [0.971835, 0.580382, 0.254931, 1.0],
                [0.973416, 0.585761, 0.251540, 1.0],
                [0.974947, 0.591165, 0.248151, 1.0],
                [0.976428, 0.596595, 0.244767, 1.0],
                [0.977856, 0.602051, 0.241387, 1.0],
                [0.979233, 0.607532, 0.238013, 1.0],
                [0.980556, 0.613039, 0.234646, 1.0],
                [0.981826, 0.618572, 0.231287, 1.0],
                [0.983041, 0.624131, 0.227937, 1.0],
                [0.984199, 0.629718, 0.224595, 1.0],
                [0.985301, 0.635330, 0.221265, 1.0],
                [0.986345, 0.640969, 0.217948, 1.0],
                [0.987332, 0.646633, 0.214648, 1.0],
                [0.988260, 0.652325, 0.211364, 1.0],
                [0.989128, 0.658043, 0.208100, 1.0],
                [0.989935, 0.663787, 0.204859, 1.0],
                [0.990681, 0.669558, 0.201642, 1.0],
                [0.991365, 0.675355, 0.198453, 1.0],
                [0.991985, 0.681179, 0.195295, 1.0],
                [0.992541, 0.687030, 0.192170, 1.0],
                [0.993032, 0.692907, 0.189084, 1.0],
                [0.993456, 0.698810, 0.186041, 1.0],
                [0.993814, 0.704741, 0.183043, 1.0],
                [0.994103, 0.710698, 0.180097, 1.0],
                [0.994324, 0.716681, 0.177208, 1.0],
                [0.994474, 0.722691, 0.174381, 1.0],
                [0.994553, 0.728728, 0.171622, 1.0],
                [0.994561, 0.734791, 0.168938, 1.0],
                [0.994495, 0.740880, 0.166335, 1.0],
                [0.994355, 0.746995, 0.163821, 1.0],
                [0.994141, 0.753137, 0.161404, 1.0],
                [0.993851, 0.759304, 0.159092, 1.0],
                [0.993482, 0.765499, 0.156891, 1.0],
                [0.993033, 0.771720, 0.154808, 1.0],
                [0.992505, 0.777967, 0.152855, 1.0],
                [0.991897, 0.784239, 0.151042, 1.0],
                [0.991209, 0.790537, 0.149377, 1.0],
                [0.990439, 0.796859, 0.147870, 1.0],
                [0.989587, 0.803205, 0.146529, 1.0],
                [0.988648, 0.809579, 0.145357, 1.0],
                [0.987621, 0.815978, 0.144363, 1.0],
                [0.986509, 0.822401, 0.143557, 1.0],
                [0.985314, 0.828846, 0.142945, 1.0],
                [0.984031, 0.835315, 0.142528, 1.0],
                [0.982653, 0.841812, 0.142303, 1.0],
                [0.981190, 0.848329, 0.142279, 1.0],
                [0.979644, 0.854866, 0.142453, 1.0],
                [0.977995, 0.861432, 0.142808, 1.0],
                [0.976265, 0.868016, 0.143351, 1.0],
                [0.974443, 0.874622, 0.144061, 1.0],
                [0.972530, 0.881250, 0.144923, 1.0],
                [0.970533, 0.887896, 0.145919, 1.0],
                [0.968443, 0.894564, 0.147014, 1.0],
                [0.966271, 0.901249, 0.148180, 1.0],
                [0.964021, 0.907950, 0.149370, 1.0],
                [0.961681, 0.914672, 0.150520, 1.0],
                [0.959276, 0.921407, 0.151566, 1.0],
                [0.956808, 0.928152, 0.152409, 1.0],
                [0.954287, 0.934908, 0.152921, 1.0],
                [0.951726, 0.941671, 0.152925, 1.0],
                [0.949151, 0.948435, 0.152178, 1.0],
                [0.946602, 0.955190, 0.150328, 1.0],
                [0.944152, 0.961916, 0.146861, 1.0],
                [0.941896, 0.968590, 0.140956, 1.0],
                [0.940015, 0.975158, 0.131326, 1.0]]

	# colormap for the new viridis 
	viridis_data = [[0.267004, 0.004874, 0.329415, 1.0],
                 [0.268510, 0.009605, 0.335427, 1.0],
                 [0.269944, 0.014625, 0.341379, 1.0],
                 [0.271305, 0.019942, 0.347269, 1.0],
                 [0.272594, 0.025563, 0.353093, 1.0],
                 [0.273809, 0.031497, 0.358853, 1.0],
                 [0.274952, 0.037752, 0.364543, 1.0],
                 [0.276022, 0.044167, 0.370164, 1.0],
                 [0.277018, 0.050344, 0.375715, 1.0],
                 [0.277941, 0.056324, 0.381191, 1.0],
                 [0.278791, 0.062145, 0.386592, 1.0],
                 [0.279566, 0.067836, 0.391917, 1.0],
                 [0.280267, 0.073417, 0.397163, 1.0],
                 [0.280894, 0.078907, 0.402329, 1.0],
                 [0.281446, 0.084320, 0.407414, 1.0],
                 [0.281924, 0.089666, 0.412415, 1.0],
                 [0.282327, 0.094955, 0.417331, 1.0],
                 [0.282656, 0.100196, 0.422160, 1.0],
                 [0.282910, 0.105393, 0.426902, 1.0],
                 [0.283091, 0.110553, 0.431554, 1.0],
                 [0.283197, 0.115680, 0.436115, 1.0],
                 [0.283229, 0.120777, 0.440584, 1.0],
                 [0.283187, 0.125848, 0.444960, 1.0],
                 [0.283072, 0.130895, 0.449241, 1.0],
                 [0.282884, 0.135920, 0.453427, 1.0],
                 [0.282623, 0.140926, 0.457517, 1.0],
                 [0.282290, 0.145912, 0.461510, 1.0],
                 [0.281887, 0.150881, 0.465405, 1.0],
                 [0.281412, 0.155834, 0.469201, 1.0],
                 [0.280868, 0.160771, 0.472899, 1.0],
                 [0.280255, 0.165693, 0.476498, 1.0],
                 [0.279574, 0.170599, 0.479997, 1.0],
                 [0.278826, 0.175490, 0.483397, 1.0],
                 [0.278012, 0.180367, 0.486697, 1.0],
                 [0.277134, 0.185228, 0.489898, 1.0],
                 [0.276194, 0.190074, 0.493001, 1.0],
                 [0.275191, 0.194905, 0.496005, 1.0],
                 [0.274128, 0.199721, 0.498911, 1.0],
                 [0.273006, 0.204520, 0.501721, 1.0],
                 [0.271828, 0.209303, 0.504434, 1.0],
                 [0.270595, 0.214069, 0.507052, 1.0],
                 [0.269308, 0.218818, 0.509577, 1.0],
                 [0.267968, 0.223549, 0.512008, 1.0],
                 [0.266580, 0.228262, 0.514349, 1.0],
                 [0.265145, 0.232956, 0.516599, 1.0],
                 [0.263663, 0.237631, 0.518762, 1.0],
                 [0.262138, 0.242286, 0.520837, 1.0],
                 [0.260571, 0.246922, 0.522828, 1.0],
                 [0.258965, 0.251537, 0.524736, 1.0],
                 [0.257322, 0.256130, 0.526563, 1.0],
                 [0.255645, 0.260703, 0.528312, 1.0],
                 [0.253935, 0.265254, 0.529983, 1.0],
                 [0.252194, 0.269783, 0.531579, 1.0],
                 [0.250425, 0.274290, 0.533103, 1.0],
                 [0.248629, 0.278775, 0.534556, 1.0],
                 [0.246811, 0.283237, 0.535941, 1.0],
                 [0.244972, 0.287675, 0.537260, 1.0],
                 [0.243113, 0.292092, 0.538516, 1.0],
                 [0.241237, 0.296485, 0.539709, 1.0],
                 [0.239346, 0.300855, 0.540844, 1.0],
                 [0.237441, 0.305202, 0.541921, 1.0],
                 [0.235526, 0.309527, 0.542944, 1.0],
                 [0.233603, 0.313828, 0.543914, 1.0],
                 [0.231674, 0.318106, 0.544834, 1.0],
                 [0.229739, 0.322361, 0.545706, 1.0],
                 [0.227802, 0.326594, 0.546532, 1.0],
                 [0.225863, 0.330805, 0.547314, 1.0],
                 [0.223925, 0.334994, 0.548053, 1.0],
                 [0.221989, 0.339161, 0.548752, 1.0],
                 [0.220057, 0.343307, 0.549413, 1.0],
                 [0.218130, 0.347432, 0.550038, 1.0],
                 [0.216210, 0.351535, 0.550627, 1.0],
                 [0.214298, 0.355619, 0.551184, 1.0],
                 [0.212395, 0.359683, 0.551710, 1.0],
                 [0.210503, 0.363727, 0.552206, 1.0],
                 [0.208623, 0.367752, 0.552675, 1.0],
                 [0.206756, 0.371758, 0.553117, 1.0],
                 [0.204903, 0.375746, 0.553533, 1.0],
                 [0.203063, 0.379716, 0.553925, 1.0],
                 [0.201239, 0.383670, 0.554294, 1.0],
                 [0.199430, 0.387607, 0.554642, 1.0],
                 [0.197636, 0.391528, 0.554969, 1.0],
                 [0.195860, 0.395433, 0.555276, 1.0],
                 [0.194100, 0.399323, 0.555565, 1.0],
                 [0.192357, 0.403199, 0.555836, 1.0],
                 [0.190631, 0.407061, 0.556089, 1.0],
                 [0.188923, 0.410910, 0.556326, 1.0],
                 [0.187231, 0.414746, 0.556547, 1.0],
                 [0.185556, 0.418570, 0.556753, 1.0],
                 [0.183898, 0.422383, 0.556944, 1.0],
                 [0.182256, 0.426184, 0.557120, 1.0],
                 [0.180629, 0.429975, 0.557282, 1.0],
                 [0.179019, 0.433756, 0.557430, 1.0],
                 [0.177423, 0.437527, 0.557565, 1.0],
                 [0.175841, 0.441290, 0.557685, 1.0],
                 [0.174274, 0.445044, 0.557792, 1.0],
                 [0.172719, 0.448791, 0.557885, 1.0],
                 [0.171176, 0.452530, 0.557965, 1.0],
                 [0.169646, 0.456262, 0.558030, 1.0],
                 [0.168126, 0.459988, 0.558082, 1.0],
                 [0.166617, 0.463708, 0.558119, 1.0],
                 [0.165117, 0.467423, 0.558141, 1.0],
                 [0.163625, 0.471133, 0.558148, 1.0],
                 [0.162142, 0.474838, 0.558140, 1.0],
                 [0.160665, 0.478540, 0.558115, 1.0],
                 [0.159194, 0.482237, 0.558073, 1.0],
                 [0.157729, 0.485932, 0.558013, 1.0],
                 [0.156270, 0.489624, 0.557936, 1.0],
                 [0.154815, 0.493313, 0.557840, 1.0],
                 [0.153364, 0.497000, 0.557724, 1.0],
                 [0.151918, 0.500685, 0.557587, 1.0],
                 [0.150476, 0.504369, 0.557430, 1.0],
                 [0.149039, 0.508051, 0.557250, 1.0],
                 [0.147607, 0.511733, 0.557049, 1.0],
                 [0.146180, 0.515413, 0.556823, 1.0],
                 [0.144759, 0.519093, 0.556572, 1.0],
                 [0.143343, 0.522773, 0.556295, 1.0],
                 [0.141935, 0.526453, 0.555991, 1.0],
                 [0.140536, 0.530132, 0.555659, 1.0],
                 [0.139147, 0.533812, 0.555298, 1.0],
                 [0.137770, 0.537492, 0.554906, 1.0],
                 [0.136408, 0.541173, 0.554483, 1.0],
                 [0.135066, 0.544853, 0.554029, 1.0],
                 [0.133743, 0.548535, 0.553541, 1.0],
                 [0.132444, 0.552216, 0.553018, 1.0],
                 [0.131172, 0.555899, 0.552459, 1.0],
                 [0.129933, 0.559582, 0.551864, 1.0],
                 [0.128729, 0.563265, 0.551229, 1.0],
                 [0.127568, 0.566949, 0.550556, 1.0],
                 [0.126453, 0.570633, 0.549841, 1.0],
                 [0.125394, 0.574318, 0.549086, 1.0],
                 [0.124395, 0.578002, 0.548287, 1.0],
                 [0.123463, 0.581687, 0.547445, 1.0],
                 [0.122606, 0.585371, 0.546557, 1.0],
                 [0.121831, 0.589055, 0.545623, 1.0],
                 [0.121148, 0.592739, 0.544641, 1.0],
                 [0.120565, 0.596422, 0.543611, 1.0],
                 [0.120092, 0.600104, 0.542530, 1.0],
                 [0.119738, 0.603785, 0.541400, 1.0],
                 [0.119512, 0.607464, 0.540218, 1.0],
                 [0.119423, 0.611141, 0.538982, 1.0],
                 [0.119483, 0.614817, 0.537692, 1.0],
                 [0.119699, 0.618490, 0.536347, 1.0],
                 [0.120081, 0.622161, 0.534946, 1.0],
                 [0.120638, 0.625828, 0.533488, 1.0],
                 [0.121380, 0.629492, 0.531973, 1.0],
                 [0.122312, 0.633153, 0.530398, 1.0],
                 [0.123444, 0.636809, 0.528763, 1.0],
                 [0.124780, 0.640461, 0.527068, 1.0],
                 [0.126326, 0.644107, 0.525311, 1.0],
                 [0.128087, 0.647749, 0.523491, 1.0],
                 [0.130067, 0.651384, 0.521608, 1.0],
                 [0.132268, 0.655014, 0.519661, 1.0],
                 [0.134692, 0.658636, 0.517649, 1.0],
                 [0.137339, 0.662252, 0.515571, 1.0],
                 [0.140210, 0.665859, 0.513427, 1.0],
                 [0.143303, 0.669459, 0.511215, 1.0],
                 [0.146616, 0.673050, 0.508936, 1.0],
                 [0.150148, 0.676631, 0.506589, 1.0],
                 [0.153894, 0.680203, 0.504172, 1.0],
                 [0.157851, 0.683765, 0.501686, 1.0],
                 [0.162016, 0.687316, 0.499129, 1.0],
                 [0.166383, 0.690856, 0.496502, 1.0],
                 [0.170948, 0.694384, 0.493803, 1.0],
                 [0.175707, 0.697900, 0.491033, 1.0],
                 [0.180653, 0.701402, 0.488189, 1.0],
                 [0.185783, 0.704891, 0.485273, 1.0],
                 [0.191090, 0.708366, 0.482284, 1.0],
                 [0.196571, 0.711827, 0.479221, 1.0],
                 [0.202219, 0.715272, 0.476084, 1.0],
                 [0.208030, 0.718701, 0.472873, 1.0],
                 [0.214000, 0.722114, 0.469588, 1.0],
                 [0.220124, 0.725509, 0.466226, 1.0],
                 [0.226397, 0.728888, 0.462789, 1.0],
                 [0.232815, 0.732247, 0.459277, 1.0],
                 [0.239374, 0.735588, 0.455688, 1.0],
                 [0.246070, 0.738910, 0.452024, 1.0],
                 [0.252899, 0.742211, 0.448284, 1.0],
                 [0.259857, 0.745492, 0.444467, 1.0],
                 [0.266941, 0.748751, 0.440573, 1.0],
                 [0.274149, 0.751988, 0.436601, 1.0],
                 [0.281477, 0.755203, 0.432552, 1.0],
                 [0.288921, 0.758394, 0.428426, 1.0],
                 [0.296479, 0.761561, 0.424223, 1.0],
                 [0.304148, 0.764704, 0.419943, 1.0],
                 [0.311925, 0.767822, 0.415586, 1.0],
                 [0.319809, 0.770914, 0.411152, 1.0],
                 [0.327796, 0.773980, 0.406640, 1.0],
                 [0.335885, 0.777018, 0.402049, 1.0],
                 [0.344074, 0.780029, 0.397381, 1.0],
                 [0.352360, 0.783011, 0.392636, 1.0],
                 [0.360741, 0.785964, 0.387814, 1.0],
                 [0.369214, 0.788888, 0.382914, 1.0],
                 [0.377779, 0.791781, 0.377939, 1.0],
                 [0.386433, 0.794644, 0.372886, 1.0],
                 [0.395174, 0.797475, 0.367757, 1.0],
                 [0.404001, 0.800275, 0.362552, 1.0],
                 [0.412913, 0.803041, 0.357269, 1.0],
                 [0.421908, 0.805774, 0.351910, 1.0],
                 [0.430983, 0.808473, 0.346476, 1.0],
                 [0.440137, 0.811138, 0.340967, 1.0],
                 [0.449368, 0.813768, 0.335384, 1.0],
                 [0.458674, 0.816363, 0.329727, 1.0],
                 [0.468053, 0.818921, 0.323998, 1.0],
                 [0.477504, 0.821444, 0.318195, 1.0],
                 [0.487026, 0.823929, 0.312321, 1.0],
                 [0.496615, 0.826376, 0.306377, 1.0],
                 [0.506271, 0.828786, 0.300362, 1.0],
                 [0.515992, 0.831158, 0.294279, 1.0],
                 [0.525776, 0.833491, 0.288127, 1.0],
                 [0.535621, 0.835785, 0.281908, 1.0],
                 [0.545524, 0.838039, 0.275626, 1.0],
                 [0.555484, 0.840254, 0.269281, 1.0],
                 [0.565498, 0.842430, 0.262877, 1.0],
                 [0.575563, 0.844566, 0.256415, 1.0],
                 [0.585678, 0.846661, 0.249897, 1.0],
                 [0.595839, 0.848717, 0.243329, 1.0],
                 [0.606045, 0.850733, 0.236712, 1.0],
                 [0.616293, 0.852709, 0.230052, 1.0],
                 [0.626579, 0.854645, 0.223353, 1.0],
                 [0.636902, 0.856542, 0.216620, 1.0],
                 [0.647257, 0.858400, 0.209861, 1.0],
                 [0.657642, 0.860219, 0.203082, 1.0],
                 [0.668054, 0.861999, 0.196293, 1.0],
                 [0.678489, 0.863742, 0.189503, 1.0],
                 [0.688944, 0.865448, 0.182725, 1.0],
                 [0.699415, 0.867117, 0.175971, 1.0],
                 [0.709898, 0.868751, 0.169257, 1.0],
                 [0.720391, 0.870350, 0.162603, 1.0],
                 [0.730889, 0.871916, 0.156029, 1.0],
                 [0.741388, 0.873449, 0.149561, 1.0],
                 [0.751884, 0.874951, 0.143228, 1.0],
                 [0.762373, 0.876424, 0.137064, 1.0],
                 [0.772852, 0.877868, 0.131109, 1.0],
                 [0.783315, 0.879285, 0.125405, 1.0],
                 [0.793760, 0.880678, 0.120005, 1.0],
                 [0.804182, 0.882046, 0.114965, 1.0],
                 [0.814576, 0.883393, 0.110347, 1.0],
                 [0.824940, 0.884720, 0.106217, 1.0],
                 [0.835270, 0.886029, 0.102646, 1.0],
                 [0.845561, 0.887322, 0.099702, 1.0],
                 [0.855810, 0.888601, 0.097452, 1.0],
                 [0.866013, 0.889868, 0.095953, 1.0],
                 [0.876168, 0.891125, 0.095250, 1.0],
                 [0.886271, 0.892374, 0.095374, 1.0],
                 [0.896320, 0.893616, 0.096335, 1.0],
                 [0.906311, 0.894855, 0.098125, 1.0],
                 [0.916242, 0.896091, 0.100717, 1.0],
                 [0.926106, 0.897330, 0.104071, 1.0],
                 [0.935904, 0.898570, 0.108131, 1.0],
                 [0.945636, 0.899815, 0.112838, 1.0],
                 [0.955300, 0.901065, 0.118128, 1.0],
                 [0.964894, 0.902323, 0.123941, 1.0],
                 [0.974417, 0.903590, 0.130215, 1.0],
                 [0.983868, 0.904867, 0.136897, 1.0],
                 [0.993248, 0.906157, 0.143936, 1.0]]

 	cmap_256 = np.array(viridis_data) * 255

	src, data = getNiftiAsScalarField(vol_file)

	iso = mlab.pipeline.iso_surface(src, opacity=0.2, contours=10, vmin=0, vmax=1.0)
	iso.module_manager.scalar_lut_manager.lut.table = cmap_256

	if show_label==1:
		mlab.colorbar(object=iso, nb_labels=10, nb_colors=10, orientation='vertical')


	if plane_orientation=='z_axes':
		mlab.gcf().scene.camera.parallel_projection=True
		mlab.view(azimuth=0, elevation=180, distance='auto', focalpoint='auto')		
	elif plane_orientation=='x_axes':
		mlab.gcf().scene.camera.parallel_projection=True
		mlab.view(azimuth=180, elevation=90, distance='auto', focalpoint='auto')		
	elif plane_orientation=='y_axes':
		mlab.gcf().scene.camera.parallel_projection=True
		mlab.view(azimuth=90, elevation=90, distance='auto', focalpoint='auto')		
	else:
		mlab.gcf().scene.isometric_view()


	if bg_file != '':
		mrsrc, data = getNiftiAsScalarField(bg_file)
		orie = plane_orientation
		if plane_orientation=='iso':
			orie = 'z_axes'

		# from scipy import stats
		# data = stats.threshold(data, threshmin=0.5, threshmax=1, newval=0)			
		# print data.shape

		from scipy.ndimage.measurements import center_of_mass, maximum_position
		com = maximum_position(data)
		print '# max pos = ',com
		if auto_slice:
			if orie=='x_axes':
				slice_index = com[0]
			elif orie=='y_axes':
				slice_index = com[1]			
			elif orie=='z_axes':
				slice_index = com[2]
			else:
				slice_index = com[2]					

		opacity=0.5
		slice_index = int(slice_index)
		# auto flip z-index to below center
		# if plane_orientation=='iso':
		# 	opacity=0.5
		# 	center = data.shape[2]/2
		# 	if slice_index > center:
		# 		d = abs(center-slice_index)
		# 		slice_index = center-d
		# 	slice_index = com[2]

		mlab.pipeline.image_plane_widget(mrsrc, opacity=opacity, plane_orientation=orie, slice_index=int(slice_index), colormap='black-white', line_width=0, reset_zoom=False)

		if show_outline:
			mlab.outline()


	




	if save_fig:
		mlab.savefig(save_fig)
		if force_show_fig:
			mlab.show()
		else:
			mlab.close()

	else:
		mlab.show()		




if __name__ == '__main__':
    parser = OptionParser(usage="Usage: %prog [options] <subject_dir>")
    parser.add_option("-b", "--background", dest="bg", default='', help="Background MRI volume to draw")
    parser.add_option("-o", "--output", dest="output", default=None, help="Figure image to save as output")
    parser.add_option("-l", "--show_label", dest="show_label", default=1, type='int', help="Show label")
    parser.add_option("-s", "--slice_index", dest="slice_index", default=0, help="Slicing index")
    parser.add_option("-r", "--orientation", dest="orientation", default='z_axes', help="Initial view orientation. (x_axes, y_axes, z_axes)")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(2)
    else:
		run(options, args)
