

import streamlit as st
import csv
import os
import re

FILE_NAME = "enquiries.csv"

PROPERTIES = [
    {"name": "Green Homes", "type": "2BHK",
     "location": "Vijayawada", "price": 30},
    {"name": "Sunrise Residency", "type": "3BHK",
     "location": "Vijayawada", "price": 45},
    {"name": "Happy Villas", "type": "Villa",
     "location": "Guntur", "price": 55},
    {"name": "City Plot", "type": "Plot",
     "location": "Vijayawada", "price": 18},
    {"name": "Budget Homes", "type": "1BHK",
     "location": "Vijayawada", "price": 15},
]

st.set_page_config(
    page_title="Real Estate AI Agent",
    page_icon="🏡"
)

st.title("🏡 Real Estate Enquiry Agent")
st.write("Find a property that matches your needs.")

st.divider()
st.subheader("📝 Submit a Property Enquiry")

with st.form("enquiry_form"):
    name = st.text_input("Your name")
    phone = st.text_input("Phone number")
    property_type = st.selectbox(
        "Property type",
        ["1BHK", "2BHK", "3BHK", "Villa", "Plot"]
    )
    location = st.text_input("Preferred location")
    budget = st.selectbox(
        "Your budget",
        [
            "Below ₹20 lakhs",
            "₹20–40 lakhs",
            "₹40–60 lakhs",
            "₹60 lakhs–₹1 crore",
            "Above ₹1 crore"
        ]
    )

    submitted = st.form_submit_button("Submit Enquiry")

if submitted:
    if not name.strip() or not location.strip() or not phone.strip():
        st.error("Please fill in all the fields.")
    elif not phone.strip().isdigit() or len(phone.strip()) != 10:
        st.error("Enter a valid 10-digit phone number.")
    else:
        file_exists = os.path.isfile(FILE_NAME)

        with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists or os.path.getsize(FILE_NAME) == 0:
                writer.writerow([
                    "Customer Name", "Phone Number",
                    "Property Type", "Location", "Budget"
                ])

            writer.writerow([
                name.strip(), phone.strip(),
                property_type, location.strip(), budget
            ])

        st.success("Enquiry saved successfully!")

        limits = {
            "Below ₹20 lakhs": (0, 20),
            "₹20–40 lakhs": (20, 40),
            "₹40–60 lakhs": (40, 60),
            "₹60 lakhs–₹1 crore": (60, 100),
            "Above ₹1 crore": (100, float("inf"))
        }

        low, high = limits[budget]

        matches = [
            p for p in PROPERTIES
            if p["type"] == property_type
            and location.strip().lower() in p["location"].lower()
            and low <= p["price"] < high
        ]

        st.subheader("🏠 Matching Sample Properties")

        if matches:
            for p in matches:
                st.write(
                    f"**{p['name']}** — {p['type']}, "
                    f"{p['location']}, ₹{p['price']} lakhs"
                )
        else:
            st.info("No sample property matches all your preferences.")

        st.caption(
            "Demo listings only. These properties and prices are fictional."
        )

st.divider()
st.subheader("💬 Property Chat Assistant")
st.write("Example: I want a 2BHK in Vijayawada under 40 lakhs.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask about properties...")

if question:
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    q = question.lower()
    requested_type = None

    for t in ["1bhk", "2bhk", "3bhk", "villa", "plot"]:
        if t in q:
            requested_type = t.upper()
            break

    requested_location = None
    for p in PROPERTIES:
        if p["location"].lower() in q:
            requested_location = p["location"]
            break

    numbers = re.findall(r"\d+", q)
    max_price = int(numbers[-1]) if numbers and (
        "under" in q or "below" in q or "within" in q
    ) else None

    matches = [
        p for p in PROPERTIES
        if (not requested_type or p["type"].lower() == requested_type.lower())
        and (not requested_location or
             p["location"].lower() == requested_location.lower())
        and (max_price is None or p["price"] <= max_price)
    ]

    if matches:
        reply = "Here are sample properties matching your request:\n\n"
        for p in matches:
            reply += (
                f"- {p['name']}: {p['type']} in {p['location']}, "
                f"₹{p['price']} lakhs\n"
            )
        reply += "\nThese are fictional demo listings, not verified properties."
    else:
        reply = (
            "I couldn't find a matching sample property. "
            "Try asking for a 2BHK in Vijayawada under 40 lakhs."
        )

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()