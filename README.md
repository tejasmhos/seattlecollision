# Seattle Collision Research Tool
## Use Cases
Key functionality: Enable users to view map of magnitude of collisions near new buildings in Seattle, before, during and after construction
Use cases: 
1. Set Date Range 
2. Select Radius size 
3. Toggle accident type (per/bike etc) 
4. Toggle Permit Type 
5. Zoom ?

## Use Case: Duration Views

#### Name: 
set_duration

#### What it does: 
Allows user to adjust map view by setting construction window and duration range of collision data before and after construction.

#### Inputs:
 - jupyter map view of before, during, and after construction with default duration settings
 - constr_start and constr_end from jupyter interactive slider
 - collision_duration in months from jupyter interactive radio buttons (3, 6, 9, 12 months)
 - database derived from building permit and collision data that has collision counts within pre-determined radius of construction site by date, as well as start and end dates for all building construction

#### Outputs: 
Adjusted map view in jupyter notebook that represents the selected time windows.

#### Pseudo code:
 - Set constr_start and constr_end from jupyter input slider.
 - Calculate constr_dur, the duration of the construction task to be normalized.
 - Set before_start date as the constr_start minus the collision_duration selected in the jupyter radio button.
 - Set after_end date as the constr_end plus the collision_duration selected in the jupyter radio button.
 - Query all construction sites from the derived construction database that were started and completed within the (constr_start, constr_end) time frame. Set sites to display_sites.
 - Query the collision counts in the pre-defined radius for each site in display_sites in the following time frames:
   - before_ct: (before_start, constr_start)
   - during_ct: (constr_start, constr_end)
   - after_ct: (constr_end, after_end)
 - Normalize the during_ct so it reflects the same time period as before and after: 
   - during_ct_normalized = during_ct * constr_dur / collision_duration
 - Update map display:
   - Display only construction sites in display_sites.
   - Use updated before_ct, during_ct_normalized, and after_ct for map data views.
   - Allow user to re-adjust jupyter settings and repeat process with new inputs.




#### Component Specification
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


#### Subomponent 3: Plot permit/collision data on map
* **Name:** PlotPermitSites
* **What it does:** Plots permits on map
* **Inputs:** Lat/Lon (floats) for permit loaction, number (int) of accidents of specified type
* **Outputs:** Points plotted on map corresponding to location of coordinates and magnitude of accident volume
* **Pseudo code:**
	TBD depending on mapping software used

