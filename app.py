import streamlit as st
import random

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sports Data Investigator",
    page_icon="🔎",
    layout="wide"
)

# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

st.markdown("""
<style>

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
    margin-bottom: 24px;
}

.hero h1 {
    margin: 0;
    font-size: 42px;
}

.hero p {
    font-size: 18px;
    margin-top: 8px;
    color: #e5e7eb;
}

.challenge-box {
    padding: 24px;
    border-radius: 16px;
    border: 2px solid #d1d5db;
    margin-top: 15px;
    margin-bottom: 15px;
}

.mission {
    font-size: 21px;
    font-weight: 700;
}

.small-title {
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ATHLETE DATABASE
# Temporary database until live sports data is connected.
# ---------------------------------------------------------

ATHLETES = {

    "LeBron James": {
        "sport": "🏀 Basketball",
        "league": "NBA",
        "challenges": [
            {
                "type": "Change Over Time",
                "question":
                    "Has LeBron James become a better 3-point shooter "
                    "as his career has progressed?",
                "research": [
                    "Find his 3-point percentage from 3 early-career seasons.",
                    "Find his 3-point percentage from 3 middle-career seasons.",
                    "Find his 3-point percentage from 3 recent seasons."
                ],
                "thinking": [
                    "Do the percentages show a clear pattern?",
                    "Does one unusually high or low season affect your conclusion?",
                    "Is percentage more useful here than total 3-pointers made?"
                ]
            },

            {
                "type": "Consistency",
                "question":
                    "Has LeBron James been a consistent scorer "
                    "throughout his career?",
                "research": [
                    "Find points per game from at least 6 seasons.",
                    "Include seasons from different parts of his career.",
                    "Identify the highest and lowest values you found."
                ],
                "thinking": [
                    "How much do his scoring averages change?",
                    "What is the range of your selected values?",
                    "Would looking at more seasons strengthen your claim?"
                ]
            },

            {
                "type": "Rate vs. Total",
                "question":
                    "Which tells us more about LeBron James as a scorer: "
                    "total points or points per game?",
                "research": [
                    "Find total points from several seasons.",
                    "Find points per game from those same seasons.",
                    "Record how many games he played each season."
                ],
                "thinking": [
                    "How does games played affect a season total?",
                    "Can a player have a great scoring rate but a lower total?",
                    "Which statistic better answers your question?"
                ]
            }
        ]
    },

    "Aaron Judge": {
        "sport": "⚾ Baseball",
        "league": "MLB",
        "challenges": [
            {
                "type": "Relationship",
                "question":
                    "Does Aaron Judge hit more home runs mainly because "
                    "he plays more games?",
                "research": [
                    "Find games played for at least 5 seasons.",
                    "Find home runs for those same seasons.",
                    "Look for a season that does not fit the pattern."
                ],
                "thinking": [
                    "When games played increase, do home runs always increase?",
                    "Are there seasons that challenge the pattern?",
                    "What other statistic might help explain the results?"
                ]
            },

            {
                "type": "Rate vs. Total",
                "question":
                    "Is total home runs the fairest way to compare "
                    "Aaron Judge's seasons?",
                "research": [
                    "Find home runs from at least 5 seasons.",
                    "Find games played for those seasons.",
                    "Compare totals with a home-run rate."
                ],
                "thinking": [
                    "How does playing time affect totals?",
                    "Would a rate make the comparison fairer?",
                    "Does the season with the most home runs also have the best rate?"
                ]
            }
        ]
    },

    "Patrick Mahomes": {
        "sport": "🏈 Football",
        "league": "NFL",
        "challenges": [
            {
                "type": "Change Over Time",
                "question":
                    "Has Patrick Mahomes' passing production changed "
                    "as his career has progressed?",
                "research": [
                    "Find passing yards from at least 6 seasons.",
                    "Find passing touchdowns from those seasons.",
                    "Record games played for each season."
                ],
                "thinking": [
                    "Do passing yards and touchdowns show the same pattern?",
                    "Could games played affect the totals?",
                    "Would per-game statistics tell a different story?"
                ]
            }
        ]
    },

    "Connor McDavid": {
        "sport": "🏒 Hockey",
        "league": "NHL",
        "challenges": [
            {
                "type": "Relationship",
                "question":
                    "For Connor McDavid, do more goals usually lead "
                    "to more total points?",
                "research": [
                    "Find goals from at least 6 seasons.",
                    "Find assists from those same seasons.",
                    "Find total points from those seasons."
                ],
                "thinking": [
                    "Do goals and points always rise together?",
                    "How do assists affect total points?",
                    "Can you find a season that challenges the pattern?"
                ]
            }
        ]
    },

    "Lionel Messi": {
        "sport": "⚽ Soccer",
        "league": "Soccer",
        "challenges": [
            {
                "type": "Change Over Time",
                "question":
                    "How has Lionel Messi's goal-scoring rate changed "
                    "across different stages of his career?",
                "research": [
                    "Choose seasons from early, middle and later parts of his career.",
                    "Find goals for each selected season.",
                    "Find appearances or minutes played."
                ],
                "thinking": [
                    "Is total goals enough for a fair comparison?",
                    "Would goals per game or goals per 90 minutes be better?",
                    "Does changing leagues make the comparison more difficult?"
                ]
            }
        ]
    }
}


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

def get_challenge(athlete):
    return random.choice(ATHLETES[athlete]["challenges"])


def reset_investigation():
    for key in [
        "evidence_1",
        "evidence_2",
        "evidence_3",
        "claim"
    ]:
        if key in st.session_state:
            st.session_state[key] = ""


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "challenge" not in st.session_state:
    st.session_state.challenge = None

if "current_athlete" not in st.session_state:
    st.session_state.current_athlete = None


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="small-title">SPORTS BY THE NUMBERS</div>
    <h1>🔎 Sports Data Investigator</h1>
    <p>
        Choose an athlete. Investigate the numbers.
        Find evidence. Make a claim.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ATHLETE SEARCH
# ---------------------------------------------------------

st.subheader("🏆 Who do you want to investigate?")

athlete = st.selectbox(
    "Choose an athlete",
    list(ATHLETES.keys())
)

difficulty = st.radio(
    "Choose your challenge level",
    ["Starter", "Analyst", "Expert"],
    horizontal=True
)

col1, col2 = st.columns([1, 3])

with col1:

    if st.button(
        "🚀 BUILD MY CHALLENGE",
        type="primary",
        use_container_width=True
    ):

        st.session_state.current_athlete = athlete
        st.session_state.challenge = get_challenge(athlete)

        reset_investigation()

        st.rerun()


# ---------------------------------------------------------
# CHALLENGE
# ---------------------------------------------------------

if st.session_state.challenge:

    athlete_name = st.session_state.current_athlete
    athlete_info = ATHLETES[athlete_name]
    challenge = st.session_state.challenge

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown("### 🪪 Athlete File")

        st.markdown(
            f"""
            **{athlete_name}**

            {athlete_info["sport"]}

            **League:** {athlete_info["league"]}

            **Investigation:**  
            {challenge["type"]}

            **Difficulty:**  
            {difficulty}
            """
        )

    with col2:

        st.markdown("### 🕵️ Your Sports Data Challenge")

        st.markdown(
            f"""
            <div class="challenge-box">
                <div class="mission">
                    {challenge["question"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔄 Give Me Another Challenge"):

            st.session_state.challenge = get_challenge(athlete_name)

            reset_investigation()

            st.rerun()


    # -----------------------------------------------------
    # RESEARCH DIRECTIONS
    # -----------------------------------------------------

    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown("### 🔎 What should I research?")

        if difficulty == "Starter":

            for item in challenge["research"]:
                st.markdown(f"- {item}")

        elif difficulty == "Analyst":

            st.markdown(
                f"- {challenge['research'][0]}"
            )

            st.markdown(
                "- Choose at least **two additional statistics** "
                "that would help answer the question."
            )

            st.markdown(
                "- Be ready to explain why you chose them."
            )

        else:

            st.markdown(
                """
                You are the lead analyst.

                Decide:

                - What statistics should be researched?
                - How many seasons should be included?
                - What would make the comparison fair?
                """
            )


    with right:

        st.markdown("### 🧠 Think Like a Statistician")

        for item in challenge["thinking"]:
            st.markdown(f"- {item}")

        if difficulty == "Expert":

            st.markdown(
                "- What is one limitation of the data you collected?"
            )

            st.markdown(
                "- What additional evidence could challenge your claim?"
            )


    # -----------------------------------------------------
    # EVIDENCE
    # -----------------------------------------------------

    st.divider()

    st.markdown("## 🔐 Evidence Locker")

    st.caption(
        "Record actual statistics from your research. "
        "Numbers first. Claim second."
    )

    evidence_1 = st.text_area(
        "Evidence #1",
        placeholder="Example: 2012-13 — 40.6% from three",
        key="evidence_1"
    )

    evidence_2 = st.text_area(
        "Evidence #2",
        placeholder="Enter another statistic...",
        key="evidence_2"
    )

    evidence_3 = st.text_area(
        "Evidence #3",
        placeholder="Enter another statistic...",
        key="evidence_3"
    )


    # -----------------------------------------------------
    # CLAIM
    # -----------------------------------------------------

    st.divider()

    st.markdown("## 📣 Make Your Claim")

    if difficulty == "Starter":

        st.info(
            "Sentence starter: **Based on the data, I claim that...**"
        )

    elif difficulty == "Analyst":

        st.info(
            "Sentence starter: **My evidence suggests that... because...**"
        )

    else:

        st.info(
            "Write a defensible claim and support it with numerical evidence."
        )

    claim = st.text_area(
        "Your Claim",
        height=140,
        placeholder=(
            "Write your claim here. Use your evidence "
            "to explain what the numbers show."
        ),
        key="claim"
    )


    # -----------------------------------------------------
    # TEMPORARY COACH
    # -----------------------------------------------------

    st.divider()

    st.markdown("## 🤖 Sports Data Coach")

    st.caption(
        "For now this uses simple checks. "
        "Next we'll replace this with the real AI coach."
    )

    if st.button(
        "🏟️ ASK MY DATA COACH",
        type="primary"
    ):

        evidence_count = sum(
            bool(x.strip())
            for x in [
                evidence_1,
                evidence_2,
                evidence_3
            ]
        )

        if evidence_count < 2:

            st.warning(
                "You need more evidence before making a strong claim. "
                "Try finding at least two useful statistics."
            )

        elif len(claim.strip()) < 20:

            st.warning(
                "You've collected evidence, but your claim needs "
                "more explanation. What do your numbers actually show?"
            )

        else:

            st.success(
                "You have multiple pieces of evidence and a claim. "
                "Now ask yourself: Does every part of your claim match "
                "what your evidence actually proves?"
            )

            st.info(
                "💡 **Next step:** Look for one statistic that might "
                "challenge your conclusion. Does your claim still hold?"
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Sports Data Investigator • Sports by the Numbers"
)
