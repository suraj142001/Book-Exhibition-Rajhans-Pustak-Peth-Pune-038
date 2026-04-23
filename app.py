import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# HEADER (LOGO + SHOP INFO)
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.jpg", width=900)   # 👉 तुमचा logo.jpg project मध्ये ठेवा

with col2:
    st.title("📚 राजहंस पुस्तक पेठ, पुणे ०३८")
    st.write("📞 संपर्क: 9322630703")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

df = load_data()

# =========================
# CART
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# SEARCH
# =========================
search = st.text_input("🔎 पुस्तक शोधा")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

# =========================
# BOOK LIST (TABLE STYLE)
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

for i, row in filtered.iterrows():

    col1, col2, col3, col4, col5 = st.columns([3,2,2,2,2])

    with col1:
        st.write(f"📖 **{row['पुस्तकाचे नाव']}**")

    with col2:
        st.write(f"✍️ {row['लेखक']}")

    with col3:
        st.write(f"₹{row['किंमत']}")

    with col4:
        st.write(f"🔥 ₹{row['सवलतीत']}")

    with col5:
        if st.button("🛒 Add", key=i):
            st.session_state.cart.append(row)

    st.divider()

# =========================
# CART VIEW
# =========================
st.subheader("🛒 तुमची ऑर्डर")

total = 0
order_text = ""

for item in st.session_state.cart:
    st.write(f"{item['पुस्तकाचे नाव']} - ₹{item['सवलतीत']}")
    total += item['सवलतीत']
    order_text += f"{item['पुस्तकाचे नाव']} - ₹{item['सवलतीत']}%0A"

st.success(f"Total: ₹{total}")

# =========================
# DIRECT WHATSAPP ORDER
# =========================
phone = "919322630703"   # ✅ तुमचा नंबर

message = f"""नमस्कार,
मला खालील पुस्तके हवी आहेत:

{order_text}

Total: ₹{total}
"""

encoded_message = urllib.parse.quote(message)

whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

# 👉 BIG BUTTON
st.markdown(
    f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            padding:15px 25px;
            border:none;
            border-radius:10px;
            font-size:18px;
            cursor:pointer;">
            📲 WhatsApp वर ऑर्डर करा
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
