# RCEMIP

** **This repository is currently being built** **

Python scripts are provided that were used for the analysis in the references listed below.

References
----------
**Stauffer, C.L.** and A.A. Wing (2022): Properties, Changes, and Controls of Deep-Convecting Clouds in Radiative-Convective Equilibrium, J. Adv. Model. Earth Syst., in review. 

Wing, A.A., **C.L. Stauffer**, T. Becker, K.A. Reed, M.-S. Ahn, N.P. Arnold, S. Bony, M. Branson, G.H. Bryan, J.-P. Chaboureau, S.R. de Roode, K. Gayatri, C. Hohenegger, I.-K. Hu, F. Jansson, T.R. Jones, M. Khairoutdinov, D. Kim, Z.K. Martin, S. Matsugishi, B. Medeiros, H. Miura, Y. Moon, S.K. Müller, T. Ohno, M. Popp, T. Prabhakaran, D. Randall, R. Rios-Berrios, N. Rochetin, R. Roehrig, D.M. Romps, J.H. Ruppert, Jr., M. Satoh, L.G. Silvers, M.S. Singh, B. Stevens, L. Tomassini, C.C. van Heerwaarden, S. Wang, and M. Zhao (2020): Clouds and convective self-aggregation in a multi-model ensemble of radiative-convective equilibrium simulations, J. Adv. Model. Earth Syst., 12, e2020MS002138, [doi:10.1029/2020MS002138](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020MS002138).

Input, Output, and Examples
----------

The below table has the lcoation of the input data, output data, and example usage of the script using Jupyter Notebook:

| Code | Input Data | Output Data | Example Usage |
|:-----|:-----------|:------------|:--------------|
| [cloudfraction.py](https://github.com/clstauffer/rcemip/tree/main/scripts/cloudfraction.py) | [DKRZ 3D model output](http://hdl.handle.net/21.14101/d4beee8e-6996-453e-bbd1-ff53b6874c0e) | [Cloud Fraction Profiles](https://github.com/clstauffer/rcemip/tree/main/data/) | [cloudfraction.ipynb](https://github.com/clstauffer/rcemip/tree/main/examples/cloudfraction.ipynb) |
| [conditionalstats.py](https://github.com/clstauffer/rcemip/tree/main/scripts/conditionalstats.py) | [DKRZ 3D model output](http://hdl.handle.net/21.14101/d4beee8e-6996-453e-bbd1-ff53b6874c0e) | [Conditional Statistics Profiles](https://github.com/clstauffer/rcemip/tree/main/data/) | [conditionalstats.ipynb](https://github.com/clstauffer/rcemip/tree/main/examples/) |
| [divergence.py](https://github.com/clstauffer/rcemip/tree/main/scripts/divergence.py) | [DKRZ 1D model output](http://hdl.handle.net/21.14101/d4beee8e-6996-453e-bbd1-ff53b6874c0e) | [Radiatively-Driven Divergence Profiles](https://github.com/clstauffer/rcemip/tree/main/data/) | [divergence.ipynb](https://github.com/clstauffer/rcemip/tree/main/examples/) |
| [midlevelscaling.py](https://github.com/clstauffer/rcemip/tree/main/scripts/midlevelscaling.py) | [Conditional Statistics](https://github.com/clstauffer/rcemip/tree/main/data/) and [Mid-level Scaling Profiles](https://github.com/clstauffer/rcemip/tree/main/data/) | [Mid-level Scaling Profiles](https://github.com/clstauffer/rcemip/tree/main/data/) | [midlevel.ipynb](https://github.com/clstauffer/rcemip/tree/main/examples/midlevel.ipynb) |

Figures
----------
Figures generated by the Notebooks are located in the [images directory](https://github.com/clstauffer/rcemip/tree/main/data/) and [Mid-level Scaling Profiles](https://github.com/clstauffer/rcemip/tree/main/images/).

Contact
----------
Please feel free to contact me at cls14b@fsu.edu if you have any questions, concerns, or suggestions related to the RCEMIP data and its implementation!
