
"""
COLLIDIUM
Data Processing Module

Module Summary:
The process_data.py module includes the functions used to clean the collisions and building
permit datasets, as well as a function to create a radius table of building/collision pairs
within 1500 feet of each other. The two *_clean functions take the respective raw data as
input and output a pandas dataframe of the processed data tables. The create_radius_table
uses each of the dataframes created in the *_clean functions to build a new data table of
building and collision pairs within 1500 feet of each other. The geopy library's vincenty
function is used to determine building/collision distances.

Infile/outfile constants are set immediately after the import statements in this module. A
short script is run at the EOF to build each of the required processed dataframes and output
them to the specified locations in csv format.

Exceptions (ValueError) are raised if either of the raw data file paths are invalid.

Raw Data Sources:
 - Building Permit data: (TODO: add web address)
 - Collision data: (TODO: add web address)

Data Processing Assumptions:
 - Collisions were restricted to 2013 and later (buildings permit data starts in 2014)
 - Buildings were restricted to being over $1 Million in value, to focus on large projects
 - TODO: add rest of assumptions/restrictions
"""
from datetime import datetime
import os
from geopy.distance import vincenty
import pandas as pd
import numpy as np

# INPUT FILEPATHS
COLLISIONS_RAW_INFILE = "data/raw_data/raw_collisions_input.csv"
BUILDINGS_RAW_INFILE = "data/raw_data/raw_buildings_input.csv"
# OUTPUT FILEPATHS
COLLISIONS_PROCESSED_OUTFILE = "data/collisions.csv"
BUILDINGS_PROCESSED_OUTFILE = "data/buildings.csv"
RADIUS_PROCESSED_OUTFILE = "data/radius.csv"

def collisions_clean(file_path=COLLISIONS_RAW_INFILE):
    """
    Filters and removes unneeded observations from the collisions dataset

    The function removes any missing or unknown observations, takes a subset of the
    columns, and calculates a new vehicles only crash column based off the values in ped/cyc.

    Args:
        file_path (str): The file path of the Collisions.csv file from Seattle Open Data

    Returns:
        Dataframe of the filtered and clean collisions dataset. A .csv file is also created
        with the to_csv method in the directory from which the module is run.

    Raises:
        ValueError: If the file path does not exist.
    """
    if not os.path.exists(file_path):
        raise ValueError('The file path is not valid')
    collisions = pd.read_csv(file_path, sep=',', header=0)
    date_time = []
    for i in range(0, len(collisions)):
        if len(collisions['incdttm'][i]) > 10:
            obj = datetime.strptime(collisions["incdttm"][i], '%m/%d/%Y %I:%M:%S %p')
            date_time.append(obj.replace(hour=0, minute=0, second=0))
        else:
            obj = datetime.strptime(collisions["incdttm"][i], '%m/%d/%Y')
            obj.replace(hour=0, minute=0, second=0)
            date_time.append(obj.replace(hour=0, minute=0, second=0))
    collisions["date_time"] = date_time
    collisions = collisions[collisions["date_time"] > datetime(2013, 1, 1)]
    collisions = collisions[["objectid",
                             "X",
                             "Y",
                             "date_time",
                             "pedcount",
                             "pedcylcount",
                             "severitycode",
                             "severitydesc"]]
    collisions.dropna(inplace=True)
    collisions = collisions.rename(columns={"objectid": "c_id",
                                            "X": "c_long",
                                            "Y":"c_lat",
                                            "date_time":"c_datetime",
                                            "pedcount": "c_ped",
                                            "pedcylcount" : "c_cyc",
                                            "severitycode" : "c_severity_code",
                                            "severitydesc" : "c_severity_desc"})
    collisions['c_accident_type'] = np.where(collisions['c_cyc'] == 0,
                                   np.where(collisions['c_ped'] == 0, "Vehicle Only", "Bike/Pedestrian"), "Bike/Pedestrian")
    collisions = collisions[collisions["c_severity_desc"] != "Unknown"]
    print("Woo hoo! Collisions complete.")
    return collisions

def buildings_clean(file_path=BUILDINGS_RAW_INFILE):
    """
    Filters and removes unneeded observations from the Building Permits dataset

    The function removes any missing or unknown observations, takes a subset of the
    columns, and calculates a new vehicles only crash column based off the values in ped/cyc.

    Args:
        file_path (str): The file path of the clean_permits.csv file from Seattle Open Data

    Returns:
        Dataframe of the filtered and clean collisions dataset. A .csv file is also created
        with the to_csv method in the directory from which the module is run.

    Raises:
        ValueError: If the file path does not exist.
    """
    buildings = pd.read_csv(file_path, sep=',', header=0, index_col=0)
    issue_date = []
    final_date = []
    for i in range(0, len(buildings)):
        if pd.notnull(buildings["Issue Date"][i]):
            i_obj = datetime.strptime(buildings["Issue Date"][i], '%Y-%m-%d')
            issue_date.append(i_obj)
        else:
            i_obj = float('NaN')
            issue_date.append(i_obj)
        if pd.notnull(buildings["Final Date"][i]):
            f_obj = datetime.strptime(buildings["Final Date"][i], '%Y-%m-%d')
            final_date.append(f_obj)
        else:
            f_obj = (float('NaN'))
            final_date.append(f_obj)
    buildings["b_issue_date"] = issue_date
    buildings["b_final_date"] = final_date
    buildings = buildings[["Application/Permit Number",
                           "Category",
                           "Action Type",
                           "Value",
                           "b_issue_date",
                           "b_final_date",
                           "Status",
                           "Latitude",
                           "Longitude"]]
    buildings = buildings[buildings["Action Type"] == "NEW"]
    buildings = buildings[buildings["Value"] > 1000000]
    buildings = buildings[pd.notnull(buildings["b_issue_date"])]
    buildings = buildings[pd.notnull(buildings["b_final_date"])]
    buildings = buildings[buildings["b_final_date"] < datetime(2017, 4, 1)]
    buildings = buildings[buildings["Status"] != "CANCELLED"]
    buildings = buildings.rename(columns={"Application/Permit Number": "b_id",
                                          "Category" : "b_category",
                                          "Value": "b_value",
                                          "Status" : "b_status",
                                          "Latitude" : "b_lat",
                                          "Longitude" : "b_long"})
    buildings.drop("Action Type", axis=1, inplace=True)
    print("Woo hoo! Buildings Complete")
    return buildings

def create_radius_table(collisions, buildings):
    """
    Uses geopy's vincenty distance function to calculate collision distance
    from each building site. Distance is recorded in feet.

    For all collisions within 1500 feet of a building site, a builing/collision
    pair is added to the radius data table.

    Args:
        collisions: a processed collisions pandas dataframe (returned by
		    collisions_clean function)
        buildings: a processed building permit pandas dataframe (returned by
		    buildings_clean function)

    Returns:
        Radius table as a pandas dataframe (see table specs below)

        Radius data table includes (for unique (building, collision) pairs):
            build_id: (string) matches to buildings_clean table
            coll_id: (string) mathces to collision_clean table
            build_lat: (float) building latitude
            build_long: (float) building longitude
            build_start_dt: (datetime.date) date with time stripped
            build_end_dt: (datetime.date) date with time stripped
            coll_dt: (datetime.date) date with time stripped
            coll_lat: (float) collision latitude
            coll_long: (float) collision longitude
            radius: (float) distance in feet between building and collision
    """
    rad_data = []

    for _i, build in buildings.iterrows():
        b_loc = (build["b_lat"], build["b_long"])
        for _j, coll in collisions.iterrows():
            c_loc = (coll["c_lat"], coll["c_long"])
            dist = vincenty(b_loc, c_loc).ft
            if dist <= 1500:
                rad_data.append({
                    'build_id': build["b_id"],
                    'coll_id': coll["c_id"],
                    'build_lat': b_loc[0],
                    'build_long':  b_loc[1],
                    'build_start_dt': build["b_issue_date"],
                    'build_end_dt': build["b_final_date"],
                    'coll_dt': coll["c_datetime"],
                    'coll_lat': c_loc[0],
                    'coll_long': c_loc[1],
                    'radius': dist
                })
            else:
                pass

    return pd.DataFrame(rad_data)

# PROCESS DATAFRAMES
COLLISIONS = collisions_clean()
BUILDINGS = buildings_clean()
RADIUS = create_radius_table(COLLISIONS, BUILDINGS)

# EXPORT TO CSV FILES
COLLISIONS.to_csv(COLLISIONS_PROCESSED_OUTFILE)
BUILDINGS.to_csv(BUILDINGS_PROCESSED_OUTFILE)
RADIUS.to_csv(RADIUS_PROCESSED_OUTFILE)
