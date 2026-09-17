
import streamlit as st
import json
import math
from pathlib import Path

st.set_page_config(page_title="Sports by the Numbers", page_icon="📊", layout="wide")

DATA_FILE = Path(__file__).with_name("curated_data.json")

SPORT_ICONS = {
    "NFL":"🏈","NBA":"🏀","MLB":"⚾","NHL":"🏒","Soccer":"⚽","Formula 1":"🏎️"
}
MODE_ICONS = {
    "Percent Change":"📈",
    "MAD Consistency":"🎯",
    "Frequency Table":"📊"
}

st.markdown("""
<style>
.stApp {background:linear-gradient(180deg,#08111f,#111827);}
.main .block-container {max-width:1180px;padding-top:1.2rem;padding-bottom:4rem;}
h1,h2,h3 {color:#fff!important;}
.stMarkdown p,.stMarkdown li,[data-testid="stCaptionContainer"] p {color:#e5e7eb!important;}
div[data-testid="stSelectbox"] > label,
div[data-testid="stTextArea"] > label,
div[data-testid="stNumberInput"] > label,
div[data-testid="stRadio"] > label {color:#f8fafc!important;font-weight:700;}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
 background:#fff!important;color:#000!important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
 color:#000!important;fill:#000!important;
}
[role="listbox"],[role="option"] {background:#fff!important;color:#000!important;}
[role="option"] * {color:#000!important;}
[role="option"]:hover,[role="option"][aria-selected="true"] {background:#e5e7eb!important;color:#000!important;}
input,textarea {background:#fff!important;color:#111827!important;}
.hero,.card {
 background:rgba(255,255,255,.065);border:1px solid rgba(255,255,255,.12);
 border-radius:18px;padding:1.15rem 1.3rem;margin-bottom:1rem;
}
.step {color:#93c5fd;font-weight:900;text-transform:uppercase;letter-spacing:.06em;font-size:.88rem;}
.formula {background:#fff;color:#111827;border-radius:12px;padding:.8rem 1rem;font-weight:800;margin:.6rem 0 1rem;}
.score {font-size:3rem;font-weight:900;text-align:center;color:#fff;}
.small-note {color:#cbd5e1;font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_pack():
    if not DATA_FILE.exists():
        return None
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

pack = load_pack()
if not pack or "records" not in pack:
    st.error("curated_data.json is missing. Put it in the same GitHub folder as app.py.")
    st.stop()

records = pack["records"]

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
<p>50 curated athletes. Three focused math investigations. No live API and no AI required.</p>
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
