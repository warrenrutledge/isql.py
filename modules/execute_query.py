""" process the query and display the output """
import time
from typing import Iterable, Dict
from prettytable import from_db_cursor
from rich.console import Console
from rich.table import Table
import modules.output_fun as of
import modules.substitute_vars as sv

console = Console()


def formatted_output(options: Dict) -> None:
    """Common code for formatted output via csv, pretty or rich"""
    headers = options["CURSOR"].description
    if headers is not None:
        while True:
            if options["OUTPUT_CSV"] is True:
                csv_output(headers, options)
            elif options["OUTPUT_METHOD"] == "pretty":
                pretty_output(headers, options)
            elif options["OUTPUT_METHOD"] == "rich":
                rich_output(headers, options)

            if options["ARGS"].servertype == "MSSQL":
                # Handle multiple result sets under MSSQL
                if not options["CURSOR"].nextset():
                    break
                headers = options["CURSOR"].description
            else:
                break


def csv_output(headers: Iterable, options: Dict) -> None:
    """Handle the output to csv file"""
    headerline = []
    for head in headers:
        headerline.append(head[0])
    test = of.write_output_file(headerline, options)
    records = options["CURSOR"].fetchall()
    if test != 100:  # 100 is a magic number & means we have no output file
        for rec in records:
            of.write_output_file(rec, options)
        console.print("Output written to output file", style="b r")


def pretty_output(_, options: Dict) -> None:
    """Send output to pretty printer"""
    tbl = from_db_cursor(options["CURSOR"])
    # Make sure we have results to format
    if tbl is not None:
        tbl.set_style(options["OUTPUT_STYLE"])
        tbl.align = options["OUTPUT_ALIGN"]
        tbl.header = options["OUTPUT_HEADER"]
        tbl.border = options["OUTPUT_BORDER"]
        tbl.header_style = options["HEADER_STYLE"]
        if options["PAGER"] is True:
            # We aren't using the rich format, just the pager
            with console.pager():
                console.print(str(tbl))
        else:
            print(tbl)
        of.write_cache(str(tbl), options)
        if options["ARGS"].output is not None:
            of.write_output_file(str(tbl), options)


def rich_output(headers: Iterable, options: Dict) -> None:
    """Send output to the rich console"""
    records = options["CURSOR"].fetchall()
    table = Table()
    for head in headers:
        table.add_column(head[0])
    for rec in records:
        # We don't support writing rich out to output file
        # We have to map str on to rec tuple and then unpack it
        table.add_row(*map(str, rec))
    of.write_cache(str(table), options)
    if options["PAGER"] is True:
        with console.pager():
            console.print(table)
    else:
        console.print(table)


def default_output(options: Dict) -> None:
    """Just print the column name and value for each result"""
    headers = options["CURSOR"].description
    records = options["CURSOR"].fetchall()
    buffer = ""
    row_sep = "-----------------------------"
    for rec in records:
        for i, value in enumerate(rec):
            if options["PAGER"] is True:
                # We have to buffer to use the pager
                buffer += f"{headers[i][0]} :: {value}\n"
            else:
                print(f"{headers[i][0]} :: {value}")
            if options["ARGS"].output is not None:
                of.write_output_file(f"{headers[i][0]} :: {value}\n", options)
        # Write the row boundary marker
        if options["PAGER"] is True:
            buffer += row_sep + "\n"
        else:
            print(row_sep)
        if options["ARGS"].output is not None:
            of.write_output_file(row_sep + "\n", options)

    if options["PAGER"] is True:
        # We aren't using the rich format, just the pager
        with console.pager():
            console.print(buffer)


def submit_query(options: Dict) -> None:
    """A basic query execution function"""
    values = sv.analyze_query(options)
    of.write_logfile(options["SQL_BUFFER"], options, no_print=True)
    start = time.perf_counter()
    try:
        if not values:
            options["CURSOR"].execute(options["SQL_BUFFER"])
        else:
            # We found variables that needed to be substituted
            options["CURSOR"].execute(options["SQL_BUFFER"], values)
        querystop = time.perf_counter()

        if (
            options["OUTPUT_CSV"] is True
            or options["OUTPUT_METHOD"] == "pretty"
            or options["OUTPUT_METHOD"] == "rich"
        ):
            formatted_output(options)
        else:
            default_output(options)

        if options["ARGS"].quiet is not True:
            final = time.perf_counter()
            diff = querystop - start
            tot = final - start
            of.write_logfile(
                f"Rows returned = {options['CURSOR'].rowcount} \
                    \tQuery time elapsed = {diff:.4f} \
                    \tTotal time elapsed = {tot:.4f}",
                options,
            )
    except Exception as err:
        # We have to be generic because we support multiple DBMS libraries
        of.write_logfile(f"Error: {err}", options, iserr=True)
        of.write_logfile(
            f"Error generated by {options['SQL_BUFFER']}", options, iserr=True
        )
        options["ERROR"] = True
