import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Blinkit Dashboard",
    page_icon="🛒",
    layout="wide"
)

df=pd.read_excel("Blinkit Grocery Data.xlsx" )

df["Item Fat Content"] = df["Item Fat Content"].replace({
    "low fat": "Low Fat",
    "LF": "Low Fat",
    "reg": "Regular"
})
st.sidebar.title("Filters")

item_type = st.sidebar.multiselect(
    "Item Type",
    df["Item Type"].unique(),
    default=df["Item Type"].unique()
)

outlet_location=st.sidebar.multiselect(
    "Outlet Location",
    df["Outlet Location Type"].unique(),
    default=df["Outlet Location Type"].unique()
)

outlet_size=st.sidebar.multiselect(
    "Outlet Size",
    df["Outlet Size"].unique(),
    default=df["Outlet Size"].unique()
)

df=df[
    (df["Item Type"].isin(item_type)) &
    (df["Outlet Location Type"].isin(outlet_location))&
    (df["Outlet Size"].isin(outlet_size))
]
st.markdown("<h1 style='text-align:center;'>Blinkit Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

total_sales=df["Sales"].sum()
avg_sales=df["Sales"].mean()
avg_rating = df["Rating"].mean()
total_items = df["Item Identifier"].nunique()


k1,k2,k3,k4 = st.columns(4)
k1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
k2.metric("📈 Average Sales",f"₹{avg_sales:,.0f}")
k3.metric("🛒 Number of Items",total_items)
k4.metric("Average Rating", round(avg_rating, 2))

st.markdown("---")

c1,c2 = st.columns(2)

with c1:
    st.subheader("Fat Content")
    fat=df.groupby("Item Fat Content")["Sales"].sum()
    fig,ax=plt.subplots()
    ax.pie(fat, labels=fat.index, autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)

with c2:
    st.subheader("Item Type ")
    item=df.groupby("Item Type")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.bar(item.index, item.values)
    ax.set_ylabel("Sales")
    plt.xticks(rotation=90)
    st.pyplot(fig)

c3,c4=st.columns(2)

with c3:
    st.subheader("Outlet Establishment")
    est = df.groupby("Outlet Establishment Year")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.plot(est.index, est.values, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sales")
    st.pyplot(fig)

with c4:
    st.subheader("Outlet Size")
    size = df.groupby("Outlet Size")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.pie(size, labels=size.index, autopct="%1.1f%%")
    st.pyplot(fig)

c5, c6 = st.columns(2)

with c5:
    st.subheader("Fat by Outlet Size")
    fat_outlet = df.pivot_table(
        values="Sales",
        index="Outlet Size",
        columns="Item Fat Content",
        aggfunc="sum"
    )
    fig, ax = plt.subplots()
    fat_outlet.plot(kind="bar", stacked=True, ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

with c6:
    st.subheader("Outlet Type")
    outlet_type = df.groupby("Outlet Type")["Sales"].sum()
    fig, ax = plt.subplots()
    ax.bar(outlet_type.index, outlet_type.values)
    ax.set_ylabel("Sales")
    st.pyplot(fig)




