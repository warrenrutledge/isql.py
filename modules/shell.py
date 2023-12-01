""" command line processing """
import os
from typing import Dict
import tempfile
import modules.output_fun as of


def invoke_editor(mode: str, options: Dict) -> str:
    """Allow the user to invoke terminal text editor"""
    of.write_logfile("Invoking external editor", options)
    try:
        editor = os.environ["EDITOR"]
    except KeyError:
        of.write_logfile("No EDITOR environment variable defined", options)
        return ""

    if mode != "":
        # Do some error checking before hitting the main code
        if mode.isnumeric() is False:
            print("Error: must pass either blank or number of history buffer")
            return ""
        if int(mode) >= len(options["HISTORY"]):
            print("Error: History buffer index out of range")
            return ""

    try:
        # We don't use with here because we need to store the tempfile handle
        # We also have a specific cleanup for it in our exit code
        tsqlfile = tempfile.NamedTemporaryFile(
            mode="w", buffering=-1, suffix=".sql", delete=False
        )
    except OSError as err:
        print(f"Error: {err}")
        return ""

    if mode == "":
        # We're writing the buffer contents to the temp file
        tsqlfile.write(options["SQL_BUFFER"])
    else:
        # We're writing a history buffer to the temp file
        tsqlfile.write(options["HISTORY"][int(mode)])
    tsqlfile.close()

    try:
        # Open the tempfile using the editor, we used .sql as the file
        # extension so that if the editor support syntax highlighting
        # it will just work.
        os.system(f"{editor} {tsqlfile.name}")
    except OSError as err:
        of.write_logfile(f"ERROR: {err}", options)

    # Once the editor exits, we reload the contents of the tempfile
    # into our SQL buffer as line 1
    load_file(tsqlfile.name, options)

    # Clean up the tempfile
    try:
        os.unlink(tsqlfile.name)
    except OSError as err:
        of.write_logfile(f"Error: {err}", options)

    return options["SQL_BUFFER"]


def invoke_os_command(command: str, options: Dict) -> None:
    """Simple function to shell out and run command, no return value"""
    try:
        os.system(command)
    except OSError as err:
        of.write_logfile(f"Error: {err}", options)


def load_file(fname: str, options: Dict) -> str:
    """Load the contents of a file into the SQL buffer
    This replaces the existing contents of the buffer with
    the contents of the file.
    """
    try:
        with open(fname, "r", encoding="utf-8") as file:
            options["SQL_BUFFER"] = file.read()
            print(options["SQL_BUFFER"])
            options["LINE_NO"] = 2
    except OSError as err:
        of.write_logfile(f"Error: {err}", options)

    return options["SQL_BUFFER"]
