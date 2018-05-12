# Seattle Collision Research Tool

## Pre-dependencies
The user will interact with a jupyter notebook that displays greater Seattle maps 
with default construction and collision data visualized. In each of our use cases, 
jupyter interact widgets will allow the user to interact with our settings and 
update the map views. Maps will each have before, during, and after construction 
views of collision density at each new building site under the default (or selected) parameters.

The underlying databases required to update our maps will be created in our 
python package, and the processed data will be divided into 3 tables: Building, 
Collision and Radius. The Building table contains information about the dates of construction, the type and permit number as a key. The Collisions table contains information about specific collisions, such as the date location and severity. Finally the Radius table contains the building id, collision id and a radius value. This table is important to select buildings given a radius size.

## Targeted user
**Urban planner:** An urban planner could use this tool to visulaize the impact of construction and increased density on the rate traffic collisions. This could be used to identify potential problem areas that result from construction (e.g., pedestrian collisions tend to increase during construction, or parked car collisions tend to increase after construction). These insights could inform urban planning decisions for future building sites. We assume the urban planner is familiar with these data sets and the definitions of fields. He or she may not be familiar with python programming so we will seek to enable all required user interactions to be entered via a GUI. The use cases we provide will allow the urban planner to explore a variety of scenarios to identify where issues are currently occuring.

**Community activist:** Community activitst may seek to ensure certain safety standards are maintained during this period of rapid growth in Seattle. This tool will allow activitists to identify areas where safety may be compromised during growth so they may lobby for policy improvements, with facts to support their efforts. They may be less familiar with the data set than the urban planners. They will also desire to use GUI for all user inputs. 

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


## 2. Use Case: Toggle Permit Type

* **What it does:** Changes which permits to plot by letting user specify selection criteria
  Selection criteria could include: 
  	* **Category** (e.g., single family, multi-family, commercial or industrial)
  	* **Value:** The value of work to be conducted
* **Inputs:** 
  * Map of permits and collision
  * Field\_selection (string) Select which field you want to filter, by moving a value\_selection toggle or slider
  * Value_selection (string, float or int depending on field selected e.g., if user selects "category" as their selected field, the value selection is a string, if the user selected value as thier field the value selection would be an int). Value selection comes from interactive Jupyter radio buttons (category) or slider (value)
* **Outputs:** 
  * Updated map that includes permits selected by inputs, and associated collision data (based on selected radius)


## 3. Use Case: Select Radius Size
* **Name:** select_radius_size
* **What it does:** Allows users to set a radius value that is used to filter the data and display a subset of the crashes within the selected radius of a building. 
* **Inputs:**
   - Radius value, that is specified by the user through a jupyter slider. There are three different values, small, medium and large.
   - 3 databases, Collisions, Building and Radius. Collisions contains a set of collisions and attributes, buildings contains info on buildings permits and radius contains building ids, collision ids and radius (distance between buildings and collision occurrences).
* **Outputs:** 
   - Jupyter map that displays the collisions that are within the selected radius, for each collision - building pairs

## 4. Use Case: Toggle Accident Severity
* **Name:** accident_severity
* **What it does:** Allows user to adjust map view by filtering based on the severity of the accident that occurred around where building permits are issued. The user will then be able to compare the severity of accidents within the proximity of building permits before, during, and after construction.  The severity classifications included in the Collisions dataset are Property Damage, Injury, Serious Injury, Fatality or Unknown.
* **Inputs:**
   - The user inputs the accident severity level they are interested in comparing. This could include one, all, or a subset of the accident severity codes associated with each collision.
   - The selected accident severity is used to filter the collisions database. The collision IDs are then fed into the Radius database that associates collisions with certain building permits.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected severity code. 

## 5. Use Case: Toggle Accident Type
* **Name:** accident_type
* **What it does:** Allows user to adjust map view by filtering based on the type of accident that occurred around where building permits are issued. The user will then be able to compare the type of accidents within the proximity of building permits before, during, and after construction.  The classifications included whether the accident involved pedestrians, cyclists, or vehicle only. 
* **Inputs:**
   - The user inputs the accident type they are interested in comparing. This could include one, all, or a subset of the accident types that are used to classify each collision.
   - The selected accident type is used to filter the collisions database. The collision IDs are then fed into the Radius database that associates collisions with certain building permits.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected accident type

## Components

The components that we will be using for the project are listed below:



## Draw_markers

- **Name:** Draw_markers
- **What it does:** component is used to place markers on the map that correspond to collision occurrences.
- **Inputs:**
  - Latitude (float): The latitude value for the given point.
  - Longitude (float): The longitude value for the given point.
- **Outputs:** The code to plot the point on the map.



## Build_query

- **Name:** Build_query
- **What it does:** It builds or constructs the SQL query based on the selectors from the sliders.
- **Inputs:** The values from the sliders (integer and float based.)
- **Outputs:** A SQL query that is sent to SQLite for processing



## Build_ui

- **Name:** Build_ui
- **What it does:** This component is used to construct our maps that we use to visualize our data.
- **Inputs:** Dates, in the form of a string.
- **Outputs:** Three maps are constructed by our component, one for each time period corresponding to before construction, during construction and after construction. The layout of these maps, along with the interaction widgets are all constructed by this component.

## Build_date_query

- **Name:** Build_date_query

- **What it Does:** The construction of the query that handles time periods (the before, during and after) is performed by this component.

- **Inputs:** A date, that is in the form of a string.

- **Outputs:** Three different periods, before, during and after, in the form of dates.

  

## Interactions

We detail some sample interaction scenarios in this section. 

### Setting a Date Range

**Pseudo code:**

- Set constr\_start and constr_end from jupyter input slider.
- Calculate constr\_dur, the duration of the construction task to be normalized.
- Set before\_start date as the constr\_start minus the data\_dur selected in the jupyter radio button.
- Set after\_end date as the constr\_end plus the data\_dur selected in the jupyter radio button.
- Query all construction sites from the derived construction database that were started and completed within the (constr\_start, constr\_end) time frame. Set sites to display\_sites.
- Query the collision counts in the pre-defined radius for each site in display\_sites in the following time frames:
  - before\_ct: (before\_start, constr\_start)
  - during\_ct: (constr\_start, constr\_end)
  - after\_ct: (constr\_end, after\_end)
- Normalize the during\_ct so it reflects the same time period as before and after: 
  - during\_ct_normalized = during\_ct * constr_dur / data\_dur
- Update map display:
  - Display only construction sites in display\_sites.
  - Use updated before\_ct, during\_ct\_normalized, and after\_ct for map data views.
  - Allow user to re-adjust jupyter settings and repeat process with new inputs.

### Toggling a Permit Type

**Pseudo code:**

- Field\_selection = field selection identified in toggle
- Value\_selection = value selection identified in toggle
- Using pandas filter the permit data base based on field\_selection and value_selection 
- Take the resulting permit ID column as a vector and filter the Radius database based on those permit IDs
- Feed new data into map for automatic update
- Return updated map

### Selecting a Radius Size

**Pseudocode:**

- Read the radius size that is set by the user.
  - The radius size is a string that specifies small, medium and large.
  - This radius size is converted into a number that is passed on to the query.
- Generate a query in SQL that performs a search on the Radius DB
  - Take the returned size from the Jupyter slider.
  - Pass this query back to the SQL backend.
- Execute the query on the Radius DB, and collect the returned results. 
  - Process the returned tuples and perform a computation that determines whether a point needs to be added or removed.
- Perform an update of the map displays, so that they reflect

### Toggling Accident Severity

**Pseudo code:**

- Receive accident severity input levels selected by user via the interactive feature on the map
- Using pandas, filter the Collisions database with the severity code column based on the user input. 
- Take the resulting Collision ID column as a vector and filter the Radius database based on those collision IDs
- Feed new data into map for automatic update.

### Toggling Accident Type

**Pseudo code:**

- Receive accident type selected by user via the interactive feature on the map[
- Using pandas, filter the Collisions database with the accident type column based on the user input. 
- Take the resulting Collision ID column as a vector and filter the Radius database based on those collision IDs
- Feed new data into map for automatic update.