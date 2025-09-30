import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Title ---
st.set_page_config(page_title="Unwanted Purchase Dashboard", layout="wide")
st.title("Unwanted Purchase Quantity Dashboard")

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

# Item filter (optional)
items = filtered_items['Item Name'].dropna().unique().tolist()
items.sort()
items = ["All"] + items
selected_item = st.sidebar.selectbox("Select Item", items)

if selected_item != "All":
    filtered_items = filtered_items[filtered_items['Item Name'] == selected_item]

# --- Create Tabs ---
tab1, tab2 = st.tabs(["Top Unwanted Purchase Items", "Suppliers Analysis"])

# ---------------- Tab 1: Top Unwanted Purchase Items ----------------
with tab1:
    st.subheader("Top Unwanted Purchase Items by Quantity")

    top_items_qty = filtered_items.sort_values(by='Stock', ascending=False)

    st.dataframe(top_items_qty[['Item Name', 'Category', 'Stock', 'LP Qty']].head(20))

    # Horizontal bar chart for Stock Quantity
    fig_qty = px.bar(
        top_items_qty.head(20),
        x='Stock',
        y='Item Name',
        orientation='h',
        text='Stock',
        title="Top 20 Unwanted Purchase Items by Quantity",
        height=600
    )
    fig_qty.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
    fig_qty.update_traces(marker_color='indianred', marker_line_color='black', marker_line_width=1.5)
    st.plotly_chart(fig_qty, use_container_width=True)

    # Optional: bar chart for LP Qty if available
    if 'LP Qty' in filtered_items.columns:
        fig_lpqty = px.bar(
            top_items_qty.head(20),
            x='LP Qty',
            y='Item Name',
            orientation='h',
            text='LP Qty',
            title="Top 20 Unwanted Purchase Items by Purchased Quantity (LP Qty)",
            height=600
        )
        fig_lpqty.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
        fig_lpqty.update_traces(marker_color='mediumseagreen', marker_line_color='black', marker_line_width=1.5)
        st.plotly_chart(fig_lpqty, use_container_width=True)

# ---------------- Tab 2: Suppliers Analysis ----------------
with tab2:
    st.subheader("Suppliers with Highest Unwanted Purchase Quantity")

    supplier_analysis = filtered_items.groupby('LP Supplier')['Stock'].sum().reset_index()
    supplier_analysis = supplier_analysis.sort_values(by='Stock', ascending=False)

    st.dataframe(supplier_analysis)

    # Horizontal bar chart for suppliers by quantity
    fig_supplier = px.bar(
        supplier_analysis,
        x='Stock',
        y='LP Supplier',
        orientation='h',
        text='Stock',
        title="Suppliers by Total Unwanted Purchase Quantity",
        height=600
    )
    fig_supplier.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150, r=50, t=50, b=50))
    fig_supplier.update_traces(marker_color='royalblue', marker_line_color='black', marker_line_width=1.5)
    st.plotly_chart(fig_supplier, use_container_width=True)

    # Optional: select supplier to see their top items
    supplier_select = st.selectbox("Select Supplier to view top items", supplier_analysis['LP Supplier'].unique())
    top_items_supplier = filtered_items[filtered_items['LP Supplier'] == supplier_select]
    top_items_supplier = top_items_supplier.sort_values(by='Stock', ascending=False)
    st.dataframe(top_items_supplier[['Item Name', 'Category', 'Stock', 'LP Qty']].head(20))
