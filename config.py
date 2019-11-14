#path to folder that contains the mesa executable
#mesa_root_dir = '/vol/aibn1107/data2/schanlar/mesa-r10398'
#mesa_directory = '/vol/aibn1107/data2/schanlar/mesa-r10398/star/test_suite/Condor'
#out_directory= '/vol/hal/halraid/schanlar/Condor/HeZAMS'
#script_directory = '/vol/aibn1107/data2/schanlar/MESAcondor'

#mesa_root_dir = ''
mesa_directory = '/home/schanlar/MESAslurm/Condor'
out_directory = '/home/schanlar/test_output'
script_directory = '/home/schanlar/MESAslurm'


#Can explore up to three variables

variable1 = {'name': 'initial_mass',
             'location': 'inlist_var',
             'type': 'array',
             'minimum': 1.5,
             'maximum': 1.5,
             'step': 0.1,
}

variable2 = {'name': 'initial_z',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             #'values': [0.0001,0.001,0.02]
	'values': [0.02]
}

variable3 = {'name': 'wind_scaling_factor',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             #'values': [0.1, 0.5, 2.0, 10.0]
		'values': [1.0]
}
