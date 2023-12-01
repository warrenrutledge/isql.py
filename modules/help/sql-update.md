# Help Using SQL - UPDATE statement
SQL is the lingua franca of the database world.  Here are some quick hints to help you in writing queries.
**UPDATE**
UPDATE table
SET col1 = val1, col2 = val2, ..., coln = valn
WHERE **conditions**
##
You can also provide values from a JOIN
UPDATE table
SET col1 = table1.val1, col2 = table2.val2, ..., coln = tablen.valn
FROM table1
JOIN table2 on table1.col = table2.col
WHERE **conditions**
##
**NOTE** isql.py sets the connection to the database to autocommit
This means that each transaction, such as an update statement is 
committed to the database once the action is complete.  If you want
to manually control the commits, you need to issue a BEGIN TRANSACTION 
command prior to running your insert.  Then, when you are done, you
will need to issue a COMMIT command to have all the work committed to 
the database.
##
