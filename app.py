import streamlit as st
import pandas as pd
import pickle
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

st.title("📚 राजहंस पुस्तक पेठ")

# =========================
# LOAD DATA (FIXED)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8-sig")
    
    # ✅ Clean column names
    df.columns = df.columns.str.strip()
    
    # ✅ Remove unwanted columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    return df

df = load_data()

# Debug (optional - first run)
# st.write(df.columns)

# =========================
# CART SYSTEM
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# SEARCH (SAFE)
# =========================
search = st.text_input("🔎 पुस्तक शोधा")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

# =========================
# BOOK DISPLAY
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

cols = st.columns(3)

for i, row in filtered.iterrows():
    with cols[i % 3]:
        st.markdown(f"### {row['पुस्तकाचे नाव']}")
        st.write(f"✍️ {row['लेखक']}")
        st.write(f"💰 ₹{row['किंमत']} → 🔥 ₹{row['सवलतीत']}")

        if st.button(f"🛒 Add {i}"):
            st.session_state.cart.append(row)

# =========================
# CART VIEW
# =========================
st.subheader("🛒 Cart")

total = 0
order_text = ""

for item in st.session_state.cart:
    st.write(item['पुस्तकाचे नाव'], "-", item['सवलतीत'])
    total += item['सवलतीत']
    order_text += f"{item['पुस्तकाचे नाव']}%0A"

st.success(f"Total: ₹{total}")

# =========================
# WHATSAPP ORDER
# =========================
phone = "91XXXXXXXXXX"  # तुमचा नंबर टाका

message = f"Hello, मला खालील पुस्तके हवी आहेत:%0A{order_text}%0ATotal: ₹{total}"
url = f"https://wa.me/{phone}?text={message}"

st.markdown(f"[📲 WhatsApp वर ऑर्डर करा]({url})")

# =========================
# COMBO OFFER
# =========================
st.subheader("🔥 Combo Offer")

if st.button("Generate Combo"):
    combo = df.sample(min(3, len(df)))
    combo_price = combo['सवलतीत'].sum()

    st.write(combo[['पुस्तकाचे नाव', 'सवलतीत']])
    st.success(f"Combo Price: ₹{combo_price} (Special Offer)")

# =========================
# DASHBOARD
# =========================
st.subheader("📊 Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Books", len(df))

with col2:
    st.metric("Avg Price", int(df['किंमत'].mean()))

# =========================
# FILE UPLOAD
# =========================
st.subheader("📥 Upload New Stock")

file = st.file_uploader("Upload CSV")

if file:
    new_df = pd.read_csv(file, encoding="utf-8-sig")
    new_df.columns = new_df.columns.str.strip()
    st.write(new_df.head())

# =========================
# AI MODEL
# =========================
st.subheader("🤖 AI Prediction")

try:
    model = pickle.load(open("model.pkl", "rb"))

    price = st.number_input("Price", 100)
    discount = st.number_input("Discount", 10)

    if st.button("Predict Demand"):
        pred = model.predict([[price, discount]])
        st.success(f"Demand Score: {pred[0]}")

except:
    st.warning("Model load झाला नाही")
