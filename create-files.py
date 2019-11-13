import requests
import json
import os

previous_points = {}


def create_players(players):
    with open('players.txt', 'w') as outfile:
        json.dump(players, outfile)


def get_detailed_players(player_id):
    r = \
        requests.get(url='https://fantasy.premierleague.com/api/element-summary/'
                      + player_id + '/')
    overview_JSON = r.json()
    if 'detail' in overview_JSON and overview_JSON['detail'] \
        == 'Not found.':
        return 50.437
    elif 'history_past' in overview_JSON \
        and overview_JSON['history_past']:

  # elif 'history_past' in overview_JSON and overview_JSON['history_past'] and 'season_name' in overview_JSON['history_past']:

        history = overview_JSON['history_past']
        found_season = False
        for season in history:
            if season['season_name'] == '2018/19':
                found_season = True
                return season['total_points']
        if found_season == False:
            return 50.437
    else:
        return 50.437


def create_previous_points(number_players):
    seasons = {'past_season_points': {}}
    total = 0
    with open('players.txt') as json_file:
        data = json.load(json_file)
        for d in data:
            x = get_detailed_players(str(d['id']))
            total += x
            seasons['past_season_points'][d['id']] = x

    with open('previous_points.txt', 'a') as outfile:
        json.dump(seasons, outfile)

  # Create previous points JSON file

    if os.path.exists('prev_average.txt') == False:
        with open('prev_average.txt', 'w') as outfile:
            json.dump(round(total / number_players, 3), outfile)


def main():
    r = \
        requests.get(url='https://fantasy.premierleague.com/api/bootstrap-static/'
                     )
    overview_JSON = r.json()
    players = overview_JSON['elements']

  # Create initial players JSON file

    if os.path.exists('players.txt') == False:
        create_players(players)

  # Create previous points JSON file

    if os.path.exists('previous_points.txt') == False:
        create_previous_points(len(players))

main()
