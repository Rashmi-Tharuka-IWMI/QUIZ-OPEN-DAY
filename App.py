import os
import random
import time
import streamlit as st

st.set_page_config(page_title="IWMI Open Day Challenge", layout="wide", initial_sidebar_state="collapsed")

# -----------------------------------------------------------------------------
# EDIT HERE: app title, timer, placeholder labels and final QR content
# -----------------------------------------------------------------------------
MAIN_TITLE = "IWMI Open Day Project Challenge"
TIME_LIMIT = 25  # seconds per question
QR_IMAGE_PATH = ""  # Optional: set to a local QR image path, e.g. "assets/surprise-qr.png"

PROJECTS = ["Project 1", "Project 2", "Project 3", "Project 4"]

# All wording is placeholder content. Replace these labels with your real questions later.
def make_question(level, project_index, kind):
    project = PROJECTS[project_index]
    problem_number = [2, 4, 1, 3][project_index]
    common = {
        "project": project,
        "q": f"Level {level} {project.lower().replace(' ', ' ')} Problem {problem_number}",
    }
    if kind == "yesno":
        # The first option is the correct-answer placeholder. When editing a real question,
        # replace it with the true answer (e.g. "No") and the second with the other option.
        options = ["Correct", "Wrong"]
        return {**common, "options": options, "answer": options[0]}
    if kind == "mcq":
        # Five placeholder choices, with one correct answer and four wrong answers.
        options = ["Correct", "Wrong", "Wrong", "Wrong", "Wrong"]
        random.shuffle(options)
        return {**common, "options": options, "answer": options.index("Correct")}
    options = [f"Statement {letter}" for letter in "ABCDE"]
    correct_count = random.randint(1, 4)
    correct_indices = set(random.sample(range(len(options)), correct_count))
    labels = ["Correct" if i in correct_indices else "Wrong" for i in range(len(options))]
    return {**common, "options": options, "labels": labels, "answer": correct_indices}

LEVELS = {
    1: {"name": "Yes or No", "type": "yesno", "pool": [(i, make_question(1, i, "yesno")) for i in range(len(PROJECTS))]},
    2: {"name": "Multiple Choice", "type": "mcq", "pool": [(i, make_question(2, i, "mcq")) for i in range(len(PROJECTS))]},
    3: {"name": "Statements", "type": "select", "pool": [(i, make_question(3, i, "select")) for i in range(len(PROJECTS))]},
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --violet:#9b5cff; --blue:#4e7bff; --cyan:#7ce7ff; --ink:#080519; --muted:#b7afd5; }
html, body, .stApp, button, p, div, input, label { font-family:'Inter',sans-serif; }
.stApp { color:#f7f3ff; background:radial-gradient(ellipse at 50% 42%, rgba(88,31,184,.24) 0%, transparent 38%), radial-gradient(ellipse at 15% 10%, rgba(35,62,160,.15), transparent 34%), #070416; }
.block-container { max-width:1120px !important; padding:1.2rem 4vw 3rem !important; }
#MainMenu, footer, header[data-testid='stHeader'] { visibility:hidden; }
.title { text-align:center; font-weight:600; font-size:clamp(2rem,4.7vw,3.7rem); line-height:1.12; letter-spacing:-.055em; background:linear-gradient(100deg,#fff 15%,#d7c6ff 52%,#8d9dff 90%); -webkit-background-clip:text; background-clip:text; color:transparent; margin:1.1rem 0 .65rem; }
.subtitle { text-align:center; color:#b9b1d1; font-size:1.08rem; margin:0 0 1.4rem; }
.announcement { display:table; margin:0 auto 1.1rem; border:1px solid rgba(178,132,255,.4); border-radius:999px; padding:.45rem 1rem; color:#d8c7ff; background:rgba(109,65,184,.12); font-size:.88rem; box-shadow:0 0 24px rgba(133,65,255,.1) inset; }
.panel { border:1px solid rgba(166,119,255,.25); border-radius:24px; padding:1.6rem; background:linear-gradient(145deg,rgba(30,20,62,.86),rgba(11,7,30,.9)); box-shadow:0 0 35px rgba(99,45,202,.13), inset 0 1px rgba(255,255,255,.04); margin:1rem 0; text-align:center; }
.eyebrow { color:#c8b0ff; border:1px solid rgba(177,128,255,.38); background:rgba(132,76,224,.13); border-radius:999px; display:inline-block; padding:.4rem .85rem; font-size:.88rem; }
.hint { color:#f5efff; font-size:clamp(1.6rem,3vw,2.45rem); font-weight:600; letter-spacing:-.04em; margin:.9rem 0 .3rem; }
.project, .project-label, .spin-project-label { display:none !important; }
.qbox { color:#faf7ff; font-weight:600; font-size:clamp(1.45rem,2.8vw,2.15rem); line-height:1.3; text-align:center; padding:1.7rem 1.4rem; margin:.6rem 0 1rem; border:1px solid rgba(170,119,255,.32); border-radius:22px; background:linear-gradient(130deg,rgba(94,51,161,.24),rgba(30,40,104,.18)); box-shadow:inset 0 0 28px rgba(132,67,255,.08),0 0 26px rgba(107,50,212,.08); }
.sub { text-align:center; color:#b7afd5; font-size:1rem; margin:.6rem 0; }
.tbar { height:7px; background:rgba(255,255,255,.1); border-radius:999px; overflow:hidden; margin:1rem 0 .45rem; }
.tbar > div { height:100%; background:linear-gradient(90deg,#4e7bff,#b25dff,#f2b9ff); border-radius:999px; box-shadow:0 0 14px #a34dff; transition:width 1s linear; }
.tsec { text-align:center; color:#cbb7ff; font-weight:600; margin-bottom:.6rem; }
.stButton, [data-testid='stElementContainer']:has(.stButton) { width:100% !important; }
[data-testid='stHorizontalBlock'] { gap:1rem; align-items:stretch; }
.stButton > button { width:100%; min-height:62px; border-radius:14px; border:1px solid rgba(166,123,255,.55); background:rgba(35,23,70,.78); color:#f7f3ff; transition:all .18s ease; }
.stButton > button p { font-size:1.05rem; font-weight:600; }
.st-key-next_participant_reset button { width:auto !important; min-height:34px !important; padding:.25rem .7rem !important; border-radius:9px !important; font-size:.72rem !important; opacity:.78; }
.st-key-next_participant_reset button p { font-size:.72rem !important; font-weight:500 !important; }
.stButton > button:hover { border-color:#d8aaff; background:rgba(92,52,160,.45); box-shadow:0 0 22px rgba(163,77,255,.22); transform:translateY(-2px); color:white; }
.stButton > button[kind='primary'], .stButton > button[data-testid='stBaseButton-primary'] { background:linear-gradient(105deg,#5633b8,#813bce); border:1px solid #bd8cff; color:white; box-shadow:0 0 22px rgba(127,60,224,.2); }
.stButton > button[kind='primary']:hover { background:linear-gradient(105deg,#6543cf,#9849e8); }
.reel-stage { width:100% !important; display:flex !important; justify-content:center !important; align-items:center !important; clear:both; margin:.65rem auto 1rem; }
.reel-window { --row-step:48px; height:calc(var(--row-step) * 4); overflow:hidden; position:relative; width:max-content; max-width:calc(100vw - 32px); margin:.45rem auto; padding:0 .25rem; -webkit-mask-image:linear-gradient(to bottom,transparent 0%,#000 12%,#000 88%,transparent 100%); mask-image:linear-gradient(to bottom,transparent 0%,#000 12%,#000 88%,transparent 100%); }
.reel-track { display:flex; flex-direction:column; align-items:stretch; gap:6px; width:max-content; min-width:0; animation:reelScroll var(--spin-duration,4.6s) cubic-bezier(.10,.72,.12,1) forwards; will-change:transform; }
.reel-stage .reel-row { display:block; flex:0 0 42px; box-sizing:border-box; width:max-content; min-width:210px; max-width:calc(100vw - 48px); height:42px; border:1px solid rgba(166,123,255,.28); border-radius:11px; padding:.55rem 1.8rem; margin:0 auto; text-align:center; white-space:nowrap; color:#b9afd5; font-size:1rem; line-height:1.25; opacity:.72; background:rgba(24,16,51,.72); }
.reel-stage .reel-row.cur { opacity:1; color:#fff; font-size:1.12rem; font-weight:700; border-color:#bd8cff; background:linear-gradient(100deg,rgba(79,66,174,.52),rgba(129,59,206,.45)); box-shadow:0 0 28px rgba(153,82,255,.32),inset 0 0 20px rgba(153,82,255,.14); }
@keyframes reelScroll { from { transform:translateY(0); } to { transform:translateY(var(--spin-distance)); } }
.st-key-next_participant_reset { position:fixed !important; left:50% !important; bottom:16px !important; transform:translateX(-50%) !important; z-index:10000 !important; display:flex !important; justify-content:center !important; align-items:center !important; width:max-content !important; max-width:calc(100vw - 24px) !important; margin:0 !important; padding:0 !important; }
.st-key-next_participant_reset button { width:auto !important; min-width:0 !important; max-width:260px !important; min-height:32px !important; padding:.2rem .7rem !important; border-radius:8px !important; font-size:.72rem !important; opacity:.75; white-space:nowrap !important; }
.st-key-next_participant_reset button p { font-size:.72rem !important; font-weight:500 !important; margin:0 !important; }
.reel.stop .cur { animation:reelPulse .55s ease 2; }
.confetti-layer { position:fixed; inset:0; overflow:hidden; pointer-events:none; z-index:9999; }
.confetti-layer i { position:absolute; top:-18px; width:7px; height:13px; border-radius:2px; animation:confettiFall linear infinite; box-shadow:0 0 8px currentColor; }
@keyframes reelPulse { 50% { transform:scale(1.035); box-shadow:0 0 34px rgba(174,95,255,.55); } }
@keyframes confettiFall { to { transform:translateY(112vh) rotate(760deg); } }
.result-mark { font-size:clamp(2rem,5vw,3.4rem); font-weight:700; letter-spacing:-.05em; background:linear-gradient(90deg,#fff,#d9baff,#8da5ff); -webkit-background-clip:text; background-clip:text; color:transparent; margin:.5rem 0; }
.winner { font-size:clamp(2rem,5vw,3.7rem); font-weight:700; letter-spacing:-.05em; text-align:center; background:linear-gradient(90deg,#fff,#d8b8ff,#8b9eff); -webkit-background-clip:text; background-clip:text; color:transparent; margin:1rem auto; }
.qr-box { width:min(270px,72vw); aspect-ratio:1/1; margin:1.2rem auto; border:1px dashed rgba(195,156,255,.8); border-radius:20px; display:flex; align-items:center; justify-content:center; padding:1rem; background:repeating-linear-gradient(135deg,rgba(123,76,198,.06),rgba(123,76,198,.06) 10px,rgba(34,24,67,.22) 10px,rgba(34,24,67,.22) 20px); color:#c8b5ef; text-align:center; }
.qr-caption { color:#e7dcff; font-size:1.2rem; font-weight:600; text-align:center; }
@media(max-width:640px){ .panel{padding:1.1rem;border-radius:18px}.qbox{padding:1.25rem .9rem} }
</style>
"""

def html(s, to=st):
    to.markdown(s, unsafe_allow_html=True)

def set_color(_color=None):
    # Kept as a small helper so the screen functions remain easy to customise.
    pass

def init_state():
    defaults = dict(status="ready", level=1, won=[], current=None, deadline=None, fail_reason="", failed_level=None, sel=[])
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

def fail(reason):
    s = st.session_state
    s.status, s.fail_reason, s.failed_level = "failed", reason, s.level
    s.current, s.deadline, s.sel = None, None, []
    st.rerun()

def is_correct(cur, given, kind):
    if kind == "yesno":
        return given == cur["answer"]
    if kind == "mcq":
        return given == cur["answer"]
    expected = {cur["options"][i] for i in cur["answer"]}
    return set(given) == expected

def resolve(given):
    s = st.session_state
    if s.status != "question" or not s.current:
        return
    kind = LEVELS[s.level]["type"]
    if time.time() > s.deadline:
        fail("Time's up")
        return
    if not is_correct(s.current, given, kind):
        fail("Wrong")
        return
    s.won.append(s.level)
    s.current, s.deadline, s.sel = None, None, []
    s.status = "completed" if s.level == 3 else "result"
    st.rerun()

def next_level():
    s = st.session_state
    if s.status == "result":
        s.level += 1
        s.status = "ready"
        s.current, s.deadline, s.sel = None, None, []

def toggle(opt):
    s = st.session_state
    if s.status == "question":
        s.sel = [o for o in s.sel if o != opt] if opt in s.sel else s.sel + [opt]

def reel_html(projects, target_index, final=False):
    """Show a compact four-row reel that scrolls smoothly and settles on one random project.

    The repeated rows exist only inside the clipped animation track; the participant sees
    a short four-box window, never a long list of repeated project names.
    """
    total = len(projects)
    visible_rows = 4
    row_step = 48
    # Four short cycles are enough to create a convincing spin without a long visible list.
    sequence = [projects[i % total] for i in range(total * 4)]
    # Stop on the chosen project in the second visible row, after passing at least one cycle.
    stop_at = total * 2 + target_index
    translate_rows = stop_at - 1
    rows = []
    for i, project in enumerate(sequence):
        cls = "cur" if i == stop_at else "dim"
        rows.append(f'<div class="reel-row {cls}">{project}</div>')
    distance = translate_rows * row_step
    duration = "4.6s" if not final else "0s"
    return (
        '<div class="reel-stage"><div class="reel-window" '
        f'style="--row-step:{row_step}px;height:calc(var(--row-step) * {visible_rows});">'
        f'<div class="reel-track" style="--spin-distance:-{distance}px;--spin-duration:{duration};">'
        + "".join(rows)
        + '</div></div></div>'
    )


def confetti(count=90):
    neon_colors = ["#8f5bff", "#b56bff", "#4e7bff", "#7ce7ff", "#eadcff", "#ffffff"]
    pieces = "".join(
        f'<i style="left:{random.randint(0,100)}%;color:{color};background:{color};'
        f'animation-delay:{random.random()*2.2:.2f}s;animation-duration:{2.2+random.random()*2.2:.2f}s;'
        f'transform:rotate({random.randint(0,360)}deg)"></i>'
        for color in (random.choice(neon_colors) for _ in range(count))
    )
    html(f'<div class="confetti-layer">{pieces}</div>')


def spin_and_open(reel_slot, btn_slot):
    s = st.session_state
    if s.status != "ready" or s.current:
        return
    pool = LEVELS[s.level]["pool"]
    target = random.randrange(len(pool))
    projects = [item[1]["project"] for item in pool]
    # Render a single continuous CSS animation: four rows are visible while the
    # reel cycles through the four projects and eases to the random selection.
    btn_slot.empty()
    reel_slot.markdown(reel_html(projects, target), unsafe_allow_html=True)
    time.sleep(4.75)
    question = dict(pool[target][1])
    if LEVELS[s.level]["type"] == "mcq":
        # Keep the correct placeholder option attached to its answer after shuffling.
        question["options"] = random.sample(question["options"], len(question["options"]))
        question["answer"] = question["options"].index("Correct")
    s.current = question
    s.sel = []
    s.deadline = time.time() + TIME_LIMIT
    s.status = "question"
    st.rerun()


def render_ready():
    s = st.session_state
    lv = LEVELS[s.level]
    ready_message = "Ready to start?" if s.level == 1 else "Ready for the next level?"
    html(f'<div class="announcement">LEVEL {s.level} / 3 &nbsp; · &nbsp; CHALLENGE MODE</div><div class="title">Think clearly. Solve the challenge.</div><div class="subtitle">Three levels. One final surprise.</div><div class="panel"><div class="eyebrow">LEVEL {s.level} OF 3 · {lv["name"]}</div><div class="hint">{ready_message}</div></div>')
    reel_slot = st.empty()
    _, mid, _ = st.columns([2, 1, 2])
    btn_slot = mid.empty()
    if btn_slot.button("SPIN", type="primary", key=f"start{s.level}"):
        spin_and_open(reel_slot, btn_slot)

@st.fragment(run_every=1)
def timer_bar():
    s = st.session_state
    if s.status != "question" or not s.deadline:
        return
    left = s.deadline - time.time()
    if left <= 0:
        fail("Time's up")
        return
    pct = max(0, min(100, left / TIME_LIMIT * 100))
    html(f'<div class="tbar"><div style="width:{pct:.0f}%"></div></div><div class="tsec">{int(left) + 1} seconds remaining</div>')

def render_question():
    s = st.session_state
    cur, lv = s.current, LEVELS[s.level]
    html(f'<div class="announcement">LEVEL {s.level} OF 3 · {lv["name"]}</div><div class="qbox">{cur["q"]}</div>')
    timer_bar()
    opts, lvl = cur["options"], s.level
    if lv["type"] == "yesno":
        cols = st.columns(2)
        for i, opt in enumerate(opts):
            if cols[i].button(opt, key=f"o{lvl}_{i}"):
                resolve(opt)
    elif lv["type"] == "mcq":
        # Four choices in a balanced 2x2 grid; the fifth is centered underneath.
        for row_start in (0, 2):
            cols = st.columns(2)
            for i in range(row_start, row_start + 2):
                opt = opts[i]
                if cols[i - row_start].button(f"{'ABCDE'[i]}. {opt}", key=f"o{lvl}_{i}"):
                    resolve(i)
        _, fifth_col, _ = st.columns([1, 2, 1])
        if fifth_col.button(f"{'ABCDE'[4]}. {opts[4]}", key=f"o{lvl}_4"):
            resolve(4)
    else:
        html('<div class="sub">Select the statements you think are correct, then submit.</div>')
        # Four statements in a balanced 2x2 grid; the fifth is centered underneath.
        for row_start in (0, 2):
            cols = st.columns(2)
            for i in range(row_start, row_start + 2):
                opt = opts[i]
                label = f"{opt} — {cur['labels'][i]}"
                picked = opt in s.sel
                cols[i - row_start].button(label, key=f"o{lvl}_{i}", type="primary" if picked else "secondary", on_click=toggle, args=(opt,))
        _, fifth_col, _ = st.columns([1, 2, 1])
        opt = opts[4]
        label = f"{opt} — {cur['labels'][4]}"
        picked = opt in s.sel
        fifth_col.button(label, key=f"o{lvl}_4", type="primary" if picked else "secondary", on_click=toggle, args=(opt,))
        _, mid, _ = st.columns([1, 1.4, 1])
        if mid.button("SUBMIT ANSWERS", key=f"sub{lvl}", type="primary", disabled=not s.sel):
            resolve(list(s.sel))

def render_result():
    s = st.session_state
    lvl = s.level
    confetti(75)
    html(f'<div class="panel"><div class="eyebrow">LEVEL {lvl} PASSED</div><div class="result-mark">Congratulations!</div><div class="sub">Correct — Level {lvl} complete.</div></div>')
    _, mid, _ = st.columns([1, 1.4, 1])
    mid.button(f"CONTINUE TO LEVEL {lvl + 1}", type="primary", key=f"next{lvl}", on_click=next_level)

def render_failed():
    s = st.session_state
    html(f'<div class="panel"><div class="eyebrow">CHALLENGE ENDED</div><div class="result-mark">{s.fail_reason}</div><div class="hint">You did not pass Level {s.failed_level}</div><div class="sub">Thank you for participating.</div></div>')

def render_winner():
    confetti(130)
    html('<div class="announcement">ALL LEVELS PASSED</div><div class="winner">Congratulations, you are a winner!</div><div class="panel"><div class="hint">Your surprise is waiting</div><div class="sub">Scan the QR code below to reveal your surprise.</div></div>')
    if QR_IMAGE_PATH and os.path.exists(QR_IMAGE_PATH):
        st.image(QR_IMAGE_PATH, width=270)
    else:
        html('<div class="qr-box">QR CODE</div>')
    html('<div class="qr-caption">Scan here for a surprise</div>')

def reset_for_next_participant():
    """Clear the current player's progress and return to Level 1."""
    st.session_state.clear()
    st.rerun()


def host_panel():
    pin = os.environ.get("HOST_PIN")
    if pin and st.query_params.get("host") == pin:
        with st.sidebar:
            if st.button("Reset for next participant", key="host_reset"):
                reset_for_next_participant()
        return True
    return False

init_state()
is_host = host_panel()
html(CSS)
if not is_host:
    html("<style>header[data-testid='stHeader']{display:none}</style>")
html(f'<div class="title">{MAIN_TITLE}</div>')
status = st.session_state.status
if status == "ready":
    render_ready()
elif status == "question":
    render_question()
elif status == "result":
    render_result()
elif status == "failed":
    render_failed()
else:
    render_winner()

# Always available for Open Day staff, fixed at the bottom-center of the viewport.
if st.button("RESET FOR NEXT PARTICIPANT", key="next_participant_reset", type="secondary"):
    reset_for_next_participant()
