# Data Preparation and Characteristics

To properly prepare raw free-air anomaly (FAA) datasets - satellite-derived (downloaded from [source](https://topex.ucsd.edu/pub/global_grav_1min_SWOT/)) and available shipborne - for further processing and Bouguer anomaly computation, multiple notebooks were used.

## General Approach

The process multiple steps:

1. **Installation of all necessary libraries**

2. **Loading the data - satellite + shipborne**
  
3. **Calulations of the statistics of the difference bertween both datasets**  

   3.1 **Encoding the data**

   3.2 **Rearrange**

   3.3 **Pivot the data (Column of CDR3s starts with C and ends with F)**

   3.4 **Transform data into a matrix**

   3.5 **Prepare CDR3 matrix for 34 patients**
   
4. **Filtering**

5. **Interpolation of the shipborne and satellite data**

6. **Preparation of the bathymetry data ([GEBCO 20204](https://www.gebco.net/data-products/gridded-bathymetry-data)**

7. **Complete Bouguer anomaly computations using Geosoft software (Oasis montaj)**

<br>

**_Please note_:  
All additional files are relevant in one or another way to the project and are therefore kept for the sake of completeness !!**  
<br>

**[Notebook](exploratory_data_analysis.ipynb)**
