

import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text
import re
import json

st.set_page_config(
    page_title="EstateMate | Property Finder",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROPERTIES = [
    {"name": "Green Homes", "type": "2BHK", "location": "Vijayawada", "price": 30, "tag": "Popular choice", "description": "Comfortable family living with practical space."},
    {"name": "Sunrise Residency", "type": "3BHK", "location": "Vijayawada", "price": 45, "tag": "Family favourite", "description": "Extra room for growing families and guests."},
    {"name": "Happy Villas", "type": "Villa", "location": "Guntur", "price": 55, "tag": "More space", "description": "A spacious villa-style sample listing."},
    {"name": "City Plot", "type": "Plot", "location": "Vijayawada", "price": 18, "tag": "Build your plan", "description": "A sample plot listing for your future project."},
    {"name": "Budget Homes", "type": "1BHK", "location": "Vijayawada", "price": 15, "tag": "Budget pick", "description": "A compact sample home for simple living."},
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#142b27; --muted:#65756f; --green:#176b52; --mint:#eaf5ef; --gold:#e7b86b; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#f6faf7 0%,#ffffff 52%,#f6faf7 100%); color:var(--ink); }
.block-container { max-width:1180px; padding-top:1.7rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:var(--ink) !important; }
.hero { padding:2.6rem 2.6rem 2.2rem; border-radius:28px; background:linear-gradient(125deg,#123b31,#176b52 65%,#34866b); color:white; position:relative; overflow:hidden; margin-bottom:1.3rem; }
.hero:after { content:'⌂'; position:absolute; right:4%; top:-55px; font-size:230px; color:rgba(255,255,255,.07); font-family:serif; }
.eyebrow { color:#c7ead7; text-transform:uppercase; letter-spacing:2px; font-size:.76rem; font-weight:700; }
.hero h1 { color:white !important; font-size:clamp(2rem,4vw,3.5rem) !important; line-height:1.12; margin:.7rem 0; }
.hero p { color:#e5f2eb; font-size:1.04rem; max-width:640px; }
.pill { display:inline-block; padding:.42rem .8rem; border:1px solid rgba(255,255,255,.35); border-radius:99px; margin:.3rem .3rem 0 0; color:white; font-size:.82rem; }
.section-kicker { color:var(--green); text-transform:uppercase; letter-spacing:1.6px; font-size:.75rem; font-weight:800; margin-bottom:.35rem; }
.section-note { color:var(--muted); margin-top:-.5rem; margin-bottom:1rem; }
.property { background:white; border:1px solid #e1ebe5; border-radius:20px; padding:1.25rem; box-shadow:0 8px 25px rgba(20,60,45,.045); min-height:205px; }
.property-top { display:flex; justify-content:space-between; gap:.6rem; align-items:center; }
.property-icon { width:46px; height:46px; display:flex; align-items:center; justify-content:center; border-radius:14px; background:#eaf5ef; font-size:1.4rem; }
.tag { background:#f3f7ef; color:#28644e; padding:.35rem .55rem; border-radius:99px; font-size:.72rem; font-weight:700; }
.property h3 { margin:.9rem 0 .2rem; font-size:1.12rem; }
.meta { color:#65756f; font-size:.88rem; }
.price { font-family:'Manrope',sans-serif; color:#176b52; font-size:1.45rem; font-weight:800; margin-top:.7rem; }
.price small { font-size:.78rem; font-weight:500; color:#65756f; }
.info-card { border:1px solid #e1ebe5; border-radius:20px; background:white; padding:1.3rem; }
div[data-testid="stForm"] { background:white; border:1px solid #e1ebe5; padding:1.2rem; border-radius:18px; }
.stButton > button, div[data-testid="stFormSubmitButton"] button { border-radius:12px; border:0; background:#176b52; color:white; font-weight:700; padding:.65rem 1rem; }
.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover { background:#104d3c; color:white; }
input, textarea, [data-baseweb="select"] > div { border-radius:10px !important; }

/* Keep typed chat text visible before pressing Send */
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] input {
    color: #142b27 !important;
    -webkit-text-fill-color: #142b27 !important;
    background-color: #ffffff !important;
    caret-color: #176b52 !important;
    opacity: 1 !important;
}
div[data-testid="stChatInput"] textarea::placeholder,
div[data-testid="stChatInput"] input::placeholder {
    color: #65756f !important;
    -webkit-text-fill-color: #65756f !important;
    opacity: 1 !important;
}
div[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #b8d5c4 !important;
    border-radius: 14px !important;
}
div[data-testid="stForm"] input {
    color: #142b27 !important;
    -webkit-text-fill-color: #142b27 !important;
    background: #ffffff !important;
    caret-color: #176b52 !important;
    opacity: 1 !important;
}
div[data-testid="stForm"] input::placeholder {
    color: #65756f !important;
    -webkit-text-fill-color: #65756f !important;
    opacity: 1 !important;
}


/* Make chat messages readable without clicking */
div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #d9e8df !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    color: #142b27 !important;
    box-shadow: 0 4px 14px rgba(20,60,45,.06) !important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div,
div[data-testid="stChatMessage"] li {
    color: #142b27 !important;
    opacity: 1 !important;
    visibility: visible !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #142b27 !important;
    opacity: 1 !important;
}
div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    background-color: #dcefe4 !important;
}
div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background-color: #176b52 !important;
}

.footer { text-align:center; color:#718079; padding:1.5rem .5rem .3rem; font-size:.82rem; }
hr { border-color:#e4ece7; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">A simpler way to find your next place</div>
  <h1>Find a place that<br>feels like home.</h1>
  <p>Share what you need, explore matching sample listings, and ask our property assistant for a quick starting point.</p>
  <span class="pill">🏡 Homes</span><span class="pill">📍 Local search</span><span class="pill">💬 Quick enquiries</span>
</div>
""", unsafe_allow_html=True)

# Overview metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="info-card"><div class="section-kicker">Sample listings</div><h2 style="margin:0">05</h2><div class="meta">Demo properties to explore</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="info-card"><div class="section-kicker">Locations</div><h2 style="margin:0">02</h2><div class="meta">Vijayawada and Guntur</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="info-card"><div class="section-kicker">Your next step</div><h2 style="margin:0">01</h2><div class="meta">Tell us your requirements</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="section-kicker">Explore the collection</div><h2 style="margin-top:0">Sample properties</h2><div class="section-note">Use the filters to narrow the demo listings.</div>', unsafe_allow_html=True)
f1, f2 = st.columns([1, 1])
with f1:
    filter_location = st.selectbox("Filter by location", ["All locations", "Vijayawada", "Guntur"])
with f2:
    filter_type = st.selectbox("Filter by property type", ["All types", "1BHK", "2BHK", "3BHK", "Villa", "Plot"])

visible = [p for p in PROPERTIES if (filter_location == "All locations" or p["location"] == filter_location) and (filter_type == "All types" or p["type"] == filter_type)]
cards = st.columns(3)
icons = {"1BHK":"🏠", "2BHK":"🏡", "3BHK":"🏘️", "Villa":"🏰", "Plot":"🌳"}
for i, p in enumerate(visible):
    with cards[i % 3]:
        st.markdown(f"""
        <div class="property">
          <div class="property-top"><div class="property-icon">{icons.get(p['type'],'🏡')}</div><span class="tag">{p['tag']}</span></div>
          <h3>{p['name']}</h3>
          <div class="meta">📍 {p['location']} &nbsp;·&nbsp; {p['type']}</div>
          <div class="price">₹{p['price']} lakhs <small>indicative demo price</small></div>
          <p class="meta">{p['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
if not visible:
    st.info("No sample listings match these filters.")

st.divider()
left, right = st.columns([1.05, .95], gap="large")
with left:
    st.markdown('<div class="section-kicker">Tell us what you need</div><h2 style="margin-top:0">Submit an enquiry</h2><div class="section-note">Fill in the form and we will show matching demo listings.</div>', unsafe_allow_html=True)
    with st.form("enquiry_form", clear_on_submit=False):
        name = st.text_input("Your name")
        phone = st.text_input("Phone number", max_chars=10, help="Use a 10-digit number for this demo.")
        property_type = st.selectbox("Property type", ["1BHK", "2BHK", "3BHK", "Villa", "Plot"])
        location = st.text_input("Preferred location", placeholder="e.g. Vijayawada")
        budget = st.selectbox("Your budget", ["Below ₹20 lakhs", "₹20–40 lakhs", "₹40–60 lakhs", "₹60 lakhs–₹1 crore", "Above ₹1 crore"])
        submitted = st.form_submit_button("Find matching properties", use_container_width=True)

    if submitted:
        clean_name, clean_phone, clean_location = name.strip(), phone.strip(), location.strip()
        if not clean_name or not clean_location or not clean_phone:
            st.error("Please fill in all fields.")
        elif not clean_phone.isdigit() or len(clean_phone) != 10:
            st.error("Please enter a valid 10-digit phone number.")
        else:
            limits = {"Below ₹20 lakhs": (0,20), "₹20–40 lakhs": (20,40), "₹40–60 lakhs": (40,60), "₹60 lakhs–₹1 crore": (60,100), "Above ₹1 crore": (100,float("inf"))}
            low, high = limits[budget]
            matches = [p for p in PROPERTIES if p["type"] == property_type and clean_location.lower() in p["location"].lower() and low <= p["price"] < high]
            st.session_state["latest_enquiry"] = {"name": clean_name, "type": property_type, "location": clean_location, "budget": budget}
            st.success("Thanks! Your demo enquiry has been received in this session.")
            st.markdown("#### Matching sample properties")
            if matches:
                for p in matches:
                    st.write(f"**{p['name']}** — {p['type']} · {p['location']} · ₹{p['price']} lakhs")
            else:
                st.info("No sample property matches every preference. Try another location or budget.")
            st.caption("Demo only: this version does not store enquiries permanently or send them to an agent.")

with right:
    st.markdown('<div class="section-kicker">Ask a question</div><h2 style="margin-top:0">Property assistant</h2><div class="section-note">Try: “I want a 2BHK in Vijayawada under 40 lakhs.”</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">💬 Ask about property type, location, or maximum budget. Replies use fictional demo listings.</div>', unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg_index, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant":
                spoken_text = json.dumps(message["content"], ensure_ascii=False)
                voice_locale = "te-IN" if any("\u0c00" <= ch <= "\u0c7f" for ch in message["content"]) else "en-IN"
                voice_html = f"""
                <div style="font-family:Arial,sans-serif;margin:4px 0 8px;">
                  <button id="speak-{msg_index}" style="background:#176b52;color:white;border:0;border-radius:10px;padding:9px 13px;font-size:14px;cursor:pointer;">
                    🔊 Read answer aloud
                  </button>
                  <button id="stop-{msg_index}" style="background:#eaf5ef;color:#142b27;border:1px solid #c9dfd1;border-radius:10px;padding:9px 13px;font-size:14px;cursor:pointer;margin-left:6px;">
                    ⏹ Stop
                  </button>
                  <span id="status-{msg_index}" style="color:#43574f;font-size:12px;margin-left:6px;"></span>
                </div>
                <script>
                const answerText = {spoken_text};
                const lang = "{voice_locale}";
                const speakBtn = document.getElementById("speak-{msg_index}");
                const stopBtn = document.getElementById("stop-{msg_index}");
                speakBtn.onclick = () => {{
                  if (!("speechSynthesis" in window)) {{
                    document.getElementById("status-{msg_index}").textContent = "Speech playback is not supported in this browser.";
                    return;
                  }}
                  window.speechSynthesis.cancel();
                  const utterance = new SpeechSynthesisUtterance(answerText);
                  utterance.lang = lang;
                  utterance.rate = 0.9;
                  utterance.onstart = () => document.getElementById("status-{msg_index}").textContent = "Speaking…";
                  utterance.onend = () => document.getElementById("status-{msg_index}").textContent = "";
                  window.speechSynthesis.speak(utterance);
                }};
                stopBtn.onclick = () => {{ window.speechSynthesis.cancel(); document.getElementById("status-{msg_index}").textContent = ""; }};
                </script>
                """
                components.html(voice_html, height=58)
    # Voice language and microphone input (browser speech recognition).
    if "chat_draft" not in st.session_state:
        st.session_state.chat_draft = ""

    voice_language = st.selectbox(
        "Voice language / మాట్లాడే భాష",
        options=["Telugu (తెలుగు)", "English"],
        key="voice_language_choice",
    )
    speech_lang = "te-IN" if voice_language.startswith("Telugu") else "en-IN"
    st.caption("🎤 Tap Start speaking, allow microphone access, speak, then review the text before sending.")

    try:
        transcript = speech_to_text(
            language=speech_lang,
            start_prompt="🎤 Start speaking",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key=f"estate_mate_stt_{speech_lang}",
        )
    except Exception:
        transcript = None
        st.info("Voice input is not available in this browser right now. You can type your question below.")

    if transcript and transcript.strip():
        st.session_state.chat_draft = transcript.strip()

    with st.form("property_chat_form", clear_on_submit=True):
        chat_col, send_col = st.columns([5, 1])
        with chat_col:
            question = st.text_input(
                "Type your question here",
                key="chat_draft",
                placeholder="e.g. 2BHK in Vijayawada under 40 lakhs",
                label_visibility="collapsed",
            )
        with send_col:
            send_question = st.form_submit_button("Send", use_container_width=True)

    if send_question and question.strip():
        question = question.strip()
        st.session_state.chat_history.append({"role": "user", "content": question})
        q = question.lower().replace("₹", " ").replace(",", " ")

        # Understand English and common Telugu-in-English (transliterated) phrases.
        type_aliases = {
            "1bhk": ["1bhk", "1 bhk", "one bhk", "1 bedroom", "one bedroom", "oka bhk", "1 bed room"],
            "2bhk": ["2bhk", "2 bhk", "two bhk", "2 bedroom", "two bedroom", "rendu bhk", "2 bed room"],
            "3bhk": ["3bhk", "3 bhk", "three bhk", "3 bedroom", "three bedroom", "moodu bhk", "3 bed room"],
            "Villa": ["villa", "villas", "independent house", "separate house", "illuu", "illu", "house"],
            "Plot": ["plot", "land", "open plot", "place to build"]
        }
        requested_type = next((kind for kind, aliases in type_aliases.items() if any(alias in q for alias in aliases)), None)

        requested_location = next((p["location"] for p in PROPERTIES if p["location"].lower() in q), None)
        # Common location phrasing such as "Vijayawada lo" is covered by substring matching.
        number_matches = re.findall(r"\d+(?:\.\d+)?", q)
        budget_words = ["under", "below", "within", "less than", "budget", "lakhs", "lakh", "lo", "lopu", "varaku", "less", "cheap", "affordable", "takkuva", "budget lo"]
        max_price = None
        if number_matches and any(word in q for word in budget_words):
            # Avoid treating a bedroom count (1/2/3) as the budget when another amount exists.
            amounts = [float(n) for n in number_matches if float(n) not in (1, 2, 3) or any(w in q for w in ["lakh", "lakhs", "budget", "under", "below", "within", "lo", "lopu", "varaku"])]
            if amounts:
                max_price = amounts[-1]

        matches = [p for p in PROPERTIES
                   if (not requested_type or p["type"].lower() == requested_type.lower())
                   and (not requested_location or p["location"].lower() == requested_location.lower())
                   and (max_price is None or p["price"] <= max_price)]

        telugu_style = any(word in q for word in ["kavali", "kavali", "cheppu", "chupinchu", "undi", "lo", "naaku", "naku", "manchi", "takkuva", "entha", "ekkada", "ledu", "ivvu"])
        if matches:
            listing_lines = [f"- {p['name']}: {p['type']} in {p['location']} — ₹{p['price']} lakhs" for p in matches]
            if telugu_style:
                reply = "Mee requirements ki match ayye sample properties ఇవి / Here are matching sample properties:\n\n" + "\n".join(listing_lines) + "\n\nIvi demo examples maatrame; verified properties kaavu. These are fictional examples, not verified listings."
            else:
                reply = "Here are matching fictional demo listings:\n\n" + "\n".join(listing_lines) + "\n\nThese are demo examples, not verified properties."
        else:
            if telugu_style:
                reply = "Ee requirements ki matching sample property dorakaledu. Vere location/budget try cheyyandi. Example: ‘2BHK Vijayawada lo 40 lakhs lopu kavali’.\n\nI couldn't find a matching demo listing; try changing the type, location, or budget."
            else:
                reply = "I couldn't find a matching sample listing. Try: ‘2BHK in Vijayawada under 40 lakhs.’"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.chat_draft = ""
        st.rerun()
    elif send_question:
        st.warning("Please type a question first / Dayachesi question type cheyyandi.")

st.divider()
st.markdown('<div class="footer">ESTATEMATE · REAL ESTATE ENQUIRY DEMO<br>All listings and prices are fictional examples. No enquiries are sent to a real estate agent.</div>', unsafe_allow_html=True)
