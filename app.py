
import streamlit as st
import json
import math

st.set_page_config(page_title="Sports by the Numbers", page_icon="📊", layout="wide")

CURATED_DATA = json.loads(r'''{
  "version": "1.0",
  "frozen_for_classroom": true,
  "athlete_count": 50,
  "records": {
    "Patrick Mahomes": {
      "sport": "NFL",
      "stat_label": "Passing yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        4740,
        4839,
        5250,
        4183,
        3928,
        3587
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/patrick-mahomes/stats/career",
      "note": "Regular-season passing yards."
    },
    "Josh Allen": {
      "sport": "NFL",
      "stat_label": "Total touchdowns",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        45,
        42,
        42,
        44,
        40,
        39
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/josh-allen/stats/career",
      "note": "Passing TDs + rushing TDs."
    },
    "Lamar Jackson": {
      "sport": "NFL",
      "stat_label": "Rushing yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        1005,
        767,
        764,
        821,
        915,
        349
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/lamar-jackson/stats/career",
      "note": "Regular-season rushing yards."
    },
    "Joe Burrow": {
      "sport": "NFL",
      "stat_label": "Passing yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        2688,
        4611,
        4475,
        2309,
        4918,
        1809
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/joe-burrow/stats/career",
      "note": "Regular-season passing yards."
    },
    "Justin Jefferson": {
      "sport": "NFL",
      "stat_label": "Receiving yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        1400,
        1616,
        1809,
        1074,
        1533,
        1048
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/justin-jefferson/stats/career",
      "note": "Regular-season receiving yards."
    },
    "Ja'Marr Chase": {
      "sport": "NFL",
      "stat_label": "Receptions",
      "labels": [
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        81,
        87,
        100,
        127,
        125
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/ja-marr-chase/stats/career",
      "note": "Regular-season receptions."
    },
    "Saquon Barkley": {
      "sport": "NFL",
      "stat_label": "Rushing yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        34,
        593,
        1312,
        962,
        2005,
        1140
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/saquon-barkley/stats/career",
      "note": "Regular-season rushing yards."
    },
    "Christian McCaffrey": {
      "sport": "NFL",
      "stat_label": "Yards from scrimmage",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        374,
        785,
        1880,
        2023,
        348,
        2126
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/christian-mccaffrey/stats/career",
      "note": "Rushing yards + receiving yards."
    },
    "Derrick Henry": {
      "sport": "NFL",
      "stat_label": "Rushing yards",
      "labels": [
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
      ],
      "values": [
        2027,
        937,
        1538,
        1167,
        1921,
        1595
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/derrick-henry/stats/career",
      "note": "Regular-season rushing yards."
    },
    "Dan Marino": {
      "sport": "NFL",
      "stat_label": "Passing yards",
      "labels": [
        "1983",
        "1984",
        "1985",
        "1986",
        "1987",
        "1988"
      ],
      "values": [
        2210,
        5084,
        4137,
        4746,
        3245,
        4434
      ],
      "source": "NFL.com",
      "source_url": "https://www.nfl.com/players/dan-marino/stats/",
      "note": "Six early-career regular seasons."
    },
    "LeBron James": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        27.0,
        29.3,
        29.3,
        26.2,
        25.2,
        22.7
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/j/jamesle01.html",
      "note": "Regular-season scoring average."
    },
    "Stephen Curry": {
      "sport": "NBA",
      "stat_label": "3-pointers made",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        337,
        285,
        273,
        357,
        311,
        190
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/c/curryst01.html",
      "note": "Regular-season made 3-pointers."
    },
    "Kevin Durant": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2018-19",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        26.0,
        26.9,
        29.9,
        29.1,
        27.1,
        26.6
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/d/duranke01.html",
      "note": "Selected regular seasons; 2019-20 omitted because Durant did not play."
    },
    "Nikola Jokić": {
      "sport": "NBA",
      "stat_label": "Assists per game",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        7.0,
        8.3,
        7.9,
        9.8,
        9.0,
        10.2
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/j/jokicni01.html",
      "note": "Regular-season assists per game."
    },
    "Giannis Antetokounmpo": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        28.1,
        29.9,
        31.1,
        30.4,
        30.4,
        27.6
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/a/antetgi01.html",
      "note": "Regular-season scoring average."
    },
    "Luka Dončić": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        28.8,
        27.7,
        28.4,
        32.4,
        33.9,
        28.2
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/d/doncilu01.html",
      "note": "Regular-season scoring average."
    },
    "Jayson Tatum": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        26.4,
        26.9,
        30.1,
        26.9,
        26.8,
        21.8
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/t/tatumja01.html",
      "note": "Regular-season scoring average."
    },
    "Shai Gilgeous-Alexander": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        19.0,
        23.7,
        24.5,
        31.4,
        30.1,
        32.7
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/g/gilgesh01.html",
      "note": "Regular-season scoring average."
    },
    "Anthony Edwards": {
      "sport": "NBA",
      "stat_label": "3-pointers made",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        171,
        215,
        213,
        190,
        320,
        205
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/e/edwaran01.html",
      "note": "Regular-season made 3-pointers."
    },
    "Michael Jordan": {
      "sport": "NBA",
      "stat_label": "Points per game",
      "labels": [
        "1984-85",
        "1985-86",
        "1986-87",
        "1987-88",
        "1988-89",
        "1989-90"
      ],
      "values": [
        28.2,
        22.7,
        37.1,
        35.0,
        32.5,
        33.6
      ],
      "source": "Basketball-Reference",
      "source_url": "https://www.basketball-reference.com/players/j/jordami01.html",
      "note": "Six early-career regular seasons."
    },
    "Aaron Judge": {
      "sport": "MLB",
      "stat_label": "Home runs",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        27,
        9,
        39,
        62,
        37,
        58
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/j/judgeaa01.shtml",
      "note": "Regular-season home runs."
    },
    "Shohei Ohtani": {
      "sport": "MLB",
      "stat_label": "Home runs",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        18,
        7,
        46,
        34,
        44,
        54
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/o/ohtansh01.shtml",
      "note": "Regular-season home runs."
    },
    "Juan Soto": {
      "sport": "MLB",
      "stat_label": "Walks",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        108,
        41,
        145,
        135,
        132,
        129
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/s/sotoju01.shtml",
      "note": "Regular-season bases on balls."
    },
    "Mookie Betts": {
      "sport": "MLB",
      "stat_label": "Runs scored",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        135,
        47,
        93,
        117,
        126,
        75
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/b/bettsmo01.shtml",
      "note": "Regular-season runs scored."
    },
    "Francisco Lindor": {
      "sport": "MLB",
      "stat_label": "Home runs",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        32,
        8,
        20,
        26,
        31,
        33
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/l/lindofr01.shtml",
      "note": "Regular-season home runs."
    },
    "Ronald Acuña Jr.": {
      "sport": "MLB",
      "stat_label": "Stolen bases",
      "labels": [
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023"
      ],
      "values": [
        16,
        37,
        8,
        17,
        29,
        73
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/a/acunaro01.shtml",
      "note": "Regular-season stolen bases."
    },
    "Bryce Harper": {
      "sport": "MLB",
      "stat_label": "Home runs",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        35,
        13,
        35,
        18,
        21,
        30
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/h/harpebr03.shtml",
      "note": "Regular-season home runs."
    },
    "Gerrit Cole": {
      "sport": "MLB",
      "stat_label": "Strikeouts",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        326,
        94,
        243,
        257,
        222,
        99
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/c/colege01.shtml",
      "note": "Regular-season strikeouts."
    },
    "Paul Skenes": {
      "sport": "MLB",
      "stat_label": "Strikeouts",
      "labels": [
        "2024",
        "2025",
        "2026"
      ],
      "values": [
        170,
        216,
        185
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/s/skenepa01.shtml",
      "note": "Strikeouts by MLB season. The 2026 value is a frozen in-season snapshot, not a completed-season total."
    },
    "Babe Ruth": {
      "sport": "MLB",
      "stat_label": "Home runs",
      "labels": [
        "1920",
        "1921",
        "1922",
        "1923",
        "1924",
        "1925"
      ],
      "values": [
        54,
        59,
        35,
        41,
        46,
        25
      ],
      "source": "Baseball-Reference",
      "source_url": "https://www.baseball-reference.com/players/r/ruthba01.shtml",
      "note": "Six Yankees seasons."
    },
    "Connor McDavid": {
      "sport": "NHL",
      "stat_label": "Points",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        97,
        105,
        123,
        153,
        132,
        100
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/m/mcdavco01.html",
      "note": "Regular-season points."
    },
    "Nathan MacKinnon": {
      "sport": "NHL",
      "stat_label": "Points",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        93,
        65,
        88,
        111,
        140,
        116
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/m/mackina01.html",
      "note": "Regular-season points."
    },
    "Auston Matthews": {
      "sport": "NHL",
      "stat_label": "Goals",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        47,
        41,
        60,
        40,
        69,
        33
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/m/matthau01.html",
      "note": "Regular-season goals."
    },
    "Sidney Crosby": {
      "sport": "NHL",
      "stat_label": "Points",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        47,
        62,
        84,
        93,
        94,
        91
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/c/crosbsi01.html",
      "note": "Regular-season points."
    },
    "Alex Ovechkin": {
      "sport": "NHL",
      "stat_label": "Goals",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        48,
        24,
        50,
        42,
        31,
        44
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/o/ovechal01.html",
      "note": "Regular-season goals."
    },
    "Artemi Panarin": {
      "sport": "NHL",
      "stat_label": "Points",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        95,
        58,
        96,
        92,
        120,
        89
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/p/panarar01.html",
      "note": "Regular-season points."
    },
    "Igor Shesterkin": {
      "sport": "NHL",
      "stat_label": "Save percentage",
      "labels": [
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        91.6,
        93.5,
        91.6,
        91.2,
        90.5
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/s/shestig01.html",
      "note": "Save percentage shown as percentage points, not decimals."
    },
    "Wayne Gretzky": {
      "sport": "NHL",
      "stat_label": "Points",
      "labels": [
        "1981-82",
        "1982-83",
        "1983-84",
        "1984-85",
        "1985-86",
        "1986-87"
      ],
      "values": [
        212,
        196,
        205,
        208,
        215,
        183
      ],
      "source": "Hockey-Reference",
      "source_url": "https://www.hockey-reference.com/players/g/gretzwa01.html",
      "note": "Six Edmonton regular seasons."
    },
    "Lionel Messi": {
      "sport": "Soccer",
      "stat_label": "League goals",
      "labels": [
        "2014-15",
        "2015-16",
        "2016-17",
        "2017-18",
        "2018-19",
        "2019-20"
      ],
      "values": [
        43,
        26,
        37,
        34,
        36,
        25
      ],
      "source": "FBref",
      "source_url": "https://fbref.com/en/players/d70ce98e/Lionel-Messi",
      "note": "La Liga goals for Barcelona."
    },
    "Kylian Mbappé": {
      "sport": "Soccer",
      "stat_label": "League goals",
      "labels": [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24"
      ],
      "values": [
        33,
        18,
        27,
        28,
        29,
        27
      ],
      "source": "FBref",
      "source_url": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe",
      "note": "Ligue 1 goals for Paris Saint-Germain."
    },
    "Erling Haaland": {
      "sport": "Soccer",
      "stat_label": "League goals",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        13,
        27,
        22,
        36,
        27,
        22
      ],
      "source": "Bundesliga / Premier League",
      "source_url": "https://www.premierleague.com/players/65970/Erling-Haaland/overview",
      "note": "League goals; 2019-20 through 2021-22 are Bundesliga, later seasons are Premier League."
    },
    "Mohamed Salah": {
      "sport": "Soccer",
      "stat_label": "Premier League goals",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        19,
        22,
        23,
        19,
        18,
        29
      ],
      "source": "Premier League",
      "source_url": "https://www.premierleague.com/players/5178/Mohamed-Salah/overview",
      "note": "Premier League goals."
    },
    "Vinícius Júnior": {
      "sport": "Soccer",
      "stat_label": "La Liga goals",
      "labels": [
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25"
      ],
      "values": [
        3,
        3,
        17,
        10,
        15,
        11
      ],
      "source": "FBref",
      "source_url": "https://fbref.com/en/players/7111d552/Vinicius-Junior",
      "note": "La Liga goals for Real Madrid."
    },
    "Lamine Yamal": {
      "sport": "Soccer",
      "stat_label": "La Liga goals",
      "labels": [
        "2023-24",
        "2024-25",
        "2025-26"
      ],
      "values": [
        5,
        9,
        16
      ],
      "source": "LaLiga",
      "source_url": "https://www.laliga.com/en-GB/player/lamine-yamal",
      "note": "La Liga goals."
    },
    "Pelé": {
      "sport": "Soccer",
      "stat_label": "World Cup goals",
      "labels": [
        "1958",
        "1962",
        "1966",
        "1970"
      ],
      "values": [
        6,
        1,
        1,
        4
      ],
      "source": "FIFA",
      "source_url": "https://www.fifa.com/en/tournaments/mens/worldcup/articles/top-brazil-goalscorers-history",
      "note": "Goals scored at each FIFA World Cup Pelé played."
    },
    "Max Verstappen": {
      "sport": "Formula 1",
      "stat_label": "Championship points",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        278,
        214,
        395.5,
        454,
        575,
        437
      ],
      "source": "Formula 1",
      "source_url": "https://www.formula1.com/en/results",
      "note": "Season Drivers' Championship points."
    },
    "Lewis Hamilton": {
      "sport": "Formula 1",
      "stat_label": "Championship points",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        413,
        347,
        387.5,
        240,
        234,
        223
      ],
      "source": "Formula 1",
      "source_url": "https://www.formula1.com/en/results",
      "note": "Season Drivers' Championship points."
    },
    "Charles Leclerc": {
      "sport": "Formula 1",
      "stat_label": "Championship points",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        264,
        98,
        159,
        308,
        206,
        356
      ],
      "source": "Formula 1",
      "source_url": "https://www.formula1.com/en/results",
      "note": "Season Drivers' Championship points."
    },
    "Lando Norris": {
      "sport": "Formula 1",
      "stat_label": "Championship points",
      "labels": [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024"
      ],
      "values": [
        49,
        97,
        160,
        122,
        205,
        374
      ],
      "source": "Formula 1",
      "source_url": "https://www.formula1.com/en/results",
      "note": "Season Drivers' Championship points."
    },
    "Ayrton Senna": {
      "sport": "Formula 1",
      "stat_label": "Championship points",
      "labels": [
        "1985",
        "1986",
        "1987",
        "1988",
        "1989",
        "1990"
      ],
      "values": [
        38,
        55,
        57,
        90,
        60,
        78
      ],
      "source": "Formula 1",
      "source_url": "https://www.formula1.com/en/results",
      "note": "Season Drivers' Championship points under the scoring system used at the time."
    }
  }
}''')

records = CURATED_DATA["records"]


SPORT_ICONS = {
    "NFL": "🏈",
    "NBA": "🏀",
    "MLB": "⚾",
    "NHL": "🏒",
    "Soccer": "⚽",
    "Formula 1": "🏎️",
}

MODE_ICONS = {
    "Percent Change": "📈",
    "MAD Consistency": "🎯",
    "Frequency Table": "📊",
}

def reset_work():
    keep = {"sport_select","athlete_select","mode_select"}
    for key in list(st.session_state.keys()):
        if key not in keep and (
            key.startswith("pc_") or key.startswith("mad_") or key.startswith("freq_")
            or key.startswith("coach_")
            or key in {"claim","observation","revised","score_result","ready_to_revise","coach_stage","coach_answers"}
        ):
            del st.session_state[key]

def fmt(v):
    if isinstance(v, float) and not v.is_integer():
        return f"{v:.1f}"
    return f"{int(v):,}" if float(v).is_integer() else f"{v:,}"

def selected_indices(n):
    if n <= 4:
        return list(range(n))
    # Four evenly spread checkpoints.
    idx = [0, round((n-1)/3), round(2*(n-1)/3), n-1]
    out = []
    for x in idx:
        if x not in out:
            out.append(x)
    return out

def make_bins(values):
    lo, hi = min(values), max(values)
    if math.isclose(lo, hi):
        return [(f"{fmt(lo)}", lo-0.01, hi+0.01)]
    width = (hi-lo)/3
    # Keep simple classroom-friendly boundaries.
    if all(float(v).is_integer() for v in values):
        a = math.floor(lo)
        b1 = math.floor(lo + width)
        b2 = math.floor(lo + 2*width)
        c = math.ceil(hi)
        if b1 < a: b1 = a
        if b2 <= b1: b2 = b1 + 1
        return [
            (f"{a}–{b1}", a, b1),
            (f"{b1+1}–{b2}", b1+1, b2),
            (f"{b2+1}–{c}", b2+1, c),
        ]
    b1 = lo+width
    b2 = lo+2*width
    return [
        (f"{lo:.1f}–{b1:.1f}", lo, b1),
        (f">{b1:.1f}–{b2:.1f}", b1, b2),
        (f">{b2:.1f}–{hi:.1f}", b2, hi+1e-9),
    ]

def coach_question(stage):
    qs = [
        ("Does your claim clearly answer the investigation question?", ["Yes","Not yet","I'm not sure"]),
        ("Did you use at least one specific number from your work?", ["Yes","No","I'm not sure"]),
        ("Did you explain what the number means instead of only listing it?", ["Yes","Not yet","I'm not sure"]),
        ("Is your claim limited to the data you actually studied?", ["Yes","No — my claim is broader","I'm not sure"]),
    ]
    return qs[min(stage,3)]

def score_argument(original, revised, observation, answers):
    words = revised.split()
    claim = 25 if len(words)>=10 else 20 if len(words)>=6 else 15
    evidence = 25 if any(ch.isdigit() for ch in revised) else 15
    reasoning_terms = ["because","shows","suggests","compared","higher","lower","increase","decrease","consistent","frequency","percent"]
    reasoning = 25 if observation.strip() and any(x in revised.lower() for x in reasoning_terms) else 20 if observation.strip() else 15
    changed = revised.strip().lower() != original.strip().lower()
    fairness = 25 if len(answers)>=4 and changed else 20 if changed else 15
    return {"claim":claim,"evidence":evidence,"reasoning":reasoning,"fairness":fairness,
            "total":claim+evidence+reasoning+fairness}

def percent_change_engine(rec):
    labels, values = rec["labels"], [float(x) for x in rec["values"]]
    idx = selected_indices(len(values))
    labels = [labels[i] for i in idx]
    values = [values[i] for i in idx]

    st.markdown('<div class="step">Investigation 1 · Change over time</div>', unsafe_allow_html=True)
    st.subheader(f"How did {athlete}'s {rec['stat_label'].lower()} change across the selected periods?")
    st.markdown('<div class="formula">Percent Change = (New − Old) ÷ Old × 100</div>', unsafe_allow_html=True)

    st.info(
        "For each pair, you will find the numerical change, calculate the percent change, "
        "and identify whether it is a **percent increase** or **percent decrease**. "
        "Rounding is allowed within **0.5 percentage points**."
    )

    st.markdown("### 1. Read the data")
    st.dataframe(
        [{"Period": l, rec["stat_label"]: v} for l, v in zip(labels, values)],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 2. Calculate the changes")

    results = []

    for i in range(1, len(values)):
        old, new = values[i-1], values[i]
        true_change = new - old
        true_pct = (true_change / old) * 100 if old != 0 else 0

        st.markdown(f"**{labels[i-1]} → {labels[i]}**")
        st.caption(f"Use: ({fmt(new)} − {fmt(old)}) ÷ {fmt(old)} × 100")

        a, b = st.columns(2)

        student_change = a.number_input(
            "Change",
            key=f"pc_change_{i}",
            help="Answers within 0.5 of the exact change are accepted."
        )

        student_pct = b.number_input(
            "Percent change",
            key=f"pc_pct_{i}",
            help="You may round. Answers within 0.5 percentage points are accepted."
        )

        direction = st.radio(
            "Was this an increase or decrease?",
            ["Increase", "Decrease", "No Change"],
            key=f"pc_direction_{i}",
            horizontal=True
        )

        true_direction = "Increase" if true_change > 0 else "Decrease" if true_change < 0 else "No Change"

        change_ok = math.isclose(float(student_change), true_change, abs_tol=0.5)
        pct_ok = math.isclose(float(student_pct), true_pct, abs_tol=0.5)
        direction_ok = direction == true_direction

        results.append({
            "i": i,
            "old": old,
            "new": new,
            "true_change": true_change,
            "true_pct": true_pct,
            "student_change": float(student_change),
            "student_pct": float(student_pct),
            "student_direction": direction,
            "true_direction": true_direction,
            "change_ok": change_ok,
            "pct_ok": pct_ok,
            "direction_ok": direction_ok,
            "label": f"{labels[i-1]} → {labels[i]}",
        })

    if "pc_check_attempts" not in st.session_state:
        st.session_state.pc_check_attempts = 0

    if st.button("Check My Percent Changes", use_container_width=True):
        all_correct = all(r["change_ok"] and r["pct_ok"] and r["direction_ok"] for r in results)

        if all_correct:
            st.success("✅ Correct! Your answers are within the accepted rounding range.")
            st.session_state.pc_check_attempts = 0
        else:
            st.session_state.pc_check_attempts += 1

            if st.session_state.pc_check_attempts < 2:
                st.info(
                    "Not quite yet. Try one more time using this order: "
                    "**New − Old → divide by Old → multiply by 100.** "
                    "If it is still off on your next check, I’ll show you exactly where the mistake is."
                )
            else:
                st.warning("You’ve missed it twice, so here’s a more specific hint for each row that needs work:")

                for r in results:
                    if r["change_ok"] and r["pct_ok"] and r["direction_ok"]:
                        continue

                    st.markdown(f"#### {r['label']}")

                    if not r["direction_ok"]:
                        st.write(
                            f"**Check whether the value went up or down.** "
                            f"It went from {fmt(r['old'])} to {fmt(r['new'])}, "
                            f"so this is a **{r['true_direction'].lower()}**."
                        )

                    if not r["change_ok"]:
                        expected_change = r["true_change"]
                        entered_change = r["student_change"]

                        # Sign error
                        if math.isclose(entered_change, -expected_change, abs_tol=0.5):
                            st.write(
                                f"**Your change has the sign reversed.** "
                                f"Use New − Old: {fmt(r['new'])} − {fmt(r['old'])}."
                            )
                        else:
                            st.write(
                                f"**First fix the raw change.** "
                                f"You entered {entered_change:g}. "
                                f"Subtract the old value from the new value: "
                                f"{fmt(r['new'])} − {fmt(r['old'])}."
                            )

                    if r["change_ok"] and not r["pct_ok"]:
                        entered_pct = r["student_pct"]
                        true_pct = r["true_pct"]

                        decimal_form = true_pct / 100
                        using_new_denominator = (
                            (r["true_change"] / r["new"]) * 100 if r["new"] != 0 else None
                        )
                        no_times_100 = r["true_change"] / r["old"] if r["old"] != 0 else None

                        if math.isclose(entered_pct, decimal_form, abs_tol=0.05):
                            st.write(
                                "**You stopped at the decimal.** "
                                "After dividing by the old value, multiply by 100 to turn it into a percent."
                            )
                        elif no_times_100 is not None and math.isclose(entered_pct, no_times_100, abs_tol=0.05):
                            st.write(
                                "**You forgot the ×100 step.** "
                                "Your division is on the right track; now multiply that result by 100."
                            )
                        elif using_new_denominator is not None and math.isclose(entered_pct, using_new_denominator, abs_tol=0.5):
                            st.write(
                                "**It looks like you divided by the new value.** "
                                "Percent change always divides by the **old/original value**."
                            )
                        elif math.isclose(entered_pct, abs(true_pct), abs_tol=0.5) and true_pct < 0:
                            st.write(
                                "**Your size is right, but the sign is missing.** "
                                "Because the value decreased, the percent change should be negative."
                            )
                        else:
                            st.write(
                                f"**Your raw change is correct, so focus on the percent step.** "
                                f"Take your change, divide by the old value ({fmt(r['old'])}), then multiply by 100."
                            )

                    elif not r["change_ok"] and not r["pct_ok"]:
                        st.write(
                            "Fix the raw change first. Once that is correct, use that change in the percent formula."
                        )

                st.caption(
                    "The app still accepts answers within ±0.5 for the raw change and ±0.5 percentage points for percent change."
                )

    st.markdown("### 3. See the trend")
    st.line_chart(
        [{"Period": l, "Value": v} for l, v in zip(labels, values)],
        x="Period",
        y="Value",
        use_container_width=True
    )

    obs = st.text_area(
        "What is the biggest change you notice?",
        key="pc_observation"
    )
    st.session_state.observation = obs

    return f"How did {athlete}'s {rec['stat_label'].lower()} change across the selected periods?"

def mad_engine(rec):
    labels, values = rec["labels"], [float(x) for x in rec["values"]]

    st.markdown('<div class="step">Investigation 2 · Consistency</div>', unsafe_allow_html=True)
    st.subheader(f"How consistent was {athlete}'s {rec['stat_label'].lower()} across these periods?")

    st.info(
        "MAD stands for Mean Absolute Deviation. It tells us the typical distance "
        "between each value and the mean. A smaller MAD means the values are more consistent."
    )

    # STEP 1
    st.markdown("### Step 1 · Look at the data")
    st.dataframe(
        [{"Period": lab, rec["stat_label"]: val} for lab, val in zip(labels, values)],
        use_container_width=True,
        hide_index=True
    )

    # STEP 2
    true_mean = sum(values) / len(values)

    st.markdown("### Step 2 · Find the mean")
    st.write(
        f"Add all **{len(values)}** values together, then divide by **{len(values)}**."
    )
    st.markdown(
        f'<div class="formula">Mean = Sum of all values ÷ {len(values)}</div>',
        unsafe_allow_html=True
    )

    student_mean = st.number_input(
        "Your mean",
        key="mad_mean",
        help="Your answer can be within 0.5 of the exact answer."
    )

    if st.button("Check My Mean", use_container_width=True):
        if math.isclose(float(student_mean), true_mean, abs_tol=0.5):
            st.success("✅ Correct — or close enough! Move on to Step 3.")
        else:
            st.info(
                f"Not quite. Add the {len(values)} values, then divide by {len(values)}. "
                "Answers within 0.5 are accepted."
            )

    # STEP 3
    st.markdown("### Step 3 · Find each deviation from the mean")
    st.write(
        "For each value, subtract the mean you found in Step 2. "
        "A deviation can be positive or negative."
    )
    st.markdown(
        '<div class="formula">Deviation = Value − Mean</div>',
        unsafe_allow_html=True
    )

    # STEP 4
    st.markdown("### Step 4 · Turn each deviation into an absolute deviation")
    st.write(
        "Absolute value means distance, so make every deviation positive. "
        "For example, **−4 becomes 4**."
    )
    st.markdown(
        '<div class="formula">Absolute Deviation = | Value − Mean |</div>',
        unsafe_allow_html=True
    )

    true_deviations = []
    true_abs_deviations = []
    row_checks = []

    header = st.columns([1.6, 1, 1.2, 1.2])
    header[0].markdown("**Period**")
    header[1].markdown("**Value**")
    header[2].markdown("**Deviation**")
    header[3].markdown("**Absolute Deviation**")

    for i, (lab, val) in enumerate(zip(labels, values)):
        true_dev = val - true_mean
        true_abs = abs(true_dev)
        true_deviations.append(true_dev)
        true_abs_deviations.append(true_abs)

        c1, c2, c3, c4 = st.columns([1.6, 1, 1.2, 1.2])
        c1.write(f"**{lab}**")
        c2.write(fmt(val))

        student_dev = c3.number_input(
            "Deviation",
            key=f"mad_dev_{i}",
            label_visibility="collapsed",
            help="Value − Mean. Answers within 0.5 are accepted."
        )

        student_abs = c4.number_input(
            "Absolute deviation",
            min_value=0.0,
            key=f"mad_abs_{i}",
            label_visibility="collapsed",
            help="Make the deviation positive. Answers within 0.5 are accepted."
        )

        dev_ok = math.isclose(float(student_dev), true_dev, abs_tol=0.5)
        abs_ok = math.isclose(float(student_abs), true_abs, abs_tol=0.5)
        row_checks.append(dev_ok and abs_ok)

    if st.button("Check My Deviations", use_container_width=True):
        correct_rows = sum(1 for x in row_checks if x)
        if correct_rows == len(row_checks):
            st.success("✅ All of your deviations and absolute deviations are close enough.")
        else:
            st.info(
                f"You have {correct_rows} of {len(row_checks)} rows correct. "
                "Remember: first subtract the mean, then make the answer positive."
            )

    # STEP 5 — explicitly sum the absolute deviations
    st.markdown("### Step 5 · Add the absolute deviations")
    st.write(
        "Now add the numbers in the **Absolute Deviation** column. "
        "This total is what you will divide to find the MAD."
    )

    true_abs_sum = sum(true_abs_deviations)

    student_abs_sum = st.number_input(
        "Sum of the absolute deviations",
        min_value=0.0,
        key="mad_abs_sum",
        help="Add every number from the Absolute Deviation column. Answers within 0.5 are accepted."
    )

    if st.button("Check My Absolute-Deviation Total", use_container_width=True):
        if math.isclose(float(student_abs_sum), true_abs_sum, abs_tol=0.5):
            st.success("✅ Correct — or close enough! Now use that total to find the MAD.")
        else:
            st.info(
                "Add all of the numbers in your Absolute Deviation column. "
                "Answers within 0.5 of the exact total are accepted."
            )

    # STEP 6 — explicitly mean those numbers
    st.markdown("### Step 6 · Find the mean of the absolute deviations")
    st.write(
        f"This is the final MAD step. Take the total from Step 5 and divide by "
        f"the number of absolute deviations, which is **{len(true_abs_deviations)}**."
    )

    st.markdown(
        f'<div class="formula">MAD = Sum of Absolute Deviations ÷ {len(true_abs_deviations)}</div>',
        unsafe_allow_html=True
    )

    true_mad = true_abs_sum / len(true_abs_deviations)

    student_mad = st.number_input(
        "Your MAD",
        min_value=0.0,
        key="mad_final",
        help="Your final MAD can be within 0.5 of the exact answer."
    )

    if st.button("Check My MAD", use_container_width=True):
        if math.isclose(float(student_mad), true_mad, abs_tol=0.5):
            st.success(
                f"✅ Correct — or close enough! The exact MAD is {true_mad:.2f}."
            )
        else:
            st.info(
                f"Take your total absolute deviation from Step 5 and divide by "
                f"{len(true_abs_deviations)}. Answers within 0.5 are accepted."
            )

    # STEP 7 — interpret
    st.markdown("### Step 7 · Interpret the MAD")
    st.caption(
        "MAD tells you the typical distance from the mean. "
        "Smaller MAD = more consistent. Larger MAD = less consistent."
    )

    st.scatter_chart(
        [{"Value": v, "Row": 1} for v in values],
        x="Value",
        y="Row",
        use_container_width=True
    )

    obs = st.text_area(
        "What does the MAD tell you about this athlete's consistency?",
        key="mad_observation",
        placeholder=(
            "Example: The MAD is about 4.2, so the values are usually about "
            "4.2 units away from the mean..."
        )
    )
    st.session_state.observation = obs

    return f"How consistent was {athlete}'s {rec['stat_label'].lower()} across these periods?"

def frequency_engine(rec):
    labels, values = rec["labels"], [float(x) for x in rec["values"]]
    bins = make_bins(values)
    st.markdown('<div class="step">Investigation 3 · Frequency table</div>', unsafe_allow_html=True)
    st.subheader(f"How are {athlete}'s {rec['stat_label'].lower()} values distributed?")
    st.caption("Frequency tells how often something happens. Relative frequency tells what percent of the data falls in each group.")

    st.markdown("### 1. Look at the raw values")
    st.dataframe([{"Period":l,rec["stat_label"]:v} for l,v in zip(labels,values)],
                 use_container_width=True,hide_index=True)

    counts = []
    for bi,(label,low,high) in enumerate(bins):
        if bi < len(bins)-1:
            count = sum(1 for v in values if low <= v <= high)
        else:
            count = sum(1 for v in values if low <= v <= high)
        counts.append((label,count))

    st.markdown("### 2. Build the table")
    all_ok = True
    graph_rows = []
    for label,count in counts:
        expected = count/len(values)*100
        c1,c2,c3 = st.columns([2,1,1])
        c1.write(f"**{label}**")
        f = c2.number_input("Frequency", min_value=0, max_value=len(values), step=1,
                            key=f"freq_{label}",label_visibility="collapsed")
        r = c3.number_input("Relative frequency %",min_value=0.0,max_value=100.0,
                            key=f"freq_rel_{label}",label_visibility="collapsed")
        if int(f)!=count or not math.isclose(float(r),expected,abs_tol=.2):
            all_ok=False
        graph_rows.append({"Range":label,"Frequency":count})

    if st.button("Check My Frequency Table",use_container_width=True):
        if all_ok:
            st.success("✅ Correct frequency table.")
        else:
            st.info(f"Relative frequency = Frequency ÷ {len(values)} × 100.")

    st.markdown("### 3. See the frequency graph")
    st.bar_chart(graph_rows,x="Range",y="Frequency",use_container_width=True)
    obs = st.text_area("Which range occurs most often? What does that tell you?", key="freq_observation")
    st.session_state.observation = obs
    return f"How are {athlete}'s {rec['stat_label'].lower()} values distributed?"

# HEADER
st.markdown("""
<div class="hero">
<h1>📊 Sports by the Numbers</h1>
<p>50 curated athletes. Three focused math investigations. No live API, no AI, and no separate data file required.</p>
</div>
""", unsafe_allow_html=True)

# Selection
sports = ["NFL","NBA","MLB","NHL","Soccer","Formula 1"]
c1,c2,c3 = st.columns(3)
with c1:
    sport = st.selectbox("Sport", sports, format_func=lambda s:f"{SPORT_ICONS[s]} {s}", key="sport_select")
names = sorted([n for n,r in records.items() if r["sport"]==sport])
with c2:
    athlete = st.selectbox("Athlete", names, key="athlete_select")
with c3:
    mode = st.selectbox("Investigation", list(MODE_ICONS),
        format_func=lambda m:f"{MODE_ICONS[m]} {m}", key="mode_select")

rec = records[athlete]

st.markdown(f"""
<div class="card">
<div class="step">{SPORT_ICONS[sport]} {sport}</div>
<h2>{athlete}</h2>
<p><b>Math focus:</b> {mode}</p>
<p><b>Data:</b> {rec["stat_label"]}</p>
</div>
""",unsafe_allow_html=True)

if st.button("Start / Reset Investigation",use_container_width=True):
    reset_work()
    st.rerun()

with st.expander("About this classroom data"):
    st.write(rec.get("note",""))
    st.write(f"Source: {rec.get('source','')}")
    st.write(rec.get("source_url",""))
    st.caption("This is a frozen classroom dataset so every student sees the same values.")

if mode=="Percent Change":
    question = percent_change_engine(rec)
elif mode=="MAD Consistency":
    question = mad_engine(rec)
else:
    question = frequency_engine(rec)

# Claim + coach
st.markdown("---")
st.markdown('<div class="step">Explain what the data means</div>',unsafe_allow_html=True)
claim = st.text_area("Make a claim", key="claim",
    placeholder="Based on the data, I think...")
obs = st.session_state.get("observation","")

if st.button("🧠 Start Built-In Coach",disabled=not(claim.strip() and obs.strip()),use_container_width=True):
    st.session_state.coach_stage=0
    st.session_state.coach_answers=[]
    st.session_state.ready_to_revise=False
    st.rerun()

if "coach_stage" in st.session_state and not st.session_state.get("ready_to_revise"):
    stage=st.session_state.coach_stage
    q,opts=coach_question(stage)
    st.markdown(f"### Coach Check {stage+1} of 4")
    ans=st.radio(q,opts,key=f"coach_radio_{stage}")
    if st.button("Continue →",key=f"coach_continue_{stage}",use_container_width=True):
        st.session_state.coach_answers.append(ans)
        if stage>=3:
            st.session_state.ready_to_revise=True
        else:
            st.session_state.coach_stage+=1
        st.rerun()

if st.session_state.get("ready_to_revise"):
    st.markdown("### Revise your claim")
    st.write(f"**Original:** {claim}")
    revised=st.text_area("Stronger final claim",key="revised")
    if st.button("🏆 Score My Argument",disabled=not revised.strip(),use_container_width=True):
        st.session_state.score_result=score_argument(
            claim,revised,obs,st.session_state.get("coach_answers",[])
        )
        st.rerun()

if st.session_state.get("score_result"):
    s=st.session_state.score_result
    st.markdown(f'<div class="score">{s["total"]}/100</div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric("Clear Claim",f'{s["claim"]}/25')
    b.metric("Evidence",f'{s["evidence"]}/25')
    c.metric("Reasoning",f'{s["reasoning"]}/25')
    d.metric("Strength & Fairness",f'{s["fairness"]}/25')
    st.caption("The score checks argument features, not whether the student's sports opinion matches an outside answer.")

st.markdown("---")
st.caption("Sports by the Numbers · Curated classroom edition · 50 athletes · 150 investigations")
