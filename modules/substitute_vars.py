""" Handle the ability to support placeholders in sql
and substitute for values """
import re
from typing import Union, Dict, Tuple
from rich.console import Console


console = Console()


def analyze_query(options: Dict) -> Union[Dict, Tuple]:
    """Find all the variable definitions and substitute for them"""
    # Our variables are bracketed by : like :var:
    matches = re.findall(r":.+:", options["SQL_BUFFER"])
    if options["ARGS"].servertype in ("ORACLE", "SQLITE"):
        # SQLITE supports named substitutions which I prefer
        local_vars = {}
        if matches:
            # We will prompt for the values for each variable
            for item in matches:
                local_vars[item[1:-1]] = console.input(f"{item}? ")
            for item in matches:
                options["SQL_BUFFER"] = re.sub(
                    item, f":{item[1:-1]}", options["SQL_BUFFER"]
                )
        ret_val = local_vars
    else:  # options["ARGS"].servertype in ("MSSQL", "PSQL", "MYSQL"):
        local_var_list = []
        if matches:
            # We will prompt for the values for each variable
            for item in matches:
                local_var_list.append(console.input(f"{item}? "))
            for item in matches:
                options["SQL_BUFFER"] = re.sub(item, "%s", options["SQL_BUFFER"])
        ret_val = tuple(local_var_list)

    return ret_val
