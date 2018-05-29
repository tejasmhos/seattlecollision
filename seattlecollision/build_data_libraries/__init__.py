"""
Infile/outfile constants are set immediately after the import statements in this module. A
short script is run at the EOF to build each of the required processed dataframes and output
them to the specified locations in csv format.
"""

from process_data import *
from table_builder import create_table

# INPUT FILEPATHS
COLLISIONS_RAW_INFILE = "../data/raw_data/raw_collisions_input.csv"
BUILDINGS_RAW_INFILE = "../data/raw_data/raw_buildings_input.csv"
# OUTPUT FILEPATHS
COLLISIONS_PROCESSED_OUTFILE = "../data/collisions.csv"
BUILDINGS_PROCESSED_OUTFILE = "../data/buildings.csv"
COLLIDIUM_PROCESSED_OUTFILE = "../data/collidium_data.csv"

# PROCESS DATAFRAMES
COLLISIONS = collisions_clean(COLLISIONS_RAW_INFILE)
BUILDINGS = buildings_clean(BUILDINGS_RAW_INFILE)
COLLIDIUM = create_collidium_table(COLLISIONS, BUILDINGS.head(1))

# EXPORT TO CSV FILES
COLLISIONS.to_csv(COLLISIONS_PROCESSED_OUTFILE)
BUILDINGS.to_csv(BUILDINGS_PROCESSED_OUTFILE)
COLLIDIUM.to_csv(COLLIDIUM_PROCESSED_OUTFILE)

# BUILD SQLITE DB FOR COLLIDIUM DATA
create_table('Collidium',COLLIDIUM_PROCESSED_OUTFILE)