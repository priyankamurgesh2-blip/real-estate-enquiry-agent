
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
    if "chat_draft_input" not in st.session_state:
        st.session_state.chat_draft_input = ""

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
        st.session_state.chat_draft_input = transcript.strip()

    with st.form("property_chat_form", clear_on_submit=True):
        chat_col, send_col = st.columns([5, 1])
        with chat_col:
            question = st.text_input(
                "Type your question here",
                key="chat_draft_input",
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
        # clear_on_submit=True clears the form without modifying widget state here.
        st.rerun()
    elif send_question:
        st.warning("Please type a question first / Dayachesi question type cheyyandi.")

st.divider()
st.markdown('<div class="footer">ESTATEMATE · REAL ESTATE ENQUIRY DEMO<br>All listings and prices are fictional examples. No enquiries are sent to a real estate agent.</div>', unsafe_allow_html=True)
