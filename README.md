# isql.py is a simple program to interactively access and work with SQL databases
It is intended to be used interactively, but can be used in scripts with input and output files.
This was developed by Warren L. Rutledge
Copyright 2023, All Rights Reserved.
This code is distributed under the GNU GPL and the license file should be found with this code.
## Dependencies
As much as possible, it has been developed using the Python standard library to limit the number
of modules you may need to add via pip or conda depending on your Python installation.
## Modules that you may need to add via pip or conda:
    **pymssql**  This provides the connectivity to SQL Server and ASE
    **psycopg2**  This provides the connectivity to PostgreSQL
    **sqlite3**  This should be in your python distribution
    **python-mysql-connector**  This provides the connectivity to MySQL and MariaDB
    **oracledb**  This provides the connectivity to Oracle
    **rich**  This provides the nice formatted output by default
    **readline** (pyreadline if on Windows)
    **prettytable**  This provides the older style, mysql like formatted output
## This program will create a .isql directory in your home directory if one does not exist
This directory will get a copy of: 
* the current baseline configuration file ***isql.cfg***
* the current baseline snippets for each platform in the ***snippets*** directory
Additionally, it will create a directory to hold the log files for the application in ***logs***
#####
If you should decide to change the defaults via the config file, the easiest way to get a 
clean copy is to rename your old file and start isql.py which will force the application to
copy the baseline config file to your directory again.
##
