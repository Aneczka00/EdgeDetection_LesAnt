# Data Preparation and Characteristics

To prepare the raw free-air anomaly (FAA) satellite-derived datasets (downloaded from [source](https://topex.ucsd.edu/pub/global_grav_1min_SWOT/)) and the available shipborne datasets for further processing and Bouguer anomaly computation, multiple notebooks were used.

## General Approach

The process included numerous steps:

1. **Installing all necessary libraries.**

2. **Loading the satellite and shipborne data.**
  
3. **Calculating the statistics of the difference between both datasets.**  

   3.1 ****
   
4. **Filtering.**

5. **Interpolation of the shipborne and satellite data.**

6. **Preparation of the bathymetry data ([GEBCO 2024](https://www.gebco.net/data-products/gridded-bathymetry-data)).**

7. **Complete Bouguer anomaly computations using Geosoft's Oasis Montaj software.**

<br>

**_Please note_:  
All additional files are relevant in one or another way to the project and are therefore kept for the sake of completeness !!**  
<br>

**[Notebook](exploratory_data_analysis.ipynb)**
