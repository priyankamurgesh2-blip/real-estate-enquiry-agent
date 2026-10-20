

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
