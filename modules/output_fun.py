""" output functions """
import datetime as dt
from typing import Union, Dict, List
import logging
import logging.handlers
import tempfile
import csv
import pickle
from rich.console import Console
from rich.panel import Panel

console = Console()


def set_logger(options: Dict) -> None:
    """set up the logger"""
    options["LOG_FILENAME"] = f"{options['LOG_PATH']}/isql.log"

    isql_log = logging.getLogger("Logger")
    isql_log.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        filename=options["LOG_FILENAME"], maxBytes=65536, backupCount=5,
    )
    isql_log.addHandler(handler)
    options["LOG_HANDLER"] = isql_log


def write_message(text: str, options: Dict) -> None:
    """write messages but never to log"""
    if options["OUTPUT_METHOD"] == "rich":
        console.print(Panel(text, expand=False, border_style="white"))
    else:
        print(text)


def write_logfile(
    text: str, options: Dict, no_print: bool = False, iserr: bool = False
) -> None:
    """provide a common function for logging"""
    if no_print is False:
        if options["OUTPUT_METHOD"] == "rich":
            if iserr is False:
                if options["ARGS"].quiet is False:
                    console.print(text, style="bold")
            else:
                error_console = Console(style="bold italic red")
                error_console.print(Panel(text, expand=False, border_style="red"))
        else:
            if options["ARGS"].quiet is False:
                print(text)
    timestamp = dt.datetime.today()
    line = f"{timestamp}:{options['ARGS'].user}:{text}"
    options["LOG_HANDLER"].info(line)


def write_output_file(buffer: Union[List, str], options: Dict) -> int:
    """handle -o flag output"""
    if options["ARGS"].output is None:
        print("No output file defined")
        return 100

    if options["OUTPUT_CSV"] is True:
        with open(options["ARGS"].output, "a", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(buffer)
    else:
        with open(options["ARGS"].output, "a", encoding="utf-8") as outfile:
            outfile.write(str(buffer))

    return 0


def write_cache(data: str, options: Dict) -> None:
    """write results to a cache that we can reuse"""
    if "RESULTS_CACHE_NAME" not in options:
        with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as t_file:
            options["RESULTS_CACHE_NAME"] = t_file.name

    with open(options["RESULTS_CACHE_NAME"], "wb", encoding=None) as t_file:
        pickle.dump(data, t_file)


def read_cache(options: Dict) -> str:
    """read cache and return the results"""
    if "RESULTS_CACHE_NAME" not in options:
        print("No results to redisplay")
        res = ""
    else:
        print("** Fetching from cache **")
        with open(options["RESULTS_CACHE_NAME"], "rb", encoding=None) as cache:
            res = pickle.load(cache)

    return res
