import pandas as pd
import streamlit as st

# Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load data into dataframe
    df = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file)

    # Filter out rows with filled "status" column
    df = df[df["status"].isnull()]

    # Display current and total row counts
    global current_row
    current_row = 0
    total_row = len(df)
    st.text(f"Row {current_row + 1} of {total_row}")

    # Display current address_1 and address_2
    address_1 = df.iloc[current_row]["address_1"]
    address_2 = df.iloc[current_row]["address_2"]
    st.write(f"Address 1: {address_1}")
    st.write(f"Address 2: {address_2}")

    # Add status column with default value of None
    df["status"] = None

    # Define button functions
    def next_matched():
        global current_row
        df.iloc[current_row, df.columns.get_loc("status")] = "matched"
        current_row += 1
        st.text(f"Row {current_row + 1} of {total_row}")

    def next_not_match():
        global current_row
        df.iloc[current_row, df.columns.get_loc("status")] = "non_match"
        current_row += 1
        st.text(f"Row {current_row + 1} of {total_row}")

    def next_not_address():
        global current_row
        df.iloc[current_row, df.columns.get_loc("status")] = "non_address"
        current_row += 1
        st.text(f"Row {current_row + 1} of {total_row}")

    def back():
        global current_row
        current_row = max(current_row - 1, 0)
        st.text(f"Row {current_row + 1} of {total_row}")

    # Add buttons
    col1, col2, col3, col4 = st.beta_columns(4)
    col1.button("Next (Matched)", on_click=next_matched)
    col2.button("Next (Not match)", on_click=next_not_match)
    col3.button("Next (Not address)", on_click=next_not_address)
    col4.button("Back", on_click=back)

    # Display number of filled and unfilled rows
    filled_count = len(df[df["status"].notnull()])
    unfilled_count = total_row - filled_count
    st.text(f"{filled_count} rows filled, {unfilled_count} rows left")

    # Display download button
    if filled_count > 0:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="annotated_data.csv">Download annotated data</a>'
        st.markdown(href, unsafe_allow_html=True)
