
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

/* Strong, always-visible form labels and input text */
.stApp label,
.stApp label p,
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stMarkdownContainer"] label {
    color: #142b27 !important;
    -webkit-text-fill-color: #142b27 !important;
    opacity: 1 !important;
    visibility: visible !important;
    font-weight: 700 !important;
}
.stApp input,
.stApp textarea {
    color: #142b27 !important;
    -webkit-text-fill-color: #142b27 !important;
    background-color: #ffffff !important;
    border: 1px solid #9ab9a8 !important;
    caret-color: #176b52 !important;
    opacity: 1 !important;
}
.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #65756f !important;
    -webkit-text-fill-color: #65756f !important;
    opacity: 1 !important;
}
.stApp [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #9ab9a8 !important;
}
.stApp [data-baseweb="select"] *,
.stApp [data-baseweb="select"] span {
    color: #142b27 !important;
    -webkit-text-fill-color: #142b27 !important;
    opacity: 1 !important;
}
.stApp [data-testid="stForm"] {
    background: #ffffff !important;
    border: 1px solid #c9ded1 !important;
    box-shadow: 0 8px 26px rgba(20,60,45,.07) !important;
}

