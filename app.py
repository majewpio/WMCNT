import streamlit as st
import random
import time
import uuid
import math
import matplotlib.pyplot as plt

# =============================
# KONFIG
# =============================
st.set_page_config(page_title="Quiz: Warmia i Mazury – Koło Fortuny", page_icon="🎡", layout="wide")

# Motyw / drobny CSS dla efektu "wow"
st.markdown(
    """
    <style>
      .main {background: linear-gradient(135deg,#0b132b,#1c2541);} 
      .block-container {padding-top: 1.4rem;}
      h1, h2, h3, .stMetric, .stButton>button {font-weight: 800;}
      .stButton>button {border-radius: 12px; padding: .6rem 1rem;}
      .good {background: rgba(34,197,94,.15); border: 1px solid rgba(34,197,94,.5); padding: .7rem 1rem; border-radius: 10px}
      .bad {background: rgba(239,68,68,.15); border: 1px solid rgba(239,68,68,.5); padding: .7rem 1rem; border-radius: 10px}
      .info {opacity:.9}
      .coupon {font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; font-weight: 800; letter-spacing: .08em}
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# DANE: Kategorie i bank pytań (>= 15 unikalnych)
# =============================
CATEGORIES = [
    {"key": "jeziora", "label": "Jeziora"},
    {"key": "zabytki", "label": "Zabytki"},
    {"key": "liczby", "label": "Liczby"},
    {"key": "przyroda", "label": "Przyroda"},
    {"key": "miasta", "label": "Miasta i historia"},
]

QUESTION_BANK = {
    "jeziora": [
        {"q": "Największe jezioro w Polsce, położone na Mazurach, to…", "opts": ["Mamry", "Śniardwy", "Niegocin", "Tałty"], "correct": 1, "info": "Śniardwy mają ok. 113,8 km² powierzchni."},
        {"q": "Najdłuższe jezioro w Polsce leżące w Iławie to…", "opts": ["Jeziorak", "Łańskie", "Wigry", "Hańcza"], "correct": 0, "info": "Jeziorak ma ok. 27,5 km długości."},
        {"q": "Które miasto bywa nazywane ‘stolicą żeglarstwa’?", "opts": ["Mikołajki", "Giżycko", "Mrągowo", "Ruciane‑Nida"], "correct": 1, "info": "Giżycko – między Niegocinem a Kisajnem."},
        {"q": "Przez które jeziora biegnie trzon szlaku WJM?", "opts": ["Śniardwy–Mikołajskie–Niegocin", "Wigry–Mamry–Roś", "Hańcza–Tałty–Ukiel", "Łebsko–Gardno–Jamno"], "correct": 0, "info": "To klasyczny odcinek żeglarski regionu."},
    ],
    "zabytki": [
        {"q": "Siedziba biskupów warmińskich – gotycki zamek – znajduje się w…", "opts": ["Lidzbarku Warmińskim", "Reszlu", "Nidzicy", "Kętrzynie"], "correct": 0, "info": "Lidzbark Warmiński – perła gotyku."},
        {"q": "Zespół katedralny Kopernika jest w…", "opts": ["Fromborku", "Olsztynie", "Elblągu", "Pasłęku"], "correct": 0, "info": "We Fromborku Kopernik żył i pracował."},
        {"q": "‘Wilczy Szaniec’ leży w…", "opts": ["Gierłoży", "Rynie", "Srokowie", "Świętej Lipce"], "correct": 0, "info": "Gierłoż, koło Kętrzyna."},
        {"q": "Sanktuarium z barokowym kościołem i słynnymi organami to…", "opts": ["Święta Lipka", "Gietrzwałd", "Stoczek Klasztorny", "Pieniężno"], "correct": 0, "info": "Święta Lipka – ‘perła baroku’."},
    ],
    "liczby": [
        {"q": "Ile pochylni funkcjonuje dziś w systemie Kanału Elbląskiego?", "opts": ["3", "4", "5", "6"], "correct": 2, "info": "Buczyniec, Kąty, Oleśnica, Jelenie, Całuny."},
        {"q": "Przybliżona długość Jezioraka to…", "opts": ["10 km", "18 km", "27 km", "39 km"], "correct": 2, "info": "Jeziorak ma ok. 27,5 km."},
        {"q": "Granica woj. warmińsko‑mazurskiego z zagranicą ma…", "opts": ["ok. 10 km", "ok. 50 km", "ponad 100 km", "ponad 200 km"], "correct": 3, "info": "Ponad 200 km z obwodem kaliningradzkim."},
        {"q": "Najgłębsze jezioro w Polsce to…", "opts": ["Hańcza", "Drawsko", "Mamry", "Łebsko"], "correct": 0, "info": "Hańcza (108,5 m) – Suwalszczyzna, ale liczba bywa mylona."},
    ],
    "przyroda": [
        {"q": "Unikalność Kanału Elbląskiego polega na tym, że statki…", "opts": ["płyną po szynach", "są holowane przez konie", "‘jadą po trawie’ na platformach", "używają tylko żagli"], "correct": 2, "info": "Pochylnie unoszą jednostki na wózkach po trawie."},
        {"q": "Jezioro Łuknajno to…", "opts": ["rezerwat biosfery UNESCO", "najgłębsze jezioro", "sztuczny zbiornik", "zalew morski"], "correct": 0, "info": "Rezerwat ptactwa wodnego, UNESCO."},
        {"q": "Wieś słynąca z bocianów białych to…", "opts": ["Żywkowo", "Nikielkowo", "Dajtki", "Bęsia"], "correct": 0, "info": "Żywkowo – ‘bociania stolica Polski’."},
    ],
    "miasta": [
        {"q": "Stolicą województwa jest…", "opts": ["Elbląg", "Olsztyn", "Ełk", "Mrągowo"], "correct": 1, "info": "Siedziba władz w Olsztynie."},
        {"q": "Bitwa z 1410 r. odbyła się pod…", "opts": ["Tannenbergiem (Stębark/Grunwald)", "Cedynią", "Kłuszynem", "Wiedniem"], "correct": 0, "info": "Pola Grunwaldu w dzisiejszym województwie."},
        {"q": "Miasto najmocniej kojarzone z Kopernikiem w regionie to…", "opts": ["Frombork", "Pasłęk", "Iława", "Bartoszyce"], "correct": 0, "info": "Frombork – lata pracy Kopernika."},
    ],
}

# zapas: 4+4+4+3+3 = 18 pytań (losujemy z całej puli)

# =============================
# STAN APLIKACJI
# =============================
ss = st.session_state
if "correct" not in ss: ss.correct = 0
if "wrong" not in ss: ss.wrong = 0
if "round" not in ss: ss.round = 1
if "current_category" not in ss: ss.current_category = None
if "current_question" not in ss: ss.current_question = None
if "used_global" not in ss: ss.used_global = set()  # {(cat, idx)}
if "won" not in ss: ss.won = False
if "coupon" not in ss: ss.coupon = None
if "startangle" not in ss: ss.startangle = 90
if "spinning" not in ss: ss.spinning = False
if "await_next" not in ss: ss.await_next = False  # po odpowiedzi

TARGET_CORRECT = 3  # nagroda po tylu poprawnych


# =============================
# FUNKCJE
# =============================

def all_questions():
    return sum(len(QUESTION_BANK[c["key"]]) for c in CATEGORIES)


def pick_random_category():
    return random.choice(CATEGORIES)


def pick_question(cat_key):
    pool = QUESTION_BANK[cat_key]
    # znajdź pierwszy nieużyty globalnie, w razie czego resetuj
    unused = [i for i in range(len(pool)) if (cat_key, i) not in ss.used_global]
    if not unused:
        ss.used_global = set()
        unused = list(range(len(pool)))
    idx = random.choice(unused)
    ss.used_global.add((cat_key, idx))
    return idx, pool[idx]


def animate_wheel_to_index(target_idx, frames=42, extra_turns=4):
    """Prosta animacja: obracamy wykres tak, by target_idx trafił pod wskaźnik (na górze)."""
    slice_angle = 360 / len(CATEGORIES)
    target_center = 90 - (target_idx * slice_angle + slice_angle / 2)
    final_angle = target_center + 360 * extra_turns
    start_angle = ss.startangle

    placeholder = st.empty()

    for f in range(frames):
        t = (f + 1) / frames
        ease = 1 - (1 - t) ** 3  # ease-out-cubic
        angle = start_angle + (final_angle - start_angle) * ease
        ss.startangle = angle

        fig, ax = plt.subplots(figsize=(5.2, 5.2))
        labels = [c["label"] for c in CATEGORIES]
        cols = ["#5bc0be", "#9b59b6", "#f1c40f", "#e67e22", "#3498db"]
        ax.pie([1]*len(labels), labels=labels, startangle=ss.startangle, counterclock=False, wedgeprops=dict(width=0.92))
        ax.annotate("", xy=(0, 1.08), xytext=(0, 0.55), arrowprops=dict(arrowstyle="-|>", lw=2))
        ax.set_aspect('equal')
        placeholder.pyplot(fig)
        time.sleep(0.02)


def spin():
    if ss.spinning or ss.won: 
        return
    ss.spinning = True
    # losuj kategorię i jej indeks
    target_idx = random.randrange(len(CATEGORIES))
    animate_wheel_to_index(target_idx)
    cat = CATEGORIES[target_idx]
    q_idx, q = pick_question(cat["key"])
    ss.current_category = cat
    ss.current_question = {"idx": q_idx, **q}
    ss.await_next = False
    ss.spinning = False


def answer(i):
    if ss.won or ss.spinning or ss.current_question is None:
        return
    correct_idx = ss.current_question["correct"]
    is_ok = (i == correct_idx)
    if is_ok:
        ss.correct += 1
    else:
        ss.wrong += 1

    # feedback w tym samym przebiegu rendera
    if is_ok:
        st.markdown("<div class='good'>✅ Dobrze!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='bad'>❌ Niedobrze.</div>", unsafe_allow_html=True)

    info = ss.current_question.get("info")
    if info:
        st.markdown(f"<div class='info'>ℹ️ {info}</div>", unsafe_allow_html=True)

    if ss.correct >= TARGET_CORRECT and not ss.won:
        ss.won = True
        ss.coupon = "WM-" + uuid.uuid4().hex[:6].upper()
    else:
        ss.round += 1
        ss.await_next = True


# =============================
# UI: nagłówki, staty, layout
# =============================
left, right = st.columns([1, 1])
with left:
    st.title("Quiz o Warmii i Mazurach – Koło Fortuny 🎡")
    st.write("Zakręć kołem, odpowiedz na pytanie z wylosowanej kategorii. Zdobądź **3 poprawne odpowiedzi**, a odblokujesz **kod nagrody**.")
with right:
    c1, c2, c3 = st.columns(3)
    c1.metric("Poprawne", ss.correct)
    c2.metric("Niepoprawne", ss.wrong)
    c3.metric("Runda", ss.round)

# WHEEL render (ostatni kąt w ss.startangle)
wheel_placeholder = st.empty()
fig, ax = plt.subplots(figsize=(5.2, 5.2))
labels = [c["label"] for c in CATEGORIES]
cols = ["#5bc0be", "#9b59b6", "#f1c40f", "#e67e22", "#3498db"]
ax.pie([1]*len(labels), labels=labels, startangle=ss.startangle, counterclock=False, wedgeprops=dict(width=0.92))
ax.annotate("", xy=(0, 1.08), xytext=(0, 0.55), arrowprops=dict(arrowstyle="-|>", lw=2))
ax.set_aspect('equal')
wheel_placeholder.pyplot(fig)

# Przyciski główne
b1, b2, b3 = st.columns([2,1,1])
if b1.button("🎲 Zakręć kołem", disabled=ss.spinning or ss.won):
    spin()
    st.experimental_rerun()

if b2.button("↻ Reset gry"):
    ss.correct = ss.wrong = 0
    ss.round = 1
    ss.current_category = None
    ss.current_question = None
    ss.used_global = set()
    ss.won = False
    ss.coupon = None
    ss.startangle = 90
    ss.spinning = False
    ss.await_next = False
    st.experimental_rerun()

if b3.button("⤴️ Następne", disabled=not ss.await_next or ss.won):
    # automatyczny spin do kolejnego pytania
    spin()
    st.experimental_rerun()

# BLOK PYTANIA
if ss.current_category and ss.current_question:
    st.subheader(f"Kategoria: {ss.current_category['label']}")
    st.write(ss.current_question["q"]) 

    # Opcje odpowiedzi
    for i, opt in enumerate(ss.current_question["opts"]):
        if st.button(opt, key=f"opt_{ss.round}_{i}", disabled=ss.await_next or ss.won):
            answer(i)
            st.experimental_rerun()

# NAGRODA
if ss.won:
    st.success("Gratulacje! Masz 3 poprawne odpowiedzi 🎉")
    st.write("**Twój kod nagrody:**")
    st.code(ss.coupon)
    st.caption("Pokaż kod przy odbiorze nagrody.")
    if st.button("Zagraj ponownie"):
        ss.correct = ss.wrong = 0
        ss.round = 1
        ss.current_category = None
        ss.current_question = None
        ss.used_global = set()
        ss.won = False
        ss.coupon = None
        ss.startangle = 90
        ss.spinning = False
        ss.await_next = False
        st.experimental_rerun()

# STOPKA
st.caption("Pula pytań: {}. Pytania i kategorie edytujesz w sekcjach CATEGORIES oraz QUESTION_BANK w pliku app.py.".format(all_questions()))
