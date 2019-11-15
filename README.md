# MESAslurm
Scripts to submit jobs at [Slurm](https://slurm.schedmd.com/overview.html) cluster manager

## Download
You can download the repository as a zip file, or by typing

```bash
 ~$ git clone https://github.com/schanlar/MESAslurm.git
```

in a terminal window.

## Initialize and Run
**Step 0** : Open the template for the batch script required to submit jobs at Slurm.
You can change the directives depending on your needs (e.g. number of nodes, cpus per task etc).
**DO NOT** modify the script besides the directives that are meant to be used with Slurm (the ones starting with ``#SBATCH``).

**Step 1** : Open ``config.py`` using the editor of your choice.

**Step 2** : Specify the paths for the ``MESA`` stellar evolution code (check their [site](http://mesa.sourceforge.net/)),
the output directory etc.

> Warning: You need to create a copy of the ``work`` directory used in MESA.
You also need to specify the absolute path to this copied version using the ``mesa_directory`` variable.

**Step 3** : Create your stellar grid. You can explore up to 3 variables at a time.

**Step 4** : Save your changes and the run the ``submit_jobs.py`` script.
