
# interactive_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
@st.cache_data
def load_data():
    d = pd.read_csv("cause_of_deaths.csv")
    d.rename(columns={'Code': 'Abbreviation'}, inplace=True)
    d = d.drop_duplicates()
    return d

d = load_data()
disease_columns = d.columns[3:]

# --- Sidebar Controls ---
st.sidebar.title("Controls")
view = st.sidebar.radio("Select View", ["Snapshot (Single Year)", "Trend (Multi-Year)"])
country = st.sidebar.selectbox("Select Country", ["Global"] + sorted(d["Country/Territory"].unique().tolist()))

# --- Report Title & Intro ---
st.title("Global Causes of Death (1990–2019)")

st.markdown("""
### Overview
This interactive report explores the leading causes of death worldwide between 1990 and 2019.  
The dataset comes from [Kaggle - Madhur Pant](https://www.kaggle.com/datasets/madhurpant/world-deaths-and-causes-1990-2019)  
and provides annual death counts by disease and region.  

The purpose of this dashboard is to:
- Identify the **most common causes of mortality** globally and by country.  
- Explore how **patterns have shifted over time**, such as the rise and decline of certain diseases.  
- Provide an **interactive way to compare countries and years** using visualizations.  

---
""")

# --- Snapshot View ---
if view == "Snapshot (Single Year)":
    year = st.sidebar.slider("Select Year", min_value=1990, max_value=2019, value=2000)

    if country == "Global":
        filtered = d[d["Year"] == year]
        total_deaths = filtered[disease_columns].sum().reset_index()
    else:
        filtered = d[(d["Year"] == year) & (d["Country/Territory"] == country)]
        total_deaths = filtered[disease_columns].iloc[0].reset_index()

    total_deaths.columns = ["Disease", "Deaths"]

    # Chart
    fig = px.bar(
        total_deaths.sort_values("Deaths", ascending=False),
        x="Disease",
        y="Deaths",
        color="Deaths",
        title=f"Causes of Death in {country} ({year})",
        height=600
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Textual insights
    st.markdown(f"""
    ### Key Insights for {country} in {year}
    - The chart above shows the **distribution of deaths by cause**.  
    - The diseases at the top of the chart represent the **leading drivers of mortality**.  
    - The relative position of diseases highlights **which causes dominate public health** in this year and region.  
    """)

    st.subheader("Top 5 Causes of Death")
    st.table(total_deaths.sort_values("Deaths", ascending=False).head(5))

# --- Trend View ---
else:
    disease = st.sidebar.selectbox("Select Disease", disease_columns)

    if country == "Global":
        trend = d.groupby("Year")[disease].sum().reset_index()
    else:
        trend = d[d["Country/Territory"] == country][["Year", disease]]

    fig = px.line(
        trend,
        x="Year",
        y=disease,
        title=f"Trend of {disease} Deaths in {country} (1990–2019)",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Textual insights
    st.markdown(f"""
    ### Trend Analysis: {disease} in {country}
    - This line chart shows how **{disease} deaths have evolved** over nearly three decades.  
    - Notice the **long-term increases or decreases** that may reflect medical advances, prevention strategies, or demographic changes.  
    - Comparing different countries (by switching the dropdown) can reveal **regional differences in health outcomes**.  
    """)

    st.subheader(f"Data for {disease} in {country}")
    st.dataframe(trend)

# --- Closing Notes ---
st.markdown("""
---
### Conclusion
This dashboard highlights the shifting landscape of global health between 1990 and 2019.  
By examining snapshots and long-term trends, we can see both persistent challenges (such as cardiovascular diseases)  
and areas where progress has been made (such as certain infectious diseases).  

Use the controls in the sidebar to explore further:  
- Change the **view mode** between a single-year snapshot and a multi-year trend.  
- Compare **different countries and diseases** interactively.  

This kind of analysis provides valuable context for **public health planning, medical research, and policy development**.
""")

