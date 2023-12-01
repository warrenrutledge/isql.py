""" Manage connections to databases """
import sys
from collections.abc import Callable
from typing import Any, Dict, Iterable
import sqlite3
import pymssql
import psycopg2
import mysql.connector
import oracledb
import modules.output_fun as of


def build_msg_handler(opts: Dict) -> Callable[[int, int, str, bytes, int, bytes], None]:
    """This code is only used by MSSQL or potentially Sybase ASE"""

    # We need opts for printing the output, but the callback won't pass it
    # So we define the function here with the opts and return the function
    # reference

    def msg_handler(
        msgstate: int, severity: int, _: str, procname: bytes, line: int, msgtext: bytes
    ) -> None:
        """_ is servername"""
        d_msgtext = msgtext.decode("utf-8")
        d_procname = procname.decode("utf-8")
        tokens = d_msgtext.split(" ")
        if severity > 10:  # Will be raised as errors and handled there
            return
        if d_msgtext.strip() == "":  # No message, skip it
            return
        if tokens[0] == "Changed":  # Changing database, no need to say it
            return

        if msgstate != 0 and severity != 0:
            of.write_message(f"state={msgstate}, sev={severity}", opts)
        of.write_message(f"{d_procname}:line {line}:\n{d_msgtext}", opts)

    # Returning the msg_handler creates a closure for use in other functions
    return msg_handler


def parameters(opts: Dict) -> Dict:
    """Determine the parameters needed for connection string"""
    if opts["ARGS"].servertype == "SQLITE":
        ret_val = {
            "database": opts["ARGS"].sqlitedb,
        }
    else:
        std_args = {
            "host": opts["ARGS"].server,
            "port": opts["ARGS"].port,
            "user": opts["ARGS"].user,
            "password": opts["ARGS"].password,
            "database": opts["ARGS"].database,
        }
        # Now, we augment as needed by the specific handler
        if opts["ARGS"].servertype == "MSSQL":
            std_args["server"] = std_args["host"]
            del std_args["host"]  # Server is used rather than host
            std_args["appname"] = "isql.py"
        elif opts["ARGS"].servertype == "PSQL":
            std_args["application_name"] = "isql.py"
        elif opts["ARGS"].servertype == "MYSQL":
            std_args["autocommit"] = True
            std_args["raise_on_warnings"] = True
        elif opts["ARGS"].servertype == "ORACLE":
            del std_args["database"]
            std_args["service_name"] = opts["ARGS"].database
            std_args["encoding"] = "UTF-8"

        ret_val = std_args

    return ret_val


class ConnectionDispatchTable:
    """This is effectively a switch/case statement
    to build the connection string based on the servertype"""

    dispatch = {
        "MSSQL": pymssql.connect,
        "MYSQL": mysql.connector.connect,
        "PSQL": psycopg2.connect,
        "SQLITE": sqlite3.connect,
        "ORACLE": oracledb.connect,
    }

    def list_supported_type(self) -> Iterable:
        """ Return the supported connection types """
        return self.dispatch.keys()

    def run(self, cmd: str, opts: Dict) -> Any:
        """exec the function pointed to by cmd in dispatch"""
        if cmd in self.dispatch.keys():
            try:
                params = parameters(opts)
                return self.dispatch[cmd](**params)
            except Exception as err:
                of.write_logfile(f"Error: {err}", opts)
                sys.exit(1)
        else:
            print(f"Unknown connection type: {cmd}")
            sys.exit(1)


def connect(options: Dict, value: bool = False) -> None:
    """connect to database server and create a cursor"""
    of.write_logfile("Establishing connection to server", options, no_print=value)
    dispatch = ConnectionDispatchTable()
    options["CONN"] = dispatch.run(options["ARGS"].servertype, options)

    # Set connection parameters
    if options["ARGS"].servertype == "SQLITE":
        sqlite3.paramstyle = "named"
    elif options["ARGS"].servertype == "MSSQL":
        options["CONN"].autocommit(True)
        options["CONN"]._conn.set_msghandler(build_msg_handler(options))
    elif options["ARGS"].servertype == "PSQL":
        options["CONN"].autocommit = True
    elif options["ARGS"].servertype == "ORACLE":
        options["CONN"].autocommit = True
    elif options["ARGS"].servertype == "MYSQL":
        # No extra options for MYSQL
        pass

    options["CURSOR"] = options["CONN"].cursor()


def disconnect(options: Dict) -> None:
    """close everything up cleanly from the database"""
    of.write_logfile("Disconnecting from server", options, no_print=True)
    options["CURSOR"].close()
    options["CONN"].close()


def get_dbname(options: Dict) -> str:
    """Get the current database"""
    database = ""
    select_stmt = ""
    if options["ARGS"].servertype == "MSSQL":
        select_stmt = "select db_name()"
    elif options["ARGS"].servertype == "PSQL":
        select_stmt = "select current_database()"
    elif options["ARGS"].servertype == "MYSQL":
        select_stmt = "select database()"
    elif options["ARGS"].servertype == "ORACLE":
        select_stmt = "select sys_context('userenv', 'instance_name') from dual"

    if select_stmt != "":
        try:
            options["CURSOR"].execute(select_stmt)
            rows = options["CURSOR"].fetchall()
            if rows[0][0] is not None:
                database = rows[0][0]
        except Exception:  # If we get an exception here, we've lost connection
            if options["ERROR"]:
                options["ERROR"] = False
                connect(options)

    return database


def get_prompt(options: Dict) -> str:
    """walk through the components of the prompt and build it"""
    f_string = options["PROMPT"]
    if f_string == "":
        f_string = "[$t|$s|$u|$d]::$n>"
    prompt = ""
    prompt_vars = {
        "s": options["ARGS"].server,
        "d": get_dbname(options),
        "t": options["ARGS"].servertype,
        "n": str(options["LINE_NO"]),
        "u": options["ARGS"].user,
        "f": options["OUTPUT_METHOD"],
    }

    pos = 0
    f_len = len(f_string)
    while pos < f_len:
        f_char = f_string[pos]
        pos += 1
        if f_char == "$":
            if pos == f_len:
                print("Error: format is incomplete")
            else:
                try:
                    prompt = prompt + prompt_vars[f_string[pos]]
                except LookupError:
                    # We are using the $ as an escape for $
                    prompt = prompt + f_string[pos]
                pos += 1
        else:
            prompt = prompt + f_char

    return f"{prompt}"
