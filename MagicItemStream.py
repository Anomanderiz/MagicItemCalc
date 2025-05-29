# save as app.py
import streamlit as st
import random

st.set_page_config(page_title="Magic Item Valuator")

st.title("🧙‍♂️ Mystic Market Valuator")

rarity = st.selectbox("Choose item rarity:", ["Common", "Uncommon", "Rare", "Very Rare"])
discount = st.slider("Discount (%)", 0, 100, 0)

# Roll price once and store it
if "base_price" not in st.session_state or st.button("Re-roll Price"):
    def roll_price(r):
        if r == "Common":
            return (random.randint(1, 6) + 1) * 10
        elif r == "Uncommon":
            base = random.randint(1, 6) * 100
            markup = random.choice([0, 0.10, 0.15])
            return int(base * (1 + markup))
        elif r == "Rare":
            base = (random.randint(1, 10) + random.randint(1, 10)) * 1000
            markup = random.uniform(0.10, 0.15)
            return int(base * (1 + markup))
        elif r == "Very Rare":
            base = (random.randint(1, 4) + 1) * 10000
            markup = random.uniform(0.10, 0.15)
            return int(base * (1 + markup))
        return 0

    st.session_state.base_price = roll_price(rarity)

base = st.session_state.get("base_price", 0)
final = int(base * (1 - discount / 100))

st.markdown(f"**Base Price:** {base:,} gp")
st.markdown(f"**Final Price after {discount}% discount:** {final:,} gp")
