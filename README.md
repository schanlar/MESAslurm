# MESAslurm
Scripts to submit jobs at [Slurm](https://slurm.schedmd.com/overview.html) cluster manager

## Download
You can download the repository as a zip file, or by typing

```bash
 ~$ git clone https://github.com/schanlar/MESAslurm.git
```

in a terminal window.

## Initialize and Run
**Step 0** : Open the template for the batch script that contains directives to submit jobs at Slurm manager.
You can edit the base options (e.g. number of nodes, cpus per task etc) depending on your needs.
**DO NOT** modify the batch script besides the directives that were meant
to be used with Slurm (the ones starting with ``#SBATCH``).

**Step 1** : Open ``config.py`` using the editor of your choice.

**Step 2** : Specify the paths for the ``MESA`` stellar evolution code (check their [site](http://mesa.sourceforge.net/)),
the output directory etc.

> Warning: You need to create a copy of the ``work`` directory used in MESA.
You also need to specify the absolute path to this copied version using the ``mesa_directory`` variable.

**Step 3** : Create your stellar grid. You can explore up to 3 variables at a time.

**Step 4** : Save your changes and the run the ``submit_jobs.py`` script.
