from turtle import pd

from data_loader import load_data
import streamlit as st
import plotly.express as px
import pandas as pd

df = load_data()

st.title("Industry Inspection")

summary_df = df[
    (df["age"] == "Total")
    & (df["level"] == "Total")
    & (df["sex"] == "Total")
]

col1,col2 = st.columns(2)

col1.plotly_chart(
    px.line(
        summary_df.groupby(
            ["academic_year",
             "industry"], as_index=False
        ).agg(starts=("starts", "sum")),
        x="academic_year",
        y="starts",
        color="industry",
        markers=True,
        labels={"starts":"Starts", "academic_year":"Academic Year", "industry":"Industry"},
        title="Industry Starts over Time"
    )
)

starts_by_workforce = (
    summary_df
    .groupby(["academic_year", "industry"], as_index=False)
    .agg({
        "starts": "sum",
        "mean_jobs": "sum"
    })
)
starts_by_workforce["starts_per_1000_jobs"] = (
    starts_by_workforce["starts"]
    /
    starts_by_workforce["mean_jobs"]
) * 1000

col2.plotly_chart(
    px.line(
        starts_by_workforce.groupby(
            ["academic_year",
             "industry"], as_index=False
        ).agg(starts_per_1000_jobs=("starts_per_1000_jobs", "sum")),
        x="academic_year",
        y="starts_per_1000_jobs",
        color="industry",
        markers=True,
        labels={"starts_per_1000_jobs":"Starts per 1k Jobs", "academic_year":"Academic Year", "industry":"Industry"},
        title="Industry Starts per 1k jobs over Time"
    )
)

# Selectors
col1,col2,col3,col4,col5 = st.columns(5)
industry = col1.selectbox(
    "Industry",
    sorted(df["industry"].unique())
)

year = col2.selectbox(
    "Academic Year",
    sorted(df["academic_year"].unique(), reverse=True)
)

sex = col3.selectbox(
    "sex",
    sorted(df["sex"].unique(), reverse=True)
)

level = col4.selectbox(
    "level",
    sorted(df["level"].unique(), reverse=True)
)

age = col5.selectbox(
    "age",
    sorted(df["age"].unique()),
    2 # index of the defualt option
)

summary = df[
    (df["age"] == age)
    & (df["level"] == level)
    & (df["sex"] == sex)
    & (df["academic_year"] == year)
    & (df["industry"] == industry)
]

total_workforce = summary["mean_jobs"].sum()

total_starts = summary["starts"].sum()

avg_intensity = (
    summary["starts_per_1000_jobs"]
    .mean()
)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Workforce*",
    f'''{total_workforce:,.0f}  
    :small[_*no break down on level and age available_]'''
)

col2.metric(
    "Apprenticeship Starts",
    f"{total_starts:,.0f}"
)

col3.metric(
    "Starts per 1,000 Jobs",
    f"{avg_intensity:.1f}"
)

treemap_df = (
    df[
        (df["age"] != "Total" if age == "Total" else df["age"] == age)
        & (df["level"] != "Total" if level == "Total" else df["level"] == level)
        & (df["sex"] != "Total" if sex == "Total" else df["sex"] == sex)
        & (df["academic_year"] == year)
        & (df["industry"] == industry)
    ])

fig = px.treemap(treemap_df,
                 path=[px.Constant(industry), 'age', 'sex', 'level'],
                 values='starts')
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.update_traces(marker=dict(cornerradius=5),
                  textinfo="label+text+value",
                  root_color="black")
st.plotly_chart(fig, width="stretch")

st.plotly_chart(
    px.scatter(
        #plot_df,
        summary,
        x="mean_jobs",
        y="starts_per_1000_jobs",
        size="starts",
        hover_name="region",
        color="region",
        labels={"mean_jobs":"Workforce Size", "starts_per_1000_jobs":"Starts per 1k Jobs", "starts":"Apprenticeship Starts"},
        title="Apprenticeship Starts vs Workforce Size"
    ),
    width="stretch"
)

industry_performance = df[
    (df["age"] == "Total")
    & (df["level"] == "Total")
    & (df["sex"] == "Total")
    & (df["academic_year"] == year)
]

best_perf = industry_performance.loc[industry_performance.groupby("industry")["starts_per_1000_jobs"].idxmax()][["industry", "region", "starts_per_1000_jobs"]].copy()
worst_perf = industry_performance.loc[industry_performance.groupby("industry")["starts_per_1000_jobs"].idxmin()][["industry", "region", "starts_per_1000_jobs"]].copy()

ibw = pd.DataFrame(industry_performance["industry"].unique(), columns=["industry"])
ibw = ibw.merge(best_perf, on="industry")
ibw = ibw.merge(worst_perf, on="industry", suffixes=("_best", "_worst"))
ibw.rename(columns={"region_best":"Best Performing Region", "starts_per_1000_jobs_best":"Best Performance (Starts per 1k Jobs)", "region_worst":"Worst Performing Region", "starts_per_1000_jobs_worst":"Worst Performance (Starts per 1k Jobs)"}, inplace=True)

st.header(f"Industry Total Performance by Region for {year}")
st.dataframe(ibw,
             hide_index = True
)
