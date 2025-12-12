# -------------------------------------------------------------
# Flipkart E-Commerce Data Analysis Dashboard
# -------------------------------------------------------------

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------- PAGE CONFIG (MUST BE FIRST) -------------------
st.set_page_config(page_title="Flipkart Dashboard", layout="wide")

# ------------------- DATA LOADING -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("flipkart_com-ecommerce_sample.csv")

    # Extract main category from product_category_tree
    df["main_category"] = (
        df["product_category_tree"]
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace("'", "", regex=False)
        .str.split(">>")
        .str[0]
        .str.strip()
    )

    # Convert ratings to numeric
    df["product_rating"] = pd.to_numeric(df["product_rating"], errors="coerce")
    df["overall_rating"] = pd.to_numeric(df["overall_rating"], errors="coerce")

    df["product_rating"] = df["product_rating"].fillna(df["product_rating"].median())
    df["overall_rating"] = df["overall_rating"].fillna(df["overall_rating"].median())

    # Discount percentage
    df["discount_percent"] = (
        (df["retail_price"] - df["discounted_price"]) / df["retail_price"]
    ) * 100

    return df

df = load_data()

# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.title("📊 Dashboard Navigation")

    page = st.radio(
        "Go to section:",
        [
            "🏠 Overview",
            "📦 Product Categories",
            "⭐ Rating Analysis",
            "💰 Price Analysis",
            "🏷️ Discount Analysis",
            "🔍 Filter by Category",
        ]
    )
    st.markdown("---")
    st.write("Created by **Chandana** 😊")

# -------------------------------------------------------------
# 1️⃣ OVERVIEW PAGE
# -------------------------------------------------------------
if page == "🏠 Overview":
    st.title("🏠 Flipkart E-Commerce Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", f"{len(df):,}")
    col2.metric("Unique Categories", df["main_category"].nunique())
    col3.metric("Average Rating", round(df["product_rating"].mean(), 2))

    st.write("### 📌 Dataset Preview")
    st.dataframe(df.head(10))

# -------------------------------------------------------------
# 2️⃣ PRODUCT CATEGORIES
# -------------------------------------------------------------
elif page == "📦 Product Categories":
    st.title("📦 Product Count by Main Category")

    top_categories = df["main_category"].value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette="viridis")
    plt.title("Top 15 Product Categories")
    plt.xlabel("Count")
    plt.ylabel("Category")
    st.pyplot(fig)

# -------------------------------------------------------------
# 3️⃣ RATING ANALYSIS
# -------------------------------------------------------------
elif page == "⭐ Rating Analysis":
    st.title("⭐ Distribution of Product Ratings")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["product_rating"], bins=30, kde=True)
    plt.xlabel("Rating")
    plt.ylabel("Number of Products")
    st.pyplot(fig)

# -------------------------------------------------------------
# 4️⃣ PRICE ANALYSIS
# -------------------------------------------------------------
elif page == "💰 Price Analysis":
    st.title("💰 Relationship Between Price and Rating")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=df["discounted_price"], y=df["product_rating"], alpha=0.5)
    plt.xlabel("Selling Price (Discounted Price)")
    plt.ylabel("Product Rating")
    st.pyplot(fig)

# -------------------------------------------------------------
# 5️⃣ DISCOUNT ANALYSIS
# -------------------------------------------------------------
elif page == "🏷️ Discount Analysis":
    st.title("🏷️ Distribution of Discount Percentage")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["discount_percent"], bins=50, kde=True)
    plt.xlabel("Discount (%)")
    plt.ylabel("Number of Products")
    st.pyplot(fig)

# -------------------------------------------------------------
# 6️⃣ FILTER PRODUCTS BY CATEGORY
# -------------------------------------------------------------
elif page == "🔍 Filter by Category":
    st.title("🔍 Filter Products by Category")

    categories = sorted(df["main_category"].dropna().unique())
    category_selected = st.selectbox("Select a category:", categories)

    filtered = df[df["main_category"] == category_selected]

    st.write(f"### Showing {len(filtered)} products in **{category_selected}**")
    st.dataframe(filtered[["product_name", "retail_price", "discounted_price", "product_rating"]])
