# Todo list for exploration
For each dataset, do the following to explore for better decision making in next phases:
 
  ### 1. Initial Data Understanding & Loading
  - **Load Dataset**: Read the raw data into a pandas DataFrame.
  - **Basic Information**:
    - Check `df.shape` for dimensions.
    - View `df.head()` and `df.tail()` for a glimpse of the data.
    - Use `df.info()` to understand data types and non-null counts.
    - Use `df.dtypes` to specifically check column data types.
  - **Descriptive Statistics**:
    - Use `df.describe(include='all')` for a statistical summary of all columns (numerical and categorical).

  ### 2. Data Cleaning and Preprocessing (Preliminary)
  - **Identify and Handle Missing Values**:
    - Calculate `df.isnull().sum()` to count missing values per column.
    - Calculate percentage of missing values: `(df.isnull().sum() / len(df)) * 100`.
    - Visualize missing values (e.g., `sns.heatmap(df.isnull())`).
    - Strategize for imputation (mean, median, mode, model-based) or removal, based on the percentage and nature of missing data.
  - **Handle Duplicates**:
    - Check for fully duplicate rows: `df.duplicated().sum()`.
    - Check for duplicates based on key identifier columns (e.g., 'Mã tin', URL).
    - Check for duplicates based on a subset of meaningful columns (e.g., address, area, price).
    - Decide on removal strategy for duplicates.
  - **Data Type Conversion**:
    - Convert columns to appropriate types (e.g., 'price' to numeric, 'area' to numeric, date columns to datetime).
    - Ensure units are consistent (e.g., price in VND, area in m²).
  - **Feature Engineering (Initial)**:
    - Extract numerical values from text (e.g., price, area).
    - Create flags or separate columns for mixed information (e.g., `price_per_m2_flag`).
    - Consider extracting features from `address` (e.g., district, city, street, ward).
    - Consider extracting features from `description` or `title` (e.g., presence of keywords like "mặt tiền", "hẻm", "view").
    - If date information is available (e.g., 'Ngày đăng', 'Ngày hết hạn'), extract components like year, month, day, day of week.

  ### 3. Univariate Analysis (Analyzing individual features)
  - **Numerical Features**:
    - **Distribution Plots**: Histograms (`sns.histplot`) and KDE plots for key numerical features like `price_numeric`, `area_numeric`, `Số phòng ngủ`, `Số lầu`.
    - **Box Plots** (`sns.boxplot`): To identify central tendency, spread, and outliers for numerical features.
    - **Log Transformation**: For skewed numerical data (like price or area) to help in visualization and modeling.
  - **Categorical Features**:
    - **Frequency Counts**: `value_counts()` for columns like `Loại tin`, `Loại BDS`, `Pháp lý`, extracted location parts (district, city).
    - **Bar Plots** (`sns.countplot`): To visualize the frequency of categories.
    - Analyze cardinality (number of unique values) of categorical features. High cardinality might require special handling.

  ### 4. Bivariate Analysis (Analyzing relationships between two features)
  - **Target Variable vs. Other Features** (assuming `price_numeric` is the target):
    - **Numerical vs. Numerical**:
      - Scatter plots (`sns.scatterplot`) between `price_numeric` and other numerical features (`area_numeric`, `Số phòng ngủ`, `Số lầu`).
      - Correlation matrix (`df.corr()`) and heatmap (`sns.heatmap`) to quantify linear relationships.
    - **Categorical vs. Numerical (Target)**:
      - Box plots or Violin plots (`sns.boxplot`, `sns.violinplot`) of `price_numeric` grouped by categorical features (`Loại BDS`, `Pháp lý`, district, city).
      - Bar plots of mean/median `price_numeric` for each category.
  - **Feature vs. Feature**:
    - **Numerical vs. Numerical**: Scatter plots and correlation matrix for relationships between independent numerical features.
    - **Categorical vs. Categorical**:
      - Crosstabulations (`pd.crosstab`) and stacked bar charts.
      - Chi-squared test for independence if appropriate.
    - **Categorical vs. Numerical (Independent)**: Box plots, violin plots.

  ### 5. Multivariate Analysis (Analyzing relationships between three or more features)
  - **Pair Plots** (`sns.pairplot`): To visualize pairwise relationships between a subset of important numerical features, possibly colored by a categorical variable.
  - Grouped aggregations: e.g., mean price by `Loại BDS` and `district`.
  - Consider 3D scatter plots for visualizing three numerical variables if appropriate.

  ### 6. Geospatial Analysis (If detailed location data is available)
  - If latitude/longitude are available or can be derived:
    - Plot property locations on a map.
    - Create heatmaps of average prices by geographical areas.
    - Analyze proximity to amenities (schools, hospitals, transport) if this data can be obtained/engineered.
  - Analyze price variations across different administrative units (district, ward, city) using bar plots or choropleth maps.

  ### 7. Text Data Analysis (for 'title', 'description')
  - **Word Clouds**: To visualize frequent words.
  - **N-gram analysis**: To find common phrases.
  - Basic sentiment analysis if applicable (e.g., positive/negative language in descriptions).
  - Identify keywords related to property features or condition.

  ### 8. Time Series Analysis (If date/time information is available and relevant)
  - If features like 'listing date' or 'sale date' exist:
    - Plot average price trends over time.
    - Analyze seasonality in listings or prices.

  ### 9. Outlier Detection and Treatment Strategy
  - Revisit outlier detection using box plots, scatter plots, or statistical methods (e.g., Z-score, IQR).
  - Investigate outliers: Are they data entry errors or genuine extreme values?
  - Decide on a strategy for handling outliers (e.g., capping, transformation, removal – be cautious with removal).

  ### 10. Summarize Findings and Hypotheses
  - Document key insights, patterns, and relationships discovered.
  - Note any data quality issues or limitations.
  - Formulate initial hypotheses about what features might be important for predicting real estate prices.
  - Identify features that might need further cleaning or transformation in the preprocessing phase.
  - Consider potential new features that could be engineered.