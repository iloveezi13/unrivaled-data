from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import dateparser


OUTPUT_DIRECTORY = "output"
GAMES_DIRECTORY = "games"
UNRIVALED_SCEDHULE_LINK = "https://www.unrivaled.basketball/schedule"
DAYS_CSS_CLASS = "div.flex.row-12.p-12"
DATE_CSS_CLASS = "span.uppercase.weight-500"
BOX_SCORE_A_FRAME_CSS_CLASS = "div.flex-row.justify-between.w-100.items-center.px-16.py-12 > a"
TEAM_NAME_CSS_CLASS = "div.flex-row.items-center.pl-6.pb-6.col-6"
TEAM_TABLE_CSS_CLASS = "table.w-100"
TABLE_ROW = "tr"
TABLE_HEADER = "th"
TABLE_DATA = "td"
REG_SEASON_LAST_DAY = "MONDAY, MARCH 10, 2025"


def get_dates_and_links(driver):
    driver.get(UNRIVALED_SCEDHULE_LINK)
    driver.implicitly_wait(2)

    days = driver.find_elements(by=By.CSS_SELECTOR, value=DAYS_CSS_CLASS)

    dates_and_links = {}
    for day in days:
        date = day.find_element(by=By.CSS_SELECTOR, value=DATE_CSS_CLASS)
        date_text = date.text
        parsed_date = parse_date(date_text)
        
        if (parsed_date and parsed_date <= parse_date(REG_SEASON_LAST_DAY)): # Regular season only
          divs = day.find_elements(by=By.CSS_SELECTOR, value=BOX_SCORE_A_FRAME_CSS_CLASS)
          links = []
          for div in divs:
              href = div.get_attribute("href")
              links.append(href)
          dates_and_links[date_text] = links

    return dates_and_links


def get_game_stats(driver, link):
    driver.get(link)
    driver.implicitly_wait(2)

    teams = driver.find_elements(by=By.CSS_SELECTOR, value=TEAM_NAME_CSS_CLASS)
    tables = driver.find_elements(by=By.CSS_SELECTOR, value=TEAM_TABLE_CSS_CLASS)

    game_stats = {}

    for x in range(2):
        team_name = get_team_name(teams[x])
        team_table = tables[x]
        team_headers = get_headers(team_table)
        team_players = get_players(team_table)
        team_stats = [team_headers] + team_players

        game_stats[team_name] = team_stats

    return game_stats


def get_headers(players_stats):
    headers = []
    header_row = players_stats.find_element(by=By.CSS_SELECTOR, value=TABLE_ROW)
    for header in header_row.find_elements(by=By.CSS_SELECTOR, value=TABLE_HEADER):
      header_text = header.text
      headers.append(header_text)

    return headers


def get_players(players_stats):
    players = []
    for player_stats in players_stats.find_elements(by=By.CSS_SELECTOR, value=TABLE_ROW):
        player = []
        for stat in player_stats.find_elements(by=By.CSS_SELECTOR, value=TABLE_DATA):
            stat_text = stat.text
            player.append(stat_text)
        if player:
            players.append(player)

    return players


def write_games_stats(date, stats):
    # TODO fix this relative path nonsense
    scraper_directory = os.path.dirname(os.path.abspath(__file__))
    for team_name, team_stats in stats.items():
        filename = f'{scraper_directory}/../{OUTPUT_DIRECTORY}/{GAMES_DIRECTORY}/{remove_whitespace(date).lower()}_{remove_whitespace(team_name)}.csv'
        if os.path.exists(filename):
          os.remove(filename)
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(team_stats)


def write_games(driver, dates_and_links):
    for full_date, links in dates_and_links.items():
        for link in links:
            game_stats = get_game_stats(driver, link)
            date = remove_whitespace(full_date).split(",")[1]
            write_games_stats(date, game_stats)


def remove_whitespace(str):
    return str.replace(" ", "")


def get_team_name(team):
    return team.find_element(by=By.CSS_SELECTOR, value="h4").text


def parse_date(date_text):
    try:
        return dateparser.parse(date_text, date_formats=["%A, %B %d, %Y"])
    except Exception:
        return None


if __name__ == "__main__":
  driver = webdriver.Chrome()
  
  dates_and_links = get_dates_and_links(driver)
  write_games(driver, dates_and_links)

  driver.quit()
