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
