import pandas as pd
import matplotlib.pyplot as plt

messy = pd.DataFrame({
    "product": ["Widget A", "Widget B", "widget a", "Widget C", "Widget B",
                "Widget A", " Widget C", "Widget D", None, "Widget A"],
    "sales": ["150", "200", "175", "300", "200",
              "180", "250", "abc", "100", "-50"],
    "date": ["2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02", "2025-01-03",
             "2025-01-03", "2025-01-04", "2025-01-04", "2025-01-05", "2025-01-05"],
    "region": ["North", "South", "north", "East", "South",
               "West", "east", "North", "South", "West"],
})

df = pd.DataFrame(messy)
print("=== Original Data ===")
print(df)

df["product"] = df["product"].str.strip()

df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["region"] = df["region"].str.strip().str.title()
df["product"] = df["product"].str.strip().str.title()

df = df.drop_duplicates(subset=["product", "date", "region"], keep="first")

df = df.dropna(subset=["product"])
df.loc[df["sales"] < 0, "sales"] = pd.NA
print("\n=== Cleaned Data ===")
print(df)

fig, axes = plt.subplots(1, 3, figsize=(15,5))
# Chart 1: Total Sales by Product
product_sales = df.groupby("product")["sales"].sum().sort_values(ascending=False)
axes[0].bar(product_sales.index, product_sales.values, color="skyblue")
axes[0].set_title("Total Sales by Product")
axes[0].set_ylabel("Total Sales")
axes[0].tick_params(axis="x", rotation=45)

# Chart 2: Daily Trend
daily_trend = df.groupby("date")["sales"].mean().sort_values(ascending=False)
axes[1].bar(daily_trend.index, daily_trend.values, color="seagreen")
axes[1].set_title("Daily Trend")
axes[1].set_xlabel("Date")

# Chart 3: Distribution
df["sales"].dropna().hist(ax=axes[2], bins=10, color="purple", edgecolor="black")
axes[2].set_title("Sales Distribution")
axes[2].set_xlabel("Sales ($)")
axes[2].set_ylabel("Count")

plt.tight_layout()
plt.savefig("Visualizations.png")
plt.show()
