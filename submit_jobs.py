from __future__ import print_function 
import numpy as np
import os

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


from config import *

grid_variables = [variable1,variable2,variable3]

def replace_line(file_path, old_line, new_line, new_file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(old_line, new_line))
    move(abs_path, new_file_path)


def modify_inlist_value(inlist,variable_name,value,inlist_out):

    if variable_name == 'wind_scaling_factor':
        replace_line(inlist, 'Dutch_scaling_factor', 'Dutch_scaling_factor = '+np.str(value), inlist_out)
    elif variable_name == 'initial_z':
        replace_line(inlist,'initial_z','initial_z = '+np.str(value),inlist_out)
        y = 1 - value 
        replace_line(inlist,'initial_y','initial_y = '+np.str(y),inlist_out)
        replace_line(inlist,'initial_he4','initial_he4 = '+np.str(y),inlist_out)
        replace_line(inlist,'Zbase','Zbase = '+np.str(value),inlist_out)
    else:
        replace_line(inlist,variable_name,variable_name + ' = ' + np.str(value),inlist_out) 


# Make grid of initial masses

for variable in grid_variables:
    if variable['type'] == 'array':
        variable['values'] = np.arange(variable['minimum'],
                                      variable['maximum']+variable['step'],
                                      variable['step'])



def main():
    for value1 in variable1['values']:
        for value2 in variable2['values']:
            for value3 in variable3['values']:
            	output_directory = "{:0.4f}_{:0.4f}_{:0.4f}".format(value1,value2,value3) # Format of output folder: mass_metallicity_wind



              	output_directory = os.path.join(out_directory,output_directory)
              	LOGS = os.path.join(output_directory,'LOGS')
              	photos = os.path.join(output_directory,'photos')

              	condor_job = os.path.join(output_directory,'condor.job')
              	run_mesa = os.path.join(output_directory,'run_mesa.sh')
              	inlist_project = os.path.join(output_directory,'inlist_project')
              	model_name = os.path.join(output_directory,'final_model.mod')
              	final_profile_name = os.path.join(output_directory,'final_profile.data')
            
              	if not os.path.exists(output_directory):
                	os.makedirs(output_directory)

			replace_line('templates/inlist_project.template', 
                   			   'save_model_filename', 
                             		   'save_model_filename = ' + '\''+model_name+'\'', 
                             		   inlist_project)

                	replace_line(inlist_project, 
                             'filename_for_profile_when_terminate', 
                             'filename_for_profile_when_terminate =' +  '\''+final_profile_name+ '\'', 
                             inlist_project)

                	replace_line(inlist_project, 
                             'log_directory', 
                             'log_directory = ' +  '\''+LOGS+'\'', 
                             inlist_project)

                	replace_line(inlist_project, 
                             'photo_directory', 
                             'photo_directory = ' +  '\''+photos+'\'', 
                             inlist_project)

                	modify_inlist_value(inlist_project,variable1['name'],value1,inlist_project)
                	modify_inlist_value(inlist_project,variable2['name'],value2,inlist_project)
                	modify_inlist_value(inlist_project,variable3['name'],value3,inlist_project)

			replace_line(os.path.join(script_directory, 'templates/run_mesa.sh.template'),
                                        '# SBATCH --job-name=run_mesa_template',
                                        "# SBATCH --job-name=run_mesa_" + "{:0.4f}_{:0.4f}_{:0.4f}".format(value1,value2,value3),
                                        run_mesa)

			replace_line(run_mesa,
                             'cp -r', 
                             'cp -r ' + os.path.join(mesa_directory,'*')+ ' '+output_directory,
                             run_mesa)

                	#replace_line(run_mesa,
                        #     './rn', 
                        #     os.path.join(output_directory,'*')+ 'star',
			#     'echo ./rn',
			#     run_mesa)


			os.system('chmod +x ' + run_mesa)
                	print('')
                	print('creating files in' + output_directory)
                	#os.system('cat '+ os.path.join(output_directory,'inlist_project')+ ' ' + '|grep log_directory')
                	print('')
			os.system('bash ' + run_mesa) # FOR DEBUGGING ONLY!
			#os.chdir(output_directory)
			#os.system('# sbatch run_mesa.sh')
			#os.chdir(script_directory)

if __name__ == '__main__':
	main()
