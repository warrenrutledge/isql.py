""" Global use environment variables """
import sys
import os
import argparse
import getpass
import shutil
from typing import Dict
from configparser import ConfigParser
from rich.console import Console
from prettytable import DEFAULT, MSWORD_FRIENDLY, PLAIN_COLUMNS


# We need to find where our stuff is so we can set up the personal copy
code_dir = os.path.dirname(os.path.abspath(__file__))

# Check for .isql directory for logging, etc.
# If it is not there, create it
HOME = os.path.expanduser(f"~{getpass.getuser()}")
ISQL_PATH = os.path.join(HOME, ".isql")
if os.path.exists(ISQL_PATH) is False:
    os.makedirs(ISQL_PATH)

if not os.path.exists(f"{ISQL_PATH}/isql.cfg"):
    shutil.copyfile(f"{code_dir}/isql.cfg", f"{ISQL_PATH}/isql.cfg")

if not os.path.exists(f"{ISQL_PATH}/snippets"):
    shutil.copytree(f"{code_dir}/snippets", f"{ISQL_PATH}/snippets")

LOG_PATH = os.path.join(ISQL_PATH, "logs")
if os.path.exists(LOG_PATH) is False:
    os.makedirs(LOG_PATH)


def pretty_options(parse_val: str) -> int:
    """Need to convert the text into a value"""
    ret_val = DEFAULT
    if parse_val.upper() == "MSWORD_FRIENDLY":
        ret_val = MSWORD_FRIENDLY
    if parse_val.upper() == "PLAIN_COLUMNS":
        ret_val = PLAIN_COLUMNS

    return ret_val


def build_options() -> Dict:
    """set up global variables"""
    parser = ConfigParser(allow_no_value=True)
    parser.read(f"{ISQL_PATH}/isql.cfg")

    # This holds our working data and data structures
    # FIXME: add fallback to get methods below to account for defaults
    opts = {
        "HOME": HOME,  # Path to home directory
        "CODE_DIR": code_dir,
        "LOG_PATH": LOG_PATH,  # Path to log files
        "SNIPPETS_PATH": parser.get("general", "snippets"),
        "SQL_BUFFER": "",  # This is buffer used to hold the query
        "LINE_NO": 1,  # We start at line 1 for user friendliness
        "HISTORY": [],  # Our history list
        "OUTPUT_STYLE": pretty_options(parser.get("output", "style").upper()),
        "OUTPUT_ALIGN": parser.get("output", "align"),
        "OUTPUT_HEADER": parser.getboolean("output", "header"),
        "OUTPUT_BORDER": parser.getboolean("output", "border"),
        "HEADER_STYLE": parser.get("output", "hcaps"),
        "OUTPUT_METHOD": parser.get("output", "method"),
        "OUTPUT_CSV": parser.getboolean("output", "csv"),
        "PAGER": parser.getboolean("output", "pager"),
        "PROMPT": parser.get("prompt", "format", fallback=""),
        "CONN": None,  # Current connection
        "CURSOR": None,  # Current cursor
        "SIG_INT": False,  # Did someone hit control c?
        "ERROR": False,  # Did we get an error?
    }

    parse_args(opts)

    return opts


def parse_args(options: Dict) -> None:
    """Parse command line arguments and add to options"""
    parser = argparse.ArgumentParser(
        description="isql.py - simple command line sql tool\
                for use with SQL Server, MySQL, and PostgreSQL.\\n \
                Party on, dudes!"
    )
    parser.add_argument("-U", "--user", help="user name for connection")
    parser.add_argument("-S", "--server", help="servername or ip address")
    parser.add_argument("-D", "--database", help="database name")
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-P", "--password", help="password")
    parser.add_argument("-p", "--port", help="port number")
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress messages")
    parser.add_argument("-Q", "--query", help="query to execute")
    parser.add_argument("-T", "--servertype", help="MSSQL|MYSQL|PSQL|SQLITE")
    parser.add_argument("-F", "--sqlitedb", help="location of sqlite db file")

    options["ARGS"] = parser.parse_args()

    # If we aren't passed a password, we'll prompt for it securely
    if options["ARGS"].password is None:
        try:
            password = getpass.getpass()
            options["ARGS"].password = password
        except getpass.GetPassWarning as err:
            print(f"ERROR: {err}")
            sys.exit(1)

    # We default to SQL Server, since I use that the most
    if options["ARGS"].servertype is None and options["ARGS"].server is not None:
        if options["ARGS"].quiet is None:
            print("Defaulting to severtype MSSQL")
        options["ARGS"].servertype = "MSSQL"

    # Get our default port if none was provided
    if options["ARGS"].port is None:
        if options["ARGS"].servertype == "MSSQL":
            options["ARGS"].port = "1433"
        elif options["ARGS"].servertype == "PSQL":
            options["ARGS"].port = "5432"
        elif options["ARGS"].servertype == "MYSQL":
            options["ARGS"].port = "3306"
        elif options["ARGS"].servertype == "ORACLE":
            options["ARGS"].port = "1521"
        else:
            pass  # We're assuming SQLITE

        if options["ARGS"].quiet is None:
            print(f"Defaulting to port {options['ARGS'].port}")


def print_opts(opts: Dict) -> None:
    """Dump options info out to the screen"""
    console = Console()
    console.print(opts)
