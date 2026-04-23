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
# SIDEBAR (UPDATED)
# =========================
with st.sidebar:

    st.title("🛒 आपण निवडलेली पुस्तके")

    total = 0
    order_text = ""

    has_items = False

    for item_name, item in st.session_state.cart.items():
        qty = item["qty"]

        if qty > 0:
            has_items = True
            price = item["data"]['सवलतीत']
            subtotal = price * qty

            st.write(f"📖 {item_name}")
            st.caption(f"{qty} x ₹{price} = ₹{subtotal}")

            total += subtotal
            order_text += f"{item_name} x {qty} = ₹{subtotal}%0A"

    if not has_items:
        st.info("अजून पुस्तक निवडलेले नाही")

    st.divider()
    st.success(f"Total: ₹{total}")

    # =========================
    # CUSTOMER INFO
    # =========================
    st.markdown("### 🧾 तुमची माहिती")

    name_input = st.text_input("नाव")
    phone_input = st.text_input("फोन")
    address_input = st.text_area("पत्ता")
    pincode_input = st.text_input("पिनकोड")

    # =========================
    # WHATSAPP ORDER
    # =========================
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

            url = f"https://wa.me/919322630703?text={urllib.parse.quote(message)}"

            st.success("👉 खाली क्लिक करा")
            st.markdown(f"[📲 WhatsApp उघडा]({url})")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1,5])

with col1:
    st.image("logo.jpg", width=70)

with col2:
    st.markdown("### 📚 राजहंस पुस्तक पेठ")
    st.caption("📞 9322630703")

# =========================
# SEARCH
# =========================
search = st.text_input("🔎 शोधा")

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
# PAGINATION BOTTOM
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
