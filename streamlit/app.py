
import streamlit as st
import os
import pandas as pd
import altair as alt

st.set_page_config(page_title="Global Retail Sales Dashboard", layout="wide")

# Custom CSS for KPI cards
st.markdown("""
<style>
    .dashboard-header {
        padding: 0.5rem 0 1.5rem 0;
    }
    .dashboard-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .dashboard-header p {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 0;
    }
    .kpi-section-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        color: #6b7280;
        text-transform: uppercase;
        margin-bottom: 1rem;
        padding-top: 0.5rem;
    }
    .kpi-card {
        background: linear-gradient(180deg, #ffffff 0%, #f0f7ff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: left;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.75rem;
    }
    .kpi-icon svg {
        width: 18px;
        height: 18px;
        color: #3b5bdb;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: #6b7280;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.3rem;
    }
    .kpi-subtitle {
        font-size: 0.72rem;
        color: #94a3b8;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="dashboard-header">
    <h1>Global Retail Sales Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# Connect to Snowflake
conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()


@st.cache_data
def load_sales_data():
    return session.table("COMMERCIAL_ANALYTICS.SILVER.SALES_CLEAN").to_pandas()


with st.spinner("Loading data..."):
    df = load_sales_data()

# Parse year and month from SALE_DATE
df["SALE_DATE"] = pd.to_datetime(df["SALE_DATE"])
df["YEAR"] = df["SALE_DATE"].dt.year
df["MONTH"] = df["SALE_DATE"].dt.month

# --- Filters (horizontal row below header) ---
month_names = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}

all_countries = sorted(df["COUNTRY"].unique().tolist())
all_years = sorted(df["YEAR"].unique().tolist())
month_options = ["All"] + [month_names[m] for m in sorted(df["MONTH"].unique().tolist())]
all_customers = sorted(df["CUSTOMER_NAME"].unique().tolist())

with st.container(border=True):
    st.markdown("""
    <div style="margin-bottom: 0.75rem;">
        <span style="font-size: 1.1rem; font-weight: 700; color: #1a1a2e;">🔽 Filters</span><br>
        <span style="font-size: 0.85rem; color: #6b7280;">Refine dashboard insights</span>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1, 0.6])
    with f1:
        selected_country = st.selectbox("🌍 Country", ["All"] + all_countries)
    with f2:
        selected_year = st.selectbox("📅 Year", ["All"] + all_years)
    with f3:
        selected_month_label = st.selectbox("🗓️ Month", month_options)
    with f4:
        selected_customer = st.selectbox("👤 Customer", ["All"] + all_customers)
    with f5:
        st.markdown("<br>", unsafe_allow_html=True)

        def clear_cache():
            load_sales_data.clear()

        st.button("🔄 Reset Filters", on_click=clear_cache, type="primary")

# --- Apply filters ---
filtered = df.copy()
if selected_country != "All":
    filtered = filtered[filtered["COUNTRY"] == selected_country]
if selected_year != "All":
    filtered = filtered[filtered["YEAR"] == selected_year]
if selected_month_label != "All":
    month_num = [k for k, v in month_names.items() if v == selected_month_label][0]
    filtered = filtered[filtered["MONTH"] == month_num]
if selected_customer != "All":
    filtered = filtered[filtered["CUSTOMER_NAME"] == selected_customer]

# ============================================================
# SECTION 1: Key Performance Indicators
# ============================================================
st.markdown('<div class="kpi-section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

total_sales = filtered["TOTAL_AMOUNT"].sum()
total_orders = filtered["SALE_ID"].nunique()
avg_order = total_sales / total_orders if total_orders > 0 else 0
total_quantity = filtered["QUANTITY"].sum()


def format_compact(value, prefix="", suffix=""):
    if value >= 1_000_000:
        return f"{prefix}{value / 1_000_000:,.2f}M{suffix}"
    elif value >= 1_000:
        return f"{prefix}{value / 1_000:,.2f}K{suffix}"
    return f"{prefix}{value:,.2f}{suffix}"


def kpi_card_html(icon_svg, label, value, subtitle):
    return f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-icon">{icon_svg}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """


icon_dollar = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b5bdb"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.637.392M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/></svg>'
icon_orders = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b5bdb"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"/></svg>'
icon_avg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b5bdb"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Z"/></svg>'
icon_qty = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b5bdb"><path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"/></svg>'

kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")

with kpi1:
    st.markdown(kpi_card_html(icon_dollar, "Total Sales", format_compact(total_sales, prefix="$"), "Total revenue generated"), unsafe_allow_html=True)
with kpi2:
    st.markdown(kpi_card_html(icon_orders, "Orders", format_compact(total_orders), "Total number of orders"), unsafe_allow_html=True)
with kpi3:
    st.markdown(kpi_card_html(icon_avg, "Average Order Value", f"${avg_order:,.2f}", "Average order amount"), unsafe_allow_html=True)
with kpi4:
    st.markdown(kpi_card_html(icon_qty, "Quantity Sold", format_compact(total_quantity), "Total items sold"), unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 2: Sales by Country & Top Products (side by side)
# ============================================================
st.markdown("""
<div style="margin-top: 1rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem;">🌍 Regional & Product Performance</h2>
    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0;">Sales distribution by country and top performing products</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="medium")

with col_left:
    with st.container(border=True, height=450):
        st.markdown("**Sales by Country**")
        st.caption("Total sales generated in each country")
        sales_by_country = (
            filtered.groupby("COUNTRY")["TOTAL_AMOUNT"]
            .sum()
            .reset_index()
            .rename(columns={"TOTAL_AMOUNT": "Total Sales (USD)"})
        )
        bars = alt.Chart(sales_by_country).mark_bar(
            color="#3b5bdb", cornerRadiusTopLeft=4, cornerRadiusTopRight=4
        ).encode(
            x=alt.X("COUNTRY:N", title="Country", sort="-y"),
            y=alt.Y("Total Sales (USD):Q", title="Total Sales (USD)"),
        )
        text = bars.mark_text(dy=-10, fontSize=11, fontWeight="bold").encode(
            text=alt.Text("Total Sales (USD):Q", format=",.0f")
        )
        st.altair_chart(bars + text, use_container_width=True)

with col_right:
    with st.container(border=True, height=450):
        st.markdown("**Top 10 Products**")
        st.caption("By total sales")
        top_products = (
            filtered.groupby("PRODUCT_NAME")["TOTAL_AMOUNT"]
            .sum()
            .reset_index()
            .rename(columns={"TOTAL_AMOUNT": "Total Sales (USD)"})
            .sort_values("Total Sales (USD)", ascending=False)
            .head(10)
        )
        chart_products = alt.Chart(top_products).mark_bar(
            color="#3b5bdb", cornerRadiusEnd=4
        ).encode(
            x=alt.X("Total Sales (USD):Q", title="Total Sales (USD)"),
            y=alt.Y("PRODUCT_NAME:N", title="Product", sort="-x"),
        )
        st.altair_chart(chart_products, use_container_width=True)

# Insights box
top_country = (
    filtered.groupby("COUNTRY")["TOTAL_AMOUNT"].sum().idxmax()
    if not filtered.empty else "N/A"
)
top_product = (
    filtered.groupby("PRODUCT_NAME")["TOTAL_AMOUNT"].sum().idxmax()
    if not filtered.empty else "N/A"
)
st.info(f"**Insights:** {top_country} leads in total sales among countries. {top_product} is the top performing product.")

st.divider()

# ============================================================
# SECTION 3: Monthly Sales Trend (full width)
# ============================================================
st.markdown("""
<div style="margin-top: 1rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem;">📈 Monthly Sales Trend</h2>
    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0;">Total sales over time</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    filtered["SALE_MONTH"] = filtered["SALE_DATE"].dt.to_period("M").astype(str)
    sales_by_month = (
        filtered.groupby("SALE_MONTH")["TOTAL_AMOUNT"]
        .sum()
        .reset_index()
        .rename(columns={"TOTAL_AMOUNT": "TOTAL_SALES"})
        .sort_values("SALE_MONTH")
    )

    # Summary KPI row
    total_sales_all = sales_by_month["TOTAL_SALES"].sum()
    best_month_row = sales_by_month.loc[sales_by_month["TOTAL_SALES"].idxmax()]
    worst_month_row = sales_by_month.loc[sales_by_month["TOTAL_SALES"].idxmin()]
    avg_monthly = sales_by_month["TOTAL_SALES"].mean()

    # Period-over-period growth
    if len(sales_by_month) >= 2:
        prev_val = sales_by_month.iloc[-2]["TOTAL_SALES"]
        curr_val = sales_by_month.iloc[-1]["TOTAL_SALES"]
        growth_pct = ((curr_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
    else:
        growth_pct = 0

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; padding: 0.75rem; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div>
            <span style="font-size: 0.75rem; color: #6b7280;">Total Sales</span><br>
            <span style="font-size: 1.3rem; font-weight: 700; color: #1a1a2e;">{format_compact(total_sales_all, prefix="$")}</span>
        </div>
        <div style="margin-left: 1rem;">
            <span style="font-size: 0.75rem; color: {'#16a34a' if growth_pct >= 0 else '#dc2626'};">{"+" if growth_pct >= 0 else ""}{growth_pct:.1f}%</span><br>
            <span style="font-size: 0.7rem; color: #94a3b8;">vs previous period</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Line chart with points
    line = alt.Chart(sales_by_month).mark_line(
        color="#3b5bdb", strokeWidth=2.5
    ).encode(
        x=alt.X("SALE_MONTH:N", title="Month", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("TOTAL_SALES:Q", title="Total Sales (USD)", scale=alt.Scale(zero=False)),
    )
    points = alt.Chart(sales_by_month).mark_circle(
        color="#3b5bdb", size=40
    ).encode(
        x=alt.X("SALE_MONTH:N"),
        y=alt.Y("TOTAL_SALES:Q"),
    )
    area = alt.Chart(sales_by_month).mark_area(
        opacity=0.08, color="#3b5bdb"
    ).encode(
        x=alt.X("SALE_MONTH:N"),
        y=alt.Y("TOTAL_SALES:Q", scale=alt.Scale(zero=False)),
    )
    st.altair_chart(area + line + points, use_container_width=True)

    # Bottom metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 0.7rem; color: #6b7280;">Best Month</span><br>
            <span style="font-size: 1rem; font-weight: 700; color: #1a1a2e;">{best_month_row['SALE_MONTH']}</span><br>
            <span style="font-size: 0.7rem; color: #94a3b8;">{format_compact(best_month_row['TOTAL_SALES'], prefix="$")}</span>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 0.7rem; color: #6b7280;">Average Monthly Sales</span><br>
            <span style="font-size: 1rem; font-weight: 700; color: #1a1a2e;">{format_compact(avg_monthly, prefix="$")}</span>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 0.7rem; color: #6b7280;">Lowest Month</span><br>
            <span style="font-size: 1rem; font-weight: 700; color: #1a1a2e;">{worst_month_row['SALE_MONTH']}</span><br>
            <span style="font-size: 0.7rem; color: #94a3b8;">{format_compact(worst_month_row['TOTAL_SALES'], prefix="$")}</span>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 0.7rem; color: #6b7280;">vs Previous Period</span><br>
            <span style="font-size: 1rem; font-weight: 700; color: {'#16a34a' if growth_pct >= 0 else '#dc2626'};">{"+" if growth_pct >= 0 else ""}{growth_pct:.1f}%</span><br>
            <span style="font-size: 0.7rem; color: #94a3b8;">Growth</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 4: Top Customers (full-width interactive table)
# ============================================================
st.markdown("""
<div style="margin-top: 1rem;">
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem;">👥 Top 10 Customers</h2>
    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0;">Customers ranked by total sales</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    top_customers = (
        filtered.groupby("CUSTOMER_NAME")["TOTAL_AMOUNT"]
        .sum()
        .reset_index()
        .rename(columns={"CUSTOMER_NAME": "Customer Name", "TOTAL_AMOUNT": "Total Sales (USD)"})
        .sort_values("Total Sales (USD)", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top_customers.index = top_customers.index + 1
    top_customers.index.name = "Rank"

    st.dataframe(
        top_customers.style.format({"Total Sales (USD)": "${:,.2f}"}).bar(
            subset=["Total Sales (USD)"], color="#c7d2fe", vmin=0
        ),
        use_container_width=True,
        height=420,
    )
    st.caption(f"Showing 1 to 10 of {min(10, len(top_customers))} customers")
