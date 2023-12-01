""" parse command line input """
import os
from typing import Dict, List, Tuple
import time
import numbers
import modules.output_fun as of
import modules.shell as sh
import modules.output_settings as op
import modules.execute_query as eq


def process_input_file(options: Dict, filename: str = "") -> None:
    """handle -i flag inputfile"""
    if filename == "":
        if options["ARGS"].input is not None:
            filename = options["ARGS"].input
        else:
            of.write_logfile("Error: No file provided", options)
            return

    try:
        with open(filename, "r") as file:
            for line in file:
                process_input(options, [line[0:-1]])
    except OSError as err:
        of.write_logfile(f"Error: {err}", options)


def handle_go_options(tokens: List, options: Dict) -> Tuple[int, int]:
    """Parse support options for running the query"""
    repeat = 1
    pause = 0
    token_cnt = len(tokens)
    if token_cnt == 1:  # There are no more arguments
        return repeat, pause

    if tokens[1] == ">":
        options["ARGS"].output = tokens[2]
        if options["OUTPUT_METHOD"] == "rich":
            if options["OUTPUT_CSV"] is False:
                print("** NOTE: rich output not written to output file **")
                print("** Change to pretty, default, or set CSV **")
    elif isinstance(int(tokens[1]), numbers.Number):
        repeat = int(tokens[1])
        if token_cnt > 2:
            if tokens[2].lower() == "wait":
                if token_cnt > 3:
                    if tokens[3].isdigit() is True:
                        pause = int(tokens[3])
                else:
                    raise ValueError("Invalid wait time specified")

    return repeat, pause


def go_function(options: Dict, tokens: List) -> None:
    """Go signals us to execute the SQL Buffer"""
    # End the batch, append to history and then execute the query,
    # reset buffers and line counters
    options["HISTORY"].append(options["SQL_BUFFER"])
    tmp_out = options["ARGS"].output
    options["SIG_INT"] = False
    options["ERROR"] = False
    try:
        repeat, pause = handle_go_options(tokens, options)
        # check for repeat and continue unless we get an interrupt or error
        while (repeat != 0) and (not options["SIG_INT"]) and (not options["ERROR"]):
            eq.submit_query(options)
            repeat = repeat - 1
            if repeat != 0:
                time.sleep(pause)
    except ValueError as err:
        of.write_logfile(f"Error: {err}", options)
    options["LINE_NO"] = 1
    options["SQL_BUFFER"] = ""
    options["ARGS"].output = tmp_out


def get_history(tokens: List, options: Dict) -> None:
    """Take the query from history and make it the buffer,
    increment the line count"""
    if tokens[0][1].isdigit() is True:  # Use the buffer provided
        options["SQL_BUFFER"] = options["HISTORY"][int(tokens[0][1:])]
        print(options["SQL_BUFFER"])
        options["LINE_NO"] += 1
    elif tokens[0][1] == "!":  # Use last command
        options["SQL_BUFFER"] = options["HISTORY"][-1]
        print(options["SQL_BUFFER"])
        options["LINE_NO"] += 1
    else:
        print(f"Unknown option {tokens[0]}")


def shell_out(input_line: str, options: Dict) -> None:
    """support shell commands including some built ins"""
    if input_line[1:5].lower() == "edit":
        sh.invoke_editor(str(input_line[5:].strip()), options)
    elif input_line[1:3].lower() == "cd":
        try:
            os.chdir(input_line[3:].strip())
        except OSError as err:
            print(f"Error: {err}")
    elif input_line[1:5].lower() == "load":
        sh.load_file(input_line[5:].strip(), options)
    elif input_line[1:5].lower() == "exec":
        process_input_file(options, filename=input_line[5:].strip())
    elif input_line[1:4].lower() == "def":
        key, value = input_line[4:].split("=")
        os.putenv(key.strip(), value.strip())
    else:
        sh.invoke_os_command(input_line[1:], options)


def get_snippet(tokens: List, options: Dict) -> None:
    """Check for a snippet and load if found"""
    cmd = tokens[0][1:].strip()
    if cmd in options["CACHE"]:
        options["SQL_BUFFER"] += "".join(options["CACHE"][cmd])
        print(options["SQL_BUFFER"])
        options["LINE_NO"] += 1
    elif cmd.lower() == "list":
        for name in options["CACHE"]:
            print(name)
    else:
        print(f"{cmd} is not in snippet code cache")


def process_input(options: Dict, tokens: List) -> None:
    """handle the special cases of input looking for a leading glyph
    to call a special case function or default append to SQL Buffer"""
    if tokens[0][0] == "!":
        get_history(tokens, options)
    elif tokens[0][0] == ":":
        # user wants to change options for output
        op.set_options(tokens, options)
    elif tokens[0][0] == "@":
        shell_out(" ".join(tokens), options)
    elif tokens[0][0] == "#":
        get_snippet(tokens, options)
    else:
        # Default case, we just add the line to our buffer
        # and increment the line count
        options["SQL_BUFFER"] = options["SQL_BUFFER"] + " ".join(tokens) + "\n"
        options["LINE_NO"] += 1
