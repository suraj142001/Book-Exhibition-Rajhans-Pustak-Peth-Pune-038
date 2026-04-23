           
# =========================
# AMAZON STYLE BOOK CARDS
# =========================
st.subheader("📚 उपलब्ध पुस्तके")

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
