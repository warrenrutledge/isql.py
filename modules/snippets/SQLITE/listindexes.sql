select name, tbl_name from sqlite_schema
where type = 'index'
and tbl_name like ':tbl_name:'
and name like ':idx_name:'
order by name
