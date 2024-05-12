import sys
import re
import json
from collections import namedtuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

TWO_ASSISTS = r"(#\d+ [A-Z']+ .*) scored for (.*) \(Assisted by (#\d+ [A-Z']+ .*) and (#\d+ [A-Z']+ .*)\)\."
ONE_ASSIST = r"(#\d+ [A-Z']+ .*) scored for (.*) \(Assisted by (#\d+ [A-Z']+ .*)\)\."
NO_ASSIST = r"(#\d+ [A-Z']+ .*) scored for (.*)\."

PLAYER = r"#(\d+) ([A-Z ']+) (.*)"


def parse_details(description):
    if match := re.match(TWO_ASSISTS, description):
        scorer, country, assist_1, assist_2 = match.groups()
        s_number, s_last, s_first = re.match(PLAYER, scorer).groups()
        a1_number, a1_last, a1_first = re.match(PLAYER, assist_1).groups()
        a2_number, a2_last, a2_first = re.match(PLAYER, assist_2).groups()

        return {
            "goal": {
                "country": country,
                "number": s_number,
                "first": s_first.title(),
                "last": s_last.title(),
            },
            "assists": [
                {
                    "country": country,
                    "number": a1_number,
                    "first": a1_first.title(),
                    "last": a1_last.title(),
                },
                {
                    "country": country,
                    "number": a2_number,
                    "first": a2_first.title(),
                    "last": a2_last.title(),
                },
            ],
        }
    elif match := re.match(ONE_ASSIST, description):
        scorer, country, assist = match.groups()
        s_number, s_last, s_first = re.match(PLAYER, scorer).groups()
        a_number, a_last, a_first = re.match(PLAYER, assist).groups()

        return {
            "goal": {
                "country": country,
                "number": s_number,
                "first": s_first.title(),
                "last": s_last.title(),
            },
            "assists": [
                {
                    "country": country,
                    "number": a_number,
                    "first": a_first.title(),
                    "last": a_last.title(),
                },
            ],
        }

    elif match := re.match(NO_ASSIST, description):
        scorer, country = match.groups()
        number, last, first = re.match(PLAYER, scorer).groups()
        return {
            "goal": {
                "country": country,
                "number": number,
                "first": first.title(),
                "last": last.title(),
            },
            "assists": [],
        }
    else:
        return None


def parse_goals(soup):
    events = soup.css.select("[period-key='period-all'] .s-timeline-event")
    goals = []
    for event in events:
        title = event.css.select(".s-title")[0].text.strip()
        if "Goal!" not in title:
            continue

        time = event.css.select(".s-cell--time")[0].text

        # Penaltie shootout goals don't count
        if time == "65:00":
            continue

        description = event.css.select(".s-description")[0].text.strip()
        goal = parse_details(description)

        if not goal:
            continue

        goals.append(goal)

    print(f"{len(goals)} scored")
    return goals


def parse_game(url):
    driver = webdriver.Firefox()
    driver.get(url)
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".s-timeline-event")
        )
    )

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    game = {}

    teams = soup.css.select(".s-team-info")
    for team in teams:
        name = team.css.select(".s-title--full")[0].text
        if "home" in game:
            game["away"] = name
        else:
            game["home"] = name

    date = soup.css.select(".s-date")[0].text
    game["date"] = date

    goals = parse_goals(soup)
    game["goals"] = goals

    return game


def store_game(game):
    games = None
    try:
        with open("../_data/games.json", "r") as games_db:
            games = json.load(games_db)
    except FileNotFoundError:
        games = []

    games.append(game)

    with open("../_data/games.json", "w") as games_db:
        games_db.write(json.dumps(games))


def parse_points_leaders(url):
    driver = webdriver.Firefox()
    driver.get(url)
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".s-cell--rank")
        )
    )

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    scoring_leaders_table = soup.css.select(".s-table")[
        3
    ]  # 4th table is currently what we want
    rows = scoring_leaders_table.css.select("tr.js-table-row")

    leaders = []
    for row in rows:
        try:
            rank = row.css.select(".s-cell--rank")[0].text.strip()
        except IndexError:
            continue
        if rank == "1":
            last, first = row.css.select(".s-cell--name")[0].text.strip().split(" ")
            name = f"{first.title()} {last.title()}"
            # breakpoint()
            goals = row.css.select("td.s-cell--g")[0].text.strip()
            assists = row.css.select("td.s-cell--a")[0].text.strip()
            points = row.css.select("td.s-cell--pts")[0].text.strip()

            leaders.append(
                {"name": name, "goals": goals, "assists": assists, "points": points}
            )
    return leaders


def store_leaders(leaders):
    with open("../_data/leaders.json", "w") as leaders_db:
        leaders_db.write(json.dumps(leaders))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse.py [url]")
    url = sys.argv[1]
    if not url.startswith("https://www.iihf.com/en/events/"):
        print("The URL must be for an IIHF score sheet")

    # game = parse_game(url)
    # store_game(game)

    leaders = parse_points_leaders(
        "https://www.iihf.com/en/events/2024/wm/skaters/scoringleaders"
    )
    store_leaders(leaders)
