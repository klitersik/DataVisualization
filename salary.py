%%writefile salary.py 
import pandas as pd
import plotly.express as px
import streamlit as st

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Salaries in IT Dashboard", page_icon=":money_with_wings::", layout="wide")

@st.cache
# ---- READ EXCEL ----
def get_data_from_excel():
    df = pd.read_csv("/content/salary.csv")
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

experience_level = st.sidebar.multiselect(
    "Select the experience_level:",
    options=df["experience_level"].unique(),
    default=df["experience_level"].unique(),
)

remote_ratio = st.sidebar.multiselect(
    "Select the remote_ratio:",
    options=df["remote_ratio"].unique(),
    default=df["remote_ratio"].unique(),
)

company_size = st.sidebar.multiselect(
    "Select the company_size:",
    options=df["company_size"].unique(),
    default=df["company_size"].unique(),
)

df_selection = df.query(
    "experience_level == @experience_level & remote_ratio == @remote_ratio & company_size == @company_size"
)


st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


total_positions = int(len(df_selection["salary_in_usd"]))

average_salary = round(df_selection["salary_in_usd"].mean(), 1)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Total positions:")
    st.subheader({total_positions})

with right_column:
    st.subheader("Average Salary:")
    st.subheader(f"US $ {average_salary}")

st.markdown("""---""")

counter = st.number_input("Number of top average salaries",min_value = 3)

st.title(f"top {counter} Average salary")

top_10_jobs_by_average_salary = (
    df_selection.groupby(["job_title"])["salary_in_usd"].mean().sort_values(ascending=False).head(counter).reset_index()
)

top_10_jobs_by_average_salary_chart = st.bar_chart(top_10_jobs_by_average_salary, x = "job_title", y = "salary_in_usd", use_container_width = True)

st.markdown("""---""")

left_column_chart, right_column_chart = st.columns(2)

top_jobs_by_company_size = df_selection.groupby(["company_size"])["salary_in_usd"].mean().sort_values(ascending=False).head(counter).reset_index()

top_jobs_by_remote_ratio = df_selection.groupby(["remote_ratio"])["salary_in_usd"].mean().sort_values(ascending=False).head(counter).reset_index()

with left_column_chart:
    st.subheader("Average salary by company size:")
    top_jobs_by_company_size_chart = st.bar_chart(top_jobs_by_company_size, x = "company_size", y = "salary_in_usd", use_container_width = True)

with right_column_chart:
    st.subheader("Average salary by remote ratio:")
    top_jobs_by_remote_ratio_chart = st.bar_chart(top_jobs_by_remote_ratio, x = "remote_ratio", y = "salary_in_usd", use_container_width = True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
