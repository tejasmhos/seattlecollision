# Collidium

## Introduction
Collidium is a tool that helps users gain insight about how collision volumes change around construction sites, before, during and after building construction. The tool allows users to enter their desired filtering criteria through a jupyter notebook based user interface. It then creates three maps showing the location of buildings that meet the critera. The size of the building marker corresponds to the number of collisions that occured before, during and after the building was constructed. 

## Targeted user
**Urban planner:** An urban planner could use this tool to visulaize the impact of construction and increased density on the rate traffic collisions. This could be used to identify potential problem areas that result from construction (e.g., pedestrian collisions tend to increase during construction, or parked car collisions tend to increase after construction). These insights could inform urban planning decisions for future building sites. We assume the urban planner is familiar with these data sets and the definitions of fields. He or she may not be familiar with python programming so we will seek to enable all required user interactions to be entered via a GUI. The use cases we provide will allow the urban planner to explore a variety of scenarios to identify where issues are currently occuring.

**Community activist:** Community activitst may seek to ensure certain safety standards are maintained during this period of rapid growth in Seattle. This tool will allow activitists to identify areas where safety may be compromised during growth so they may lobby for policy improvements, with facts to support their efforts. They may be less familiar with the data set than the urban planners. They will also desire to use GUI for all user inputs. 

**Municipal Politician:** Municipal politicians seek information to inform their policy priorities and budgeting decisions. This tool will allow them to gain insight regarding potential safety areas so that they may choose to how to address them. 

## Use Cases
Key functionality: Enable users to view map of magnitude of collisions near new buildings in Seattle, before, during and after construction
Use cases: 
1. [Set building type] (#1-use-case-set-building-type)
2a. [Set base year](#2-use-case-set-base_year_and_collision_interval) 
2b. [Select collision interval](#2-use-case-toggle-permit-type) 
3. [Select Radius Size](#3-use-case-select-radius-size) 
4. [Toggle Accident Severity](#4-use-case-toggle-accident-severity)  
5. [Toggle Accident Type](#5-use-case-toggle-accident-type) (per/bike etc)
6. [Custom filter all attributes] (#5-use-case-custom-filter-all-attributes)

## 1. Use Case: Set building type

* **What it does:** Changes which permits to plot by letting user specify selection criteria for biulidng type
  Selection criteria could include: 
    * **Category** (e.g., single family, multifamily, commercial or industrial)

* **Inputs:** 
  * Map of permits and collision
  * Building_category (string),comes from interactive Jupyter drop down menu
  * collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** 
  * Updated maps that includes permits selected by inputs, and associated collision count data before, during and after building construction (based on selected radius)

 
## 2. Use Case: Set base year and collision interval
* **Name:** set\_base\_year\_and\_collision\_interval
* **What it does:** Allows user to adjust map view by choosing which year they would like to view building data for (base_year), as well as how long before and after the construction period would they like to count collisions (collision_interval)
* **Inputs:**
   - jupyter map view of before, during, and after construction with default duration settings
   - Collision Interval from jupyter drop down menu
   - Base year from jupyter drop down menu
   - collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** Adjusted map view in jupyter notebook that represents the selected building finish date time and collision intervals. Three maps are presented showing collision count, one each for before, during, and after construction


## 3. Use Case: Select Radius Size
* **Name:** select_radius_size
* **What it does:** Allows users to set a radius value that is used to filter the data and display a subset of the crashes within the selected radius of a building. 
* **Inputs:**
   - Radius value, that is specified by the user through a jupyter slider. There are three different values, small, medium and large.
   - collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** 
   - Jupyter map that displays the collisions that are within the selected radius, for each collision - building pairs. Three maps are presented showing collision count, one each for before, during, and after construction

## 4. Use Case: Toggle Accident Severity
* **Name:** accident_severity
* **What it does:** Allows user to adjust map view by filtering based on the severity of the accident that occurred around where building permits are issued. The user will then be able to compare the severity of accidents within the proximity of building permits before, during, and after construction.  The severity classifications included in the Collisions dataset are Property Damage, Injury, Serious Injury, Fatality or Unknown.
* **Inputs:**
   - The user inputs the accident severity level they are interested in comparing. This could include property damage, injury, severe injury or fatality.
   - collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected severity code. Three maps are presented showing collision count, one each for before, during, and after construction


## 5. Use Case: Toggle Accident Type
* **Name:** accident_type
* **What it does:** Allows user to adjust map view by filtering based on the type of accident that occurred around where building permits are issued. The user will then be able to compare the type of accidents within the proximity of building permits before, during, and after construction.  The classifications included whether the accident involved pedestrians/bikers, or vehicle only. 
* **Inputs:**
   - The user inputs the accident type they are interested in comparing. This could include one, all, or a subset of the accident types that are used to classify each collision.
   - collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected accident type. Three maps are presented showing collision count, one each for before, during, and after construction

## 6. Use Case: Custom filter all attributes
* **Name:** Custom filter all attributes
* **What it does:** Allows user to adjust map view by filtering based any or all of the attributes outlined above (builidng type, base date, collision interval, radius, collision type and collision severity) The user will then be able to compare the number of accidents within the proximity of building permits before, during, and after construction. 
* **Inputs:**
  - The user inputs values for each of the attributes including:
    - building type
    - base year
    - collision interval
    - collision severity
    - collision type
    - radius from building
  -  This could include one, all, or a subset of the accident types that are used to classify each collision.
   - collidium_data table that has collision and building pairs within pre-determined radius of construction site by date, indicator for whether the collision happened before, during or after construction, number of days the collision occured during consturction window, collision type, building type, and collision severity.
* **Outputs:** 
   - The map displayed within Jupyter notebook updates according to the number of accidents associated with the selected filtering criteria. Three maps are presented showing collision count, one each for before, during, and after construction