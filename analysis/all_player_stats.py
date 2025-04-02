import os
import csv


# TODO fix relative path nonsense
ANALYSIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = f'{ANALYSIS_DIRECTORY}/../output'
GAMES_DIRECTORY = "games"
PLAYERS_DIRECTORY = "players"
STAT_OUTPUT_HEADER = ["gp", "gs", "dnp", "min", "mpg", "pts", "ppg", "ppm", "ast", "apg", "apm", "to", "topg", "topm", "ast:to",
                      "reb", "rpg", "rpm", "oreb",  "dreb",  "stl", "spg", "spm", "blk", "bpg", "bpm", "pf", "pfpg", "pfpm",
                      "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "ftp"]


def get_players_dict():
    players_dict = {}
    directory = f'{OUTPUT_DIRECTORY}/{GAMES_DIRECTORY}/'
    for filename in os.listdir(directory):
      if not filename.endswith(".csv"):
          continue
      with open(os.path.join(directory, filename), "r") as csvfile:
          reader = csv.reader(csvfile, delimiter=",")
          header = next(reader)
          for row in reader:
              if not is_team_row(row):
                start = False
                dnp = False
                player_name = row[0]

                if player_name.startswith("S "):
                    start = True
                
                player_name = player_name.replace("S ", "", 1)
                
                if "DNP" in row[1]:
                    dnp = True

                if player_name in players_dict:
                    player_dict = players_dict[player_name]
                else:
                    player_dict = {}
                player_dict = get_player_dict(header, row, start, dnp, player_dict)
                players_dict[player_name] = player_dict
    return players_dict


def get_player_dict(header, row, start, dnp, player_dict):
    if not player_dict:
        player_dict = {
            "gp": 1 if not dnp else 0,
            "gs": 1 if start else 0,
            "dnp": 1 if dnp else 0
        }
    else:
        if dnp:
            player_dict["dnp"] += 1
        else:
            player_dict["gp"] += 1
            if start:
                player_dict["gs"] += 1

    # For each stat in the table, add it
    for x in (range(1, len(header))):
        stat = header[x].lower()

        if dnp:
            value = 0
        else:
            value = row[x]

        # Split stats are fg, 3pt, or ft which are denoted "x-y" rather than just an int
        if is_split_stat(stat):
            (before_dash_stat, after_dash_stat) = get_split_stat_name(stat)
            if value == 0:
                before_dash_value, after_dash_value = 0, 0
            else:
                values = value.split("-")
                before_dash_value, after_dash_value = int(values[0]), int(values[1])
            add_to_dict(player_dict, before_dash_stat, before_dash_value)
            add_to_dict(player_dict, after_dash_stat, after_dash_value)
        else: # Normal stat, value is int
            add_to_dict(player_dict, stat, int(value))
    return player_dict


def write_player_file(player_name, player_dict):
    stats = []
    for stat in STAT_OUTPUT_HEADER:
        if stat in player_dict:
            stats.append(player_dict[stat])
        else:
            stats.append(0)

    filename = f'{OUTPUT_DIRECTORY}/{PLAYERS_DIRECTORY}/{player_name.replace(" ", "_")}.csv'
    if os.path.exists(filename):
      os.remove(filename)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(STAT_OUTPUT_HEADER)
        writer.writerow(stats)


def finish_player_stats(player_dict):
    games_played = player_dict["gp"]
    minutes_played = player_dict["min"]

    percentage_stats = ["fg", "3p", "ft"]
    for stat in percentage_stats:
        player_dict[f'{stat}%'] = percentage(player_dict[f'{stat}m'], player_dict[f'{stat}a'])

    per_stats = ["min", "pts", "ast", "to", "reb", "stl", "blk", "pf"]
    for stat in per_stats:
        if stat == "to" or stat == "pf":
            stat_prefix = stat
        else:
            stat_prefix = stat[0]

        player_dict[f'{stat_prefix}pg'] = division(player_dict[stat], games_played)
        if stat != "min": # If we included this we'd get min per min lol
            # Why am I including per minute stats? Because why not
            player_dict[f'{stat_prefix}pm'] = division(player_dict[stat], minutes_played)
    # Free throw points (points off free throws)
    player_dict["ftp"] = player_dict["pts"] - (3 * player_dict["3pm"] + 2 * (player_dict["fgm"] - player_dict["3pm"]))

    player_to = player_dict["to"]
    player_dict["ast:to"] = division(player_dict["ast"], player_to)


### Helper functions

def is_team_row(row):
    # "TEAM" totals row or team %'s row
    return row[0].startswith("TEAM") or not row[0]


def is_split_stat(stat):
    return stat == "fg" or stat == "3pt" or stat == "ft"
        

def get_split_stat_name(stat):
    # I'm leaving the various iterations of this here just for fun
    # match stat:
    #     case "fg":
    #         return ("fgm", "fga")
    #     case "3pt":
    #         return ("3pm", "3pa")
    #     case "ft":
    #         return ("ftm", "fta")
    #
    # if stat == "fg":
    #     return ("fgm", "fga")
    # elif stat == "3pt":
    #     return ("3pm", "3pa")
    # elif stat == "ft":
    #     return ("ftm", "fta")
    stat_prefix = stat[:2]
    return (f'{stat_prefix}m', f'{stat_prefix}a')
        

# There's definitely a cleaner way to do these next 3 functions
def add_to_dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    else:
        dictionary[key] += value


def division(part, whole):
    if whole == 0:
        return 0
    return round(float(part) / float(whole), 3)


def percentage(part, whole):
  if whole == 0:
      return 0
  return round((100 * float(part) / float(whole)), 3)


if __name__ == "__main__":
    players_dict = get_players_dict()

    # after the players_dict has everyone
    for player_name, player_dict in players_dict.items():
        finish_player_stats(player_dict)
        write_player_file(player_name, player_dict)
