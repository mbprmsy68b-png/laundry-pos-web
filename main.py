import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Hypertoony Laundry POS", layout="centered")

DB_FILE = "local_sales.csv"

def save_to_local(new_entry):
    df = pd.DataFrame([new_entry])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

st.title("🧺 Hypertoony Laundry POS")
st.caption("v2.0 - 6 Machine Tracking")

tab1, tab2 = st.tabs(["New Sale", "View History"])

with tab1:
    # Machine Selection
    machine = st.selectbox("Select Machine", [f"Washing Machine {i}" for i in range(1, 7)])
    mode = st.radio("Service Type", ["Self-Service", "Drop-off"], horizontal=True)
    
    if mode == "Self-Service":
        col1, col2 = st.columns(2)
        with col1:
            w = st.checkbox("Wash (₱80)")
            d = st.checkbox("Dry (₱80)")
            f = st.checkbox("Fold (₱50)")
        with col2:
            det = st.number_input("Detergent (₱15)", 0, 10, step=1)
            dow = st.number_input("Downy (₱15)", 0, 10, step=1)
        
        total = (80 if w else 0) + (80 if d else 0) + (50 if f else 0) + (det * 15) + (dow * 15)
        
        if st.button(f"Confirm Sale: ₱{total}"):
            details = f"Det:{det}, Dow:{dow}"
            data = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Machine": machine, "Type": "Self-Service", "Customer": "Walk-in", "Total": total, "Details": details}
            save_to_local(data)
            st.success(f"Recorded ₱{total} for {machine}")

    else:
        weight = st.number_input("Weight (kg)", 0.0, 20.0, step=0.1)
        # Assuming Drop-off still follows your P250/P375 rule or custom
        price = 250 if weight <= 8 else 375
        cust = st.text_input("Customer Name")
        if st.button("Confirm Drop-off Sale"):
            data = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Machine": machine, "Type": "Drop-off", "Customer": cust, "Total": price, "Details": f"{weight}kg"}
            save_to_local(data)
            st.success(f"Recorded ₱{price} for {cust}")

with tab2:
    st.subheader("Recent Records")
    if os.path.isfile(DB_FILE):
        history = pd.read_csv(DB_FILE)
        st.dataframe(history.tail(20), use_container_width=True)
        
        st.divider()
        st.metric("Total Revenue", f"₱{history['Total'].sum()}")
        
        # Monthly/Daily backup button
        csv = history.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Backup (CSV)", data=csv, file_name=f"laundry_report_{datetime.now().strftime('%Y-%m-%d')}.csv", mime="text/csv")
    else:
        st.info("No sales recorded yet today.")
