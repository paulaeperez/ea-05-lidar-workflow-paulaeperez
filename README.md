# Assignment ea-05-lidar-workflow

Author: Paula Pérez

## Purpose of repo
This repository holds Assignment 5 for the Earth Analytics course at the CU Earth Lab. It contains a reproducible workflow to process and compare LiDAR and insitu tree height data from a canopy height model at two NEON sites:

1. [Soaproot Saddle (SOAP)](https://www.neonscience.org/field-sites/soap)
2. [San Joaquin Experimental Range (SJER)](https://www.neonscience.org/field-sites/sjer)

## Data sources
The workflow uses data from the earthpy package. The entire lidar and insitu data for the sites can be downloaded with:

```
earthpy.data.get_data('spatial-vector-lidar)
```

## Setup (env install)
The repo has the following dependencies:

- os
- pathlib
- earthpy
- pandas
- geopandas
- matplotlib.pyplot
- rasterstats
- seaborn

The entire conda environment can be configured by following [these steps](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/).