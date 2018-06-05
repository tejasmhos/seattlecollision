"""
COLLIDIUM

This module contains a python script to process raw data and
build the Collidium sqlite database.

NOTE: This takes significant time to execute. However,
the completed database is included in the git repository and
unpackaged by the setup.py, so it should be unnecessary to
execute this script.

Infile/outfile constants are set immediately after the import
statements.
"""

import process_data
from table_builder import create_table

# INPUT FILEPATHS
COLLISIONS_RAW_INFILE = "../data/raw_data/raw_collisions_input.csv"
BUILDINGS_RAW_INFILE = "../data/raw_data/raw_buildings_input.csv"
# OUTPUT FILEPATHS
COLLISIONS_PROCESSED_OUTFILE = "../data/collisions.csv"
BUILDINGS_PROCESSED_OUTFILE = "../data/buildings.csv"
COLLIDIUM_PROCESSED_OUTFILE = "../data/collidium_data.csv"

# PROCESS DATAFRAMES
COLLISIONS = process_data.collisions_clean(COLLISIONS_RAW_INFILE)
BUILDINGS = process_data.buildings_clean(BUILDINGS_RAW_INFILE)
COLLIDIUM = process_data.create_collidium_table(COLLISIONS, BUILDINGS)

# EXPORT TO CSV FILES
COLLISIONS.to_csv(COLLISIONS_PROCESSED_OUTFILE)
BUILDINGS.to_csv(BUILDINGS_PROCESSED_OUTFILE)
COLLIDIUM.to_csv(COLLIDIUM_PROCESSED_OUTFILE)

# BUILD SQLITE DB FOR COLLIDIUM DATA
create_table('../data/Collidium', COLLIDIUM_PROCESSED_OUTFILE)
