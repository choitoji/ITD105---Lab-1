import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Title of the app
st.title('Exploratory Data Analysis Dashboard')

# File uploader
uploaded_file = st.file_uploader("Upload CSV file here", type="csv")

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file, delimiter=';')

    # Sidebar for filtering
    st.sidebar.header('Filter Data')
    
    # Gender filter
    gender_column = 'sex'  # Replace with actual column name if different
    if gender_column in df.columns:
        gender = st.sidebar.multiselect('Select Gender:', df[gender_column].unique())
        if gender:
            df = df[df[gender_column].isin(gender)]

    # Parental Education filter
    st.sidebar.subheader('Parental Education')
    education_filter = st.sidebar.selectbox('Select Parental Education Column:', ['Medu', 'Fedu'])
    if education_filter in df.columns:
        education_values = df[education_filter].unique()
        parental_education = st.sidebar.multiselect('Select Parental Education:', education_values)
        if parental_education:
            df = df[df[education_filter].isin(parental_education)]
    else:
        st.sidebar.warning(f"'{education_filter}' column not found in the dataset.")

    st.sidebar.header('Options')

    option = st.sidebar.selectbox('Select a category:', 
                                  ['Data', 'Data Visualization', 'Outliers', 'Winsorized','Questions'])

    if option == 'Data':
        # Main section: Displaying data and summary statistics
        st.subheader('Data Preview')
        st.write(df.head())

        st.subheader('Summary Statistics')
        st.write(df.describe(include='all'))

        st.subheader('Data Info')
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.subheader('Missing Values')
        st.write(df.isnull().sum())
        df.fillna(df.select_dtypes(include=[np.number]).mean(), inplace=True)

    elif option == 'Data Visualization':
        # Layout for visualizations
        st.subheader('Data Visualizations')

        # Tabs for different types of visualizations
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Histograms", "Density Plots", "Box & Whisker Plots", "Correlation Heatmap", "Scatter Plots", "Bar Charts", "Pair Plot"])

        with tab1:
            st.header("Histograms and Density Plots")
            num_cols = df.select_dtypes(include=[np.number]).columns
            st.write("Histograms")
            for col in num_cols:
                fig, ax = plt.subplots()
                df[col].hist(ax=ax, bins=20)
                ax.set_title(f'Histogram of {col}')
                st.pyplot(fig)

        with tab2:    
            st.write("Density Plots")
            for col in num_cols:
                fig, ax = plt.subplots()
                sns.kdeplot(df[col], ax=ax, fill=True)
                ax.set_title(f'Density Plot of {col}')
                st.pyplot(fig)
            
        with tab3:
            st.header("Box and Whisker Plots")
            for col in num_cols:
                try:
                    if pd.api.types.is_numeric_dtype(df[col]) and df[col].apply(lambda x: isinstance(x, (int, float))).all():
                        fig, ax = plt.subplots()
                        sns.boxplot(x=df[col], ax=ax)
                        ax.set_title(f'Box and Whisker Plot of {col}')
                        st.pyplot(fig)
                    else:
                        st.write(f"Skipping column {col} as it doesn't contain simple numeric data.")
                except ValueError as e:
                    st.write(f"Error plotting column {col}: {e}")

        with tab4:
            st.header("Correlation and Scatter Plots")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            # Correlation Heatmap
            st.subheader('Correlation Heatmap')
            selected_cols = st.multiselect('Select columns for the correlation heatmap:', numeric_cols)
            if len(selected_cols) > 1:
                filtered_corr = df[selected_cols].corr()
                fig, ax = plt.subplots()
                sns.heatmap(filtered_corr, annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
            else:
                st.write('Select at least two columns to generate the heatmap')

        with tab5:
            # Scatter Plots
            st.subheader('Scatter Plots')
            scatter_col1 = st.selectbox('Select the X-axis column for scatter plot:', numeric_cols)
            scatter_col2 = st.selectbox('Select the Y-axis column for scatter plot:', numeric_cols)
            
            if scatter_col1 and scatter_col2:
                fig, ax = plt.subplots()
                ax.scatter(df[scatter_col1], df[scatter_col2])
                ax.set_xlabel(scatter_col1)
                ax.set_ylabel(scatter_col2)
                ax.set_title(f'Scatter Plot of {scatter_col1} vs {scatter_col2}')
                st.pyplot(fig)

        with tab6:
            # Additional Visualization
            st.subheader('Bar Charts')
            categorical_cols = df.select_dtypes(include=['object']).columns
            bar_chart_col = st.selectbox('Select categorical column for bar chart:', categorical_cols)
            
            if bar_chart_col:
                st.write(f'Bar chart for {bar_chart_col}')
                fig, ax = plt.subplots()
                df[bar_chart_col].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(f'Bar Chart of {bar_chart_col}')
                st.pyplot(fig)

        with tab7:
            # Pair Plot
            st.subheader('Pair Plot')
            pair_plot_cols = st.multiselect('Select columns for pair plot:', numeric_cols)
            if len(pair_plot_cols) > 1:
                st.write(f'Pair plot for selected columns')
                fig = sns.pairplot(df[pair_plot_cols])
                st.pyplot(fig)

    elif option == 'Outliers':
        # Outlier Detection
        st.subheader('Outlier Detection')
        z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
        outliers_zscore = (z_scores > 3).sum(axis=0)
        st.write('Number of outliers detected using Z-Score:')
        st.write(outliers_zscore)

        # Handling Outliers
        st.subheader('Handling Outliers')
        df_no_outliers = df.copy()
        df_no_outliers = df_no_outliers[~((z_scores > 3).any(axis=1))]
        st.write('Data shape before removing outliers:', df.shape)
        st.write('Data shape after removing outliers:', df_no_outliers.shape)

    elif option == 'Winsorized':
        # Transforming Data
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

        # Summary Statistics
        st.subheader('Summary Statistics (Winsorized)')
        st.write(df_winsorized.describe())

        # Data Info (Winsorized)
        st.subheader('Data Info (Winsorized)')
        buffer = io.StringIO()
        df_winsorized.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    elif option == 'Questions':
        # Analyzing the data to answer the questions
        st.subheader('Questions')
        num_cols = df.select_dtypes(include=[np.number]).columns
        
        # Question 1: Features with highest correlation with final exam scores
        st.write('### Highest Correlation with Final Exam Scores (G1, G2, G3)')
        final_exam_scores = ['G1', 'G2', 'G3']
        correlation = df[final_exam_scores + num_cols.tolist()].corr()
        final_exam_corr = correlation.loc[final_exam_scores].drop(final_exam_scores, axis=1)
        st.write(final_exam_corr)

        # Question 2: Correlation between study time and exam performance
        st.subheader('Correlation between Study Time and Exam Performance')
        if 'studytime' in df.columns:
            studytime_corr = df[['studytime'] + final_exam_scores].corr()
            st.write(studytime_corr)
            fig, ax = plt.subplots()
            sns.scatterplot(x='studytime', y='G3', data=df, ax=ax)
            ax.set_title('Scatter Plot of Study Time vs Final Exam Score (G3)')
            st.pyplot(fig)
        else:
            st.write("Study time column ('studytime') not found in the dataset.")

        # Question 3: Insights from the boxplot
        st.subheader('Insights from the Boxplot')
        if any(col in df.columns for col in final_exam_scores):
            fig, ax = plt.subplots()
            sns.boxplot(data=df[final_exam_scores], ax=ax)
            ax.set_title('Boxplot of Final Exam Scores (G1, G2, G3)')
            st.pyplot(fig)
        else:
            st.write("Final exam score columns ('G1', 'G2', 'G3') not found in the dataset.")

        # How does gender impact the final exam scores (G1, G2, G3)?
        st.write('### Impact of Gender on Final Exam Scores')
        if 'sex' in df.columns:
            gender_impact = df.groupby('sex')[final_exam_scores].mean()
            st.write(gender_impact)
        else:
            st.write("'sex' column not found in the dataset.")