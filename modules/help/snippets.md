# Help About Snippets
isql.py has a feature called snippets that cache SQL statements (per platform).
Snippets are used to hold quick queries that might help an administrator.
######
On first startup, isql.py will create the snippets directory in the user's home directory/.isql
Under the snippets directory, you will find a directory for MSSQL, MYSQL, and PSQL
######
In the isql program, you can enter **#list** to see the snippets loaded in your program.
To use one, just enter **#snippetname** and the snippet will be loaded into your SQL buffer and 
displayed on the screen.  Just enter **go** to run.  You can also edit it using **@edit**.
The edits you make only apply to that buffer.  To make permanent changes, you'll need to update
the code in your snippets directory.
######
##
