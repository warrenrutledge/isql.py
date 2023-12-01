# Help Using SQL - INSERT statement
SQL is the lingua franca of the database world.  Here are some quick hints to help you in writing queries.
**INSERT**
INSERT INTO table
(col1, col2, ..., coln)
VALUES
(val1, val2, ..., valn)
##
You can also populate a table from a SELECT statement like so:
INSERT INTO table
(col1, col2, ..., coln)
SELECT col1, col2, ..., coln
FROM table1
JOIN table2 on table1.col = table2.col
WHERE **conditions**
##
**NOTE** isql.py sets the connection to the database to autocommit
This means that each transaction, such as an insert statement is 
committed to the database once the action is complete.  If you want
to manually control the commits, you need to issue a BEGIN TRANSACTION 
command prior to running your insert.  Then, when you are done, you
will need to issue a COMMIT command to have all the work committed to 
the database.
##
