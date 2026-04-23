import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.jpg", width=900)

with col2:
    st.title("📚 राजहंस पुस्तक पेठ, पुणे ०३८")
    st.write("📞 9322630703")

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
# CART (DICT FORMAT)
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}   # {book_name: {data + qty}}

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
# BOOK LIST
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

for i, row in filtered.iterrows():

    # Skip invalid
    if pd.isna(row['पुस्तकाचे नाव']):
        continue

    name = str(row['पुस्तकाचे नाव']).strip()

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    col1, col2, col3, col4, col5 = st.columns([3,2,2,2,2])

    with col1:
        st.write(f"📖 **{name}**")

    with col2:
        st.write(f"✍️ {row['लेखक']}")

    with col3:
        st.write(f"₹{row['किंमत']}")

    with col4:
        st.write(f"🔥 ₹{row['सवलतीत']}")

    # ✅ FIXED BUTTON UI
    with col5:
        qty = st.session_state.cart[name]["qty"]

        c1, c2, c3 = st.columns([1,1,1])

        with c1:
            if st.button("➖", key=f"minus_{i}"):
                if qty > 0:
                    st.session_state.cart[name]["qty"] -= 1
                    st.rerun()

        with c2:
            st.markdown(f"### {st.session_state.cart[name]['qty']}")

        with c3:
            if st.button("➕", key=f"plus_{i}"):
                st.session_state.cart[name]["qty"] += 1
                st.rerun()

    st.divider()
# =========================
# CUSTOMER INFO
# =========================
st.subheader("🧾 तुमची माहिती")

name_input = st.text_input("आपले नाव")
phone_input = st.text_input("फोन नंबर")
address_input = st.text_area("पत्ता")
pincode_input = st.text_input("पिन कोड")

# =========================
# CART VIEW
# =========================
st.subheader("🛒 तुमची ऑर्डर")

total = 0
order_text = ""

for item_name, item in st.session_state.cart.items():
    qty = item["qty"]

    if qty > 0:
        price = item["data"]['सवलतीत']
        subtotal = price * qty

        st.write(f"{item_name} x {qty} = ₹{subtotal}")

        total += subtotal
        order_text += f"{item_name} x {qty} = ₹{subtotal}%0A"

st.success(f"Total: ₹{total}")

# =========================
# WHATSAPP ORDER (VALIDATION)
# =========================
phone = "919322630703"

if st.button("📲 WhatsApp वर ऑर्डर करा"):

    if not name_input or not phone_input or not address_input or not pincode_input:
        st.error("⚠️ कृपया सर्व माहिती भरा")
    
    elif total == 0:
        st.error("⚠️ कृपया किमान एक पुस्तक निवडा")
    
    else:
        message = f"""
नमस्कार,

नाव: {name_input}
फोन: {phone_input}
पत्ता: {address_input}
पिनकोड: {pincode_input}

मला खालील पुस्तके हवी आहेत:

{order_text}

Total: ₹{total}
"""

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"

        st.success("Redirecting to WhatsApp...")

        st.markdown(f"[👉 इथे क्लिक करा]({whatsapp_url})")










for i, row in filtered.iterrows():

    name = str(row['पुस्तकाचे नाव'])

    # ❌ skip invalid rows
    if pd.isna(row['पुस्तकाचे नाव']):
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}
