
import streamlit as st
import json
import math

st.set_page_config(page_title="Sports by the Numbers", page_icon="📊", layout="wide")

CURATED_DATA = {
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
}

records = CURATED_DATA["records"]

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

    st.markdown("### 1. Read the data")
    st.dataframe([{"Period":l, rec["stat_label"]:v} for l,v in zip(labels,values)],
                 use_container_width=True, hide_index=True)

    st.markdown("### 2. Calculate the changes")
    correct_flags = []
    for i in range(1,len(values)):
        old,new = values[i-1],values[i]
        true_change = new-old
        true_pct = (true_change/old)*100 if old else 0
        st.markdown(f"**{labels[i-1]} → {labels[i]}**")
        a,b = st.columns(2)
        ch = a.number_input("Change", key=f"pc_change_{i}")
        pct = b.number_input("Percent change", key=f"pc_pct_{i}")
        correct_flags.append(
            math.isclose(float(ch),true_change,abs_tol=.05)
            and math.isclose(float(pct),true_pct,abs_tol=.2)
        )
    if st.button("Check My Percent Changes",use_container_width=True):
        if all(correct_flags):
            st.success("✅ Correct! You calculated every percent change.")
        else:
            st.info("Try again: New − Old → divide by Old → multiply by 100.")

    st.markdown("### 3. See the trend")
    st.line_chart([{"Period":l,"Value":v} for l,v in zip(labels,values)],
                  x="Period",y="Value",use_container_width=True)
    obs = st.text_area("What is the biggest change you notice?", key="pc_observation")
    st.session_state.observation = obs
    return f"How did {athlete}'s {rec['stat_label'].lower()} change across the selected periods?"

def mad_engine(rec):
    labels, values = rec["labels"], [float(x) for x in rec["values"]]
    st.markdown('<div class="step">Investigation 2 · Consistency</div>', unsafe_allow_html=True)
    st.subheader(f"How consistent was {athlete}'s {rec['stat_label'].lower()} across these periods?")
    st.caption("MAD = Mean Absolute Deviation. A smaller MAD means the values stayed closer to the mean.")

    st.markdown("### 1. Start with the data")
    st.dataframe([{"Period":l,rec["stat_label"]:v} for l,v in zip(labels,values)],
                 use_container_width=True, hide_index=True)

    true_mean = sum(values)/len(values)
    st.markdown("### 2. Find the mean")
    mean_ans = st.number_input("Mean", key="mad_mean")
    if st.button("Check Mean",use_container_width=True):
        if math.isclose(mean_ans,true_mean,abs_tol=.05):
            st.success("✅ Correct mean.")
        else:
            st.info(f"Add the {len(values)} values and divide by {len(values)}.")

    st.markdown("### 3. Find each absolute deviation")
    st.caption("Subtract the mean from each value. Then make the answer positive.")
    true_abs = []
    checks = []
    for i,(lab,val) in enumerate(zip(labels,values)):
        dev = val-true_mean
        adev = abs(dev)
        true_abs.append(adev)
        c1,c2,c3,c4 = st.columns([1.6,1,1,1])
        c1.write(f"**{lab}**")
        c2.write(fmt(val))
        d = c3.number_input("Value − Mean", key=f"mad_dev_{i}", label_visibility="collapsed")
        a = c4.number_input("Absolute deviation", min_value=0.0, key=f"mad_abs_{i}", label_visibility="collapsed")
        checks.append(math.isclose(d,dev,abs_tol=.05) and math.isclose(a,adev,abs_tol=.05))

    true_mad = sum(true_abs)/len(true_abs)
    st.markdown("### 4. Find the MAD")
    mad_ans = st.number_input("MAD", min_value=0.0, key="mad_final")
    if st.button("Check My MAD",use_container_width=True):
        if all(checks) and math.isclose(mad_ans,true_mad,abs_tol=.05):
            st.success(f"✅ Correct! MAD = {true_mad:.2f}")
        elif math.isclose(mad_ans,true_mad,abs_tol=.05):
            st.success(f"✅ Your final MAD is correct: {true_mad:.2f}. Check any unfinished rows above.")
        else:
            st.info(f"Find the mean of the {len(true_abs)} absolute deviations.")

    st.markdown("### 5. Look at the spread")
    st.scatter_chart([{"Value":v,"Row":1} for v in values],x="Value",y="Row",use_container_width=True)
    obs = st.text_area("What does the MAD tell you about this athlete's consistency?", key="mad_observation")
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
