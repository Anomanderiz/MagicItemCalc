# save as app.py
import streamlit as st
import random

st.set_page_config(page_title="Magic Item Valuator")

st.title("🧙‍♂️ Mystic Market Valuator")

rarity = st.selectbox("Choose item rarity:", ["Common", "Uncommon", "Rare", "Very Rare"])
discount = st.slider("Manual Discount (%)", 0, 100, 0)

# Persuasion check input
persuasion_roll = st.number_input(
    "Persuasion check total (d20 + modifiers):",
    min_value=1,
    max_value=40,
    step=1,
    value=10,
    help="Only rolls of 15 or higher give a discount."
)

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

def persuasion_discount_from_roll(roll: int) -> int:
    """Return percentage discount from Persuasion roll."""
    if roll < 15:
        return 0
    if roll <= 17:
        return 5
    if roll <= 20:
        return 10
    if roll <= 23:
        return 15
    if roll <= 26:
        return 20
    if roll <= 29:
        return 25
    return 30  # 30+ is capped at 30%

# Roll price once and store it
if "base_price" not in st.session_state or st.button("Re-roll Price"):
    st.session_state.base_price = roll_price(rarity)

base = st.session_state.get("base_price", 0)

persuasion_discount = persuasion_discount_from_roll(int(persuasion_roll))

total_discount = discount + persuasion_discount
# Optional: uncomment to cap total discount at something saner
# total_discount = min(total_discount, 60)

final = int(base * (1 - total_discount / 100))

st.markdown(f"**Base Price:** {base:,} gp")
st.markdown(f"**Manual Discount:** {discount}%")
st.markdown(f"**Persuasion Discount from roll {int(persuasion_roll)}:** {persuasion_discount}%")
st.markdown(f"**Total Discount:** {total_discount}%")
st.markdown(f"**Final Price after discounts:** {final:,} gp")
