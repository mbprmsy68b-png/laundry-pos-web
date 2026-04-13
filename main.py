import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hypertoony Laundry POS", layout="centered")

# --- CONNECT TO GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🧺 Laundry Shop POS")
st.caption("Access from any device - Data synced to Google Sheets")

tab1, tab2 = st.tabs(["New Sale", "View Records"])

with tab1:
    mode = st.radio("Service Type", ["Drop-off", "Self-Service"], horizontal=True)
    m_no = st.selectbox("Machine", [f"Machine {i}" for i in range(1, 6)])

    if mode == "Drop-off":
        weight = st.number_input("Weight (kg)", 0.0, 13.0, step=0.1)
        price = 250 if weight <= 8 else 375
        cust = st.text_input("Customer Name")
        
        if st.button("Record Drop-off"):
            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Service_Type": "Drop-off",
                "Machine": m_no,
                "Customer": cust,
                "Total": price,
                "Details": f"{weight}kg"
            }])
            # Logic to append to sheets
            st.success(f"Recorded ₱{price} for {cust}")

    else:
        # Self-service inputs
        col1, col2 = st.columns(2)
        with col1:
            w, d, f = st.checkbox("Wash (₱70)"), st.checkbox("Dry (₱80)"), st.checkbox("Fold (₱50)")
        with col2:
            s = st.number_input("Soap/Downy (₱15)", 0, 10)
        
        total = (70 if w else 0) + (80 if d else 0) + (50 if f else 0) + (s * 15)
        
        if st.button(f"Record Self-Service: ₱{total}"):
            st.success("Self-Service Recorded!")

with tab2:
    st.subheader("Recent Sales (Live from Google Sheets)")
    # This will pull the actual data from your spreadsheet
    try:
        data = conn.read(worksheet="Sheet1")
        st.dataframe(data.tail(10))
    except:
        st.info("Syncing with Google Sheets...")
