
"""
The data_clean.py module includes the functions used to clean the collisions and building permit datasets.
The two respective functions take the raw data as an input and output a dataframe along with
a created dataframe file.

"""

import os
import pandas as pd
import numpy as np

def collision_clean(file_path):
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
  collisions = collisions[["objectid",
                           "X",
                           "Y",
                           "incdate",
                           "incdttm",
                           "pedcount",
                           "pedcylcount",
                           "severitycode",
                           "severitydesc"]]
  collisions.dropna(inplace=True)
  collisions = collisions.rename(columns={"objectid": "c_id",
                                          "X": "c_long",
                                          "Y":"c_lat",
                                          "incdate": "c_date",
                                          "incdttm":"c_datetime",
                                          "pedcount": "c_ped",
                                          "pedcylcount" : "c_cyc",
                                          "severitycode" : "c_severity_code",
                                          "severitydesc" : "c_severity_desc"})
  collisions['c_veh'] = np.where(collisions['c_cyc'] == 0,
                                 np.where(collisions['c_ped'] == 0, 1, 0), 0)
  collisions = collisions[collisions["c_severity_desc"] != "Unknown"]
  collisions.to_csv('processed_collisions_outfile.csv')
  return collisions

"""
This buildings_clean functions cleans the building permits dataset from Seattle Open Data portal.
Only new construction is selected, along with projects that have a value > $250,000
The column names are renamed and NA observations are removed.
"""
def buildings_clean(file_path):
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
  if not os.path.exists(file_path):
        raise ValueError('The file path is not valid')
  buildings = pd.read_csv(file_path, sep=',', header=0, index_col=0)
  buildings = buildings[["Application/Permit Number",
                         "Permit Type",
                         "Category",
                         "Action Type",
                         "Work Type",
                         "Value",
                         "Issue Date",
                         "Final Date",
                         "Expiration Date",
                         "Status",
                         "Latitude",
                         "Longitude"]]
  buildings = buildings[buildings["Action Type"] == "NEW"]
  buildings = buildings[buildings["Value"] > 500000]
  buildings = buildings[pd.notnull(buildings["Issue Date"])]
  buildings = buildings[pd.notnull(buildings["Final Date"]) |
                        pd.notnull(buildings["Expiration Date"])]
  buildings = buildings[buildings["Status"] != "CANCELLED"]
  buildings = buildings[buildings["Category"]=="COMMERCIAL"]
  buildings = buildings.rename(columns={"Application/Permit Number": "b_id",
                                        "Permit Type": "b_permit_type",
                                        "Category" : "b_category",
                                        "Action Type" : "b_action_type",
                                        "Work Type" : "b_work_type",
                                        "Value": "b_value",
                                        "Issue Date" : "b_issue_date",
                                        "Final Date" : "b_final_date",
                                        "Expiration Date" : "b_expiration_date",
                                        "Status" : "b_status",
                                        "Latitude" : "b_lat",
                                        "Longitude" : "b_long"})
  buildings.to_csv('processed_buildings_outfile.csv')
  return buildings


collision_clean("Collisions.csv")
buildings_clean("clean_permits.csv")
