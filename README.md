# RealEstate-EDA-Modeling

A data science project for predicting real estate prices in Hanoi using online data (location, area, amenities, price trends, etc.). Includes data collection, EDA, and predictive modeling to support buyers and investors.

## Project Overview

This project develops a machine learning model to predict real estate prices in Hanoi, Vietnam. By analyzing various factors that influence property values, the model aims to provide accurate price estimates to assist potential buyers, sellers, and investors in making data-driven decisions in the Hanoi real estate market.

## Objectives

- Collect comprehensive real estate data from online sources in Hanoi
- Perform exploratory data analysis (EDA) to identify patterns and relationships
- Develop and compare multiple predictive models for real estate price estimation
- Evaluate model performance and select the most accurate approach
- Create interpretable insights to understand key price-driving factors

## Data Sources

The project uses data collected from various online real estate platforms, including:

- Property details (area, number of bedrooms, number of bathrooms, etc.)
- Location information (district, proximity to city center, etc.)
- Nearby amenities (schools, hospitals, parks, public transportation)
- Historical price trends
- Additional features (property age, renovation status, etc.)

## Methodology

1. **Data Collection**: Web scraping and API integration with real estate platforms
2. **Data Cleaning & Preprocessing**: Handling missing values, outlier detection, feature engineering
3. **Exploratory Data Analysis**: Statistical analysis and visualization of relationships between variables
4. **Feature Selection**: Identifying the most significant factors affecting property prices
5. **Model Development**: Training various algorithms (Linear Regression, Random Forest, XGBoost, etc.)
6. **Model Evaluation**: Comparing models using metrics like RMSE, MAE, and R²
7. **Interpretation & Insights**: Extracting actionable insights from the best-performing model

## Project Structure

```
RealEstate-EDA-Modeling/
├── Data Collection/         # Scripts and data collection methods
├── Data Exploration/        # Jupyter notebooks exploring data
├── data/                    # Raw and processed datasets
├── Data Preprocessing       # Scripts for data cleaning and feature engineering
├── Modeling                 # 
└── Report/                  # Report pdf file
```

## Technologies Used

- Python
- Pandas, NumPy for data manipulation
- Matplotlib, Seaborn for data visualization
- Scikit-learn, XGBoost for modeling
- GeoPandas for geospatial analysis
- Jupyter Notebooks for interactive development

## Results and Insights

The project aims to identify key factors influencing real estate prices in Hanoi and provide a reliable prediction model. Results will include:
- Analysis of which districts show the highest price growth
- Importance of different amenities on property values
- Price predictions with confidence intervals
- Recommendations for investment opportunities

## Future Work

- Incorporate more dynamic factors like economic indicators
- Develop a web interface for real-time price predictions
- Extend the model to other Vietnamese cities
- Include time series forecasting for future price trends

## Contributors

- [Your Name]

## License

[Specify license information]
