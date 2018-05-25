
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
COLLIDIUM_PROCESSED_OUTFILE = "data/collidium_data.csv"

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
    tmp_cyc_or_ped = collisions['c_cyc'] + collisions['c_ped']
    collisions['c_accident_type'] = np.where(tmp_cyc_or_ped > 0, "Bike/Pedestrian", "Vehicle Only")
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

def create_collidium_table(collisions, buildings):
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
            b_id: (string) matches to buildings_clean table
            c_id: (string) mathces to collision_clean table
            b_lat: (float) building latitude
            b_long: (float) building longitude
            b_category: (string) building category
            b_start_dt: (datetime.date) date with time stripped
            b_end_dt: (datetime.date) date with time stripped
            c_dt: (datetime.date) date with time stripped
            c_lat: (float) collision latitude
            c_long: (float) collision longitude
            acc_type: (string) collision type
            acc_severity: (string) collision severity description
            radius: (float) distance in feet between building and collision
            coll_before: (1 or 0) collision within 12 months before building period
            coll_during: (float) during indicator normalized to one year of exposure
            coll_after: (1 or 0) collision within 12 months after building period
            coll_days_from_build: (int) number of days between collision and build period
    """
    rad_data = []

    for _i, build in buildings.iterrows():
        b_loc = (build["b_lat"], build["b_long"])
        for _j, coll in collisions.iterrows():
            c_loc = (coll["c_lat"], coll["c_long"])
            dist = vincenty(b_loc, c_loc).ft
            if dist <= 1500:
                days_from_build = 0
                before = 0
                during = 0
                after = 0
                if coll["c_datetime"] < build["b_issue_date"]:
                    days_from_build = (coll["c_datetime"] - build["b_issue_date"]).days
                    before = 1
                elif coll["c_datetime"] > build["b_final_date"]:
                    days_from_build = (coll["c_datetime"] - build["b_final_date"]).days
                    after = 1
                else:
                    # Adjust during indicator for one year of exposure
                    during = ((build["b_final_date"] - build["b_issue_date"]).days)/365

                if abs(days_from_build) <= 365:
                    rad_data.append({
                        'b_id': build["b_id"],
                        'c_id': coll["c_id"],
                        'b_lat': b_loc[0],
                        'b_long':  b_loc[1],
                        'b_category': build["b_category"],
                        'b_start_dt': build["b_issue_date"],
                        'b_end_dt': build["b_final_date"],
                        'c_dt': coll["c_datetime"],
                        'c_lat': c_loc[0],
                        'c_long': c_loc[1],
                        'c_type': coll["c_accident_type"],
                        'c_severity': coll["c_severity_desc"].replace(' Collision', ''),
                        'radius': dist,
                        'coll_before': before,
                        'coll_during': during,
                        'coll_after': after,
                        'coll_days_from_build': days_from_build
                    })
                else:
                    pass
            else:
                pass
    print("Woo hoo! Collidium Data Complete")
    return pd.DataFrame(rad_data)

# PROCESS DATAFRAMES
COLLISIONS = collisions_clean()
BUILDINGS = buildings_clean()
COLLIDIUM = create_collidium_table(COLLISIONS, BUILDINGS)

# EXPORT TO CSV FILES
COLLISIONS.to_csv(COLLISIONS_PROCESSED_OUTFILE)
BUILDINGS.to_csv(BUILDINGS_PROCESSED_OUTFILE)
COLLIDIUM.to_csv(COLLIDIUM_PROCESSED_OUTFILE)
