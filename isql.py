#!/usr/bin/env python3
"""
  **********************************************************
    Interactive SQL app
    Supports MSSQL, ASE, Postgresql, MySQL, SQLITE3, ORACLE
    author: Warren L. Rutledge
    date: 19 Sep 2023
  **********************************************************
  Copyright (C) 2023 Warren L Rutledge - All Rights Reserved
  You may use, distribute and modify this code under the
  terms of the GPL v3 license.
  **********************************************************
  Edited with gvim and neovim
"""
import signal
import sys
import os
import readline
from rich.console import Console
import modules.env_vars as ev
import modules.dispatch as dp
import modules.process_input as pi
import modules.output_fun as of
import modules.connection as cn
import modules.snippets as sn


def signal_handler(sig, frame):
    """Handle the case of control c to kill a query"""
    of.write_logfile(f"{sig} caught:{frame}", options)
    cn.disconnect(options)
    options["SIG_INT"] = True  # Set a flag to let other routines know
    cn.connect(options)


# Start of main program

# Set readline to support vi editing commands
readline.parse_and_bind("set editing-mode vi")

options = ev.build_options()
options["CACHE"] = sn.get_snippet_list(options)

console = Console()

of.set_logger(options)
of.write_logfile(f"Starting isql with {sys.argv}", options, no_print=True)

# Establish connection
cn.connect(options, True)

# Install our signal handler for Control C
signal.signal(signal.SIGINT, signal_handler)

# Set up our dispatch table object for internal commands
dispatch_table = dp.DispatchTable()

IN_LINE = ""

# If we were passed an input file, process it
# This could be for setting things the way you want
if options["ARGS"].input is not None:
    pi.process_input_file(options)

# If we got passed a query on the command line via -Q
# run the query, then exit
if options["ARGS"].query is not None:
    pi.process_input(options, [options["ARGS"].query])
    dispatch_table.run("go", options, ["go"])  # Execute query
    IN_LINE = "exit"

# Main processing loop
while IN_LINE.lower() != "exit":
    tokens = IN_LINE.split(" ")
    if tokens[0] == "":
        # Skip blank lines
        pass
    else:
        dispatch_table.run(tokens[0].lower(), options, tokens)

    # Prompt user for input
    # The rich input is acting weird, so I'm not using it right now
    #if options["OUTPUT_METHOD"] == "rich":
    #    IN_LINE = console.input(f"[i bold]{cn.get_prompt(options)}[/]")
    #else:
    IN_LINE = input(f"{cn.get_prompt(options)}")

# Clean up
cn.disconnect(options)
if "RESULTS_CACHE_NAME" in options:
    os.remove(options["RESULTS_CACHE_NAME"])
of.write_logfile("Exiting isql.py", options, no_print=True)
