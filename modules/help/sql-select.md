# Help Using SQL - SELECT statement
SQL is the lingua franca of the database world.  Here are some quick hints to help you in writing queries.
**SELECT**
SELECT col1, col2, ..., coln
FROM table1
JOIN table2 on table1.col = table2.col
WHERE **conditions**
GROUP BY col1, ..., coln
HAVING **conditions**
ORDER BY col ASC|DESC
##
**conditions** are a set of tests to restrict the data being returned.
In the case of the WHERE clause this applies to the values in table columns and can
include subqueries.  Subqueries can also include references to columns from the enclosing query
and this is known as a correlated subquery.
## 
In the case of the HAVING clause, the tests apply to the aggregates you created via the GROUP BY clause.
##
##
