
import streamlit as st
import json
import math
import random
import copy
import html
from fractions import Fraction
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
        "Mahomes · Passing Yards per Game": {
            "unit": "passing yards per game", "total_label": "passing yards",
            "total": 4839, "games": 17, "projection_games": 12,
            "story": "Patrick Mahomes threw for 4,839 yards over 17 games.",
            "task_type": "unit_rate"
        },
        "Jefferson · Receiving Yards per Game": {
            "unit": "receiving yards per game", "total_label": "receiving yards",
            "total": 1616, "games": 17, "projection_games": 10,
            "story": "Justin Jefferson recorded 1,616 receiving yards over 17 games.",
            "task_type": "unit_rate"
        },
        "Allen · Touchdowns per Game": {
            "unit": "touchdowns per game", "total_label": "touchdowns",
            "total": 42, "games": 17, "projection_games": 12,
            "story": "Josh Allen recorded 42 total touchdowns over 17 games.",
            "task_type": "unit_rate"
        },
        "Henry · Yards per Carry": {
            "unit": "yards per carry", "total_label": "rushing yards",
            "total": 1538, "games": 280, "projection_games": 325,
            "story": "Derrick Henry gained 1,538 rushing yards on 280 carries.",
            "task_type": "unit_rate",
            "denominator_label": "carries",
            "projection_label": "carries"
        },
        "Receiver Catch Rate": {
            "unit": "catches per target", "total_label": "catches",
            "total": 84, "games": 126, "projection_games": 150,
            "story": "A receiver caught 84 passes on 126 targets.",
            "task_type": "unit_rate",
            "denominator_label": "targets",
            "projection_label": "targets"
        },
        "Field Goal Pace": {
            "unit": "made field goals per attempt", "total_label": "made field goals",
            "total": 27, "games": 30, "projection_games": 40,
            "story": "A kicker made 27 field goals in 30 attempts.",
            "task_type": "unit_rate",
            "denominator_label": "attempts",
            "projection_label": "attempts"
        },
    },
    "NBA": {
        "Curry · Threes per Game": {
            "unit": "made 3-pointers per game", "total_label": "made 3-pointers",
            "total": 337, "games": 63, "projection_games": 70,
            "story": "Stephen Curry made 337 three-pointers over 63 games.",
            "task_type": "unit_rate"
        },
        "Jordan · Points per Game": {
            "unit": "points per game", "total_label": "points",
            "total": 3041, "games": 82, "projection_games": 60,
            "story": "Michael Jordan scored 3,041 points over 82 games in 1986-87.",
            "task_type": "unit_rate"
        },
        "LeBron · Assists per Game": {
            "unit": "assists per game", "total_label": "assists",
            "total": 518, "games": 71, "projection_games": 65,
            "story": "LeBron James recorded 518 assists over 71 games.",
            "task_type": "unit_rate"
        },
        "Free Throw Rate": {
            "unit": "made free throws per attempt", "total_label": "made free throws",
            "total": 72, "games": 90, "projection_games": 120,
            "story": "A player made 72 free throws in 90 attempts.",
            "task_type": "unit_rate",
            "denominator_label": "attempts",
            "projection_label": "attempts"
        },
        "Rebounds per Minute": {
            "unit": "rebounds per minute", "total_label": "rebounds",
            "total": 14, "games": 28, "projection_games": 36,
            "story": "A player grabbed 14 rebounds in 28 minutes.",
            "task_type": "unit_rate",
            "denominator_label": "minutes",
            "projection_label": "minutes"
        },
        "Team Scoring Pace": {
            "unit": "points per quarter", "total_label": "points",
            "total": 84, "games": 3, "projection_games": 4,
            "story": "A team scored 84 points through 3 quarters.",
            "task_type": "unit_rate",
            "denominator_label": "quarters",
            "projection_label": "quarters"
        },
    },
    "MLB": {
        "Judge · Home Runs per Game": {
            "unit": "home runs per game", "total_label": "home runs",
            "total": 62, "games": 157, "projection_games": 100,
            "story": "Aaron Judge hit 62 home runs over 157 games in 2022.",
            "task_type": "unit_rate"
        },
        "Ohtani · Home Runs per Game": {
            "unit": "home runs per game", "total_label": "home runs",
            "total": 54, "games": 159, "projection_games": 120,
            "story": "Shohei Ohtani hit 54 home runs over 159 games.",
            "task_type": "unit_rate"
        },
        "Hits per At-Bat": {
            "unit": "hits per at-bat", "total_label": "hits",
            "total": 45, "games": 150, "projection_games": 200,
            "story": "A hitter recorded 45 hits in 150 at-bats.",
            "task_type": "unit_rate",
            "denominator_label": "at-bats",
            "projection_label": "at-bats"
        },
        "Strikeouts per Inning": {
            "unit": "strikeouts per inning", "total_label": "strikeouts",
            "total": 72, "games": 60, "projection_games": 90,
            "story": "A pitcher recorded 72 strikeouts in 60 innings.",
            "task_type": "unit_rate",
            "denominator_label": "innings",
            "projection_label": "innings"
        },
        "Runs per Inning": {
            "unit": "runs per inning", "total_label": "runs",
            "total": 18, "games": 6, "projection_games": 9,
            "story": "A team scored 18 runs over 6 innings in a classroom simulation.",
            "task_type": "unit_rate",
            "denominator_label": "innings",
            "projection_label": "innings"
        },
        "Stolen Base Pace": {
            "unit": "stolen bases per game", "total_label": "stolen bases",
            "total": 24, "games": 40, "projection_games": 75,
            "story": "A player stole 24 bases over 40 games.",
            "task_type": "unit_rate"
        },
    },
    "NHL": {
        "McDavid · Points per Game": {
            "unit": "points per game", "total_label": "points",
            "total": 153, "games": 82, "projection_games": 60,
            "story": "Connor McDavid recorded 153 points over 82 games.",
            "task_type": "unit_rate"
        },
        "Matthews · Goals per Game": {
            "unit": "goals per game", "total_label": "goals",
            "total": 69, "games": 81, "projection_games": 60,
            "story": "Auston Matthews scored 69 goals over 81 games.",
            "task_type": "unit_rate"
        },
        "Shots per Game": {
            "unit": "shots per game", "total_label": "shots",
            "total": 96, "games": 24, "projection_games": 35,
            "story": "A player recorded 96 shots over 24 games.",
            "task_type": "unit_rate"
        },
        "Saves per Shot": {
            "unit": "saves per shot", "total_label": "saves",
            "total": 45, "games": 50, "projection_games": 80,
            "story": "A goalie made 45 saves on 50 shots.",
            "task_type": "unit_rate",
            "denominator_label": "shots",
            "projection_label": "shots"
        },
        "Penalty Minutes per Game": {
            "unit": "penalty minutes per game", "total_label": "penalty minutes",
            "total": 36, "games": 18, "projection_games": 30,
            "story": "A player accumulated 36 penalty minutes over 18 games.",
            "task_type": "unit_rate"
        },
        "Power-Play Goals per Chance": {
            "unit": "goals per power-play chance", "total_label": "power-play goals",
            "total": 12, "games": 48, "projection_games": 80,
            "story": "A team scored 12 power-play goals in 48 chances.",
            "task_type": "unit_rate",
            "denominator_label": "power-play chances",
            "projection_label": "power-play chances"
        },
    },
    "Soccer": {
        "Messi · Goals per Match": {
            "unit": "goals per match", "total_label": "goals",
            "total": 43, "games": 38, "projection_games": 30,
            "story": "Lionel Messi scored 43 league goals over 38 matches in 2014-15.",
            "task_type": "unit_rate"
        },
        "Haaland · Goals per Match": {
            "unit": "goals per match", "total_label": "goals",
            "total": 36, "games": 35, "projection_games": 30,
            "story": "Erling Haaland scored 36 league goals over 35 matches in 2022-23.",
            "task_type": "unit_rate"
        },
        "Passes per Minute": {
            "unit": "completed passes per minute", "total_label": "completed passes",
            "total": 54, "games": 90, "projection_games": 60,
            "story": "A midfielder completed 54 passes in 90 minutes.",
            "task_type": "unit_rate",
            "denominator_label": "minutes",
            "projection_label": "minutes"
        },
        "Shots per Match": {
            "unit": "shots per match", "total_label": "shots",
            "total": 28, "games": 7, "projection_games": 12,
            "story": "A forward took 28 shots over 7 matches.",
            "task_type": "unit_rate"
        },
        "Penalty Conversion Rate": {
            "unit": "goals per penalty attempt", "total_label": "penalty goals",
            "total": 8, "games": 10, "projection_games": 15,
            "story": "A player scored on 8 of 10 penalty attempts.",
            "task_type": "unit_rate",
            "denominator_label": "penalty attempts",
            "projection_label": "penalty attempts"
        },
        "Team Points per Match": {
            "unit": "table points per match", "total_label": "table points",
            "total": 21, "games": 9, "projection_games": 15,
            "story": "A club earned 21 table points over 9 matches.",
            "task_type": "unit_rate"
        },
    },
    "Formula 1": {
        "Verstappen · Points per Race": {
            "unit": "championship points per race", "total_label": "championship points",
            "total": 575, "games": 22, "projection_games": 20,
            "story": "Max Verstappen scored 575 championship points over 22 races in 2023.",
            "task_type": "unit_rate"
        },
        "Hamilton · Points per Race": {
            "unit": "championship points per race", "total_label": "championship points",
            "total": 413, "games": 21, "projection_games": 18,
            "story": "Lewis Hamilton scored 413 championship points over 21 races in 2019.",
            "task_type": "unit_rate"
        },
        "Laps per Minute": {
            "unit": "laps per minute", "total_label": "laps",
            "total": 18, "games": 27, "projection_games": 45,
            "story": "A driver completed 18 laps in 27 minutes during a practice simulation.",
            "task_type": "unit_rate",
            "denominator_label": "minutes",
            "projection_label": "minutes"
        },
        "Pit Stops per Race": {
            "unit": "pit stops per race", "total_label": "pit stops",
            "total": 12, "games": 6, "projection_games": 10,
            "story": "A team made 12 pit stops over 6 races.",
            "task_type": "unit_rate"
        },
        "Fuel per Lap": {
            "unit": "liters per lap", "total_label": "liters of fuel",
            "total": 90, "games": 50, "projection_games": 70,
            "story": "A race simulation used 90 liters of fuel over 50 laps.",
            "task_type": "unit_rate",
            "denominator_label": "laps",
            "projection_label": "laps"
        },
        "Points per Sprint": {
            "unit": "points per sprint", "total_label": "points",
            "total": 24, "games": 4, "projection_games": 7,
            "story": "A driver earned 24 sprint points over 4 sprint events.",
            "task_type": "unit_rate",
            "denominator_label": "sprints",
            "projection_label": "sprints"
        },
    },
}

def rate_tolerance(correct):
    return max(0.1, abs(correct) * 0.015)

def ratios_rates_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_athlete=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Ratios, Rates & Proportions</div>', unsafe_allow_html=True)
    st.subheader("🏁 Sports Rate Lab")
    st.write(
        "Use the sports situation to decide what math you need. "
        "Try each step first — the app gives stronger help only after repeated mistakes."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        athlete = generated_athlete or generated_case.get("title", "Generated Scenario")
    elif generated_sport and generated_athlete:
        sport = generated_sport
        athlete = generated_athlete
    else:
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
                "Scenario",
                list(RATE_CASES[sport]),
                key="rate_athlete"
            )

    case = generated_case if generated_case is not None else RATE_CASES[sport][athlete]
    total = float(case["total"])
    games = float(case["games"])
    target_games = float(case["projection_games"])
    denominator_label = case.get("denominator_label", "games")
    projection_label = case.get("projection_label", denominator_label)
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
        f"Write a ratio that compares **{case['total_label']}** to **{denominator_label}**."
    )
    ratio_raw = st.text_input(
        "Your ratio",
        key="rate_ratio",
        placeholder="Type your ratio"
    )

    if "ratio_attempts" not in st.session_state:
        st.session_state.ratio_attempts = 0

    def ratio_is_correct(text):
        """Accept equivalent ratios in simplified or unsimplified form."""
        compact = str(text).lower().strip().replace(" ", "").replace(",", "")
        if not compact:
            return False

        # Remove a few optional words students may type.
        for word in [
            "games", "game", "matches", "match", "races", "race",
            "attempts", "attempt", "carries", "carry", "targets", "target",
            "minutes", "minute", "innings", "inning", "laps", "lap",
            "quarters", "quarter", "shots", "shot", "sprints", "sprint",
            "power-playchances", "power-playchance",
            "penaltyattempts", "penaltyattempt"
        ]:
            compact = compact.replace(word, "")

        # Normalize common ratio separators.
        compact = compact.replace("÷", "/").replace(":", "/")

        # Accept a fraction/ratio such as 90/50, 9/5, 18/10, etc.
        if "/" in compact:
            parts = compact.split("/")
            if len(parts) != 2:
                return False
            try:
                student_num = Fraction(parts[0])
                student_den = Fraction(parts[1])
                if student_den == 0:
                    return False
                student_ratio = student_num / student_den
                true_ratio = Fraction(str(total)) / Fraction(str(games))
                return student_ratio == true_ratio
            except (ValueError, ZeroDivisionError):
                return False

        # Also accept a decimal equivalent if a student chooses to enter one.
        try:
            student_value = float(compact)
            true_value = total / games
            return math.isclose(student_value, true_value, rel_tol=1e-9, abs_tol=1e-9)
        except ValueError:
            return False

    if st.button("Check My Ratio", use_container_width=True):
        if ratio_is_correct(ratio_raw):
            st.success("✅ Yes. You compared the total statistic to the number of games.")
            st.session_state.ratio_attempts = 0
        else:
            st.session_state.ratio_attempts += 1
            if st.session_state.ratio_attempts == 1:
                st.info(
                    f"Look back at the situation. Which number is the **{case['total_label']}** total, "
                    f"and which number is the number of **{denominator_label}**?"
                )
            else:
                st.warning(
                    f"Use the total first and the comparison amount second: "
                    f"**{fmt(total)} to {fmt(games)}**. "
                    "You may write the original ratio or any equivalent simplified ratio "
                    "using a colon, fraction bar, or division sign."
                )

    # -----------------------------
    # STEP 2 — Unit rate; no formula shown first
    # -----------------------------
    st.markdown("### Step 2 · Find the unit rate")
    st.write(
        f"What is the **{case['unit']}**?"
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
                    f"A unit rate tells the amount for **1 {denominator_label.rstrip('s')}**. "
                    "Think about which operation turns the denominator into 1."
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
        f"If the same rate continued for **{fmt(target_games)} {projection_label}**, "
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
                    f"How can you use that rate with **{fmt(target_games)} {projection_label}**?"
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
            "title": "Field Goal Scoring",
            "kind": "Equation",
            "story": "A kicker scores x total points using only field goals. Each field goal is worth 3 points, and the kicker scores 18 points.",
            "question": "How many field goals were made?",
            "models": ["3x = 18", "x + 3 = 18", "18x = 3", "x / 3 = 18"],
            "correct_model": "3x = 18",
            "answer": 6,
            "unit": "field goals",
            "hint1": "Each made field goal contributes 3 points.",
            "hint2": "3x = 18, so divide 18 by 3.",
            "meaning": "The kicker made 6 field goals."
        },
        {
            "title": "Fourth-Quarter Comeback",
            "kind": "Equation",
            "story": "A team has 17 points. Each remaining touchdown with the extra point adds 7 points. The team wants exactly 31 points.",
            "question": "How many touchdowns are needed?",
            "models": ["17 + 7x = 31", "17 + x = 31", "7x = 31", "31 + 7x = 17"],
            "correct_model": "17 + 7x = 31",
            "answer": 2,
            "unit": "touchdowns",
            "hint1": "The team starts at 17, and each scoring event adds 7.",
            "hint2": "17 + 7x = 31 → subtract 17, then divide by 7.",
            "meaning": "The team needs 2 touchdowns."
        },
        {
            "title": "Sack Yardage Loss",
            "kind": "Equation",
            "story": "An offense had 46 net passing yards on a drive before losing x yards on a sack. It finished with 38 net passing yards.",
            "question": "How many yards were lost on the sack?",
            "models": ["46 - x = 38", "46 + x = 38", "38 - x = 46", "46x = 38"],
            "correct_model": "46 - x = 38",
            "answer": 8,
            "unit": "yards",
            "hint1": "The sack decreases the original amount.",
            "hint2": "46 − x = 38, so x = 8.",
            "meaning": "The sack caused an 8-yard loss."
        },
        {
            "title": "Practice Repetition Limit",
            "kind": "Inequality",
            "story": "A quarterback has already thrown 32 practice passes. The coach wants no more than 50 total passes.",
            "question": "What is the greatest number of additional passes allowed?",
            "models": ["32 + x ≤ 50", "32 + x ≥ 50", "32x ≤ 50", "50 + x ≤ 32"],
            "correct_model": "32 + x ≤ 50",
            "answer": 18,
            "unit": "passes",
            "hint1": "'No more than 50' means 50 or less.",
            "hint2": "50 − 32 = 18.",
            "meaning": "The quarterback can throw at most 18 more passes."
        },
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
            "title": "Quarter Scoring Average",
            "kind": "Equation",
            "story": "A team scored x total points across 4 quarters and averaged 24 points per quarter.",
            "question": "How many total points did the team score?",
            "models": ["x / 4 = 24", "4x = 24", "x + 4 = 24", "24 / x = 4"],
            "correct_model": "x / 4 = 24",
            "answer": 96,
            "unit": "points",
            "hint1": "The total is being split equally across 4 quarters.",
            "hint2": "x ÷ 4 = 24, so multiply 24 by 4.",
            "meaning": "The team scored 96 total points."
        },
        {
            "title": "Comeback With Free Throws",
            "kind": "Equation",
            "story": "A team has 58 points. Each trip to the line adds 2 points. The team wants exactly 72 points.",
            "question": "How many 2-point trips to the free-throw line are needed?",
            "models": ["58 + 2x = 72", "58 + x = 72", "2x = 72", "72 + 2x = 58"],
            "correct_model": "58 + 2x = 72",
            "answer": 7,
            "unit": "trips",
            "hint1": "The team starts with 58 and gains 2 points each time.",
            "hint2": "58 + 2x = 72 → subtract 58, then divide by 2.",
            "meaning": "The team needs 7 two-point trips to reach 72."
        },
        {
            "title": "Turnovers Reduced",
            "kind": "Equation",
            "story": "A team had 19 turnovers in one game. After improving, it had 11. Let x be the number of turnovers reduced.",
            "question": "How many fewer turnovers did the team have?",
            "models": ["19 - x = 11", "19 + x = 11", "11 - x = 19", "19x = 11"],
            "correct_model": "19 - x = 11",
            "answer": 8,
            "unit": "turnovers",
            "hint1": "The starting amount becomes smaller by x.",
            "hint2": "19 − x = 11, so x = 8.",
            "meaning": "The team reduced its turnovers by 8."
        },
        {
            "title": "Minutes Limit",
            "kind": "Inequality",
            "story": "A player has already played 24 minutes. The coach wants the player to finish with no more than 34 minutes.",
            "question": "What is the greatest number of additional minutes the player can play?",
            "models": ["24 + x ≤ 34", "24 + x ≥ 34", "24x ≤ 34", "34 + x ≤ 24"],
            "correct_model": "24 + x ≤ 34",
            "answer": 10,
            "unit": "minutes",
            "hint1": "'No more than' means the final total must be 34 or less.",
            "hint2": "34 − 24 = 10, so x can be at most 10.",
            "meaning": "The player can play at most 10 more minutes."
        },
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
            "title": "Runs Per Inning",
            "kind": "Equation",
            "story": "A team scored x total runs evenly across 3 scoring innings, averaging 4 runs in each of those innings.",
            "question": "How many total runs were scored in those innings?",
            "models": ["x / 3 = 4", "3x = 4", "x + 3 = 4", "4 / x = 3"],
            "correct_model": "x / 3 = 4",
            "answer": 12,
            "unit": "runs",
            "hint1": "The total is split equally among 3 innings.",
            "hint2": "x ÷ 3 = 4, so x = 12.",
            "meaning": "The team scored 12 runs across those innings."
        },
        {
            "title": "Extra-Base Hit Points",
            "kind": "Equation",
            "story": "In a classroom scoring game, a player already has 14 points. Each double is worth 2 more points. The target is 24 points.",
            "question": "How many doubles are needed?",
            "models": ["14 + 2x = 24", "14 + x = 24", "2x = 24", "24 + 2x = 14"],
            "correct_model": "14 + 2x = 24",
            "answer": 5,
            "unit": "doubles",
            "hint1": "Start at 14, then add 2 for each double.",
            "hint2": "14 + 2x = 24 → subtract 14, then divide by 2.",
            "meaning": "The player needs 5 doubles."
        },
        {
            "title": "Pitch Count Drop",
            "kind": "Equation",
            "story": "A pitcher threw 92 pitches in one start and then threw x fewer pitches in the next start, finishing with 78.",
            "question": "How many fewer pitches were thrown?",
            "models": ["92 - x = 78", "92 + x = 78", "78 - x = 92", "92x = 78"],
            "correct_model": "92 - x = 78",
            "answer": 14,
            "unit": "pitches",
            "hint1": "The second total is lower than the first.",
            "hint2": "92 − x = 78, so x = 14.",
            "meaning": "The pitcher threw 14 fewer pitches."
        },
        {
            "title": "Concession Budget",
            "kind": "Inequality",
            "story": "A student has $35 at a baseball game and already spent $11. Each snack costs $6.",
            "question": "What is the greatest number of snacks the student can still buy?",
            "models": ["11 + 6x ≤ 35", "11 + 6x ≥ 35", "6 + 11x ≤ 35", "35 + 6x ≤ 11"],
            "correct_model": "11 + 6x ≤ 35",
            "answer": 4,
            "unit": "snacks",
            "hint1": "The total spending cannot exceed $35.",
            "hint2": "35 − 11 = 24, then 24 ÷ 6 = 4.",
            "meaning": "The student can buy at most 4 snacks."
        },
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
            "title": "Goals Per Period",
            "kind": "Equation",
            "story": "A team scored x total goals evenly across 3 periods at a rate of 2 goals per period.",
            "question": "How many total goals were scored?",
            "models": ["x / 3 = 2", "3x = 2", "x + 3 = 2", "2 / x = 3"],
            "correct_model": "x / 3 = 2",
            "answer": 6,
            "unit": "goals",
            "hint1": "The total is split across 3 equal periods.",
            "hint2": "x ÷ 3 = 2, so x = 6.",
            "meaning": "The team scored 6 total goals."
        },
        {
            "title": "Power-Play Comeback",
            "kind": "Equation",
            "story": "A team has 2 goals. Each successful power play adds 1 goal. The team wants to finish with exactly 5 goals.",
            "question": "How many successful power plays are needed?",
            "models": ["2 + x = 5", "2x = 5", "5 + x = 2", "2 - x = 5"],
            "correct_model": "2 + x = 5",
            "answer": 3,
            "unit": "power-play goals",
            "hint1": "What must be added to 2 to reach 5?",
            "hint2": "5 − 2 = 3.",
            "meaning": "The team needs 3 more power-play goals."
        },
        {
            "title": "Ice Time Reduced",
            "kind": "Equation",
            "story": "A player usually logs 24 minutes of ice time. In one game the coach reduces that by x minutes, leaving 18 minutes.",
            "question": "How many minutes were removed?",
            "models": ["24 - x = 18", "24 + x = 18", "18 - x = 24", "24x = 18"],
            "correct_model": "24 - x = 18",
            "answer": 6,
            "unit": "minutes",
            "hint1": "The amount starts at 24 and decreases.",
            "hint2": "24 − x = 18, so x = 6.",
            "meaning": "The player's ice time was reduced by 6 minutes."
        },
        {
            "title": "Equipment Budget",
            "kind": "Inequality",
            "story": "A team has $260 for practice pucks after already spending $80 on cones. Each puck pack costs $30.",
            "question": "What is the greatest number of puck packs the team can buy?",
            "models": ["80 + 30x ≤ 260", "80 + 30x ≥ 260", "30 + 80x ≤ 260", "260 + 30x ≤ 80"],
            "correct_model": "80 + 30x ≤ 260",
            "answer": 6,
            "unit": "puck packs",
            "hint1": "The total spending cannot be more than $260.",
            "hint2": "260 − 80 = 180, then 180 ÷ 30 = 6.",
            "meaning": "The team can buy at most 6 puck packs."
        },
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
            "title": "Goals Per Match",
            "kind": "Equation",
            "story": "A club scored x total goals across 5 matches at an average of 3 goals per match.",
            "question": "How many total goals were scored?",
            "models": ["x / 5 = 3", "5x = 3", "x + 5 = 3", "3 / x = 5"],
            "correct_model": "x / 5 = 3",
            "answer": 15,
            "unit": "goals",
            "hint1": "The total is split equally across 5 matches.",
            "hint2": "x ÷ 5 = 3, so x = 15.",
            "meaning": "The club scored 15 total goals."
        },
        {
            "title": "Penalty Kick Practice",
            "kind": "Equation",
            "story": "A player has already made 12 penalty kicks in practice. Each new round adds 3 made kicks. The target is 24.",
            "question": "How many new rounds are needed?",
            "models": ["12 + 3x = 24", "12 + x = 24", "3x = 24", "24 + 3x = 12"],
            "correct_model": "12 + 3x = 24",
            "answer": 4,
            "unit": "rounds",
            "hint1": "Start at 12 and add 3 for each new round.",
            "hint2": "12 + 3x = 24 → subtract 12, then divide by 3.",
            "meaning": "The player needs 4 more practice rounds."
        },
        {
            "title": "Possession Drop",
            "kind": "Equation",
            "story": "A team had 61% possession in one match and x percentage points less in the next match, finishing at 54%.",
            "question": "How many percentage points did possession decrease?",
            "models": ["61 - x = 54", "61 + x = 54", "54 - x = 61", "61x = 54"],
            "correct_model": "61 - x = 54",
            "answer": 7,
            "unit": "percentage points",
            "hint1": "The second value is lower than the first.",
            "hint2": "61 − x = 54, so x = 7.",
            "meaning": "Possession decreased by 7 percentage points."
        },
        {
            "title": "Practice Ball Budget",
            "kind": "Inequality",
            "story": "A team has $300 for equipment. It already spent $84 on cones. Each soccer ball costs $27.",
            "question": "What is the greatest number of soccer balls the team can buy?",
            "models": ["84 + 27x ≤ 300", "84 + 27x ≥ 300", "27 + 84x ≤ 300", "300 + 27x ≤ 84"],
            "correct_model": "84 + 27x ≤ 300",
            "answer": 8,
            "unit": "soccer balls",
            "hint1": "The total cost cannot exceed $300.",
            "hint2": "300 − 84 = 216, then 216 ÷ 27 = 8.",
            "meaning": "The team can buy at most 8 soccer balls."
        },
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
            "title": "Points Per Race",
            "kind": "Equation",
            "story": "A driver earned x total points across 6 races at an average of 18 points per race.",
            "question": "How many total points did the driver earn?",
            "models": ["x / 6 = 18", "6x = 18", "x + 6 = 18", "18 / x = 6"],
            "correct_model": "x / 6 = 18",
            "answer": 108,
            "unit": "points",
            "hint1": "The total is spread across 6 races.",
            "hint2": "x ÷ 6 = 18, so x = 108.",
            "meaning": "The driver earned 108 total points."
        },
        {
            "title": "Sprint Points Chase",
            "kind": "Equation",
            "story": "A driver has 74 points. Each sprint win in this classroom model adds 8 points. The target is 98 points.",
            "question": "How many sprint wins are needed?",
            "models": ["74 + 8x = 98", "74 + x = 98", "8x = 98", "98 + 8x = 74"],
            "correct_model": "74 + 8x = 98",
            "answer": 3,
            "unit": "sprint wins",
            "hint1": "Start at 74 and add 8 for each win.",
            "hint2": "74 + 8x = 98 → subtract 74, then divide by 8.",
            "meaning": "The driver needs 3 sprint wins."
        },
        {
            "title": "Lap Time Improvement",
            "kind": "Equation",
            "story": "A driver's lap time was 92 seconds, then improved by x seconds to 87 seconds.",
            "question": "How many seconds faster was the new lap?",
            "models": ["92 - x = 87", "92 + x = 87", "87 - x = 92", "92x = 87"],
            "correct_model": "92 - x = 87",
            "answer": 5,
            "unit": "seconds",
            "hint1": "A faster lap means the time decreased.",
            "hint2": "92 − x = 87, so x = 5.",
            "meaning": "The new lap was 5 seconds faster."
        },
        {
            "title": "Merchandise Budget",
            "kind": "Inequality",
            "story": "A fan has $250. After spending $70 on a ticket, each team shirt costs $45.",
            "question": "What is the greatest number of shirts the fan can buy?",
            "models": ["70 + 45x ≤ 250", "70 + 45x ≥ 250", "45 + 70x ≤ 250", "250 + 45x ≤ 70"],
            "correct_model": "70 + 45x ≤ 250",
            "answer": 4,
            "unit": "shirts",
            "hint1": "The total cost cannot be more than $250.",
            "hint2": "250 − 70 = 180, and 180 ÷ 45 = 4.",
            "meaning": "The fan can buy at most 4 shirts."
        },
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

def equations_inequalities_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Equations & Inequalities</div>', unsafe_allow_html=True)
    st.subheader("⚖️ Sports Equation Lab")
    st.write(
        "Translate a sports situation into math, solve it, and explain what the answer means. "
        "Try first — stronger hints appear only after repeated mistakes."
    )

    if generated_case is not None and generated_sport:
        eq_sport = generated_sport
        case = generated_case
    elif generated_sport and generated_title:
        eq_sport = generated_sport
        case_options = EQUATION_CASES[eq_sport]
        matches = [c for c in case_options if c["title"] == generated_title]
        if not matches:
            st.error("The generated problem could not be found.")
            return
        case = matches[0]
    else:
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

        # Reset the chosen problem if the sport changes.
        sport_state_key = "eq_last_sport"
        if st.session_state.get(sport_state_key) != eq_sport:
            st.session_state[sport_state_key] = eq_sport
            st.session_state.pop("eq_case", None)

        def choose_different_equation_problem(options):
            current = st.session_state.get("eq_case")
            choices = [label for label in options if label != current]
            if choices:
                st.session_state["eq_case"] = random.choice(choices)

        with c2:
            case_label = st.selectbox("Problem", list(labels), key="eq_case")

        st.button(
            "🎲 Give Me a Different Problem",
            key="eq_new_problem",
            use_container_width=True,
            on_click=choose_different_equation_problem,
            args=(list(labels),),
        )

        case = labels[st.session_state.get("eq_case", case_label)]

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
# 7TH GRADE MATH LAB — PROBABILITY
# =========================================================
PROBABILITY_CASES = {
    "NFL": [
        {
            "title": "Field Goal Success",
            "story": "A kicker made 18 of 24 field-goal attempts.",
            "successes": 18, "trials": 24, "future": 40,
            "event": "made field goals", "trial_label": "attempts"
        },
        {
            "title": "Two-Point Conversion",
            "story": "A team converted 7 of 10 two-point attempts.",
            "successes": 7, "trials": 10, "future": 20,
            "event": "successful conversions", "trial_label": "attempts"
        },
        {
            "title": "Third-Down Conversions",
            "story": "An offense converted 16 of 40 third downs.",
            "successes": 16, "trials": 40, "future": 60,
            "event": "third-down conversions", "trial_label": "third downs"
        },
        {
            "title": "Interception Frequency",
            "story": "A quarterback threw 5 interceptions in 100 pass attempts.",
            "successes": 5, "trials": 100, "future": 200,
            "event": "interceptions", "trial_label": "pass attempts"
        },
        {
            "title": "Red-Zone Touchdowns",
            "story": "A team scored touchdowns on 21 of 30 red-zone trips.",
            "successes": 21, "trials": 30, "future": 50,
            "event": "red-zone touchdowns", "trial_label": "red-zone trips"
        },
        {
            "title": "Coin Toss Simulation",
            "story": "In a classroom football simulation, heads appeared 27 times in 50 tosses.",
            "successes": 27, "trials": 50, "future": 100,
            "event": "heads", "trial_label": "coin tosses"
        },
    ],
    "NBA": [
        {
            "title": "Free Throw Success",
            "story": "A player made 72 of 90 free throws.",
            "successes": 72, "trials": 90, "future": 50,
            "event": "made free throws", "trial_label": "free-throw attempts"
        },
        {
            "title": "Three-Point Shooting",
            "story": "A player made 15 of 40 three-point attempts.",
            "successes": 15, "trials": 40, "future": 80,
            "event": "made three-pointers", "trial_label": "three-point attempts"
        },
        {
            "title": "Layup Drill",
            "story": "A player made 18 of 20 layups in practice.",
            "successes": 18, "trials": 20, "future": 50,
            "event": "made layups", "trial_label": "layup attempts"
        },
        {
            "title": "Steal Chance",
            "story": "A defender recorded a steal on 9 of 30 tracked possessions.",
            "successes": 9, "trials": 30, "future": 100,
            "event": "steals", "trial_label": "possessions"
        },
        {
            "title": "Shot Contest Result",
            "story": "An opponent missed 14 of 25 shots when closely defended.",
            "successes": 14, "trials": 25, "future": 50,
            "event": "missed shots", "trial_label": "closely defended shots"
        },
        {
            "title": "Half-Court Challenge",
            "story": "A student made 3 of 20 half-court shots.",
            "successes": 3, "trials": 20, "future": 60,
            "event": "made half-court shots", "trial_label": "half-court attempts"
        },
    ],
    "MLB": [
        {
            "title": "Hit Probability",
            "story": "A hitter recorded 32 hits in 100 at-bats.",
            "successes": 32, "trials": 100, "future": 150,
            "event": "hits", "trial_label": "at-bats"
        },
        {
            "title": "Home Run Frequency",
            "story": "A hitter hit 8 home runs in 50 at-bats.",
            "successes": 8, "trials": 50, "future": 125,
            "event": "home runs", "trial_label": "at-bats"
        },
        {
            "title": "Stolen Base Success",
            "story": "A runner was successful on 21 of 25 stolen-base attempts.",
            "successes": 21, "trials": 25, "future": 40,
            "event": "successful steals", "trial_label": "stolen-base attempts"
        },
        {
            "title": "Strikeout Rate",
            "story": "A pitcher struck out 27 of 90 batters faced.",
            "successes": 27, "trials": 90, "future": 180,
            "event": "strikeouts", "trial_label": "batters faced"
        },
        {
            "title": "Fielding Success",
            "story": "A fielder made the play on 47 of 50 chances.",
            "successes": 47, "trials": 50, "future": 100,
            "event": "successful fielding plays", "trial_label": "fielding chances"
        },
        {
            "title": "Pitch Location",
            "story": "A pitcher threw 36 strikes in 60 pitches.",
            "successes": 36, "trials": 60, "future": 100,
            "event": "strikes", "trial_label": "pitches"
        },
    ],
    "NHL": [
        {
            "title": "Save Probability",
            "story": "A goalie saved 45 of 50 shots.",
            "successes": 45, "trials": 50, "future": 80,
            "event": "saves", "trial_label": "shots faced"
        },
        {
            "title": "Shootout Success",
            "story": "A player scored on 6 of 10 shootout attempts.",
            "successes": 6, "trials": 10, "future": 25,
            "event": "shootout goals", "trial_label": "shootout attempts"
        },
        {
            "title": "Power-Play Success",
            "story": "A team scored on 9 of 30 power-play chances.",
            "successes": 9, "trials": 30, "future": 50,
            "event": "power-play goals", "trial_label": "power-play chances"
        },
        {
            "title": "Faceoff Wins",
            "story": "A center won 28 of 50 faceoffs.",
            "successes": 28, "trials": 50, "future": 75,
            "event": "faceoff wins", "trial_label": "faceoffs"
        },
        {
            "title": "Penalty Kill",
            "story": "A team successfully killed 24 of 30 penalties.",
            "successes": 24, "trials": 30, "future": 50,
            "event": "successful penalty kills", "trial_label": "penalties"
        },
        {
            "title": "Shot Accuracy",
            "story": "A player put 18 of 30 shot attempts on goal.",
            "successes": 18, "trials": 30, "future": 60,
            "event": "shots on goal", "trial_label": "shot attempts"
        },
    ],
    "Soccer": [
        {
            "title": "Penalty Kick Success",
            "story": "A player scored 8 of 10 penalty kicks.",
            "successes": 8, "trials": 10, "future": 25,
            "event": "penalty goals", "trial_label": "penalty attempts"
        },
        {
            "title": "Shots on Target",
            "story": "A forward put 21 of 35 shots on target.",
            "successes": 21, "trials": 35, "future": 70,
            "event": "shots on target", "trial_label": "shots"
        },
        {
            "title": "Pass Completion",
            "story": "A midfielder completed 72 of 90 passes.",
            "successes": 72, "trials": 90, "future": 120,
            "event": "completed passes", "trial_label": "passes"
        },
        {
            "title": "Corner Kick Conversion",
            "story": "A team scored from 3 of 20 corner kicks.",
            "successes": 3, "trials": 20, "future": 60,
            "event": "goals from corners", "trial_label": "corner kicks"
        },
        {
            "title": "Tackle Success",
            "story": "A defender won 18 of 24 tackles.",
            "successes": 18, "trials": 24, "future": 40,
            "event": "successful tackles", "trial_label": "tackles"
        },
        {
            "title": "Goalkeeper Saves",
            "story": "A goalkeeper saved 27 of 30 shots on target.",
            "successes": 27, "trials": 30, "future": 50,
            "event": "saves", "trial_label": "shots on target"
        },
    ],
    "Formula 1": [
        {
            "title": "Podium Frequency",
            "story": "A driver finished on the podium in 9 of 12 races.",
            "successes": 9, "trials": 12, "future": 20,
            "event": "podium finishes", "trial_label": "races"
        },
        {
            "title": "Top-10 Finish Rate",
            "story": "A driver finished in the top 10 in 14 of 18 races.",
            "successes": 14, "trials": 18, "future": 24,
            "event": "top-10 finishes", "trial_label": "races"
        },
        {
            "title": "Pit Stop Success",
            "story": "A team completed 23 of 25 pit stops without an error.",
            "successes": 23, "trials": 25, "future": 50,
            "event": "error-free pit stops", "trial_label": "pit stops"
        },
        {
            "title": "Qualifying Advancement",
            "story": "A driver advanced to the final qualifying round in 11 of 15 events.",
            "successes": 11, "trials": 15, "future": 20,
            "event": "final-round qualifying appearances", "trial_label": "qualifying events"
        },
        {
            "title": "Race Finish Reliability",
            "story": "A car finished 17 of 20 races.",
            "successes": 17, "trials": 20, "future": 30,
            "event": "race finishes", "trial_label": "race starts"
        },
        {
            "title": "Fastest Lap Frequency",
            "story": "A driver recorded fastest lap in 4 of 16 races.",
            "successes": 4, "trials": 16, "future": 24,
            "event": "fastest laps", "trial_label": "races"
        },
    ],
}

def probability_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Probability</div>', unsafe_allow_html=True)
    st.subheader("🎲 Sports Probability Lab")
    st.write(
        "Use experimental results to find probability, convert between forms, and make a prediction."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    elif generated_sport and generated_title:
        sport = generated_sport
        matches = [c for c in PROBABILITY_CASES[sport] if c["title"] == generated_title]
        if not matches:
            st.error("The generated probability problem could not be found.")
            return
        case = matches[0]
    else:
        sports = list(PROBABILITY_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="prob_sport")
        labels = {c["title"]: c for c in PROBABILITY_CASES[sport]}
        selected = st.selectbox("Scenario", list(labels), key="prob_case")
        case = labels[selected]

    successes = float(case["successes"])
    trials = float(case["trials"])
    future = float(case["future"])
    true_decimal = successes / trials
    true_percent = true_decimal * 100
    true_prediction = true_decimal * future
    case_id = clean_filename(f"{sport}_{case['title']}")

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 · Write the experimental probability")
    st.write(
        f"Write the probability of **{case['event']}** using the results above."
    )
    ratio_raw = st.text_input(
        "Probability as a fraction or ratio",
        key=f"prob_ratio_{case_id}",
        placeholder="Type a fraction or ratio"
    )

    def probability_ratio_correct(text):
        compact = str(text).strip().replace(" ", "").replace(",", "").replace(":", "/").replace("÷", "/")
        if not compact:
            return False
        if "/" in compact:
            parts = compact.split("/")
            if len(parts) != 2:
                return False
            try:
                return Fraction(parts[0]) / Fraction(parts[1]) == Fraction(str(successes)) / Fraction(str(trials))
            except (ValueError, ZeroDivisionError):
                return False
        try:
            return math.isclose(float(compact), true_decimal, abs_tol=0.0001)
        except ValueError:
            return False

    ratio_attempt_key = f"prob_ratio_attempts_{case_id}"
    if ratio_attempt_key not in st.session_state:
        st.session_state[ratio_attempt_key] = 0

    if st.button("Check My Probability", key=f"prob_ratio_check_{case_id}", use_container_width=True):
        if probability_ratio_correct(ratio_raw):
            st.success("✅ Correct. Equivalent fractions are accepted.")
            st.session_state[ratio_attempt_key] = 0
        else:
            st.session_state[ratio_attempt_key] += 1
            if st.session_state[ratio_attempt_key] == 1:
                st.info("Experimental probability = successful outcomes ÷ total trials.")
            else:
                simplified = Fraction(int(successes), int(trials))
                st.warning(
                    f"Use **{int(successes)}/{int(trials)}**. "
                    f"That simplifies to **{simplified.numerator}/{simplified.denominator}**."
                )

    st.markdown("### Step 2 · Convert to a decimal")
    dec_raw = st.text_input(
        "Probability as a decimal",
        key=f"prob_decimal_{case_id}",
        placeholder="Type your answer"
    )
    dec = parse_student_number(dec_raw)

    if st.button("Check My Decimal", key=f"prob_dec_check_{case_id}", use_container_width=True):
        if dec is not None and math.isclose(dec, true_decimal, abs_tol=0.01):
            st.success(f"✅ Correct — about {true_decimal:.2f}.")
        else:
            if difficulty == "Guided":
                st.info("Divide the number of successful outcomes by the total number of trials.")
            else:
                st.info("Check your decimal and try again.")

    st.markdown("### Step 3 · Convert to a percent")
    pct_raw = st.text_input(
        "Probability as a percent",
        key=f"prob_percent_{case_id}",
        placeholder="Type the percent"
    )
    pct = parse_student_number(pct_raw)

    if st.button("Check My Percent", key=f"prob_pct_check_{case_id}", use_container_width=True):
        if pct is not None and math.isclose(pct, true_percent, abs_tol=0.5):
            st.success(f"✅ Correct — about {true_percent:.1f}%.")
        else:
            st.info("Convert the decimal to a percent. Think about multiplying by 100.")

    st.markdown("### Step 4 · Make a prediction")
    st.write(
        f"If the same experimental rate continued over **{fmt(future)} {case['trial_label']}**, "
        f"about how many **{case['event']}** would you predict?"
    )
    pred_raw = st.text_input(
        "Predicted number of successful outcomes",
        key=f"prob_prediction_{case_id}",
        placeholder="Type your answer"
    )
    pred = parse_student_number(pred_raw)

    if st.button("Check My Prediction", key=f"prob_pred_check_{case_id}", use_container_width=True):
        tol = max(0.5, abs(true_prediction) * 0.02)
        if pred is not None and math.isclose(pred, true_prediction, abs_tol=tol):
            st.success(f"✅ Reasonable prediction — about {true_prediction:.1f}.")
        else:
            if difficulty == "Guided":
                st.info("Use your probability from Step 2 with the new number of trials.")
            else:
                st.info("Check how you used the probability to scale up.")

    st.markdown("### Step 5 · Probability means prediction, not certainty")
    reasoning = st.text_area(
        "Why is your predicted result not guaranteed to happen exactly?",
        key=f"prob_reasoning_{case_id}",
        placeholder="Explain in your own words."
    )

# =========================================================
# 7TH GRADE MATH LAB — PERCENT & PERCENT CHANGE
# =========================================================
PERCENT_CASES = {
    "NFL": [
        {
            "title": "Completion Percentage",
            "kind": "Percent",
            "story": "A quarterback completed 24 of 32 passes.",
            "part": 24, "whole": 32,
            "question": "What percent of passes were completed?",
            "answer": 75.0,
            "unit": "%",
            "hint1": "Think: part ÷ whole × 100.",
            "hint2": "24 ÷ 32 = 0.75, then 0.75 × 100 = 75%."
        },
        {
            "title": "Red-Zone Success",
            "kind": "Percent",
            "story": "A team scored touchdowns on 21 of 30 red-zone trips.",
            "part": 21, "whole": 30,
            "question": "What percent of red-zone trips ended in touchdowns?",
            "answer": 70.0,
            "unit": "%",
            "hint1": "Use successful trips as the part and total trips as the whole.",
            "hint2": "21 ÷ 30 = 0.70, so the answer is 70%."
        },
        {
            "title": "Receiving Yards Increase",
            "kind": "Percent Change",
            "story": "A receiver increased from 900 receiving yards to 1,080 receiving yards.",
            "old": 900, "new": 1080,
            "question": "What was the percent change?",
            "answer": 20.0,
            "direction": "increase",
            "hint1": "Find the change first, then compare it to the original amount.",
            "hint2": "1,080 − 900 = 180; 180 ÷ 900 × 100 = 20%."
        },
        {
            "title": "Sack Total Decrease",
            "kind": "Percent Change",
            "story": "A quarterback's sack total dropped from 40 to 30.",
            "old": 40, "new": 30,
            "question": "What was the percent change?",
            "answer": -25.0,
            "direction": "decrease",
            "hint1": "Use new − old, then divide by the old amount.",
            "hint2": "30 − 40 = −10; −10 ÷ 40 × 100 = −25%."
        },
        {
            "title": "Fantasy Bonus",
            "kind": "Percent Of",
            "story": "A fantasy team scored 120 points. A bonus is worth 15% of that score.",
            "percent": 15, "base": 120,
            "question": "How many bonus points is that?",
            "answer": 18.0,
            "unit": "points",
            "hint1": "Find 15% of 120.",
            "hint2": "0.15 × 120 = 18."
        },
        {
            "title": "Ticket Discount",
            "kind": "Discount",
            "story": "A football ticket costs $80 and is discounted by 25%.",
            "percent": 25, "base": 80,
            "question": "What is the sale price?",
            "answer": 60.0,
            "unit": "dollars",
            "hint1": "First find 25% of $80, then subtract the discount.",
            "hint2": "0.25 × 80 = 20; 80 − 20 = 60."
        },
    ],
    "NBA": [
        {
            "title": "Free Throw Percentage",
            "kind": "Percent",
            "story": "A player made 18 of 24 free throws.",
            "part": 18, "whole": 24,
            "question": "What percent of free throws were made?",
            "answer": 75.0,
            "unit": "%",
            "hint1": "Made shots are the part; attempts are the whole.",
            "hint2": "18 ÷ 24 = 0.75 = 75%."
        },
        {
            "title": "Three-Point Percentage",
            "kind": "Percent",
            "story": "A player made 14 of 40 three-point attempts.",
            "part": 14, "whole": 40,
            "question": "What percent of three-point attempts were made?",
            "answer": 35.0,
            "unit": "%",
            "hint1": "Use makes ÷ attempts × 100.",
            "hint2": "14 ÷ 40 = 0.35 = 35%."
        },
        {
            "title": "Scoring Increase",
            "kind": "Percent Change",
            "story": "A player's scoring average rose from 20 points per game to 25.",
            "old": 20, "new": 25,
            "question": "What was the percent change?",
            "answer": 25.0,
            "direction": "increase",
            "hint1": "Compare the 5-point increase to the original 20.",
            "hint2": "5 ÷ 20 × 100 = 25%."
        },
        {
            "title": "Turnover Reduction",
            "kind": "Percent Change",
            "story": "A team reduced its turnovers from 16 per game to 12.",
            "old": 16, "new": 12,
            "question": "What was the percent change?",
            "answer": -25.0,
            "direction": "decrease",
            "hint1": "Use new − old and divide by the old amount.",
            "hint2": "12 − 16 = −4; −4 ÷ 16 × 100 = −25%."
        },
        {
            "title": "Charity Shot Donation",
            "kind": "Percent Of",
            "story": "A fundraiser collected $240. Twenty percent will be donated to a youth basketball program.",
            "percent": 20, "base": 240,
            "question": "How much money will be donated?",
            "answer": 48.0,
            "unit": "dollars",
            "hint1": "Find 20% of 240.",
            "hint2": "0.20 × 240 = 48."
        },
        {
            "title": "Jersey Sale",
            "kind": "Discount",
            "story": "A basketball jersey costs $90 and is discounted by 30%.",
            "percent": 30, "base": 90,
            "question": "What is the sale price?",
            "answer": 63.0,
            "unit": "dollars",
            "hint1": "Find the discount amount first, then subtract it.",
            "hint2": "0.30 × 90 = 27; 90 − 27 = 63."
        },
    ],
    "MLB": [
        {
            "title": "Hit Percentage",
            "kind": "Percent",
            "story": "A hitter got 36 hits in 120 at-bats.",
            "part": 36, "whole": 120,
            "question": "What percent of at-bats resulted in hits?",
            "answer": 30.0,
            "unit": "%",
            "hint1": "Hits are the part; at-bats are the whole.",
            "hint2": "36 ÷ 120 = 0.30 = 30%."
        },
        {
            "title": "Stolen Base Success",
            "kind": "Percent",
            "story": "A runner was successful on 18 of 24 stolen-base attempts.",
            "part": 18, "whole": 24,
            "question": "What was the stolen-base success percentage?",
            "answer": 75.0,
            "unit": "%",
            "hint1": "Use successes ÷ attempts × 100.",
            "hint2": "18 ÷ 24 = 75%."
        },
        {
            "title": "Home Run Increase",
            "kind": "Percent Change",
            "story": "A hitter increased from 24 home runs to 30.",
            "old": 24, "new": 30,
            "question": "What was the percent change?",
            "answer": 25.0,
            "direction": "increase",
            "hint1": "Find the increase and compare it with the original 24.",
            "hint2": "30 − 24 = 6; 6 ÷ 24 × 100 = 25%."
        },
        {
            "title": "ERA Drop",
            "kind": "Percent Change",
            "story": "A pitcher's ERA dropped from 4.00 to 3.20.",
            "old": 4.0, "new": 3.2,
            "question": "What was the percent change?",
            "answer": -20.0,
            "direction": "decrease",
            "hint1": "The change is negative because the value went down.",
            "hint2": "3.2 − 4.0 = −0.8; −0.8 ÷ 4.0 × 100 = −20%."
        },
        {
            "title": "Concession Donation",
            "kind": "Percent Of",
            "story": "A concession stand made $350. Twelve percent goes to the baseball program.",
            "percent": 12, "base": 350,
            "question": "How much goes to the baseball program?",
            "answer": 42.0,
            "unit": "dollars",
            "hint1": "Find 12% of 350.",
            "hint2": "0.12 × 350 = 42."
        },
        {
            "title": "Cap Sale",
            "kind": "Discount",
            "story": "A baseball cap costs $32 and is discounted by 25%.",
            "percent": 25, "base": 32,
            "question": "What is the sale price?",
            "answer": 24.0,
            "unit": "dollars",
            "hint1": "Find 25% of 32 and subtract.",
            "hint2": "0.25 × 32 = 8; 32 − 8 = 24."
        },
    ],
    "NHL": [
        {
            "title": "Save Percentage",
            "kind": "Percent",
            "story": "A goalie saved 45 of 50 shots.",
            "part": 45, "whole": 50,
            "question": "What percent of shots were saved?",
            "answer": 90.0,
            "unit": "%",
            "hint1": "Saves are the part; shots faced are the whole.",
            "hint2": "45 ÷ 50 = 0.90 = 90%."
        },
        {
            "title": "Faceoff Win Percentage",
            "kind": "Percent",
            "story": "A center won 28 of 40 faceoffs.",
            "part": 28, "whole": 40,
            "question": "What percent of faceoffs were won?",
            "answer": 70.0,
            "unit": "%",
            "hint1": "Use wins ÷ total faceoffs × 100.",
            "hint2": "28 ÷ 40 = 70%."
        },
        {
            "title": "Goal Increase",
            "kind": "Percent Change",
            "story": "A player's goal total increased from 32 to 40.",
            "old": 32, "new": 40,
            "question": "What was the percent change?",
            "answer": 25.0,
            "direction": "increase",
            "hint1": "Compare the 8-goal increase to the original 32.",
            "hint2": "8 ÷ 32 × 100 = 25%."
        },
        {
            "title": "Penalty Minutes Decrease",
            "kind": "Percent Change",
            "story": "A player's penalty minutes fell from 50 to 35.",
            "old": 50, "new": 35,
            "question": "What was the percent change?",
            "answer": -30.0,
            "direction": "decrease",
            "hint1": "Use new − old, then divide by old.",
            "hint2": "35 − 50 = −15; −15 ÷ 50 × 100 = −30%."
        },
        {
            "title": "Equipment Fund",
            "kind": "Percent Of",
            "story": "A team raises $500. Eighteen percent is used for new pucks.",
            "percent": 18, "base": 500,
            "question": "How much money is used for pucks?",
            "answer": 90.0,
            "unit": "dollars",
            "hint1": "Find 18% of 500.",
            "hint2": "0.18 × 500 = 90."
        },
        {
            "title": "Stick Discount",
            "kind": "Discount",
            "story": "A hockey stick costs $120 and is discounted by 20%.",
            "percent": 20, "base": 120,
            "question": "What is the sale price?",
            "answer": 96.0,
            "unit": "dollars",
            "hint1": "Find the 20% discount, then subtract it.",
            "hint2": "0.20 × 120 = 24; 120 − 24 = 96."
        },
    ],
    "Soccer": [
        {
            "title": "Pass Completion Percentage",
            "kind": "Percent",
            "story": "A midfielder completed 72 of 90 passes.",
            "part": 72, "whole": 90,
            "question": "What percent of passes were completed?",
            "answer": 80.0,
            "unit": "%",
            "hint1": "Completed passes are the part.",
            "hint2": "72 ÷ 90 = 0.80 = 80%."
        },
        {
            "title": "Penalty Kick Percentage",
            "kind": "Percent",
            "story": "A player scored on 8 of 10 penalty kicks.",
            "part": 8, "whole": 10,
            "question": "What percent of penalty kicks were scored?",
            "answer": 80.0,
            "unit": "%",
            "hint1": "Use goals ÷ attempts × 100.",
            "hint2": "8 ÷ 10 = 80%."
        },
        {
            "title": "Goal Increase",
            "kind": "Percent Change",
            "story": "A player's goal total increased from 15 to 18.",
            "old": 15, "new": 18,
            "question": "What was the percent change?",
            "answer": 20.0,
            "direction": "increase",
            "hint1": "Compare the 3-goal increase to the original 15.",
            "hint2": "3 ÷ 15 × 100 = 20%."
        },
        {
            "title": "Shots Decrease",
            "kind": "Percent Change",
            "story": "A team reduced its shots allowed from 20 per match to 15.",
            "old": 20, "new": 15,
            "question": "What was the percent change?",
            "answer": -25.0,
            "direction": "decrease",
            "hint1": "Use new − old and divide by the original amount.",
            "hint2": "15 − 20 = −5; −5 ÷ 20 × 100 = −25%."
        },
        {
            "title": "Club Fundraiser",
            "kind": "Percent Of",
            "story": "A club raises $420. Fifteen percent will be used for equipment.",
            "percent": 15, "base": 420,
            "question": "How much money will be used for equipment?",
            "answer": 63.0,
            "unit": "dollars",
            "hint1": "Find 15% of 420.",
            "hint2": "0.15 × 420 = 63."
        },
        {
            "title": "Scarf Sale",
            "kind": "Discount",
            "story": "A team scarf costs $40 and is discounted by 35%.",
            "percent": 35, "base": 40,
            "question": "What is the sale price?",
            "answer": 26.0,
            "unit": "dollars",
            "hint1": "Find the discount amount and subtract it.",
            "hint2": "0.35 × 40 = 14; 40 − 14 = 26."
        },
    ],
    "Formula 1": [
        {
            "title": "Race Finish Percentage",
            "kind": "Percent",
            "story": "A driver finished 18 of 20 races.",
            "part": 18, "whole": 20,
            "question": "What percent of races were finished?",
            "answer": 90.0,
            "unit": "%",
            "hint1": "Finished races are the part; starts are the whole.",
            "hint2": "18 ÷ 20 = 90%."
        },
        {
            "title": "Top-10 Percentage",
            "kind": "Percent",
            "story": "A driver finished in the top 10 in 14 of 20 races.",
            "part": 14, "whole": 20,
            "question": "What percent of races were top-10 finishes?",
            "answer": 70.0,
            "unit": "%",
            "hint1": "Use top-10 finishes ÷ races × 100.",
            "hint2": "14 ÷ 20 = 70%."
        },
        {
            "title": "Points Increase",
            "kind": "Percent Change",
            "story": "A driver's championship points increased from 200 to 250.",
            "old": 200, "new": 250,
            "question": "What was the percent change?",
            "answer": 25.0,
            "direction": "increase",
            "hint1": "Compare the increase of 50 to the original 200.",
            "hint2": "50 ÷ 200 × 100 = 25%."
        },
        {
            "title": "Pit Time Reduction",
            "kind": "Percent Change",
            "story": "A pit stop time improved from 4.0 seconds to 3.2 seconds.",
            "old": 4.0, "new": 3.2,
            "question": "What was the percent change?",
            "answer": -20.0,
            "direction": "decrease",
            "hint1": "A faster pit stop means the time decreased.",
            "hint2": "3.2 − 4.0 = −0.8; −0.8 ÷ 4.0 × 100 = −20%."
        },
        {
            "title": "Merchandise Share",
            "kind": "Percent Of",
            "story": "A race-day shop makes $600. Twelve percent goes to a youth racing program.",
            "percent": 12, "base": 600,
            "question": "How much money goes to the youth program?",
            "answer": 72.0,
            "unit": "dollars",
            "hint1": "Find 12% of 600.",
            "hint2": "0.12 × 600 = 72."
        },
        {
            "title": "Team Shirt Discount",
            "kind": "Discount",
            "story": "A team shirt costs $50 and is discounted by 30%.",
            "percent": 30, "base": 50,
            "question": "What is the sale price?",
            "answer": 35.0,
            "unit": "dollars",
            "hint1": "Find 30% of 50 and subtract it.",
            "hint2": "0.30 × 50 = 15; 50 − 15 = 35."
        },
    ],
}

def percent_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Percent & Percent Change</div>', unsafe_allow_html=True)
    st.subheader("📈 Sports Percent Lab")
    st.write(
        "Work with percent, percent of a number, discounts, and percent change in sports situations."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    elif generated_sport and generated_title:
        sport = generated_sport
        matches = [c for c in PERCENT_CASES[sport] if c["title"] == generated_title]
        if not matches:
            st.error("The generated percent problem could not be found.")
            return
        case = matches[0]
    else:
        sports = list(PERCENT_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="pct_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in PERCENT_CASES[sport]}
        chosen = st.selectbox("Scenario", list(labels), key="pct_case")
        case = labels[chosen]

    case_id = clean_filename(f"{sport}_{case['title']}")
    answer = float(case["answer"])

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 · Decide what matters")
    if case["kind"] == "Percent":
        prompt = "Which relationship should you use?"
        options = [
            "part ÷ whole × 100",
            "whole ÷ part × 100",
            "part + whole",
            "whole − part"
        ]
        correct_option = "part ÷ whole × 100"
    elif case["kind"] == "Percent Change":
        prompt = "Which relationship should you use?"
        options = [
            "(new − old) ÷ old × 100",
            "(old − new) ÷ new × 100",
            "new ÷ old",
            "old + new"
        ]
        correct_option = "(new − old) ÷ old × 100"
    elif case["kind"] == "Percent Of":
        prompt = "Which relationship should you use?"
        options = [
            "percent as a decimal × whole",
            "whole ÷ percent",
            "whole + percent",
            "percent ÷ whole"
        ]
        correct_option = "percent as a decimal × whole"
    else:
        prompt = "Which plan makes sense?"
        options = [
            "find the discount, then subtract it from the original price",
            "add the discount to the original price",
            "divide the original price by the discount percent",
            "use only the discount as the sale price"
        ]
        correct_option = "find the discount, then subtract it from the original price"

    order_key = f"pct_model_order_{case_id}"
    if order_key not in st.session_state:
        shuffled = list(options)
        random.shuffle(shuffled)
        st.session_state[order_key] = shuffled

    model = st.radio(prompt, st.session_state[order_key], key=f"pct_model_{case_id}")

    if st.button("Check My Plan", key=f"pct_model_check_{case_id}", use_container_width=True):
        if model == correct_option:
            st.success("✅ Good plan.")
        else:
            st.info("Look at what the question is asking you to find and try again.")

    st.markdown("### Step 2 · Calculate")
    raw = st.text_input(
        "Your answer",
        key=f"pct_answer_{case_id}",
        placeholder="Type your answer"
    )
    student = parse_student_number(raw)

    attempts_key = f"pct_attempts_{case_id}"
    if attempts_key not in st.session_state:
        st.session_state[attempts_key] = 0

    if st.button("Check My Answer", key=f"pct_answer_check_{case_id}", use_container_width=True):
        tolerance = max(0.1, abs(answer) * 0.01)
        if student is not None and math.isclose(student, answer, abs_tol=tolerance):
            if case["kind"] == "Percent Change":
                direction = "increase" if answer > 0 else "decrease" if answer < 0 else "no change"
                st.success(f"✅ Correct — {abs(answer):.1f}% {direction}.")
            elif case.get("unit") == "%":
                st.success(f"✅ Correct — {answer:.1f}%.")
            elif case.get("unit") == "dollars":
                st.success(f"✅ Correct — ${answer:.2f}.")
            else:
                st.success(f"✅ Correct — {answer:.1f} {case.get('unit','')}.")
            st.session_state[attempts_key] = 0
        else:
            st.session_state[attempts_key] += 1
            if st.session_state[attempts_key] == 1:
                st.info(case["hint1"])
            else:
                st.warning(case["hint2"])

    if case["kind"] == "Percent Change":
        st.markdown("### Step 3 · Increase or decrease?")
        direction_choice = st.radio(
            "How did the value change?",
            ["Increase", "Decrease", "No Change"],
            horizontal=True,
            key=f"pct_direction_{case_id}"
        )
        if st.button("Check Direction", key=f"pct_direction_check_{case_id}", use_container_width=True):
            expected = "Increase" if answer > 0 else "Decrease" if answer < 0 else "No Change"
            if direction_choice == expected:
                st.success("✅ Correct.")
            else:
                st.info("Look at whether the new value is larger or smaller than the old value.")

    st.markdown("### Final · Explain what your answer means")
    st.text_area(
        "Explain the result in the context of the sports situation.",
        key=f"pct_reasoning_{case_id}",
        placeholder="Use the numbers and the situation in your explanation."
    )

# =========================================================
# 7TH GRADE MATH LAB — RATIONAL NUMBERS
# =========================================================
RATIONAL_CASES = {
    "NFL": [
        {
            "title": "Drive Yardage Change",
            "kind": "Integer Addition",
            "story": "An offense gains 18 yards, then loses 7 yards on the next play.",
            "expression": "18 + (-7)",
            "answer": 11,
            "unit": "yards",
            "question": "What is the net yardage change?",
            "hint1": "A loss can be represented by a negative number.",
            "hint2": "18 + (−7) = 11."
        },
        {
            "title": "Penalty Loss",
            "kind": "Integer Subtraction",
            "story": "A team is at +12 yards on a drive, then receives a 15-yard penalty.",
            "expression": "12 - 15",
            "answer": -3,
            "unit": "yards",
            "question": "What is the team's net position compared with where the drive started?",
            "hint1": "Subtract the penalty from the gain.",
            "hint2": "12 − 15 = −3."
        },
        {
            "title": "Fantasy Point Swing",
            "kind": "Decimal Addition",
            "story": "A fantasy player earns 8.6 points, then loses 2.0 points because of a turnover.",
            "expression": "8.6 + (-2.0)",
            "answer": 6.6,
            "unit": "fantasy points",
            "question": "What is the player's net fantasy score from those events?",
            "hint1": "Treat the lost points as a negative value.",
            "hint2": "8.6 + (−2.0) = 6.6."
        },
        {
            "title": "Field Position Difference",
            "kind": "Integer Difference",
            "story": "One drive starts at the 25-yard line and another starts at the 42-yard line.",
            "expression": "42 - 25",
            "answer": 17,
            "unit": "yards",
            "question": "How much better is the second starting field position?",
            "hint1": "Find the distance between the two positions.",
            "hint2": "42 − 25 = 17."
        },
        {
            "title": "Quarter Scoring Differential",
            "kind": "Signed Difference",
            "story": "A team scores 10 points in one quarter and allows 17.",
            "expression": "10 - 17",
            "answer": -7,
            "unit": "points",
            "question": "What is the scoring differential for the quarter?",
            "hint1": "Differential = points scored − points allowed.",
            "hint2": "10 − 17 = −7."
        },
        {
            "title": "Average Yardage Adjustment",
            "kind": "Decimal Subtraction",
            "story": "A runner averages 5.4 yards per carry before a game and 4.8 after.",
            "expression": "4.8 - 5.4",
            "answer": -0.6,
            "unit": "yards per carry",
            "question": "What is the change in average yards per carry?",
            "hint1": "Change = new value − old value.",
            "hint2": "4.8 − 5.4 = −0.6."
        },
    ],
    "NBA": [
        {
            "title": "Plus-Minus Swing",
            "kind": "Integer Addition",
            "story": "A player is +9 in the first half and −4 in the second half.",
            "expression": "9 + (-4)",
            "answer": 5,
            "unit": "plus-minus",
            "question": "What is the player's total plus-minus?",
            "hint1": "Combine the positive and negative values.",
            "hint2": "9 + (−4) = 5."
        },
        {
            "title": "Scoring Differential",
            "kind": "Signed Difference",
            "story": "A team scores 102 points and allows 110.",
            "expression": "102 - 110",
            "answer": -8,
            "unit": "points",
            "question": "What is the team's scoring differential?",
            "hint1": "Differential = points scored − points allowed.",
            "hint2": "102 − 110 = −8."
        },
        {
            "title": "Three-Point Percentage Change",
            "kind": "Decimal Subtraction",
            "story": "A player's three-point percentage changes from 38.5% to 35.2%.",
            "expression": "35.2 - 38.5",
            "answer": -3.3,
            "unit": "percentage points",
            "question": "What is the change in percentage points?",
            "hint1": "Use new value − old value.",
            "hint2": "35.2 − 38.5 = −3.3."
        },
        {
            "title": "Bench Scoring Difference",
            "kind": "Integer Difference",
            "story": "One team's bench scores 36 points while the other bench scores 29.",
            "expression": "36 - 29",
            "answer": 7,
            "unit": "points",
            "question": "What is the scoring difference between the benches?",
            "hint1": "Subtract the smaller total from the larger.",
            "hint2": "36 − 29 = 7."
        },
        {
            "title": "Net Rating Change",
            "kind": "Decimal Addition",
            "story": "A team's net rating is +6.8, then changes by −2.5.",
            "expression": "6.8 + (-2.5)",
            "answer": 4.3,
            "unit": "rating points",
            "question": "What is the new net rating?",
            "hint1": "A decrease is represented by a negative value.",
            "hint2": "6.8 + (−2.5) = 4.3."
        },
        {
            "title": "Shot Value Difference",
            "kind": "Rational Difference",
            "story": "A two-point shot is worth 2 points and a free throw is worth 1 point.",
            "expression": "2 - 1",
            "answer": 1,
            "unit": "point",
            "question": "What is the difference in value between the two shots?",
            "hint1": "Compare the two point values.",
            "hint2": "2 − 1 = 1."
        },
    ],
    "MLB": [
        {
            "title": "Run Differential",
            "kind": "Signed Difference",
            "story": "A team scores 4 runs and allows 7.",
            "expression": "4 - 7",
            "answer": -3,
            "unit": "runs",
            "question": "What is the run differential?",
            "hint1": "Run differential = runs scored − runs allowed.",
            "hint2": "4 − 7 = −3."
        },
        {
            "title": "Batting Average Change",
            "kind": "Decimal Subtraction",
            "story": "A player's batting average changes from .284 to .271.",
            "expression": "0.271 - 0.284",
            "answer": -0.013,
            "unit": "batting-average points",
            "question": "What is the change in batting average?",
            "hint1": "Use new average − old average.",
            "hint2": "0.271 − 0.284 = −0.013."
        },
        {
            "title": "Pitch Count Adjustment",
            "kind": "Integer Addition",
            "story": "A pitcher is scheduled for 85 pitches, but the limit is adjusted downward by 12.",
            "expression": "85 + (-12)",
            "answer": 73,
            "unit": "pitches",
            "question": "What is the new pitch limit?",
            "hint1": "A downward adjustment can be represented as a negative number.",
            "hint2": "85 + (−12) = 73."
        },
        {
            "title": "Inning Run Swing",
            "kind": "Integer Addition",
            "story": "A team has a +3 run differential through six innings, then is outscored by 5 runs.",
            "expression": "3 + (-5)",
            "answer": -2,
            "unit": "runs",
            "question": "What is the new run differential?",
            "hint1": "Being outscored by 5 changes the differential by −5.",
            "hint2": "3 + (−5) = −2."
        },
        {
            "title": "ERA Difference",
            "kind": "Decimal Difference",
            "story": "Pitcher A has a 3.40 ERA and Pitcher B has a 4.15 ERA.",
            "expression": "4.15 - 3.40",
            "answer": 0.75,
            "unit": "ERA",
            "question": "What is the difference between their ERAs?",
            "hint1": "Subtract the smaller ERA from the larger.",
            "hint2": "4.15 − 3.40 = 0.75."
        },
        {
            "title": "Base Advancement",
            "kind": "Integer Subtraction",
            "story": "A runner moves forward 3 bases in one sequence, then is forced back 1 base in a classroom simulation.",
            "expression": "3 - 1",
            "answer": 2,
            "unit": "bases",
            "question": "What is the net advancement?",
            "hint1": "Forward movement is positive; backward movement reduces it.",
            "hint2": "3 − 1 = 2."
        },
    ],
    "NHL": [
        {
            "title": "Plus-Minus Total",
            "kind": "Integer Addition",
            "story": "A player is +6 over one stretch and −9 over another.",
            "expression": "6 + (-9)",
            "answer": -3,
            "unit": "plus-minus",
            "question": "What is the combined plus-minus?",
            "hint1": "Combine the positive and negative values.",
            "hint2": "6 + (−9) = −3."
        },
        {
            "title": "Goal Differential",
            "kind": "Signed Difference",
            "story": "A team scores 2 goals and allows 5.",
            "expression": "2 - 5",
            "answer": -3,
            "unit": "goals",
            "question": "What is the goal differential?",
            "hint1": "Differential = goals scored − goals allowed.",
            "hint2": "2 − 5 = −3."
        },
        {
            "title": "Save Percentage Change",
            "kind": "Decimal Subtraction",
            "story": "A goalie's save percentage changes from .918 to .904.",
            "expression": "0.904 - 0.918",
            "answer": -0.014,
            "unit": "save-percentage points",
            "question": "What is the change in save percentage?",
            "hint1": "Use new − old.",
            "hint2": "0.904 − 0.918 = −0.014."
        },
        {
            "title": "Penalty Differential",
            "kind": "Integer Difference",
            "story": "One team takes 6 penalties and the other takes 4.",
            "expression": "6 - 4",
            "answer": 2,
            "unit": "penalties",
            "question": "What is the difference in penalty totals?",
            "hint1": "Compare the two totals.",
            "hint2": "6 − 4 = 2."
        },
        {
            "title": "Shot Differential Swing",
            "kind": "Integer Addition",
            "story": "A team is +8 in shot differential, then is outshot by 11.",
            "expression": "8 + (-11)",
            "answer": -3,
            "unit": "shots",
            "question": "What is the new shot differential?",
            "hint1": "Being outshot by 11 changes the differential by −11.",
            "hint2": "8 + (−11) = −3."
        },
        {
            "title": "Ice Time Difference",
            "kind": "Decimal Difference",
            "story": "One player logs 21.5 minutes and another logs 18.75 minutes.",
            "expression": "21.5 - 18.75",
            "answer": 2.75,
            "unit": "minutes",
            "question": "What is the difference in ice time?",
            "hint1": "Subtract the smaller time from the larger.",
            "hint2": "21.5 − 18.75 = 2.75."
        },
    ],
    "Soccer": [
        {
            "title": "Goal Differential",
            "kind": "Signed Difference",
            "story": "A club scores 1 goal and allows 3.",
            "expression": "1 - 3",
            "answer": -2,
            "unit": "goals",
            "question": "What is the goal differential?",
            "hint1": "Goal differential = goals scored − goals allowed.",
            "hint2": "1 − 3 = −2."
        },
        {
            "title": "Table Point Swing",
            "kind": "Integer Addition",
            "story": "A club is 5 points above a rival, then loses 8 points of ground over several matches.",
            "expression": "5 + (-8)",
            "answer": -3,
            "unit": "points",
            "question": "What is the club's new position relative to the rival?",
            "hint1": "Losing ground is a negative change.",
            "hint2": "5 + (−8) = −3."
        },
        {
            "title": "Possession Change",
            "kind": "Decimal Subtraction",
            "story": "A team's possession changes from 57.5% to 52.0%.",
            "expression": "52.0 - 57.5",
            "answer": -5.5,
            "unit": "percentage points",
            "question": "What is the change in possession?",
            "hint1": "Use new value − old value.",
            "hint2": "52.0 − 57.5 = −5.5."
        },
        {
            "title": "Shot Difference",
            "kind": "Integer Difference",
            "story": "One team takes 14 shots and the opponent takes 9.",
            "expression": "14 - 9",
            "answer": 5,
            "unit": "shots",
            "question": "What is the shot difference?",
            "hint1": "Subtract the opponent's total.",
            "hint2": "14 − 9 = 5."
        },
        {
            "title": "Expected Goals Change",
            "kind": "Decimal Addition",
            "story": "A team's expected-goals difference is +1.4, then changes by −2.1.",
            "expression": "1.4 + (-2.1)",
            "answer": -0.7,
            "unit": "xG",
            "question": "What is the new expected-goals difference?",
            "hint1": "Combine the positive value with the negative change.",
            "hint2": "1.4 + (−2.1) = −0.7."
        },
        {
            "title": "Match Rating Difference",
            "kind": "Decimal Difference",
            "story": "Two players receive ratings of 8.2 and 6.9.",
            "expression": "8.2 - 6.9",
            "answer": 1.3,
            "unit": "rating points",
            "question": "What is the difference in their ratings?",
            "hint1": "Subtract the smaller rating from the larger.",
            "hint2": "8.2 − 6.9 = 1.3."
        },
    ],
    "Formula 1": [
        {
            "title": "Grid Position Change",
            "kind": "Integer Addition",
            "story": "A driver gains 6 positions, then loses 4 positions.",
            "expression": "6 + (-4)",
            "answer": 2,
            "unit": "positions",
            "question": "What is the net change in position?",
            "hint1": "A loss of position is negative.",
            "hint2": "6 + (−4) = 2."
        },
        {
            "title": "Championship Point Gap",
            "kind": "Signed Difference",
            "story": "Driver A has 188 points and Driver B has 205.",
            "expression": "188 - 205",
            "answer": -17,
            "unit": "points",
            "question": "What is Driver A's point differential relative to Driver B?",
            "hint1": "Use Driver A − Driver B.",
            "hint2": "188 − 205 = −17."
        },
        {
            "title": "Lap Time Change",
            "kind": "Decimal Subtraction",
            "story": "A lap improves from 91.8 seconds to 90.9 seconds.",
            "expression": "90.9 - 91.8",
            "answer": -0.9,
            "unit": "seconds",
            "question": "What is the change in lap time?",
            "hint1": "Use new time − old time.",
            "hint2": "90.9 − 91.8 = −0.9."
        },
        {
            "title": "Position Differential",
            "kind": "Integer Difference",
            "story": "One driver finishes 4th and another finishes 11th.",
            "expression": "11 - 4",
            "answer": 7,
            "unit": "positions",
            "question": "How many finishing positions separate the drivers?",
            "hint1": "Find the distance between 4 and 11.",
            "hint2": "11 − 4 = 7."
        },
        {
            "title": "Team Point Adjustment",
            "kind": "Integer Addition",
            "story": "A team has 46 points, then receives a −10 point penalty.",
            "expression": "46 + (-10)",
            "answer": 36,
            "unit": "points",
            "question": "What is the adjusted point total?",
            "hint1": "A penalty can be represented by a negative number.",
            "hint2": "46 + (−10) = 36."
        },
        {
            "title": "Pit Stop Difference",
            "kind": "Decimal Difference",
            "story": "Two pit stops take 2.4 seconds and 3.1 seconds.",
            "expression": "3.1 - 2.4",
            "answer": 0.7,
            "unit": "seconds",
            "question": "What is the difference in pit-stop time?",
            "hint1": "Subtract the shorter time from the longer.",
            "hint2": "3.1 − 2.4 = 0.7."
        },
    ],
}

def rational_numbers_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Rational Numbers</div>', unsafe_allow_html=True)
    st.subheader("➕➖ Sports Rational Numbers Lab")
    st.write(
        "Use positive and negative numbers, decimals, and differences to describe changes in sports."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    elif generated_sport and generated_title:
        sport = generated_sport
        matches = [c for c in RATIONAL_CASES[sport] if c["title"] == generated_title]
        if not matches:
            st.error("The generated rational-numbers problem could not be found.")
            return
        case = matches[0]
    else:
        sports = list(RATIONAL_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="ratnum_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in RATIONAL_CASES[sport]}
        chosen = st.selectbox("Scenario", list(labels), key="ratnum_case")
        case = labels[chosen]

    case_id = clean_filename(f"{sport}_{case['title']}")
    correct = float(case["answer"])

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 · Predict the sign")
    sign_options = ["Positive", "Negative", "Zero"]
    sign_key = f"ratnum_sign_order_{case_id}"
    if sign_key not in st.session_state:
        shuffled = list(sign_options)
        random.shuffle(shuffled)
        st.session_state[sign_key] = shuffled

    sign_choice = st.radio(
        "Before calculating, should the answer be positive, negative, or zero?",
        st.session_state[sign_key],
        key=f"ratnum_sign_{case_id}"
    )
    expected_sign = "Positive" if correct > 0 else "Negative" if correct < 0 else "Zero"

    if st.button("Check My Sign", key=f"ratnum_sign_check_{case_id}", use_container_width=True):
        if sign_choice == expected_sign:
            st.success("✅ Correct.")
        else:
            st.info("Think about whether the situation ends above, below, or exactly at zero.")

    st.markdown("### Step 2 · Write the numerical expression")
    # Build distractors that are mathematically different from the correct expression.
    # Do NOT include equivalent rewrites such as 3 + (-5) and 3 - 5 as separate choices.
    correct_expr = case["expression"]

    if "+ (-" in correct_expr:
        # Example correct form: 3 + (-5)
        # Use sign/operation mistakes as distractors, not an equivalent subtraction form.
        left, right = correct_expr.split("+ (-", 1)
        right = right.replace(")", "").strip()
        expression_options = [
            correct_expr,
            f"{left.strip()} + {right}",
            f"-{left.strip()} + {right}",
            f"{right} - {left.strip()}",
        ]
    elif " - " in correct_expr:
        left, right = correct_expr.split(" - ", 1)
        expression_options = [
            correct_expr,
            f"{left} + {right}",
            f"{right} - {left}",
            f"-{left} - {right}",
        ]
    elif " + " in correct_expr:
        left, right = correct_expr.split(" + ", 1)
        expression_options = [
            correct_expr,
            f"{left} - {right}",
            f"{right} - {left}",
            f"-{left} + {right}",
        ]
    else:
        expression_options = [
            correct_expr,
            f"-({correct_expr})",
            f"{abs(correct)} + {abs(correct)}",
            f"{abs(correct)} - 0",
        ]

    # Remove accidental duplicates while preserving order.
    expression_options = list(dict.fromkeys(expression_options))
    expr_order_key = f"ratnum_expr_order_{case_id}"
    if expr_order_key not in st.session_state:
        shuffled = list(expression_options)
        random.shuffle(shuffled)
        st.session_state[expr_order_key] = shuffled

    expr_choice = st.radio(
        "Which expression matches the situation?",
        st.session_state[expr_order_key],
        key=f"ratnum_expr_{case_id}"
    )

    if st.button("Check My Expression", key=f"ratnum_expr_check_{case_id}", use_container_width=True):
        if expr_choice == case["expression"]:
            st.success("✅ Correct expression.")
        else:
            st.info("Match the direction of each change in the story to a positive or negative value.")

    st.markdown("### Step 3 · Calculate")
    raw = st.text_input(
        f"Answer in {case['unit']}",
        key=f"ratnum_answer_{case_id}",
        placeholder="Type your answer"
    )
    student = parse_student_number(raw)

    attempts_key = f"ratnum_attempts_{case_id}"
    if attempts_key not in st.session_state:
        st.session_state[attempts_key] = 0

    if st.button("Check My Answer", key=f"ratnum_answer_check_{case_id}", use_container_width=True):
        tolerance = 0.001 if abs(correct) < 1 else 0.05
        if student is not None and math.isclose(student, correct, abs_tol=tolerance):
            st.success(f"✅ Correct — {fmt(correct)} {case['unit']}.")
            st.session_state[attempts_key] = 0
        else:
            st.session_state[attempts_key] += 1
            if st.session_state[attempts_key] == 1:
                st.info(case["hint1"])
            else:
                st.warning(case["hint2"])

    st.markdown("### Step 4 · Interpret the answer")
    if correct < 0:
        context_options = [
            f"The result is negative, meaning the situation represents a decrease, loss, or value below the comparison point.",
            f"The result is positive, meaning the value increased.",
            "The sign does not matter in this situation."
        ]
        correct_context = context_options[0]
    elif correct > 0:
        context_options = [
            f"The result is positive, meaning the situation represents a gain, advantage, or value above the comparison point.",
            f"The result is negative, meaning the value decreased.",
            "The sign does not matter in this situation."
        ]
        correct_context = context_options[0]
    else:
        context_options = [
            "The result is zero, meaning there is no net difference.",
            "The result must be positive.",
            "The result must be negative."
        ]
        correct_context = context_options[0]

    context_order_key = f"ratnum_context_order_{case_id}"
    if context_order_key not in st.session_state:
        shuffled = list(context_options)
        random.shuffle(shuffled)
        st.session_state[context_order_key] = shuffled

    context_choice = st.radio(
        "Which interpretation fits best?",
        st.session_state[context_order_key],
        key=f"ratnum_context_{case_id}"
    )

    if st.button("Check My Interpretation", key=f"ratnum_context_check_{case_id}", use_container_width=True):
        if context_choice == correct_context:
            st.success("✅ Correct.")
        else:
            st.info("Connect the sign of your answer back to the sports situation.")

    st.markdown("### Final · Explain it in your own words")
    st.text_area(
        "Explain what the positive or negative answer means in this situation.",
        key=f"ratnum_reasoning_{case_id}",
        placeholder="Use the sports context in your explanation."
    )

# =========================================================
# 7TH GRADE MATH LAB — GEOMETRY
# =========================================================
GEOMETRY_CASES = {
    "NFL": [
        {"title":"Midfield Logo Circle","kind":"Circle Area","story":"A circular midfield logo has a radius of 8 yards.","question":"What is the area of the logo?","shape":"circle_area","a":8,"answer":math.pi*8**2,"unit":"square yards"},
        {"title":"Practice Ring","kind":"Circumference","story":"A circular agility ring has a diameter of 12 feet.","question":"What is its circumference?","shape":"circumference_d","a":12,"answer":math.pi*12,"unit":"feet"},
        {"title":"End-Zone Banner","kind":"Rectangle Area","story":"An end-zone banner is 18 feet long and 7 feet tall.","question":"What is the area of the banner?","shape":"rectangle","a":18,"b":7,"answer":126,"unit":"square feet"},
        {"title":"Equipment Box","kind":"Volume","story":"An equipment box is 4 feet long, 3 feet wide, and 2 feet high.","question":"What is its volume?","shape":"volume","a":4,"b":3,"c":2,"answer":24,"unit":"cubic feet"},
        {"title":"Play Diagram Scale","kind":"Scale Drawing","story":"On a play diagram, 1 inch represents 5 yards. A route measures 7 inches on the diagram.","question":"How long is the real route?","shape":"scale","a":5,"b":7,"answer":35,"unit":"yards"},
        {"title":"Sideline Angle","kind":"Angle Relationship","story":"Two adjacent angles form a straight line. One angle measures 68°.","question":"What is the other angle?","shape":"supplement","a":68,"answer":112,"unit":"degrees"},
    ],
    "NBA": [
        {"title":"Center-Court Circle","kind":"Circle Area","story":"A circular center-court design has a radius of 6 feet.","question":"What is the area of the circle?","shape":"circle_area","a":6,"answer":math.pi*6**2,"unit":"square feet"},
        {"title":"Training Hoop","kind":"Circumference","story":"A circular training target has a diameter of 3 feet.","question":"What is its circumference?","shape":"circumference_d","a":3,"answer":math.pi*3,"unit":"feet"},
        {"title":"Backboard Panel","kind":"Rectangle Area","story":"A practice panel is 6 feet wide and 4 feet tall.","question":"What is its area?","shape":"rectangle","a":6,"b":4,"answer":24,"unit":"square feet"},
        {"title":"Ball Storage Crate","kind":"Volume","story":"A basketball storage crate is 5 feet long, 2 feet wide, and 3 feet high.","question":"What is its volume?","shape":"volume","a":5,"b":2,"c":3,"answer":30,"unit":"cubic feet"},
        {"title":"Court Diagram Scale","kind":"Scale Drawing","story":"On a court diagram, 1 inch represents 8 feet. A passing lane is 4.5 inches long.","question":"How long is it on the real court?","shape":"scale","a":8,"b":4.5,"answer":36,"unit":"feet"},
        {"title":"Passing Angle","kind":"Angle Relationship","story":"Two angles are complementary. One angle is 37°.","question":"What is the other angle?","shape":"complement","a":37,"answer":53,"unit":"degrees"},
    ],
    "MLB": [
        {"title":"On-Deck Circle","kind":"Circle Area","story":"An on-deck training circle has a radius of 5 feet.","question":"What is its area?","shape":"circle_area","a":5,"answer":math.pi*5**2,"unit":"square feet"},
        {"title":"Batting Circle Edge","kind":"Circumference","story":"A circular batting-practice marker has a diameter of 10 feet.","question":"What is its circumference?","shape":"circumference_d","a":10,"answer":math.pi*10,"unit":"feet"},
        {"title":"Tarp Section","kind":"Rectangle Area","story":"A tarp section is 30 feet long and 18 feet wide.","question":"What is its area?","shape":"rectangle","a":30,"b":18,"answer":540,"unit":"square feet"},
        {"title":"Baseball Storage Bin","kind":"Volume","story":"A storage bin is 4 feet long, 2.5 feet wide, and 2 feet high.","question":"What is its volume?","shape":"volume","a":4,"b":2.5,"c":2,"answer":20,"unit":"cubic feet"},
        {"title":"Ballpark Map","kind":"Scale Drawing","story":"On a ballpark map, 1 inch represents 20 feet. A walkway measures 6 inches.","question":"How long is the real walkway?","shape":"scale","a":20,"b":6,"answer":120,"unit":"feet"},
        {"title":"Foul-Line Angle","kind":"Angle Relationship","story":"Two adjacent angles form a straight line. One angle is 74°.","question":"What is the other angle?","shape":"supplement","a":74,"answer":106,"unit":"degrees"},
    ],
    "NHL": [
        {"title":"Faceoff Circle","kind":"Circle Area","story":"A practice faceoff circle has a radius of 15 feet.","question":"What is its area?","shape":"circle_area","a":15,"answer":math.pi*15**2,"unit":"square feet"},
        {"title":"Goal-Crease Arc","kind":"Circumference","story":"A circular training marking has a diameter of 8 feet.","question":"What is its circumference?","shape":"circumference_d","a":8,"answer":math.pi*8,"unit":"feet"},
        {"title":"Rink Advertising Panel","kind":"Rectangle Area","story":"An advertising panel is 12 feet long and 3 feet tall.","question":"What is its area?","shape":"rectangle","a":12,"b":3,"answer":36,"unit":"square feet"},
        {"title":"Puck Storage Box","kind":"Volume","story":"A puck box is 3 feet long, 2 feet wide, and 1.5 feet high.","question":"What is its volume?","shape":"volume","a":3,"b":2,"c":1.5,"answer":9,"unit":"cubic feet"},
        {"title":"Rink Diagram Scale","kind":"Scale Drawing","story":"On a rink diagram, 1 inch represents 10 feet. A skating path measures 7.5 inches.","question":"How long is the real skating path?","shape":"scale","a":10,"b":7.5,"answer":75,"unit":"feet"},
        {"title":"Passing Lane Angle","kind":"Angle Relationship","story":"Two angles are complementary. One measures 42°.","question":"What is the other angle?","shape":"complement","a":42,"answer":48,"unit":"degrees"},
    ],
    "Soccer": [
        {"title":"Center Circle","kind":"Circle Area","story":"A circular training area has a radius of 10 yards.","question":"What is its area?","shape":"circle_area","a":10,"answer":math.pi*10**2,"unit":"square yards"},
        {"title":"Training Circle Border","kind":"Circumference","story":"A circular drill area has a diameter of 18 yards.","question":"What is its circumference?","shape":"circumference_d","a":18,"answer":math.pi*18,"unit":"yards"},
        {"title":"Goal Banner","kind":"Rectangle Area","story":"A banner behind the goal is 14 feet wide and 6 feet tall.","question":"What is its area?","shape":"rectangle","a":14,"b":6,"answer":84,"unit":"square feet"},
        {"title":"Equipment Crate","kind":"Volume","story":"A soccer equipment crate is 5 feet long, 3 feet wide, and 2 feet high.","question":"What is its volume?","shape":"volume","a":5,"b":3,"c":2,"answer":30,"unit":"cubic feet"},
        {"title":"Field Diagram Scale","kind":"Scale Drawing","story":"On a field diagram, 1 inch represents 12 yards. A run measures 5.5 inches.","question":"How long is the actual run?","shape":"scale","a":12,"b":5.5,"answer":66,"unit":"yards"},
        {"title":"Corner-Kick Angle","kind":"Angle Relationship","story":"Two adjacent angles form a straight line. One angle measures 63°.","question":"What is the other angle?","shape":"supplement","a":63,"answer":117,"unit":"degrees"},
    ],
    "Formula 1": [
        {"title":"Circular Test Pad","kind":"Circle Area","story":"A circular test pad has a radius of 20 meters.","question":"What is its area?","shape":"circle_area","a":20,"answer":math.pi*20**2,"unit":"square meters"},
        {"title":"Tire Training Ring","kind":"Circumference","story":"A circular training ring has a diameter of 2 meters.","question":"What is its circumference?","shape":"circumference_d","a":2,"answer":math.pi*2,"unit":"meters"},
        {"title":"Garage Floor Section","kind":"Rectangle Area","story":"A garage work area is 12 meters long and 8 meters wide.","question":"What is its area?","shape":"rectangle","a":12,"b":8,"answer":96,"unit":"square meters"},
        {"title":"Parts Container","kind":"Volume","story":"A parts container is 3 meters long, 2 meters wide, and 1.5 meters high.","question":"What is its volume?","shape":"volume","a":3,"b":2,"c":1.5,"answer":9,"unit":"cubic meters"},
        {"title":"Track Map Scale","kind":"Scale Drawing","story":"On a track map, 1 centimeter represents 200 meters. A straight measures 3.5 centimeters.","question":"How long is the real straight?","shape":"scale","a":200,"b":3.5,"answer":700,"unit":"meters"},
        {"title":"Turn Angle","kind":"Angle Relationship","story":"Two angles are complementary. One angle measures 28°.","question":"What is the other angle?","shape":"complement","a":28,"answer":62,"unit":"degrees"},
    ],
}

def geometry_tolerance(case):
    """Student-friendly tolerance, especially for circle calculations using pi."""
    answer = float(case["answer"])
    if case["shape"] in ("circle_area", "circumference_d"):
        # Accept common pi approximations, ordinary rounding, and minor calculator-entry differences.
        # About ±2% with an absolute floor of 0.5.
        return max(0.5, abs(answer) * 0.02)
    if abs(answer) < 10:
        return 0.1
    return max(0.25, abs(answer) * 0.005)

def geometry_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Geometry</div>', unsafe_allow_html=True)
    st.subheader("📐 Sports Geometry Lab")
    st.write(
        "Use sports spaces, equipment, diagrams, circles, angles, area, and volume to solve geometry problems."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    elif generated_sport and generated_title:
        sport = generated_sport
        matches = [c for c in GEOMETRY_CASES[sport] if c["title"] == generated_title]
        if not matches:
            st.error("The generated geometry problem could not be found.")
            return
        case = matches[0]
    else:
        sports = list(GEOMETRY_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="geo_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in GEOMETRY_CASES[sport]}
        selected = st.selectbox("Scenario", list(labels), key="geo_case")
        case = labels[selected]

    case_id = clean_filename(f"{sport}_{case['title']}")
    correct = float(case["answer"])

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 · Choose a plan")
    if case["shape"] == "circle_area":
        options = ["πr²", "2πr", "length × width", "πd"]
        correct_plan = "πr²"
    elif case["shape"] == "circumference_d":
        options = ["πd", "πr²", "length × width", "2r²"]
        correct_plan = "πd"
    elif case["shape"] == "rectangle":
        options = ["length × width", "2(length + width)", "πr²", "length + width"]
        correct_plan = "length × width"
    elif case["shape"] == "volume":
        options = ["length × width × height", "length × width", "2(length + width)", "base + height"]
        correct_plan = "length × width × height"
    elif case["shape"] == "scale":
        options = ["use the scale factor to multiply", "add the scale numbers", "subtract the scale numbers", "divide the real distance by itself"]
        correct_plan = "use the scale factor to multiply"
    elif case["shape"] == "supplement":
        options = ["subtract from 180°", "subtract from 90°", "double the angle", "divide the angle by 2"]
        correct_plan = "subtract from 180°"
    else:
        options = ["subtract from 90°", "subtract from 180°", "double the angle", "add 90°"]
        correct_plan = "subtract from 90°"

    order_key = f"geo_plan_order_{case_id}"
    if order_key not in st.session_state:
        shuffled = list(options)
        random.shuffle(shuffled)
        st.session_state[order_key] = shuffled

    plan = st.radio(
        "Which plan or formula fits this problem?",
        st.session_state[order_key],
        key=f"geo_plan_{case_id}"
    )

    if st.button("Check My Plan", key=f"geo_plan_check_{case_id}", use_container_width=True):
        if plan == correct_plan:
            st.success("✅ Correct plan.")
        else:
            if difficulty == "Guided":
                st.info("Think about what the question asks you to measure: around, inside, space, scale, or angle.")
            else:
                st.info("Try another plan.")

    st.markdown("### Step 2 · Calculate")
    if case["shape"] in ("circle_area", "circumference_d"):
        st.caption("For circle problems, answers using π, 3.14, 3.1416, or normal rounding are accepted within a reasonable range.")

    raw = st.text_input(
        f"Your answer ({case['unit']})",
        key=f"geo_answer_{case_id}",
        placeholder="Type your answer"
    )
    student = parse_student_number(raw)

    attempts_key = f"geo_attempts_{case_id}"
    if attempts_key not in st.session_state:
        st.session_state[attempts_key] = 0

    if st.button("Check My Answer", key=f"geo_answer_check_{case_id}", use_container_width=True):
        tol = geometry_tolerance(case)
        if student is not None and math.isclose(student, correct, abs_tol=tol):
            if case["shape"] in ("circle_area", "circumference_d"):
                st.success(f"✅ Correct — your rounded answer is within the accepted range. Using π gives about **{correct:.2f} {case['unit']}**.")
            else:
                st.success(f"✅ Correct — {fmt(correct)} {case['unit']}.")
            st.session_state[attempts_key] = 0
        else:
            st.session_state[attempts_key] += 1
            if st.session_state[attempts_key] == 1:
                if case["shape"] == "circle_area":
                    st.info("Area of a circle uses the radius twice: π × r × r.")
                elif case["shape"] == "circumference_d":
                    st.info("If you know the diameter, circumference can be found with π × diameter.")
                elif case["shape"] == "rectangle":
                    st.info("Think about how many square units cover the rectangle.")
                elif case["shape"] == "volume":
                    st.info("Volume measures three-dimensional space.")
                elif case["shape"] == "scale":
                    st.info("Use the amount represented by 1 unit on the drawing.")
                elif case["shape"] == "supplement":
                    st.info("Angles on a straight line total 180°.")
                else:
                    st.info("Complementary angles total 90°.")
            else:
                if case["shape"] == "circle_area":
                    st.warning(f"Use **π × {case['a']}²**. Using 3.14 or your calculator's π button is fine.")
                elif case["shape"] == "circumference_d":
                    st.warning(f"Use **π × {case['a']}**. Using 3.14 or your calculator's π button is fine.")
                elif case["shape"] == "rectangle":
                    st.warning(f"Use **{case['a']} × {case['b']}**.")
                elif case["shape"] == "volume":
                    st.warning(f"Use **{case['a']} × {case['b']} × {case['c']}**.")
                elif case["shape"] == "scale":
                    st.warning(f"Use **{case['a']} × {case['b']}**.")
                elif case["shape"] == "supplement":
                    st.warning(f"Use **180 − {case['a']}**.")
                else:
                    st.warning(f"Use **90 − {case['a']}**.")

    st.markdown("### Step 3 · Check the unit")
    if "square" in case["unit"]:
        unit_options = [case["unit"], case["unit"].replace("square ", ""), "cubic " + case["unit"].replace("square ", ""), "degrees"]
    elif "cubic" in case["unit"]:
        unit_options = [case["unit"], case["unit"].replace("cubic ", ""), "square " + case["unit"].replace("cubic ", ""), "degrees"]
    elif case["unit"] == "degrees":
        unit_options = ["degrees", "square degrees", "feet", "cubic degrees"]
    else:
        unit_options = [case["unit"], "square " + case["unit"], "cubic " + case["unit"], "degrees"]

    unit_options = list(dict.fromkeys(unit_options))
    unit_order_key = f"geo_unit_order_{case_id}"
    if unit_order_key not in st.session_state:
        shuffled = list(unit_options)
        random.shuffle(shuffled)
        st.session_state[unit_order_key] = shuffled

    unit_choice = st.radio(
        "Which unit belongs with your answer?",
        st.session_state[unit_order_key],
        key=f"geo_unit_{case_id}"
    )

    if st.button("Check My Unit", key=f"geo_unit_check_{case_id}", use_container_width=True):
        if unit_choice == case["unit"]:
            st.success("✅ Correct unit.")
        else:
            st.info("Think about whether you measured length, area, volume, or an angle.")

    st.markdown("### Final · Explain your reasoning")
    st.text_area(
        "Explain why your formula or strategy matched the sports situation.",
        key=f"geo_reasoning_{case_id}",
        placeholder="Explain your geometry thinking in your own words."
    )

# =========================================================
# 7TH GRADE MATH LAB — STATISTICS & SAMPLING
# =========================================================
STATISTICS_CASES = {
    "NFL": [
        {"title":"Fan Survey Sample","kind":"Sampling","mode":"sample","story":"A team surveys 24 randomly selected fans, and 15 say defense is the team's biggest strength.","sample":24,"success":15,"population":240,"question":"About how many fans in a group of 240 would you predict would give the same answer?"},
        {"title":"Biased Survey","kind":"Sampling Bias","mode":"bias","story":"A football team asks only members of its official fan club whether the team has the best offense in the league.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Two Game Samples","kind":"Compare Samples","mode":"compare_means","a":[24,27,21,30,28],"b":[18,22,20,19,21],"question":"Which sample has the higher mean scoring total?"},
        {"title":"Consistency Check","kind":"Spread","mode":"range","a":[17,20,21,19,23],"b":[10,18,24,28,20],"question":"Which sample is more consistent based on range?"},
        {"title":"Season Claim","kind":"Claim Check","mode":"claim","story":"A player scored 100+ rushing yards in 4 of 5 sampled games.","sample":5,"success":4,"question":"Does this sample support the claim that the player usually reaches 100 rushing yards?"},
        {"title":"Random Sample Method","kind":"Sampling Method","mode":"method","story":"A coach wants a fair sample of students' favorite NFL teams.","correct":"Randomly select students from the full class list","question":"Which method would be most representative?"}
    ],
    "NBA": [
        {"title":"Favorite Player Survey","kind":"Sampling","mode":"sample","story":"A school surveys 30 randomly selected students, and 18 choose the same favorite NBA player.","sample":30,"success":18,"population":300,"question":"About how many of 300 students would you predict would choose that player?"},
        {"title":"Student Section Bias","kind":"Sampling Bias","mode":"bias","story":"A basketball team asks only students sitting in the home student section whether home games are exciting.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Scoring Samples","kind":"Compare Samples","mode":"compare_means","a":[22,24,28,25,26],"b":[18,21,20,23,19],"question":"Which sample has the higher mean scoring total?"},
        {"title":"Scoring Consistency","kind":"Spread","mode":"range","a":[19,20,21,20,20],"b":[12,18,24,28,18],"question":"Which player is more consistent based on range?"},
        {"title":"Three-Point Claim","kind":"Claim Check","mode":"claim","story":"A player made at least 3 three-pointers in 8 of 10 sampled games.","sample":10,"success":8,"question":"Does this sample support the claim that the player usually makes at least 3 threes?"},
        {"title":"Fair Survey Method","kind":"Sampling Method","mode":"method","story":"A teacher wants a fair sample of students' favorite NBA teams.","correct":"Randomly select students from the entire grade","question":"Which method would be most representative?"}
    ],
    "MLB": [
        {"title":"Ballpark Food Survey","kind":"Sampling","mode":"sample","story":"A team surveys 20 randomly selected fans, and 13 prefer hot dogs over pizza.","sample":20,"success":13,"population":200,"question":"About how many of 200 fans would you predict would prefer hot dogs?"},
        {"title":"Season Ticket Bias","kind":"Sampling Bias","mode":"bias","story":"A baseball team surveys only season-ticket holders about whether ticket prices are affordable.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Hit Samples","kind":"Compare Samples","mode":"compare_means","a":[2,1,3,2,2],"b":[1,0,2,1,1],"question":"Which sample has the higher mean hits per game?"},
        {"title":"Pitching Consistency","kind":"Spread","mode":"range","a":[5,6,5,7,6],"b":[2,5,8,9,4],"question":"Which pitcher is more consistent based on range?"},
        {"title":"Hit Claim","kind":"Claim Check","mode":"claim","story":"A hitter recorded at least one hit in 9 of 12 sampled games.","sample":12,"success":9,"question":"Does this sample support the claim that the hitter usually gets a hit?"},
        {"title":"Fair Fan Sample","kind":"Sampling Method","mode":"method","story":"A team wants a fair sample of fans entering the stadium.","correct":"Select every 20th fan entering through several gates","question":"Which method would be most representative?"}
    ],
    "NHL": [
        {"title":"Favorite Jersey Survey","kind":"Sampling","mode":"sample","story":"A team surveys 25 randomly selected fans, and 16 prefer the alternate jersey.","sample":25,"success":16,"population":250,"question":"About how many of 250 fans would you predict would prefer it?"},
        {"title":"Supporters Club Bias","kind":"Sampling Bias","mode":"bias","story":"A hockey team asks only members of its supporters club whether the arena atmosphere is excellent.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Goal Samples","kind":"Compare Samples","mode":"compare_means","a":[3,4,2,5,3],"b":[1,2,2,3,2],"question":"Which sample has the higher mean goals?"},
        {"title":"Save Consistency","kind":"Spread","mode":"range","a":[28,30,29,31,30],"b":[20,25,34,36,24],"question":"Which goalie is more consistent based on range?"},
        {"title":"Save Claim","kind":"Claim Check","mode":"claim","story":"A goalie saved at least 90% of shots in 7 of 9 sampled games.","sample":9,"success":7,"question":"Does this sample support the claim that the goalie usually reaches a .900 save rate?"},
        {"title":"Fair Arena Sample","kind":"Sampling Method","mode":"method","story":"A team wants to know what all arena visitors think about concessions.","correct":"Randomly survey fans from different sections and price levels","question":"Which method would be most representative?"}
    ],
    "Soccer": [
        {"title":"Favorite Formation Survey","kind":"Sampling","mode":"sample","story":"A club surveys 40 randomly selected fans, and 26 prefer a 4-3-3 formation.","sample":40,"success":26,"population":400,"question":"About how many of 400 fans would you predict would prefer it?"},
        {"title":"Supporters Group Bias","kind":"Sampling Bias","mode":"bias","story":"A soccer club asks only members of one supporters group whether that group creates the best atmosphere.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Goal Samples","kind":"Compare Samples","mode":"compare_means","a":[2,3,1,4,2],"b":[1,1,2,2,1],"question":"Which sample has the higher mean goals?"},
        {"title":"Passing Consistency","kind":"Spread","mode":"range","a":[78,80,81,79,82],"b":[65,72,84,89,70],"question":"Which player is more consistent based on range?"},
        {"title":"Scoring Claim","kind":"Claim Check","mode":"claim","story":"A forward scored in 6 of 8 sampled matches.","sample":8,"success":6,"question":"Does this sample support the claim that the forward usually scores?"},
        {"title":"Fair Fan Sample","kind":"Sampling Method","mode":"method","story":"A club wants a fair sample of opinions from match-going fans.","correct":"Randomly select fans from multiple seating areas","question":"Which method would be most representative?"}
    ],
    "Formula 1": [
        {"title":"Favorite Driver Survey","kind":"Sampling","mode":"sample","story":"A race event surveys 30 randomly selected fans, and 21 choose the same favorite driver.","sample":30,"success":21,"population":300,"question":"About how many of 300 fans would you predict would choose that driver?"},
        {"title":"Team Fan Bias","kind":"Sampling Bias","mode":"bias","story":"A racing team asks only visitors to its own merchandise booth whether it is the most popular team.","correct":"Biased","question":"Is this sample likely representative or biased?"},
        {"title":"Points Samples","kind":"Compare Samples","mode":"compare_means","a":[18,22,20,25,21],"b":[12,16,15,17,14],"question":"Which sample has the higher mean points?"},
        {"title":"Lap Time Consistency","kind":"Spread","mode":"range","a":[91.2,91.5,91.3,91.4,91.2],"b":[90.8,91.1,92.0,92.4,91.0],"question":"Which driver is more consistent based on range?"},
        {"title":"Top-10 Claim","kind":"Claim Check","mode":"claim","story":"A driver finished in the top 10 in 9 of 12 sampled races.","sample":12,"success":9,"question":"Does this sample support the claim that the driver usually finishes in the top 10?"},
        {"title":"Fair Grandstand Sample","kind":"Sampling Method","mode":"method","story":"An event organizer wants a fair sample of spectators' opinions.","correct":"Randomly survey spectators from several grandstands and ticket levels","question":"Which method would be most representative?"}
    ],
}

def make_dynamic_statistics_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    mode = case["mode"]

    if mode == "sample":
        sample = random.choice([20,24,25,30,32,40,50])
        ratio = random.choice([0.4,0.5,0.6,0.65,0.7,0.75,0.8])
        success = max(1, round(sample*ratio))
        population = sample * random.choice([5,8,10,12])
        case["sample"] = sample
        case["success"] = success
        case["population"] = population
        case["story"] = f"In a random {sport} survey, {success} of {sample} people chose the same response."
        case["question"] = f"About how many people in a group of {population} would you predict would give that response?"
        case["answer"] = (success/sample)*population
    elif mode == "compare_means":
        base_a = random.randint(12,30)
        base_b = random.randint(8,25)
        while abs(base_a-base_b) < 4:
            base_b = random.randint(8,25)
        a = [base_a + random.randint(-3,3) for _ in range(5)]
        b = [base_b + random.randint(-3,3) for _ in range(5)]
        case["a"] = a
        case["b"] = b
    elif mode == "range":
        center = random.randint(15,35)
        a = [center-1, center, center+1, center, center+2]
        b = [center-random.randint(5,10), center-2, center+3, center+random.randint(6,12), center]
        random.shuffle(a); random.shuffle(b)
        case["a"] = a
        case["b"] = b
    elif mode == "claim":
        sample = random.choice([8,10,12,15,20])
        success = random.randint(max(1, sample//2), sample)
        case["sample"] = sample
        case["success"] = success
        case["story"] = f"In a random sample of {sample} {sport} events, the condition happened {success} times."
    case["dynamic_id"] = f"{mode}|{case.get('sample')}|{case.get('success')}|{case.get('a')}|{case.get('b')}"
    return case

def statistics_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Statistics & Sampling</div>', unsafe_allow_html=True)
    st.subheader("📊 Sports Statistics & Sampling Lab")
    st.write("Use samples, averages, spread, and sampling methods to decide what the data can reasonably tell you.")

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    else:
        sports = list(STATISTICS_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="stats_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in STATISTICS_CASES[sport]}
        selected = st.selectbox("Scenario", list(labels), key="stats_case")
        case = labels[selected]

    cid = clean_filename(f"{sport}_{case['title']}")
    mode = case["mode"]

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case.get('story','')}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    if mode == "sample":
        st.markdown("### Step 1 · Find the sample proportion")
        ratio_raw = st.text_input("Sample proportion or percent", key=f"stats_ratio_{cid}", placeholder="Example: 0.6 or 60")
        ratio_ans = parse_student_number(ratio_raw)
        true_prop = case["success"]/case["sample"]

        if st.button("Check Sample Proportion", key=f"stats_ratio_check_{cid}", use_container_width=True):
            ok = False
            if ratio_ans is not None:
                ok = math.isclose(ratio_ans, true_prop, abs_tol=0.01) or math.isclose(ratio_ans, true_prop*100, abs_tol=0.5)
            if ok:
                st.success(f"✅ Correct — about {true_prop:.2f}, or {true_prop*100:.1f}%.")
            else:
                st.info("Divide the number with the response by the sample size.")

        st.markdown("### Step 2 · Predict the larger population")
        pred_raw = st.text_input("Predicted number", key=f"stats_answer_{cid}", placeholder="Type your answer")
        pred = parse_student_number(pred_raw)
        true_pred = true_prop*case["population"]
        if st.button("Check My Prediction", key=f"stats_answer_check_{cid}", use_container_width=True):
            if pred is not None and math.isclose(pred,true_pred,abs_tol=max(1,0.03*true_pred)):
                st.success(f"✅ Reasonable prediction — about {true_pred:.0f}.")
            else:
                st.info("Use the sample proportion and apply it to the larger population.")

    elif mode == "bias":
        st.markdown("### Step 1 · Judge the sample")
        opts = ["Representative","Biased","Not enough information"]
        order_key=f"stats_bias_order_{cid}"
        if order_key not in st.session_state:
            vals=list(opts); random.shuffle(vals); st.session_state[order_key]=vals
        choice=st.radio("How would you classify the sample?",st.session_state[order_key],key=f"stats_bias_{cid}")
        if st.button("Check My Choice",key=f"stats_bias_check_{cid}",use_container_width=True):
            if choice==case["correct"]:
                st.success("✅ Correct.")
            else:
                st.info("Ask whether everyone in the population had a fair chance to be selected.")

    elif mode == "compare_means":
        st.markdown("### Step 1 · Compare two samples")
        st.write(f"**Sample A:** {case['a']}")
        st.write(f"**Sample B:** {case['b']}")
        mean_a=sum(case["a"])/len(case["a"]); mean_b=sum(case["b"])/len(case["b"])
        ans_a=st.text_input("Mean of Sample A",key=f"stats_mean_a_{cid}",placeholder="Type your answer")
        ans_b=st.text_input("Mean of Sample B",key=f"stats_mean_b_{cid}",placeholder="Type your answer")
        a_num=parse_student_number(ans_a); b_num=parse_student_number(ans_b)
        if st.button("Check Means",key=f"stats_means_check_{cid}",use_container_width=True):
            if a_num is not None and b_num is not None and math.isclose(a_num,mean_a,abs_tol=.1) and math.isclose(b_num,mean_b,abs_tol=.1):
                st.success("✅ Both means are correct.")
            else:
                st.info("Add each sample and divide by the number of values.")
        higher="A" if mean_a>mean_b else "B" if mean_b>mean_a else "Same"
        comp=st.radio("Which sample has the higher mean?",["A","B","Same"],horizontal=True,key=f"stats_compare_{cid}")
        if st.button("Check Comparison",key=f"stats_compare_check_{cid}",use_container_width=True):
            if comp==higher: st.success("✅ Correct.")
            else: st.info("Compare the two means you calculated.")

    elif mode == "range":
        st.markdown("### Step 1 · Compare spread")
        st.write(f"**Sample A:** {case['a']}")
        st.write(f"**Sample B:** {case['b']}")
        range_a=max(case["a"])-min(case["a"]); range_b=max(case["b"])-min(case["b"])
        ra=st.text_input("Range of Sample A",key=f"stats_range_a_{cid}",placeholder="Type your answer")
        rb=st.text_input("Range of Sample B",key=f"stats_range_b_{cid}",placeholder="Type your answer")
        ra_num=parse_student_number(ra); rb_num=parse_student_number(rb)
        if st.button("Check Ranges",key=f"stats_ranges_check_{cid}",use_container_width=True):
            if ra_num is not None and rb_num is not None and math.isclose(ra_num,range_a,abs_tol=.1) and math.isclose(rb_num,range_b,abs_tol=.1):
                st.success("✅ Both ranges are correct.")
            else:
                st.info("Range = maximum − minimum.")
        consistent="A" if range_a<range_b else "B" if range_b<range_a else "Same"
        comp=st.radio("Which sample is more consistent?",["A","B","Same"],horizontal=True,key=f"stats_consistent_{cid}")
        if st.button("Check Consistency",key=f"stats_consistent_check_{cid}",use_container_width=True):
            if comp==consistent: st.success("✅ Correct — smaller range means less spread.")
            else: st.info("The smaller range indicates more consistency.")

    elif mode == "claim":
        st.markdown("### Step 1 · Evaluate the claim")
        pct=case["success"]/case["sample"]
        answer=st.radio("What is the best conclusion?",[
            "The sample supports the claim, but it does not prove it for every event.",
            "The sample proves the claim will always be true.",
            "The sample tells us nothing at all."
        ],key=f"stats_claim_{cid}")
        if st.button("Check Claim",key=f"stats_claim_check_{cid}",use_container_width=True):
            if answer.startswith("The sample supports"):
                st.success(f"✅ Good reasoning. The condition occurred in about {pct*100:.1f}% of the sample.")
            else:
                st.info("A sample can provide evidence, but it does not guarantee every future result.")

    elif mode == "method":
        st.markdown("### Step 1 · Choose a sampling method")
        distractors=[
            case["correct"],
            "Ask only the easiest people to reach",
            "Ask only people who already agree",
            "Let volunteers decide whether to participate"
        ]
        order_key=f"stats_method_order_{cid}"
        if order_key not in st.session_state:
            vals=list(dict.fromkeys(distractors)); random.shuffle(vals); st.session_state[order_key]=vals
        choice=st.radio("Which method is best?",st.session_state[order_key],key=f"stats_method_{cid}")
        if st.button("Check Sampling Method",key=f"stats_method_check_{cid}",use_container_width=True):
            if choice==case["correct"]: st.success("✅ Correct.")
            else: st.info("A representative sample should give the full population a fair chance to be included.")

    st.markdown("### Final · Explain your reasoning")
    st.text_area(
        "Explain what the sample or statistics tell you — and what they do not guarantee.",
        key=f"stats_reasoning_{cid}",
        placeholder="Use the data in your explanation."
    )

# =========================================================
# 7TH GRADE MATH LAB — EXPRESSIONS & ALGEBRAIC REASONING
# =========================================================
EXPRESSION_CASES = {
    "NFL": [
        {"title":"Fantasy Scoring Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Quarterback Scoring","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Receiving Yard Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Practice Rep Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Touchdown Scoring Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Football Expression","kind":"Write Expression","mode":"write"},
    ],
    "NBA": [
        {"title":"Basketball Scoring Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Evaluate a Scoring Line","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Shot Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Quarter Scoring Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Equivalent Scoring Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Basketball Expression","kind":"Write Expression","mode":"write"},
    ],
    "MLB": [
        {"title":"Total Bases Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Evaluate a Hitting Line","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Hit Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Batting Practice Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Equivalent Total-Base Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Baseball Expression","kind":"Write Expression","mode":"write"},
    ],
    "NHL": [
        {"title":"Hockey Points Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Evaluate a Points Line","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Shot Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Shift Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Equivalent Goal Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Hockey Expression","kind":"Write Expression","mode":"write"},
    ],
    "Soccer": [
        {"title":"Table Points Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Evaluate League Points","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Passing Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Training Drill Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Equivalent Points Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Soccer Expression","kind":"Write Expression","mode":"write"},
    ],
    "Formula 1": [
        {"title":"Race Points Formula","kind":"Translate Expression","mode":"translate"},
        {"title":"Evaluate Championship Points","kind":"Evaluate Expression","mode":"evaluate"},
        {"title":"Lap Groups","kind":"Combine Like Terms","mode":"combine"},
        {"title":"Tire Set Groups","kind":"Distributive Property","mode":"distribute"},
        {"title":"Equivalent Lap Forms","kind":"Equivalent Expressions","mode":"equivalent"},
        {"title":"Write a Racing Expression","kind":"Write Expression","mode":"write"},
    ],
}

def normalize_expression_text(text):
    return (
        str(text).lower().replace(" ", "")
        .replace("*","").replace("×","")
        .replace("–","-").replace("—","-")
    )

def make_dynamic_expression_case(sport, template, previous=None):
    """Create algebra problems where the expression actually represents a sports quantity."""
    case = copy.deepcopy(template)
    mode = case["mode"]

    if sport == "NFL":
        if mode == "translate":
            td = random.randint(1,5)
            fg = random.randint(1,4)
            case.update({
                "story": f"A football team scores x touchdowns worth 6 points each and also makes {fg} field goals worth 3 points each.",
                "question": "Which expression represents the team's total points?",
                "correct": f"6x + {3*fg}",
                "variable_meaning": "x = number of touchdowns",
            })
        elif mode == "evaluate":
            x = random.randint(2,5)
            fixed = random.choice([3,6,9,12])
            case.update({
                "story": f"A quarterback earns 4 fantasy points for each passing touchdown, plus {fixed} other fantasy points.",
                "expression": f"4x + {fixed}", "x": x, "answer": 4*x+fixed,
                "question": f"If the quarterback throws {x} passing touchdowns, how many fantasy points does the expression give?",
                "variable_meaning": "x = passing touchdowns",
            })
        elif mode == "combine":
            a,b = random.randint(2,6), random.randint(2,6)
            case.update({
                "story": f"A receiver gains {a}x yards in one group of plays and {b}x yards in another group, plus 10 yards on one extra play.",
                "expression": f"{a}x + {b}x + 10",
                "correct": f"{a+b}x + 10",
                "question": "Simplify the expression for total receiving yards.",
                "variable_meaning": "x = a repeated yardage amount",
            })
        elif mode == "distribute":
            groups = random.randint(2,5); extra = random.randint(2,8)
            case.update({
                "story": f"A football drill has {groups} identical stations. At each station, a player completes x regular reps and {extra} bonus reps.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Rewrite the total number of reps using the distributive property.",
                "variable_meaning": "x = regular reps at each station",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(2,7)
            case.update({
                "story": f"A team runs {groups} identical practice blocks. Each block contains x normal plays and {extra} red-zone plays.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression gives the same total number of plays?",
                "variable_meaning": "x = normal plays in each block",
            })
        else:
            start = random.randint(20,60); per = random.randint(3,8)
            case.update({
                "story": f"A running back already has {start} rushing yards and then gains {per} yards on each of x carries.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the running back's total rushing yards.",
                "variable_meaning": "x = number of additional carries",
            })

    elif sport == "NBA":
        if mode == "translate":
            twos = random.randint(2,6)
            case.update({
                "story": f"A player makes x three-pointers worth 3 points each and also makes {twos} two-point baskets.",
                "question": "Which expression represents the player's total points from those shots?",
                "correct": f"3x + {2*twos}",
                "variable_meaning": "x = made three-pointers",
            })
        elif mode == "evaluate":
            x = random.randint(2,7); fixed = random.choice([4,6,8,10,12])
            case.update({
                "story": f"A player scores 3 points for each made three-pointer and already has {fixed} points from other shots.",
                "expression": f"3x + {fixed}", "x": x, "answer": 3*x+fixed,
                "question": f"If the player makes {x} three-pointers, what is the total score represented by the expression?",
                "variable_meaning": "x = made three-pointers",
            })
        elif mode == "combine":
            a,b = random.randint(2,5), random.randint(2,5)
            case.update({
                "story": f"A player scores {a}x points in one stretch and {b}x points in another, plus 6 free-throw points.",
                "expression": f"{a}x + {b}x + 6",
                "correct": f"{a+b}x + 6",
                "question": "Simplify the expression for total points.",
                "variable_meaning": "x = the same repeated scoring amount",
            })
        elif mode == "distribute":
            q = random.choice([2,3,4]); bonus = random.randint(2,6)
            case.update({
                "story": f"A team scores x regular points plus {bonus} bonus points in each of {q} equal scoring periods.",
                "expression": f"{q}(x + {bonus})",
                "correct": f"{q}x + {q*bonus}",
                "question": "Rewrite the total points using the distributive property.",
                "variable_meaning": "x = regular points per period",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(2,8)
            case.update({
                "story": f"A player repeats the same scoring drill {groups} times. Each drill gives x regular points plus {extra} bonus points.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression is equivalent to the total scoring expression?",
                "variable_meaning": "x = regular points in each drill",
            })
        else:
            start = random.randint(8,30); per = random.choice([2,3])
            shot_name = "two-point baskets" if per==2 else "three-pointers"
            case.update({
                "story": f"A player already has {start} points and then makes x {shot_name}, each worth {per} points.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the player's final point total.",
                "variable_meaning": f"x = number of additional {shot_name}",
            })

    elif sport == "MLB":
        if mode == "translate":
            doubles = random.randint(1,5)
            case.update({
                "story": f"A hitter records x singles worth 1 total base each and {doubles} doubles worth 2 total bases each.",
                "question": "Which expression represents the hitter's total bases from these hits?",
                "correct": f"x + {2*doubles}",
                "variable_meaning": "x = number of singles",
            })
        elif mode == "evaluate":
            x = random.randint(2,6); fixed = random.choice([2,4,6,8])
            case.update({
                "story": f"A hitter's simplified total-base model is 2x + {fixed}, where x is the number of doubles.",
                "expression": f"2x + {fixed}", "x": x, "answer": 2*x+fixed,
                "question": f"If the hitter has {x} doubles, how many total bases does the model give?",
                "variable_meaning": "x = doubles",
            })
        elif mode == "combine":
            a,b = random.randint(2,6), random.randint(2,6)
            case.update({
                "story": f"A hitter gets {a}x hits in one stretch and {b}x hits in another, plus 2 extra hits.",
                "expression": f"{a}x + {b}x + 2",
                "correct": f"{a+b}x + 2",
                "question": "Simplify the expression for total hits.",
                "variable_meaning": "x = the same repeated hit amount",
            })
        elif mode == "distribute":
            groups = random.randint(2,5); extra = random.randint(1,5)
            case.update({
                "story": f"A batting practice has {groups} rounds. In each round, a hitter takes x normal swings and {extra} bonus swings.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Rewrite the total swings using the distributive property.",
                "variable_meaning": "x = normal swings per round",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(1,6)
            case.update({
                "story": f"A pitcher completes {groups} bullpen sets. Each set contains x regular pitches and {extra} warm-up pitches.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression is equivalent to the total pitches?",
                "variable_meaning": "x = regular pitches per set",
            })
        else:
            start = random.randint(20,60); per = random.randint(3,10)
            case.update({
                "story": f"A pitcher has already thrown {start} pitches and then throws {per} pitches in each of x additional innings.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the total pitches thrown.",
                "variable_meaning": "x = additional innings",
            })

    elif sport == "NHL":
        if mode == "translate":
            assists = random.randint(2,8)
            case.update({
                "story": f"A hockey player has x goals and {assists} assists. A player's points equal goals plus assists.",
                "question": "Which expression represents the player's total points?",
                "correct": f"x + {assists}",
                "variable_meaning": "x = goals",
            })
        elif mode == "evaluate":
            x = random.randint(2,8); assists = random.randint(2,8)
            case.update({
                "story": f"A hockey player's point total is modeled by x + {assists}, where x is goals.",
                "expression": f"x + {assists}", "x": x, "answer": x+assists,
                "question": f"If the player scores {x} goals, how many total points does the model give?",
                "variable_meaning": "x = goals",
            })
        elif mode == "combine":
            a,b = random.randint(2,5), random.randint(2,5)
            case.update({
                "story": f"A player takes {a}x shots in one stretch and {b}x shots in another, plus 4 extra shots.",
                "expression": f"{a}x + {b}x + 4",
                "correct": f"{a+b}x + 4",
                "question": "Simplify the expression for total shots.",
                "variable_meaning": "x = repeated shot amount",
            })
        elif mode == "distribute":
            shifts = random.randint(2,5); extra = random.randint(1,5)
            case.update({
                "story": f"A player has {shifts} identical practice shifts. Each shift has x normal reps and {extra} bonus reps.",
                "expression": f"{shifts}(x + {extra})",
                "correct": f"{shifts}x + {shifts*extra}",
                "question": "Rewrite the total reps using the distributive property.",
                "variable_meaning": "x = normal reps per shift",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(1,5)
            case.update({
                "story": f"A team completes {groups} shooting stations. Each station has x regular shots and {extra} bonus shots.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression is equivalent to the total shots?",
                "variable_meaning": "x = regular shots per station",
            })
        else:
            start = random.randint(10,35); per = random.randint(2,6)
            case.update({
                "story": f"A goalie already has {start} saves and then makes {per} saves in each of x later periods or drill segments.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the goalie's total saves.",
                "variable_meaning": "x = later periods or drill segments",
            })

    elif sport == "Soccer":
        if mode == "translate":
            draws = random.randint(1,5)
            case.update({
                "story": f"A soccer club earns 3 points for each win and 1 point for each draw. The club has x wins and {draws} draws.",
                "question": "Which expression represents the club's table points?",
                "correct": f"3x + {draws}",
                "variable_meaning": "x = wins",
            })
        elif mode == "evaluate":
            x = random.randint(2,8); draws = random.randint(1,5)
            case.update({
                "story": f"A club's table points are modeled by 3x + {draws}, where x is wins.",
                "expression": f"3x + {draws}", "x": x, "answer": 3*x+draws,
                "question": f"If the club has {x} wins, how many table points does the model give?",
                "variable_meaning": "x = wins",
            })
        elif mode == "combine":
            a,b = random.randint(2,6), random.randint(2,6)
            case.update({
                "story": f"A midfielder completes {a}x passes in one phase and {b}x passes in another, plus 5 extra passes.",
                "expression": f"{a}x + {b}x + 5",
                "correct": f"{a+b}x + 5",
                "question": "Simplify the expression for total completed passes.",
                "variable_meaning": "x = repeated pass amount",
            })
        elif mode == "distribute":
            groups = random.randint(2,5); extra = random.randint(2,6)
            case.update({
                "story": f"A player completes {groups} identical drills. Each drill has x normal touches and {extra} bonus touches.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Rewrite the total touches using the distributive property.",
                "variable_meaning": "x = normal touches per drill",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(2,6)
            case.update({
                "story": f"A club runs {groups} training blocks. Each block contains x regular shots and {extra} penalty kicks.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression is equivalent to the total number of shots?",
                "variable_meaning": "x = regular shots per block",
            })
        else:
            start = random.randint(10,40); per = random.randint(3,8)
            case.update({
                "story": f"A midfielder already has {start} completed passes and then completes {per} passes in each of x later possessions.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the total completed passes.",
                "variable_meaning": "x = later possessions",
            })

    else:  # Formula 1
        if mode == "translate":
            bonus = random.randint(2,8)
            case.update({
                "story": f"A driver earns x points in each of 4 race segments in a classroom simulation, plus {bonus} bonus points.",
                "question": "Which expression represents the driver's total points?",
                "correct": f"4x + {bonus}",
                "variable_meaning": "x = points per race segment",
            })
        elif mode == "evaluate":
            x = random.randint(5,20); bonus = random.randint(2,10)
            case.update({
                "story": f"A classroom racing score is modeled by 4x + {bonus}.",
                "expression": f"4x + {bonus}", "x": x, "answer": 4*x+bonus,
                "question": f"If x = {x} points per segment, what total score does the model give?",
                "variable_meaning": "x = points per segment",
            })
        elif mode == "combine":
            a,b = random.randint(2,6), random.randint(2,6)
            case.update({
                "story": f"A driver completes {a}x laps in one stint and {b}x laps in another, plus 3 formation laps.",
                "expression": f"{a}x + {b}x + 3",
                "correct": f"{a+b}x + 3",
                "question": "Simplify the expression for total laps.",
                "variable_meaning": "x = repeated lap amount",
            })
        elif mode == "distribute":
            sets = random.randint(2,5); extra = random.randint(1,4)
            case.update({
                "story": f"A team prepares {sets} identical tire sets. Each set includes x standard checks and {extra} extra checks.",
                "expression": f"{sets}(x + {extra})",
                "correct": f"{sets}x + {sets*extra}",
                "question": "Rewrite the total checks using the distributive property.",
                "variable_meaning": "x = standard checks per tire set",
            })
        elif mode == "equivalent":
            groups = random.randint(2,5); extra = random.randint(1,5)
            case.update({
                "story": f"A driver runs {groups} equal practice stints. Each stint includes x timed laps and {extra} warm-up laps.",
                "expression": f"{groups}(x + {extra})",
                "correct": f"{groups}x + {groups*extra}",
                "question": "Which expression is equivalent to the total laps?",
                "variable_meaning": "x = timed laps per stint",
            })
        else:
            start = random.randint(10,30); per = random.randint(3,8)
            case.update({
                "story": f"A driver has completed {start} laps and then completes {per} laps in each of x additional stints.",
                "correct": f"{start} + {per}x",
                "question": "Write an expression for the total laps.",
                "variable_meaning": "x = additional stints",
            })

    case["dynamic_id"] = f"{sport}|{mode}|{case.get('correct')}|{case.get('expression')}|{case.get('x')}"
    return case

def expressions_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Expressions & Algebraic Reasoning</div>', unsafe_allow_html=True)
    st.subheader("🧠 Sports Expressions Lab")
    st.write(
        "Use algebra to represent real sports quantities — scoring, yards, total bases, points, passes, laps, and practice totals."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    else:
        sports = list(EXPRESSION_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="expr_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in EXPRESSION_CASES[sport]}
        selected = st.selectbox("Scenario", list(labels), key="expr_case")
        case = make_dynamic_expression_case(sport, labels[selected])

    cid = clean_filename(f"{sport}_{case['title']}")
    mode = case["mode"]

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case.get('story','')}</p>
      <p><b>What x means:</b> {case.get('variable_meaning','')}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    if mode in ("translate","equivalent","distribute"):
        correct = case["correct"]

        if mode == "translate":
            compact = normalize_expression_text(correct)
            if "+" in compact:
                left,right = compact.split("+",1)
                options = [
                    correct,
                    f"{right} + {left.replace('x','')}x" if "x" in left else f"{right}x + {left}",
                    correct.replace("+","-",1),
                    f"{left}{right}"
                ]
            else:
                options = [correct, f"2{correct}", f"{correct} + x", f"{correct} - x"]
        else:
            outer = int(case["expression"].split("(")[0])
            inner = int(case["expression"].split("+")[1].replace(")","").strip())
            options = [
                correct,
                f"{outer}x + {inner}",
                f"{outer+inner}x",
                f"{outer}x + {inner+outer}",
            ]

        options = list(dict.fromkeys(options))
        order_key=f"expr_order_{cid}"
        if order_key not in st.session_state:
            vals=list(options); random.shuffle(vals); st.session_state[order_key]=vals

        choice=st.radio("Choose the expression that matches the sports situation.",st.session_state[order_key],key=f"expr_choice_{cid}")
        if st.button("Check My Expression",key=f"expr_choice_check_{cid}",use_container_width=True):
            if normalize_expression_text(choice)==normalize_expression_text(correct):
                st.success("✅ Correct.")
            else:
                if difficulty=="Guided":
                    st.info(
                        f"Use the meaning of x: {case.get('variable_meaning','')}. "
                        "Match each part of the expression to the quantities in the sports situation."
                    )
                else:
                    st.info("Match each term to the sports quantities and try again.")

    elif mode == "write":
        raw=st.text_input("Your expression",key=f"expr_written_{cid}",placeholder="Write an algebraic expression")
        if st.button("Check My Expression",key=f"expr_written_check_{cid}",use_container_width=True):
            student=normalize_expression_text(raw)
            correct=normalize_expression_text(case["correct"])
            alt=""
            if "+" in correct:
                parts=correct.split("+")
                alt="+".join(reversed(parts))
            if student==correct or student==alt:
                st.success("✅ Correct.")
            else:
                if difficulty=="Guided":
                    st.info(
                        f"Remember: {case.get('variable_meaning','')}. "
                        "The fixed amount and the repeated amount should both appear."
                    )
                else:
                    st.info("Check how the variable connects to the sports quantity.")

    elif mode == "evaluate":
        st.markdown(f"### Sports formula: {case['expression']}")
        st.write(f"Here, {case.get('variable_meaning','x is the variable')}.")
        raw=st.text_input("Calculated sports total",key=f"expr_answer_{cid}",placeholder="Type your answer")
        ans=parse_student_number(raw)
        if st.button("Check My Value",key=f"expr_answer_check_{cid}",use_container_width=True):
            if ans is not None and math.isclose(ans,float(case["answer"]),abs_tol=.05):
                st.success(f"✅ Correct — the sports total is {fmt(float(case['answer']))}.")
            else:
                if difficulty=="Guided":
                    st.info(
                        f"Substitute x = {case['x']} into the sports formula first, "
                        "then calculate the total."
                    )
                else:
                    st.info("Check your substitution and arithmetic.")

    elif mode == "combine":
        st.markdown(f"### Sports expression: {case['expression']}")
        st.write(f"Here, {case.get('variable_meaning','x is the repeated sports amount')}.")
        raw=st.text_input("Simplified sports expression",key=f"expr_written_{cid}",placeholder="Simplify the expression")
        if st.button("Check My Simplified Expression",key=f"expr_written_check_{cid}",use_container_width=True):
            if normalize_expression_text(raw)==normalize_expression_text(case["correct"]):
                st.success("✅ Correct.")
            else:
                if difficulty=="Guided":
                    st.info("The x-terms represent the same type of sports quantity, so those coefficients can be combined.")
                else:
                    st.info("Check which terms describe the same quantity.")

    st.markdown("### Final · Explain the sports meaning")
    st.text_area(
        "Explain what each part of your expression represents in this sports situation.",
        key=f"expr_reasoning_{cid}",
        placeholder="Example: 3x represents three points for each made three-pointer..."
    )


# =========================================================
# 7TH GRADE MATH LAB — FRACTIONS & RATIONAL NUMBER OPERATIONS
# =========================================================
FRACTION_CASES = {
    "NFL": [
        {"title":"Completed Passes","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Practice Completion","kind":"Add Fractions","mode":"add"},
        {"title":"Drive Progress","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Game Plan Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Practice Time","kind":"Divide Fractions","mode":"divide"},
        {"title":"Fraction to Decimal","kind":"Convert Fraction","mode":"convert"},
    ],
    "NBA": [
        {"title":"Shots Made","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Workout Completion","kind":"Add Fractions","mode":"add"},
        {"title":"Game Time Remaining","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Shooting Drill Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Court Time","kind":"Divide Fractions","mode":"divide"},
        {"title":"Free-Throw Rate","kind":"Convert Fraction","mode":"convert"},
    ],
    "MLB": [
        {"title":"Hits in At-Bats","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Bullpen Work","kind":"Add Fractions","mode":"add"},
        {"title":"Innings Remaining","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Batting Practice Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Pitch Count","kind":"Divide Fractions","mode":"divide"},
        {"title":"Hit Rate Conversion","kind":"Convert Fraction","mode":"convert"},
    ],
    "NHL": [
        {"title":"Shots on Goal","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Practice Blocks","kind":"Add Fractions","mode":"add"},
        {"title":"Period Remaining","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Power-Play Drill Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Ice Time","kind":"Divide Fractions","mode":"divide"},
        {"title":"Save Rate Fraction","kind":"Convert Fraction","mode":"convert"},
    ],
    "Soccer": [
        {"title":"Passes Completed","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Training Session","kind":"Add Fractions","mode":"add"},
        {"title":"Match Time Remaining","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Shooting Drill Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Possession Time","kind":"Divide Fractions","mode":"divide"},
        {"title":"Passing Rate Conversion","kind":"Convert Fraction","mode":"convert"},
    ],
    "Formula 1": [
        {"title":"Laps Completed","kind":"Fraction of a Set","mode":"fraction_of"},
        {"title":"Practice Session","kind":"Add Fractions","mode":"add"},
        {"title":"Race Remaining","kind":"Subtract Fractions","mode":"subtract"},
        {"title":"Tire-Stint Portion","kind":"Multiply Fractions","mode":"multiply"},
        {"title":"Split Fuel Load","kind":"Divide Fractions","mode":"divide"},
        {"title":"Lap Fraction Conversion","kind":"Convert Fraction","mode":"convert"},
    ],
}

def _fraction_text(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"

def _parse_fraction_answer(text):
    """Accept fractions, mixed numbers, decimals, or whole numbers."""
    raw = str(text).strip().replace(" ", "")
    if not raw:
        return None

    # Mixed number forms like 1 1/2 become 11/2 after removing spaces,
    # so handle mixed number before stripping spaces in a second pass.
    original = str(text).strip()
    try:
        if " " in original and "/" in original:
            whole, frac = original.split(None, 1)
            f = Fraction(frac)
            sign = -1 if whole.startswith("-") else 1
            w = abs(int(whole))
            return float(sign * (Fraction(w, 1) + f))
    except Exception:
        pass

    try:
        if "/" in raw:
            return float(Fraction(raw))
        return float(raw)
    except Exception:
        return None

def make_dynamic_fraction_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    mode = case["mode"]

    if mode == "fraction_of":
        denominator = random.choice([4,5,6,8,10,12])
        numerator = random.randint(1, denominator-1)
        total = denominator * random.choice([3,4,5,6,8,10])
        answer = Fraction(numerator, denominator) * total

        noun = {
            "NFL":"passes",
            "NBA":"shots",
            "MLB":"at-bats",
            "NHL":"shots",
            "Soccer":"passes",
            "Formula 1":"laps",
        }[sport]

        case.update({
            "story": f"A {sport} athlete completes {_fraction_text(Fraction(numerator,denominator))} of {total} {noun}.",
            "question": f"How many {noun} does that represent?",
            "fraction": Fraction(numerator,denominator),
            "total": total,
            "answer": float(answer),
            "unit": noun,
            "hint1": "Multiply the total amount by the fraction.",
            "hint2": f"{_fraction_text(Fraction(numerator,denominator))} × {total} = {float(answer):g}.",
        })

    elif mode == "add":
        d1 = random.choice([4,6,8,10,12])
        d2 = random.choice([4,6,8,10,12])
        n1 = random.randint(1,d1-1)
        n2 = random.randint(1,d2-1)
        f1 = Fraction(n1,d1)
        f2 = Fraction(n2,d2)
        answer = f1 + f2

        noun = {
            "NFL":"practice session",
            "NBA":"workout",
            "MLB":"bullpen session",
            "NHL":"practice",
            "Soccer":"training session",
            "Formula 1":"practice session",
        }[sport]

        case.update({
            "story": f"An athlete completes {_fraction_text(f1)} of a {noun} in one block and {_fraction_text(f2)} in another block.",
            "question": "What total fraction of the session was completed?",
            "f1": f1, "f2": f2, "answer": float(answer),
            "unit": "of the session",
            "hint1": "Find a common denominator before adding.",
            "hint2": f"{_fraction_text(f1)} + {_fraction_text(f2)} = {_fraction_text(answer)}.",
        })

    elif mode == "subtract":
        d = random.choice([4,5,6,8,10,12])
        start_num = random.randint(2,d)
        sub_num = random.randint(1,start_num-1)
        f1 = Fraction(start_num,d)
        f2 = Fraction(sub_num,d)
        answer = f1-f2

        context = {
            "NFL":"game plan completed",
            "NBA":"game time used",
            "MLB":"innings completed",
            "NHL":"period completed",
            "Soccer":"match time used",
            "Formula 1":"race completed",
        }[sport]

        case.update({
            "story": f"A team had {_fraction_text(f1)} of the {context}, then {_fraction_text(f2)} was removed from that amount.",
            "question": "What fraction remains?",
            "f1": f1, "f2": f2, "answer": float(answer),
            "unit": "remaining",
            "hint1": "Subtract the second fraction from the first.",
            "hint2": f"{_fraction_text(f1)} − {_fraction_text(f2)} = {_fraction_text(answer)}.",
        })

    elif mode == "multiply":
        f1 = Fraction(random.randint(1,4), random.choice([4,5,6,8]))
        f2 = Fraction(random.randint(1,4), random.choice([4,5,6,8]))
        answer = f1*f2

        context = {
            "NFL":"practice reps",
            "NBA":"shooting drill",
            "MLB":"batting-practice swings",
            "NHL":"power-play drill",
            "Soccer":"shooting drill",
            "Formula 1":"tire-stint plan",
        }[sport]

        case.update({
            "story": f"A coach uses {_fraction_text(f1)} of the full {context}, and then uses {_fraction_text(f2)} of that selected part.",
            "question": "What fraction of the full amount is actually used?",
            "f1": f1, "f2": f2, "answer": float(answer),
            "unit": "of the full amount",
            "hint1": "The word 'of' usually signals multiplication.",
            "hint2": f"{_fraction_text(f1)} × {_fraction_text(f2)} = {_fraction_text(answer)}.",
        })

    elif mode == "divide":
        # Choose values that often produce a simple quotient.
        divisor = Fraction(random.choice([1,2,3]), random.choice([2,3,4,5]))
        groups = random.randint(2,6)
        total = divisor * groups
        if total > 1:
            # Keep contexts easy to interpret as portions of a whole.
            divisor = Fraction(1, random.choice([3,4,5,6]))
            groups = random.randint(2, min(5, divisor.denominator))
            total = divisor * groups

        context = {
            "NFL":"practice time",
            "NBA":"court time",
            "MLB":"pitch-count budget",
            "NHL":"ice time",
            "Soccer":"possession time",
            "Formula 1":"fuel load",
        }[sport]

        case.update({
            "story": f"A team has {_fraction_text(total)} of its {context} available. Each equal segment uses {_fraction_text(divisor)} of the full amount.",
            "question": "How many equal segments can be made?",
            "f1": total, "f2": divisor, "answer": float(groups),
            "unit": "segments",
            "hint1": "Ask how many times the smaller fraction fits into the larger fraction.",
            "hint2": f"{_fraction_text(total)} ÷ {_fraction_text(divisor)} = {groups}.",
        })

    else:  # convert
        denominator = random.choice([4,5,8,10,20])
        numerator = random.randint(1,denominator-1)
        fr = Fraction(numerator,denominator)
        decimal = float(fr)

        context = {
            "NFL":"completion rate",
            "NBA":"shooting rate",
            "MLB":"hit rate",
            "NHL":"save rate",
            "Soccer":"passing rate",
            "Formula 1":"lap-completion rate",
        }[sport]

        case.update({
            "story": f"A {sport} {context} is {_fraction_text(fr)}.",
            "question": "Write this fraction as a decimal.",
            "fraction": fr, "answer": decimal,
            "unit": "decimal",
            "hint1": "A fraction bar means division.",
            "hint2": f"{fr.numerator} ÷ {fr.denominator} = {decimal:g}.",
        })

    case["dynamic_id"] = f"{sport}|{mode}|{case.get('f1')}|{case.get('f2')}|{case.get('fraction')}|{case.get('total')}|{case.get('answer')}"
    return case

def fractions_engine(sport_filter="Any Sport", difficulty="Guided", generated_sport=None, generated_title=None, generated_case=None):
    st.markdown('<div class="step">7th Grade Math Lab · Fractions & Rational Number Operations</div>', unsafe_allow_html=True)
    st.subheader("➗ Sports Fractions Lab")
    st.write(
        "Use fractions as real parts of sports totals, practice sessions, rates, and game situations."
    )

    if generated_case is not None and generated_sport:
        sport = generated_sport
        case = generated_case
    else:
        sports = list(FRACTION_CASES)
        if sport_filter != "Any Sport":
            sports = [sport_filter]
        sport = st.selectbox("Sport", sports, key="frac_sport")
        labels = {f"{c['kind']} · {c['title']}": c for c in FRACTION_CASES[sport]}
        selected = st.selectbox("Scenario", list(labels), key="frac_case")
        case = make_dynamic_fraction_case(sport, labels[selected])

    cid = clean_filename(f"{sport}_{case['title']}")
    correct = float(case["answer"])

    st.markdown(f"""
    <div class="card">
      <div class="step">{SPORT_ICONS.get(sport,'')} {sport} · {case['kind']}</div>
      <h2>{case['title']}</h2>
      <p><b>Situation:</b> {case['story']}</p>
      <p><b>Question:</b> {case['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Step 1 · Choose the operation")
    mode = case["mode"]
    correct_op = {
        "fraction_of":"Multiply",
        "add":"Add",
        "subtract":"Subtract",
        "multiply":"Multiply",
        "divide":"Divide",
        "convert":"Divide numerator by denominator",
    }[mode]

    choices = ["Add","Subtract","Multiply","Divide"]
    if mode == "convert":
        choices = [
            "Divide numerator by denominator",
            "Add numerator and denominator",
            "Multiply numerator and denominator",
            "Subtract denominator from numerator",
        ]

    order_key=f"frac_op_order_{cid}"
    if order_key not in st.session_state:
        vals=list(choices); random.shuffle(vals); st.session_state[order_key]=vals

    op = st.radio("What should you do first?", st.session_state[order_key], key=f"frac_op_{cid}")
    if st.button("Check My Plan", key=f"frac_op_check_{cid}", use_container_width=True):
        if op == correct_op:
            st.success("✅ Correct plan.")
        else:
            if difficulty == "Guided":
                st.info(case.get("hint1","Think about what the fractions represent."))
            else:
                st.info("Try another operation.")

    st.markdown("### Step 2 · Solve")
    if mode in ("add","subtract","multiply"):
        st.caption("You may enter a fraction, mixed number, or decimal.")
    elif mode == "divide":
        st.caption("Your final answer is the number of equal segments.")
    elif mode == "convert":
        st.caption("Enter the decimal equivalent.")
    else:
        st.caption("Enter the number represented by the fraction of the total.")

    raw = st.text_input(
        f"Your answer ({case['unit']})",
        key=f"frac_answer_{cid}",
        placeholder="Examples: 3/4, 1 1/2, 0.75, or 6"
    )
    ans = _parse_fraction_answer(raw)

    if st.button("Check My Answer", key=f"frac_answer_check_{cid}", use_container_width=True):
        tol = 0.01 if abs(correct) < 10 else max(0.1,abs(correct)*0.01)
        if ans is not None and math.isclose(ans,correct,abs_tol=tol):
            exact = Fraction(correct).limit_denominator(100)
            if mode in ("add","subtract","multiply"):
                st.success(f"✅ Correct — {_fraction_text(exact)} (about {correct:.3f} as a decimal).")
            else:
                st.success(f"✅ Correct — {fmt(correct)}.")
        else:
            if difficulty == "Guided":
                st.info(case.get("hint1","Check how the fractions are related."))
                st.caption(case.get("hint2",""))
            else:
                st.info("Check your fraction operation and try again.")

    st.markdown("### Step 3 · Interpret the result")
    if mode == "fraction_of":
        prompt = "What does your answer count in this sports situation?"
    elif mode == "convert":
        prompt = "What does this decimal represent as a rate?"
    elif mode == "divide":
        prompt = "What do the equal segments represent?"
    else:
        prompt = "What does your fraction tell you about the sports situation?"

    st.text_area(
        prompt,
        key=f"frac_reasoning_{cid}",
        placeholder="Explain your answer using the sports situation."
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
        ["Ratios, Rates & Proportions", "Equations & Inequalities", "Probability", "Percent & Percent Change", "Rational Numbers", "Geometry", "Statistics & Sampling", "Expressions & Algebraic Reasoning", "Fractions & Rational Number Operations", "Sports Math Challenge"],
        key="teacher_topic"
    )
    count = st.selectbox("Activities required", [1,2,3], key="teacher_count")
    sport_limit = st.selectbox("Allowed sport", ["Any Sport"] + list(RATE_CASES), key="teacher_sport")

    if assignment_type in ["Ratios, Rates & Proportions", "Equations & Inequalities", "Probability", "Percent & Percent Change", "Rational Numbers", "Geometry", "Statistics & Sampling", "Expressions & Algebraic Reasoning", "Fractions & Rational Number Operations"]:
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


# =========================================================
# DYNAMIC MATH LAB NUMBER GENERATOR
# Each generated question keeps a familiar sports template
# but creates fresh numbers so the practice bank does not
# "run out" after students cycle through the scenarios.
# =========================================================

SPORT_CONTEXT = {
    "NFL": {
        "item": "yards", "attempt": "plays", "score": "points",
        "object": "football", "place": "field"
    },
    "NBA": {
        "item": "points", "attempt": "shots", "score": "points",
        "object": "basketball", "place": "court"
    },
    "MLB": {
        "item": "runs", "attempt": "at-bats", "score": "runs",
        "object": "baseball", "place": "field"
    },
    "NHL": {
        "item": "shots", "attempt": "shot attempts", "score": "goals",
        "object": "puck", "place": "rink"
    },
    "Soccer": {
        "item": "goals", "attempt": "shots", "score": "goals",
        "object": "soccer ball", "place": "field"
    },
    "Formula 1": {
        "item": "points", "attempt": "races", "score": "points",
        "object": "race car", "place": "track"
    },
}

def _different_from_previous(value, previous_value):
    return previous_value is None or value != previous_value

def _clean_int(value):
    return int(round(float(value)))

def make_dynamic_ratio_case(sport, template, previous=None):
    """Fresh numbers for a ratio/rate/proportion template."""
    case = copy.deepcopy(template)
    denominator_label = case.get("denominator_label", "games")
    projection_label = case.get("projection_label", denominator_label)
    unit = case["unit"]
    total_label = case.get("total_label", case.get("label", "total"))

    # Build friendly exact/near-exact rates with varied denominators.
    den_choices = [6, 8, 10, 12, 15, 16, 18, 20, 24, 25, 30, 40, 50, 60, 75, 80, 90, 100]
    den = random.choice(den_choices)
    rate_choices = [0.4, 0.5, 0.6, 0.75, 0.8, 1.2, 1.5, 1.8, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20]
    rate = random.choice(rate_choices)
    total = round(den * rate, 2)

    # Avoid implausibly tiny/huge values for common sport units.
    if "yards" in unit and "carry" not in unit:
        den = random.choice([8, 10, 12, 16, 17])
        rate = random.choice([180, 220, 240, 260, 280, 300, 320])
        total = den * rate
    elif "yards per carry" in unit:
        den = random.choice([120, 150, 180, 200, 240, 280])
        rate = random.choice([3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
        total = round(den * rate, 1)
    elif "passes per minute" in unit:
        den = random.choice([60, 75, 90])
        rate = random.choice([0.4, 0.5, 0.6, 0.7, 0.8])
        total = round(den * rate)
    elif "points per race" in unit:
        den = random.choice([8, 10, 12, 15, 18, 20])
        rate = random.choice([8, 10, 12, 15, 18, 20, 22])
        total = den * rate

    target = random.choice([x for x in [10, 12, 15, 20, 24, 25, 30, 40, 50, 60, 75, 100, 120, 150, 200] if x != den])

    case["total"] = total
    case["games"] = den
    case["projection_games"] = target
    case["story"] = (
        f"In this {sport} practice scenario, there are **{fmt(float(total))} {total_label}** "
        f"over **{fmt(float(den))} {denominator_label}**."
    )
    case["dynamic_id"] = f"{total}|{den}|{target}"
    return case

def make_dynamic_equation_case(sport, template, previous=None):
    """Fresh equation/inequality numbers and multiple-choice models."""
    ctx = SPORT_CONTEXT[sport]
    case = copy.deepcopy(template)
    kind = case["kind"]

    if kind == "Inequality":
        subtype = random.choice(["at_least", "at_most", "cost"])
        if subtype == "at_least":
            start = random.randint(20, 90)
            needed = random.randint(8, 35)
            target = start + needed
            case.update({
                "story": f"A {sport} team already has {start} {ctx['score']}. It needs at least {target} {ctx['score']} to reach its goal.",
                "question": f"What is the minimum number of additional {ctx['score']} needed?",
                "models": [f"{start} + x ≥ {target}", f"{start} + x ≤ {target}", f"{start}x ≥ {target}", f"{target} + x ≥ {start}"],
                "correct_model": f"{start} + x ≥ {target}",
                "answer": needed,
                "unit": ctx["score"],
                "hint1": f"'At least {target}' means {target} or more.",
                "hint2": f"{target} − {start} = {needed}, so x must be at least {needed}.",
                "meaning": f"The team needs at least {needed} more {ctx['score']}."
            })
        elif subtype == "at_most":
            start = random.randint(10, 40)
            extra = random.randint(6, 25)
            maximum = start + extra
            case.update({
                "story": f"A player has already completed {start} {ctx['attempt']}. The limit is no more than {maximum}.",
                "question": f"What is the greatest number of additional {ctx['attempt']} allowed?",
                "models": [f"{start} + x ≤ {maximum}", f"{start} + x ≥ {maximum}", f"{start}x ≤ {maximum}", f"{maximum} + x ≤ {start}"],
                "correct_model": f"{start} + x ≤ {maximum}",
                "answer": extra,
                "unit": ctx["attempt"],
                "hint1": "'No more than' means the total must stay at or below the limit.",
                "hint2": f"{maximum} − {start} = {extra}.",
                "meaning": f"The player can complete at most {extra} more {ctx['attempt']}."
            })
        else:
            fixed = random.choice([40, 50, 60, 75, 80, 100, 120, 140])
            each = random.choice([5, 6, 8, 10, 12, 15, 20, 25])
            count = random.randint(3, 8)
            budget = fixed + each * count
            case.update({
                "story": f"A {sport} activity has a fixed cost of ${fixed}. Each participant costs ${each}. The total budget is ${budget}.",
                "question": "What is the greatest number of participants the budget can cover?",
                "models": [f"{fixed} + {each}x ≤ {budget}", f"{fixed} + {each}x ≥ {budget}", f"{each} + {fixed}x ≤ {budget}", f"{budget} + {each}x ≤ {fixed}"],
                "correct_model": f"{fixed} + {each}x ≤ {budget}",
                "answer": count,
                "unit": "participants",
                "hint1": "The total cost cannot exceed the budget.",
                "hint2": f"{budget} − {fixed} = {each*count}; then divide by {each}.",
                "meaning": f"The budget can cover at most {count} participants."
            })
    else:
        subtype = random.choice(["addition", "subtraction", "multiplication", "division", "two_step"])
        if subtype == "addition":
            start = random.randint(15, 80)
            x = random.randint(6, 30)
            target = start + x
            case.update({
                "story": f"A {sport} player has {start} {ctx['item']} and wants exactly {target}.",
                "question": f"How many more {ctx['item']} are needed?",
                "models": [f"{start} + x = {target}", f"{start} - x = {target}", f"{start}x = {target}", f"{target} + x = {start}"],
                "correct_model": f"{start} + x = {target}", "answer": x, "unit": ctx["item"],
                "hint1": f"What must be added to {start} to reach {target}?",
                "hint2": f"{target} − {start} = {x}.",
                "meaning": f"The player needs {x} more {ctx['item']}."
            })
        elif subtype == "subtraction":
            start = random.randint(20, 90)
            x = random.randint(5, min(25, start-1))
            end = start - x
            case.update({
                "story": f"A {sport} value starts at {start} and is reduced by x to finish at {end}.",
                "question": "How much was the value reduced?",
                "models": [f"{start} - x = {end}", f"{start} + x = {end}", f"{end} - x = {start}", f"{start}x = {end}"],
                "correct_model": f"{start} - x = {end}", "answer": x, "unit": ctx["item"],
                "hint1": "The starting value becomes smaller by x.",
                "hint2": f"{start} − x = {end}, so x = {x}.",
                "meaning": f"The value was reduced by {x} {ctx['item']}."
            })
        elif subtype == "multiplication":
            multiplier = random.randint(3, 9)
            x = random.randint(2, 14)
            total = multiplier * x
            case.update({
                "story": f"A {sport} drill has {multiplier} equal rounds. Each round has x successful results, for {total} total.",
                "question": "How many successful results are in each round?",
                "models": [f"{multiplier}x = {total}", f"x + {multiplier} = {total}", f"{total}x = {multiplier}", f"x - {multiplier} = {total}"],
                "correct_model": f"{multiplier}x = {total}", "answer": x, "unit": "results per round",
                "hint1": f"{multiplier} equal groups make a total of {total}.",
                "hint2": f"{multiplier}x = {total}; divide by {multiplier}.",
                "meaning": f"Each round has {x} successful results."
            })
        elif subtype == "division":
            groups = random.randint(3, 8)
            per = random.randint(3, 15)
            total = groups * per
            case.update({
                "story": f"A {sport} team divides {total} practice items equally among {groups} stations.",
                "question": "How many items go to each station?",
                "models": [f"x / {groups} = {per}", f"{groups}x = {total}", f"x + {groups} = {total}", f"{total} - x = {groups}"],
                "correct_model": f"{groups}x = {total}", "answer": per, "unit": "items per station",
                "hint1": f"There are {groups} equal groups totaling {total}.",
                "hint2": f"{groups}x = {total}; divide by {groups}.",
                "meaning": f"Each station gets {per} items."
            })
        else:
            start = random.randint(10, 60)
            each = random.choice([2, 3, 4, 5, 6, 7])
            x = random.randint(2, 9)
            target = start + each * x
            case.update({
                "story": f"A {sport} team starts with {start} {ctx['score']}. Each successful play adds {each} {ctx['score']}. The target is {target}.",
                "question": "How many successful plays are needed?",
                "models": [f"{start} + {each}x = {target}", f"{start} + x = {target}", f"{each}x = {target}", f"{target} + {each}x = {start}"],
                "correct_model": f"{start} + {each}x = {target}", "answer": x, "unit": "successful plays",
                "hint1": f"Start at {start}, then add {each} for each successful play.",
                "hint2": f"{start} + {each}x = {target}; subtract {start}, then divide by {each}.",
                "meaning": f"The team needs {x} successful plays."
            })

    case["dynamic_id"] = f"{case['correct_model']}|{case['answer']}"
    return case

def make_dynamic_probability_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    trials = random.choice([20, 24, 25, 30, 32, 36, 40, 50, 60, 75, 80, 90, 100])
    simple_fraction = random.choice([(1,2),(3,4),(2,5),(3,5),(4,5),(1,4),(3,10),(7,10),(9,10),(2,3),(5,6)])
    successes = round(trials * simple_fraction[0] / simple_fraction[1])
    # Make sure successes/trials is valid and useful.
    successes = max(1, min(trials-1, successes))
    future = random.choice([x for x in [40,50,60,75,80,100,120,150,200] if x != trials])
    case["successes"] = successes
    case["trials"] = trials
    case["future"] = future
    case["story"] = f"In a {sport} sample, **{successes} of {trials} {case['trial_label']}** resulted in **{case['event']}**."
    case["dynamic_id"] = f"{successes}|{trials}|{future}"
    return case

def make_dynamic_percent_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    kind = case["kind"]

    if kind == "Percent":
        whole = random.choice([20, 24, 25, 30, 32, 40, 50, 60, 75, 80, 100])
        pct = random.choice([20,25,30,40,50,60,70,75,80,90])
        part = whole * pct / 100
        if abs(part-round(part)) > 1e-9:
            # choose a clean whole for that percent
            whole = 100
            part = pct
        part = int(round(part))
        case.update({
            "part": part, "whole": whole, "answer": float(pct),
            "story": f"In a {sport} sample, {part} of {whole} attempts were successful.",
            "question": "What percent of the attempts were successful?",
            "hint1": "Use successful outcomes as the part and total attempts as the whole.",
            "hint2": f"{part} ÷ {whole} × 100 = {pct}%."
        })
    elif kind == "Percent Change":
        old = random.choice([20, 24, 25, 30, 40, 50, 60, 75, 80, 100, 120, 150, 200])
        pct = random.choice([10,20,25,30,40,50])
        direction = random.choice(["increase","decrease"])
        change = old * pct / 100
        new = old + change if direction == "increase" else old - change
        if abs(new-round(new)) < 1e-9:
            new = int(round(new))
        answer = pct if direction == "increase" else -pct
        case.update({
            "old": old, "new": new, "answer": float(answer), "direction": direction,
            "story": f"A {sport} statistic changes from {fmt(float(old))} to {fmt(float(new))}.",
            "question": "What was the percent change?",
            "hint1": "Find new − old, then compare that change with the original amount.",
            "hint2": f"{fmt(float(new))} − {fmt(float(old))} = {fmt(float(new-old))}; divide by {old} and multiply by 100."
        })
    elif kind == "Percent Of":
        pct = random.choice([10,12,15,20,25,30,35,40])
        base = random.choice([80,100,120,150,180,200,240,300,350,400,500,600])
        ans = base * pct / 100
        case.update({
            "percent": pct, "base": base, "answer": float(ans),
            "story": f"A {sport} fundraiser collects ${base}. **{pct}%** is set aside for the program.",
            "question": "How much money is set aside?",
            "unit": "dollars",
            "hint1": f"Find {pct}% of {base}.",
            "hint2": f"{pct/100:.2f} × {base} = {fmt(float(ans))}."
        })
    else:  # Discount
        pct = random.choice([10,15,20,25,30,35,40,50])
        base = random.choice([40,50,60,80,90,100,120,150,200])
        discount = base * pct / 100
        ans = base - discount
        case.update({
            "percent": pct, "base": base, "answer": float(ans),
            "story": f"A {sport} item costs ${base} and is discounted by **{pct}%**.",
            "question": "What is the sale price?",
            "unit": "dollars",
            "hint1": f"Find {pct}% of ${base}, then subtract the discount.",
            "hint2": f"{pct/100:.2f} × {base} = {fmt(float(discount))}; ${base} − ${fmt(float(discount))} = ${fmt(float(ans))}."
        })
    case["dynamic_id"] = f"{kind}|{case.get('answer')}"
    return case

def make_dynamic_rational_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    kind = case["kind"]

    # Preserve the mathematical flavor of the template, but refresh values.
    if "Decimal" in kind:
        a = round(random.uniform(1.5, 9.5), 1)
        delta = round(random.uniform(0.4, 3.5), 1)
        if "Addition" in kind:
            b = -delta
            answer = round(a + b, 1)
            expr = f"{a} + ({b})"
            story = f"A {sport} metric starts at +{a} and changes by {b}."
        else:
            new = round(a - delta, 1)
            answer = round(new - a, 1) if "Subtraction" in kind else round(abs(a-new),1)
            if "Difference" in kind:
                high, low = max(a,new), min(a,new)
                answer = round(high-low,1)
                expr = f"{high} - {low}"
                story = f"Two {sport} values are {high} and {low}."
            else:
                expr = f"{new} - {a}"
                story = f"A {sport} metric changes from {a} to {new}."
    elif "Addition" in kind:
        a = random.randint(3, 20)
        b = random.randint(a+1, a+15)
        answer = a - b
        expr = f"{a} + (-{b})"
        story = f"A {sport} team is at +{a}, then has a change of −{b}."
    elif "Difference" in kind and "Signed" not in kind:
        low = random.randint(3, 20)
        high = low + random.randint(2, 15)
        answer = high - low
        expr = f"{high} - {low}"
        story = f"Two {sport} values are {high} and {low}."
    else:
        scored = random.randint(1, 15)
        allowed = scored + random.randint(1, 10)
        answer = scored - allowed
        expr = f"{scored} - {allowed}"
        story = f"A {sport} team records {scored} for and {allowed} against."

    case["story"] = story
    case["expression"] = expr
    case["answer"] = answer
    case["question"] = "What is the resulting signed value or difference?"
    case["hint1"] = "Pay attention to which values represent gains and which represent losses."
    case["hint2"] = f"{expr} = {fmt(float(answer))}."
    case["dynamic_id"] = f"{expr}|{answer}"
    return case

def make_dynamic_geometry_case(sport, template, previous=None):
    case = copy.deepcopy(template)
    shape = case["shape"]
    place = SPORT_CONTEXT[sport]["place"]

    if shape == "circle_area":
        r = random.randint(3, 20)
        case.update({
            "a": r, "answer": math.pi*r*r,
            "story": f"A circular {sport} training area has a radius of {r} units.",
            "question": "What is the area of the circle?"
        })
    elif shape == "circumference_d":
        d = random.randint(4, 24)
        case.update({
            "a": d, "answer": math.pi*d,
            "story": f"A circular {sport} marker has a diameter of {d} units.",
            "question": "What is its circumference?"
        })
    elif shape == "rectangle":
        a = random.randint(5, 30); b = random.randint(3, 20)
        case.update({
            "a": a, "b": b, "answer": a*b,
            "story": f"A rectangular section of the {place} is {a} units by {b} units.",
            "question": "What is its area?"
        })
    elif shape == "volume":
        a = random.randint(2, 8); b = random.randint(2, 6); c = random.choice([1.5,2,2.5,3,4])
        case.update({
            "a": a, "b": b, "c": c, "answer": a*b*c,
            "story": f"A {sport} equipment box measures {a} units by {b} units by {c} units.",
            "question": "What is its volume?"
        })
    elif shape == "scale":
        scale = random.choice([5,8,10,12,15,20,25,50,100,200])
        drawing = random.choice([2.5,3,3.5,4,4.5,5,5.5,6,7,8])
        case.update({
            "a": scale, "b": drawing, "answer": scale*drawing,
            "story": f"On a {sport} diagram, 1 drawing unit represents {scale} real units. A route measures {drawing} drawing units.",
            "question": "How long is the route in real units?"
        })
    elif shape == "supplement":
        angle = random.randint(25, 155)
        case.update({
            "a": angle, "answer": 180-angle,
            "story": f"Two adjacent angles in a {sport} diagram form a straight line. One angle is {angle}°.",
            "question": "What is the other angle?"
        })
    else:
        angle = random.randint(15, 75)
        case.update({
            "a": angle, "answer": 90-angle,
            "story": f"Two angles in a {sport} diagram are complementary. One angle is {angle}°.",
            "question": "What is the other angle?"
        })
    case["dynamic_id"] = f"{shape}|{case.get('a')}|{case.get('b')}|{case.get('c')}"
    return case

def make_dynamic_math_case(topic, sport, template, previous_case=None):
    """Create a fresh numeric version of the selected question template."""
    if topic == "Ratios, Rates & Proportions":
        return make_dynamic_ratio_case(sport, template, previous_case)
    if topic == "Equations & Inequalities":
        return make_dynamic_equation_case(sport, template, previous_case)
    if topic == "Probability":
        return make_dynamic_probability_case(sport, template, previous_case)
    if topic == "Percent & Percent Change":
        return make_dynamic_percent_case(sport, template, previous_case)
    if topic == "Rational Numbers":
        return make_dynamic_rational_case(sport, template, previous_case)
    if topic == "Geometry":
        return make_dynamic_geometry_case(sport, template, previous_case)
    if topic == "Statistics & Sampling":
        return make_dynamic_statistics_case(sport, template, previous_case)
    if topic == "Expressions & Algebraic Reasoning":
        return make_dynamic_expression_case(sport, template, previous_case)
    if topic == "Fractions & Rational Number Operations":
        return make_dynamic_fraction_case(sport, template, previous_case)
    return copy.deepcopy(template)


def math_lab_case_id(generated):
    title = generated.get("title") or generated.get("athlete") or "Math_Lab"
    return clean_filename(f"{generated.get('sport','Sport')}_{title}")

def math_lab_final_reasoning(generated):
    """Read the final written response for the active Math Lab strand."""
    topic = generated.get("topic")
    cid = math_lab_case_id(generated)

    if topic == "Ratios, Rates & Proportions":
        return st.session_state.get("rate_explanation", "").strip()
    if topic == "Equations & Inequalities":
        return st.session_state.get(f"eq_reasoning_{cid}", "").strip()
    if topic == "Probability":
        return st.session_state.get(f"prob_reasoning_{cid}", "").strip()
    if topic == "Percent & Percent Change":
        return st.session_state.get(f"pct_reasoning_{cid}", "").strip()
    if topic == "Rational Numbers":
        return st.session_state.get(f"ratnum_reasoning_{cid}", "").strip()
    if topic == "Geometry":
        return st.session_state.get(f"geo_reasoning_{cid}", "").strip()
    if topic == "Statistics & Sampling":
        return st.session_state.get(f"stats_reasoning_{cid}", "").strip()
    if topic == "Expressions & Algebraic Reasoning":
        return st.session_state.get(f"expr_reasoning_{cid}", "").strip()
    if topic == "Fractions & Rational Number Operations":
        return st.session_state.get(f"frac_reasoning_{cid}", "").strip()
    return ""

def math_lab_answer_summary(generated):
    """Collect visible student work for the receipt."""
    topic = generated.get("topic")
    case = generated.get("case", {})
    cid = math_lab_case_id(generated)
    rows = []

    if topic == "Ratios, Rates & Proportions":
        rows = [
            ("Ratio", st.session_state.get("rate_ratio", "")),
            ("Unit rate", st.session_state.get("rate_unit_answer", "")),
            ("Proportion setup", st.session_state.get("rate_proportion_setup", "")),
            ("Prediction", st.session_state.get("rate_projection", "")),
            ("Proportional?", st.session_state.get("rate_proportional", "")),
            ("Explanation", st.session_state.get("rate_explanation", "")),
        ]
    elif topic == "Equations & Inequalities":
        rows = [
            ("Meaning of x", st.session_state.get(f"eq_unknown_{cid}", "")),
            ("Model", st.session_state.get(f"eq_model_{cid}", "")),
            ("Solution", st.session_state.get(f"eq_answer_{cid}", "")),
            ("Interpretation", st.session_state.get(f"eq_interpret_{cid}", "")),
            ("Reasoning", st.session_state.get(f"eq_reasoning_{cid}", "")),
        ]
    elif topic == "Probability":
        rows = [
            ("Probability ratio/fraction", st.session_state.get(f"prob_ratio_{cid}", "")),
            ("Decimal", st.session_state.get(f"prob_decimal_{cid}", "")),
            ("Percent", st.session_state.get(f"prob_percent_{cid}", "")),
            ("Prediction", st.session_state.get(f"prob_prediction_{cid}", "")),
            ("Reasoning", st.session_state.get(f"prob_reasoning_{cid}", "")),
        ]
    elif topic == "Percent & Percent Change":
        rows = [
            ("Plan", st.session_state.get(f"pct_model_{cid}", "")),
            ("Answer", st.session_state.get(f"pct_answer_{cid}", "")),
            ("Direction", st.session_state.get(f"pct_direction_{cid}", "")),
            ("Reasoning", st.session_state.get(f"pct_reasoning_{cid}", "")),
        ]
    elif topic == "Rational Numbers":
        rows = [
            ("Predicted sign", st.session_state.get(f"ratnum_sign_{cid}", "")),
            ("Expression", st.session_state.get(f"ratnum_expr_{cid}", "")),
            ("Answer", st.session_state.get(f"ratnum_answer_{cid}", "")),
            ("Interpretation", st.session_state.get(f"ratnum_context_{cid}", "")),
            ("Reasoning", st.session_state.get(f"ratnum_reasoning_{cid}", "")),
        ]
    elif topic == "Geometry":
        rows = [
            ("Plan", st.session_state.get(f"geo_plan_{cid}", "")),
            ("Answer", st.session_state.get(f"geo_answer_{cid}", "")),
            ("Unit", st.session_state.get(f"geo_unit_{cid}", "")),
            ("Reasoning", st.session_state.get(f"geo_reasoning_{cid}", "")),
        ]
    elif topic == "Statistics & Sampling":
        rows = [
            ("Sample proportion", st.session_state.get(f"stats_ratio_{cid}", "")),
            ("Prediction", st.session_state.get(f"stats_answer_{cid}", "")),
            ("Bias judgment", st.session_state.get(f"stats_bias_{cid}", "")),
            ("Mean A", st.session_state.get(f"stats_mean_a_{cid}", "")),
            ("Mean B", st.session_state.get(f"stats_mean_b_{cid}", "")),
            ("Mean comparison", st.session_state.get(f"stats_compare_{cid}", "")),
            ("Range A", st.session_state.get(f"stats_range_a_{cid}", "")),
            ("Range B", st.session_state.get(f"stats_range_b_{cid}", "")),
            ("Consistency", st.session_state.get(f"stats_consistent_{cid}", "")),
            ("Claim conclusion", st.session_state.get(f"stats_claim_{cid}", "")),
            ("Sampling method", st.session_state.get(f"stats_method_{cid}", "")),
            ("Reasoning", st.session_state.get(f"stats_reasoning_{cid}", "")),
        ]
    elif topic == "Expressions & Algebraic Reasoning":
        rows = [
            ("Selected expression", st.session_state.get(f"expr_choice_{cid}", "")),
            ("Written expression", st.session_state.get(f"expr_written_{cid}", "")),
            ("Evaluated value", st.session_state.get(f"expr_answer_{cid}", "")),
            ("Reasoning", st.session_state.get(f"expr_reasoning_{cid}", "")),
        ]
    elif topic == "Fractions & Rational Number Operations":
        rows = [
            ("Operation/plan", st.session_state.get(f"frac_op_{cid}", "")),
            ("Answer", st.session_state.get(f"frac_answer_{cid}", "")),
            ("Reasoning", st.session_state.get(f"frac_reasoning_{cid}", "")),
        ]

    return [(label, str(value)) for label, value in rows if str(value).strip()]

def math_lab_core_answer_correct(generated):
    """Check the main numerical work before allowing a completion receipt."""
    topic = generated.get("topic")
    case = generated.get("case", {})
    cid = math_lab_case_id(generated)

    try:
        if topic == "Ratios, Rates & Proportions":
            total = float(case["total"])
            games = float(case["games"])
            target = float(case["projection_games"])
            rate = parse_student_number(st.session_state.get("rate_unit_answer", ""))
            pred = parse_student_number(st.session_state.get("rate_projection", ""))
            true_rate = total / games
            true_pred = true_rate * target
            return (
                rate is not None
                and math.isclose(rate, true_rate, abs_tol=rate_tolerance(true_rate))
                and pred is not None
                and math.isclose(pred, true_pred, abs_tol=max(0.5, abs(true_pred) * 0.02))
            )

        if topic == "Equations & Inequalities":
            ans = parse_student_number(st.session_state.get(f"eq_answer_{cid}", ""))
            return ans is not None and math.isclose(ans, float(case["answer"]), abs_tol=0.1)

        if topic == "Probability":
            dec = parse_student_number(st.session_state.get(f"prob_decimal_{cid}", ""))
            pct = parse_student_number(st.session_state.get(f"prob_percent_{cid}", ""))
            pred = parse_student_number(st.session_state.get(f"prob_prediction_{cid}", ""))
            successes = float(case["successes"])
            trials = float(case["trials"])
            future = float(case["future"])
            true_dec = successes / trials
            true_pct = true_dec * 100
            true_pred = true_dec * future
            return (
                dec is not None and math.isclose(dec, true_dec, abs_tol=0.01)
                and pct is not None and math.isclose(pct, true_pct, abs_tol=0.5)
                and pred is not None and math.isclose(pred, true_pred, abs_tol=max(0.5, abs(true_pred) * 0.02))
            )

        if topic == "Percent & Percent Change":
            ans = parse_student_number(st.session_state.get(f"pct_answer_{cid}", ""))
            correct = float(case["answer"])
            return ans is not None and math.isclose(ans, correct, abs_tol=max(0.1, abs(correct) * 0.01))

        if topic == "Rational Numbers":
            ans = parse_student_number(st.session_state.get(f"ratnum_answer_{cid}", ""))
            correct = float(case["answer"])
            tol = 0.001 if abs(correct) < 1 else 0.05
            return ans is not None and math.isclose(ans, correct, abs_tol=tol)

        if topic == "Geometry":
            ans = parse_student_number(st.session_state.get(f"geo_answer_{cid}", ""))
            return ans is not None and math.isclose(
                ans,
                float(case["answer"]),
                abs_tol=geometry_tolerance(case)
            )

        if topic == "Statistics & Sampling":
            mode = case.get("mode")
            if mode == "sample":
                ans = parse_student_number(st.session_state.get(f"stats_answer_{cid}", ""))
                true_pred = (case["success"]/case["sample"])*case["population"]
                return ans is not None and math.isclose(ans,true_pred,abs_tol=max(1,0.03*true_pred))
            if mode == "bias":
                return st.session_state.get(f"stats_bias_{cid}") == case.get("correct")
            if mode == "compare_means":
                a = parse_student_number(st.session_state.get(f"stats_mean_a_{cid}", ""))
                b = parse_student_number(st.session_state.get(f"stats_mean_b_{cid}", ""))
                ma=sum(case["a"])/len(case["a"]); mb=sum(case["b"])/len(case["b"])
                higher="A" if ma>mb else "B" if mb>ma else "Same"
                return a is not None and b is not None and math.isclose(a,ma,abs_tol=.1) and math.isclose(b,mb,abs_tol=.1) and st.session_state.get(f"stats_compare_{cid}")==higher
            if mode == "range":
                a = parse_student_number(st.session_state.get(f"stats_range_a_{cid}", ""))
                b = parse_student_number(st.session_state.get(f"stats_range_b_{cid}", ""))
                ra=max(case["a"])-min(case["a"]); rb=max(case["b"])-min(case["b"])
                consistent="A" if ra<rb else "B" if rb<ra else "Same"
                return a is not None and b is not None and math.isclose(a,ra,abs_tol=.1) and math.isclose(b,rb,abs_tol=.1) and st.session_state.get(f"stats_consistent_{cid}")==consistent
            if mode == "claim":
                return str(st.session_state.get(f"stats_claim_{cid}","")).startswith("The sample supports")
            if mode == "method":
                return st.session_state.get(f"stats_method_{cid}")==case.get("correct")
            return False

        if topic == "Expressions & Algebraic Reasoning":
            mode = case.get("mode")
            if mode in ("translate","equivalent","distribute"):
                return normalize_expression_text(st.session_state.get(f"expr_choice_{cid}","")) == normalize_expression_text(case.get("correct",""))
            if mode in ("write","combine"):
                student = normalize_expression_text(st.session_state.get(f"expr_written_{cid}",""))
                correct = normalize_expression_text(case.get("correct",""))
                if mode == "write" and "+" in correct:
                    parts = correct.split("+")
                    alt = "+".join(reversed(parts))
                    return student == correct or student == alt
                return student == correct
            if mode == "evaluate":
                ans = parse_student_number(st.session_state.get(f"expr_answer_{cid}",""))
                return ans is not None and math.isclose(ans,float(case.get("answer",0)),abs_tol=.05)
            return False

        if topic == "Fractions & Rational Number Operations":
            ans = _parse_fraction_answer(st.session_state.get(f"frac_answer_{cid}",""))
            correct = float(case.get("answer",0))
            tol = 0.01 if abs(correct) < 10 else max(0.1, abs(correct)*0.01)
            return ans is not None and math.isclose(ans,correct,abs_tol=tol)
    except Exception:
        return False

    return False

def build_math_lab_receipt_pdf(student_name, class_period, generated, completion_id):
    """Create a compact PDF completion receipt for any Math Lab strand."""
    buffer = BytesIO()
    generated_time = datetime.now().strftime("%Y-%m-%d %H:%M")

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
        "MathLabReceiptTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=21,
        spaceAfter=8,
        textColor=colors.HexColor("#0F2747"),
    )
    heading = ParagraphStyle(
        "MathLabReceiptHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor("#173F73"),
    )
    body = ParagraphStyle(
        "MathLabReceiptBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        spaceAfter=4,
    )

    topic = generated.get("topic", "")
    sport = generated.get("sport", "")
    title = generated.get("title") or generated.get("athlete") or "Generated Practice"
    case = generated.get("case", {})
    story = case.get("story", "")
    question = case.get("question", "")

    def p(text):
        return Paragraph(html.escape(str(text)).replace("\n", "<br/>"), body)

    elements = [
        Paragraph("Sports by the Numbers · Math Lab Completion Receipt", title_style),
        p(f"Student: {student_name}"),
        p(f"Class Period: {class_period}"),
        p(f"Topic: {topic}"),
        p(f"Sport: {sport}"),
        p(f"Scenario: {title}"),
        p(f"Generated: {generated_time}"),
        p(f"Completion ID: {completion_id}"),
        Spacer(1, 8),
        Paragraph("Problem", heading),
        p(story),
    ]

    if question:
        elements.append(p(question))

    elements.append(Paragraph("Student Work", heading))
    for label, value in math_lab_answer_summary(generated):
        elements.append(p(f"{label}: {value}"))

    elements.extend([
        Paragraph("Completion Check", heading),
        p("The main numerical answer(s) were checked by the app before this receipt was unlocked."),
        p("Written reasoning was required for completion but was not automatically graded for quality."),
    ])

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def render_math_lab_submission(generated):
    """Unified finish/submit flow for every Math Lab strand."""
    if not generated:
        return

    st.markdown("---")
    st.markdown("## 🏁 Finish & Submit")
    st.write(
        "When your work is complete, submit it here to unlock your completion receipt."
    )

    cid = math_lab_case_id(generated)
    receipt_key = f"mathlab_submitted_{cid}_{generated.get('case',{}).get('dynamic_id','')}"
    completion_key = f"mathlab_completion_{cid}_{generated.get('case',{}).get('dynamic_id','')}"

    if st.button(
        "✅ Submit My Math Lab Work",
        key=f"mathlab_submit_button_{cid}_{generated.get('case',{}).get('dynamic_id','')}",
        use_container_width=True,
    ):
        missing = []

        student_name = st.session_state.get("math_student_name", "").strip()
        class_period = st.session_state.get("math_class_period", "").strip()
        reasoning = math_lab_final_reasoning(generated)

        if not student_name:
            missing.append("student name")
        if not class_period:
            missing.append("class period")
        if not math_lab_core_answer_correct(generated):
            missing.append("correct main calculation(s)")
        if len(reasoning) < 15:
            missing.append("final explanation/reasoning")

        if missing:
            st.session_state[receipt_key] = False
            st.warning("Before submitting, complete: " + ", ".join(missing) + ".")
        else:
            if completion_key not in st.session_state:
                st.session_state[completion_key] = uuid.uuid4().hex[:8].upper()
            st.session_state[receipt_key] = True

    if st.session_state.get(receipt_key, False):
        completion_id = st.session_state.get(completion_key, "")
        student_name = st.session_state.get("math_student_name", "").strip()
        class_period = st.session_state.get("math_class_period", "").strip()

        st.success(f"✅ Math Lab Complete · Completion ID: **{completion_id}**")
        st.write("Download your PDF receipt and submit it using your teacher's normal class submission method.")

        pdf_bytes = build_math_lab_receipt_pdf(
            student_name,
            class_period,
            generated,
            completion_id
        )

        title = generated.get("title") or generated.get("athlete") or "Math_Lab"
        filename = (
            f"Math_Lab_"
            f"{clean_filename(student_name)}_"
            f"{clean_filename(generated.get('topic','Topic'))}_"
            f"{clean_filename(title)}_"
            f"{completion_id}.pdf"
        )

        st.download_button(
            "📄 Download My Math Lab Completion Receipt",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            key=f"mathlab_download_{completion_id}",
            use_container_width=True,
        )

        st.caption(
            "The receipt includes the generated problem, the student's entered work, "
            "final reasoning, and a unique completion ID."
        )

if branch == "7th Grade Math Lab":
    st.markdown("""
    <div class="card">
      <div class="step">7th Grade Math Lab</div>
      <h2>Real sports. Real 7th-grade math.</h2>
      <p>Choose your topic, sport, and support level first. A question will not appear until you generate one.</p>
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

    valid_config = True

    if entry == "I Have an Assignment Code":
        code_in = st.text_input(
            "Assignment Code",
            key="student_assignment_code",
            placeholder="Paste code from your teacher"
        )
        valid_config = False
        if code_in.strip():
            decoded = decode_assignment(code_in)
            if decoded:
                if decoded.get("topic") == "Sports Math Challenge":
                    st.warning("That code belongs in the Sports Math Challenge branch.")
                else:
                    config.update(decoded)
                    valid_config = True
                    st.success(
                        f"Loaded: {config['topic']} · {config['count']} activity(ies) · "
                        f"{config['sport']} · {config['difficulty']}"
                    )
            else:
                st.error("That assignment code could not be read.")

    if entry == "Free Explore":
        st.markdown("### 1 · Choose your practice settings")
        s1, s2, s3 = st.columns(3)
        with s1:
            config["topic"] = st.selectbox(
                "Math topic",
                ["Ratios, Rates & Proportions", "Equations & Inequalities", "Probability", "Percent & Percent Change", "Rational Numbers", "Geometry", "Statistics & Sampling", "Expressions & Algebraic Reasoning", "Fractions & Rational Number Operations"],
                key="math_topic_select"
            )
        with s2:
            config["sport"] = st.selectbox(
                "Sport",
                ["Any Sport"] + list(RATE_CASES),
                key="math_sport_filter"
            )
        with s3:
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

    def generate_math_question():
        topic = config.get("topic")
        chosen_sport = config.get("sport", "Any Sport")
        actual_sport = chosen_sport
        if actual_sport == "Any Sport":
            actual_sport = random.choice(list(RATE_CASES))

        previous = st.session_state.get("math_generated_question")
        previous_case = previous.get("case") if previous else None

        # Pick a wording/template, avoiding the immediately previous template when possible.
        if topic == "Equations & Inequalities":
            options = EQUATION_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Probability":
            options = PROBABILITY_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Percent & Percent Change":
            options = PERCENT_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Rational Numbers":
            options = RATIONAL_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Geometry":
            options = GEOMETRY_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Statistics & Sampling":
            options = STATISTICS_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Expressions & Algebraic Reasoning":
            options = EXPRESSION_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        elif topic == "Fractions & Rational Number Operations":
            options = FRACTION_CASES[actual_sport]
            previous_title = previous.get("title") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [c for c in options if c["title"] != previous_title] or options
            template = random.choice(choices)
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "title": template["title"], "case": fresh_case
            }
        else:
            labels = list(RATE_CASES[actual_sport])
            previous_label = previous.get("athlete") if previous and previous.get("topic") == topic and previous.get("sport") == actual_sport else None
            choices = [label for label in labels if label != previous_label] or labels
            selected_label = random.choice(choices)
            template = RATE_CASES[actual_sport][selected_label]
            fresh_case = make_dynamic_math_case(topic, actual_sport, template, previous_case)
            generated = {
                "topic": topic, "sport": actual_sport,
                "difficulty": config.get("difficulty", "Guided"),
                "athlete": selected_label, "case": fresh_case
            }

        # Clear answer/check state from the prior Math Lab problem.
        clear_prefixes = (
            "rate_", "ratio_", "projection_",
            "eq_unknown_", "eq_model_", "eq_answer_", "eq_interpret_",
            "eq_reasoning_", "eq_model_attempts_", "eq_answer_attempts_",
            "eq_model_order_", "eq_interpret_order_",
            "prob_ratio_", "prob_decimal_", "prob_percent_", "prob_prediction_",
            "prob_reasoning_", "prob_ratio_attempts_",
            "pct_model_", "pct_model_order_", "pct_answer_", "pct_attempts_",
            "pct_direction_", "pct_reasoning_",
            "ratnum_sign_", "ratnum_sign_order_", "ratnum_expr_", "ratnum_expr_order_",
            "ratnum_answer_", "ratnum_attempts_", "ratnum_context_", "ratnum_context_order_",
            "ratnum_reasoning_",
            "geo_plan_", "geo_plan_order_", "geo_answer_", "geo_attempts_",
            "geo_unit_", "geo_unit_order_", "geo_reasoning_",
            "stats_ratio_", "stats_answer_", "stats_bias_", "stats_bias_order_",
            "stats_mean_a_", "stats_mean_b_", "stats_compare_", "stats_range_a_",
            "stats_range_b_", "stats_consistent_", "stats_claim_", "stats_method_",
            "stats_method_order_", "stats_reasoning_",
            "expr_order_", "expr_choice_", "expr_written_", "expr_answer_", "expr_reasoning_",
            "frac_op_order_", "frac_op_", "frac_answer_", "frac_reasoning_"
        )
        for key in list(st.session_state.keys()):
            if key.startswith(clear_prefixes):
                del st.session_state[key]

        st.session_state["math_generated_question"] = generated

    st.markdown("### 2 · Generate your question")
    st.caption("Each click creates fresh numbers. A familiar question type may return later, but the values will change.")
    if valid_config:
        button_label = (
            "🎲 Generate Question"
            if "math_generated_question" not in st.session_state
            else "🎲 Generate a New Question"
        )
        st.button(
            button_label,
            key="math_generate_question",
            use_container_width=True,
            on_click=generate_math_question
        )
    else:
        st.info("Enter a valid assignment code before generating a question.")

    generated = st.session_state.get("math_generated_question")

    # If the visible selections no longer match the generated question,
    # hide the old question until the student presses Generate again.
    if generated:
        selection_matches = (
            generated.get("topic") == config.get("topic")
            and generated.get("difficulty") == config.get("difficulty")
            and (
                config.get("sport") == "Any Sport"
                or generated.get("sport") == config.get("sport")
            )
        )
        if not selection_matches:
            st.session_state.pop("math_generated_question", None)
            generated = None
            st.info("Your settings changed. Press **Generate Question** to create a problem with the new choices.")

    if generated:
        st.markdown("---")
        st.markdown("### 3 · Work the generated question")
        if generated["topic"] == "Equations & Inequalities":
            equations_inequalities_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Probability":
            probability_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Percent & Percent Change":
            percent_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Rational Numbers":
            rational_numbers_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Geometry":
            geometry_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Statistics & Sampling":
            statistics_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Expressions & Algebraic Reasoning":
            expressions_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        elif generated["topic"] == "Fractions & Rational Number Operations":
            fractions_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_title=generated["title"],
                generated_case=generated.get("case")
            )
        else:
            ratios_rates_engine(
                generated["sport"],
                generated["difficulty"],
                generated_sport=generated["sport"],
                generated_athlete=generated["athlete"],
                generated_case=generated.get("case")
            )

        render_math_lab_submission(generated)
    else:
        st.caption("No practice question has been generated yet.")

    st.markdown("---")
    st.caption("7th Grade Math Lab · Ratios & Proportions · Equations & Inequalities · Probability · Percent & Percent Change · Rational Numbers · Geometry · Statistics & Sampling · Expressions & Algebraic Reasoning · Fractions & Rational Number Operations")
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
