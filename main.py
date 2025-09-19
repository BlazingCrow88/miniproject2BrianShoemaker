# INF601 - Advanced Programming in Python
# Brian Shoemaker
# Mini Project 2 - Global CO2 Emissions Analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import os
from pathlib import Path
import numpy as np


def create_charts_directory():
    """Create charts directory if it doesn't exist"""
    charts_dir = Path("charts")
    charts_dir.mkdir(exist_ok=True)
    return charts_dir


def fetch_co2_data():
    """
    Fetch CO2 emissions data from World Bank API
    Returns a pandas DataFrame with CO2 emissions data
    """
    print("Fetching CO2 emissions data...")

    # World Bank API endpoint for CO2 emissions (metric tons per capita)
    url = "http://api.worldbank.org/v2/country/all/indicator/EN.ATM.CO2E.PC"
    params = {
        'format': 'json',
        'date': '2010:2020',  # Last 10 years of data
        'per_page': 1000,
        'page': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # The API returns data in the second element of the response
        if len(data) > 1 and data[1]:
            emissions_data = data[1]

            # Convert to DataFrame
            df = pd.DataFrame(emissions_data)

            # Clean and process the data
            df = df[['country', 'date', 'value']].copy()
            df = df.dropna(subset=['value'])
            df['country_name'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else x)
            df['year'] = pd.to_numeric(df['date'])
            df['co2_emissions'] = pd.to_numeric(df['value'])

            # Select only the columns we need
            df = df[['country_name', 'year', 'co2_emissions']].copy()

            return df
        else:
            print("No data received from API. Using sample data.")
            return create_sample_data()

    except Exception as e:
        print(f"Error fetching data from API: {e}")
        print("Using sample data instead.")
        return create_sample_data()


def create_sample_data():
    """Create sample CO2 emissions data if API fails"""
    countries = ['United States', 'China', 'Germany', 'Japan', 'India',
                 'Canada', 'United Kingdom', 'France', 'Brazil', 'Australia']
    years = list(range(2010, 2021))

    data = []
    np.random.seed(42)  # For reproducible results

    for country in countries:
        base_emission = np.random.uniform(5, 20)  # Base emission level
        for year in years:
            # Add some trend and randomness
            trend = (year - 2010) * 0.1 * np.random.uniform(-1, 1)
            noise = np.random.uniform(-1, 1)
            emission = max(0, base_emission + trend + noise)

            data.append({
                'country_name': country,
                'year': year,
                'co2_emissions': round(emission, 2)
            })

    return pd.DataFrame(data)


def analyze_data(df):
    """Perform basic analysis on the CO2 emissions data"""
    print("\n=== CO2 EMISSIONS ANALYSIS ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Countries in dataset: {df['country_name'].nunique()}")
    print(f"Years covered: {df['year'].min()} - {df['year'].max()}")

    print("\n=== TOP 10 COUNTRIES BY AVERAGE CO2 EMISSIONS ===")
    avg_emissions = df.groupby('country_name')['co2_emissions'].mean().sort_values(ascending=False)
    print(avg_emissions.head(10).round(2))

    print("\n=== BASIC STATISTICS ===")
    print(df['co2_emissions'].describe().round(2))

    return avg_emissions


def create_visualizations(df, charts_dir):
    """Create various visualizations of the CO2 emissions data"""

    # Set the style for better-looking plots
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # 1. Line plot showing trends over time for top countries
    plt.figure(figsize=(12, 8))
    top_countries = df.groupby('country_name')['co2_emissions'].mean().nlargest(8).index

    for country in top_countries:
        country_data = df[df['country_name'] == country]
        plt.plot(country_data['year'], country_data['co2_emissions'],
                 marker='o', linewidth=2, label=country)

    plt.title('CO2 Emissions Trends Over Time (Top 8 Countries)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('CO2 Emissions (metric tons per capita)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(charts_dir / 'co2_trends_line_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: co2_trends_line_plot.png")

    # 2. Bar chart of average emissions by country
    plt.figure(figsize=(12, 8))
    avg_emissions = df.groupby('country_name')['co2_emissions'].mean().sort_values(ascending=False).head(10)

    bars = plt.bar(range(len(avg_emissions)), avg_emissions.values,
                   color=sns.color_palette("viridis", len(avg_emissions)))
    plt.title('Average CO2 Emissions by Country (2010-2020)', fontsize=16, fontweight='bold')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Average CO2 Emissions (metric tons per capita)', fontsize=12)
    plt.xticks(range(len(avg_emissions)), avg_emissions.index, rotation=45, ha='right')

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(charts_dir / 'average_emissions_bar_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: average_emissions_bar_chart.png")

    # 3. Heatmap showing emissions by country and year
    plt.figure(figsize=(14, 10))

    # Pivot the data for heatmap
    heatmap_data = df.pivot(index='country_name', columns='year', values='co2_emissions')

    # Select top 15 countries for readability
    top_15_countries = df.groupby('country_name')['co2_emissions'].mean().nlargest(15).index
    heatmap_data = heatmap_data.loc[top_15_countries]

    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd',
                cbar_kws={'label': 'CO2 Emissions (metric tons per capita)'})
    plt.title('CO2 Emissions Heatmap by Country and Year', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.tight_layout()
    plt.savefig(charts_dir / 'emissions_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: emissions_heatmap.png")

    # 4. Box plot showing distribution of emissions
    plt.figure(figsize=(12, 8))

    # Select a subset of countries for clarity
    selected_countries = df.groupby('country_name')['co2_emissions'].mean().nlargest(8).index
    subset_df = df[df['country_name'].isin(selected_countries)]

    sns.boxplot(data=subset_df, x='country_name', y='co2_emissions', palette='Set2')
    plt.title('Distribution of CO2 Emissions by Country (2010-2020)', fontsize=16, fontweight='bold')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('CO2 Emissions (metric tons per capita)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(charts_dir / 'emissions_distribution_boxplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: emissions_distribution_boxplot.png")

    # 5. Scatter plot with trend line
    plt.figure(figsize=(12, 8))

    # Calculate global average by year
    global_avg = df.groupby('year')['co2_emissions'].mean().reset_index()

    plt.scatter(global_avg['year'], global_avg['co2_emissions'],
                s=100, alpha=0.7, color='darkblue', edgecolors='black', linewidth=1)

    # Add trend line
    z = np.polyfit(global_avg['year'], global_avg['co2_emissions'], 1)
    p = np.poly1d(z)
    plt.plot(global_avg['year'], p(global_avg['year']), "r--", alpha=0.8, linewidth=2)

    plt.title('Global Average CO2 Emissions Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Global Average CO2 Emissions (metric tons per capita)', fontsize=12)
    plt.grid(True, alpha=0.3)

    # Add trend equation
    slope, intercept = z
    equation = f'Trend: y = {slope:.3f}x + {intercept:.1f}'
    plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(charts_dir / 'global_trend_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: global_trend_scatter.png")


def main():
    """Main function to run the CO2 emissions analysis"""
    print("🌍 Starting CO2 Emissions Analysis Project")
    print("=" * 50)

    # Create charts directory
    charts_dir = create_charts_directory()
    print(f"✓ Charts directory created: {charts_dir}")

    # Fetch and load data
    df = fetch_co2_data()
    print(f"✓ Data loaded successfully: {len(df)} records")

    # Perform analysis
    avg_emissions = analyze_data(df)

    # Create visualizations
    print(f"\n📊 Creating visualizations...")
    create_visualizations(df, charts_dir)

    print(f"\n✅ Analysis complete! Check the '{charts_dir}' folder for generated charts.")
    print("\n🎯 KEY FINDINGS:")
    print(f"   • {df['country_name'].nunique()} countries analyzed")
    print(f"   • Data spans {df['year'].max() - df['year'].min() + 1} years ({df['year'].min()}-{df['year'].max()})")
    print(
        f"   • Highest average emissions: {avg_emissions.index[0]} ({avg_emissions.iloc[0]:.2f} metric tons per capita)")
    print(f"   • Global average: {df['co2_emissions'].mean():.2f} metric tons per capita")


if __name__ == "__main__":
    main()