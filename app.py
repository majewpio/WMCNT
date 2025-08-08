import streamlit as st
import random
import time
import uuid
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quiz: Warmia i Mazury – Koło fortuny", page_icon="🎡", layout="centered")

# =============================
# DANE: Kategorie i bank pytań
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
        {"q": "Największe jezioro w Polsce, położone na Mazurach, to…",
         "opts": ["Mamry", "Śniardwy", "Niegocin", "Tałty"], "correct": 1,
         "info": "Śniardwy mają ok. 113,8 km² powierzchni."},
        {"q": "Najdłuższe jezioro w Polsce leżące w Iławie to…",
         "opts": ["Jeziorak", "Łańskie", "Wigry", "Hańcza"], "correct": 0,
         "info": "Jeziorak ma ok. 27,5 km długości (woj. warmińsko‑mazurskie)."},
        {"q": "Które miasto na Mazurach bywa nazywane ‘stolicą żeglarstwa’?",
         "opts": ["Mikołajki", "Giżycko", "Mrągowo", "Ruciane‑Nida"], "correct": 1,
         "info": "Giżycko – położone między Niegocinem a Kisajnem."},
        {"q": "Przez które jeziora prowadzi szlak Wielkich Jezior Mazurskich?",
         "opts": ["Śniardwy–Mikołajskie–Niegocin", "Wigry–Mamry–Roś", "Hańcza–Tałty–Ukiel", "Łebsko–Gardno–Jamno"], "correct": 0,
         "info": "To trzon żeglarskiego serca regionu."},
    ],
    "zabytki": [
        {"q": "Siedziba biskupów warmińskich – gotycki zamek – znajduje się w…",
         "opts": ["Lidzbarku Warmińskim", "Reszlu", "Nidzicy", "Kętrzynie"], "correct": 0,
         "info": "Zamek w Lidzbarku Warmińskim to perła gotyku."},
        {"q": "Zespół katedralny związany z Mikołajem Kopernikiem znajduje się w…",
         "opts": ["Fromborku", "Olsztynie", "Elblągu", "Pasłęku"], "correct": 0,
         "info": "We Fromborku Kopernik żył i pracował."},
        {"q": "‘Wilczy Szaniec’ – dawna kwatera główna – leży w…",
         "opts": ["Gierłoży", "Rynie", "Srokowie", "Świętej Lipce"], "correct": 0,
         "info": "Gierłoż, koło Kętrzyna."},
        {"q": "Sanktuarium słynące z barokowego kościoła i muzyki organowej to…",
         "opts": ["Święta Lipka", "Gietrzwałd", "Stoczek Klasztorny", "Pieniężno"], "correct": 0,
         "info": "Święta Lipka bywa nazywana ‘perłą baroku’."},
    ],
    "liczby": [
        {"q": "Ile pochylni funkcjonuje dziś w systemie Kanału Elbląskiego?",
         "opts": ["3", "4", "5", "6"], "correct": 2,
         "info": "Buczyniec, Kąty, Oleśnica, Jelenie, Całuny (5)."},
        {"q": "Przybliżona długość Jezioraka wynosi…",
         "opts": ["10 km", "18 km", "27 km", "39 km"], "correct": 2,
         "info": "Jeziorak ma ok. 27,5 km."},
        {"q": "Województwo warmińsko‑mazurskie graniczy z zagranicą na odcinku…",
         "opts": ["ok. 10 km", "ok. 50 km", "ponad 100 km", "ponad 200 km"], "correct": 3,
         "info": "Granica z obwodem kaliningradzkim przekracza 200 km."},
    ],
    "przyroda": [
        {"q": "Cechą unikalną Kanału Elbląskiego jest to, że statki…",
         "opts": ["płyną po szynach", "są holowane przez konie", "‘jadą po trawie’ na platformach", "używają tylko żagli"], "correct": 2,
         "info": "Dzięki pochylniom statki pokonują różnice wysokości ‘po trawie’."},
        {"q": "Jezioro Łuknajno koło Mikołajek to…",
         "opts": ["rezerwat biosfery UNESCO", "najgłębsze jezioro w Polsce", "sztuczny zbiornik", "morze śródlądowe"], "correct": 0,
         "info": "Rezerwat ptactwa wodnego, Rezerwat Biosfery UNESCO."},
        {"q": "Wieś słynąca z bocianów białych to…",
         "opts": ["Żywkowo", "Nikielkowo", "Dajtki", "Bęsia"], "correct": 0,
         "info": "Żywkowo – ‘bociania stolica Polski’."},
    ],
    "miasta": [
        {"q": "Stolicą województwa warmińsko‑mazurskiego jest…",
         "opts": ["Elbląg", "Olsztyn", "Ełk", "Mrągowo"], "correct": 1,
         "info": "Siedziba władz wojewódzkich znajduje się w Olsztynie."},
        {"q": "Słynna bitwa z 1410 r. rozegrała się pod…",
         "opts": ["Tannenbergiem (Stębark/Grunwald)", "Cedynią", "Kłuszynem", "Wiedniem"], "correct": 0,
         "info": "Pola Grunwaldu leżą w dzisiejszym woj. warmińsko‑mazurskim."},
        {"q": "Z Mikołajem Kopernikiem najmocniej kojarzony jest…",
         "opts": ["Frombork", "Pasłęk", "Iława", "Bartoszyce"], "correct": 0,
         "info": "We Fromborku Kopernik spędził wiele lat swojej pracy."},
    ],
}

# =============================
# STAN APLIKACJI (Session State)
# =============================
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "current_category" not in st.session_state:
    st.session_state.current_category = None  # dict z CATEGORIES
if "current_question" not in st.session_state:
    st.session_state.current_question = None  # dict z pytaniem
if "used" not in st.session_state:
    st.session_state.used = {c["key"]: set() for c in CATEGORIES}
if "answered" not in st.session_state:
    st.session_state.answered = False
if "won" not in st.session_state:
    st.session_state.won = False
if "coupon" not in st.session_state:
    st.session_state.coupon = None
if "startangle" not in st.session_state:
    st.session_state.startangle = 90  # tak aby wskaźnik był u góry


def reset_game():
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.round = 1
    st.session_state.current_category = None
    st.session_state.current_question = None
    st.session_state.used = {c["key"]: set() for c in CATEGORIES}
    st.session_state.answered = False
    st.session_state.won = False
    st.session_state.coupon = None
    st.session_state.startangle = 90


# =============================
# LOGIKA: losowanie kategorii i pytania
# =============================

def pick_question(cat_key):
    pool = QUESTION_BANK[cat_key]
    used_idx = st.session_state.used[cat_key]
    available = [i for i in range(len(pool)) if i not in used_idx]
    if not available:
        used_idx.clear()
        available = list(range(len(pool)))
    idx = random.choice(available)
    used_idx.add(idx)
    return pool[idx]


def spin_wheel():
    # Losuj indeks kategorii
    idx = random.randrange(len(CATEGORIES))
    cat = CATEGORIES[idx]

    # Ustal kąt startowy tak, aby wylosowana kategoria wypadła na górze (wskaźnik przy 90°)
    slice_angle = 360 / len(CATEGORIES)
    target_center = 90 - (idx * slice_angle + slice_angle / 2)
    # Dodaj kilka pełnych obrotów dla ‘efektu’
    extra = 360 * random.randint(3, 5)
    st.session_state.startangle = target_center + extra

    st.session_state.current_category = cat
    st.session_state.current_question = pick_question(cat["key"])
    st.session_state.answered = False


# =============================
# UI: nagłówek i statystyki
# =============================
col1, col2 = st.columns([1, 1])
with col1:
    st.title("Quiz o Warmii i Mazurach – Koło Fortuny 🎡")
    st.write("Zakręć kołem, odpowiedz na pytanie z wylosowanej kategorii. Zdobądź **3 poprawne odpowiedzi**, a odblokujesz **kod nagrody**.")
with col2:
    st.metric("Poprawne", st.session_state.correct)
    st.metric("Niepoprawne", st.session_state.wrong)
    st.metric("Runda", st.session_state.round)

# =============================
# WHEEL: prosta wizualizacja ‘koła’
# =============================
fig, ax = plt.subplots(figsize=(4.8, 4.8))
labels = [c["label"] for c in CATEGORIES]
colors = ["#5bc0be", "#9b59b6", "#f1c40f", "#e67e22", "#3498db"]
ax.pie([1]*len(labels), labels=labels, startangle=st.session_state.startangle, counterclock=False,
       wedgeprops=dict(width=0.9))
# Wskaźnik na górze (trójkąt/marker)
ax.annotate("", xy=(0, 1.05), xytext=(0, 0.5),
            arrowprops=dict(arrowstyle="-|>", lw=2))
ax.set_aspect('equal')
st.pyplot(fig)

# Przyciski akcji
spin_col, reset_col = st.columns([2,1])
can_spin = not st.session_state.won and not st.session_state.answered
if spin_col.button("Zakręć kołem", disabled=not can_spin, use_container_width=True):
    spin_wheel()
    # lekka pauza dla ‘wrażenia’ losowania
    time.sleep(0.25)
    st.rerun()

if reset_col.button("Reset gry", use_container_width=True):
    reset_game()
    st.rerun()

# =============================
# BLOK PYTANIA
# =============================
if st.session_state.current_category and st.session_state.current_question:
    cat = st.session_state.current_category
    q = st.session_state.current_question

    st.subheader(f"Kategoria: {cat['label']}")
    st.write(q["q"]) 

    # Opcje odpowiedzi jako przyciski
    opt_cols = st.columns(1)
    for i, opt in enumerate(q["opts"]):
        correct_idx = q["correct"]
        key = f"opt_{cat['key']}_{i}_{st.session_state.round}"
        disabled = st.session_state.answered or st.session_state.won
        if st.button(opt, key=key, disabled=disabled, use_container_width=True):
            # Oceniaj
            is_correct = (i == correct_idx)
            st.session_state.answered = True
            if is_correct:
                st.session_state.correct += 1
            else:
                st.session_state.wrong += 1

            # Informacja zwrotna
            if is_correct:
                st.success("✅ Dobrze!")
            else:
                st.error("❌ Niedobrze.")
            if q.get("info"):
                st.info(q["info"])

            # Sprawdź nagrodę
            if st.session_state.correct >= 3 and not st.session_state.won:
                st.session_state.won = True
                st.session_state.coupon = "WM-" + uuid.uuid4().hex[:6].upper()

            # Następna runda jeśli jeszcze gramy
            if not st.session_state.won:
                st.session_state.round += 1
            st.rerun()

# =============================
# NAGRODA
# =============================
if st.session_state.won:
    st.success("Gratulacje! Masz 3 poprawne odpowiedzi 🎉")
    st.write("**Twój kod nagrody:**")
    st.code(st.session_state.coupon)
    st.caption("Pokaż kod przy odbiorze nagrody.")

    if st.button("Zagraj ponownie"):
        reset_game()
        st.rerun()

# =============================
# STOPKA / instrukcja
# =============================
st.caption("Pytania i kategorie edytujesz w sekcjach CATEGORIES oraz QUESTION_BANK w pliku app.py.")
