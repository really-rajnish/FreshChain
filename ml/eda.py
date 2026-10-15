import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any
from ml.data_loader import load_raw_data, clean_and_standardize_data

# Dark modern aesthetic theme for plots
plt.style.use("dark_background")
PALETTE = ["#10b981", "#ef4444", "#3b82f6", "#f59e0b", "#8b5cf6"]

def get_charts_dir() -> str:
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "charts")
    os.makedirs(charts_dir, exist_ok=True)
    return charts_dir

def generate_all_eda_charts(df: pd.DataFrame = None) -> List[str]:
    """
    Generates rich exploratory data analysis charts and saves them to static/charts.
    Returns list of generated chart image filenames.
    """
    if df is None:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        
    charts_dir = get_charts_dir()
    generated_files = []
    
    # 1. Target Class Distribution
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#1f2937")
    
    class_counts = df["Class"].value_counts()
    colors = ["#10b981" if c == "Good" else "#ef4444" for c in class_counts.index]
    bars = ax.bar(class_counts.index, class_counts.values, color=colors, edgecolor="#374151", width=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f"{int(height)} ({height/len(df)*100:.1f}%)",
                ha="center", va="bottom", color="#f3f4f6", fontsize=10, fontweight="bold")
                
    ax.set_title("Produce Quality Class Distribution", fontsize=12, fontweight="bold", pad=15, color="#f9fafb")
    ax.set_ylabel("Count", fontsize=10, color="#9ca3af")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#4b5563")
    plt.tight_layout()
    chart1_path = os.path.join(charts_dir, "class_distribution.png")
    fig.savefig(chart1_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    generated_files.append("class_distribution.png")
    
    # 2. Fruit Counts Distribution
    fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#1f2937")
    
    fruit_counts = df["Fruit"].value_counts().reset_index()
    fruit_counts.columns = ["Fruit", "Count"]
    sns.barplot(data=fruit_counts, x="Fruit", y="Count", hue="Fruit", palette="viridis", ax=ax, edgecolor="#374151", legend=False)
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", xytext=(0, 4), textcoords="offset points", color="#f3f4f6", fontsize=9)
    ax.set_title("Sample Count per Fruit Variety", fontsize=12, fontweight="bold", pad=15, color="#f9fafb")
    ax.set_ylabel("Count", fontsize=10, color="#9ca3af")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#4b5563")
    plt.tight_layout()
    chart2_path = os.path.join(charts_dir, "fruit_distribution.png")
    fig.savefig(chart2_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    generated_files.append("fruit_distribution.png")
    
    # 3. Fruit vs Quality Class breakdown
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#1f2937")
    
    crosstab = pd.crosstab(df["Fruit"], df["Class"])
    crosstab.plot(kind="bar", stacked=False, color=["#ef4444", "#10b981"], ax=ax, edgecolor="#374151", width=0.6)
    ax.set_title("Fruit Variety vs Freshness Quality Outcome", fontsize=12, fontweight="bold", pad=15, color="#f9fafb")
    ax.set_ylabel("Count", fontsize=10, color="#9ca3af")
    ax.set_xlabel("Fruit", fontsize=10, color="#9ca3af")
    ax.legend(title="Quality", facecolor="#1f2937", edgecolor="#374151")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#4b5563")
    plt.xticks(rotation=0)
    plt.tight_layout()
    chart3_path = os.path.join(charts_dir, "fruit_vs_quality.png")
    fig.savefig(chart3_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    generated_files.append("fruit_vs_quality.png")
    
    # 4. Temperature & Humidity Boxplots by Class
    num_cols = ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"]
    valid_num_cols = [c for c in num_cols if c in df.columns]
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor("#111827")
    
    palette_dict = {"Good": "#10b981", "Bad": "#ef4444"}
    
    for i, col in enumerate(valid_num_cols):
        ax = axes[i // 2, i % 2]
        ax.set_facecolor("#1f2937")
        sns.boxplot(x="Class", y=col, data=df, hue="Class", palette=palette_dict, ax=ax, width=0.4, fliersize=2, legend=False)
        ax.set_title(f"{col} Distribution by Quality", fontsize=11, fontweight="bold", color="#f9fafb")
        ax.grid(True, linestyle="--", alpha=0.2, color="#4b5563")
        ax.set_xlabel("")

        
    plt.tight_layout()
    chart4_path = os.path.join(charts_dir, "environmental_distributions.png")
    fig.savefig(chart4_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    generated_files.append("environmental_distributions.png")
    
    # 5. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#1f2937")
    
    num_df = df[valid_num_cols].copy()
    if "Class" in df.columns:
        num_df["Target_Good"] = (df["Class"] == "Good").astype(int)
        
    corr = num_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax,
                linewidths=1, linecolor="#111827", annot_kws={"size": 9, "fontweight": "bold"})
    ax.set_title("Feature Correlation Heatmap", fontsize=12, fontweight="bold", pad=15, color="#f9fafb")
    plt.tight_layout()
    chart5_path = os.path.join(charts_dir, "correlation_heatmap.png")
    fig.savefig(chart5_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    generated_files.append("correlation_heatmap.png")
    
    return generated_files

def get_eda_insights(df: pd.DataFrame = None) -> Dict[str, Any]:
    """Calculates granular statistical aggregations for the EDA web UI."""
    if df is None:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        
    insights = {
        "total_records": len(df),
        "good_pct": round((df["Class"] == "Good").mean() * 100, 2) if "Class" in df.columns else 0,
        "bad_pct": round((df["Class"] == "Bad").mean() * 100, 2) if "Class" in df.columns else 0,
        "fruit_breakdown": df.groupby("Fruit")["Class"].value_counts(normalize=True).unstack().round(3).to_dict(orient="index") if "Fruit" in df.columns and "Class" in df.columns else {},
        "env_averages_by_class": df.groupby("Class")[["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"]].mean().round(2).to_dict(orient="index") if "Class" in df.columns else {}
    }
    return insights

if __name__ == "__main__":
    charts = generate_all_eda_charts()
    print("Generated charts:", charts)
    print("Insights:", get_eda_insights())
