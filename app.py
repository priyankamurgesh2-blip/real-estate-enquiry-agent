


import os
import re
import json
import logging

import psycopg
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text


st.set_page_config(
    page_title="EstateMate | Property Finder",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("estatemate")

DATABASE_URL = os.getenv("DATABASE_URL")

PROPERTIES = [
    {
        "name": "Green Homes",
        "type": "2BHK",
        "location": "Vijayawada",
        "price": 30,
        "tag": "Popular choice",
        "description": "Comfortable family living with practical space.",
    },
    {
        "name": "Sunrise Residency",
        "type": "3BHK",
        "location": "Vijayawada",
        "price": 45,
        "tag": "Family favourite",
        "description": "Extra room for growing families and guests.",
    },
    {
        "name": "Happy Villas",
        "type": "Villa",
        "location": "Guntur",
        "price": 55,
        "tag": "More space",
        "description": "A sample villa listing.",
    },
    {
        "name": "City Plot",
        "type": "Plot",
        "location": "Vijayawada",
        "price": 18,
        "tag": "Build your plan",
        "description": "A sample plot listing.",
    },
    {
        "name": "Budget Homes",
        "type": "1BHK",
        "location": "Vijayawada",
        "price": 15,
        "tag": "Budget pick",
        "description": "A compact sample home.",
    },
]


# ---------------- DATABASE ----------------

def init_db():
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable is missing.")
        return False

    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=10) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS enquiries (
                    id BIGSERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    property_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    budget TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        logger.info("Database connection and enquiries table check succeeded.")
        return True
    except Exception:
        logger.exception("Database initialisation failed. Check DATABASE_URL and Neon database settings.")
        raise


def save_enquiry(name, phone, property_type, location, budget):
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is missing.")

    with psycopg.connect(DATABASE_URL, connect_timeout=10) as conn:
        conn.execute(
            """
            INSERT INTO enquiries
                (name, phone, property_type, location, budget)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, phone, property_type, location, budget),
        )


# ---------------- DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink:#142b27;
    --muted:#65756f;
    --green:#176b52;
    --mint:#eaf5ef;
}

html, body, [class*="css"] {
    font-family:'DM Sans',sans-serif;
}

.stApp {
    background:linear-gradient(180deg,#f6faf7,#ffffff 52%,#f6faf7);
    color:var(--ink);
}

.block-container {
    max-width:1180px;
    padding-top:1.7rem;
    padding-bottom:3rem;
}

h1,h2,h3 {
    font-family:'Manrope',sans-serif !important;
    color:var(--ink) !important;
}

.hero {
    padding:2.6rem;
    border-radius:28px;
    background:linear-gradient(125deg,#123b31,#176b52 65%,#34866b);
    color:white;
    margin-bottom:1.3rem;
}

.hero h1 {
    color:white !important;
    font-size:clamp(2rem,4vw,3.5rem) !important;
}

.hero p {
    color:#e5f2eb;
    font-size:1.04rem;
}

.eyebrow,.section-kicker {
    text-transform:uppercase;
    letter-spacing:1.5px;
    font-size:.75rem;
    font-weight:800;
}

.eyebrow { color:#c7ead7; }
.section-kicker { color:var(--green); }

.pill {
    display:inline-block;
    padding:.42rem .8rem;
    border:1px solid rgba(255,255,255,.35);
    border-radius:99px;
    margin:.3rem;
    color:white;
}

.section-note,.meta {
    color:var(--muted);
}

.property,.info-card {
    background:white;
    border:1px solid #e1ebe5;
    border-radius:20px;
    padding:1.25rem;
    box-shadow:0 8px 25px rgba(20,60,45,.045);
    margin-bottom:.7rem;
}

.property { min-height:205px; }

.property-icon {
    font-size:1.5rem;
}

.tag {
    background:#f3f7ef;
    color:#28644e;
    padding:.35rem .55rem;
    border-radius:99px;
    font-size:.75rem;
}

.price {
    color:var(--green);
    font-family:'Manrope',sans-serif;
    font-size:1.4rem;
    font-weight:800;
}

div[data-testid="stForm"] {
    background:white !important;
    border:1px solid #c9ded1 !important;
    padding:1.2rem;
    border-radius:18px;
}

.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    border-radius:12px;
    border:0;
    background:#176b52;
    color:white;
    font-weight:700;
    padding:.65rem 1rem;
}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background:#104d3c;
    color:white;
}

.stApp label,
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p {
    color:#142b27 !important;
    opacity:1 !important;
    font-weight:700 !important;
}

.stApp input,.stApp textarea {
    color:#142b27 !important;
    -webkit-text-fill-color:#142b27 !important;
    background:white !important;
    border:1px solid #9ab9a8 !important;
}

div[data-testid="stChatMessage"] {
    background:white !important;
    border:1px solid #d9e8df;
    border-radius:16px;
    padding:1rem;
    margin:.5rem 0;
    color:#142b27 !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span {
    color:#142b27 !important;
}

.footer {
    text-align:center;
    color:#718079;
    padding:1.5rem .5rem .3rem;
    font-size:.82rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------- INITIALISE DATABASE ----------------

if DATABASE_URL:
    try:
        if init_db():
            st.session_state["database_ready"] = True
    except Exception:
        st.session_state["database_ready"] = False
else:
    st.session_state["database_ready"] = False


# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">A simpler way to find your next place</div>
    <h1>Find a place that<br>feels like home.</h1>
    <p>Explore sample listings, share your requirements,
    and ask our property assistant.</p>
    <span class="pill">🏡 Homes</span>
    <span class="pill">📍 Local search</span>
    <span class="pill">💬 Quick enquiries</span>
</div>
""", unsafe_allow_html=True)


# ---------------- OVERVIEW ----------------

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="info-card">
    <div class="section-kicker">Sample listings</div>
    <h2>05</h2><div class="meta">Demo properties</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="info-card">
    <div class="section-kicker">Locations</div>
    <h2>02</h2><div class="meta">Vijayawada and Guntur</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="info-card">
    <div class="section-kicker">Your next step</div>
    <h2>01</h2><div class="meta">Tell us your requirements</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- PROPERTY FILTERS ----------------

st.write("")
st.markdown(
    '<div class="section-kicker">Explore the collection</div>'
    '<h2>Sample properties</h2>'
    '<div class="section-note">Filter the demo listings.</div>',
    unsafe_allow_html=True,
)

f1, f2 = st.columns(2)

with f1:
    filter_location = st.selectbox(
        "Filter by location",
        ["All locations", "Vijayawada", "Guntur"],
    )

with f2:
    filter_type = st.selectbox(
        "Filter by property type",
        ["All types", "1BHK", "2BHK", "3BHK", "Villa", "Plot"],
    )

visible = [
    p for p in PROPERTIES
    if (filter_location == "All locations"
        or p["location"] == filter_location)
    and (filter_type == "All types"
         or p["type"] == filter_type)
]

icons = {
    "1BHK": "🏠",
    "2BHK": "🏡",
    "3BHK": "🏘️",
    "Villa": "🏰",
    "Plot": "🌳",
}

cards = st.columns(3)

for i, p in enumerate(visible):
    with cards[i % 3]:
        st.markdown(f"""
        <div class="property">
            <div class="property-icon">{icons[p['type']]}</div>
            <span class="tag">{p['tag']}</span>
            <h3>{p['name']}</h3>
            <div class="meta">📍 {p['location']} · {p['type']}</div>
            <div class="price">₹{p['price']} lakhs</div>
            <p class="meta">{p['description']}</p>
            <small>Fictional demo listing</small>
        </div>
        """, unsafe_allow_html=True)

if not visible:
    st.info("No sample listings match these filters.")


# ---------------- ENQUIRY FORM ----------------

st.divider()
left, right = st.columns([1.05, .95], gap="large")

with left:
    st.markdown(
        '<div class="section-kicker">Tell us what you need</div>'
        '<h2>Submit an enquiry</h2>'
        '<div class="section-note">Share your property requirements.</div>',
        unsafe_allow_html=True,
    )

    with st.form("enquiry_form", clear_on_submit=False):
        name = st.text_input("Your name", placeholder="Full name")
        phone = st.text_input(
            "Phone number",
            max_chars=10,
            placeholder="10-digit phone number",
        )
        property_type = st.selectbox(
            "Property type",
            ["1BHK", "2BHK", "3BHK", "Villa", "Plot"],
        )
        location = st.text_input(
            "Preferred location",
            placeholder="e.g. Vijayawada",
        )
        budget = st.selectbox(
            "Your budget",
            [
                "Below ₹20 lakhs",
                "₹20–40 lakhs",
                "₹40–60 lakhs",
                "₹60 lakhs–₹1 crore",
                "Above ₹1 crore",
            ],
        )
        submitted = st.form_submit_button(
            "Find matching properties",
            use_container_width=True,
        )

    if submitted:
        clean_name = name.strip()
        clean_phone = phone.strip()
        clean_location = location.strip()

        if not clean_name or not clean_phone or not clean_location:
            st.error("Please fill in all fields.")
        elif not clean_phone.isdigit() or len(clean_phone) != 10:
            st.error("Enter a valid 10-digit phone number.")
        elif not DATABASE_URL:
            st.error(
                "Database is not configured yet. Please contact the site administrator."
            )
        else:
            try:
                save_enquiry(
                    clean_name,
                    clean_phone,
                    property_type,
                    clean_location,
                    budget,
                )

                st.session_state["latest_enquiry"] = {
                    "name": clean_name,
                    "type": property_type,
                    "location": clean_location,
                    "budget": budget,
                }

                st.success(
                    "Thank you! Your enquiry was saved successfully."
                )

                limits = {
                    "Below ₹20 lakhs": (0, 20),
                    "₹20–40 lakhs": (20, 40),
                    "₹40–60 lakhs": (40, 60),
                    "₹60 lakhs–₹1 crore": (60, 100),
                    "Above ₹1 crore": (100, float("inf")),
                }

                low, high = limits[budget]

                matches = [
                    p for p in PROPERTIES
                    if p["type"] == property_type
                    and clean_location.lower() in p["location"].lower()
                    and low <= p["price"] < high
                ]

                st.markdown("#### Matching sample properties")

                if matches:
                    for p in matches:
                        st.write(
                            f"**{p['name']}** — {p['type']} · "
                            f"{p['location']} · ₹{p['price']} lakhs"
                        )
                else:
                    st.info(
                        "No sample property matches all preferences. "
                        "Try a different location or budget."
                    )

            except Exception:
                logger.exception(
                    "Saving enquiry failed. Check the Render logs for the database error."
                )
                st.error(
                    "We could not save your enquiry. "
                    "Please try again later."
                )


# ---------------- PROPERTY CHAT ASSISTANT ----------------

with right:
    st.markdown(
        '<div class="section-kicker">Ask a question</div>'
        '<h2>Property assistant</h2>'
        '<div class="section-note">Try: 2BHK in Vijayawada under 40 lakhs.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="info-card">💬 Ask about property type, '
        'location, or budget. Listings are fictional demo examples.</div>',
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for index, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.write(message["content"])

            if message["role"] == "assistant":
                spoken_text = json.dumps(
                    message["content"],
                    ensure_ascii=False,
                )
                voice_locale = (
                    "te-IN"
                    if any("\u0c00" <= ch <= "\u0c7f"
                           for ch in message["content"])
                    else "en-IN"
                )

                voice_html = f"""
                <div>
                    <button id="speak-{index}"
                    style="background:#176b52;color:white;border:0;
                    border-radius:10px;padding:9px 13px;cursor:pointer">
                    🔊 Read answer aloud</button>
                    <button id="stop-{index}"
                    style="background:#eaf5ef;color:#142b27;border:0;
                    border-radius:10px;padding:9px 13px;cursor:pointer">
                    ⏹ Stop</button>
                    <span id="status-{index}"></span>
                </div>
                <script>
                const answerText = {spoken_text};
                const lang = "{voice_locale}";
                document.getElementById("speak-{index}").onclick = () => {{
                    if (!("speechSynthesis" in window)) return;
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(answerText);
                    utterance.lang = lang;
                    utterance.rate = 0.9;
                    utterance.onstart = () =>
                        document.getElementById("status-{index}").textContent = "Speaking...";
                    utterance.onend = () =>
                        document.getElementById("status-{index}").textContent = "";
                    window.speechSynthesis.speak(utterance);
                }};
                document.getElementById("stop-{index}").onclick = () => {{
                    window.speechSynthesis.cancel();
                    document.getElementById("status-{index}").textContent = "";
                }};
                </script>
                """
                components.html(voice_html, height=55)

    voice_language = st.selectbox(
        "Voice language / మాట్లాడే భాష",
        ["English", "Telugu (తెలుగు)"],
    )
    speech_lang = (
        "te-IN" if voice_language.startswith("Telugu") else "en-IN"
    )

    st.caption(
        "Click Start speaking, allow microphone access, speak, then stop."
    )

    transcript = None

    try:
        transcript = speech_to_text(
            language=speech_lang,
            start_prompt="🎤 Start speaking",
            stop_prompt="⏹️ Stop recording",
            just_once=False,
            use_container_width=True,
            key=f"estate_mate_stt_{speech_lang}",
        )
    except Exception:
        st.warning(
            "Voice input unavailable. Try Chrome or type your question below."
        )

    if isinstance(transcript, str) and transcript.strip():
        st.session_state["voice_transcript"] = transcript.strip()

    with st.form("property_chat_form", clear_on_submit=True):
        question = st.text_input(
            "Type your question here",
            value=st.session_state.pop("voice_transcript", ""),
            placeholder="e.g. 2BHK in Vijayawada under 40 lakhs",
        )
        send_question = st.form_submit_button("Send")

    if send_question and question.strip():
        question = question.strip()
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        q = question.lower().replace("₹", " ").replace(",", " ")

        aliases = {
            "1BHK": ["1bhk", "1 bhk", "one bhk", "1 bedroom"],
            "2BHK": ["2bhk", "2 bhk", "two bhk", "2 bedroom"],
            "3BHK": ["3bhk", "3 bhk", "three bhk", "3 bedroom"],
            "Villa": ["villa", "villas", "independent house", "house"],
            "Plot": ["plot", "land", "open plot"],
        }

        requested_type = next(
            (
                kind for kind, words in aliases.items()
                if any(word in q for word in words)
            ),
            None,
        )

        requested_location = next(
            (
                p["location"] for p in PROPERTIES
                if p["location"].lower() in q
            ),
            None,
        )

        numbers = re.findall(r"\d+(?:\.\d+)?", q)
        max_price = None

        if numbers and any(
            word in q for word in
            ["under", "below", "within", "lakhs", "lakh", "lopu", "budget"]
        ):
            amounts = [
                float(n) for n in numbers
                if float(n) not in (1, 2, 3)
                or any(word in q for word in ["lakh", "lakhs", "under", "below"])
            ]
            if amounts:
                max_price = amounts[-1]

        matches = [
            p for p in PROPERTIES
            if (not requested_type or p["type"] == requested_type)
            and (not requested_location
                 or p["location"] == requested_location)
            and (max_price is None or p["price"] <= max_price)
        ]

        if matches:
            listing_lines = [
                f"- {p['name']}: {p['type']} in {p['location']} "
                f"— ₹{p['price']} lakhs"
                for p in matches
            ]
            reply = (
                "Here are matching fictional demo listings:\n\n"
                + "\n".join(listing_lines)
                + "\n\nThese are demo examples, not verified properties."
            )
        else:
            reply = (
                "I couldn't find a matching sample listing. "
                "Try: 2BHK in Vijayawada under 40 lakhs."
            )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )
        st.rerun()

    elif send_question:
        st.warning("Please type a question first.")


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div class="footer">
    ESTATEMATE · REAL ESTATE ENQUIRY DEMO<br>
    All listings and prices are fictional examples.
    Enquiries are saved to the configured database;
    they are not automatically sent to a real estate agent.
</div>
""", unsafe_allow_html=True)
