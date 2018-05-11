
"""
This module includes the functions used to clean the collisions and building permit datasets.
the function will take the raw files and then produce a csv of the cleaned data
"""

def collision_clean(file_path):
    collisions = pd.read_csv(file_path, sep=',',header=0)
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
    collisions['c_veh'] = np.where(collisions['c_cyc']==0,np.where(collisions['c_ped']==0,1,0),0)
    collisions.to_csv('collisions_clean.csv')
    return collisions


def buildings_clean(file_path):
    buildings = pd.read_csv(file_path, sep=',',header=0, index_col = 0)
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
    buildings = buildings[buildings["Action Type"]=="NEW"]
    buildings = buildings[buildings["Value"] > 250000]
    buildings = buildings[pd.notnull(buildings["Issue Date"])]
    buildings = buildings[pd.notnull(buildings["Final Date"]) | pd.notnull(buildings["Expiration Date"])]
    buildings = buildings[buildings["Status"] != "CANCELLED"]
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
                                       "Latitude" : "b_latitude",
                                        "Longitude" : "b_longitude" })
    buildings.to_csv('buildings_clean.csv')
    return buildings


collision_clean("GitHub/data/Collisions.csv")
buildings_clean('GitHub/data/clean_permits.csv')
