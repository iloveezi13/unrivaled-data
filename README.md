# Unrivaled Data

## Summary

[Unrivaled Basketball](https://www.unrivaled.basketball)'s statistics pages are pretty good, but they are by no means comprehensive. I wanted to gather and curate the available data in order to hopefully inspire more insights.

I did this for fun so it's not well written at all. If I ever want to attach my name to it, I'll clean it up.

2 seconds is probably too long to make the scraper wait but my Wifi was really bad at the time.

**Note:** the scraper relies on the Unrivaled website's HTML/CSS. If they change the website in certain ways, the scraper will no longer work.

## If you just want the data

Download [this file](https://github.com/iloveezi/unrivaled-data/blob/main/output/aggregated_player_stats/aggregated_player_stats.csv) and open it in Excel or Google Sheets. Freeze the first row and column.

## Usage Guide

All commands are for MacOS or Linux.

I pushed the files that are created by the code as well as the code assuming most peopl ejust want the data, but some may want to tweak the way the data is collected and modified.

In order to run the whole thing from scratch, first empty the output directory's sub directories. I usually just do this on my computer but I guess you could do something along the lines of, starting in the project root directory:

```
$ rm -rf output
$ mkdir output
$ cd output
$ mkdir games
$ mkdir players
$ mkdir aggregated_player_stats
```

I'm sure there's a way to do it in 1 command but if you haven't picked up on it yet I'm a bit lazy.

Also, I think I messed up my Python installation at some point so I have to run all `python` commands with `python3`, but you may be able to use just `python`.

After having the output directory with empty subdirectories, run:

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
$ python3 scraper/scrape_games.py
$ python3 analysis/all_player_stats.py
$ python3 analysis/aggregate_players.py
```

If you want to add more stats, I recommend doing it in the all_player_stats.py script, which writes to the output/players directory. The aggregate_players.py script should work out of the box no matter what the player files have in them (I think).

Thanks :)
