# Data Preparation and Characteristics

To prepare the raw free-air anomaly (FAA) satellite-derived datasets (downloaded from [source](https://topex.ucsd.edu/pub/global_grav_1min_SWOT/)) and the available shipborne datasets for further processing and Bouguer anomaly computation, multiple notebooks were used.

## General Approach

The process included numerous steps:

1. **Installing all necessary libraries.**

2. **Loading the satellite and shipborne data.**
  
3. **Calculating the statistics of the difference between both datasets.**  

   3.1 **Plotting spatial variations of the difference**
   
   3.2 **Basic statistics**
   
   3.3 **Comaprison with 2016/2017 satellite datasets.**
   
4. **Filtering.**

   4.1 **Removal of multiplied coordinates.**
   
   4.2 **Statistical removal of anomalous data.**
   
   4.3 **Removal of unnecessary OBS lines.**

5. **Interpolation of the shipborne and satellite data.**
   
   5.1 **First test on a smaller area.**
   
   5.2 **Interpolation of the whole area of interest**

6. **Preparation of the bathymetry data ([GEBCO 2024](https://www.gebco.net/data-products/gridded-bathymetry-data)).**

   6.1 **Interpolating bathymetry data onto a regular grid identical to gravity grid.**
   
   6.2 **Merging the GEBCO 2024 and shipborne data.**

7. **Complete Bouguer anomaly computations using Geosoft's Oasis Montaj software.**

   7.1 **Simple Bouguer anomaly.**
   
   7.2 **Topographic + Bullard correction.**

<br>

**[Notebook 1](M2_gravity.ipynb)** - shipborne vs satellite 2024  
**[Notebook 2](M2_2016_2017.ipynb)** - shipborne vs satellite 2016/2017  
**[Notebook 3](M2_gravity_filtering-with_OBS.ipynb)** - initial filtering  
**[Notebook 4](M2_gravity_filtering_no_OBS.ipynb)** - final filtering  
**[Notebook 5](bathy_interp_KDTree.py)** - Interpolating bathymetry using KDTree to speed up the proces
**[Notebook 6](projecting_bathy_on_gravi_grid.py)** - Projecting bathymetry on gravity grid
**[Notebook 7](projecting_bathy_on_gravi_grid.py)** - Adjusting bathymetry to a smaller grid


**_Additional codes related to the project:_**  
<br>

**[Notebook 1](earthquakes_depth_slab.py)** - Earthquakes at the depth slab
**[Notebook 2](earthquakes_depth_slab_3D.py)** - Creating a 3D plot (earthquakes + slab) 


