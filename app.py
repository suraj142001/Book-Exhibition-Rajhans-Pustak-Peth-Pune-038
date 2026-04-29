import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# 🔥 CLEAN FUNCTION (IMPORTANT)
# =========================
def clean_price(col):
    return (
        col.astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace("/-", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8-sig")

    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 🔥 CLEAN PRICE (MAIN FIX)
    df['किंमत'] = pd.to_numeric(clean_price(df['किंमत']), errors='coerce').fillna(0)
    df['सवलतीत'] = pd.to_numeric(clean_price(df['सवलतीत']), errors='coerce').fillna(0)

    return df

df = load_data()

# =========================
# SESSION
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = 1

# =========================
# SIDEBAR CART
# =========================
with st.sidebar:
    st.markdown("## 🏪 राजहंस पुस्तक पेठ")
    st.markdown("### 🛒 Cart")

    total = 0
    order_text = ""
    sr = 1

    for name, item in st.session_state.cart.items():
        qty = item["qty"]

        if qty > 0:
            price = item["data"]['सवलतीत']
            subtotal = price * qty

            st.write(f"{sr}. {name}")
            st.caption(f"{qty} x ₹{int(price)} = ₹{int(subtotal)}")

            total += subtotal
            order_text += f"{sr}. {name} x {qty} = ₹{int(subtotal)}\n"
            sr += 1

    if total == 0:
        st.info("अजून पुस्तक निवडलेले नाही")

    st.divider()
    st.success(f"Total: ₹{int(total)}")

    # =========================
    # CUSTOMER
    # =========================
    name_input = st.text_input("नाव")
    phone_input = st.text_input("फोन")
    address_input = st.text_area("पत्ता")
    pincode_input = st.text_input("पिनकोड")

    if st.button("📲 WhatsApp Order"):
        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("सर्व माहिती भरा")
        elif total == 0:
            st.error("किमान 1 पुस्तक निवडा")
        else:
            msg = f"""
नमस्कार 🙏

नाव: {name_input}
फोन: {phone_input}
पत्ता: {address_input}
पिनकोड: {pincode_input}

📚 ऑर्डर:
{order_text}

एकूण: ₹{int(total)}
"""
            url = f"https://wa.me/919322630703?text={urllib.parse.quote(msg)}"
            st.markdown(f"[👉 WhatsApp उघडा]({url})")

# =========================
# HEADER
# =========================
st.title("📚 राजहंस पुस्तक पेठ")
st.caption("📞 9322630703")

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 Search Book")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

# =========================
# PAGINATION
# =========================
items_per_page = 10
total_pages = max(1, (len(filtered)-1)//items_per_page + 1)

start = (st.session_state.page - 1) * items_per_page
end = start + items_per_page

page_data = filtered.iloc[start:end]

# =========================
# BOOK LIST
# =========================
for i, row in page_data.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()
    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    col1, col2, col3 = st.columns([5,2,2])

    with col1:
        price = int(row['किंमत']) if row['किंमत'] > 0 else "-"
        offer = int(row['सवलतीत']) if row['सवलतीत'] > 0 else "-"

        st.write(f"**{name}**")
        st.caption(f"{row['लेखक']} | ₹{price} → ₹{offer}")

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
    if st.button("➡️ पुढे"):
        if st.session_state.page < total_pages:
            st.session_state.page += 1
            st.rerun()
