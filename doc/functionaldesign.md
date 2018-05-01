# Seattle Collision Research Tool

## Pre-dependencies
The user will interact with a jupyter notebook that displays greater Seattle maps 
with default construction and collision data visualized. In each of our use cases, 
jupyter interact widgets will allow the user to interact with our settings and 
update the map views. Maps will each have before, during, and after construction 
views of collision density at each new building site under the default (or selected) parameters.

The underlying databases required to update our maps will be created in our 
python package, and the processed data will be divided into 3 tables: Building.db, 
Collision.db, and Radius.db. For full details on the data sources and processed 
database structure, see [documentation file TBD]. 

## Use Cases
Key functionality: Enable users to view map of magnitude of collisions near new buildings in Seattle, before, during and after construction
Use cases: 
1. [Set Date Range](#1-use-case-set-date-range) 
2. [Toggle Permit Type](#2-use-case-toggle-permit-type) 
3. [Select Radius Size](#3-use-case-select-radius-size) 
4. [Toggle Accident Severity](#4-use-case-toggle-accident-severity)  
5. [Toggle Accident Type](#5-use-case-toggle-accident-type) (per/bike etc)

## 1. Use Case: Set Date Range
* **Name:** set_duration
* **What it does:** Allows user to adjust map view by setting construction window and duration range of collision data before and after construction.
* **Inputs:**
   - jupyter map view of before, during, and after construction with default duration settings
   - constr_start and constr_end from jupyter interactive slider
   - data_dur from jupyter interactive slider, the duration of collision data to be taken before and after construction 
   - Radius.db that has collision and building pairs within pre-determined radius of construction site by date, as well as start and end dates for each building construction
* **Outputs:** Adjusted map view in jupyter notebook that represents the selected time windows.
* **Pseudo code:**
   - Set constr_start and constr_end from jupyter input slider.
   - Calculate constr_dur, the duration of the construction task to be normalized.
   - Set before_start date as the constr_start minus the data_dur selected in the jupyter radio button.
   - Set after_end date as the constr_end plus the data_dur selected in the jupyter radio button.
   - Query all construction sites from the derived construction database that were started and completed within the (constr_start, constr_end) time frame. Set sites to display_sites.
   - Query the collision counts in the pre-defined radius for each site in display_sites in the following time frames:
     - before_ct: (before_start, constr_start)
     - during_ct: (constr_start, constr_end)
     - after_ct: (constr_end, after_end)
   - Normalize the during_ct so it reflects the same time period as before and after: 
     - during_ct_normalized = during_ct * constr_dur / data_dur
   - Update map display:
     - Display only construction sites in display_sites.
     - Use updated before_ct, during_ct_normalized, and after_ct for map data views.
     - Allow user to re-adjust jupyter settings and repeat process with new inputs.


## 2. Use Case: Toggle Permit Type
* **Name:** Toggle_permit_info
* **What it does:** Changes which permits to plot by letting user specify selection criteria
	Selection criteria could include: 
		* **Category** (e.g., single family, multi-family, commercial or industrial)
		* **Action Type** (e.g., new constructin, addition/alteration)
		* **Value:** The value of work to be conducted
		* **Status:** e.g., Permit issues, permit closed, certificate of occupancy authorized
		* **Permit type:** Construction, site development
* **Inputs:** 
	* Map of permits and collision
	* Field_selection (string)
	* Value selection (string, float or int depending on field selected e.g., if user selects "permit type" as their selected field, the value selection is a string, if the user selected value as thier field the value selection would be an int)
* **Outputs:** updated map based on field selection
* **Pseudo code:**
	* Field_selection = field selection identified in toggle
	* Value_selection = value selection identified in toggle
	* permits = read.csv(permit_data.csv)
	* temp_permits = filter permits where "selected_feild" == field selection
	* collision_count = CountCollisionsNearPermits(temp_permits, distance, collisions)
	* DrawMap(with inputs TBD)
	* PlotPermitSites(temp_permits, collision_count)
	* return updated map


#### Subcomponent 1: Draw map
* **Name:** DrawMap
* **What it does:** Draws a map of the specified region
* **Inputs:** ? Lat/Lon (floats) Coordinates of areas to be drawn - this may change as we learn more about which technology we will use to draw implement map drawing. 
* **Outputs:** Image showing map of specified region 
* **Pseudo code**
	* TBD depending on mapping package used


#### Subcomponent 2: Count collisions near permits
* **Name:** CountCollisionsNearPermits
* **What it does:** Counts how many collisions happened before, during and after construction of each permit
* **Inputs:** 
	* temp_permits: array of data for permits including floats representing permit lat/Lon coordinates, date object representing construction dates, 
	* distance: float, as radius from permit location to count collisions, 
	* temp_collisions: and array of data on permits including collision date (date objects) array of lat/lon coordinates (floats)
* **Outputs:** array of integers, representing number of collisions before, during and after construction for each permit
* **Pseudo code :**
    count_before = instantiate array of zeros to count collisions before construction
    count_during = instantiate array of zeros to count collisions during construction
    count_after = instantiate array of zeros to count collisions after construction
    counter = 0 
    
    for row in temp_permits: 
        Lat = row['Latitude']
        Lon = row['Longitude']
        dists = distance_formula( Lat, Lon, collisions['Latitude'], collisions['Longitude'])
        
        for j in range(0,len(dists)):
            if dists[j] > distance:
                continue
            else:
                if collisions_date[j] < row['Issue Date']:
                    count_before[i] += 1 
            elif (collision_date[j] > row['Issue Date']) and collision_date[j] < row['Final Date']:
                 count_during[i] += 1 
            elif collisions.incdate[j] > row['Final Date']:
                    count_after[i] += 1 
           
        counter += 1
    return count_before, count_during, count_after


#### Subcomponent 3: Plot permit/collision data on map
* **Name:** PlotPermitSites
* **What it does:** Plots permits on map
* **Inputs:** Lat/Lon (floats) for permit loaction, number (int) of accidents of specified type
* **Outputs:** Points plotted on map corresponding to location of coordinates and magnitude of accident volume
* **Pseudo code:**
	TBD depending on mapping software used

## 3. Use Case: Select Radius Size
* **Name:** select_radius_size
* **What it does:** Allows users to set a radius value that is used to filter the data and display a subset of the crashes attributed to buildings. 
* **Inputs:**
   - Radius value, that is specified by the user through a jupyter slider. There are three different values, small, medium and large.
   - 3 databases, Collisions, Building and Radius. Collisions contains a set of collisions and attributes, buildings contains info on buildings permits and radius contains building ids, collision ids and radius (distance between buildings and collision occurrences).
* **Outputs:** 
   - Jupyter map that displays the collisions that are within the selected radius, for each collision - building pairs
* **Pseudocode:**
   - Read the radius size that is set by the user.
      - The radius size is a string that specifies small, medium and large.
      - This radius size is converted into a number that is passed on to the query.
   - Generate a query in SQL that performs a search on the Radius DB
      - Take the returned size from the Jupyter slider.
      - Pass this query back to the SQL backend.
   - Execute the query on the Radius DB, and collect the returned results. 
      - Process the returned tuples and perform a computation that determines whether a point needs to be added or removed.
   - Perform an update of the map displays, so that they reflect

## 4. Use Case: Toggle Accident Severity
* **Name:** accident_severity
* **What it does:** Allows user to adjust map view by filtering based on the severity of the accident that occurred around where building permits are issued. The user will then be able to compare the severity of accidents within the proximity of building permits before, during, and after construction.  The severity classifications included in the Collisions dataset are Property Damage, Injury, Serious Injury, Fatality or Unknown.
* **Inputs:**
   - The user inputs the accident severity level they are interested in comparing. This could include one, all, or a subset of the accident severity codes associated with each collision.
   - The selected accident severity is used to filter the collisions database. The collision IDs are then fed into the Radius database that associates collisions with certain building permits.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected severity code. 
* **Pseudo code:**
   - Receive accident severity input levels selected by user via the interactive feature on the map
   - Using pandas, filter the Collisions database with the severity code column based on the user input. 
   - Take the resulting Collision ID column as a vector and filter the Radius database based on those collision IDs
   - Feed new data into map for automatic update.

## 5. Use Case: Toggle Accident Type
* **Name:** accident_type
* **What it does:** Allows user to adjust map view by filtering based on the type of accident that occurred around where building permits are issued. The user will then be able to compare the type of accidents within the proximity of building permits before, during, and after construction.  The classifications included whether the accident involved pedestrians, cyclists, or vehicle only. 
* **Inputs:**
   - The user inputs the accident type they are interested in comparing. This could include one, all, or a subset of the accident types that are used to classify each collision.
   - The selected accident type is used to filter the collisions database. The collision IDs are then fed into the Radius database that associates collisions with certain building permits.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected accident type
* **Pseudo code:**
   - Receive accident type selected by user via the interactive feature on the map[
   - Using pandas, filter the Collisions database with the accident type column based on the user input. 
   - Take the resulting Collision ID column as a vector and filter the Radius database based on those collision IDs
   - Feed new data into map for automatic update.
