import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Content Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f7f9;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .insight-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).parent
        / "netflix_content_intelligence_combined.csv"
    )

    data = pd.read_csv(file_path)

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ Dataset file not found."
    )

    st.info(
        """
        Make sure this file is uploaded to the
        same GitHub repository as app.py:

        netflix_content_intelligence_combined.csv
        """
    )

    st.stop()


except Exception as e:

    st.error(
        "❌ Unable to load the Netflix dataset."
    )

    st.exception(e)

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

df = df.copy()


# ------------------------------------------------------------
# NUMERIC COLUMNS
# ------------------------------------------------------------

numeric_columns = [
    "release_year",
    "content_age",
    "runtime_minutes",
    "imdb_rating",
    "imdb_votes",
    "tmdb_rating",
    "tmdb_popularity",
    "popularity_percentile",
    "genre_count",
    "country_count",
    "data_completeness_score",
    "match_confidence"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# DATE COLUMN
# ------------------------------------------------------------

if "date_added" in df.columns:

    df["date_added_clean"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )


# ------------------------------------------------------------
# CATEGORICAL MISSING VALUES
# ------------------------------------------------------------

categorical_columns = [
    "type",
    "rating",
    "primary_genre",
    "primary_country",
    "original_language",
    "imdb_rating_category",
    "tmdb_rating_category",
    "popularity_category",
    "release_decade",
    "release_year_group"
]


for column in categorical_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🎬 Netflix Intelligence"
)


st.sidebar.markdown(
    """
    Explore Netflix content, ratings,
    popularity, genres and global trends.
    """
)


st.sidebar.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "📌 Dashboard Navigation",
    [
        "🏠 Overview",
        "🎬 Content Analysis",
        "⭐ Ratings Analysis",
        "🔥 Popularity Analysis",
        "🌍 Genre & Country Analysis",
        "📅 Release Trends",
        "🧠 Advanced Insights",
        "📋 Data Explorer"
    ]
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🔍 Dashboard Filters"
)


# ------------------------------------------------------------
# CONTENT TYPE FILTER
# ------------------------------------------------------------

type_options = sorted(
    df["type"]
    .dropna()
    .unique()
)


selected_types = st.sidebar.multiselect(
    "Content Type",
    options=type_options,
    default=type_options
)


# ------------------------------------------------------------
# GENRE FILTER
# ------------------------------------------------------------

genre_options = sorted(
    df["primary_genre"]
    .dropna()
    .unique()
)


selected_genres = st.sidebar.multiselect(
    "Primary Genre",
    options=genre_options,
    default=genre_options
)


# ------------------------------------------------------------
# COUNTRY FILTER
# ------------------------------------------------------------

country_options = sorted(
    df["primary_country"]
    .dropna()
    .unique()
)


selected_countries = st.sidebar.multiselect(
    "Primary Country",
    options=country_options,
    default=country_options
)


# ------------------------------------------------------------
# IMDB RATING CATEGORY
# ------------------------------------------------------------

rating_category_options = sorted(
    df["imdb_rating_category"]
    .dropna()
    .unique()
)


selected_rating_categories = st.sidebar.multiselect(
    "IMDb Rating Category",
    options=rating_category_options,
    default=rating_category_options
)


# ------------------------------------------------------------
# RELEASE YEAR FILTER
# ------------------------------------------------------------

valid_years = df[
    "release_year"
].dropna()


min_year = int(
    valid_years.min()
)


max_year = int(
    valid_years.max()
)


selected_year_range = st.sidebar.slider(
    "Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (
        df["type"]
        .isin(selected_types)
    )
    &
    (
        df["primary_genre"]
        .isin(selected_genres)
    )
    &
    (
        df["primary_country"]
        .isin(selected_countries)
    )
    &
    (
        df["imdb_rating_category"]
        .isin(selected_rating_categories)
    )
    &
    (
        df["release_year"]
        >= selected_year_range[0]
    )
    &
    (
        df["release_year"]
        <= selected_year_range[1]
    )
].copy()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No records found for the selected filters."
    )

    st.stop()


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        """
        <div class="main-title">
        🎬 Netflix Content Intelligence Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="subtitle">
        Deep analysis of Netflix movies and TV shows using
        content metadata, IMDb ratings, TMDB ratings,
        popularity and global distribution.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_content = len(
        filtered_df
    )


    total_movies = int(
        (
            filtered_df["type"]
            == "Movie"
        ).sum()
    )


    total_tv_shows = int(
        (
            filtered_df["type"]
            == "TV Show"
        ).sum()
    )


    average_imdb = (
        filtered_df["imdb_rating"]
        .mean()
    )


    average_tmdb = (
        filtered_df["tmdb_rating"]
        .mean()
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "🎬 Total Content",
        f"{total_content:,}"
    )


    col2.metric(
        "🎥 Movies",
        f"{total_movies:,}"
    )


    col3.metric(
        "📺 TV Shows",
        f"{total_tv_shows:,}"
    )


    col4.metric(
        "⭐ Avg IMDb Rating",
        f"{average_imdb:.2f}"
        if pd.notna(average_imdb)
        else "N/A"
    )


    col5.metric(
        "🌟 Avg TMDB Rating",
        f"{average_tmdb:.2f}"
        if pd.notna(average_tmdb)
        else "N/A"
    )


    st.markdown("---")


    # ========================================================
    # CONTENT TYPE ANALYSIS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "🎬 Content Distribution"
        )


        content_type_data = (
            filtered_df["type"]
            .value_counts()
        )


        st.bar_chart(
            content_type_data
        )


    with col2:

        st.subheader(
            "🎭 Top Content Genres"
        )


        top_genres = (
            filtered_df[
                "primary_genre"
            ]
            .value_counts()
            .head(10)
        )


        st.bar_chart(
            top_genres
        )


    # ========================================================
    # RELEASE TREND
    # ========================================================

    st.markdown("---")


    st.subheader(
        "📅 Netflix Content Release Trend"
    )


    release_trend = (
        filtered_df
        .groupby(
            "release_year"
        )
        .size()
        .sort_index()
    )


    st.line_chart(
        release_trend
    )


    # ========================================================
    # AUTOMATIC INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">💡 Key Insights</div>',
        unsafe_allow_html=True
    )


    most_common_type = (
        filtered_df["type"]
        .mode()
    )


    if len(most_common_type) > 0:

        most_common_type = (
            most_common_type.iloc[0]
        )

    else:

        most_common_type = "N/A"


    top_genre = (
        filtered_df[
            "primary_genre"
        ]
        .mode()
    )


    if len(top_genre) > 0:

        top_genre = (
            top_genre.iloc[0]
        )

    else:

        top_genre = "N/A"


    top_country = (
        filtered_df[
            "primary_country"
        ]
        .mode()
    )


    if len(top_country) > 0:

        top_country = (
            top_country.iloc[0]
        )

    else:

        top_country = "N/A"


    st.markdown(
        f"""
        <div class="insight-card">

        🎬 <b>Dominant Content Type:</b><br>
        {most_common_type} is the most common content
        type in the selected Netflix dataset.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="insight-card">

        🎭 <b>Most Common Genre:</b><br>
        {top_genre} is the most represented
        primary genre.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="insight-card">

        🌍 <b>Leading Content Country:</b><br>
        {top_country} contributes the highest number
        of selected Netflix titles.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CONTENT ANALYSIS
# ============================================================

elif page == "🎬 Content Analysis":

    st.title(
        "🎬 Netflix Content Analysis"
    )


    # ========================================================
    # CONTENT TYPE
    # ========================================================

    st.subheader(
        "📊 Movies vs TV Shows"
    )


    type_counts = (
        filtered_df[
            "type"
        ]
        .value_counts()
    )


    st.bar_chart(
        type_counts
    )


    # ========================================================
    # CONTENT RATING
    # ========================================================

    st.subheader(
        "🔞 Content Rating Distribution"
    )


    rating_counts = (
        filtered_df[
            "rating"
        ]
        .value_counts()
        .head(15)
    )


    st.bar_chart(
        rating_counts
    )


    # ========================================================
    # RUNTIME
    # ========================================================

    st.subheader(
        "⏱️ Average Runtime by Content Type"
    )


    runtime_by_type = (
        filtered_df
        .groupby("type")[
            "runtime_minutes"
        ]
        .mean()
    )


    st.bar_chart(
        runtime_by_type
    )


    # ========================================================
    # CONTENT AGE
    # ========================================================

    st.subheader(
        "📆 Average Content Age"
    )


    age_by_type = (
        filtered_df
        .groupby("type")[
            "content_age"
        ]
        .mean()
    )


    st.bar_chart(
        age_by_type
    )


    # ========================================================
    # RECENT RELEASES
    # ========================================================

    recent_count = int(
        filtered_df[
            "is_recent_release"
        ].sum()
    )


    original_count = int(
        filtered_df[
            "is_original"
        ].sum()
    )


    col1, col2 = st.columns(2)


    col1.metric(
        "🆕 Recent Releases",
        f"{recent_count:,}"
    )


    col2.metric(
        "🎬 Netflix Originals",
        f"{original_count:,}"
    )


# ============================================================
# RATINGS ANALYSIS
# ============================================================

elif page == "⭐ Ratings Analysis":

    st.title(
        "⭐ IMDb & TMDB Ratings Analysis"
    )


    # ========================================================
    # RATING KPIs
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "IMDb Average",
        f"{filtered_df['imdb_rating'].mean():.2f}"
    )


    col2.metric(
        "IMDb Maximum",
        f"{filtered_df['imdb_rating'].max():.2f}"
    )


    col3.metric(
        "TMDB Average",
        f"{filtered_df['tmdb_rating'].mean():.2f}"
    )


    col4.metric(
        "TMDB Maximum",
        f"{filtered_df['tmdb_rating'].max():.2f}"
    )


    st.markdown("---")


    # ========================================================
    # IMDB RATING CATEGORY
    # ========================================================

    st.subheader(
        "⭐ IMDb Rating Categories"
    )


    imdb_category = (
        filtered_df[
            "imdb_rating_category"
        ]
        .value_counts()
    )


    st.bar_chart(
        imdb_category
    )


    # ========================================================
    # TMDB RATING CATEGORY
    # ========================================================

    st.subheader(
        "🌟 TMDB Rating Categories"
    )


    tmdb_category = (
        filtered_df[
            "tmdb_rating_category"
        ]
        .value_counts()
    )


    st.bar_chart(
        tmdb_category
    )


    # ========================================================
    # GENRE VS IMDB RATING
    # ========================================================

    st.subheader(
        "🎭 Average IMDb Rating by Genre"
    )


    genre_imdb = (
        filtered_df
        .groupby(
            "primary_genre"
        )[
            "imdb_rating"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )


    st.bar_chart(
        genre_imdb
    )


    # ========================================================
    # COUNTRY VS IMDB RATING
    # ========================================================

    st.subheader(
        "🌍 Average IMDb Rating by Country"
    )


    country_imdb = (
        filtered_df
        .groupby(
            "primary_country"
        )[
            "imdb_rating"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )


    st.bar_chart(
        country_imdb
    )


    # ========================================================
    # TOP RATED CONTENT
    # ========================================================

    st.subheader(
        "🏆 Top Rated Netflix Content"
    )


    top_rated = (
        filtered_df[
            [
                "title",
                "type",
                "release_year",
                "primary_genre",
                "primary_country",
                "imdb_rating",
                "tmdb_rating",
                "imdb_votes"
            ]
        ]
        .sort_values(
            "imdb_rating",
            ascending=False
        )
        .head(20)
    )


    st.dataframe(
        top_rated,
        use_container_width=True
    )


# ============================================================
# POPULARITY ANALYSIS
# ============================================================

elif page == "🔥 Popularity Analysis":

    st.title(
        "🔥 Netflix Popularity Analysis"
    )


    # ========================================================
    # POPULARITY CATEGORY
    # ========================================================

    st.subheader(
        "🔥 Content Popularity Categories"
    )


    popularity_data = (
        filtered_df[
            "popularity_category"
        ]
        .value_counts()
    )


    st.bar_chart(
        popularity_data
    )


    # ========================================================
    # GENRE POPULARITY
    # ========================================================

    st.subheader(
        "🎭 Average TMDB Popularity by Genre"
    )


    genre_popularity = (
        filtered_df
        .groupby(
            "primary_genre"
        )[
            "tmdb_popularity"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )


    st.bar_chart(
        genre_popularity
    )


    # ========================================================
    # COUNTRY POPULARITY
    # ========================================================

    st.subheader(
        "🌍 Average Popularity by Country"
    )


    country_popularity = (
        filtered_df
        .groupby(
            "primary_country"
        )[
            "tmdb_popularity"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )


    st.bar_chart(
        country_popularity
    )


    # ========================================================
    # TOP POPULAR CONTENT
    # ========================================================

    st.subheader(
        "🚀 Most Popular Content"
    )


    top_popular = (
        filtered_df[
            [
                "title",
                "type",
                "release_year",
                "primary_genre",
                "tmdb_popularity",
                "popularity_percentile",
                "tmdb_rating"
            ]
        ]
        .sort_values(
            "tmdb_popularity",
            ascending=False
        )
        .head(20)
    )


    st.dataframe(
        top_popular,
        use_container_width=True
    )


# ============================================================
# GENRE AND COUNTRY ANALYSIS
# ============================================================

elif page == "🌍 Genre & Country Analysis":

    st.title(
        "🌍 Genre & Global Content Analysis"
    )


    # ========================================================
    # TOP GENRES
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "🎭 Top 15 Genres"
        )


        genre_counts = (
            filtered_df[
                "primary_genre"
            ]
            .value_counts()
            .head(15)
        )


        st.bar_chart(
            genre_counts
        )


    with col2:

        st.subheader(
            "🌍 Top 15 Countries"
        )


        country_counts = (
            filtered_df[
                "primary_country"
            ]
            .value_counts()
            .head(15)
        )


        st.bar_chart(
            country_counts
        )


    st.markdown("---")


    # ========================================================
    # GENRE RATINGS
    # ========================================================

    st.subheader(
        "⭐ Genre Performance Based on IMDb Rating"
    )


    genre_performance = (
        filtered_df
        .groupby(
            "primary_genre"
        )
        .agg(
            Content_Count=(
                "content_id",
                "count"
            ),
            Average_IMDb_Rating=(
                "imdb_rating",
                "mean"
            ),
            Average_TMDB_Rating=(
                "tmdb_rating",
                "mean"
            ),
            Average_Popularity=(
                "tmdb_popularity",
                "mean"
            )
        )
        .sort_values(
            "Content_Count",
            ascending=False
        )
        .head(15)
    )


    st.dataframe(
        genre_performance.round(2),
        use_container_width=True
    )


    # ========================================================
    # LANGUAGE ANALYSIS
    # ========================================================

    st.subheader(
        "🗣️ Most Common Original Languages"
    )


    language_counts = (
        filtered_df[
            "original_language"
        ]
        .value_counts()
        .head(15)
    )


    st.bar_chart(
        language_counts
    )


# ============================================================
# RELEASE TRENDS
# ============================================================

elif page == "📅 Release Trends":

    st.title(
        "📅 Netflix Release Trends"
    )


    # ========================================================
    # YEARLY CONTENT TREND
    # ========================================================

    st.subheader(
        "📈 Content Released by Year"
    )


    yearly_content = (
        filtered_df
        .groupby(
            "release_year"
        )
        .size()
        .sort_index()
    )


    st.line_chart(
        yearly_content
    )


    # ========================================================
    # MOVIE VS TV SHOW TREND
    # ========================================================

    st.subheader(
        "🎬 Movies vs TV Shows Release Trend"
    )


    content_trend = (
        filtered_df
        .groupby(
            [
                "release_year",
                "type"
            ]
        )
        .size()
        .unstack(
            fill_value=0
        )
        .sort_index()
    )


    st.line_chart(
        content_trend
    )


    # ========================================================
    # DECADE ANALYSIS
    # ========================================================

    st.subheader(
        "🕰️ Content Distribution by Decade"
    )


    decade_data = (
        filtered_df[
            "release_decade"
        ]
        .value_counts()
        .sort_index()
    )


    st.bar_chart(
        decade_data
    )


    # ========================================================
    # AVERAGE RATING BY YEAR
    # ========================================================

    st.subheader(
        "⭐ Average IMDb Rating Trend"
    )


    yearly_rating = (
        filtered_df
        .groupby(
            "release_year"
        )[
            "imdb_rating"
        ]
        .mean()
        .sort_index()
    )


    st.line_chart(
        yearly_rating
    )


# ============================================================
# ADVANCED INSIGHTS
# ============================================================

elif page == "🧠 Advanced Insights":

    st.title(
        "🧠 Advanced Netflix Intelligence"
    )


    # ========================================================
    # NETFLIX ORIGINAL ANALYSIS
    # ========================================================

    st.subheader(
        "🎬 Netflix Originals vs Non-Original Content"
    )


    original_analysis = (
        filtered_df
        .groupby(
            "is_original"
        )
        .agg(
            Content_Count=(
                "content_id",
                "count"
            ),
            Average_IMDb=(
                "imdb_rating",
                "mean"
            ),
            Average_TMDB=(
                "tmdb_rating",
                "mean"
            ),
            Average_Popularity=(
                "tmdb_popularity",
                "mean"
            )
        )
    )


    st.dataframe(
        original_analysis.round(2),
        use_container_width=True
    )


    # ========================================================
    # DATA COMPLETENESS
    # ========================================================

    st.subheader(
        "📊 Data Completeness Analysis"
    )


    completeness = (
        filtered_df[
            "data_completeness_score"
        ]
        .round(1)
        .value_counts()
        .sort_index()
    )


    st.bar_chart(
        completeness
    )


    # ========================================================
    # MATCH CONFIDENCE
    # ========================================================

    st.subheader(
        "🎯 Content Matching Confidence"
    )


    confidence_data = (
        filtered_df[
            "match_confidence"
        ]
        .round(1)
        .value_counts()
        .sort_index()
    )


    st.bar_chart(
        confidence_data
    )


    # ========================================================
    # CORRELATION
    # ========================================================

    st.subheader(
        "🔗 Numerical Feature Correlation"
    )


    correlation_columns = [
        "release_year",
        "content_age",
        "runtime_minutes",
        "imdb_rating",
        "imdb_votes",
        "tmdb_rating",
        "tmdb_popularity",
        "popularity_percentile",
        "genre_count",
        "country_count",
        "data_completeness_score",
        "match_confidence"
    ]


    available_columns = [
        column
        for column in correlation_columns
        if column in filtered_df.columns
    ]


    correlation = (
        filtered_df[
            available_columns
        ]
        .corr()
        .round(2)
    )


    st.dataframe(
        correlation,
        use_container_width=True
    )


    # ========================================================
    # AUTOMATIC DATA INSIGHTS
    # ========================================================

    st.markdown("---")


    st.markdown(
        '<div class="section-title">💡 Smart Data Insights</div>',
        unsafe_allow_html=True
    )


    best_genre = (
        filtered_df
        .groupby(
            "primary_genre"
        )[
            "imdb_rating"
        ]
        .mean()
    )


    best_genre = (
        best_genre
        .dropna()
    )


    if not best_genre.empty:

        best_genre_name = (
            best_genre.idxmax()
        )

        best_genre_rating = (
            best_genre.max()
        )

    else:

        best_genre_name = "N/A"
        best_genre_rating = np.nan


    most_popular_genre = (
        filtered_df
        .groupby(
            "primary_genre"
        )[
            "tmdb_popularity"
        ]
        .mean()
        .dropna()
    )


    if not most_popular_genre.empty:

        popular_genre_name = (
            most_popular_genre.idxmax()
        )

    else:

        popular_genre_name = "N/A"


    most_common_country = (
        filtered_df[
            "primary_country"
        ]
        .mode()
    )


    if len(most_common_country) > 0:

        most_common_country = (
            most_common_country.iloc[0]
        )

    else:

        most_common_country = "N/A"


    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"""
            🏆 **Best Rated Genre**

            {best_genre_name}

            Average IMDb Rating:

            {best_genre_rating:.2f}
            """
        )


        st.info(
            f"""
            🔥 **Most Popular Genre**

            {popular_genre_name}

            has the highest average TMDB popularity.
            """
        )


    with col2:

        st.warning(
            f"""
            🌍 **Largest Content Contributor**

            {most_common_country}

            contributes the highest number of
            selected Netflix titles.
            """
        )


        original_percentage = (
            filtered_df[
                "is_original"
            ]
            .mean()
            * 100
        )


        st.info(
            f"""
            🎬 **Netflix Originals**

            {original_percentage:.2f}%

            of the selected content is marked
            as Netflix Original.
            """
        )


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "📋 Data Explorer":

    st.title(
        "📋 Netflix Dataset Explorer"
    )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.subheader(
        "🔎 Dataset Preview"
    )


    rows_to_show = st.slider(
        "Select number of rows",
        min_value=10,
        max_value=min(
            500,
            len(filtered_df)
        ),
        value=min(
            100,
            len(filtered_df)
        ),
        step=10
    )


    st.dataframe(
        filtered_df
        .head(rows_to_show),
        use_container_width=True
    )


    # ========================================================
    # DATASET METRICS
    # ========================================================

    st.subheader(
        "📊 Dataset Information"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Rows",
        f"{len(filtered_df):,}"
    )


    col2.metric(
        "Columns",
        filtered_df.shape[1]
    )


    missing_values = int(
        filtered_df
        .isnull()
        .sum()
        .sum()
    )


    col3.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


    memory_usage = (
        filtered_df
        .memory_usage(
            deep=True
        )
        .sum()
        / 1024 ** 2
    )


    col4.metric(
        "Memory Usage",
        f"{memory_usage:.2f} MB"
    )


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    st.subheader(
        "🧾 Column Information"
    )


    column_info = pd.DataFrame(
        {
            "Column": filtered_df.columns,
            "Data Type": (
                filtered_df
                .dtypes
                .astype(str)
                .values
            ),
            "Missing Values": (
                filtered_df
                .isnull()
                .sum()
                .values
            ),
            "Unique Values": (
                filtered_df
                .nunique()
                .values
            )
        }
    )


    st.dataframe(
        column_info,
        use_container_width=True
    )


    # ========================================================
    # STATISTICAL SUMMARY
    # ========================================================

    st.subheader(
        "📈 Statistical Summary"
    )


    st.dataframe(
        filtered_df
        .describe(
            include="all"
        ),
        use_container_width=True
    )


    # ========================================================
    # DOWNLOAD FILTERED DATA
    # ========================================================

    st.subheader(
        "📥 Download Filtered Dataset"
    )


    csv_data = (
        filtered_df
        .to_csv(
            index=False
        )
        .encode(
            "utf-8"
        )
    )


    st.download_button(
        label="⬇️ Download Filtered Netflix Data",
        data=csv_data,
        file_name="filtered_netflix_content.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(
    """
    <div style="text-align:center; color:#666666; padding:10px;">
        🎬 <b>Netflix Content Intelligence Dashboard</b><br>
        Built with Python • Streamlit • Pandas • NumPy
    </div>
    """,
    unsafe_allow_html=True
)
