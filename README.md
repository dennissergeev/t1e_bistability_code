<p align="center">
  <img src="https://img.shields.io/badge/wip-%20%F0%9F%9A%A7%20under%20construction%20%F0%9F%9A%A7-yellow"
       alt="wip">
</p>

<p align="center">
<a href="https://arxiv.org/abs/2207.12342">
<img src="https://img.shields.io/badge/arXiv-2207.12342-red"
     alt="arXiv preprint"></a>
<a href="https://www.python.org/downloads/">
<img src="https://img.shields.io/badge/python-3.10-blue.svg"
     alt="Python 3.9"></a>
<a href="LICENSE">
<img src="https://img.shields.io/badge/License-LGPL%20v3-green.svg"
     alt="License: LGPL v3"></a>
<a href="https://github.com/psf/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg"
     alt="black"></a>
</p>

<h1 align="center">
  Bistability of atmospheric circulation on TRAPPIST-1e
</h1>
<h3 align="center">
  Denis E. Sergeev, Neil T. Lewis, F. Hugo Lambert, Nathan J. Mayne, Ian A. Boutle, James Manners, and Krisztian Kohary
</h3>
<h4 align="center">
  Accepted for publication in Planetary Science Journal.
</h4>
<p align="center">
  Code for reproducing figures from the paper.
  Model data are available upon request (raw data O(100 Gb)).
</p>

<h2>What is in this repository?</h2>

Notebooks for each figure are in the [`code/` directory](code), while the figures themselves are in the `plots/` directory.

|  #  | Figure | Notebook |
|:---:|:-------|:---------|
|  1  | [Mean climate diagnostics](plots/ch111_mean/ch111_mean__all_sim__u_max_eq_jet_300hpa_jet_lat_free_trop_ratio_dn_ep_temp_diff_trop_t_sfc_min__u_temp_vcross.png) | [Fig01-Mean-Climate-Diagnostics-All-Experiments.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Fig01-Mean-Climate-Diagnostics-All-Experiments.ipynb) |
|  2  | [Emergence of superrotation](plots/ch111_spinup/ch111_spinup__base_sens-t280k__u_eq_jet_max_wave_amplitude_300hpa.png) | [Fig02-Spinup-Superrotation.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Fig02-Spinup-Superrotation.ipynb) |
|  3  | [First 200 days of heating rates, water vapor path, Eady Growth Rate](plots/ch111_spinup/ch111_spinup__base_sens-t280k__tseries__wvp_d_dt_sw_d_dt_lw_d_dt_cv_d_dt_diab_d_eady_growth__day000-200_mean.png) | [Fig03-Spinup-Heating-Rates.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Fig03-Spinup-Heating-Rates.ipynb) |
|  4  | [Angular momentum budget](plots/ch111_spinup/ch111_spinup__base_sens-t280k__ang_mom_bud_ang_mom_time_change__0-20_20-80_80-200_250-450__yprof.png) | [Fig04-Spinup-Momentum-Budget.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Fig04-Spinup-Momentum-Budget.ipynb) |
|  5  | [Water vapor and cloud radiative effects in night-side cold traps](plots/ch111_spinup/ch111_spinup__base_sens-t280k__wvp_cwp_wvre_lw_sfc_cre_lw_sfc_t_sfc__cold_traps.png) | [Fig05-Spinup-Cold-Traps-WVRE-CRE.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Fig05-Spinup-Cold-Traps-WVRE-CRE.ipynb) |
|  11 | [Transmission spectra](plots/) | [Transmission-Spectra.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/t1e_bistability_code/blob/main/code/Transmission-Spectra.ipynb) |


<h2>Want to run the code? Here are the instructions.</h2>

<h3>Get the data</h3>

Please email the lead author, [Denis E. Sergeev](https://dennissergeev.github.io), to get the data.

<h3>Set up Python environment</h3>

To recreate the required environment for running Python code, follow these steps. (Skip the first two steps if you have Jupyter Lab with `nb_conda_kernels` installed already.)
```bash
conda env create --file environment.yml
```
1. Install conda, e.g. using [mambaforge](https://github.com/conda-forge/miniforge#mambaforge)
2. Install necessary packages to the `base` environment. Make sure you are installing them from the `conda-forge` channel.
```bash
conda install -c conda-forge jupyterlab nb_conda_kernels
```
3. Git-clone or download this repository to your computer
4. In the command line, navigate to the downloaded folder, e.g.
```bash
cd /path/to/downloaded/t1e_bistability_code
```
5. Create a separate conda environment
```
mamba env create --file environment.yml
```
5. Run the notebooks manually or use `make` shortcuts (type `make help` for help)

<h3>Open the code</h3>

1. Start the Jupyter Lab, for example from the command line (from the `base` environment):
```bash
jupyter lab
```
2. Open noteboks in the `t1e_bistability` environment and start coding.

<h2>Bibtex entry</h2>

    @article{Sergeev22_bistability,
       author = {Denis E. Sergeev and Neil T. Lewis and F. Hugo Lambert and Nathan J. Mayne and Ian A. Boutle and James Manners and Krisztian Kohary},
       doi = {10.48550/arxiv.2207.12342},
       isbn = {2207.12342v1},
       month = {7},
       title = {Bistability of the atmospheric circulation on TRAPPIST-1e},
       url = {https://arxiv.org/abs/2207.12342v1},
       year = {2022},
    }

