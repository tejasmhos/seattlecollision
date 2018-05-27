"""
TODO Insert docstring
"""
import sqlite3
import os
import pandas as pd

import table_builder
import draw_markers
from query_class import CollidiumQuery

def generate_connection(data_directory, db_name):
    """
    TODO Insert docstring
    """
    if not os.path.exists(str(data_directory)):
        raise ValueError(str((data_directory) +" is not a valid path"))
    table_builder.create_table(db_name, data_directory)
    connection = sqlite3.connect(db_name)
    sql_cursor = connection.cursor()
    sql_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = sql_cursor.fetchall()
    table_list =  [item for sublist in table_list for item in sublist]
    true_table = 'collidium_data'
    if not true_table in table_list:
        raise Exception("The directory must contain a file called 'collidium_data.csv'")   
    return sql_cursor

SQL_CURSOR = generate_connection("data/", "collidum_db")

def generate_categories(cols_needed):
    """
    TODO Insert docstring
    """
    
    data_fields = set(["b_category", "base_year","c_severity", "c_type"])
    if not set(cols_needed).issubset(set(data_fields):
        raise IndexError("cols_needed input must only contain the fields: 'b_category', 'base_year','c_severity', 'c_type'")
    categories = list()
    i = 0
    for col in cols_needed:
        query_string = str("select distinct " + col + " from collidium_data")
        SQL_CURSOR.execute(query_string)
        temp = pd.DataFrame(SQL_CURSOR.fetchall())
        temp = temp.values.tolist()
        temp = [val for sublist in temp for val in sublist]
        temp.insert(0, 'All')
        categories.append(temp)
        i += 1
    return categories[0], categories[1], categories[2], categories[3]

def generate_table(query):
    """
    TODO Insert docstring
    """
    SQL_CURSOR.execute(query)
    temp = pd.DataFrame(SQL_CURSOR.fetchall())
    temp.columns = list(map(lambda x: x[0], SQL_CURSOR.description))
    temp['b_lat'] = temp.b_lat.astype(float)
    temp['b_long'] = temp.b_long.astype(float)
    return temp

def build_type_interact(building_category):
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)

def year_int_interact(building_year, collision_interval):
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)

def collision_severity_interact(collision_severity):
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_c_severity(collision_severity)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)

def collision_type_interact(collision_type):
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_c_type(collision_type)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)

def radius_interact(radius_from_building):
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)

def all_factor_interact(building_category, building_year, collision_interval, collision_severity, collision_type, radius_from_building): #pylint: disable=line-too-long,too-many-arguments
    """
    TODO Insert docstring
    """
    query_builder = CollidiumQuery()
    query_builder.set_b_category(building_category)
    query_builder.set_base_year(building_year)
    query_builder.set_duration(collision_interval)
    query_builder.set_c_severity(collision_severity)
    query_builder.set_c_type(collision_type)
    query_builder.set_radius(radius_from_building)
    whole_query = query_builder.get_qstring()
    mapping_data = generate_table(whole_query)
    return draw_markers.place_maps(mapping_data)
