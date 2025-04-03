import os
import csv


OUTPUT_DIRECTORY = "output"
GAMES_DIRECTORY = "games"
PLAYERS_DIRECTORY = "players"
AGGREGATED_PLAYER_STATS = "aggregated_player_stats"


if __name__ == "__main__":
    # TODO fix relative path nonsense
    analysis_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = f'{analysis_directory}/../{OUTPUT_DIRECTORY}'
    players_directory = f'{output_directory}/{PLAYERS_DIRECTORY}/'
    header = []
    stats = []
    for filename in os.listdir(players_directory):
        if filename.endswith("csv"):
          with open(os.path.join(players_directory, filename), 'r') as csvfile:
              reader = csv.reader(csvfile, delimiter=',')
              header = next(reader)
              player_name = filename[:-4].replace("_", " ")
              player_stats = next(reader)
              player_stats = [player_name] + player_stats
        stats.append(player_stats)
    header = ["player"] + header
    new_csv = [header] + stats
    with open(f'{output_directory}/{AGGREGATED_PLAYER_STATS}/{AGGREGATED_PLAYER_STATS}.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerows(new_csv)
