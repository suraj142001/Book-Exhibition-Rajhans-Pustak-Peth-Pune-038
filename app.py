import streamlit as st
import pandas as pd
import urllib.parse
import os
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df['किंमत'] = pd.to_numeric(df['किंमत'], errors='coerce')
    df['सवलतीत'] = pd.to_numeric(df['सवलतीत'], errors='coerce')
    df['स्टॉक'] = pd.to_numeric(df.get('स्टॉक', 0), errors='coerce')

    df = df.fillna(0)
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
# SAVE ORDER
# =========================
def save_order(data):
    file = "orders.csv"
    df_new = pd.DataFrame([data])

    if os.path.exists(file):
        df_old = pd.read_csv(file)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(file, index=False)

# =========================
# INVOICE
# =========================
def generate_invoice(name, order_text, total):
    file = f"invoice_{name}.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("राजहंस पुस्तक पेठ", styles['Title']))
    content.append(Paragraph(f"Customer: {name}", styles['Normal']))
    content.append(Paragraph(order_text, styles['Normal']))
    content.append(Paragraph(f"Total: ₹{int(total)}", styles['Normal']))

    doc.build(content)
    return file

# =========================
# SIDEBAR (CART)
# =========================
with st.sidebar:
    st.title("🛒 Cart")

    total = 0
    order_text = ""
    sr = 1

    for name, item in st.session_state.cart.items():
        qty = item["qty"]

        if qty > 0:
            price = float(item["data"]['सवलतीत'])
            subtotal = price * qty

            st.write(f"{sr}. {name}")
            st.caption(f"{qty} x ₹{int(price)} = ₹{int(subtotal)}")

            total += subtotal
            order_text += f"{sr}. {name} x {qty} = ₹{int(subtotal)}\n"
            sr += 1

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

        if total == 0:
            st.error("Cart empty")
        elif not name_input:
            st.error("नाव टाका")
        else:
            data = {
                "Date": datetime.datetime.now(),
                "Name": name_input,
                "Phone": phone_input,
                "Address": address_input,
                "Pincode": pincode_input,
                "Order": order_text,
                "Total": total
            }

            save_order(data)

            message = f"""
नमस्कार 🙏

नाव: {name_input}
फोन: {phone_input}

{order_text}

Total: ₹{int(total)}
"""

            url = f"https://wa.me/919322630703?text={urllib.parse.quote(message)}"
            st.markdown(f"[👉 WhatsApp उघडा]({url})")

    # =========================
    # INVOICE BUTTON
    # =========================
    if st.button("📄 Download Invoice"):
        if total > 0 and name_input:
            file = generate_invoice(name_input, order_text, total)
            with open(file, "rb") as f:
                st.download_button("Download", f, file_name=file)

# =========================
# HEADER
# =========================
st.title("📚 राजहंस पुस्तक पेठ")

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
items_per_page = 8
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
    stock = int(row.get("स्टॉक", 0))

    col1, col2, col3 = st.columns([5,2,2])

    with col1:
        st.write(f"**{name}**")
        st.caption(f"{row['लेखक']} | ₹{int(row['किंमत'])} → ₹{int(row['सवलतीत'])}")

    with col2:
        st.write(f"Qty: {qty} | Stock: {stock}")

    with col3:
        c1, c2 = st.columns(2)

        with c1:
            if st.button("➖", key=f"m{i}"):
                if qty > 0:
                    st.session_state.cart[name]["qty"] -= 1
                    st.rerun()

        with c2:
            if st.button("➕", key=f"p{i}"):
                if stock > qty:
                    st.session_state.cart[name]["qty"] += 1
                    st.rerun()
                else:
                    st.error("Stock limit reached")

    st.divider()

# =========================
# PAGINATION BUTTONS
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()

with col2:
    st.write(f"Page {st.session_state.page}/{total_pages}")

with col3:
    if st.button("➡️"):
        if st.session_state.page < total_pages:
            st.session_state.page += 1
            st.rerun()

# =========================
# ADMIN PANEL
# =========================
st.sidebar.markdown("---")

if st.sidebar.checkbox("🔐 Admin Panel"):

    st.title("📊 Admin Dashboard")

    if os.path.exists("orders.csv"):
        orders = pd.read_csv("orders.csv")

        st.subheader("Total Orders")
        st.write(len(orders))

        st.subheader("Total Sales")
        st.write(f"₹ {int(orders['Total'].sum())}")

        st.dataframe(orders)
