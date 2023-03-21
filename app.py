import streamlit as st
import pandas as pd

def process_file(file):
    if file is None:
        return None, None

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)

    if "status" not in df.columns:
        df["status"] = ""

    return df, df[df["status"] == ""]

def main():
    st.title("Address Annotation App")

    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    df, df_unfilled = process_file(uploaded_file)

    if df is not None:
        index = st.session_state.get("index", 0)
        filled_count = len(df) - len(df_unfilled)

        if index < len(df_unfilled):
            row = df_unfilled.iloc[index]
            st.write(f"Row {index + 1} of {len(df_unfilled)}")
            st.write(pd.DataFrame(row[["HOUSE_FULL_1", "HOUSE_FULL_2"]]).T)

            if st.button("Next (Matched)"):
                df.at[row.name, "status"] = "matched"
                index += 1
            if st.button("Next (Not match)"):
                df.at[row.name, "status"] = "non_match"
                index += 1
            if st.button("Next (Not address)"):
                df.at[row.name, "status"] = "non_address"
                index += 1
            if st.button("Back") and index > 0:
                index -= 1

            unfilled_count = len(df) - filled_count - (index + 1)
            st.write(f"{filled_count} rows filled, {unfilled_count} rows remaining")

        else:
            st.write("All rows annotated!")
            st.write(f"{filled_count} rows filled")

        st.write(df)
        st.download_button(
            label="Download annotated file",
            data=df.to_csv(index=False),
            file_name="annotated_file.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
