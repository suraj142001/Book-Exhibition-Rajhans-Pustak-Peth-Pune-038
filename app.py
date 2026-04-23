import streamlit as st
import pandas as pd
import urllib.parse
import os

# =========================
# PAGE CONFIG MUST BE FIRST
# =========================
st.set_page_config(page_title="राजहंस पुस्तक पेठ", layout="wide")

# =========================
# HIDE STREAMLIT HEADER
# =========================
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# =========================
# LOAD DATA WITH ERROR HANDLING
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", encoding="utf-8-sig")
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Check required columns
        required_cols = ['पुस्तकाचे नाव', 'लेखक', 'किंमत', 'सवलतीत']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns in CSV: {missing_cols}")
            st.stop()
            
        # Convert price columns to numeric
        df['किंमत'] = pd.to_numeric(df['किंमत'], errors='coerce').fillna(0)
        df['सवलतीत'] = pd.to_numeric(df['सवलतीत'], errors='coerce').fillna(0)
        
        return df
    except FileNotFoundError:
        st.error("data.csv file not found! Please make sure the file exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

df = load_data()

# =========================
# CART INITIALIZATION
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}
    
if "page" not in st.session_state:
    st.session_state.page = 1

# =========================
# SIDEBAR (ORDER FORMAT UPDATED)
# =========================
with st.sidebar:
    st.markdown("## राजहंस पुस्तक पेठ ")
    st.markdown("### 📚 आपण निवडलेली पुस्तके")

    total = 0
    order_text = ""
    sr = 1
    empty = True

    # Create a list of items to remove (can't modify dict while iterating)
    items_to_remove = []
    
    for item_name, item in st.session_state.cart.items():
        qty = item["qty"]

        if qty > 0:
            empty = False
            price = item["data"]['सवलतीत']
            subtotal = price * qty

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"{sr}. **{item_name}**")
                st.caption(f"{qty} x ₹{price:.2f} = ₹{subtotal:.2f}")
            with col2:
                if st.button("❌", key=f"remove_{item_name}"):
                    items_to_remove.append(item_name)

            total += subtotal
            order_text += f"{sr}. {item_name} x {qty} = ₹{subtotal:.2f}\n"
            sr += 1
    
    # Remove items marked for deletion
    for item_name in items_to_remove:
        del st.session_state.cart[item_name]
        st.rerun()

    if empty:
        st.info("अजून पुस्तक निवडलेले नाही")

    st.divider()
    st.success(f"एकूण: ₹{total:.2f}")

    st.markdown("### 🧾 ऑर्डर माहिती")
    st.markdown("---")
    
    name_input = st.text_input("👤 नाव", key="name_input")
    phone_input = st.text_input("📞 फोन नंबर", key="phone_input")
    address_input = st.text_area("🏠 पत्ता", key="address_input")
    pincode_input = st.text_input("📮 पिनकोड", key="pincode_input")

    if st.button("📲 WhatsApp वर ऑर्डर करा", use_container_width=True):
        if not name_input or not phone_input or not address_input or not pincode_input:
            st.error("कृपया सर्व माहिती भरा")
        elif total == 0:
            st.error("किमान एक पुस्तक निवडा")
        else:
            message = f"""*नमस्कार* 🙏

*नवीन ऑर्डर*

*ग्राहक माहिती:*
नाव: {name_input}
फोन: {phone_input}
पत्ता: {address_input}
पिनकोड: {pincode_input}

*पुस्तके:*\n{order_text}
*एकूण: ₹{total:.2f}*

धन्यवाद! 😊"""

            encoded_msg = urllib.parse.quote(message)
            url = f"https://wa.me/919322630703?text={encoded_msg}"
            
            # Create a clean button for WhatsApp
            st.markdown(f"""
            <a href="{url}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 10px 20px; 
                border: none; border-radius: 5px; cursor: pointer; font-size: 16px; 
                width: 100%;">
                    📱 WhatsApp वर पाठवा
                </button>
            </a>
            """, unsafe_allow_html=True)
            
            st.success("✅ ऑर्डर तयार आहे! वरील बटणावर क्लिक करा.")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=150)
    else:
        st.markdown("### 📚")

with col2:
    st.markdown("# 📚 राजहंस पुस्तक पेठ")
    st.caption("📞 9322630703 | 🚚 फ्री डिलिव्हरी (महाराष्ट्रात)")

st.markdown("---")

# =========================
# SEARCH AND FILTERS
# =========================
col_search, col_filter = st.columns([3, 1])

with col_search:
    search = st.text_input("🔎 पुस्तक शोधा", placeholder="पुस्तकाचे नाव टाईप करा...")

with col_filter:
    if st.button("🗑️ सर्व फिल्टर क्लियर", use_container_width=True):
        search = ""
        st.rerun()

filtered = df.copy()

if search:
    filtered = filtered[
        filtered['पुस्तकाचे नाव'].astype(str).str.contains(search, case=False, na=False) |
        filtered['लेखक'].astype(str).str.contains(search, case=False, na=False)
    ]

# Show results count
st.caption(f"📊 {len(filtered)} पुस्तके सापडली")

# =========================
# PAGINATION
# =========================
items_per_page = 8

total_pages = max(1, (len(filtered) - 1) // items_per_page + 1)

# Reset page if current page exceeds total pages
if st.session_state.page > total_pages:
    st.session_state.page = 1

start = (st.session_state.page - 1) * items_per_page
end = start + items_per_page

page_data = filtered.iloc[start:end]

# =========================
# BOOK LIST
# =========================
st.markdown("### 📚 पुस्तके")
st.markdown("---")

if len(page_data) == 0:
    st.warning("⚠️ कोणतेही पुस्तक सापडले नाही")
else:
    for i, row in page_data.iterrows():
        name = str(row['पुस्तकाचे नाव']).strip()
        if not name:
            continue

        if name not in st.session_state.cart:
            st.session_state.cart[name] = {"data": row.to_dict(), "qty": 0}

        qty = st.session_state.cart[name]["qty"]
        
        # Create a unique key for this book
        unique_key = f"book_{i}_{name.replace(' ', '_')}"

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

        with col1:
            st.markdown(f"**📖 {name}**")
            st.caption(f"✍️ {row['लेखक']}")
            st.caption(f"💰 मूळ किंमत: ₹{row['किंमत']:.2f}  →  🏷️ सवलतीत: ₹{row['सवलतीत']:.2f}")

        with col2:
            st.metric("स्टॉक", "उपलब्ध" if row.get('स्टॉक', 1) > 0 else "नाही")

        with col3:
            st.write(f"**संख्यात:** {qty}")

        with col4:
            c1, c2 = st.columns(2)
            
            with c1:
                if st.button("➖", key=f"m_{unique_key}"):
                    if qty > 0:
                        st.session_state.cart[name]["qty"] -= 1
                        st.rerun()
            
            with c2:
                if st.button("➕", key=f"p_{unique_key}"):
                    st.session_state.cart[name]["qty"] += 1
                    st.rerun()

        st.markdown("---")

# =========================
# PAGINATION BUTTONS
# =========================
if total_pages > 1:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮️ पहिले", use_container_width=True):
            st.session_state.page = 1
            st.rerun()
    
    with col2:
        if st.button("⬅️ मागे", use_container_width=True):
            if st.session_state.page > 1:
                st.session_state.page -= 1
                st.rerun()
    
    with col3:
        st.markdown(f"<h3 style='text-align: center;'>पान {st.session_state.page} / {total_pages}</h3>", 
                   unsafe_allow_html=True)
    
    with col4:
        if st.button("पुढे ➡️", use_container_width=True):
            if st.session_state.page < total_pages:
                st.session_state.page += 1
                st.rerun()
    
    with col5:
        if st.button("शेवटचे ⏭️", use_container_width=True):
            st.session_state.page = total_pages
            st.rerun()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© राजहंस पुस्तक पेठ | सर्व हक्क राखीव</p>", 
    unsafe_allow_html=True
)
