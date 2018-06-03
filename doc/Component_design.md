# Collidium

## Pre-dependencies
The user will interact with a jupyter notebook that displays greater Seattle maps with default construction and collision data visualized. In each of our use cases, jupyter interact widgets will allow the user to interact with our settings and update the map views. Maps will each have before, during, and after construction views of collision density at each new building site under the default (or selected) parameters.

The underlying database required to update our maps will be created in our 
python package, and the processed data will be condtained in a database called Collidium. This database includes fields for collision ID building pairs incluidng collision id, collision latitude and longitude, distance between collision and building site, distance between collision and construction site indicators for whether the collision happened before, during or after construction, number of days the collision occured from consturction window, collision type, building type, and collision severity. Much of the functionality of our project relies on querying this database.


## Components

The components that we will be using for the project are listed below:


## draw_markers

- **Name:** draw_markera

- **What it does:** Component is used to place markers on the map that correspond to building location and the count of collisions that occured before, during and after construction of the building. 

- **Inputs:**
  -  Collidium database that includes data for collision and building pairs within 1500 foot radius of construction site. Fields include by construction begin date, construction end date, collision date, base year, indicator for whether the collision happened before, during or after construction, number of days the collision occured from construction window, collision type, building type, and collision severity.
  -  Query_class, which is a class that creates SQL query that can be used to query database
  -  draw_markers component, is a function that takes 
- **Outputs:** 
- Three map objects with building permits plotted on it, with volume of collisions codified by size and change in volume of collisions relative to preconstruction period codified by color. The three maps correspond to collision count before construction, during construction and after construction.

- **How it interacts with other components:** Recieves database created in Recieves query created in the "build\_query" component. Builds maps using the draw_markers component and visualizes maps in the UI component


## build_query

- **Name:** build_query
- **What it does:** It filters a table using an SQL query based on the selectors from the sliders or radio buttons.

- **Inputs:** The values from the sliders (integer and float based.), a table including Lat/Lon, building type, radius size, collision type, date

- **Outputs:**  A table with the same fields as input table, but filtered with the required specifications as selected with sliders/radio buttons

- **How it interacts with other components:** The table created in the build\_query function is used as input in the draw_markers component. Also, the options selected in build\_query are based on the options created in the build\_ui component. 

## build_ui
- **Name:** build_ui
- **What it does:** This component is used to construct our user interface that we use to visualize our data, including building interactivity, as well as placing output maps in a side by side orientation.

- **Inputs:** Interactivity options selected by developers for interactivity element, and map objects created in draw_markers component for the map drawing component.

- **Outputs:** Three maps are constructed by our component, one for each time period corresponding to before construction, during construction and after construction. The layout of these maps, along with the interaction widgets are all constructed by this component.

- **How it interacts with other components:** This components has two parts, one that collects user input and one that draws output for the user to see. The UI built by this component is used to create inputs in the build\_query component; the maps drawn by this component are created in the draw\_markers component. 

## build\_date\_query

- **Name:** build\_date\_query

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