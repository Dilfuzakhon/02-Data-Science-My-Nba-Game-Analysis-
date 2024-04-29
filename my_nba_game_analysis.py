import re
import pandas as pd


def analyse_nba_game(play_by_play_moves):
    home_team = {"name": "", "players_data": {}}
    away_team = {"name": "", "players_data": {}}

    for line in play_by_play_moves:
        data = {"FG": 0, "FGA": 0, "3P": 0, "3PA": 0, "FT": 0, "FTA": 0,
                "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0,
                "TOV": 0, "PF": 0, "PTS": 0}

        line = line.split("|")
        relevant_team = line[2]
        away_team_name = line[3]
        home_team_name = line[4]
        action = line[-1]

        find_name = re.compile(r'([A-Z-ГЃ]\.\s\w+)')
        search = find_name.search(action)

        if search:
            name = search.group(1)
            data["player_name"] = name

            if "makes 2-pt" in action:
                data["FG"] += 1
                data['FGA'] += 1
                data["PTS"] += 2
            elif "makes 3-pt" in action:
                data["FG"] += 1
                data['FGA'] += 1
                data["3P"] += 1
                data["3PA"] += 1
                data["PTS"] += 3
            elif "misses 2-pt" in action:
                data["FGA"] += 1
            elif "misses 3-pt" in action:
                data["FGA"] += 1
                data["3PA"] += 1
            elif "makes free throw" in action:
                data["FT"] += 1
                data["FTA"] += 1
                data["PTS"] += 1
            elif "misses free throw" in action:
                data["FTA"] += 1
            elif "Offensive rebound" in action:
                data["ORB"] += 1
                data["TRB"] += 1
            elif "Defensive rebound" in action:
                data["DRB"] += 1
                data["TRB"] += 1
            elif "assist" in action:
                data["AST"] += 1
            elif "steal" in action:
                data["STL"] += 1
            elif 'block' in action:
                data["BLK"] += 1
            elif "Turnover" in action:
                data["TOV"] += 1

            if "Personal foul by" in action:
                data["PF"] += 1
                relevant_team = home_team_name if relevant_team == away_team_name else away_team_name

            if "Shooting foul by" in action:
                relevant_team = away_team_name if relevant_team == home_team_name else home_team_name

            team_data = home_team if relevant_team == home_team_name else away_team
            update_player_data(team_data, name, data)

    return {"home_team": home_team, "away_team": away_team}


def update_player_data(team, name, data):
    if name in team["players_data"]:
        player_stats = team["players_data"][name]
        for key, value in data.items():
            if key in player_stats:
                player_stats[key] += value
            else:
                player_stats[key] = value
    else:
        team["players_data"][name] = data

    calculate_percentages(team["players_data"][name])


def calculate_percentages(player_data):
    if player_data["FGA"] != 0:
        player_data["FG%"] = round((player_data["FG"] / player_data["FGA"]) * 100, 2)
    else:
        player_data["FG%"] = 0

    if player_data["3PA"] != 0:
        player_data["3P%"] = round((player_data["3P"] / player_data["3PA"]) * 100, 2)
    else:
        player_data["3P%"] = 0

    if player_data["FTA"] != 0:
        player_data["FT%"] = round((player_data["FT"] / player_data["FTA"]) * 100, 2)
    else:
        player_data["FT%"] = 0


def print_nba_game_stats(team_dict):
    for team_key, team_data in team_dict.items():
        team_name = team_data["name"]
        print(f"{team_key.upper()}: {team_name}")
        print(
            "{:<20}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}".format(
                "Players name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST",
                "STL", "BLK", "TOV", "PF"))
        for player_name, player_data in team_data["players_data"].items():
            print(
                "{:<20}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}".format(
                    player_name, player_data["FG"], player_data["FGA"], player_data["FG%"], player_data["3P"],
                    player_data["3PA"], player_data["3P%"],
                    player_data["FT"], player_data["FTA"], player_data["FT%"], player_data["ORB"], player_data["DRB"],
                    player_data["TRB"],
                    player_data["AST"], player_data["STL"], player_data["BLK"], player_data["TOV"], player_data["PF"]))


        team_totals = {key: sum(player_data[key] for player_data in team_data["players_data"].values()) for key in
                       team_data["players_data"]["Team Total"].keys()}
        print(
            "{:<20}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}".format(
                "Team Total", team_totals["FG"], team_totals["FGA"], team_totals["FG%"], team_totals["3P"],
                team_totals["3PA"], team_totals["3P%"],
                team_totals["FT"], team_totals["FTA"], team_totals["FT%"], team_totals["ORB"], team_totals["DRB"],
                team_totals["TRB"],
                team_totals["AST"], team_totals["STL"], team_totals["BLK"], team_totals["TOV"], team_totals["PF"]))
        print("\n")


def main():
    data_path = "./data_2.txt"
    with open(data_path, "r") as file:
        play_by_play_moves = file.readlines()

    game_summary = analyse_nba_game(play_by_play_moves[:407])
    print_nba_game_stats(game_summary)


if __name__ == "__main__":
    main()
