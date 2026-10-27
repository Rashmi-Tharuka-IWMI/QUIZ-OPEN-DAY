import os
import random
import time

import streamlit as st

st.set_page_config(page_title="IWMI Open Day Challenge", page_icon="🎁", layout="wide",
                   initial_sidebar_state="collapsed")

# ----------------------------------------------------------------------------
# EDIT HERE: titles, timer, projects and questions
# ----------------------------------------------------------------------------
MAIN_TITLE = "IWMI Open Day Project Challenge"
TIME_LIMIT = 25  # seconds per question

PRIZES = {  # level: (emoji, name, box colour)
    1: ("🍬", "Toffee", "#4FA3E0"),
    2: ("🍭", "Lollipop", "#1E9E8E"),
    3: ("🏅", "Winner Badge", "#2E9E5B"),
}

P1 = ("Project One", "#1565C0", "🌊")
P2 = ("Project Two", "#00897B", "🛰️")
P3 = ("Project Three", "#2E9E5B", "🌱")


def Q(project, q, options, answer):
    return dict(project=project[0], color=project[1], emoji=project[2],
                q=q, options=options, answer=answer)


LEVELS = {
    1: dict(name="Yes or No", color="#1976D2", type="yesno", pool=[
        Q(P1, "Can AI learn patterns from data?", ["Yes", "No"], "Yes"),
        Q(P2, "Can satellites take pictures of Earth from space?", ["Yes", "No"], "Yes"),
        Q(P3, "Is all of Earth's water found in lakes?", ["Yes", "No"], "No"),
    ]),
    2: dict(name="Multiple Choice", color="#0097A7", type="mcq", pool=[
        Q(P1, "Which of these is a type of machine learning?",
          ["Supervised learning", "Soldering", "Gardening", "Weaving"], "Supervised learning"),
        Q(P2, "Which Python library is popular for data analysis?",
          ["Pandas", "Pasta", "Pencil", "Pillow case"], "Pandas"),
        Q(P3, "What is an AI model trained on?",
          ["Data", "Candy", "Clouds", "Socks"], "Data"),
    ]),
    3: dict(name="Select All Correct", color="#2E9E5B", type="select", pool=[
        Q(P1, "Select ALL the programming languages",
          ["Python", "Java", "Banana", "R", "Table"], ["Python", "Java", "R"]),
        Q(P2, "Select ALL the sources of water",
          ["River", "Lake", "Desert sand", "Groundwater"], ["River", "Lake", "Groundwater"]),
        Q(P3, "Select ALL the types of data",
          ["Images", "Text", "Spoon", "Numbers"], ["Images", "Text", "Numbers"]),
    ]),
}

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, .stApp, button, p, div { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; }
.stApp { background: linear-gradient(135deg,#e3f2fd 0%,#ffffff 50%,#e4f5ec 100%); }
.block-container { max-width: 100% !important; padding: 1rem 4vw 2rem !important; }
#MainMenu, footer { visibility: hidden; }
.title { text-align:center; font-weight:700; font-size:clamp(2rem,4.5vw,3.6rem); line-height:1.1;
  background:linear-gradient(90deg,#0d47a1,#1e88c9,#2e9e5b); -webkit-background-clip:text;
  background-clip:text; color:transparent; margin:.2rem 0 .4rem; }
.card { background:rgba(255,255,255,.85); border-radius:36px; padding:26px 30px; text-align:center;
  box-shadow:0 12px 40px rgba(21,101,192,.18); margin:10px auto; }
.pill { display:inline-block; background:var(--pc); color:#fff; border-radius:999px; padding:4px 20px;
  font-weight:700; font-size:1.1rem; }
.hint { color:var(--pc); font-weight:700; font-size:clamp(1.4rem,2.6vw,2.2rem); margin:.6rem 0 0; }
.pname { color:var(--pc); font-weight:700; font-size:clamp(1.8rem,3.4vw,3rem); text-align:center; margin:.6rem 0 .3rem; }
.qbox { background:var(--pc); color:#fff; border-radius:34px; padding:34px 30px; text-align:center;
  font-weight:600; font-size:clamp(1.5rem,2.8vw,2.6rem); box-shadow:0 12px 0 rgba(0,0,0,.12); margin-bottom:14px; }
.tbar { height:18px; background:rgba(0,0,0,.08); border-radius:999px; overflow:hidden; margin:6px 0 4px; }
.tbar > div { height:100%; background:var(--pc); border-radius:999px; transition:width 1s linear; }
.tsec { text-align:center; color:var(--pc); font-weight:700; margin-bottom:10px; }
.sub { text-align:center; color:#2f5d7c; font-weight:600; font-size:1.2rem; margin:.4rem 0; }

/* buttons: rounded, colourful, big */
.stButton, [data-testid="stButton"],
[data-testid="stElementContainer"]:has(.stButton),
[data-testid="stElementContainer"]:has([data-testid="stButton"]) { width:100% !important; max-width:100% !important; }
[data-testid="stHorizontalBlock"] { gap:1.2rem; align-items:stretch; }
[data-testid="stColumn"] { min-width:0; }
.stButton > button { width:100% !important; min-height:84px; border-radius:999px; border:4px solid var(--pc,#1976d2);
  transition:transform .15s; display:flex; align-items:center; justify-content:center; text-align:center; margin:0; }
.stButton > button > div { width:100%; display:flex; justify-content:center; }
.pill-wrap { text-align:center; margin-top:14px; }
.stButton > button p { font-size:1.6rem; font-weight:700; }
.stButton > button:hover { transform:translateY(-3px) scale(1.02); }
.stButton > button[kind="secondary"], .stButton > button[data-testid="stBaseButton-secondary"] {
  background:#fff; color:var(--pc,#1976d2); box-shadow:0 6px 0 rgba(0,0,0,.08); }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--pc,#1976d2); color:#fff; box-shadow:0 6px 0 rgba(0,0,0,.18); }
.stButton > button:hover, .stButton > button:focus { border-color:var(--pc,#1976d2); }
.stButton > button[kind="secondary"]:hover { background:#fff; color:var(--pc,#1976d2); }
.stButton > button[kind="primary"]:hover { background:var(--pc,#1976d2); color:#fff; filter:brightness(1.08); }

/* reel (spin) */
.reel { max-width:620px; margin:14px auto; }
.reel-row { border-radius:30px; padding:14px 20px; margin:8px 0; text-align:center; font-weight:700;
  font-size:1.6rem; background:#fff; color:var(--pc); opacity:.45; }
.reel-row.cur { background:var(--pc); color:#fff; opacity:1; font-size:2.3rem; transform:scale(1.06);
  box-shadow:0 10px 0 rgba(0,0,0,.14); }
.reel.stop .cur { animation:pulse .5s ease 2; }

/* gift basket */
.basket { max-width:680px; margin:6px auto 4px; padding:2px 18px 14px; background:rgba(255,255,255,.38);
  border:3px solid rgba(255,255,255,.95); border-radius:26px 26px 60px 60px; backdrop-filter:blur(6px);
  box-shadow:inset 0 -10px 22px rgba(255,255,255,.5),0 8px 24px rgba(0,0,0,.08); }
.bt { text-align:center; font-weight:700; color:#0d47a1; font-size:1.1rem; padding-top:6px; }
.slots { display:flex; justify-content:space-around; }
.slot { text-align:center; padding:44px 6px 0; position:relative; z-index:2; }
.cap { font-size:.95rem; font-weight:600; color:#2f5d7c; margin-top:6px; line-height:1.2; }
.basket.big { max-width:900px; padding-bottom:30px; }
.basket.big .slot { padding:80px 34px 14px; }
.basket.big .gift { transform:scale(1.6); }
.basket.big .cap { font-size:1.15rem; margin-top:26px; }
.slot.flyin { animation:fly 1.1s ease 2.4s both; z-index:5; }

.gift { position:relative; width:80px; height:80px; margin:0 auto; }
.gift .body { position:absolute; bottom:0; left:5px; right:5px; height:48px; background:var(--c);
  border-radius:0 0 12px 12px; box-shadow:inset 0 -7px 0 rgba(0,0,0,.14); z-index:1; }
.gift .body::after, .gift .lid::after { content:""; position:absolute; left:50%; top:0; bottom:0; width:12px;
  margin-left:-6px; background:rgba(255,255,255,.8); }
.gift .lid { position:absolute; bottom:46px; left:0; right:0; height:22px; background:var(--c);
  border-radius:9px; filter:brightness(1.1); box-shadow:inset 0 -4px 0 rgba(0,0,0,.14);
  transform-origin:left bottom; z-index:3; }
.gift .lid::before { content:"🎀"; position:absolute; top:-24px; left:50%; transform:translateX(-50%); font-size:1.5rem; }
.gift .prize { position:absolute; left:50%; bottom:30px; font-size:2.3rem; opacity:0;
  transform:translate(-50%,0) scale(.3); z-index:2; }
.gift.locked { filter:grayscale(1); opacity:.45; }
.gift.open .lid { transform:translate(-12px,-16px) rotate(-26deg); }
.gift.open .prize { opacity:1; transform:translate(-50%,-48px) scale(1); }
.gift.lost .body, .gift.lost .lid { background:#b9b9cc; }
.gift.fresh { animation:shake .6s ease var(--d,0s) both; }
.gift.fresh .lid { animation:lid .8s ease calc(var(--d,0s) + .6s) both; }
.gift.fresh .prize { animation:pop 1.1s cubic-bezier(.2,1.6,.4,1) calc(var(--d,0s) + 1.1s) both; }
.bigbox { width:80px; margin:90px auto 40px; transform:scale(2.2); }

/* end screens */
.winner { background:linear-gradient(90deg,#0d47a1,#1e88c9,#2e9e5b,#0d47a1); background-size:200% 100%;
  animation:shine 3s linear infinite; color:#fff; border-radius:44px; padding:26px 20px; text-align:center;
  font-weight:700; font-size:clamp(1.8rem,4.6vw,3.8rem); text-shadow:0 4px 0 rgba(0,0,0,.18);
  box-shadow:0 0 0 8px #fff,0 0 0 16px #1e88c9,0 20px 40px rgba(13,71,161,.3); margin:18px auto; }
.trophy { text-align:center; font-size:7rem; animation:bounce 1.2s ease-in-out infinite; }
.sad { text-align:center; font-size:8rem; animation:wobble 1.8s ease-in-out infinite; }
.over { text-align:center; font-weight:700; font-size:clamp(2.2rem,5vw,4rem); color:#2f5d7c; }
.cf { position:fixed; inset:0; pointer-events:none; z-index:999; overflow:hidden; }
.cf i { position:absolute; top:-30px; width:11px; height:17px; animation:fall linear infinite; }

@keyframes lid { from { transform:none; } to { transform:translate(-12px,-16px) rotate(-26deg); } }
@keyframes pop { 0% { opacity:0; transform:translate(-50%,0) scale(.3); }
  100% { opacity:1; transform:translate(-50%,-48px) scale(1); } }
@keyframes shake { 0%,100% { transform:rotate(0); } 25% { transform:rotate(-7deg); } 75% { transform:rotate(7deg); } }
@keyframes fly { from { transform:translateY(340px) scale(2.6); opacity:0; } to { transform:none; opacity:1; } }
@keyframes pulse { 50% { transform:scale(1.14); } }
@keyframes wobble { 0%,100% { transform:rotate(-6deg); } 50% { transform:rotate(6deg) translateY(8px); } }
@keyframes bounce { 50% { transform:translateY(-22px); } }
@keyframes shine { to { background-position:200% 0; } }
@keyframes fall { to { transform:translateY(112vh) rotate(720deg); } }
</style>
"""


def html(s, to=st):
    to.markdown(" ".join(s.split()), unsafe_allow_html=True)


def set_color(c):
    html(f"<style>:root{{--pc:{c}}}</style>")


# ----------------------------------------------------------------------------
# HTML builders
# ----------------------------------------------------------------------------
def gift_html(lvl, cls, d=0.0, emoji=None):
    e, _, col = PRIZES[lvl]
    return (f'<div class="gift {cls}" style="--c:{col};--d:{d}s">'
            f'<div class="prize">{emoji or e}</div><div class="body"></div><div class="lid"></div></div>')


def basket_html(big=False, fly=None, show_all=False):
    s = st.session_state
    slots = ""
    for lvl in (1, 2, 3):
        e, name, _ = PRIZES[lvl]
        if lvl in s.won:
            g = gift_html(lvl, "open fresh" if show_all else "open", d=0.4 + (lvl - 1) * 1.6)
            cap = f"Level {lvl}<br><b>{e} {name}</b>"
        elif s.failed_level == lvl:
            g = gift_html(lvl, "open lost fresh", d=0.3, emoji="😢")
            cap = f"Level {lvl}<br><b>Not won</b>"
        else:
            g = gift_html(lvl, "locked")
            cap = f"Level {lvl}<br><b>???</b>"
        fly_cls = " flyin" if (fly == lvl and lvl in s.won) else ""
        slots += f'<div class="slot{fly_cls}">{g}<div class="cap">{cap}</div></div>'
    size = " big" if big else ""
    return (f'<div class="basket{size}"><div class="bt">🧺 My Gift Basket</div>'
            f'<div class="slots">{slots}</div></div>')


def reel_html(pool, idx, final=False):
    n = len(pool)
    rows = ""
    for off in (-1, 0, 1):
        p = pool[(idx + off) % n]
        cls = "cur" if off == 0 else "dim"
        rows += (f'<div class="reel-row {cls}" style="--pc:{p["color"]}">'
                 f'{p["emoji"]} {p["project"]}</div>')
    return f'<div class="reel{" stop" if final else ""}">{rows}</div>'


def confetti(n=70):
    colors = ["#0D47A1", "#1E88E5", "#81D4FA", "#00897B", "#2E9E5B", "#A5D6A7", "#FFFFFF"]
    bits = "".join(
        f'<i style="left:{random.randint(0, 100)}%;background:{random.choice(colors)};'
        f'animation-delay:{random.random() * 3:.2f}s;'
        f'animation-duration:{2 + random.random() * 3:.2f}s"></i>' for _ in range(n))
    html(f'<div class="cf">{bits}</div>')


# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
def init_state():
    # Per-browser-session state, so participants never share anything.
    defaults = dict(status="ready", level=1, won=[], current=None, deadline=None,
                    fresh=None, fail_reason="", failed_level=None, sel=[])
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def fail(reason):
    s = st.session_state
    s.status, s.fail_reason, s.failed_level = "failed", reason, s.level
    s.current, s.deadline, s.sel = None, None, []
    st.rerun()


def is_correct(cur, given):
    if isinstance(cur["answer"], list):
        return set(given) == set(cur["answer"])
    return given == cur["answer"]


def resolve(given):
    s = st.session_state
    if s.status != "question" or not s.current:
        return  # game already over or no active question: ignore
    timed_out = time.time() > s.deadline
    if timed_out or not is_correct(s.current, given):
        fail("Time's up!" if timed_out else "Oops, that wasn't right!")
    s.won.append(s.level)
    s.fresh = s.level
    s.current, s.deadline, s.sel = None, None, []
    s.status = "completed" if s.level == 3 else "result"
    st.rerun()


def next_level():
    s = st.session_state
    if s.status != "result":
        return
    s.level += 1
    s.fresh = None
    s.status = "ready"


def toggle(opt):
    s = st.session_state
    if s.status != "question":
        return
    s.sel = [o for o in s.sel if o != opt] if opt in s.sel else s.sel + [opt]


def spin_and_open(reel_slot, btn_slot):
    s = st.session_state
    if s.status != "ready" or s.current:
        return
    pool = LEVELS[s.level]["pool"]
    n, target, steps = len(pool), random.randrange(len(pool)), 24
    btn_slot.empty()
    for k in range(steps):  # scrolls, slowing down until it stops on the target
        html(reel_html(pool, (target - (steps - 1 - k)) % n), reel_slot)
        time.sleep(0.04 + 0.38 * (k / (steps - 1)) ** 3)
    html(reel_html(pool, target, final=True), reel_slot)
    time.sleep(1.1)
    q = dict(pool[target])
    q["options"] = q["options"][:] if LEVELS[s.level]["type"] == "yesno" else random.sample(
        q["options"], len(q["options"]))
    s.current, s.sel = q, []
    s.deadline = time.time() + TIME_LIMIT
    s.status = "question"
    st.rerun()


# ----------------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------------
def render_ready():
    s = st.session_state
    lv = LEVELS[s.level]
    set_color(lv["color"])
    html(basket_html())
    html(f'<div class="card"><span class="pill">Level {s.level} of 3 · {lv["name"]}</span>'
         f'<p class="hint">Spin to reveal your project question! 🎡</p></div>')
    reel_slot = st.empty()
    _, mid, _ = st.columns([1, 2, 1])
    btn_slot = mid.empty()
    if btn_slot.button("🎡 SPIN!", type="primary", key=f"spin{s.level}"):
        spin_and_open(reel_slot, btn_slot)


@st.fragment(run_every=1)
def timer_bar():
    s = st.session_state
    if s.status != "question" or not s.deadline:
        return
    left = s.deadline - time.time()
    if left <= 0:
        fail("Time's up!")
    pct = max(0, min(100, left / TIME_LIMIT * 100))
    html(f'<div class="tbar"><div style="width:{pct:.0f}%"></div></div>'
         f'<div class="tsec">⏱ {int(left) + 1}s</div>')


def render_question():
    s = st.session_state
    cur, lv = s.current, LEVELS[s.level]
    set_color(cur["color"])
    html(basket_html())
    html(f'<div class="pill-wrap"><span class="pill">Level {s.level} of 3 · {lv["name"]}</span></div>'
         f'<div class="pname">{cur["emoji"]} {cur["project"]}</div>'
         f'<div class="qbox">{cur["q"]}</div>')
    timer_bar()
    opts, lvl = cur["options"], s.level
    if lv["type"] == "yesno":
        cols = st.columns(2)
        for i, (c, o) in enumerate(zip(cols, opts)):
            if c.button(("✅ " if o == "Yes" else "❌ ") + o, key=f"o{lvl}_{i}"):
                resolve(o)
    elif lv["type"] == "mcq":
        cols = st.columns(2)
        for i, o in enumerate(opts):
            if cols[i % 2].button(f"{'ABCD'[i]}.  {o}", key=f"o{lvl}_{i}"):
                resolve(o)
    else:
        html('<div class="sub">Tap every correct answer, then press Submit 👇</div>')
        cols = st.columns(2)
        for i, o in enumerate(opts):
            picked = o in s.sel
            cols[i % 2].button(("✅ " if picked else "⬜ ") + o, key=f"o{lvl}_{i}",
                               type="primary" if picked else "secondary",
                               on_click=toggle, args=(o,))
        _, mid, _ = st.columns([1, 2, 1])
        if mid.button("🚀 Submit answers", key=f"sub{lvl}", type="primary", disabled=not s.sel):
            resolve(list(s.sel))


def render_result():
    s = st.session_state
    lvl = s.level
    e, name, _ = PRIZES[lvl]
    set_color(LEVELS[lvl]["color"])
    confetti(50)
    html(basket_html(fly=s.fresh))
    html(f'<div class="card"><div style="font-size:4rem">🎉</div>'
         f'<p class="hint" style="font-size:clamp(2rem,4vw,3.4rem)">Congratulations!</p>'
         f'<div class="sub">Correct answer, Level {lvl} complete! You won a {e} {name}!</div>'
         f'<div class="bigbox">{gift_html(lvl, "open fresh", d=0.3)}</div></div>')
    _, mid, _ = st.columns([1, 2, 1])
    mid.button(f"🎡 Spin for Level {lvl + 1}", type="primary", key=f"next{lvl}", on_click=next_level)


def render_failed():
    s = st.session_state
    set_color("#3F7CAC")
    html(basket_html())
    n = len(s.won)
    kept = (f"You collected {n} gift{'s' if n != 1 else ''}, they're safe in your basket above! 🧺"
            if n else "Every great journey starts somewhere!")
    html(f'<div class="sad">😢</div><div class="over">GAME OVER!</div>'
         f'<div class="card"><p class="hint" style="color:#2f5d7c">{s.fail_reason}</p>'
         f'<div class="sub">Good try! You reached Level {s.failed_level}.</div>'
         f'<div class="sub">{kept}</div>'
         f'<div class="sub">💙 Thank you for participating! 💙</div></div>')


def render_winner():
    set_color("#1565C0")
    confetti(120)
    html('<div class="trophy">🏆</div>'
         '<div class="winner">🎉 CONGRATULATIONS, YOU ARE A WINNER! 🎉</div>')
    html(basket_html(big=True, show_all=True))
    html('<div class="card"><div class="sub" style="font-size:1.6rem">You collected every gift: '
         '🍬 Toffee, 🍭 Lollipop and 🏅 Winner Badge!</div>'
         '<div class="sub">💚 Thank you so much for taking part! 💚</div></div>')


# ----------------------------------------------------------------------------
# Organiser-only reset: open the app with ?host=<HOST_PIN> (set HOST_PIN first).
# Nothing is shown on participant screens.
# ----------------------------------------------------------------------------
def host_panel():
    pin = os.environ.get("HOST_PIN")
    if pin and st.query_params.get("host") == pin:
        with st.sidebar:
            st.caption("Organiser only")
            if st.button("Reset for next participant", key="host_reset"):
                st.session_state.clear()
                st.rerun()
        return True
    return False


init_state()
is_host = host_panel()
html(CSS)
if not is_host:
    html("<style>header[data-testid='stHeader']{display:none}</style>")
set_color("#1976D2")
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
