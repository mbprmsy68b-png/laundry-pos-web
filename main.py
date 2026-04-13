import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Hypertoony Laundry POS", layout="centered")

# This creates a file on the server to hold your data
DB_FILE = "local_sales.csv"

def save_to_local(new_entry):
    df = pd.DataFrame([new_entry])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

st.title("🧺 Laundry Shop POS")
st.caption("Straightforward Manual Recording")

tab1, tab2 = st.tabs(["New Sale", "View History"])

with tab1:
    mode = st.radio("Service Type", ["Drop-off", "Self-Service"], horizontal=True)
    
    if mode == "Drop-off":
        weight = st.number_input("Weight (kg)", 0.0, 13.0, step=0.1)
        price = 250 if weight <= 8 else 375
        cust = st.text_input("Customer Name")
        if st.button("Confirm Drop-off"):
            data = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Type": "Drop-off", "Customer": cust, "Total": price}
            save_to_local(data)
            st.success(f"Saved! Total: ₱{price}")

    else:
        w = st.checkbox("Wash (₱70)")
        d = st.checkbox("Dry (₱80)")
        s = st.number_input("Soaps (₱15)", 0, 10)
        total = (70 if w else 0) + (80 if d else 0) + (s * 15)
        
        if st.button(f"Record Self-Service: ₱{total}"):
            data = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Type": "Self-Service", "Customer": "Walk-in", "Total": total}
            save_to_local(data)
            st.success("Sale Recorded!")

with tab2:
    st.subheader("Sales History")
    if os.path.isfile(DB_FILE):
        history = pd.read_csv(DB_FILE)
        st.dataframe(history, use_container_width=True)
        st.metric("Total Cash", f"₱{history['Total'].sum()}")
        
        # Download button so you can still get the data out
        csv = history.to_csv(index=False).encode('utf-8')
        st.download_button("Download Sales Report", data=csv, file_name="laundry_report.csv", mime="text/csv")
    else:
        st.info("No sales recorded yet.")
