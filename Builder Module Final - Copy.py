import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# Load data (replace with your real files)
@st.cache_data
def load_data():
    promoter_df = pd.read_csv('promoters.csv')  # Must have 'promotername' column
    builder_df = pd.read_csv('builders.csv')    # Must have 'builderinfo_name' column
    return promoter_df['promotername'].dropna().unique().tolist(), builder_df['builderinfo_name'].dropna().unique().tolist()

promoter_names, builderinfo_names = load_data()

# Fuzzy match logic
def get_best_match(promoter_input, builder_list, threshold=70):
    match = process.extractOne(promoter_input, builder_list, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= threshold:
        return match[0], match[1]
    return None, 0

# Streamlit UI
st.title("🔍 Builder Info Finder")

user_input = st.text_input("Enter promoter name:", "")

if user_input:
    matched_name, score = get_best_match(user_input, builderinfo_names)
    if matched_name:
        st.success(f"✅ Best match: **{matched_name}** (Score: {score})")
    else:
        st.warning("⚠️ No good match found.")
