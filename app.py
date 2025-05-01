import streamlit as st
import pandas as pd
from test import main  # Your logic from before

st.title("Git Push Tracker 💻📈")

if st.button("Run Git Tracker and Send Mails"):
    main()  # Run the function
    st.success("Emails sent and Excel updated!")

st.markdown("Upload your `git.xlsx` file and view results below.")
uploaded_file = st.file_uploader("Upload git.xlsx", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Git Users Data")
    st.dataframe(df)
