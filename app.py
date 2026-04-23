import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# HEADER
# =========================
left, right = st.columns([3, 2])

with left:
    col1, col2 = st.columns([1,5])
    with col1:
        st.image("logo.jpg", width=100)
    with col2:
        st.title("📚 राजहंस पुस्तक पेठ, पुणे ०३८")
        st.write("📞 9322630703")

with right:
    st.markdown("### 🧾 तुमची माहिती")

    name_input = st.text_input("नाव", key="name")
    phone_input = st.text_input("फोन", key="phone")
    address_input = st.text_area("पत्ता", key="address")
    pincode_input = st.text_input("पिनकोड", key="pincode")

    # WhatsApp button (top right)
    if st.button("📲 WhatsApp वर ऑर्डर करा", key="top_btn"):
        
        total = 0
        order_text = ""

        for item_name, item in st.session_state.cart.items():
            qty = item["qty"]
            if qty > 0:
                price = item["data"]['सवलतीत']
                subtotal = price * qty
                total += subtotal
                order_text += f"{item_name} x {qty} = ₹{subtotal}%0A"

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

            import urllib.parse
            encoded_message = urllib.parse.quote(message)

            url = f"https://wa.me/919322630703?text={encoded_message}"

            st.markdown(f"[👉 WhatsApp उघडा]({url})")
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
# SEARCH
# =========================
search = st.text_input("🔎 पुस्तक शोधा")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False)
    ]

# =========================
# AUTHOR FILTER (NEW)
# =========================
authors = ["All"] + sorted(filtered['लेखक'].dropna().unique().tolist())
selected_author = st.selectbox("✍️ लेखक निवडा", authors)

if selected_author != "All":
    filtered = filtered[filtered['लेखक'] == selected_author]

# =========================
# HEADER ROW (IMPORTANT)
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

h1, h2, h3, h4, h5 = st.columns([3,2,2,2,2])

h1.markdown("**📖 पुस्तकाचे नाव**")
h2.markdown("**✍️ लेखक**")
h3.markdown("**💰 किंमत**")
h4.markdown("**🔥 सवलतीत**")
h5.markdown("**🛒 Qty**")

st.divider()

# =========================
# BOOK LIST (COMPACT)
# =========================
for i, row in filtered.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()

    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    c1, c2, c3, c4, c5 = st.columns([3,2,2,2,2])

    c1.write(name)
    c2.write(row['लेखक'])
    c3.write(f"₹{row['किंमत']}")
    c4.write(f"🔥 ₹{row['सवलतीत']}")

    with c5:
        b1, b2, b3 = st.columns([1,1,1])

        with b1:
            if st.button("➖", key=f"minus_{i}"):
                if qty > 0:
                    st.session_state.cart[name]["qty"] -= 1
                    st.rerun()

        with b2:
            st.markdown(f"**{st.session_state.cart[name]['qty']}**")

        with b3:
            if st.button("➕", key=f"plus_{i}"):
                st.session_state.cart[name]["qty"] += 1
                st.rerun()

    st.divider()

# =========================
# CUSTOMER INFO
# =========================
with st.expander("🧾 तुमची माहिती भरा"):
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
# WHATSAPP ORDER
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

        st.success("✅ WhatsApp उघडत आहे...")
        st.markdown(f"[👉 इथे क्लिक करा]({whatsapp_url})")
