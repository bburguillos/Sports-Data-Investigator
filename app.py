import streamlit as st
import random
from openai import OpenAI

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Sports Data Investigator",
    page_icon="🔎",
    layout="wide"
)

# =========================================================
# OPENAI SETUP
# =========================================================

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    AI_AVAILABLE = True
except Exception:
    client = None
    AI_AVAILABLE = False

# =========================================================
# STYLING
# =========================================================

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

.coach-box {
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #374151;
    background-color: rgba(127, 127, 127, 0.08);
    margin-top: 15px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ATHLETE DATABASE
# Temporary until we connect live sports data.
# =========================================================

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


# =========================================================
# FUNCTIONS
# =========================================================

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

    st.session_state.coach_feedback = None


def ask_data_coach(
    athlete_name,
    sport,
    league,
    difficulty,
    challenge,
    evidence,
    claim,
    coach_mode="full"
):

    if not AI_AVAILABLE:
        return (
            "The Sports Data Coach is not connected yet. "
            "Please ask your teacher to check the app's AI settings."
        )

    evidence_text = "\n".join(
        [
            f"Evidence {i + 1}: {item}"
            for i, item in enumerate(evidence)
            if item.strip()
        ]
    )

    if not evidence_text:
        evidence_text = "The student has not entered evidence yet."

    if not claim.strip():
        claim_text = "The student has not written a claim yet."
    else:
        claim_text = claim

    if coach_mode == "hint":

        task_instruction = """
The student is asking for a RESEARCH HINT.

Do not provide statistics or answer the research question.

Give:
1. One short encouraging sentence.
2. One specific suggestion about the TYPE of statistic or comparison
   the student should research next.
3. One question for the student to think about.

Keep the entire response under 90 words.
"""

    elif coach_mode == "simple":

        task_instruction = """
The student wants the feedback explained more simply.

Explain what the student should do next using very simple
7th-grade language.

Do not provide the answer or write a claim for the student.

Keep the response under 90 words.
"""

    else:

        task_instruction = """
Evaluate the student's work as a sports statistics coach.

Your response must contain exactly these four sections:

### 🟢 What You're Doing Well
Identify ONE specific thing the student is doing well.

### 🟡 Look Closer
Identify ONE weakness, missing piece, unsupported conclusion,
or possible problem with the student's evidence or reasoning.

### 🔎 Your Next Move
Give ONE specific action the student should take next.
Do not provide the missing statistic or do the research for them.

### 🧠 Coach's Question
Ask ONE question that will make the student think more deeply
about the data.

Keep the response between 100 and 180 words.
"""

    teacher_instructions = """
You are the Sports Data Coach inside a middle-school statistics
course called Sports by the Numbers.

The students are approximately 7th grade.

Your job is to COACH statistical reasoning, not complete assignments.

IMPORTANT RULES:

- Never write the student's final claim for them.
- Never provide the research answer.
- Never invent statistics.
- Never pretend a statistic supplied by the student has been verified.
- Treat student-entered statistics as unverified evidence.
- If a statistic looks suspicious, tell the student to verify it
  using a reliable sports statistics source.
- Focus on whether the evidence is relevant to the research question.
- Help students notice trends, comparisons, outliers, rates,
  percentages, sample size, fairness, and limitations when appropriate.
- Challenge words such as "always," "never," "proves," or "definitely"
  when the evidence does not justify them.
- Distinguish association from causation when relevant.
- Use encouraging, age-appropriate language.
- Avoid complicated statistical vocabulary unless you explain it.
- Do not shame a student for an incorrect answer.
- Ask questions that cause the student to think.
- Do not give grades or numerical scores.
"""

    student_context = f"""
ATHLETE:
{athlete_name}

SPORT:
{sport}

LEAGUE:
{league}

CHALLENGE LEVEL:
{difficulty}

INVESTIGATION TYPE:
{challenge["type"]}

RESEARCH QUESTION:
{challenge["question"]}

STUDENT EVIDENCE:
{evidence_text}

STUDENT CLAIM:
{claim_text}

COACH REQUEST:
{task_instruction}
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=teacher_instructions,
            input=student_context,
            max_output_tokens=500
        )

        return response.output_text

    except Exception as error:

        return (
            "⚠️ The Sports Data Coach couldn't respond right now.\n\n"
            "Your work has not been lost. Try again in a moment.\n\n"
            f"Teacher note: {str(error)}"
        )


# =========================================================
# SESSION STATE
# =========================================================

if "challenge" not in st.session_state:
    st.session_state.challenge = None

if "current_athlete" not in st.session_state:
    st.session_state.current_athlete = None

if "coach_feedback" not in st.session_state:
    st.session_state.coach_feedback = None


# =========================================================
# HERO
# =========================================================

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


# =========================================================
# ATHLETE SEARCH
# =========================================================

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

if st.button(
    "🚀 BUILD MY CHALLENGE",
    type="primary",
    use_container_width=False
):

    st.session_state.current_athlete = athlete
    st.session_state.challenge = get_challenge(athlete)

    reset_investigation()

    st.rerun()


# =========================================================
# CHALLENGE
# =========================================================

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


    # =====================================================
    # RESEARCH DIRECTIONS
    # =====================================================

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

            st.markdown("""
You are the lead analyst.

Decide:

- What statistics should be researched?
- How many seasons should be included?
- What would make the comparison fair?
""")


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


    # =====================================================
    # EVIDENCE
    # =====================================================

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


    # =====================================================
    # CLAIM
    # =====================================================

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


    # =====================================================
    # REAL AI SPORTS DATA COACH
    # =====================================================

    st.divider()

    st.markdown("## 🤖 Sports Data Coach")

    st.write(
        "Your coach will read your **actual evidence and claim** "
        "and help you improve your statistical reasoning."
    )

    st.caption(
        "The coach will help you think — it will not write "
        "your final answer for you."
    )

    evidence_list = [
        evidence_1,
        evidence_2,
        evidence_3
    ]

    evidence_count = sum(
        bool(item.strip())
        for item in evidence_list
    )

    if not AI_AVAILABLE:

        st.error(
            "The AI coach is not connected. "
            "Ask your teacher to check the Streamlit secret."
        )

    coach_col1, coach_col2 = st.columns(2)

    with coach_col1:

        if st.button(
            "🏟️ ASK MY DATA COACH",
            type="primary",
            use_container_width=True
        ):

            if evidence_count < 2:

                st.session_state.coach_feedback = (
                    "### 🔎 Collect More Evidence\n\n"
                    "Before your coach evaluates your claim, find at least "
                    "**two pieces of numerical evidence** related to your "
                    "research question."
                )

            elif len(claim.strip()) < 15:

                st.session_state.coach_feedback = (
                    "### 📣 Make a Claim First\n\n"
                    "You have evidence. Now write what you think the "
                    "evidence shows. It does not have to be perfect — "
                    "your coach will help you improve it."
                )

            else:

                with st.spinner(
                    "Coach is studying your evidence..."
                ):

                    st.session_state.coach_feedback = ask_data_coach(
                        athlete_name=athlete_name,
                        sport=athlete_info["sport"],
                        league=athlete_info["league"],
                        difficulty=difficulty,
                        challenge=challenge,
                        evidence=evidence_list,
                        claim=claim,
                        coach_mode="full"
                    )

    with coach_col2:

        if st.button(
            "🔎 GIVE ME A RESEARCH HINT",
            use_container_width=True
        ):

            with st.spinner(
                "Coach is thinking of a useful hint..."
            ):

                st.session_state.coach_feedback = ask_data_coach(
                    athlete_name=athlete_name,
                    sport=athlete_info["sport"],
                    league=athlete_info["league"],
                    difficulty=difficulty,
                    challenge=challenge,
                    evidence=evidence_list,
                    claim=claim,
                    coach_mode="hint"
                )


    # =====================================================
    # DISPLAY AI FEEDBACK
    # =====================================================

    if st.session_state.coach_feedback:

        st.markdown("### 🧢 Coach's Feedback")

        st.markdown(
            st.session_state.coach_feedback
        )

        st.markdown("---")

        st.markdown(
            "**Don't just accept the feedback. "
            "Use it to improve your research or revise your claim.**"
        )

        if st.button(
            "💡 EXPLAIN THE FEEDBACK MORE SIMPLY"
        ):

            with st.spinner(
                "Coach is simplifying the feedback..."
            ):

                simple_feedback = ask_data_coach(
                    athlete_name=athlete_name,
                    sport=athlete_info["sport"],
                    league=athlete_info["league"],
                    difficulty=difficulty,
                    challenge=challenge,
                    evidence=evidence_list,
                    claim=claim,
                    coach_mode="simple"
                )

                st.session_state.coach_feedback = simple_feedback

                st.rerun()


    # =====================================================
    # STUDENT REMINDER
    # =====================================================

    st.divider()

    st.markdown("### 🏁 Before You Finish")

    st.checkbox(
        "My claim answers the research question."
    )

    st.checkbox(
        "I used numerical evidence."
    )

    st.checkbox(
        "My evidence actually supports my claim."
    )

    st.checkbox(
        "I checked that my statistics came from a reliable source."
    )

    st.checkbox(
        "I revised my work after reading my coach's feedback."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Sports Data Investigator • Sports by the Numbers"
)
