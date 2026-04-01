import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ast
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Amazon Prime EDA", page_icon="🎬", layout="wide")
st.title("🎬 Amazon Prime Video: Comprehensive EDA")
st.markdown("A structured Exploratory Data Analysis divided into Univariate, Bivariate, and Multivariate insights.")

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def clean_list_column(row):
    if not isinstance(row, str):
        return ['Unknown']
    try:
        result_list = ast.literal_eval(row)
        if len(result_list) == 0:
            return ['Unknown']
        return result_list
    except:
        return ['Unknown']

def format_axes(ax, xlabel, ylabel):
    """Helper to capitalize and bold x and y labels for matplotlib/seaborn charts"""
    ax.set_xlabel(xlabel.upper(), fontweight='bold')
    ax.set_ylabel(ylabel.upper(), fontweight='bold')

# ==========================================
# DATA LOADING & CLEANING
# ==========================================
@st.cache_data
def load_and_clean_data():
    titles = pd.read_csv('titles.csv')
    credits = pd.read_csv('credits.csv')

    titles.drop_duplicates(inplace=True)
    credits.drop_duplicates(inplace=True)
    credits.drop('character', axis=1, inplace=True, errors='ignore')

    titles['seasons'] = titles['seasons'].fillna(0)
    titles['imdb_score'] = titles['imdb_score'].fillna(0)
    titles['imdb_votes'] = titles['imdb_votes'].fillna(0)
    titles['tmdb_score'] = titles['tmdb_score'].fillna(0)
    titles['tmdb_popularity'] = titles['tmdb_popularity'].fillna(0)
    titles['age_certification'] = titles['age_certification'].fillna('Not Rated')
    titles['description'] = titles['description'].fillna('No Description')

    titles['genres'] = titles['genres'].apply(clean_list_column)
    titles['production_countries'] = titles['production_countries'].apply(clean_list_column)

    return titles, credits

with st.spinner('Loading and Processing Data...'):
    Amazon_titles, Amazon_credits = load_and_clean_data()
    df_merged = pd.merge(Amazon_titles, Amazon_credits, on='id', how='inner')

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📈 1. Univariate Analysis", "📊 2. Bivariate Analysis", "🕸️ 3. Multivariate Analysis"])

# ==========================================
# TAB 1: UNIVARIATE ANALYSIS
# ==========================================
with tab1:
    st.header("📈 Univariate Analysis")
    st.markdown("Understanding the distribution of single variables across the dataset.")
    
    # ROW 1
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.subheader("1. Content Type Distribution")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.countplot(x='type', data=Amazon_titles, palette='viridis', ax=ax1)
        for container in ax1.containers:
            ax1.bar_label(container, padding=3)
        format_axes(ax1, 'Content Type', 'Count')
        st.pyplot(fig1)
        st.info("**What it represents:** The total volume of Movies versus TV Shows available on the platform.\n\n**Key Finding:** Movies significantly outnumber TV shows, indicating Amazon's focus on feature-length content.")

    with r1_col2:
        st.subheader("2. Age Certification Breakdown")
        rated_content = Amazon_titles[Amazon_titles['age_certification'] != 'Not Rated']
        rating_counts = rated_content['age_certification'].value_counts().head(5)
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        st.pyplot(fig2)
        st.info("**What it represents:** The top 5 most common age ratings across all categorized content.\n\n**Key Finding:** Mature and R-rated content dominates the catalog, targeting adult demographics.")

    st.divider()

    # ROW 2
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.subheader("3. Top 10 Genres")
        df_genres = Amazon_titles.explode('genres')
        top_genres = df_genres['genres'].value_counts().head(10)
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=top_genres.values, y=top_genres.index, palette='mako', ax=ax3)
        for container in ax3.containers:
            ax3.bar_label(container, padding=3)
        format_axes(ax3, 'Count', 'Genre')
        st.pyplot(fig3)
        st.info("**What it represents:** The most frequently occurring genres in the dataset.\n\n**Key Finding:** Drama and Comedy are the undisputed leaders in content production.")

    with r2_col2:
        st.subheader("4. Volume of Content by Release Year (>2000)")
        recent_content = Amazon_titles[Amazon_titles['release_year'] >= 2000]
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.histplot(data=recent_content, x='release_year', kde=True, color='teal', bins=23, ax=ax4)
        format_axes(ax4, 'Release Year', 'Content Added')
        st.pyplot(fig4)
        st.info("**What it represents:** The timeline of content releases over the last two decades.\n\n**Key Finding:** A massive spike in content acquisition and production happened post-2015, aligning with the streaming wars.")


# ==========================================
# TAB 2: BIVARIATE ANALYSIS
# ==========================================
with tab2:
    st.header("📊 Bivariate Analysis")
    st.markdown("Exploring the relationship between two different variables.")

    # ROW 1
    r3_col1, r3_col2 = st.columns(2)
    with r3_col1:
        st.subheader("1. IMDb Score Spread: Movies vs Shows")
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=Amazon_titles[Amazon_titles['imdb_score']>0], x='type', y='imdb_score', palette='Set2', ax=ax5)
        format_axes(ax5, 'Content Type', 'IMDb Score')
        st.pyplot(fig5)
        st.info("**What it represents:** The distribution and outliers of IMDb ratings split by content type.\n\n**Key Finding:** TV Shows generally maintain a higher median IMDb score compared to movies.")

    with r3_col2:
        st.subheader("2. Runtime Distribution by Type")
        df_filtered = Amazon_titles[(Amazon_titles['runtime'] > 0) & (Amazon_titles['runtime'] < 200)]
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df_filtered, x='runtime', hue='type', kde=True, bins=30, palette='viridis', element='step', ax=ax6)
        format_axes(ax6, 'Runtime (Minutes)', 'Frequency')
        st.pyplot(fig6)
        st.info("**What it represents:** How long content typically lasts, comparing movies to TV episodes.\n\n**Key Finding:** Movies cluster around the 90-120 minute mark, while TV shows cluster around 30-50 minutes.")

    st.divider()

    # ROW 2
    r4_col1, r4_col2 = st.columns(2)
    with r4_col1:
        st.subheader("3. Top 'Bankable' Actors (Min 5 Titles)")
        actor_stats = df_merged[df_merged['role'] == 'ACTOR']
        actor_metrics = actor_stats.groupby('name')['imdb_score'].agg(['mean', 'count'])
        top_quality_actors = actor_metrics[actor_metrics['count'] >= 5].sort_values(by='mean', ascending=False).head(10)
        fig7, ax7 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=top_quality_actors['mean'], y=top_quality_actors.index, palette='plasma', ax=ax7)
        ax7.set_xlim(6.5, 9.5)
        format_axes(ax7, 'Average IMDb Score', 'Actor Name')
        st.pyplot(fig7)
        st.info("**What it represents:** Actors who consistently appear in highly-rated content.\n\n**Key Finding:** Voice actors and documentary narrators tend to dominate the highest average rating brackets.")

    with r4_col2:
        st.subheader("4. Impact of Age Rating on Quality")
        target_ratings = ['G', 'PG', 'PG-13', 'R', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA']
        df_age_quality = Amazon_titles[(Amazon_titles['age_certification'].isin(target_ratings)) & (Amazon_titles['imdb_score']>0)]
        fig8, ax8 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df_age_quality, x='age_certification', y='imdb_score', order=target_ratings, palette='coolwarm', ax=ax8)
        format_axes(ax8, 'Age Certification', 'IMDb Score')
        st.pyplot(fig8)
        st.info("**What it represents:** Whether restricted or family-friendly content receives better ratings.\n\n**Key Finding:** TV-MA and TV-14 content show tighter distributions at higher scores compared to general audience ratings.")


# ==========================================
# TAB 3: MULTIVARIATE ANALYSIS
# ==========================================
with tab3:
    st.header("🕸️ Multivariate Analysis")
    st.markdown("Complex relationships involving three or more variables simultaneously.")

    # ROW 1
    r5_col1, r5_col2 = st.columns(2)
    with r5_col1:
        st.subheader("1. IMDb vs TMDB Scores by Type")
        df_bubble = Amazon_titles[(Amazon_titles['imdb_score'] > 0) & (Amazon_titles['tmdb_score'] > 0) & (Amazon_titles['imdb_votes'] > 0)]
        fig_bubble = px.scatter(
            df_bubble, x='imdb_score', y='tmdb_score', size='imdb_votes',
            color='type', hover_name='title', size_max=40, opacity=0.6, template='plotly_white'
        )
        fig_bubble.add_shape(type="line", x0=0, y0=0, x1=10, y1=10, line=dict(color="Red", width=2, dash="dash"))
        fig_bubble.update_layout(
            xaxis_title="<b>IMDB SCORE</b>", yaxis_title="<b>TMDB SCORE</b>",
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        st.info("**What it represents:** Correlation between IMDb and TMDB scores, sized by total votes and colored by type.\n\n**Key Finding:** Scores correlate closely (following the red trendline), but movies gather significantly more extreme vote counts.")

    with r5_col2:
        st.subheader("2. Correlation Heatmap")
        numeric_df = Amazon_titles.select_dtypes(include=['float64', 'int64'])
        # Drop ID or year if they skew the heatmap unnecessarily, but keeping standard for now
        corr_matrix = numeric_df[['release_year', 'runtime', 'imdb_score', 'imdb_votes', 'tmdb_popularity', 'tmdb_score']].corr()
        fig10, ax10 = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax10)
        format_axes(ax10, 'Features', 'Features')
        st.pyplot(fig10)
        st.info("**What it represents:** Linear relationships between all numerical variables in the dataset.\n\n**Key Finding:** IMDb scores and TMDB scores have the strongest positive correlation, while runtime shows little to no impact on overall scores.")

    st.divider()

    # ROW 2
    r6_col1, r6_col2 = st.columns(2)
    with r6_col1:
        st.subheader("3. Trend of Avg IMDb Scores (2000-Present)")
        df_trend = Amazon_titles[Amazon_titles['release_year'] >= 2000].groupby(['release_year', 'type'])['imdb_score'].mean().reset_index()
        fig11, ax11 = plt.subplots(figsize=(8, 5))
        sns.lineplot(data=df_trend, x='release_year', y='imdb_score', hue='type', palette='tab10', marker='o', ax=ax11)
        ax11.axhline(y=6.0, color='gray', linestyle='--', label='Baseline')
        format_axes(ax11, 'Release Year', 'Average IMDb Score')
        st.pyplot(fig11)
        st.info("**What it represents:** How the average quality of released content has shifted year over year.\n\n**Key Finding:** While TV show quality has remained relatively stable, average movie scores have seen a slight decline as volume increased.")

    with r6_col2:
        st.subheader("4. Popularity by Age Rating and Type")
        target_ratings = ['PG-13', 'R', 'TV-14', 'TV-MA']
        df_pop = Amazon_titles[Amazon_titles['age_certification'].isin(target_ratings)]
        fig12, ax12 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_pop, x='age_certification', y='tmdb_popularity', hue='type', palette='Set1', errorbar=None, ax=ax12)
        format_axes(ax12, 'Age Certification', 'Average TMDB Popularity')
        st.pyplot(fig12)
        st.info("**What it represents:** The average TMDB popularity metrics across major age demographics, split by content type.\n\n**Key Finding:** TV-MA TV shows generate vastly higher popularity and engagement compared to equivalently rated Movies.")