# INF601 - Advanced Programming in Python
## Brian Shoemaker
## Mini Project 2 - Global CO2 Emissions Analysis

### 📋 Project Description

This project analyzes global CO2 emissions data to answer the research question: **"What are the trends in global CO2 emissions by country over time?"**

The project fetches real-time data from the World Bank API (or uses sample data as fallback) to examine CO2 emissions patterns across different countries from 2010-2020. It creates comprehensive visualizations to help understand emission trends, country comparisons, and global patterns.

### 🎯 Research Question

**"What are the trends in global CO2 emissions by country over time?"**

This analysis helps us understand:
- Which countries have the highest CO2 emissions per capita
- How emissions have changed over the past decade
- Global trends in carbon emissions
- Distribution patterns across different nations

### 📊 Data Source

- **Primary**: World Bank API (EN.ATM.CO2E.PC indicator)
- **Fallback**: Generated sample data using realistic patterns
- **Time Period**: 2010-2020
- **Metric**: CO2 emissions (metric tons per capita)

### 🔧 Installation Instructions

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Step 1: Clone the Repository
```bash
git clone <your-github-repository-url>
cd <repository-name>
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### 🚀 How to Execute the Program

1. **Ensure you're in the project directory** and your virtual environment is activated (if using one)

2. **Run the main program**:
   ```bash
   python main.py
   ```

3. **Program Execution Flow**:
   - The program will create a `charts` folder automatically
   - It attempts to fetch real data from the World Bank API
   - If the API is unavailable, it generates realistic sample data
   - Performs data analysis and displays key statistics
   - Creates 5 different visualizations saved as PNG files

4. **Expected Output**:
   - Console output showing analysis results
   - 5 PNG chart files saved in the `charts/` directory

### 📈 Generated Visualizations

The program creates five different charts:

1. **`co2_trends_line_plot.png`** - Line chart showing emission trends over time for top 8 countries
2. **`average_emissions_bar_chart.png`** - Bar chart of average emissions by country
3. **`emissions_heatmap.png`** - Heatmap showing emissions by country and year
4. **`emissions_distribution_boxplot.png`** - Box plot showing distribution patterns
5. **`global_trend_scatter.png`** - Scatter plot with global trend line

### 📁 Project Structure

```
project-root/
│
├── main.py                 # Main program file
├── requirements.txt        # Python package dependencies
├── README.md              # This file
├── .gitignore            # Git ignore file (excludes charts folder)
└── charts/               # Generated charts folder (created at runtime)
    ├── co2_trends_line_plot.png
    ├── average_emissions_bar_chart.png
    ├── emissions_heatmap.png
    ├── emissions_distribution_boxplot.png
    └── global_trend_scatter.png
```

### 🔍 Key Features

- **Data Fetching**: Retrieves real-time data from World Bank API
- **Error Handling**: Graceful fallback to sample data if API fails
- **Data Analysis**: Comprehensive statistical analysis using Pandas
- **Visualizations**: Five different chart types using Matplotlib and Seaborn
- **Professional Output**: High-quality PNG exports (300 DPI)
- **Clean Code**: Well-documented, modular functions

### 📋 Requirements Fulfilled

- ✅ Initial comments with name, class, and project
- ✅ Proper import of required packages
- ✅ Data retrieval from external API (World Bank)
- ✅ Pandas DataFrame for data storage and manipulation
- ✅ Multiple matplotlib/seaborn visualizations
- ✅ Automatic chart saving to `charts/` folder
- ✅ Comprehensive README with installation and execution instructions
- ✅ requirements.txt file with all dependencies

### 🛠️ Dependencies

- **pandas**: Data manipulation and analysis
- **matplotlib**: Creating static visualizations
- **seaborn**: Statistical data visualization
- **requests**: HTTP library for API calls
- **numpy**: Numerical computing support
- **pathlib**: File system path handling


**Author**: Brian Shoemaker  
**Course**: INF601 - Advanced Programming in Python  
**Project**: Mini Project 2  
**Date**: 09/19/2025