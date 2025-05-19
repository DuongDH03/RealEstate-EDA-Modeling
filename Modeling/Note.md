# Summary of EDA-new-new.ipynb

This document outlines the sequence of steps performed in the Jupyter notebook `EDA-new-new.ipynb`.

1. **Import Libraries**
   - Load essential Python packages: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `sklearn`, `warnings`, `folium`, etc.

2. **Load and Inspect Data**
   - Read cleaned CSV (`alonhadat-CLEAN2.csv`), display head and file structure.

3. **Initial Data Cleaning & Feature Engineering**
   - Remove rows with missing or zero `area` or `price` values.
   - Drop unused columns and placeholder null values.
   - Compute `price_per_m2` and handle outliers (>1500).
   - Convert `storey` to numeric and drop extreme outliers.

4. **Univariate Analysis of Price per m²**
   - Plot histogram, KDE, QQ-plot, and boxplot for `price_per_m2`.
   - Calculate skewness and observe distribution shape.

5. **Missing Data Exploration**
   - Visualize missingness matrix with `missingno`.
   - Tabulate null counts and percentages.
   - Plot percentage of missing values per column.
   - Drop rows missing in more than three selected features.

6. **Hypothesis Testing: Length vs. Area/Width**
   - Perform paired t-test comparing `length` and `area/width`.
   - Visualize scatter and distribution plots.

7. **Impute Missing Dimensions**
   - Fill missing `length` and `width` values using median.

8. **Correlation Analysis**
   - Compute correlation matrix for numerical features.
   - Plot heatmap of top correlated variables with target.

9. **Categorical Feature Analysis**
   - Plot frequency and average price per m² for categories: `direction`, `house_type`, `land_use_rights`, `district`.

10. **Bivariate Analysis**
    - Generate comprehensive heatmap of correlations among key features.

11. **Geospatial Visualization**
    - Sample 5,000 records and create Folium map with colored circle markers based on `price_per_m2`.

12. **Save Cleaned Data**
    - Export intermediate cleaned data as `alonhadat-CLEAN3.csv`.

13. **Data Engineering & Preprocessing**
    - Split data into training and test sets.
    - Impute missing numerical features (median) and categorical features (mode).
    - Remove outliers using IQR method.
    - Scale numerical features (`RobustScaler`) and positional features (`MinMaxScaler`).
    - One-hot encode categorical variables.

14. **Define Evaluation Metrics**
    - Implement function to compute R², RMSE, and MAPE (with optional log conversion).

15. **Modeling & Evaluation**
    - **XGBoost Regressor:** Train on log-transformed target, evaluate on test set, and save the model.
    - **Random Forest Regressor:** Train and evaluate performance.
    - **Linear Models:** Train LinearRegression, Lasso, Ridge (and cross-validation variants) on original target.
    - **K-Nearest Neighbors:** Train, evaluate, and tune K values via MAPE plot.
    - **Artificial Neural Network:** Build and train a Keras sequential model, evaluate on dev and test sets.

16. **Final Prediction Example**
    - Load saved scalers and XGBoost model.
    - Prepare a sample input: geocode address, impute missing, scale, and encode features.
    - Predict price per m² and compute total price for sample.
