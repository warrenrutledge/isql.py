# Help Using Variables in SQL
isql.py supports queries using parameter substitution.  A variable that you want to substitute looks like this
**:var_name:**
Here is an example query:
##
select name, tbl_name from sqlite_schema
where type = 'index'
and tbl_name like :tbl_name:
and name like :idx_name:
order by name
##
When that query is run, the SQL is scanned and isql.py prompts you for the values of
**:tbl_name:** and **:idx_name:**
The query is then rewritten to support the specific types of substitution allowed for the database connector and
the values provided by the user are returned so they can be included in the execution of the query.
##
These can be used in snippets or just in commands you type in.  Using variable substitution in snippets
works much like stored procedures though requiring interaction with the user.
##
