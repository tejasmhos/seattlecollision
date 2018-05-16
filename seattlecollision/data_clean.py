
"""
The data_clean.py module includes the functions used to clean the collisions and building permit datasets.
The two respective functions take the raw data as an input and output a dataframe along with
a created dataframe file.

"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

def collisions_clean(file_path):
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
  for i in range(0,len(collisions)):
      if len(collisions['incdttm'][i]) > 10:
          obj = datetime.strptime(collisions["incdttm"][i], '%m/%d/%Y %I:%M:%S %p')
          date_time.append(obj.replace(hour=0, minute=0, second=0))
      else:
          obj = datetime.strptime(collisions["incdttm"][i], '%m/%d/%Y')
          obj.replace(hour=0, minute=0, second=0)
          date_time.append(obj.replace(hour=0, minute=0, second=0))
  collisions["date_time"] = date_time
  collisions = collisions[collisions["date_time"] > datetime(2013,1,1)]
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
  collisions['c_veh'] = np.where(collisions['c_cyc'] == 0,
                               np.where(collisions['c_ped'] == 0, 1, 0), 0)
  collisions = collisions[collisions["c_severity_desc"] != "Unknown"]
  print("Woo hoo! Collisions complete.")
  #collisions.to_csv('processed_collisions_outfile.csv')
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
  buildings = pd.read_csv(file_path, sep=',',header=0, index_col = 0)
  issue_date = []
  final_date =[]
  for i in range(0,len(buildings)):
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
          f_obj=(float('NaN'))
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
  buildings = buildings[buildings["Action Type"]=="NEW"]
  buildings = buildings[buildings["Value"] > 1000000]
  buildings = buildings[pd.notnull(buildings["b_issue_date"])]
  buildings = buildings[pd.notnull(buildings["b_final_date"])]
  buildings = buildings[buildings["Status"] != "CANCELLED"]
  buildings = buildings.rename(columns={"Application/Permit Number": "b_id", 
                                        "Category" : "b_category", 
                                        "Value": "b_value",
                                     "Status" : "b_status",
                                     "Latitude" : "b_lat",
                                      "Longitude" : "b_long" })
  buildings.drop("Action Type", axis=1,inplace=True)
  print("Woo hoo! Buildings Complete")
  return buildings

"""

  if not os.path.exists(file_path):
        raise ValueError('The file path is not valid')
  buildings = pd.read_csv(file_path, sep=',',header=0, index_col = 0)

  buildings = buildings[["Application/Permit Number",
                       "Category", 
                       "Action Type",
                       "Value",
                       "Issue Date",
                       "Final Date",
                       "Status",
                       "Latitude",
                       "Longitude"]]
  buildings = buildings[buildings["Action Type"]=="NEW"]
  buildings = buildings[buildings["Value"] > 1000000]
  buildings = buildings[pd.notnull(buildings["Issue Date"])]
  buildings = buildings[pd.notnull(buildings["Final Date"])]
  buildings = buildings[buildings["Status"] != "CANCELLED"]
  buildings = buildings.rename(columns={"Application/Permit Number": "b_id", 
                                        "Category" : "b_category", 
                                        "Value": "b_value",
                                        "Issue Date" : "b_issue_date",
                                        "Final Date" : "b_final_date",
                                     "Status" : "b_status",
                                     "Latitude" : "b_lat",
                                      "Longitude" : "b_long" })
  buildings.drop("Action Type", axis=1,inplace=True)
  buildings.to_csv('processed_buildings_outfile.csv')
  return buildings
"""

processed_c = collisions_clean("data/raw_data/raw_collisions_input.csv")
processed_b = buildings_clean("data/raw_data/raw_buildings_input.csv")
processed_c.to_csv('data/processed_collisions_outfile.csv')
processed_b.to_csv('data/processed_buildings_outfile.csv')

