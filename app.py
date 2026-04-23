import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

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
    st.session_state.cart = {}

# =========================
# HEADER (COMPACT)
# =========================
left, right = st.columns([3,1])

with left:
    c1, c2 = st.columns([1,6])
    with c1:
        st.image("logo.jpg", width=80)
    with c2:
        st.markdown("## 📚 राजहंस पुस्तक पेठ, पुणे ०३८")
        st.markdown("📞 9322630703")

with right:
    st.markdown("### 🛒 ऑर्डर")

    total = 0
    order_text = ""

    for item_name, item in st.session_state.cart.items():
        qty = item["qty"]
        if qty > 0:
            price = item["data"]['सवलतीत']
            subtotal = price * qty
            total += subtotal
            order_text += f"{item_name} x {qty} = ₹{subtotal}%0A"
            st.write(f"{item_name} x {qty}")

    st.success(f"₹{total}")

    name_input = st.text_input("नाव", label_visibility="collapsed", placeholder="नाव")
    phone_input = st.text_input("फोन", label_visibility="collapsed", placeholder="फोन")
    address_input = st.text_area("पत्ता", label_visibility="collapsed", placeholder="पत्ता")
    pincode_input = st.text_input("पिनकोड", label_visibility="collapsed", placeholder="पिनकोड")

    if st.button("📲 ऑर्डर करा"):
        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("माहिती भरा")
        elif total == 0:
            st.error("पुस्तक निवडा")
        else:
            msg = f"""
नाव: {name_input}
फोन: {phone_input}
पत्ता: {address_input}
पिनकोड: {pincode_input}

{order_text}
Total: ₹{total}
"""
            url = f"https://wa.me/919322630703?text={urllib.parse.quote(msg)}"
            st.markdown(f"[👉 WhatsApp]({url})")

# =========================
# SEARCH + FILTER
# =========================
st.divider()

search = st.text_input("🔎 शोधा", placeholder="पुस्तकाचे नाव टाका")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

# =========================
# BOOK CARDS (COMPACT GRID)
# =========================
st.markdown("### 📚 पुस्तके")

cols = st.columns(4)  # 👉 4 per row = less scroll

for i, row in filtered.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()
    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    with cols[i % 4]:

        st.markdown(f"**{name}**")
        st.caption(row['लेखक'])

        st.markdown(f"~~₹{row['किंमत']}~~  **₹{row['सवलतीत']}**")

        c1, c2, c3 = st.columns([1,1,1])

        with c1:
            if st.button("➖", key=f"m{i}"):
                if qty > 0:
                    st.session_state.cart[name]["qty"] -= 1
                    st.rerun()

        with c2:
            st.markdown(f"**{st.session_state.cart[name]['qty']}**")

        with c3:
            if st.button("➕", key=f"p{i}"):
                st.session_state.cart[name]["qty"] += 1
                st.rerun()
