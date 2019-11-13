# Fantasy-premier-league-helper
Tool to help calculate best value for points team. Moneyball-esque

#Create-files.py
Create-files.py file first to create files to work on, will need to re-run every time you need new data. If added to a server run a cron job once every day.
We create the files to reduce the amount of calls to the API and try to avoid request limit.

#best_players.py
File calculates and prints out the best value players for points

#INSTRUCTIONS
1. Run create-files.py
2. Run best_players.py
