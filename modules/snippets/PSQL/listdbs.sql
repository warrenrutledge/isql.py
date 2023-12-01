select datname name, usename owner, datcollate collate
from pg_database 
inner join pg_user on pg_database.datdba = pg_user.usesysid
