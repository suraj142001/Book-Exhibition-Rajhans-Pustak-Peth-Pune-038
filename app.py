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
# SIDEBAR (ORDER FORMAT UPDATED)
# =========================
with st.sidebar:
    st.markdown("## राजहंस पुस्तक पेठ")
    st.markdown("### 📚 आपण निवडलेली पुस्तके")

    total = 0
    order_text = ""
    sr = 1
    empty = True

    for item_name, item in st.session_state.cart.items():
        qty = item["qty"]

        if qty > 0:
            empty = False
            price = item["data"]['सवलतीत']
            subtotal = price * qty

            st.markdown(f"{sr}. **{item_name}**")
            st.caption(f"{qty} x ₹{price} = ₹{subtotal}")

            total += subtotal
            order_text += f"{sr}. {item_name} x {qty} = ₹{subtotal}\n"
            sr += 1

    if empty:
        st.info("अजून पुस्तक निवडलेले नाही")

    st.divider()
    st.success(f"एकूण: ₹{total}")

    st.markdown("### 🧾 ऑर्डर")

    name_input = st.text_input("नाव")
    phone_input = st.text_input("फोन")
    address_input = st.text_area("पत्ता")
    pincode_input = st.text_input("पिनकोड")

    if st.button("📲 WhatsApp वर ऑर्डर करा"):

        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("कृपया सर्व माहिती भरा")

        elif total == 0:
            st.error("किमान एक पुस्तक निवडा")

        else:
            message = f"""
 नमस्कार 🙏

ऑर्डर:

नाव: {name_input}
फोन: {phone_input}
पत्ता: {address_input}
पिनकोड: {pincode_input}

पुस्तके:
{order_text}

Total: ₹{total}
"""

            url = f"https://wa.me/919322630703?text={urllib.parse.quote(message)}"
            st.markdown(f"[👉 WhatsApp उघडा]({url})")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1,5])

with col1:
    st.image("logo.jpg", width=300)

with col2:
    st.markdown("### 📚 राजहंस पुस्तक पेठ")
    st.caption("📞 9322630703")

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
# PAGINATION
# =========================
items_per_page = 8

if "page" not in st.session_state:
    st.session_state.page = 1

total_pages = max(1, (len(filtered)-1)//items_per_page + 1)

start = (st.session_state.page - 1) * items_per_page
end = start + items_per_page

page_data = filtered.iloc[start:end]

# =========================
# BOOK LIST
# =========================
st.markdown("### 📚 पुस्तके")

for i, row in page_data.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()
    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    col1, col2, col3 = st.columns([5,2,2])

    with col1:
        st.write(f"**{name}**")
        st.caption(f"{row['लेखक']} | ₹{row['किंमत']} → ₹{row['सवलतीत']}")

    with col2:
        st.write(f"Qty: {qty}")

    with col3:
        c1, c2 = st.columns(2)

        with c1:
            if st.button("➖", key=f"m{i}"):
                if qty > 0:
                    st.session_state.cart[name]["qty"] -= 1
                    st.rerun()

        with c2:
            if st.button("➕", key=f"p{i}"):
                st.session_state.cart[name]["qty"] += 1
                st.rerun()

    st.divider()

# =========================
# PAGINATION BUTTONS
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ मागे"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()

with col2:
    st.markdown(f"### Page {st.session_state.page} / {total_pages}")

with col3:
    if st.button("पुढे ➡️"):
        if st.session_state.page < total_pages:
            st.session_state.page += 1
            st.rerun()
