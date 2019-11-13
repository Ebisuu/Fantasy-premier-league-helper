import os
from operator import itemgetter
import json
import random


# Calc Average ppm for players

def calc_average(list):
    average = 0
    for item in list:
        average += item['ppm']
    return round(average / len(list), 2)


# Calc best players based on their price per million, takes in Bool argument if you want to consider last seasons points.

def calc_best_players(previous_points):
    price_per_mil_list = []

  # open players.txt file with information and loop through players

    with open('players.txt') as json_file:
        data = json.load(json_file)

    # only use this code block if a user passes wishes to include previous points in the calculations

        if previous_points == True:
            with open('previous_points.txt') as json_file:
                more_data = json.load(json_file)
                for player in data:
                    prev_points = more_data['past_season_points'
                            ][str(player['id'])]
                    current_points = player['total_points']

                # need to update this to be dynamic rather than current_points * 12(number of games played this season)

                    weighted_points = (prev_points * 38
                            + current_points * 12) / 40
                    ppm = round(weighted_points / player['now_cost'], 3)
                    price_per_mil_list.append({
                        'name': player['first_name'] + ' '
                            + player['second_name'],
                        'cost': player['now_cost'] / 10,
                        'ppm': ppm,
                        'position': get_position(player['element_type'
                                ]),
                        'injured': player['news'],
                        'team': get_team(player['team']),
                        })
        else:

    # Only consider data from this season

            for player in data:
                current_points = player['total_points']
                ppm = round(current_points * 10 / player['now_cost'], 3)
                price_per_mil_list.append({
                    'name': player['first_name'] + ' '
                        + player['second_name'],
                    'cost': player['now_cost'] / 10,
                    'ppm': ppm,
                    'position': get_position(player['element_type']),
                    'injured': player['news'],
                    'team': get_team(player['team']),
                    })

  # sort the list for highest price_per_mil players are first

    sorted_list = sorted(price_per_mil_list, key=itemgetter('ppm'),
                         reverse=True)
    return sorted_list

# print the top x number of players from a given array, limit parameter being the number of players to print out.

def print_top(sorted_list, limit):
    count = 0
    print '=' * 50 + ' Top 50 ' + '=' * 50
    for player in sorted_list:
        if count < limit:
            print (player['name'] + ':', player['ppm'], '||',
                   player['position'])
            count += 1
        else:
            break


# print the top x number of players from a given array, given a certain position e.g. strikers

def print_best_position(sorted_list, limit, position):
    count = 0
    print '=' * 50 + ' Top ' + str(limit) + ' ' + position + '=' * 50
    keyValList = [position]
    positionList = list(filter(lambda d: d['position'] in keyValList,
                        sorted_list))
    for player in positionList:
        if count < limit:
            if len(player['injured']) != 0:
                print (player['name'] + ':', player['ppm'], '-' * 5,
                       player['injured'], '-' * 5)
            else:
                print (player['name'] + ':', player['ppm'])
            count += 1
        else:
            break


# convert position given as a number from FPL API to a leigible position
# Potentially change to a switch?

def get_position(x):
    position = ''
    if x == 1:
        position = 'Goalkeeper'
    elif x == 2:
        position = 'Defender'
    elif x == 3:
        position = 'Midfielder'
    elif x == 4:
        position = 'Forward'
    else:
        position = 'Unknown'
    return position


# Create a dictionary of teams as FPL API returns a numeric value. Use this number as the key, and map a value to a legibile team name

def get_team(x):
    teamNames = {
        '1': 'Arsenal',
        '2': 'Aston Villa',
        '3': 'Bournemouth',
        '4': 'Brighton & Hove Albion',
        '5': 'Burnley',
        '6': 'Chelsea',
        '7': 'Crystal Palace',
        '8': 'Everton',
        '9': 'Leicester City',
        '10': 'Liverpool',
        '11': 'Manchester City',
        '12': 'Manchester United',
        '13': 'Newcastle United',
        '14': 'Norwich City',
        '15': 'Sheffield United',
        '16': 'Southampton',
        '17': 'Tottenham Hotspur',
        '18': 'Watford',
        '19': 'West Ham United',
        '20': 'Wolverhampton Wanderers',
        }
    return teamNames[str(x)]


# Use this to get premium players, AKA most expensive players to use for picking team algorithm

def get_prem_players(players):
    prem_players = []
    for player in players:
        prem_players.append(player)

    # print(players)

    top_players = sorted(prem_players, key=itemgetter('cost'),
                         reverse=True)
    return top_players[0:20]


def injured_players(players):
    injured = []
    for player in players:
        if len(player['injured']) != 0:
            injured.append(player)
    return injured


# Pick a team algorithm given 100million budget.
# Work in progress, potentially need to use DP, similar to coin change problem???

def pickTeam(
    budget=100,
    star_player_limit=3,
    gk=2,
    df=5,
    md=5,
    fwd=3,
    ):
    best_players = calc_best_players(False)
    prem_players = get_prem_players(best_players)
    prem_players_picked = 0
    picked_team = []
    positions = {
        'Goalkeeper': gk,
        'Defender': df,
        'Midfielder': md,
        'Forward': fwd,
        }
    teams = {}
    injured = injured_players(best_players)

  # pick the premium players

    while star_player_limit > 0:
        picked = random.choice(prem_players[0:10])
        if picked['team'] not in teams:
            teams[picked['team']] = 0
        if picked['injured'] == '' and picked not in picked_team and picked not in injured:
            star_player_limit -= 1
            picked_team.append(picked)
            budget -= picked['cost']
            teams[picked['team']] += 1
    cost_average = budget / (15 - len(picked_team))

  # pick rest of the squad

    for player in best_players:

    # print(teams)

        if player['team'] not in teams:
            teams[player['team']] = 0
        if player not in picked_team and player not in injured and player['cost'] <= budget and player['cost'] <= cost_average + 2 and positions[player['position']] > 0 and teams[player['team']] < 3:
            picked_team.append(player)
            positions[player['position']] -= 1
            budget -= player['cost']
            teams[picked['team']] += 1
            if len(picked_team) < 15:
                cost_average = budget / (15 - len(picked_team))
    return picked_team


def main():

    # Create sorted list of players based on price_per_million using this season data only

    best_players = calc_best_players(False)

    print_top(best_players, 50)
    print_best_position(best_players, 20, 'Goalkeeper')
    print_best_position(best_players, 20, 'Defender')
    print_best_position(best_players, 20, 'Midfield')
    print_best_position(best_players, 20, 'Forward')


main()
