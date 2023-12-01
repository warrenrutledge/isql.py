# Help Basic Interactive Commands
 **connect** <database name> connects/reconnects to the server, used to change database on postgres
 **exit** closes the connections and exits isql.py
 **help** shows this screen, use ***help about*** for more information on this program
 **history** lists the history array
 **redisplay** show the last result set again (doesn't run the query)
 **reparse** reload the config file, reparse ARGS, and reconnect to the server using those settings
 **reset** sets the buffer to null and line counter to 1
## Change Output Settings
 **:**<cmd> changes output settings, ***help output*** for more
## Reload Command History
 **!**<history array item> loads the command into the current buffer
## Work with snippets
**#list** lists the loaded snippets (these are by servertype)
**#**<snippet name> will load the snippet text into the sql buffer
## Interact With Shell
 **@**<cmd> support interactions with other programs
 **@cd** <dir> changes the working directory for the program
 **@def** <env var>=<value> sets an enviornment variable such as EDITOR
 **@edit** [history #] loads the sql buffer or history entry into $EDITOR and reloads it on exit
 **@exec** <file> loads a file and executes it line by line
 **@load** <file> loads a file into the sql buffer
##
