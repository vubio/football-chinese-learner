import streamlit as st
from supabase import create_client, Client

# --- 1. INITIALIZE SUPABASE CONNECTION ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- 2. FETCH DATA ---
@st.cache_data(ttl=600) # Caches the data for 10 minutes to save API calls
def fetch_vocab():
    # Including 'created_at' as requested, alongside the new 'hanzi' and 'pinyin' columns
    response = supabase.table("vocab_chinese").select("id, created_at, topic, hanzi, pinyin, en, status").execute()
    return response.data

# --- 3. MAIN UI ---
st.title("⚽ Football Chinese Coach")

vocab_data = fetch_vocab()

if vocab_data:
    for row in vocab_data:
        with st.container():
            st.markdown(f"### {row['hanzi']}")
            st.write(f"**Pinyin:** {row['pinyin']}")
            st.write(f"**English:** {row['en']}")
            
            # Displaying extra metadata at the bottom of each card
            st.caption(f"Topic: {row['topic']} | Status: {row['status']} | Added: {row['created_at'][:10]}")
            st.divider()
else:
    st.info("No vocabulary found yet. Add some rows to your 'vocab_chinese' table in Supabase!")