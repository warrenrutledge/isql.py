# Help About This Application
isql.py is a commandline interface to a sql database.  It specifically mimics the way
Sybase's isql tool used to work.  The purpose is to provide a common interface to a 
number of database platforms using a single, simple, command line tool.
######
It supports MSSQL, Syabse ASE, MySQL, MariaDB, PostgreSQL, SQLITE3 and Oracle.
It is specifically designed to be tool for administration, not database development.
######
There are functions for changing the format of output, redirecting it to a file,
reading from a file, repeating commands, and for using predefined queries (called snippets).  

## Notable features:
* All commands logged to a file in case you need to audit or refer to what happened in a session
* Multiple output methods (see ***help output***)
* Scriptable via -i flag on the commandline or @read in interactive mode
* Can reconnect including option of switching databases (***required on postgresql to change db***)
* Defaults can be configured via isql.cfg file
* Shell commands can be exectued via the **@** commands
* Edit the buffer using your $EDITOR and the tempfile is written using a .sql suffix to support syntax help, if your editor supports it

#### History:
The initial release has been written by Warren L. Rutledge, Copyright 2023.  All Rights Reserved.
This was initially developed on MacOS, it has been tested on several flavors of Linux, FreeBSD, and Windows
It was written using MacVim, GVim, vim, neovim, and Neovide on various platforms.  
It is implemented using Python and relies on the following modules:
**rich**  provides the nice formatted tables
**prettytable** provides a text output like MySQL
**pyscopg2** provides the PostgreSQL connections
**mysql-connector** provides the MySQL/MariaDB connections
**pymssql** provides the MSSQL/ASE connections
**oracledb** provides the Oracle connections
**sqlite3** provides the SQLITE3 connections
## 
Beyond these core modules were used to provide access to os functions, file paths, csv files, timing, and 
reading command line options.
## 
