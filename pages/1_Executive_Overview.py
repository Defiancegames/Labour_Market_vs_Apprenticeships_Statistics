from data_loader import load_data
import streamlit as st
import plotly.express as px

df = load_data()

st.title("Executive Overview")

summary = df[
    (df["age"] == "Total")
    & (df["level"] == "Total")
    & (df["sex"] == "Total")
]

# Level and Age over time
col1, col2 = st.columns(2)

level_data = df[
    (df["age"] == "Total")
    & (df["level"] != "Total")
    & (df["sex"] == "Total")
]

level_data = (
    level_data
    .groupby(["academic_year", "level"],
             as_index=False)
    .agg({
        "starts": "sum",
        "mean_jobs": "sum"
    })
)

fig = px.line(
    level_data,
    x="academic_year",
    y="starts",
    labels={"academic_year": "Academic Year",
            "starts": "Starts"},
    color="level",
    markers=True,
    title="Apprenticeship Starts by Level over Time"
)
col1.plotly_chart(fig, width='stretch')

age_data = df[
    (df["age"] != "Total")
    & (df["level"] == "Total")
    & (df["sex"] == "Total")
]

age_data = (
    age_data
    .groupby(["academic_year", "age"],
             as_index=False)
    .agg({
        "starts": "sum",
        "mean_jobs": "sum"
    })
)

fig = px.line(
    age_data,
    x="academic_year",
    y="starts",
    color="age",
    labels={"academic_year": "Academic Year",
            "starts": "Starts"},
    markers=True,
    title="Apprenticeship Starts by Age over Time"
)

col2.plotly_chart(fig, width='stretch')

# Academic year selection
year = st.selectbox(
    "Academic Year",
    sorted(df["academic_year"].unique(), reverse=True)
)

# industry summary for the selected year
industry_summary = (
    summary
    .groupby(["academic_year", "industry"],
             as_index=False)
    .agg({
        "starts": "sum",
        "mean_jobs": "sum"
    })
)
industry_summary["starts_per_1000_jobs"] = (
    industry_summary["starts"]
    /
    industry_summary["mean_jobs"]
) * 1000

industry_summary["change"] = (
    industry_summary
    .groupby("industry")["starts_per_1000_jobs"]
    .diff()
)

industry_summary = industry_summary[
    industry_summary["academic_year"] == year
]

# regional summary for all years
region_summary = (
    summary
    .groupby(
        ["academic_year","region"],
        as_index=False)
    .agg({
        "starts":"sum",
        "mean_jobs":"sum"
    })
)
region_summary["starts_per_1000"] = (
    region_summary["starts"]
    /
    region_summary["mean_jobs"]
) * 1000

region_summary["change"] = (
    region_summary
    .groupby("region")["starts_per_1000"]
    .diff()
)

# Regional change
# Regional Summary By Selected Year (region_summary)
region_summary = region_summary[
    region_summary["academic_year"]
    == year
]

col1, col2 = st.columns(2)
col1.metric(
    "Highest region starts per 1k jobs",
    f'''{region_summary.loc[region_summary["starts_per_1000"].idxmax()]["region"]}  
    :gray[{round(region_summary.loc[region_summary["starts_per_1000"].idxmax()]["starts_per_1000"], 2)}]    
    ''',
    f"{region_summary.loc[region_summary["starts_per_1000"].idxmax()]["change"]:.2f}",
    delta_description=f"vs {year-1}",
    border=True
)
col2.metric(
    "Highest industry starts per 1k jobs",
    f''':small[{industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmax()]["industry"]}]  
    :gray[{round(industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmax()]["starts_per_1000_jobs"], 2)}]    
    ''',
    f"{industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmax()]["change"]:.2f}",
    delta_description=f"vs {year-1}",
    border=True
)
col1, col2 = st.columns(2)
col1.metric(
    "Lowest region starts per 1k jobs",
    f'''{region_summary.loc[region_summary["starts_per_1000"].idxmin()]["region"]}  
    :gray[{round(region_summary.loc[region_summary["starts_per_1000"].idxmin()]["starts_per_1000"], 2)}]    
    ''',
    f"{region_summary.loc[region_summary["starts_per_1000"].idxmin()]["change"]:.2f}",
    delta_description=f"vs {year-1}",
    border=True
)
col2.metric(
    "Lowest industry starts per 1k jobs",
    f''':small[{industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmin()]["industry"]}]  
    :gray[{round(industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmin()]["starts_per_1000_jobs"], 2)}]    
    ''',
    f"{industry_summary.loc[industry_summary["starts_per_1000_jobs"].idxmin()]["change"]:.2f}",
    delta_description=f"vs {year-1}",
    border=True
)

# leaderboards
col1, col2 = st.columns(2)

# Regional leaderboard
regional = (
    summary[summary["academic_year"] == year]
    .groupby("region", as_index=False)
    .agg({
        "starts":"sum"
    })
    .sort_values("starts", ascending=True)
)

fig = px.bar(
    regional,
    x="starts",
    y="region",
    labels={"starts":"Starts", "region":"Region"},
    orientation="h",
    title=f"Apprenticeship Starts by Region ({year})"
)

col1.plotly_chart(fig, width='stretch')

# Region per 1000 workforce leaderboard
regional_intensity = (
    summary[summary["academic_year"] == year]
    .groupby("region", as_index=False)
    .agg({
        "starts":"sum",
        "mean_jobs":"sum"
    })
)

regional_intensity["starts_per_1000"] = (
    regional_intensity["starts"]
    /
    regional_intensity["mean_jobs"]
) * 1000

fig = px.bar(
    regional_intensity.sort_values(
        "starts_per_1000",
        ascending=True
    ),
    x="starts_per_1000",
    y="region",
    labels={"starts_per_1000":"Starts per 1k Jobs", "region":"Region"},
    orientation="h",
    title=f"Apprenticeships per 1k Jobs by Region ({year})"
)

col2.plotly_chart(fig, width='stretch')

# Removed the following as the scatter did a beter job visualising the data
# # Top 10 industries by starts
# fig = px.bar(
#     industry_summary.nlargest(10, "starts").sort_values(by="starts", ascending=True),
#     x="starts",
#     y="industry",
#     orientation="h",
#     title="Top 10 Industries by Apprenticeship Starts"
# )

# st.plotly_chart(
#     fig,
#     width='stretch'
# )

# fig = px.bar(
#     industry_summary.nlargest(10, "starts_per_1000_jobs").sort_values(
#         "starts_per_1000_jobs",
#         ascending=True
#     ).head(10),
#     x="starts_per_1000_jobs",
#     y="industry",
#     orientation="h",
#     title="Top 10 Industries by Starts per 1,000 Jobs"
# )

# st.plotly_chart(
#     fig,
#     width='stretch'
# )

st.plotly_chart(
    px.scatter(
        industry_summary,
        x="mean_jobs",
        y="starts_per_1000_jobs",
        size="starts",
        color="industry",
        hover_name="industry",
        labels={
            "mean_jobs":"Jobs",
            "starts_per_1000_jobs": "Apprenticeship starts per 1k Jobs",
            "industry":"Industry"
            }
    )
)

st.header("Regional changes in starts per 1k jobs")
st.dataframe(
    region_summary.rename(columns={"region":"Region",
                                   "starts_per_1000":"Starts per 1k Jobs",
                                   "change":"Change",
                                   "academic_year":"Academic Year",
                                   "mean_jobs":"Mean Jobs",
                                   "starts":"Starts"
                                   }).sort_values(by="Change", ascending=False).style.format({
        "starts_per_1000":"{:.2f}",
        "change":"{:+.2f}"
    }),
    hide_index = True
)
