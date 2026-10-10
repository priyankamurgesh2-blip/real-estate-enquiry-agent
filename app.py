
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
div[data-testid="stChatMessage"] { border-radius:16px; }
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
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    question = st.chat_input("Ask about sample properties...")
    if question:
        st.session_state.chat_history.append({"role":"user","content":question})
        q = question.lower()
        requested_type = next((t for t in ["1bhk","2bhk","3bhk","villa","plot"] if t in q), None)
        requested_location = next((p["location"] for p in PROPERTIES if p["location"].lower() in q), None)
        numbers = re.findall(r"\d+", q)
        max_price = int(numbers[-1]) if numbers and any(word in q for word in ["under","below","within","less than","budget"]) else None
        matches = [p for p in PROPERTIES if (not requested_type or p["type"].lower() == requested_type) and (not requested_location or p["location"].lower() == requested_location.lower()) and (max_price is None or p["price"] <= max_price)]
        if matches:
            reply = "Here are matching fictional demo listings:\n\n" + "\n".join([f"- {p['name']}: {p['type']} in {p['location']}, ₹{p['price']} lakhs" for p in matches]) + "\n\nThese are demo examples, not verified properties."
        else:
            reply = "I couldn't find a matching sample listing. Try: “2BHK in Vijayawada under 40 lakhs.”"
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()

st.divider()
st.markdown('<div class="footer">ESTATEMATE · REAL ESTATE ENQUIRY DEMO<br>All listings and prices are fictional examples. No enquiries are sent to a real estate agent.</div>', unsafe_allow_html=True)
