#path to folder that contains the mesa executable

mesa_root_dir = '/mnt/apps/prebuilt/MESA/r1039'
mesa_directory = '/mnt/scratch_a/users/c/csavvas/MESAslurm/Slurm/work'
out_directory = '/mnt/scratch_a/users/c/csavvas/gpu_tests'
script_directory = '/mnt/scratch_a/users/c/csavvas/MESAslurm'


#Can explore up to three variables

variable1 = {'name': 'initial_mass',
             'location': 'inlist_var',
             'type': 'array',
             'minimum': 2.5,
             'maximum': 2.5,
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
