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
# HEADER + RIGHT PANEL
# =========================
left, right = st.columns([3,1])

with left:
    col1, col2 = st.columns([1,5])
    with col1:
        st.image("logo.jpg", width=100)
    with col2:
        st.title("📚 राजहंस पुस्तक पेठ, पुणे ०३८")
        st.write("📞 9322630703")

with right:
    st.markdown("### 🛒 तुमची ऑर्डर")

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

    st.success(f"Total: ₹{total}")

    st.markdown("### 🧾 तुमची माहिती")

    name_input = st.text_input("नाव")
    phone_input = st.text_input("फोन")
    address_input = st.text_area("पत्ता")
    pincode_input = st.text_input("पिनकोड")

    if st.button("📲 WhatsApp Order"):

        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("⚠️ सर्व माहिती भरा")

        elif total == 0:
            st.error("⚠️ पुस्तक निवडा")

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
            encoded = urllib.parse.quote(message)
            url = f"https://wa.me/919322630703?text={encoded}"

            st.markdown(f"[👉 WhatsApp उघडा]({url})")

# =========================
# SEARCH + FILTER
# =========================
st.divider()

search = st.text_input("🔎 पुस्तक शोधा")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

authors = ["All"] + sorted(filtered['लेखक'].dropna().unique().tolist())
selected_author = st.selectbox("✍️ लेखक निवडा", authors)

if selected_author != "All":
    filtered = filtered[filtered['लेखक'] == selected_author]

# =========================
# AMAZON STYLE CARDS
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

cols = st.columns(3)

for i, row in filtered.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()
    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    with cols[i % 3]:

        st.markdown("----")

        # 📸 Placeholder Image
        st.image("https://via.placeholder.com/150", use_container_width=True)

        st.markdown(f"### {name}")
        st.write(f"✍️ {row['लेखक']}")

        st.markdown(f"~~₹{row['किंमत']}~~  🔥 **₹{row['सवलतीत']}**")

        st.write("⭐⭐⭐⭐☆")

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
