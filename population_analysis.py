import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv("population_data.csv")

# 2. Feature engineering
df["Density_per_SqKm"] = (df["Population_Millions"] * 1_000_000) / (df["Area_Thousand_SqKm"] * 1000)

# 3. Basic overview
print("=== Dataset Overview ===")
print(df.head())
print("\nShape:", df.shape)
print("Missing values:\n", df.isnull().sum())

print("\n=== Summary Statistics ===")
print(df.describe().round(2))

# 4. Key insights
print("\n=== Key Insights ===")
print("Total population (millions):", round(df["Population_Millions"].sum(), 1))
print("Average growth rate (%):", round(df["Growth_Rate_Pct"].mean(), 2))

print("\nTop 5 most populated states:")
print(df.nlargest(5, "Population_Millions")[["State", "Population_Millions"]].to_string(index=False))

print("\nTop 5 densest states:")
print(df.nlargest(5, "Density_per_SqKm")[["State", "Density_per_SqKm"]].round(1).to_string(index=False))

print("\nFastest growing states:")
print(df.nlargest(5, "Growth_Rate_Pct")[["State", "Growth_Rate_Pct"]].to_string(index=False))

# 5. Region-wise analysis
region = df.groupby("Region").agg(
    Total_Population=("Population_Millions", "sum"),
    Avg_Growth=("Growth_Rate_Pct", "mean"),
    Avg_Literacy=("Literacy_Pct", "mean"),
    Avg_Urban=("Urban_Pct", "mean"),
).round(2)
print("\n=== Region-wise Summary ===")
print(region)

# 6. Correlations
print("\n=== Correlation Matrix ===")
print(df[["Population_Millions", "Growth_Rate_Pct", "Literacy_Pct", "Urban_Pct", "Density_per_SqKm"]].corr().round(2))

# 7. Chart 1: Literacy vs Growth rate (scatter)
plt.figure(figsize=(8, 5))
plt.scatter(df["Literacy_Pct"], df["Growth_Rate_Pct"], color="teal")
m, c = pd.Series(df["Growth_Rate_Pct"]).pipe(lambda y: (
    ((df["Literacy_Pct"] - df["Literacy_Pct"].mean()) * (y - y.mean())).sum()
    / ((df["Literacy_Pct"] - df["Literacy_Pct"].mean()) ** 2).sum(),
    None))
c = df["Growth_Rate_Pct"].mean() - m * df["Literacy_Pct"].mean()
xs = [df["Literacy_Pct"].min(), df["Literacy_Pct"].max()]
plt.plot(xs, [m * x + c for x in xs], color="red", linestyle="--", label="Trend line")
plt.xlabel("Literacy Rate (%)")
plt.ylabel("Population Growth Rate (%)")
plt.title("Literacy Rate vs Population Growth Rate")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("literacy_vs_growth.png", dpi=150)
plt.close()

# 8. Chart 2: Region-wise total population (bar)
plt.figure(figsize=(8, 5))
region["Total_Population"].sort_values().plot(kind="bar", color="steelblue")
plt.xlabel("Region")
plt.ylabel("Total Population (Millions)")
plt.title("Region-wise Total Population")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("region_population.png", dpi=150)
plt.close()

print("\nCharts saved: literacy_vs_growth.png, region_population.png")
