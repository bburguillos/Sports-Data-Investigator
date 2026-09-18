
import streamlit as st
import json
import math
import random
import uuid
import base64
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

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


st.markdown("""
<style>
:root {
    --bg:#07111f;
    --panel:#0f1b2d;
    --text:#f8fafc;
    --muted:#a8b3c7;
    --line:rgba(255,255,255,.11);
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(59,130,246,.15), transparent 27%),
        radial-gradient(circle at 88% 12%, rgba(14,165,233,.08), transparent 24%),
        linear-gradient(180deg,#07111f 0%,#0b1524 100%);
    color:var(--text);
}
.main .block-container {
    max-width:1180px;
    padding-top:1.05rem;
    padding-bottom:4rem;
}
h1,h2,h3 {color:#fff!important; letter-spacing:-.02em;}
.stMarkdown p,.stMarkdown li,[data-testid="stCaptionContainer"] p {color:#d8e0ec!important;}

div[data-testid="stSelectbox"] > label,
div[data-testid="stTextArea"] > label,
div[data-testid="stTextInput"] > label,
div[data-testid="stNumberInput"] > label,
div[data-testid="stRadio"] > label {
    color:#f8fafc!important;
    font-weight:800;
}
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] span,
div[data-testid="stRadio"] [role="radiogroup"] label,
div[data-testid="stRadio"] [role="radiogroup"] label p {
    color:#f8fafc !important;
    opacity:1 !important;
}
div[data-testid="stRadio"] [role="radiogroup"] {
    background:rgba(255,255,255,.045);
    border:1px solid rgba(255,255,255,.09);
    border-radius:14px;
    padding:.55rem .65rem;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background:#fff!important;
    color:#0f172a!important;
    border-radius:12px!important;
    border:1px solid #cbd5e1!important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
    color:#0f172a!important;
    fill:#0f172a!important;
}
[role="listbox"],[role="option"] {background:#fff!important;color:#0f172a!important;}
[role="option"] * {color:#0f172a!important;}
[role="option"]:hover,[role="option"][aria-selected="true"] {
    background:#e8eef7!important;
    color:#0f172a!important;
}
input,textarea {
    background:#fff!important;
    color:#111827!important;
    border-radius:12px!important;
}

.hero {
    background:
        linear-gradient(135deg,rgba(59,130,246,.22),rgba(14,165,233,.07)),
        rgba(255,255,255,.04);
    border:1px solid rgba(96,165,250,.28);
    border-radius:22px;
    padding:1.35rem 1.5rem;
    margin-bottom:.8rem;
    box-shadow:0 18px 45px rgba(0,0,0,.18);
}
.hero h1 {margin-bottom:.15rem;font-size:2.3rem;}
.hero p {margin:0;color:#cbd5e1!important;font-size:1rem;}

.card {
    background:linear-gradient(180deg,rgba(255,255,255,.065),rgba(255,255,255,.035));
    border:1px solid var(--line);
    border-radius:18px;
    padding:1rem 1.2rem;
    margin:.8rem 0 1rem;
    box-shadow:0 12px 30px rgba(0,0,0,.12);
}
.step {
    color:#7dd3fc;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.08em;
    font-size:.82rem;
    margin-bottom:.25rem;
}
.formula {
    background:linear-gradient(180deg,#fff,#f1f5f9);
    color:#0f172a;
    border-radius:14px;
    padding:.9rem 1rem;
    font-weight:900;
    margin:.65rem 0 1rem;
    border-left:5px solid #3b82f6;
    box-shadow:0 8px 24px rgba(0,0,0,.10);
}
.score {
    font-size:3.2rem;
    font-weight:950;
    text-align:center;
    color:#fff;
    margin:.35rem 0 1rem;
}
div.stButton > button {
    border-radius:12px!important;
    min-height:46px;
    font-weight:850!important;
    box-shadow:0 7px 18px rgba(0,0,0,.10);
}
[data-testid="stAlert"] {border-radius:14px!important;}
[data-testid="stDataFrame"] {
    border-radius:14px;
    overflow:hidden;
    border:1px solid var(--line);
}
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background:rgba(255,255,255,.03);
    border:1px solid var(--line);
    border-radius:16px;
    padding:.55rem;
}
[data-testid="stMetricValue"] {color:#fff!important;font-weight:900;}
[data-testid="stMetricLabel"] {color:#a8b3c7!important;}

.progress-ribbon {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:.5rem;
    margin:.65rem 0 1.15rem;
}
.progress-chip {
    background:rgba(255,255,255,.055);
    border:1px solid rgba(255,255,255,.10);
    border-radius:12px;
    padding:.62rem .55rem;
    text-align:center;
    color:#cbd5e1;
    font-weight:800;
    font-size:.82rem;
}
.progress-chip strong {
    color:#fff;
    margin-right:.25rem;
}
hr {
    border:none!important;
    border-top:1px solid rgba(255,255,255,.10)!important;
    margin:1.6rem 0!important;
}

/* High-visibility action buttons */
div.stButton > button,
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: 1px solid #60a5fa !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 850 !important;
    box-shadow: 0 7px 18px rgba(0,0,0,.18) !important;
}
div.stButton > button *,
div[data-testid="stDownloadButton"] > button * {
    color: #ffffff !important;
}
div.stButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    border-color: #93c5fd !important;
    transform: translateY(-1px);
}
div.stButton > button:active,
div[data-testid="stDownloadButton"] > button:active {
    transform: translateY(0);
    background: #1e40af !important;
}
div.stButton > button:focus,
div[data-testid="stDownloadButton"] > button:focus {
    color: #ffffff !important;
    border-color: #bfdbfe !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,.28) !important;
}

/* Make final completion/download actions distinct */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(180deg, #16a34a 0%, #15803d 100%) !important;
    border-color: #4ade80 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%) !important;
    border-color: #86efac !important;
}

</style>
""", unsafe_allow_html=True)

def reset_work():
    keep = {"sport_select","athlete_select","mode_select"}
    for key in list(st.session_state.keys()):
        if key not in keep and (
            key.startswith("pc_") or key.startswith("mad_") or key.startswith("freq_")
            or key.startswith("coach_")
            or key in {"claim","observation","revised","score_result","ready_to_revise","coach_stage","coach_answers","completion_id"}
        ):
            del st.session_state[key]

def parse_student_number(value):
    """Allow blank answer boxes while safely parsing student-entered numbers."""
    if value is None:
        return None
    text = str(value).strip().replace(",", "").replace("%", "")
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None

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



def encode_assignment(config):
    raw = json.dumps(config, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

def decode_assignment(code):
    try:
        text = str(code).strip()
        padding = "=" * (-len(text) % 4)
        raw = base64.urlsafe_b64decode((text + padding).encode("utf-8"))
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None

RATE_CASES = {
    "NFL": {
        "Patrick Mahomes": {"total": 4839, "games": 17, "projection_games": 12, "label": "passing yards",
                           "unit": "passing yards per game", "story": "Patrick Mahomes threw for 4,839 yards over 17 games."},
        "Josh Allen": {"total": 42, "games": 17, "projection_games": 10, "label": "total touchdowns",
                       "unit": "total touchdowns per game", "story": "Josh Allen recorded 42 total touchdowns over 17 games."},
        "Justin Jefferson": {"total": 1616, "games": 17, "projection_games": 12, "label": "receiving yards",
                             "unit": "receiving yards per game", "story": "Justin Jefferson recorded 1,616 receiving yards over 17 games."},
        "Dan Marino": {"total": 5084, "games": 16, "projection_games": 12, "label": "passing yards",
                       "unit": "passing yards per game", "story": "Dan Marino threw for 5,084 yards over 16 games in 1984."},
    },
    "NBA": {
        "LeBron James": {"total": 1695, "games": 63, "projection_games": 70, "label": "points",
                         "unit": "points per game", "story": "LeBron James scored 1,695 points over 63 games."},
        "Stephen Curry": {"total": 337, "games": 63, "projection_games": 70, "label": "made 3-pointers",
                          "unit": "made 3-pointers per game", "story": "Stephen Curry made 337 three-pointers over 63 games."},
        "Michael Jordan": {"total": 3041, "games": 82, "projection_games": 60, "label": "points",
                           "unit": "points per game", "story": "Michael Jordan scored 3,041 points over 82 games in 1986-87."},
    },
    "MLB": {
        "Aaron Judge": {"total": 62, "games": 157, "projection_games": 100, "label": "home runs",
                        "unit": "home runs per game", "story": "Aaron Judge hit 62 home runs over 157 games in 2022."},
        "Shohei Ohtani": {"total": 54, "games": 159, "projection_games": 100, "label": "home runs",
                          "unit": "home runs per game", "story": "Shohei Ohtani hit 54 home runs over 159 games."},
        "Babe Ruth": {"total": 59, "games": 152, "projection_games": 100, "label": "home runs",
                      "unit": "home runs per game", "story": "Babe Ruth hit 59 home runs over 152 games in 1921."},
    },
    "NHL": {
        "Connor McDavid": {"total": 153, "games": 82, "projection_games": 60, "label": "points",
                           "unit": "points per game", "story": "Connor McDavid recorded 153 points over 82 games."},
        "Auston Matthews": {"total": 69, "games": 81, "projection_games": 60, "label": "goals",
                            "unit": "goals per game", "story": "Auston Matthews scored 69 goals over 81 games."},
        "Wayne Gretzky": {"total": 212, "games": 80, "projection_games": 60, "label": "points",
                          "unit": "points per game", "story": "Wayne Gretzky recorded 212 points over 80 games in 1981-82."},
    },
    "Soccer": {
        "Lionel Messi": {"total": 43, "games": 38, "projection_games": 30, "label": "league goals",
                         "unit": "league goals per match", "story": "Lionel Messi scored 43 league goals over 38 matches in 2014-15."},
        "Erling Haaland": {"total": 36, "games": 35, "projection_games": 30, "label": "league goals",
                           "unit": "league goals per match", "story": "Erling Haaland scored 36 league goals over 35 matches in 2022-23."},
        "Pelé": {"total": 6, "games": 4, "projection_games": 7, "label": "World Cup goals",
                 "unit": "World Cup goals per match", "story": "Pelé scored 6 goals over 4 matches at the 1958 World Cup."},
    },
    "Formula 1": {
        "Max Verstappen": {"total": 575, "games": 22, "projection_games": 20, "label": "championship points",
                           "unit": "championship points per race", "story": "Max Verstappen scored 575 championship points over 22 races in 2023."},
        "Lewis Hamilton": {"total": 413, "games": 21, "projection_games": 20, "label": "championship points",
                           "unit": "championship points per race", "story": "Lewis Hamilton scored 413 championship points over 21 races in 2019."},
        "Ayrton Senna": {"total": 90, "games": 16, "projection_games": 12, "label": "championship points",
                         "unit": "championship points per race", "story": "Ayrton Senna scored 90 championship points over 16 races in 1988."},
    },
}

def rate_tolerance(correct):
    return max(0.1, abs(correct) * 0.015)

def ratios_rates_engine(sport_filter="Any Sport", difficulty="Guided"):
    st.markdown('<div class="step">7th Grade Math Lab · Ratios, Rates & Proportions</div>', unsafe_allow_html=True)
    st.subheader("🏁 Sports Rate Lab")
    st.write(
        "Use the sports situation to decide what math you need. "
        "Try each step first — the app gives stronger help only after repeated mistakes."
    )

    allowed = list(RATE_CASES)
    if sport_filter != "Any Sport":
        allowed = [sport_filter]

    a, b = st.columns(2)
    with a:
        sport = st.selectbox(
            "Sport",
            allowed,
            format_func=lambda s:f"{SPORT_ICONS.get(s,'')} {s}",
            key="rate_sport"
        )
    with b:
        athlete = st.selectbox(
            "Athlete",
            list(RATE_CASES[sport]),
            key="rate_athlete"
        )

    case = RATE_CASES[sport][athlete]
    total = float(case["total"])
    games = float(case["games"])
    target_games = float(case["projection_games"])
    true_rate = total / games
    true_projection = true_rate * target_games

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport}</div>
      <h2>{athlete}</h2>
      <p><b>Situation:</b> {case["story"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # STEP 1 — Student constructs ratio independently
    # -----------------------------
    st.markdown("### Step 1 · Write a ratio")
    st.write(
        "Write a ratio that compares the athlete's total statistic to the number of games, matches, or races."
    )
    ratio_raw = st.text_input(
        "Your ratio",
        key="rate_ratio",
        placeholder="Type your ratio"
    )

    if "ratio_attempts" not in st.session_state:
        st.session_state.ratio_attempts = 0

    def ratio_is_correct(text):
        compact = str(text).lower().replace(" ", "").replace(",", "")
        acceptable = {
            f"{int(total)}/{int(games)}",
            f"{int(total)}:{int(games)}",
            f"{int(total)}÷{int(games)}",
            f"{int(total)}/{int(games)}games",
        }
        return compact in acceptable

    if st.button("Check My Ratio", use_container_width=True):
        if ratio_is_correct(ratio_raw):
            st.success("✅ Yes. You compared the total statistic to the number of games.")
            st.session_state.ratio_attempts = 0
        else:
            st.session_state.ratio_attempts += 1
            if st.session_state.ratio_attempts == 1:
                st.info(
                    "Look back at the situation. Which number is the total statistic, "
                    "and which number tells how many games, matches, or races were played?"
                )
            else:
                st.warning(
                    f"Use the total first and the number of games second: "
                    f"**{fmt(total)} to {fmt(games)}**. "
                    "You may write a ratio with a colon, fraction bar, or division sign."
                )

    # -----------------------------
    # STEP 2 — Unit rate; no formula shown first
    # -----------------------------
    st.markdown("### Step 2 · Find the unit rate")
    st.write(
        f"How many **{case['unit']}** did {athlete} average?"
    )
    rate_raw = st.text_input(
        "Unit rate",
        key="rate_unit_answer",
        placeholder="Type your answer"
    )
    rate_ans = parse_student_number(rate_raw)

    if "rate_attempts" not in st.session_state:
        st.session_state.rate_attempts = 0

    if st.button("Check My Unit Rate", use_container_width=True):
        if rate_ans is not None and math.isclose(
            rate_ans, true_rate, abs_tol=rate_tolerance(true_rate)
        ):
            st.success(
                f"✅ Correct — or close enough. About **{true_rate:.2f} {case['unit']}**."
            )
            st.session_state.rate_attempts = 0
        else:
            st.session_state.rate_attempts += 1
            if st.session_state.rate_attempts == 1:
                st.info(
                    "A unit rate tells the amount for **1** game, match, or race. "
                    "Think about which operation would turn the game total into 1."
                )
            else:
                st.warning(
                    f"Now use **{fmt(total)} ÷ {fmt(games)}**. "
                    f"That gives about **{true_rate:.2f}**."
                )

    # -----------------------------
    # STEP 3 — Proportional prediction; setup not pre-given
    # -----------------------------
    st.markdown("### Step 3 · Make a proportional prediction")
    st.write(
        f"If the same rate continued for **{fmt(target_games)}** games, matches, or races, "
        "what total would you predict?"
    )

    setup_raw = st.text_input(
        "How would you set up the math?",
        key="rate_proportion_setup",
        placeholder="Write an equation, proportion, or calculation"
    )

    pred_raw = st.text_input(
        "Predicted total",
        key="rate_projection",
        placeholder="Type your answer"
    )
    pred_ans = parse_student_number(pred_raw)

    if "projection_attempts" not in st.session_state:
        st.session_state.projection_attempts = 0

    if st.button("Check My Prediction", use_container_width=True):
        tol = max(0.5, abs(true_projection) * 0.02)
        if pred_ans is not None and math.isclose(
            pred_ans, true_projection, abs_tol=tol
        ):
            st.success(
                f"✅ Good prediction. About **{true_projection:.1f}** is reasonable."
            )
            st.session_state.projection_attempts = 0
        else:
            st.session_state.projection_attempts += 1
            if st.session_state.projection_attempts == 1:
                st.info(
                    "Use the unit rate you found in Step 2. "
                    "How can you use that rate with the new number of games?"
                )
            else:
                st.warning(
                    f"Multiply the unit rate, about **{true_rate:.2f}**, "
                    f"by **{fmt(target_games)}**."
                )
                if difficulty == "Guided":
                    st.caption(
                        f"Another valid setup is: {fmt(total)} / {fmt(games)} = x / {fmt(target_games)}."
                    )

    # -----------------------------
    # STEP 4 — Conceptual reasoning
    # -----------------------------
    st.markdown("### Step 4 · Is the relationship proportional?")
    answer = st.radio(
        "If the same rate continues, is this a proportional relationship?",
        ["Yes", "No", "I'm not sure"],
        horizontal=True,
        key="rate_proportional"
    )

    if st.button("Check Proportional Thinking", use_container_width=True):
        if answer == "Yes":
            st.success(
                "✅ Yes. The model assumes the same unit rate stays constant."
            )
        else:
            st.info(
                "A proportional relationship has a constant unit rate. "
                "In this model, we are assuming the athlete continues at the same rate."
            )

    # -----------------------------
    # STEP 5 — Explanation
    # -----------------------------
    st.markdown("### Step 5 · Explain your reasoning")
    st.text_area(
        "Explain what the unit rate means in this sports situation.",
        key="rate_explanation",
        placeholder="Explain it in your own words."
    )



# =========================================================
# 7TH GRADE MATH LAB — EQUATIONS & INEQUALITIES
# =========================================================
EQUATION_CASES = {
    "NFL": [
        {
            "title": "Touchdown Pace",
            "kind": "Equation",
            "story": "A running back has scored 6 touchdowns in 3 games at the same rate each game.",
            "question": "If x is the average touchdowns per game, what is x?",
            "models": ["3x = 6", "x + 3 = 6", "6x = 3", "x - 3 = 6"],
            "correct_model": "3x = 6",
            "answer": 2,
            "unit": "touchdowns per game",
            "hint1": "Three equal game amounts combine to make 6 touchdowns.",
            "hint2": "3x = 6, so divide both sides by 3.",
            "meaning": "The running back averaged 2 touchdowns per game."
        },
        {
            "title": "Fantasy Comeback",
            "kind": "Inequality",
            "story": "A fantasy football team has 94 points. It needs at least 118 points to win.",
            "question": "How many more points does the team need at minimum?",
            "models": ["94 + x ≥ 118", "94 + x ≤ 118", "94x ≥ 118", "118 + x ≥ 94"],
            "correct_model": "94 + x ≥ 118",
            "answer": 24,
            "unit": "points",
            "hint1": "The words 'at least' mean the final total can be 118 or greater.",
            "hint2": "118 − 94 = 24, so x must be at least 24.",
            "meaning": "The team needs 24 or more additional points."
        },
    ],
    "NBA": [
        {
            "title": "Target Scoring Average",
            "kind": "Equation",
            "story": "A player scored 22, 31, 27, 25, and 20 points in five games. The player wants a 26-point average after six games.",
            "question": "How many points must be scored in Game 6?",
            "models": ["125 + x = 156", "125 + x = 26", "125x = 156", "156 + x = 125"],
            "correct_model": "125 + x = 156",
            "answer": 31,
            "unit": "points",
            "hint1": "First think about the total points needed for a 26-point average over 6 games.",
            "hint2": "26 × 6 = 156 total points; 156 − 125 = 31.",
            "meaning": "The player must score 31 points in Game 6."
        },
        {
            "title": "Three-Pointer Challenge",
            "kind": "Equation",
            "story": "A team already has 52 points. Every remaining made three-pointer adds 3 points. The team wants exactly 70 points.",
            "question": "How many three-pointers are needed?",
            "models": ["52 + 3x = 70", "52 + x = 70", "3x = 70", "70 + 3x = 52"],
            "correct_model": "52 + 3x = 70",
            "answer": 6,
            "unit": "three-pointers",
            "hint1": "The team starts with 52, then each unknown three-pointer adds 3 more points.",
            "hint2": "52 + 3x = 70 → subtract 52, then divide by 3.",
            "meaning": "The team needs 6 more made three-pointers."
        },
    ],
    "MLB": [
        {
            "title": "Batting Practice Groups",
            "kind": "Equation",
            "story": "A coach has 72 baseballs and splits them equally among 6 batting stations.",
            "question": "How many baseballs should go to each station?",
            "models": ["6x = 72", "x + 6 = 72", "72x = 6", "x - 6 = 72"],
            "correct_model": "6x = 72",
            "answer": 12,
            "unit": "baseballs per station",
            "hint1": "Six equal groups make a total of 72.",
            "hint2": "6x = 72, so divide 72 by 6.",
            "meaning": "Each batting station gets 12 baseballs."
        },
        {
            "title": "Ballpark Budget",
            "kind": "Inequality",
            "story": "A class has $500 for a baseball trip. The bus costs $140, and each student ticket costs $18.",
            "question": "What is the greatest number of student tickets the class can buy?",
            "models": ["140 + 18x ≤ 500", "140 + 18x ≥ 500", "18 + 140x ≤ 500", "140x + 18 = 500"],
            "correct_model": "140 + 18x ≤ 500",
            "answer": 20,
            "unit": "student tickets",
            "hint1": "The total cost cannot go over $500.",
            "hint2": "500 − 140 = 360, and 360 ÷ 18 = 20.",
            "meaning": "The class can buy at most 20 student tickets."
        },
    ],
    "NHL": [
        {
            "title": "Penalty Minutes Drop",
            "kind": "Equation",
            "story": "A player had 18 penalty minutes, then reduced the total by x minutes to finish with 11.",
            "question": "How many penalty minutes were reduced?",
            "models": ["18 - x = 11", "18 + x = 11", "11 - x = 18", "18x = 11"],
            "correct_model": "18 - x = 11",
            "answer": 7,
            "unit": "minutes",
            "hint1": "The starting amount gets smaller by x.",
            "hint2": "18 − x = 11, so x = 7.",
            "meaning": "The player's total was reduced by 7 penalty minutes."
        },
        {
            "title": "Shots on Goal",
            "kind": "Inequality",
            "story": "A team has 21 shots on goal after two periods. The coach wants at least 32 shots by the end of the game.",
            "question": "How many shots are needed in the third period at minimum?",
            "models": ["21 + x ≥ 32", "21 + x ≤ 32", "21x ≥ 32", "32 + x ≥ 21"],
            "correct_model": "21 + x ≥ 32",
            "answer": 11,
            "unit": "shots",
            "hint1": "'At least 32' means 32 or more.",
            "hint2": "32 − 21 = 11, so x must be at least 11.",
            "meaning": "The team needs 11 or more third-period shots."
        },
    ],
    "Soccer": [
        {
            "title": "Training Sessions",
            "kind": "Equation",
            "story": "A player completes 4 identical shooting drills each session. After several sessions, the player has completed 28 drills.",
            "question": "How many training sessions were completed?",
            "models": ["4x = 28", "x + 4 = 28", "28x = 4", "x - 4 = 28"],
            "correct_model": "4x = 28",
            "answer": 7,
            "unit": "sessions",
            "hint1": "Each session contributes 4 drills.",
            "hint2": "4x = 28, so x = 7.",
            "meaning": "The player completed 7 training sessions."
        },
        {
            "title": "Tournament Points",
            "kind": "Inequality",
            "story": "A team has 7 tournament points. Each win is worth 3 points. The team wants at least 16 points.",
            "question": "What is the minimum number of additional wins needed?",
            "models": ["7 + 3x ≥ 16", "7 + 3x ≤ 16", "7x + 3 ≥ 16", "16 + 3x ≥ 7"],
            "correct_model": "7 + 3x ≥ 16",
            "answer": 3,
            "unit": "wins",
            "hint1": "Each win adds 3 points, and 'at least' means 16 or more.",
            "hint2": "16 − 7 = 9, and 9 ÷ 3 = 3.",
            "meaning": "The team needs at least 3 more wins."
        },
    ],
    "Formula 1": [
        {
            "title": "Pit Stop Average",
            "kind": "Equation",
            "story": "A team spends 48 total seconds on 6 equal-length pit stops.",
            "question": "If each pit stop takes x seconds, what is x?",
            "models": ["6x = 48", "x + 6 = 48", "48x = 6", "x - 6 = 48"],
            "correct_model": "6x = 48",
            "answer": 8,
            "unit": "seconds",
            "hint1": "Six equal pit-stop times add up to 48 seconds.",
            "hint2": "6x = 48, so divide by 6.",
            "meaning": "Each pit stop averaged 8 seconds."
        },
        {
            "title": "Race Weekend Budget",
            "kind": "Inequality",
            "story": "A fan has $420 for a race weekend. A hotel costs $180, and each event ticket costs $60.",
            "question": "What is the greatest number of event tickets the fan can buy?",
            "models": ["180 + 60x ≤ 420", "180 + 60x ≥ 420", "60 + 180x ≤ 420", "180x + 60 = 420"],
            "correct_model": "180 + 60x ≤ 420",
            "answer": 4,
            "unit": "tickets",
            "hint1": "The total spending cannot exceed $420.",
            "hint2": "420 − 180 = 240, and 240 ÷ 60 = 4.",
            "meaning": "The fan can buy at most 4 event tickets."
        },
    ],
}

def equations_inequalities_engine(sport_filter="Any Sport", difficulty="Guided"):
    st.markdown('<div class="step">7th Grade Math Lab · Equations & Inequalities</div>', unsafe_allow_html=True)
    st.subheader("⚖️ Sports Equation Lab")
    st.write(
        "Translate a sports situation into math, solve it, and explain what the answer means. "
        "Try first — stronger hints appear only after repeated mistakes."
    )

    sports = list(EQUATION_CASES)
    if sport_filter != "Any Sport":
        sports = [sport_filter]

    c1, c2 = st.columns(2)
    with c1:
        eq_sport = st.selectbox(
            "Sport",
            sports,
            format_func=lambda s: f"{SPORT_ICONS.get(s,'')} {s}",
            key="eq_sport"
        )
    case_options = EQUATION_CASES[eq_sport]
    labels = {f"{c['kind']} · {c['title']}": c for c in case_options}
    with c2:
        case_label = st.selectbox("Problem", list(labels), key="eq_case")
    case = labels[case_label]

    case_id = clean_filename(f"{eq_sport}_{case['title']}")

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(eq_sport,'')} {eq_sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 1: identify the unknown before seeing models.
    st.markdown("### Step 1 · Define the unknown")
    unknown = st.text_input(
        "What should x represent?",
        key=f"eq_unknown_{case_id}",
        placeholder="Explain what x means"
    )

    # Step 2: choose model.
    st.markdown("### Step 2 · Model the situation")
    st.write("Which mathematical statement best represents the situation?")

    model_order_key = f"eq_model_order_{case_id}"
    if model_order_key not in st.session_state:
        shuffled_models = list(case["models"])
        random.shuffle(shuffled_models)
        st.session_state[model_order_key] = shuffled_models

    model_choice = st.radio(
        "Choose a model",
        st.session_state[model_order_key],
        key=f"eq_model_{case_id}",
        label_visibility="collapsed"
    )

    model_attempt_key = f"eq_model_attempts_{case_id}"
    if model_attempt_key not in st.session_state:
        st.session_state[model_attempt_key] = 0

    if st.button("Check My Model", key=f"eq_model_check_{case_id}", use_container_width=True):
        if model_choice == case["correct_model"]:
            st.success("✅ Correct model.")
            st.session_state[model_attempt_key] = 0
        else:
            st.session_state[model_attempt_key] += 1
            if st.session_state[model_attempt_key] == 1:
                if case["kind"] == "Inequality":
                    st.info("Pay attention to words such as **at least**, **at most**, or **cannot exceed**.")
                else:
                    st.info("Ask yourself: what operation connects the current amount, the unknown, and the target?")
            else:
                st.warning(f"A correct model is **{case['correct_model']}**.")

    # Step 3: solve.
    st.markdown("### Step 3 · Solve")
    answer_raw = st.text_input(
        f"What is x? ({case['unit']})",
        key=f"eq_answer_{case_id}",
        placeholder="Type your answer"
    )
    answer = parse_student_number(answer_raw)

    answer_attempt_key = f"eq_answer_attempts_{case_id}"
    if answer_attempt_key not in st.session_state:
        st.session_state[answer_attempt_key] = 0

    if st.button("Check My Solution", key=f"eq_answer_check_{case_id}", use_container_width=True):
        if answer is not None and math.isclose(answer, float(case["answer"]), abs_tol=0.1):
            st.success(f"✅ Correct. x = {fmt(float(case['answer']))} {case['unit']}.")
            st.session_state[answer_attempt_key] = 0
        else:
            st.session_state[answer_attempt_key] += 1
            if st.session_state[answer_attempt_key] == 1:
                st.info(case["hint1"])
            else:
                st.warning(case["hint2"])

    # Step 4: inequality-specific thinking or equation check.
    st.markdown("### Step 4 · Interpret the solution")
    if case["kind"] == "Inequality":
        interpretation_options = [
            case["meaning"],
            f"The answer must be exactly {fmt(float(case['answer']))} {case['unit']} and cannot be more.",
            "There is not enough information to interpret the solution."
        ]
    else:
        interpretation_options = [
            case["meaning"],
            f"The current total is already {fmt(float(case['answer']))} {case['unit']}.",
            "The variable does not represent a quantity in this situation."
        ]

    interpretation_order_key = f"eq_interpret_order_{case_id}"
    if interpretation_order_key not in st.session_state:
        shuffled_interpretations = list(interpretation_options)
        random.shuffle(shuffled_interpretations)
        st.session_state[interpretation_order_key] = shuffled_interpretations

    interpretation = st.radio(
        "Which statement best explains the solution?",
        st.session_state[interpretation_order_key],
        key=f"eq_interpret_{case_id}"
    )

    if st.button("Check My Interpretation", key=f"eq_interpret_check_{case_id}", use_container_width=True):
        if interpretation == case["meaning"]:
            st.success("✅ Yes — that correctly explains the answer in context.")
        else:
            st.info("Go back to what x represents and connect the solution to the original question.")

    # Step 5: written reasoning.
    st.markdown("### Step 5 · Explain your reasoning")
    st.text_area(
        "Explain how you solved the problem and why your answer makes sense.",
        key=f"eq_reasoning_{case_id}",
        placeholder="Explain your steps in your own words."
    )

# =========================================================
# SPORTS MATH CHALLENGE — MULTI-SKILL HIGHER-LEVEL THINKING
# =========================================================
CHALLENGE_CASES = [
    {
        "id": "nba_average_target",
        "level": "Level 1 · Connect Two Skills",
        "sport": "NBA",
        "title": "Raise the Average",
        "story": "A player scored 18, 24, 31, 27, and 20 points in five games. After Game 6, the player wants a 25-point average.",
        "parts": [
            {
                "prompt": "How many total points were scored in the first five games?",
                "answer": 120,
                "tol": 0.1,
                "hint1": "Add all five game totals.",
                "hint2": "18 + 24 + 31 + 27 + 20 = 120."
            },
            {
                "prompt": "How many total points are needed after six games to average 25 points per game?",
                "answer": 150,
                "tol": 0.1,
                "hint1": "Think: average × number of games.",
                "hint2": "25 × 6 = 150."
            },
            {
                "prompt": "How many points must the player score in Game 6?",
                "answer": 30,
                "tol": 0.1,
                "hint1": "Compare the total needed with the current total.",
                "hint2": "150 − 120 = 30."
            },
        ],
        "reflection": "Explain why scoring 30 points in Game 6 would produce exactly a 25-point average."
    },
    {
        "id": "nfl_rate_percent",
        "level": "Level 2 · Multi-Step Investigation",
        "sport": "NFL",
        "title": "Which Season Was More Productive?",
        "story": "A quarterback threw for 3,600 yards in 12 games one season and 4,250 yards in 15 games the next season.",
        "parts": [
            {
                "prompt": "What was the passing-yards-per-game rate in the first season?",
                "answer": 300,
                "tol": 0.5,
                "hint1": "Find the amount for 1 game.",
                "hint2": "3,600 ÷ 12 = 300."
            },
            {
                "prompt": "What was the passing-yards-per-game rate in the second season?",
                "answer": 283.3333333,
                "tol": 0.6,
                "hint1": "Again, find the amount for 1 game.",
                "hint2": "4,250 ÷ 15 ≈ 283.33."
            },
            {
                "prompt": "By about what percent did the yards-per-game rate change from Season 1 to Season 2? Enter a negative percent for a decrease.",
                "answer": -5.5555556,
                "tol": 0.6,
                "hint1": "Use the change divided by the old rate, then multiply by 100.",
                "hint2": "(283.33 − 300) ÷ 300 × 100 ≈ −5.56%."
            },
        ],
        "reflection": "The second season had more total yards. Explain why the first season still had the better yards-per-game rate."
    },
    {
        "id": "mlb_probability_projection",
        "level": "Level 1 · Connect Two Skills",
        "sport": "MLB",
        "title": "Home Run Projection",
        "story": "A hitter recorded a home run in 8 of 20 games.",
        "parts": [
            {
                "prompt": "What is the experimental probability of a home run in a game as a decimal?",
                "answer": 0.4,
                "tol": 0.01,
                "hint1": "Use successes ÷ total trials.",
                "hint2": "8 ÷ 20 = 0.40."
            },
            {
                "prompt": "What is that probability as a percent?",
                "answer": 40,
                "tol": 0.2,
                "hint1": "Convert the decimal to a percent.",
                "hint2": "0.40 × 100 = 40%."
            },
            {
                "prompt": "At the same rate, about how many of the next 50 games would you predict include a home run?",
                "answer": 20,
                "tol": 0.5,
                "hint1": "Use the probability with 50 games.",
                "hint2": "0.40 × 50 = 20."
            },
        ],
        "reflection": "Why is 20 a prediction rather than a guarantee?"
    },
    {
        "id": "nhl_mean_outlier",
        "level": "Level 2 · Multi-Step Investigation",
        "sport": "NHL",
        "title": "The Outlier Game",
        "story": "A hockey player recorded 2, 3, 2, 4, 3, and 10 shots on goal across six games.",
        "parts": [
            {
                "prompt": "What is the mean number of shots per game?",
                "answer": 4,
                "tol": 0.1,
                "hint1": "Add all six values and divide by 6.",
                "hint2": "24 ÷ 6 = 4."
            },
            {
                "prompt": "What is the median number of shots per game?",
                "answer": 3,
                "tol": 0.1,
                "hint1": "Order the values and find the middle.",
                "hint2": "2, 2, 3, 3, 4, 10 → median = 3."
            },
            {
                "prompt": "If the 10-shot game were removed, what would the new mean be?",
                "answer": 2.8,
                "tol": 0.1,
                "hint1": "Remove 10 from the total and divide by 5.",
                "hint2": "14 ÷ 5 = 2.8."
            },
        ],
        "reflection": "Which measure, mean or median, better describes a typical game here? Defend your answer."
    },
    {
        "id": "soccer_ticket_budget",
        "level": "Level 2 · Multi-Step Investigation",
        "sport": "Soccer",
        "title": "Team Trip Budget",
        "story": "A class trip to a soccer match costs $28 per student plus a one-time $120 bus fee. The class has a $960 budget.",
        "parts": [
            {
                "prompt": "After paying the bus fee, how much money remains for student tickets?",
                "answer": 840,
                "tol": 0.1,
                "hint1": "Subtract the fixed cost from the budget.",
                "hint2": "960 − 120 = 840."
            },
            {
                "prompt": "What is the greatest whole number of students who can attend?",
                "answer": 30,
                "tol": 0.1,
                "hint1": "Divide the money available for tickets by the price per ticket.",
                "hint2": "840 ÷ 28 = 30."
            },
            {
                "prompt": "How much would the trip cost for 27 students?",
                "answer": 876,
                "tol": 0.1,
                "hint1": "Ticket cost plus the one-time bus fee.",
                "hint2": "27 × 28 + 120 = 876."
            },
        ],
        "reflection": "Write an inequality that could represent the budget situation and explain what the variable means."
    },
    {
        "id": "f1_points_rate",
        "level": "Level 3 · Open Challenge",
        "sport": "Formula 1",
        "title": "Championship Pace",
        "story": "Driver A earned 168 points in 8 races. Driver B earned 195 points in 10 races.",
        "parts": [
            {
                "prompt": "What is Driver A's points-per-race rate?",
                "answer": 21,
                "tol": 0.1,
                "hint1": "Find points for 1 race.",
                "hint2": "168 ÷ 8 = 21."
            },
            {
                "prompt": "What is Driver B's points-per-race rate?",
                "answer": 19.5,
                "tol": 0.1,
                "hint1": "Find points for 1 race.",
                "hint2": "195 ÷ 10 = 19.5."
            },
            {
                "prompt": "If both rates continued for 20 races, how many more points would Driver A be projected to score than Driver B?",
                "answer": 30,
                "tol": 0.5,
                "hint1": "Project each driver's total over 20 races, then compare.",
                "hint2": "A: 21×20=420; B: 19.5×20=390; difference = 30."
            },
        ],
        "reflection": "Driver B currently has more total points. Explain why Driver A can still be on the stronger pace."
    },
    {
        "id": "nba_discount_ticket",
        "level": "Level 1 · Connect Two Skills",
        "sport": "NBA",
        "title": "Ticket Discount",
        "story": "A basketball ticket costs $80. A school group receives a 15% discount, then pays a $6 service fee per ticket.",
        "parts": [
            {
                "prompt": "How much money is the 15% discount?",
                "answer": 12,
                "tol": 0.1,
                "hint1": "Find 15% of 80.",
                "hint2": "0.15 × 80 = 12."
            },
            {
                "prompt": "What is the discounted ticket price before the service fee?",
                "answer": 68,
                "tol": 0.1,
                "hint1": "Subtract the discount from the original price.",
                "hint2": "80 − 12 = 68."
            },
            {
                "prompt": "What is the final cost for 5 tickets after the fee is added to each ticket?",
                "answer": 370,
                "tol": 0.1,
                "hint1": "Add the $6 fee to one discounted ticket, then multiply by 5.",
                "hint2": "(68 + 6) × 5 = 370."
            },
        ],
        "reflection": "Explain why taking 15% off the final group total would not give the same answer."
    },
    {
        "id": "mlb_compare_samples",
        "level": "Level 3 · Open Challenge",
        "sport": "MLB",
        "title": "Can We Trust the Sample?",
        "story": "Player A had 9 hits in a 20-at-bat sample. Later, over 100 at-bats, the same player had 31 hits.",
        "parts": [
            {
                "prompt": "What was the hit rate in the 20-at-bat sample as a percent?",
                "answer": 45,
                "tol": 0.2,
                "hint1": "Hits ÷ at-bats × 100.",
                "hint2": "9 ÷ 20 × 100 = 45%."
            },
            {
                "prompt": "What was the hit rate over 100 at-bats as a percent?",
                "answer": 31,
                "tol": 0.2,
                "hint1": "Hits ÷ at-bats × 100.",
                "hint2": "31 ÷ 100 × 100 = 31%."
            },
            {
                "prompt": "How many percentage points apart are the two rates?",
                "answer": 14,
                "tol": 0.2,
                "hint1": "Subtract the smaller percent from the larger.",
                "hint2": "45 − 31 = 14 percentage points."
            },
        ],
        "reflection": "Which sample would you trust more for predicting future performance, and why?"
    },
]

def challenge_lab_engine(level_filter="Any Level", sport_filter="Any Sport"):
    st.markdown('<div class="step">Sports Math Challenge · Multi-Skill Reasoning</div>', unsafe_allow_html=True)
    st.subheader("🧠 Sports Math Challenge")
    st.write(
        "These problems do not tell you which math skill to use. "
        "Figure out what information matters, choose a strategy, and defend your reasoning."
    )

    cases = CHALLENGE_CASES
    if level_filter != "Any Level":
        cases = [c for c in cases if c["level"] == level_filter]
    if sport_filter != "Any Sport":
        cases = [c for c in cases if c["sport"] == sport_filter]

    if not cases:
        st.info("No challenge matches those filters yet.")
        return

    choices = {f"{c['sport']} · {c['title']}": c for c in cases}
    selected_label = st.selectbox("Choose a challenge", list(choices), key="challenge_choice")
    case = choices[selected_label]

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(case['sport'],'')} {case['sport']} · {case['level']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
    </div>
    """, unsafe_allow_html=True)

    plan = st.text_area(
        "Before calculating, what do you think you need to figure out?",
        key=f"challenge_plan_{case['id']}",
        placeholder="Describe your plan. You do not need to name a formula."
    )

    current_results = []

    for i, part in enumerate(case["parts"], start=1):
        st.markdown(f"### Part {i}")
        st.write(part["prompt"])
        raw = st.text_input(
            f"Answer for Part {i}",
            key=f"challenge_{case['id']}_{i}",
            placeholder="Type your answer"
        )
        ans = parse_student_number(raw)
        is_correct_now = (
            ans is not None
            and math.isclose(ans, float(part["answer"]), abs_tol=float(part["tol"]))
        )
        current_results.append(is_correct_now)

        attempt_key = f"challenge_attempts_{case['id']}_{i}"
        if attempt_key not in st.session_state:
            st.session_state[attempt_key] = 0

        if st.button(
            f"Check Part {i}",
            key=f"challenge_check_{case['id']}_{i}",
            use_container_width=True
        ):
            if is_correct_now:
                st.success("✅ Correct — or within the accepted rounding range.")
            else:
                st.session_state[attempt_key] += 1
                if st.session_state[attempt_key] == 1:
                    st.info(part["hint1"])
                else:
                    st.warning(part["hint2"])

    st.markdown("### Final Reasoning")
    st.write(case["reflection"])
    reasoning_key = f"challenge_reflection_{case['id']}"
    reasoning = st.text_area(
        "Your explanation",
        key=reasoning_key,
        placeholder="Use numbers from your work and explain your thinking."
    )

    st.markdown("---")
    st.markdown('<div class="step">Finish & Submit</div>', unsafe_allow_html=True)
    st.write(
        "When your math is correct and your final reasoning is complete, submit the challenge "
        "to unlock your completion receipt."
    )

    submitted_key = f"challenge_submitted_{case['id']}"
    completion_key = f"challenge_completion_id_{case['id']}"

    if st.button(
        "✅ Submit Final Reasoning & Complete Challenge",
        key=f"challenge_submit_{case['id']}",
        use_container_width=True
    ):
        student_name = st.session_state.get("challenge_student_name", "").strip()
        class_period = st.session_state.get("challenge_class_period", "").strip()
        missing = []

        if not student_name:
            missing.append("student name")
        if not class_period:
            missing.append("class period")
        if not all(current_results):
            missing.append("all math parts correct")
        if len(reasoning.strip()) < 20:
            missing.append("a complete final reasoning response")

        if missing:
            st.session_state[submitted_key] = False
            st.warning(
                "Before submitting, complete: " + ", ".join(missing) + "."
            )
        else:
            if completion_key not in st.session_state:
                st.session_state[completion_key] = uuid.uuid4().hex[:8].upper()
            st.session_state[submitted_key] = True

    if st.session_state.get(submitted_key, False):
        completion_id = st.session_state.get(completion_key, "")
        student_name = st.session_state.get("challenge_student_name", "").strip()
        class_period = st.session_state.get("challenge_class_period", "").strip()

        st.success(
            f"🏁 Challenge Complete · Completion ID: **{completion_id}**"
        )

        pdf_bytes = build_challenge_submission_pdf(
            student_name=student_name,
            class_period=class_period,
            case=case,
            plan=plan,
            reasoning=reasoning,
            completion_id=completion_id,
        )

        filename = (
            f"Sports_Math_Challenge_"
            f"{clean_filename(student_name)}_"
            f"{clean_filename(case['title'])}_"
            f"{completion_id}.pdf"
        )

        st.download_button(
            "📄 Download My Completion Report",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            key=f"challenge_download_{case['id']}",
            use_container_width=True,
        )
        st.caption(
            "Your report includes the challenge, your plan, your answers, your final reasoning, "
            "attempt counts, and your unique completion ID."
        )

def build_challenge_submission_pdf(student_name, class_period, case, plan, reasoning, completion_id):
    """Generate the Sports Math Challenge completion receipt."""
    buffer = BytesIO()
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.55*inch,
        leftMargin=0.55*inch,
        topMargin=0.55*inch,
        bottomMargin=0.55*inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ChallengeTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=21,
        spaceAfter=8,
        textColor=colors.HexColor("#0F2747"),
    )
    heading = ParagraphStyle(
        "ChallengeHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor("#173F73"),
    )
    body = ParagraphStyle(
        "ChallengeBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1F2937"),
    )
    small = ParagraphStyle(
        "ChallengeSmall",
        parent=body,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4B5563"),
    )

    story = []
    story.append(Paragraph("Sports Math Challenge - Completion Report", title_style))
    story.append(Paragraph(
        f"<b>Completion ID:</b> {completion_id} &nbsp;&nbsp;&nbsp; "
        f"<b>Generated:</b> {generated}",
        small
    ))
    story.append(Spacer(1, 8))

    info_data = [
        ["Student", student_name, "Class Period", class_period],
        ["Sport", case["sport"], "Challenge Level", case["level"]],
        ["Challenge", case["title"], "", ""],
    ]
    info = Table(info_data, colWidths=[0.9*inch, 2.2*inch, 1.05*inch, 2.15*inch])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("SPAN", (1,2), (3,2)),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(info)

    story.append(Paragraph("Situation", heading))
    story.append(Paragraph(case["story"], body))

    story.append(Paragraph("Student Plan", heading))
    story.append(Paragraph(plan.strip() or "(No plan entered.)", body))

    story.append(Paragraph("Math Work", heading))
    work_rows = [["Part", "Question", "Student Answer", "Attempts"]]
    for i, part in enumerate(case["parts"], start=1):
        answer = st.session_state.get(f"challenge_{case['id']}_{i}", "")
        attempts = st.session_state.get(f"challenge_attempts_{case['id']}_{i}", 0)
        work_rows.append([
            str(i),
            Paragraph(part["prompt"], small),
            str(answer),
            str(attempts),
        ])

    work_table = Table(
        work_rows,
        repeatRows=1,
        colWidths=[0.45*inch, 4.15*inch, 1.15*inch, 0.7*inch],
    )
    work_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DCEBFA")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.45, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,1), (0,-1), "CENTER"),
        ("ALIGN", (2,1), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(work_table)

    story.append(Paragraph("Final Reasoning Question", heading))
    story.append(Paragraph(case["reflection"], body))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Student Response:</b>", body))
    story.append(Paragraph(reasoning.strip(), body))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Completion status: All numeric challenge parts were correct within the accepted "
        "rounding range, and a final reasoning response was submitted. The app does not "
        "automatically grade the quality of the written reasoning.",
        small
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def clean_filename(text):
    safe = "".join(ch if ch.isalnum() else "_" for ch in str(text).strip())
    return "_".join(part for part in safe.split("_") if part) or "student"

def current_work_rows(mode, rec):
    """Collect exactly what the student entered for the selected investigation."""
    if mode == "Percent Change":
        labels = rec["labels"]
        values = [float(x) for x in rec["values"]]
        idx = selected_indices(len(values))
        labels = [labels[i] for i in idx]
        values = [values[i] for i in idx]

        rows = [["Comparison", "Old", "New", "Student Change", "Student %", "Direction"]]
        for i in range(1, len(values)):
            rows.append([
                f"{labels[i-1]} to {labels[i]}",
                fmt(values[i-1]),
                fmt(values[i]),
                str(st.session_state.get(f"pc_change_{i}", "")),
                str(st.session_state.get(f"pc_pct_{i}", "")),
                str(st.session_state.get(f"pc_direction_{i}", "")),
            ])
        return rows

    if mode == "MAD Consistency":
        labels = rec["labels"]
        values = [float(x) for x in rec["values"]]
        rows = [["Period", "Value", "Student Deviation", "Student Absolute Deviation"]]
        for i, (label, value) in enumerate(zip(labels, values)):
            rows.append([
                str(label),
                fmt(value),
                str(st.session_state.get(f"mad_dev_{i}", "")),
                str(st.session_state.get(f"mad_abs_{i}", "")),
            ])
        return rows

    # Frequency
    values = [float(x) for x in rec["values"]]
    bins = make_bins(values)
    rows = [["Range", "Student Frequency", "Student Relative Frequency %"]]
    for label, low, high in bins:
        rows.append([
            str(label),
            str(st.session_state.get(f"freq_{label}", "")),
            str(st.session_state.get(f"freq_rel_{label}", "")),
        ])
    return rows

def summary_lines(mode):
    if mode == "Percent Change":
        return [
            ["Check", "Student Entry"],
            ["Percent-change check attempts", str(st.session_state.get("pc_check_attempts", 0))],
        ]
    if mode == "MAD Consistency":
        return [
            ["MAD Step", "Student Entry"],
            ["Mean", str(st.session_state.get("mad_mean", ""))],
            ["Sum of absolute deviations", str(st.session_state.get("mad_abs_sum", ""))],
            ["Final MAD", str(st.session_state.get("mad_final", ""))],
        ]
    return []

def build_submission_pdf(student_name, class_period, sport, athlete, mode, rec, question):
    """Generate a self-contained student submission receipt as a PDF in memory."""
    if "completion_id" not in st.session_state:
        st.session_state.completion_id = uuid.uuid4().hex[:8].upper()

    completion_id = st.session_state.completion_id
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.55*inch,
        leftMargin=0.55*inch,
        topMargin=0.55*inch,
        bottomMargin=0.55*inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=19,
        leading=22,
        spaceAfter=8,
        textColor=colors.HexColor("#0F2747"),
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        spaceBefore=8,
        spaceAfter=5,
        textColor=colors.HexColor("#173F73"),
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1F2937"),
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4B5563"),
    )

    story = []
    story.append(Paragraph("Sports by the Numbers - Investigation Report", title_style))
    story.append(Paragraph(
        f"<b>Completion ID:</b> {completion_id} &nbsp;&nbsp;&nbsp; "
        f"<b>Generated:</b> {generated}",
        small
    ))
    story.append(Spacer(1, 8))

    info_data = [
        ["Student", student_name, "Class Period", class_period],
        ["Sport", sport, "Athlete", athlete],
        ["Investigation", mode, "Stat Focus", rec.get("stat_label", "")],
    ]
    info = Table(info_data, colWidths=[0.85*inch, 2.25*inch, 0.95*inch, 2.35*inch])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(info)

    story.append(Paragraph("Investigation Question", heading))
    story.append(Paragraph(str(question), body))

    story.append(Paragraph("Source Data", heading))
    source_rows = [["Period", rec.get("stat_label","")]]
    for label, value in zip(rec.get("labels", []), rec.get("values", [])):
        source_rows.append([str(label), str(value)])
    source_table = Table(source_rows, repeatRows=1, colWidths=[2.4*inch, 2.4*inch])
    source_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DCEBFA")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#0F2747")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.45, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(source_table)

    story.append(Paragraph("Student Work", heading))
    work_rows = current_work_rows(mode, rec)
    col_count = len(work_rows[0])
    widths = [6.8*inch/col_count] * col_count
    work_table = Table(work_rows, repeatRows=1, colWidths=widths)
    work_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8EEF7")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0,0), (-1,-1), 7.5),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
    ]))
    story.append(work_table)

    extra = summary_lines(mode)
    if extra:
        story.append(Spacer(1, 6))
        extra_table = Table(extra, colWidths=[2.4*inch, 2.4*inch])
        extra_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F3F4F6")),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D1D5DB")),
            ("FONTSIZE", (0,0), (-1,-1), 8),
        ]))
        story.append(extra_table)

    story.append(Paragraph("Student Interpretation", heading))
    story.append(Paragraph(
        st.session_state.get("observation", "") or "(No observation entered.)",
        body
    ))

    story.append(Paragraph("Original Claim", heading))
    story.append(Paragraph(
        st.session_state.get("claim", "") or "(No original claim entered.)",
        body
    ))

    story.append(Paragraph("Built-In Coach Responses", heading))
    coach_answers = st.session_state.get("coach_answers", [])
    if coach_answers:
        coach_data = [["Coach Check", "Student Response"]]
        for i, answer in enumerate(coach_answers, start=1):
            coach_data.append([f"Check {i}", str(answer)])
        coach_table = Table(coach_data, colWidths=[1.3*inch, 4.8*inch], repeatRows=1)
        coach_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8EEF7")),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
            ("FONTSIZE", (0,0), (-1,-1), 8.5),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(coach_table)
    else:
        story.append(Paragraph("(No Coach responses recorded.)", body))

    story.append(Paragraph("Final Revised Claim", heading))
    story.append(Paragraph(
        st.session_state.get("revised", "") or "(No revised claim entered.)",
        body
    ))

    score = st.session_state.get("score_result", {})
    story.append(Paragraph("Argument Score", heading))
    score_data = [
        ["Category", "Score"],
        ["Clear Claim", f'{score.get("claim","")}/25'],
        ["Evidence", f'{score.get("evidence","")}/25'],
        ["Reasoning", f'{score.get("reasoning","")}/25'],
        ["Strength & Fairness", f'{score.get("fairness","")}/25'],
        ["TOTAL", f'{score.get("total","")}/100'],
    ]
    score_table = Table(score_data, colWidths=[3.3*inch, 1.4*inch])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#173F73")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#E8F3E8")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ALIGN", (1,1), (1,-1), "CENTER"),
    ]))
    story.append(score_table)

    story.append(Paragraph("Classroom Data Source", heading))
    story.append(Paragraph(
        f'{rec.get("source","")} - {rec.get("note","")}',
        small
    ))
    if rec.get("source_url"):
        story.append(Paragraph(str(rec["source_url"]), small))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "This report records the student's entries from the Sports by the Numbers app. "
        "The argument score evaluates features of the written argument, not whether the student's sports opinion matches an outside answer.",
        small
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

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

        student_change_raw = a.text_input(
            "Change",
            key=f"pc_change_{i}",
            placeholder="Type your answer",
            help="Answers within 0.5 of the exact change are accepted."
        )
        student_change = parse_student_number(student_change_raw)

        student_pct_raw = b.text_input(
            "Percent change",
            key=f"pc_pct_{i}",
            placeholder="Type your answer",
            help="You may round. Answers within 0.5 percentage points are accepted."
        )
        student_pct = parse_student_number(student_pct_raw)

        direction = st.radio(
            "Was this an increase or decrease?",
            ["Increase", "Decrease", "No Change"],
            key=f"pc_direction_{i}",
            horizontal=True
        )

        true_direction = "Increase" if true_change > 0 else "Decrease" if true_change < 0 else "No Change"

        change_ok = student_change is not None and math.isclose(student_change, true_change, abs_tol=0.5)
        pct_ok = student_pct is not None and math.isclose(student_pct, true_pct, abs_tol=0.5)
        direction_ok = direction == true_direction

        results.append({
            "i": i,
            "old": old,
            "new": new,
            "true_change": true_change,
            "true_pct": true_pct,
            "student_change": student_change,
            "student_pct": student_pct,
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

                        if entered_change is None:
                            st.write("**Enter a numerical change first.** Use New − Old.")
                        # Sign error
                        elif math.isclose(entered_change, -expected_change, abs_tol=0.5):
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

                        if entered_pct is None:
                            st.write("**Enter a numerical percent change first.**")
                            continue

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

    student_mean_raw = st.text_input(
        "Your mean",
        key="mad_mean",
        placeholder="Type your answer",
        help="Your answer can be within 0.5 of the exact answer."
    )
    student_mean = parse_student_number(student_mean_raw)

    if st.button("Check My Mean", use_container_width=True):
        if student_mean is not None and math.isclose(student_mean, true_mean, abs_tol=0.5):
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

        student_dev_raw = c3.text_input(
            "Deviation",
            key=f"mad_dev_{i}",
            label_visibility="collapsed",
            placeholder="Type answer",
            help="Value − Mean. Answers within 0.5 are accepted."
        )
        student_dev = parse_student_number(student_dev_raw)

        student_abs_raw = c4.text_input(
            "Absolute deviation",
            key=f"mad_abs_{i}",
            label_visibility="collapsed",
            placeholder="Type answer",
            help="Make the deviation positive. Answers within 0.5 are accepted."
        )
        student_abs = parse_student_number(student_abs_raw)

        dev_ok = student_dev is not None and math.isclose(student_dev, true_dev, abs_tol=0.5)
        abs_ok = student_abs is not None and math.isclose(student_abs, true_abs, abs_tol=0.5)
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

    student_abs_sum_raw = st.text_input(
        "Sum of the absolute deviations",
        key="mad_abs_sum",
        placeholder="Type your answer",
        help="Add every number from the Absolute Deviation column. Answers within 0.5 are accepted."
    )
    student_abs_sum = parse_student_number(student_abs_sum_raw)

    if st.button("Check My Absolute-Deviation Total", use_container_width=True):
        if student_abs_sum is not None and math.isclose(student_abs_sum, true_abs_sum, abs_tol=0.5):
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

    student_mad_raw = st.text_input(
        "Your MAD",
        key="mad_final",
        placeholder="Type your answer",
        help="Your final MAD can be within 0.5 of the exact answer."
    )
    student_mad = parse_student_number(student_mad_raw)

    if st.button("Check My MAD", use_container_width=True):
        if student_mad is not None and math.isclose(student_mad, true_mad, abs_tol=0.5):
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
        f_raw = c2.text_input(
            "Frequency",
            key=f"freq_{label}",
            label_visibility="collapsed",
            placeholder="Type answer"
        )
        r_raw = c3.text_input(
            "Relative frequency %",
            key=f"freq_rel_{label}",
            label_visibility="collapsed",
            placeholder="Type answer"
        )
        f = parse_student_number(f_raw)
        r = parse_student_number(r_raw)
        if f is None or r is None or int(round(f)) != count or not math.isclose(r, expected, abs_tol=.2):
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
<p>Sports investigations and standards-based 7th-grade math through real athletic data.</p>
</div>
<div class="progress-ribbon">
    <div class="progress-chip"><strong>1</strong> Data</div>
    <div class="progress-chip"><strong>2</strong> Calculate</div>
    <div class="progress-chip"><strong>3</strong> Graph</div>
    <div class="progress-chip"><strong>4</strong> Claim</div>
    <div class="progress-chip"><strong>5</strong> Coach</div>
</div>
""", unsafe_allow_html=True)



if "app_branch" not in st.session_state:
    st.session_state.app_branch = "Sports Data Investigations"

st.markdown("### Choose a learning path")
branch = st.radio(
    "Choose a learning path",
    ["Sports Data Investigations", "7th Grade Math Lab", "Sports Math Challenge", "Teacher Assignment Builder"],
    key="app_branch",
    horizontal=True,
    label_visibility="collapsed"
)

if branch == "Teacher Assignment Builder":
    st.markdown("""
    <div class="card">
      <div class="step">Teacher Assignment Builder</div>
      <h2>Create a class-specific assignment</h2>
      <p>Your choices are stored only inside the assignment code, so one teacher never changes another teacher's settings.</p>
    </div>
    """, unsafe_allow_html=True)

    assignment_type = st.selectbox(
        "Assignment type",
        ["Ratios, Rates & Proportions", "Equations & Inequalities", "Sports Math Challenge"],
        key="teacher_topic"
    )
    count = st.selectbox("Activities required", [1,2,3], key="teacher_count")
    sport_limit = st.selectbox("Allowed sport", ["Any Sport"] + list(RATE_CASES), key="teacher_sport")

    if assignment_type in ["Ratios, Rates & Proportions", "Equations & Inequalities"]:
        difficulty = st.selectbox("Difficulty", ["Guided","Independent"], key="teacher_difficulty")
        challenge_level = "Any Level"
    else:
        difficulty = "Independent"
        challenge_level = st.selectbox(
            "Challenge level",
            ["Any Level", "Level 1 · Connect Two Skills", "Level 2 · Multi-Step Investigation", "Level 3 · Open Challenge"],
            key="teacher_challenge_level"
        )

    require_pdf = st.checkbox("Require PDF submission report", value=True, key="teacher_pdf")

    assignment_code = encode_assignment({
        "v":1,
        "topic":assignment_type,
        "count":count,
        "sport":sport_limit,
        "difficulty":difficulty,
        "challenge_level":challenge_level,
        "pdf":require_pdf
    })
    st.markdown("### Assignment Code")
    st.code(assignment_code, language=None)
    st.caption("Post this code in Google Classroom. Students open the matching branch and paste it there. No database or teacher account is needed.")
    st.stop()

if branch == "Sports Math Challenge":
    st.markdown("""
    <div class="card">
      <div class="step">Sports Math Challenge</div>
      <h2>One problem. Several math ideas.</h2>
      <p>Decide what math matters, solve the problem in pieces, and explain why your answer makes sense.</p>
    </div>
    """, unsafe_allow_html=True)

    challenge_entry = st.radio(
        "How are you entering?",
        ["Free Explore", "I Have an Assignment Code"],
        horizontal=True,
        key="challenge_entry"
    )

    challenge_config = {
        "topic":"Sports Math Challenge",
        "count":1,
        "sport":"Any Sport",
        "challenge_level":"Any Level"
    }

    if challenge_entry == "I Have an Assignment Code":
        challenge_code_in = st.text_input(
            "Assignment Code",
            key="challenge_assignment_code",
            placeholder="Paste code from your teacher"
        )
        if challenge_code_in.strip():
            decoded = decode_assignment(challenge_code_in)
            if decoded:
                if decoded.get("topic") != "Sports Math Challenge":
                    st.warning("That code is for a different branch of the app.")
                else:
                    challenge_config.update(decoded)
                    st.success(
                        f"Loaded: {challenge_config.get('challenge_level','Any Level')} · "
                        f"{challenge_config.get('sport','Any Sport')}"
                    )
            else:
                st.error("That assignment code could not be read.")

    st.markdown("""
    <div class="card">
      <div class="step">Student Information</div>
      <p><b>Enter this before beginning.</b></p>
    </div>
    """, unsafe_allow_html=True)
    cx, cy = st.columns([2,1])
    with cx:
        st.text_input("Student Name", key="challenge_student_name", placeholder="First and last name")
    with cy:
        st.text_input("Class Period", key="challenge_class_period", placeholder="Example: 4E")

    challenge_lab_engine(
        level_filter=challenge_config.get("challenge_level","Any Level"),
        sport_filter=challenge_config.get("sport","Any Sport")
    )
    st.markdown("---")
    st.caption("Sports Math Challenge · multi-skill reasoning · 8 starter investigations")
    st.stop()

if branch == "7th Grade Math Lab":
    st.markdown("""
    <div class="card">
      <div class="step">7th Grade Math Lab</div>
      <h2>Real sports. Real 7th-grade math.</h2>
      <p>Practice one skill at a time using sports situations, guided checking, and hints that appear only when needed.</p>
    </div>
    """, unsafe_allow_html=True)

    entry = st.radio(
        "How are you entering?",
        ["Free Explore","I Have an Assignment Code"],
        horizontal=True,
        key="math_entry"
    )

    config = {
        "topic":"Ratios, Rates & Proportions",
        "count":1,
        "sport":"Any Sport",
        "difficulty":"Guided",
        "pdf":False
    }

    assignment_loaded = False

    if entry == "I Have an Assignment Code":
        code_in = st.text_input(
            "Assignment Code",
            key="student_assignment_code",
            placeholder="Paste code from your teacher"
        )
        if code_in.strip():
            decoded = decode_assignment(code_in)
            if decoded:
                if decoded.get("topic") == "Sports Math Challenge":
                    st.warning("That code belongs in the Sports Math Challenge branch.")
                else:
                    config.update(decoded)
                    assignment_loaded = True
                    st.success(
                        f"Loaded: {config['topic']} · {config['count']} activity(ies) · "
                        f"{config['sport']} · {config['difficulty']}"
                    )
            else:
                st.error("That assignment code could not be read.")

    if entry == "Free Explore":
        config["topic"] = st.selectbox(
            "Math topic",
            ["Ratios, Rates & Proportions", "Equations & Inequalities"],
            key="math_topic_select"
        )
        config["sport"] = st.selectbox(
            "Sport filter",
            ["Any Sport"] + list(RATE_CASES),
            key="math_sport_filter"
        )
        config["difficulty"] = st.selectbox(
            "Support level",
            ["Guided", "Independent"],
            key="math_difficulty_select"
        )

    st.markdown("""
    <div class="card">
      <div class="step">Student Information</div>
      <p><b>Enter this before beginning.</b></p>
    </div>
    """, unsafe_allow_html=True)

    x,y = st.columns([2,1])
    with x:
        st.text_input("Student Name", key="math_student_name", placeholder="First and last name")
    with y:
        st.text_input("Class Period", key="math_class_period", placeholder="Example: 4E")

    if config.get("topic") == "Equations & Inequalities":
        equations_inequalities_engine(
            config.get("sport","Any Sport"),
            config.get("difficulty","Guided")
        )
    else:
        ratios_rates_engine(
            config.get("sport","Any Sport"),
            config.get("difficulty","Guided")
        )

    st.markdown("---")
    st.caption("7th Grade Math Lab · Ratios, Rates & Proportions · Equations & Inequalities")
    st.stop()

st.markdown("""
<div class="card">
<div class="step">Student Information</div>
<p style="margin:.1rem 0 .65rem;"><b>Enter this before beginning.</b> It will appear on your final submission report.</p>
</div>
""", unsafe_allow_html=True)

student_col1, student_col2 = st.columns([2,1])
with student_col1:
    student_name = st.text_input(
        "Student Name",
        key="student_name",
        placeholder="First and last name"
    )
with student_col2:
    class_period = st.text_input(
        "Class Period",
        key="class_period",
        placeholder="Example: 4E"
    )

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
<div class="step">{SPORT_ICONS[sport]} {sport} · {MODE_ICONS[mode]} {mode}</div>
<h2 style="margin-bottom:.35rem;">{athlete}</h2>
<p style="margin:.15rem 0;"><b>Stat focus:</b> {rec["stat_label"]}</p>
<p style="margin:.15rem 0;color:#a8b3c7;"><b>Classroom mode:</b> Curated frozen dataset</p>
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
    st.markdown('<div class="step">Final Submission</div>', unsafe_allow_html=True)

    student_ready = bool(st.session_state.get("student_name", "").strip())
    period_ready = bool(st.session_state.get("class_period", "").strip())
    revised_ready = bool(st.session_state.get("revised", "").strip())
    coach_ready = len(st.session_state.get("coach_answers", [])) >= 4

    if student_ready and period_ready and revised_ready and coach_ready:
        if "completion_id" not in st.session_state:
            st.session_state.completion_id = uuid.uuid4().hex[:8].upper()

        completion_id = st.session_state.completion_id
        st.success(f"✅ Investigation Complete · Completion ID: **{completion_id}**")
        st.write(
            "Download your Investigation Report and submit the PDF to your teacher "
            "through Google Classroom or the class submission method."
        )

        pdf_bytes = build_submission_pdf(
            st.session_state.get("student_name", "").strip(),
            st.session_state.get("class_period", "").strip(),
            sport,
            athlete,
            mode,
            rec,
            question,
        )

        pdf_filename = (
            f"Sports_by_the_Numbers_"
            f"{clean_filename(st.session_state.get('student_name',''))}_"
            f"{clean_filename(athlete)}_"
            f"{completion_id}.pdf"
        )

        st.download_button(
            "📄 Download My Investigation Report",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width=True,
        )

        st.caption(
            "Your report includes your data, calculations, interpretation, original claim, "
            "Coach responses, revised claim, score, and completion ID."
        )
    else:
        missing = []
        if not student_ready:
            missing.append("student name")
        if not period_ready:
            missing.append("class period")
        if not coach_ready:
            missing.append("all 4 Coach checks")
        if not revised_ready:
            missing.append("revised claim")
        st.info("Complete these before the report unlocks: " + ", ".join(missing) + ".")

st.markdown("---")
st.caption("Sports by the Numbers · Curated classroom edition · 50 athletes · 150 investigations · PDF submission receipt")
