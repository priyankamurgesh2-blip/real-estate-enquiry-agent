


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

