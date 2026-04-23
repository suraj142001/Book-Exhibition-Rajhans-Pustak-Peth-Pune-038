           
# =========================
# AMAZON STYLE BOOK CARDS
# =========================
import streamlit as st
import pandas as pd
import urllib.parse

st.subheader("📚उपलब्ध पुस्तके")

cols = st.columns(3)  # 3 cards per row

for i, row in filtered.iterrows():

    name = str(row['पुस्तकाचे नाव']).strip()
    if not name:
        continue

    if name not in st.session_state.cart:
        st.session_state.cart[name] = {"data": row, "qty": 0}

    qty = st.session_state.cart[name]["qty"]

    with cols[i % 3]:

        st.markdown("----")

        # 📸 IMAGE (placeholder)
        st.image("https://via.placeholder.com/150", use_container_width=True)

        # 📖 Book Info
        st.markdown(f"### {name}")
        st.write(f"✍️ {row['लेखक']}")
        st.write(f"~~₹{row['किंमत']}~~  🔥 **₹{row['सवलतीत']}**")

        # ⭐ rating (dummy)
        st.write("⭐⭐⭐⭐☆")

        # ➕ ➖ Qty Control
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
main, side = st.columns([3,1])

with side:
    st.markdown("## 🛒 तुमची ऑर्डर")

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

    name_input = st.text_input("नाव")
    phone_input = st.text_input("फोन")
    address_input = st.text_area("पत्ता")
    pincode_input = st.text_input("पिनकोड")

    if st.button("📲 Order Now"):
        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("⚠️ माहिती भरा")
        elif total == 0:
            st.error("⚠️ पुस्तक निवडा")
        else:
            import urllib.parse
            msg = f"नाव:{name_input}%0Aफोन:{phone_input}%0A{order_text}%0ATotal:{total}"
            url = f"https://wa.me/919322630703?text={msg}"
            st.markdown(f"[👉 WhatsApp Open करा]({url})")
