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

<h2>Want to run the code? Here are the instructions.</h2>
<h3>Get the data</h3>
<p align="center">
  <img src="https://img.shields.io/badge/wip-%20%F0%9F%9A%A7%20under%20construction%20%F0%9F%9A%A7-yellow"
       alt="wip">
</p>
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
       abstract = {Using a 3D general circulation model, we demonstrate that a confirmed rocky exoplanet and a primary observational target, TRAPPIST-1e presents an interesting case of climate bistability. We find that the atmospheric circulation on TRAPPIST-1e can exist in two distinct regimes for a 1~bar nitrogen-dominated atmosphere. One is characterized by a single strong equatorial prograde jet and a large day-night temperature difference; the other is characterized by a pair of mid-latitude prograde jets and a relatively small day-night contrast. The circulation regime appears to be highly sensitive to the model setup, including initial and surface boundary conditions, as well as physical parameterizations of convection and cloud radiative effects. We focus on the emergence of the atmospheric circulation during the early stages of simulations and show that the regime bistability is associated with a delicate balance between the zonally asymmetric heating, mean overturning circulation, and mid-latitude baroclinic instability. The relative strength of these processes places the GCM simulations on different branches of the evolution of atmospheric dynamics. The resulting steady states of the two regimes have consistent differences in the amount of water content and clouds, affecting the water absorption bands as well as the continuum level in the transmission spectrum, although they are too small to be detected with current technology. Nevertheless, this regime bistability affects the surface temperature, especially on the night side of the planet, and presents an interesting case for understanding atmospheric dynamics and highlights uncertainty in 3D GCM results, motivating more multi-model studies.},
       author = {Denis E. Sergeev and Neil T. Lewis and F. Hugo Lambert and Nathan J. Mayne and Ian A. Boutle and James Manners and Krisztian Kohary},
       doi = {10.48550/arxiv.2207.12342},
       isbn = {2207.12342v1},
       month = {7},
       title = {Bistability of the atmospheric circulation on TRAPPIST-1e},
       url = {https://arxiv.org/abs/2207.12342v1},
       year = {2022},
    }

