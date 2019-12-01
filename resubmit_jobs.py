from __future__ import print_function
import re
import os
import glob
from file_read_backwards import FileReadBackwards

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


OutputPath = '/mnt/scratch_a/users/c/csavvas/He_stars_grid/gpu_partition/z0p1_eta1p0'


def replace_line(file_path, old_line, new_line, new_file_path):
    #Create temp file
	fh, abs_path = mkstemp()
	with fdopen(fh,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(old_line, new_line))
	move(abs_path, new_file_path)


def searchOutput(path):
    '''
    Search the terminal log file for the last saved model
    '''

    with FileReadBackwards(path +'/terminal_log') as file:
        for line in file:
            if line.startswith('save ' + path + '/photos/'):
                words = re.split('/|, | ', line)
                if words[-2] == 'photos':
                    break
    return words[-1]


def createBatchScript(path):
    '''
    Create the template for resubmitting jobs to Slurm
    '''

    os.chdir(path)
    os.system('touch restart_job.sh')

    os.system('echo ' + '\#\!/bin/bash >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --job-name=restart_mesa_template >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --output=job_output.stdout >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --error=job_error.stderr >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --partition=gpu >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --nodes=1 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --ntasks-per-node=1 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --cpus-per-task=10 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --time=01-00:00:00 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --mail-type=FAIL >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --mail-user=schanlar@physics.auth.gr >> restart_job.sh')

    os.system('echo ' + 'export OMP_NUM_THREADS=\$\SLURM_CPUS_PER_TASK >> restart_job.sh')
    os.system('echo ' + 'module rm gcc python >> restart_job.sh')
    os.system('echo ' + 'module load MESA >> restart_job.sh')
    os.system('echo ' + 'source \$\MESASDK_ROOT/bin/mesasdk_init.sh >> restart_job.sh')
    os.system('echo ' + './re >> restart_job.sh')


def restartMesa(path, photo):
    '''
    Modify the template for the batch script
    '''

    os.chdir(path)

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --job-name=restart_mesa_template',
            '#SBATCH --job-name=rMESAjob',
            os.path.join(path, 'restart_job.sh'))

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --output=job_output.stdout',
            '#SBATCH --output=restarted_job_output.stdout',
            os.path.join(path, 'restart_job.sh'))

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --error=job_error.stderr',
            '#SBATCH --error=restarted_job_error.stderr',
            os.path.join(path, 'restart_job.sh'))
    
    replace_line(os.path.join(path, 'restart_job.sh'), 
            './re',
            './re ' + photo,
            os.path.join(path, 'restart_job.sh'))

    os.system('chmod +x ' + os.path.join(path, 'restart_job.sh'))
    os.system('sbatch restart_job.sh')
    #print('sbatch restart_job.sh')






def main():

    for path in glob.glob(OutputPath +'/*'):
        reachedTimeWall = False
        # Check if a stderr file exists
        for f in glob.glob(path + '/*_error.stderr'):
            with open(f) as error_file:
                keywords = ['DUE', 'TO', 'TIME', 'LIMIT']
                # Check if the model stopped due to time limit
                for line in error_file:
                    if line.startswith('slurmstepd: error:'):
                        words = re.split('-|, |\n, | ', line)
                        for key in keywords:
                            if key in words:
                                # Restart the model if it has stopped
                                # due to a specified time wall
                                # For the gpu partition --> max run time == 1 day
                                reachedTimeWall = True 
                            else:
                                reachedTimeWall = False

        if reachedTimeWall:
            photo = searchOutput(path)
            #createBatchScript(path)
            #restartMesa(path, photo)
            print(f'Restart photo {photo} from path {path}')
                                



if __name__ == "__main__":
    main()
