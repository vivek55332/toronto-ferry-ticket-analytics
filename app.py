
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Toronto Ferry Analytics",
    page_icon="⛴️",
    layout="wide"
)

# -------------------------------
# LOAD DATASET
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Toronto_Ferry_Cleaned.csv")

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    df["Sales Count"] = pd.to_numeric(
        df["Sales Count"], errors="coerce"
    )

    df["Redemption Count"] = pd.to_numeric(
        df["Redemption Count"], errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Timestamp",
            "Sales Count",
            "Redemption Count"
        ]
    )

    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Month_Name"] = df["Timestamp"].dt.month_name()
    df["Hour"] = df["Timestamp"].dt.hour
    df["Date"] = df["Timestamp"].dt.date
    df["Day_Type"] = df["Timestamp"].dt.dayofweek.map(
        lambda x: "Weekend" if x >= 5 else "Weekday"
    )

    return df


df = load_data()

# -------------------------------
# DASHBOARD TITLE
# -------------------------------
st.title("⛴️ Toronto Island Ferry Analytics")
st.markdown(
    "### Ticket Sales & Redemption Analysis Dashboard"
)

st.markdown(
    "Explore ferry ticket activity, sales trends, "
    "redemption patterns and peak periods."
)

st.divider()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Dashboard Filters")

years = sorted(df["Year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

if not selected_years:
    st.warning("Please select at least one year.")
    st.stop()

filtered_df = df[df["Year"].isin(selected_years)]

# -------------------------------
# KEY PERFORMANCE INDICATORS
# -------------------------------
total_sales = filtered_df["Sales Count"].sum()
total_redemptions = filtered_df["Redemption Count"].sum()

redemption_rate = (
    total_redemptions / total_sales * 100
    if total_sales > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets Sold", f"{total_sales:,.0f}")
col2.metric("Total Redeemed", f"{total_redemptions:,.0f}")
col3.metric("Redemption Rate", f"{redemption_rate:.2f}%")
col4.metric("Total Records", f"{len(filtered_df):,}")

st.divider()

# -------------------------------
# MONTHLY SALES ANALYSIS
# -------------------------------
st.subheader("📊 Monthly Ticket Sales and Redemptions")

monthly = filtered_df.groupby(
    ["Year", "Month", "Month_Name"],
    as_index=False
)[["Sales Count", "Redemption Count"]].sum()

monthly["Period"] = (
    monthly["Year"].astype(str) + " - " +
    monthly["Month_Name"]
)

fig_monthly = px.bar(
    monthly,
    x="Period",
    y=["Sales Count", "Redemption Count"],
    barmode="group",
    title="Monthly Sales vs Redemptions"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -------------------------------
# YEARLY SALES ANALYSIS
# -------------------------------
st.subheader("📅 Year-wise Ticket Analysis")

yearly = filtered_df.groupby(
    "Year",
    as_index=False
)[["Sales Count", "Redemption Count"]].sum()

fig_yearly = px.line(
    yearly,
    x="Year",
    y=["Sales Count", "Redemption Count"],
    markers=True,
    title="Yearly Sales and Redemption Trends"
)

st.plotly_chart(fig_yearly, use_container_width=True)

# -------------------------------
# HOURLY SALES ANALYSIS
# -------------------------------
st.subheader("🕒 Hourly Ticket Activity")

hourly = filtered_df.groupby(
    "Hour",
    as_index=False
)[["Sales Count", "Redemption Count"]].sum()

fig_hourly = px.line(
    hourly,
    x="Hour",
    y=["Sales Count", "Redemption Count"],
    markers=True,
    title="Ticket Sales by Hour"
)

fig_hourly.update_xaxes(dtick=1)

st.plotly_chart(fig_hourly, use_container_width=True)

# -------------------------------
# WEEKDAY VS WEEKEND
# -------------------------------
st.subheader("🗓️ Weekday vs Weekend Analysis")

day_summary = filtered_df.groupby(
    "Day_Type",
    as_index=False
)[["Sales Count", "Redemption Count"]].sum()

fig_day = px.bar(
    day_summary,
    x="Day_Type",
    y=["Sales Count", "Redemption Count"],
    barmode="group",
    title="Weekday vs Weekend Performance"
)

st.plotly_chart(fig_day, use_container_width=True)

# -------------------------------
# DAILY SALES TREND
# -------------------------------
st.subheader("📈 Daily Ticket Activity")

daily = filtered_df.groupby(
    "Date",
    as_index=False
)[["Sales Count", "Redemption Count"]].sum()

fig_daily = px.line(
    daily,
    x="Date",
    y=["Sales Count", "Redemption Count"],
    title="Daily Sales and Redemption Trend"
)

st.plotly_chart(fig_daily, use_container_width=True)

# -------------------------------
# TOP 10 BUSIEST DAYS
# -------------------------------
st.subheader("🏆 Top 10 Busiest Days")

top_days = daily.nlargest(10, "Sales Count")

fig_top = px.bar(
    top_days.sort_values("Sales Count"),
    x="Sales Count",
    y="Date",
    orientation="h",
    title="Top 10 Days by Ticket Sales"
)

st.plotly_chart(fig_top, use_container_width=True)

# -------------------------------
# DATA TABLE
# -------------------------------
with st.expander("View Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.divider()

st.caption(
    "Toronto Island Ferry Ticket Sales & Redemption Analytics | "
    "Unified Mentor Internship Project"
)
