import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Title of the app
st.title('Exploratory Data Analysis with Streamlit')

# File uploader
uploaded_file = st.file_uploader("Upload CSV file here", type="csv")

if uploaded_file is not None:
    # 1. Load the data
    df = pd.read_csv(uploaded_file, delimiter=';')

    # 2. Basic Data Exploration - Check the first few rows of the dataset 
    # to get an initial sense of the data's structure.
    st.subheader('Data Preview')
    st.write(df.head())

    # 3. Data Summary - Generate descriptive statistics for the data, including mean, median, 
    # standard deviation, and quartiles, to understand the central tendency and spread of the data.
    st.subheader('Summary Statistics')
    st.write(df.describe())

    #4. Data Information - check the data types of each column, 
    # the number of non-null values, and memory usage.
    st.subheader('Data Info')
    buffer = io.StringIO()
    df.info(buf=buffer) #writes the DataFrame's information to the buffer.
    s = buffer.getvalue()
    st.text(s) #displays the string content in Streamlit.

    # 5. Handling Missing Data - identify and handle missing values using techniques 
    # like imputation or removal.
    st.subheader('Missing Values')
    st.write(df.isnull().sum())
    df = df.fillna(df.mean())

    # 6. Data Visualization - Create visualizations to explore data distributions, relationships, and patterns.
    # Plot histograms for each numerical feature
    st.subheader('Histograms')
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax, bins=20)
        ax.set_title(f'Histogram of {col}')
        st.pyplot(fig)

    # Plot density plots
    st.subheader('Density Plots')
    for col in num_cols:
        fig, ax = plt.subplots()
        sns.kdeplot(df[col], ax=ax, fill=True)
        ax.set_title(f'Density Plot of {col}')
        st.pyplot(fig)

  

    # Assuming df is your DataFrame
    num_cols = df.select_dtypes(include=['number']).columns  # Only numeric columns

    st.subheader('Box and Whisker Plots')

    for col in num_cols:
        try:
            # Ensure that the column is numeric and doesn't contain lists/arrays
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].apply(lambda x: isinstance(x, (int, float))).all():
                fig, ax = plt.subplots()
                sns.boxplot(x=df[col], ax=ax)
                ax.set_title(f'Box and Whisker Plot of {col}')
                st.pyplot(fig)
            else:
                st.write(f"Skipping column {col} as it doesn't contain simple numeric data.")
        except ValueError as e:
            st.write(f"Error plotting column {col}: {e}")


    # Plot correlations heatmap
    st.subheader('Correlation Heatmap')
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)


    # Scatter Plot
    st.subheader('Scatter Plots')
    num_cols = df.select_dtypes(include=[np.number]).columns

    # Create scatter plots for all pairs of numerical features
    for i, col1 in enumerate(num_cols):
        for col2 in num_cols[i+1:]:
            fig, ax = plt.subplots()
            ax.scatter(df[col1], df[col2])
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.set_title(f'Scatter Plot of {col1} vs {col2}')
            st.pyplot(fig)


    # 7. Identifying and Handling Outliers
    st.subheader('Outlier Detection')

    # Z-Score method
    st.subheader('Outlier Detection using Z-Score')
    z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
    outliers_zscore = (z_scores > 3).sum(axis=0)
    st.write('Number of outliers detected using Z-Score:')
    st.write(outliers_zscore)

    
    # Handling Outliers
    st.subheader('Handling Outliers')

    # Remove outliers
    st.write('Removing Outliers...')
    df_no_outliers = df.copy()
    df_no_outliers = df_no_outliers[~((z_scores > 3).any(axis=1))]

    st.write('Data shape before removing outliers:', df.shape)
    st.write('Data shape after removing outliers:', df_no_outliers.shape)

    # Transforming Data (example: log transformation)
    st.write('Applying log transformation...')
    df_transformed = df.copy()
    num_cols = df_transformed.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df_transformed[col] = np.log1p(df_transformed[col])
    st.write('Data after log transformation:')
    st.write(df_transformed.head())

    # Winsorizing
    st.write('Winsorizing...')
    from scipy.stats.mstats import winsorize
    df_winsorized = df.copy()
    for col in num_cols:
        df_winsorized[col] = winsorize(df_winsorized[col], limits=[0.05, 0.05])
    st.write('Data after winsorizing:')
    st.write(df_winsorized.head())



    # 3. Data Summary - Generate descriptive statistics for the data, including mean, median, 
    # standard deviation, and quartiles, to understand the central tendency and spread of the data.
    st.subheader('Summary Statistics')
    st.write(df_winsorized.describe())

    #4. Data Information - check the data types of each column, 
    # the number of non-null values, and memory usage.
    st.subheader('Data Info')
    buffer = io.StringIO()
    df_winsorized.info(buf=buffer) #writes the DataFrame's information to the buffer.
    s = buffer.getvalue()
    st.text(s) #displays the string content in Streamlit.
