import streamlit as st
from hangman_logic import (
    DIFFICULTY_CONFIG,
    apply_guess,
    attempts_left,
    current_hints,
    get_categories,
    masked_word,
    new_game,
    reveal_next_hint,
    time_left,
    expire_if_needed,
)

st.set_page_config(page_title="Hangman", layout="wide")


def hangman_svg(wrong_count: int, max_wrong: int) -> str:
    parts = []
    if wrong_count >= 1:
        parts.append('<circle cx="210" cy="85" r="22" stroke="#E5E7EB" stroke-width="5" fill="none"/>')
    if wrong_count >= 2:
        parts.append('<line x1="210" y1="107" x2="210" y2="180" stroke="#E5E7EB" stroke-width="5"/>')
    if wrong_count >= 3:
        parts.append('<line x1="210" y1="125" x2="180" y2="150" stroke="#E5E7EB" stroke-width="5"/>')
    if wrong_count >= 4:
        parts.append('<line x1="210" y1="125" x2="240" y2="150" stroke="#E5E7EB" stroke-width="5"/>')
    if wrong_count >= 5:
        parts.append('<line x1="210" y1="180" x2="185" y2="220" stroke="#E5E7EB" stroke-width="5"/>')
    if wrong_count >= 6:
        parts.append('<line x1="210" y1="180" x2="235" y2="220" stroke="#E5E7EB" stroke-width="5"/>')

    return f"""
    <svg viewBox="0 0 340 260" width="100%" height="300" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0B1220" />
          <stop offset="100%" stop-color="#111827" />
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="340" height="260" rx="12" fill="url(#bg)"/>
      <line x1="30" y1="230" x2="300" y2="230" stroke="#22D3EE" stroke-width="6"/>
      <line x1="80" y1="230" x2="80" y2="25" stroke="#22D3EE" stroke-width="6"/>
      <line x1="80" y1="25" x2="210" y2="25" stroke="#22D3EE" stroke-width="6"/>
      <line x1="210" y1="25" x2="210" y2="60" stroke="#22D3EE" stroke-width="6"/>
      {''.join(parts)}
      <text x="16" y="24" fill="#94A3B8" font-size="13" font-family="sans-serif">Stage {wrong_count}/{max_wrong}</text>
    </svg>
    """


def word_boxes(word: str, correct: set[str]) -> str:
    boxes = []
    for ch in word:
        display = ch.upper() if ch in correct else "_"
        boxes.append(f'<span class="letter-box">{display}</span>')
    return f'<div class="word-row">{"".join(boxes)}</div>'


def chips(letters: set[str]) -> str:
    if not letters:
        return '<span class="chip chip-muted">None</span>'
    return " ".join([f'<span class="chip">{x.upper()}</span>' for x in sorted(letters)])


st.markdown(
    """
    <style>
    :root{
      --bg:#0B1220; --surface:#111827; --surface2:#1F2937;
      --text:#E5E7EB; --muted:#94A3B8; --accent:#22D3EE;
      --good:#22C55E; --bad:#F43F5E;
    }

    .stApp{
      background:
      radial-gradient(circle at 15% 10%, rgba(34,211,238,.11), transparent 40%),
      radial-gradient(circle at 85% 90%, rgba(56,189,248,.12), transparent 45%),
      var(--bg);
      color:var(--text);
    }

    .block-container{
      padding-top: calc(4.5rem + env(safe-area-inset-top)) !important;
      padding-bottom: 1rem;
      max-width: 1200px;
    }

    .top-title{
      font-size:2rem;
      line-height:1.25;
      font-weight:800;
      color:var(--text);
      margin:0 0 .6rem 0;
    }

    @media (max-width: 860px){
      .block-container{ padding-top: calc(3.2rem + env(safe-area-inset-top)) !important; }
      .top-title{font-size:1.6rem;}
      .letter-box{width:38px; height:46px; font-size:1.2rem;}
    }

    .card{
      background:linear-gradient(180deg,var(--surface),var(--surface2));
      border:1px solid rgba(148,163,184,.22);
      border-radius:16px; padding:16px;
      box-shadow:0 12px 24px rgba(0,0,0,.28);
    }
    .meta-row{display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:.75rem;}
    .pill{
      font-size:.82rem; font-weight:700; color:var(--text);
      border-radius:999px; padding:.3rem .7rem;
      border:1px solid rgba(34,211,238,.4);
      background:rgba(34,211,238,.12);
    }
    .word-row{display:flex; gap:.45rem; flex-wrap:wrap; margin:.7rem 0;}
    .letter-box{
      width:44px; height:52px; display:inline-flex; align-items:center; justify-content:center;
      border-radius:10px; border:1px solid rgba(148,163,184,.35);
      background:#0F172A; color:var(--accent); font-size:1.45rem; font-weight:800;
    }
    .label{font-size:.85rem; color:var(--muted); margin-top:.4rem;}
    .chip{
      display:inline-block; margin:.2rem .28rem 0 0; padding:.2rem .52rem;
      border-radius:999px; font-weight:700; font-size:.78rem;
      border:1px solid rgba(244,63,94,.45); color:#FECACA; background:rgba(244,63,94,.12);
    }
    .chip-muted{border-color:rgba(148,163,184,.35); color:var(--muted); background:rgba(148,163,184,.10);}
    .kbd-card{margin-top:.75rem;}
    .stButton>button{
      min-height:44px;
      border-radius:10px; font-weight:700;
      border:1px solid rgba(34,211,238,.45);
      background:linear-gradient(180deg,#0F172A,#111827);
      color:var(--text);
    }
    .stButton>button:hover{border-color:#67E8F9; color:#ECFEFF;}
    .stButton>button:disabled{opacity:.45; border-color:rgba(148,163,184,.25);}
    </style>
    """,
    unsafe_allow_html=True,
)

if "meta" not in st.session_state:
    st.session_state.meta = {"score": 0, "streak": 0, "best_streak": 0, "rounds": 0, "celebrated": False}

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "category" not in st.session_state:
    st.session_state.category = "All"

if "used_words" not in st.session_state:
    st.session_state.used_words = set()

if "game" not in st.session_state:
    st.session_state.game = new_game(
        st.session_state.difficulty,
        st.session_state.category,
        st.session_state.used_words,
    )

g = expire_if_needed(st.session_state.game)
st.session_state.game = g

st.markdown('<div style="height:0.35rem;"></div>', unsafe_allow_html=True)

meta = st.session_state.meta
g = st.session_state.game

top1, top2, top3, top4, top5 = st.columns([2.4, 1.3, 1.3, 1.3, 1.2])
with top1:
    st.markdown('<div class="top-title">Hangman</div>', unsafe_allow_html=True)
with top2:
    diff = st.selectbox("Difficulty", list(DIFFICULTY_CONFIG.keys()), index=list(DIFFICULTY_CONFIG.keys()).index(st.session_state.difficulty))
with top3:
    cat = st.selectbox("Category", get_categories(), index=get_categories().index(st.session_state.category))
with top4:
    st.markdown(
        f"""
        <div class="meta-row">
          <span class="pill">Score: {meta["score"]}</span>
          <span class="pill">Streak: {meta["streak"]}</span>
          <span class="pill">Best: {meta["best_streak"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top5:
    if st.button("New Round", use_container_width=True):
        st.session_state.game = new_game(
            st.session_state.difficulty,
            st.session_state.category,
            st.session_state.used_words,
        )
        st.session_state.meta["celebrated"] = False
        st.rerun()

if diff != st.session_state.difficulty or cat != st.session_state.category:
    st.session_state.difficulty = diff
    st.session_state.category = cat
    st.session_state.used_words = set()
    st.session_state.game = new_game(diff, cat, st.session_state.used_words)
    st.session_state.meta["celebrated"] = False
    st.rerun()

g = st.session_state.game
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    left1, left2 = st.columns([3, 1.1])
    with left1:
        st.markdown(
            f"""
            <div class="meta-row">
              <span class="pill">Category: {g["category"]}</span>
              <span class="pill">Difficulty: {g["difficulty"]}</span>
              <span class="pill">Word length: {len(g["word"])}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with left2:
        if st.button("Reveal Next Hint", use_container_width=True, disabled=g["game_over"]):
            st.session_state.game = reveal_next_hint(g)
            st.rerun()

    st.progress(g["attempts_used"] / g["max_wrong"], text=f"Attempts left: {attempts_left(g)} / {g['max_wrong']}")

    for idx, hint in enumerate(current_hints(g), start=1):
        st.info(f"Hint {idx}: {hint}")

    st.markdown(word_boxes(g["word"], g["correct_letters"]), unsafe_allow_html=True)
    st.markdown('<div class="label">Wrong Letters</div>', unsafe_allow_html=True)
    st.markdown(chips(g["wrong_letters"]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(hangman_svg(g["attempts_used"], g["max_wrong"]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card kbd-card">', unsafe_allow_html=True)
rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
for r, letters in enumerate(rows):
    cols = st.columns(len(letters))
    for i, ch in enumerate(letters):
        used = ch.lower() in g["correct_letters"] or ch.lower() in g["wrong_letters"]
        with cols[i]:
            if st.button(ch, key=f"k_{r}_{ch}", disabled=used or g["game_over"], use_container_width=True):
                st.session_state.game = apply_guess(g, ch.lower())
                st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

g = st.session_state.game
if g["game_over"] and not g["score_applied"]:
    base = DIFFICULTY_CONFIG[g["difficulty"]]["base_score"]
    streak_bonus = st.session_state.meta["streak"] * 20
    round_score = max(0, base + streak_bonus + attempts_left(g) * 12 - g["hint_level"] * 10)

    st.session_state.meta["rounds"] += 1
    if g["won"]:
        st.session_state.meta["score"] += round_score
        st.session_state.meta["streak"] += 1
        st.session_state.meta["best_streak"] = max(
            st.session_state.meta["best_streak"],
            st.session_state.meta["streak"],
        )
    else:
        st.session_state.meta["streak"] = 0

    g["score_applied"] = True

    if g["won"]:
        st.balloons()