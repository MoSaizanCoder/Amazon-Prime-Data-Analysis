# 🎬 Amazon Prime Video: Comprehensive Exploratory Data Analysis (EDA)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458.svg)
![Status](https://img.shields.io/badge/Status-Deployed-success.svg)

## 🌐 Live Dashboard
**Check out the interactive web app here:** [Click Here to View Dashboard](https://saizan-amazon-eda.streamlit.app/)

## 📊 Project Overview
This project presents a structured Exploratory Data Analysis (EDA) of the Amazon Prime Video catalog (Movies & TV Shows). The goal of this analysis is to uncover underlying trends in content production, audience preferences, and platform strategy over time. 

The analysis is transformed into a fully interactive **Streamlit Web Dashboard**, allowing technical and non-technical stakeholders to easily digest the insights through Univariate, Bivariate, and Multivariate visualizations.

## 🎯 Key Insights & Features
The dashboard is structurally divided into three analytical tiers:
1. **Univariate Analysis:** Explores the fundamental distribution of the dataset, highlighting Amazon's heavy focus on feature-length Drama and Comedy movies, alongside a massive spike in content acquisition post-2015.
2. **Bivariate Analysis:** Investigates relationships between two variables. It reveals that while movies dominate in volume, TV shows maintain a higher median IMDb score. It also identifies top-performing actors based on average content ratings.
3. **Multivariate Analysis:** Examines complex correlations. Using an interactive Plotly bubble chart and a Seaborn heatmap, it demonstrates the tight correlation between IMDb and TMDB scores, while proving that runtime has little to no impact on overall content quality.

## 🛠️ Technology Stack
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn, Plotly Express
* **Web Framework & Deployment:** Streamlit, Streamlit Community Cloud

## 💻 How to Run Locally

If you wish to run this dashboard on your local machine, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/MoSaizanCoder/Amazon-Prime-Data-Analysis.git