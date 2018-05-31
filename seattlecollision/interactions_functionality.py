"""
TODO Insert docstring

TODO: Add error checking for zero results (maybe just draw blank maps but right now it fails).

TODO:
I commented out lines below that did not work or were no longer necessary. Please review
and delete if you agree. --Ian (Also do a find on the word 'TODO' because I added another inline
comment).
"""
import sqlite3
import os
import pandas as pd
import draw_markers
from query_class import CollidiumQuery

def generate_connection(data_directory):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    connection = sqlite3.connect(data_directory)
    sql_cursor = connection.cursor()
    sql_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return sql_cursor



def generate_categories(cols_needed, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    true_set = set(['b_category', 'base_year', 'c_severity', 'c_type'])
    if not set(list(cols_needed)) == true_set:
        raise IndexError("cols_needed must only contain the fields:", true_set)
    categories = list()
    i = 0
    for col in cols_needed:
        query_string = str("select distinct " + col + " from collidium_data")
        sql_cursor = generate_connection(data_directory)
        sql_cursor.execute(query_string)
        temp = pd.DataFrame(sql_cursor.fetchall())
        temp = temp.values.tolist()
        temp = [val for sublist in temp for val in sublist]
        temp.insert(0, 'All')
        categories.append(temp)
        i += 1
    return categories[0], categories[1], categories[2], categories[3]

def generate_table(query, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    sql_cursor = generate_connection(data_directory)
    sql_cursor.execute(query)
    temp = pd.DataFrame(sql_cursor.fetchall())
    temp.columns = list(map(lambda x: x[0], sql_cursor.description))
    return temp

def build_type_interact(building_category, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    try:
        mapping_data.shape[0] > 0
    except:
        print('The filter you chose filtered out all the data!')
    return draw_markers.place_maps(mapping_data)

def year_int_interact(building_year, collision_interval, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def collision_severity_interact(collision_severity, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_c_severity(collision_severity)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def collision_type_interact(collision_type, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_c_type(collision_type)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def radius_interact(radius_from_building, data_directory="data/Collidium"):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)

def all_factor_interact(building_category, building_year, collision_interval, collision_severity, collision_type, radius_from_building, data_directory="data/Collidium"): #pylint: disable=line-too-long,too-many-arguments
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    query_builder.set_c_severity(collision_severity)
    query_builder.set_c_type(collision_type)
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    print(whole_query)
    mapping_data = generate_table(whole_query, data_directory)
    return draw_markers.place_maps(mapping_data)
