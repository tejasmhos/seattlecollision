# Collidium - Seattle Collision Research Tool
[![Build Status](https://travis-ci.org/tejasmhos/seattlecollision.svg?branch=master)](https://travis-ci.org/tejasmhos/seattlecollision.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/tejasmhos/seattlecollision/badge.svg?branch=master)](https://coveralls.io/github/tejasmhos/seattlecollision?branch=master) 

Collidium is a tool that allows users to visualize and understand the impact of construction on the occurrence of traffic accidents in the City of Seattle. It's structured as a Jupyter notebook with interactive controls. 

To use the package, you need to clone the repository from Github, and follow the instructions given in the Installation section below.


## Organization of the Project

The organization of our project is shown below:

```
seattlecollision/
	|- seattlecollision/
		|- build_data_libraries/
		        |- _build_database_script.py
			|- process_data.py
			|- table_builder.py
		|- data/
			|- raw_data/
				|- raw_buildings_input.csv
				|- raw_collision_input.csv
			|- Collidium.db
			|- Test_Data_For_Draw_Markers.csv
			|- buildings.csv
			|- collidium_data.csv
			|- collisions.csv
		|- tests/
			|- test_draw_markers.py
			|- test_interactions_functionality.py
			|- test_process_data.py
			|- test_table_builder.py
		|- Collidium.ipynb
		|- __init__.py
		|- draw_markers.py
		|- interaction_functionality.py
		|- query_class.py
	|- doc/
		|- Tech Review Presentation.pdf
		|- finalpresentation.pdf
		|- functionaldesign.md
		|- Component_design.md
		|- project_structure.png
	|- examples/
		|- Shortcut to Collidium Notebook.md
	|- .coveragerc
	|- .travis.yml
	|- LICENSE
	|- README.md
	|- collidium_env.yml
	|- requirements.txt	
	|- setup.py
```

## Installation

There are two installation options outlined in the section below which include either activating the collidium.yml environment or peforming pip installations of the minimum requirements. After installation, the project can be executed by opening the Collidium.ipynb notebook. All tools and functionality is integrated into this notebook. No other application needs to be opened. 

### Minimum Environment Activation
This option will activate the collidium.yml environment which contains the minimal requirements needed to run Collidium.

1. Clone the respository onto your machine and navigate to the main directory.
2. Activate the collidium.yml environment by entering the command below into your command line.

    ```conda env create -f collidium.yml```

3. Launch [Collidium](seattlecollision/Collidium.ipynb) in a Jupyter notebook and activate the Collidium environment. More instructions on activating the kernel for use on a Jupyter notebook is available [here](http://anbasile.github.io/programming/2017/06/25/jupyter-venv/)

### Pip Installation of Requirements
Alternatively, if there are issues running the minimum environment, users can pip install the requirements needed to run Collidium on their local environment.

1. Clone the respository onto your machine and navigate to the main directory.
2. Run the commands to install the necessary package dependencies for running the notebook.

    ``` pip install -r requirements.txt```

The package requirements for Collidium are summarized below:
 * pandas
 * numpy
 * branca
 * folium
 * ipywidgets
 * geopy
 * ipython
    
3. Launch [Collidium](seattlecollision/Collidium.ipynb) in a Jupyter notebook

## Data Sources
 The data sourced for Collidium was taken from the [Seattle Open Data Portal](https://data.seattle.gov/). The tool uses processed versions of the [Building Permits](https://data.seattle.gov/Permitting/Building-Permits-Current/mags-97de/data) dataset and the [Collisions](https://data-seattlecitygis.opendata.arcgis.com/datasets/collisions/data) dataset. 
 
 These processed datasets were aggregated into a database which provides the underlying data for the Collidium notebook. We calculate the distance between collisions and buildings and join collisions that occur within 1500 ft and 1 year of building permit. This database helps us reduce the complexity of our queries.
 
 Our package ships with the sqlite database [Collidium](seattlecollision/data/Collidium) already constructed and ready to use out of the box. However, we have also included the build script for reproducibility and transparency in our processing assumptions. Our data building modules are all contained within the [build_data_libraries](seattlecollision/build_data_libraries/) subfolder, and the `_build_database_script.py` script executes all processes to rebuild the database from scratch. (Note/warning: reprocessing the data may take a couple of hours).
 
## Project History

This project was inspired our team's observation that new building construction in Seattle is sometimes not accompanied by corresponding transportation infrastructure. We conducted this analysis to see if there is a visible difference in the number of collisions during and after construction, as compared to the period before construction. This project can be used by community activists, city planners and municipal politicians to help guide their decisions and agendas. 

## Limitations

This project has several limitations. These include: 

 - Some functionality can only be run on Python 3.5 or later
 - When we processed the data we normalized the construction period so that we could compare collisions during construction on an apples to apples basis to the before construction period and after construction period. When we normalized the data we did not take seasonality into account. This may result in a bias.
 - This project does not include statistical analysis. Although some differences in collisions are detected, we did not identify whether the differences arestatistically significant.
 - Users are required to use Jupyter notebook to run this project. Some of our targeted user group may not have access or knowledge of how to use Jupyter notebooks. 
 
## Acknowledgements
 
 Collidium was developed for a class project in Spring 2018 for the Data 515A - Software Engineering for Data Scientists course at University of Washington. Many thanks to instructors David A. C. Beck and Joseph L. Hellerstein of the University of Washington eScience Institute for their insight and guidance throughout project development.

## Contributors

There are 4 primary contributors to this project. They are:

- Alyssa Goodrich
- Dan White
- Ian Kirkman 
- Tejas Hosangadi

## License

This project is licensed under the MIT license.
