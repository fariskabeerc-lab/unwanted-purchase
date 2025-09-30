import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Title ---
st.set_page_config(page_title="Non-Selling Items Dashboard", layout="wide")
st.title("High-Value Non-Selling Items Dashboard")

# --- Load Excel Files ---
file1 = "unwanted1.xlsx"
file2 = "unwanted2.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# --- Combine both files ---
df = pd.concat([df1, df2], ignore_index=True)
df.columns = df.columns.str.strip()

# --- Filter zero sales items ---
zero_sales_items = df[df['Total Sales'] == 0].copy()

# --- Calculate Stock Value if not present ---
if 'Stock Value' not in zero_sales_items.columns or zero_sales_items['Stock Value'].isnull().all():
    zero_sales_items['Stock Value'] = zero_sales_items['Cost'] * zero_sales_items['Stock']

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Category filter with "All"
categories = zero_sales_items['Category'].dropna().unique().tolist()
categories.sort()
categories = ["All"] + categories
selected_category = st.sidebar.selectbox("Select Category", categories)

if selected_category != "All":
    filtered_items = zero_sales_items[zero_sales_items['Category'] == selected_category]
else:
    filtered_items = zero_sales_items.copy()

# Item filter (optional, itemwise)
items = filtered_items['Item Name'].dropna().unique().tolist()
items.sort()
items = ["All"] + items
selected_item = st.sidebar.selectbox("Select Item", items)

if selected_item != "All":
    filtered_items = filtered_items[filtered_items['Item Name'] == selected_item]

# --- Create Tabs ---
tab1, tab2 = st.tabs(["Top Valued Items", "Suppliers Analysis"])

# ---------------- Tab 1: Top Valued Items ----------------
with tab1:
    st.subheader("Top Non-Selling Items by Value and Quantity")

    top_value_items = filtered_items.sort_values(by='Stock Value', ascending=False)

    st.dataframe(top_value_items[['Item Name', 'Category', 'Stock', 'Cost', 'Stock Value']].head(20))

    # Horizontal bar chart for Stock Value
    fig_value = px.bar(
        top_value_items.head(20),
        x='Stock Value',
        y='Item Name',
        orientation='h',
        text='Stock Value',
        title="Top 20 Non-Selling Items by Stock Value",
        height=600
    )
    fig_value.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
    fig_value.update_traces(marker_color='indianred', marker_line_color='black', marker_line_width=1.5)
    st.plotly_chart(fig_value, use_container_width=True)

    # Horizontal bar chart for Quantity (Stock)
    fig_qty = px.bar(
        top_value_items.head(20),
        x='Stock',
        y='Item Name',
        orientation='h',
        text='Stock',
        title="Top 20 Non-Selling Items by Quantity",
        height=600
    )
    fig_qty.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
    fig_qty.update_traces(marker_color='mediumseagreen', marker_line_color='black', marker_line_width=1.5)
    st.plotly_chart(fig_qty, use_container_width=True)

# ---------------- Tab 2: Suppliers Analysis ----------------
with tab2:
    st.subheader("Suppliers with Highest Value of Non-Selling Items")

    supplier_analysis = filtered_items.groupby('LP Supplier')['Stock Value'].sum().reset_index()
    supplier_analysis = supplier_analysis.sort_values(by='Stock Value', ascending=False)

    st.dataframe(supplier_analysis)

    # Horizontal bar chart for suppliers
    fig_supplier = px.bar(
        supplier_analysis,
        x='Stock Value',
        y='LP Supplier',
        orientation='h',
        text='Stock Value',
        title="Suppliers by Total Value of Non-Selling Items",
        height=600
    )
    fig_supplier.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
    fig_supplier.update_traces(marker_color='royalblue', marker_line_color='black', marker_line_width=1.5)
    st.plotly_chart(fig_supplier, use_container_width=True)

    # Optional: select supplier to see their top items
    supplier_select = st.selectbox("Select Supplier to view top items", supplier_analysis['LP Supplier'].unique())
    top_items = filtered_items[filtered_items['LP Supplier'] == supplier_select]
    top_items = top_items.sort_values(by='Stock Value', ascending=False)
    st.dataframe(top_items[['Item Name', 'Category', 'Stock', 'Cost', 'Stock Value']].head(20))
