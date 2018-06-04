"""
This module contains the setup.py for running the Collidium tool
"""
from setuptools import setup, find_packages
PACKAGES = find_packages()


opts = dict(name='Collidium',
            maintainer='Alyssa Goodrich, Tejas Hosangadi, Ian Kirkman, Dan White',
            maintainer_email='dkwhite@uw.edu',
            description='Seattle Construction and Traffic Accident Visualization Tool',
            long_description=("""Collidium is a tool that allows users to visualize and
             understand the impact of construction on the occurence of traffic accidents 
             in the City of Seattle. It's structered as a Jupyter notebook with 
             interactive controls"""),
            url='https://github.com/tejasmhos/seattlecollision',
            license='MIT',
            author='Collidium',
            author_email='dkwhite@uw.edu',
            version='0.1',
            packages=PACKAGES,
            package_data={'seattlecollision': ['data/*', 'tests/*']},
           )
# setup(...,
#       packages=['mypkg'],
#       package_dir={'mypkg': 'src/mypkg'},
#       package_data={'mypkg': ['data/*.dat']},
#       )

if __name__ == '__main__':
    setup(**opts)
