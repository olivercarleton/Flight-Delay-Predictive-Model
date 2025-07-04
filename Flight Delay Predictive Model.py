# -*- coding: utf-8 -*-
"""Daly-Carleton-Tutorial.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12--WgQ87-uzDA2D8fjHfhU0DFxJAdjRU

# **Final Tutorial:**
Oliver Carleton || Killian Daly

# Webpage #
https://kdaly24.github.io/
# Goal #

Every day, thousands of flights across America leave from busy airports containing hundreds of thousands of passengers. Every day, while most flights leave on time, many flights can be delayed due to a variety of factors, many of which are witheld from passengers. Our model seeks to answer a question any passenger has. Why is my flight delayed, and for how long will it be delayed?

Using linear regression, the goal to create a predictive model that uses historical flight data of the past five years (2019-2024) to estimate whether a flight will be delayed, and if so by how much. Based on the series of factors from our dataset, the model will output an estimated numerical minute value for the user. The model relies on features of historical data to make these predictions, such as airport location, departure time, and current weather data pulled from two separate airport datasets.


# Data Collection
Our datasets are pulled from a military America weather dataset, as well as a domestic airline dataset found on Kaggle. Links to our datasets are found below. For those interested in **further research** and testing, we can use any of the other datasets found at the other provided links to get insights as to other features, such as past specific plane ID (tracking number of past flights to determine if a plane may need spontaneous repair services which could cause delay).

CSV- flights_sample_3m.csv || /content/flights_sample_3m.csv.zip

API Dataset-

*  Kaggle dataset (Airline Delays): Historical flight delay data, including flight times, causes of delays, and airports.
*  RapidAPI for weather data: Retrieve weather conditions during flight departures for each airport.
*  OpenSky Network API: Real-time and historical flight tracking data, which includes flight departures.

API links for Historical Flight and Weather Data-

https://rapidapi.com/collection/flight-data-apis

https://openskynetwork.github.io/opensky-api/rest.html

https://www.kaggle.com/datasets/sriharshaeedala/airline-delay

# Model

Our specific model utilized a handful of selected features for linear regression, but you can use any number of features and adjacent model types and achieve different results.

Some suggested models worth exploring for those looking to **further this tutorial and deepdive** would be a K-Nearest Neighbor Model.

Find more information here:
https://www.geeksforgeeks.org/k-nearest-neighbours/


# Collaboration Plan
To ensure we stay on track with the project roadmap and meet all assignment requirements, we will hold weekly progress meetings. These meetings will serve to review our milestones, address any roadblocks, and adjust our timeline if necessary.

Work will be evenly distributed, with both parties contributing equally to the project in terms of coding and writing. Each team member will take responsibility for completing their assigned tasks within the agreed-upon deadlines, ensuring a balance of effort in all aspects of the project.

The first few lines of our code import a series of libraries that we will need for this project, including seaborn and pandas.

Additionally, we have mounted our google drive folder to utilize the downloaded kaggle airport flight delay dataset as a dataframe in python.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# jupyter nbconvert --to html /content/drive/MyDrive/Daly-Carleton-Tutorial.ipynb

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd #Importing all necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('/content/drive/MyDrive/flights_sample_3m.csv') #Reading to a dataframe

df.head()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

df.rename(columns={
    'FL_DATE': 'Flight Date',
    'AIRLINE': 'Airline Name',
    'AIRLINE_DOT': 'Airline Dot Code',
    'AIRLINE_CODE': 'Airline Code',
    'DOT_CODE': 'Dot Code',
    'FL_NUMBER': 'Flight Number',
    'ORIGIN': 'Origin Airport',
    'ORIGIN_CITY': 'Origin City',
    'DEST': 'Destination Airport',
    'DEST_CITY': 'Destination City',
    'CRS_ELAPSED_TIME': 'CRS Elapsed Time',
    'ELAPSED_TIME': 'Elapsed Time',
    'AIR_TIME': 'Air Time',
    'DISTANCE': 'Distance',
    'DELAY_DUE_CARRIER': 'Delay Due To Carrier',
    'DELAY_DUE_WEATHER': 'Delay Due To Weather',
    'DELAY_DUE_NAS': 'Delay Due To Nas',
    'DELAY_DUE_SECURITY': 'Delay Due To Security',
    'DELAY_DUE_LATE_AIRCRAFT': 'Delay Due To Late Aircraft'
}, inplace=True)
# Running these lines to rename our columns to proper terms for our use. Since our data is obtained from a government database, much of the tidy data principles are followed already.
df.head()

"""# **Data Principle Applications**
The dataset shown in the image follows tidy data principles because each column contains a single variable ("Flight Date," "Airline Name," "Origin City"), each row represents an observation (a single flight), and there is a uniform structure for missing data (with `NaN` indicating missing values). The column names are descriptive and meaningful, and the data is organized such that each variable forms a column and each type of observation forms a row.

# Extraction, Transformation, Loading (ETL) - Load and Tidy Data

*  Datset contains flight related data including flight dates, airline names, orgin and destination airports and various delay causes such as carrier weather and air traffic control issues.
*   Dataset used to answer questions related to flight puntuality. Identifying patterns that lead to delyas and analyzing performace difference across airlines, assecin impact of weahter on flight schedules.
*  The dataset is open-access from Kaggle collected using airlines, airpiort, Department of Transportation DOT, and Bureau of Transportation Statistics BTS.

Tidy Data Principles
*   Each Variable forms a column
*   Each Obervation forms a row
*   Each Obervational unit forms a table
"""

df.info() # As we can see here, all of our categorical variables are "objects" whilst our critical numerical observations are represented in ints or floats. This is a big first step of our tidy data principles already accomplished!

df['Airline Name'].unique() # Here we can see all the major airlines we will be using from this dataset. It includes common household brands like United and Delta, as well as lesser known ones.

sub_df = df[['Origin City','CRS_DEP_TIME','DEP_TIME','Flight Date',"DEP_DELAY",'CANCELLED','DIVERTED']] # We create a sub-dataframe of just key statistics for further analysis.

top_3_cities = df['Origin City'].value_counts().nlargest(3).index.tolist()  # This contains just top three most used airports, which we can combine with the previous dataframe.
sub_df_top_3 = sub_df[sub_df['Origin City'].isin(top_3_cities)] #Thus creating a dataframe of only the top three cities and their most relevant statistics. This may be useful for further EDA.

delay_frequency_by_airline = (df.groupby('Airline Name')['DEP_DELAY'].apply(lambda x: (x > 15).mean()) * 100).sort_values(ascending=False)
delay_frequency_by_airline #Using a groupby with a lambda function we can aggregate all rows where the flight was delayed by a relevant amount of time, i.e. more than 15 minutes.
#Then, we calculate the frequency of this relative to the airline.

avg_delay_by_airline = df.groupby('Airline Name')['DEP_DELAY'].mean().sort_values(ascending=False) # Here we can use a groupby to gather all flights and sort by mean departure delays.
avg_delay_by_airline #Here we can see similarities between the delays.

airline_performance = pd.DataFrame({ # Let's now take our statistics from above regarding delay and create a dataframe of just these points so we can easily use them for a graphic.
    'Delay Frequency (%)': delay_frequency_by_airline,
    'Average Delay Length (min)': avg_delay_by_airline
})

plt.figure(figsize=(16, 10)) # Here we create a graphic to depict airline performance by comparing the average likelihood of a delay to the length of said delay.
sns.scatterplot(x='Delay Frequency (%)', y='Average Delay Length (min)', data=airline_performance, color = 'red', s=100, alpha = .8)
# Here we add labels for each point on the graph.
for id, row in airline_performance.iterrows():
    plt.annotate(id, (row['Delay Frequency (%)'], row['Average Delay Length (min)']), xytext=(-10,3), color = 'black', textcoords='offset points', fontsize=9, alpha=0.8, rotation = 25)
# Offset and rotation here is key to avoid overlapping text annotations.
plt.title('Airline Performance: Delay Frequency vs Average Delay Length', fontsize=16)
plt.xlabel('Delay Frequency (%)', fontsize=12)
plt.ylabel('Average Delay Length (min)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

"""# **Relevance of Statistics**

The statistics shown are relevant because they provide key insights into the factors influencing flight delays.
- **Day of the Week and Month Delays**: These help identify patterns, showing that certain days (weekends) or months (holiday seasons) are more prone to delays. This is relevant for understanding when delays are more likely to occur based on travel behavior.
- **City-Specific Delays**: This statistic identifies cities with higher average delays, like Ogden, UT, which may be affected by seasonal factors (winter sports) or weather conditions. This is useful for identifying geographic risk factors.
- **Airline Performance**: The graph plotting delay frequency versus average delay length per airline helps visualize which airlines are more prone to delays and how long those delays typically last. This is crucial for understanding carrier-specific behavior, which can be a predictive factor in the model.

The graphic showing **Airline Performance (Delay Frequency vs. Average Delay Length)** is particularly relevant to the project, as it visually conveys how often delays occur for different airlines and the severity of those delays. Understanding these patterns is essential for predicting delays based on the airline a user is flying with, thus improving the model's accuracy when incorporating this feature.

"""

df['Day Of Week'] = pd.to_datetime(df['Flight Date']).dt.dayofweek #Here we find an additional important summary statistic by aggregating departure delay by day of the week.
avg_delay_by_day = df.groupby('Day Of Week')['DEP_DELAY'].mean() #This clearly shows us that departure delay is lowest during Monday and Tuesday, which makes sense.
avg_delay_by_day # Monday and Tuesday are the days when people take the least recreational flights / vacations.

median_delay_by_origin = df.groupby('Origin City')['DEP_DELAY'].median().sort_values(ascending=False).head(20) #Here we find the places with the greatest median departure delay, to identify outliers.
median_delay_by_origin #Clearly, Cold Bay Alaska is a massive outliar in the data, with incredible average delay relative to the next best, Ogden.
#Ogden is the second largest average delay. Since it is a town adjacent to many ski resorts in Utah, this delay could potentially be ascribed to large delays during ski season and cold weather.

df['Month'] = pd.to_datetime(df['Flight Date']).dt.month #This aggregates by month to determine which times of year may result in the largest delays
avg_delay_by_month = df.groupby('Month')['DEP_DELAY'].mean() #Using a groupby, we clearly identify the summer months (June through August) and December as the most likely months for delays.
avg_delay_by_month # This is clearly related to most common vacation times, as people (especially large groups) are more likely to take vacations during School and Winter breaks.

"""# **End of Step One**

Now that we have properly loaded, tidied, and examined the domestic airline dataset, it is time to input our weather dataset and examine the correlations that appear!

# **Milestone Two -- Working with the Weather Dataset**

Working towards our ultimate goal of creating a model which can predict flight delays, we plan to incorporate a second dataset that tracks weather patterns over the same period of time. By ascribing the relevant weather events to flights that left at the same time at the same airport that reported it, we can dig deeper into the "flight delay" metric of our first dataset and identify root causes for why a delay may be caused.
"""

weather_df = pd.read_csv('/content/drive/MyDrive/WeatherEvents_Jan2016-Dec2022.csv') #Loading in our dataset.
weather_df.head()

#First we must clean our data for merging. given that the processing time of colab does not effectively run through 3 million and 4.9 million data point merges.
# We will create "state" signifiers for our original dataframe, and a "year" signifier for both dataframes that can be used to merge our datasets.
weather_df['Flight Date'] = weather_df['StartTime(UTC)'].astype(str).str.slice(0, 10)
df['Origin State'] = df['Origin City'].str.split(', ')
df['Origin State'] = df['Origin State'].astype(str).str.slice(-4,-2)
df['Destination State'] = df['Destination City'].str.split(', ')
df['Destination State'] = df['Destination State'].astype(str).str.slice(-4,-2)
transpose_weather_df = weather_df[['EventId', 'Type','Severity', 'Flight Date','Precipitation(in)','State']]
transpose_weather_df['Year'] = transpose_weather_df['Flight Date'].str.slice(0,4)
merge_weather_df = transpose_weather_df[transpose_weather_df['Year'].astype(int) >= 2019] # Here we take only the relevent data -- 2019 or newer, which works with our other dataset.

severity_order = {'Severe': 1, 'Heavy': 2, 'Moderate': 3, 'Light': 4, 'Other': 5, 'UNK': 6} # Here we create a priority order for severity to compress data.
# We need to do this because the amount of data we have forces google colab to regularly crash, so in order to follow tidy data principles we must compress the weather types.

def combine_types(types): # Here we create our combine function.
    return ', '.join(sorted(set(types)))

def highest_severity(severities): # Here is his severity sorting function.
    return min(severities, key=lambda x: severity_order.get(x, float('inf')))

result_df = merge_weather_df.groupby(['Flight Date', 'State']).agg({ # Here we compress our dataframe properly by using our above features, but we take the first/greatest available data point
# for year, event, and precipitation, so we can keep the relevant precipitation data whilst compressing the other data.
    'Type': combine_types,
    'Severity': highest_severity,
    'Year': 'first',
    'EventId': 'first',
    'Precipitation(in)': 'max'
}).reset_index()

merged_df = pd.merge(df, result_df, left_on=['Flight Date', 'Origin State'], right_on=['Flight Date', 'State'], how='left') # Now we merge our two dataframes on date and state of origin.

merged_df['Precipitation(in)'] = merged_df['Precipitation(in)'].fillna(0.00) #Here we tidy our now combined dataframe, filling empty precipitation, type, and severity columns.
merged_df['Type'] = merged_df['Type'].fillna('None')
merged_df['Severity'] = merged_df['Severity'].fillna('None')
merged_df.drop(columns=['State', "EventId"], inplace = True) # We also drop irrelevant columns used for merging.

"""Now that we have merged our datasets, we can explore the newly merged weather data and find potential correlations to flight delays."""

# To analyze severity, we group data by 'Origin State' and 'Severity', counting the frequency of delays.
delay_counts = merged_df.groupby(['Origin State', 'Severity']).size().unstack(fill_value=0)

# Plotting our delay frequency.
delay_counts.plot(kind='bar', stacked=True, figsize=(14, 8))
plt.title('Weather Event Severity vs Delay Frequency by Origin State')
plt.xlabel('Origin State')
plt.ylabel('Delay Frequency')
plt.legend(title='Severity')
plt.xticks(rotation=45)
plt.show()

"""Displays the frequency of delays by severity level (Heavy, Moderate, Light, None, Severe, Unknown) across various origin states. This shows how often delays occur with different severities in each state."""

from sklearn.linear_model import LinearRegression

# Next, we are going to look at weather severity and map it to numerical values to categorically compare this to numerical values.
severity_mapping = {'Severe': 3, 'Moderate': 2, 'Light': 1}
merged_df['Severity_Num'] = merged_df['Severity'].map(severity_mapping)

# Now we can remove  rows with missing delay values and calculate total delay by summing different types of delay columns to get total delay
delay_columns = ['Delay Due To Nas', 'Delay Due To Security', 'Delay Due To Late Aircraft']
merged_df['Total_Delay'] = merged_df[delay_columns].sum(axis=1, skipna=True)

# Now we will group by Origin State and quantitative Severity and calculate the average delay
delay_data = merged_df.groupby(['Origin State', 'Severity_Num']).agg({'Total_Delay': 'mean'}).reset_index()

# Plot our data
plt.figure(figsize=(10, 6))
sns.regplot(x='Severity_Num', y='Total_Delay', data=delay_data, scatter_kws={'s': 50, 'alpha': 0.7})
plt.title('Correlation between Weather Severity and Average Delay')
plt.xlabel('Weather Event Severity (1=Light, 2=Moderate, 3=Severe)')
plt.ylabel('Average Delay (minutes)')
plt.show()

# For additional data, we can also calculate correlation.
correlation = delay_data['Severity_Num'].corr(delay_data['Total_Delay'])
print(f"Correlation between weather severity and delay: {correlation:.2f}")

"""This shows the relationship between weather event severity (mapped numerically from Light = 1 to Severe = 3) and average delay in minutes, with a regression line. It indicates a positive but weak correlation between higher severity and longer delays. Potentially, once we remove some outliars and add in additional features, this could make up the basis of our model."""

# Now that we know there is a non-zero correlation between weather severity and delay, we can look for other correlations, for example precipitation

rain_only = merged_df.loc[merged_df['Type'] == 'Rain'] # Here we create a dataframe where only rain is a weather effect.
plt.figure(figsize=(10, 6))

# Using seaborne, create a scatter plot with regression to analyze precipitation
sns.regplot(
    x='Precipitation(in)', y='Delay Due To Weather', data=rain_only,
    scatter_kws={'s': 70, 'alpha': 0.6}, line_kws={'color': 'darkblue'}
)

# We plot our data here
plt.title('Relationship between Precipitation and Average Delay', fontsize=16, weight='bold')
plt.xlabel('Precipitation (inches)', fontsize=12)
plt.ylabel('Average Delay (minutes)', fontsize=12)
plt.ylim(0, 25)  # Set y axis and x axis limit to focus on relevant range of data
plt.xlim(0, rain_only['Precipitation(in)'].max() * 1.1)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Show plot
plt.show()

# Again, we can calculate the correlation coefficient for more insight!
correlation_precip = rain_only['Precipitation(in)'].corr(rain_only['Delay Due To Weather'])
print(f"Correlation between precipitation and delay: {correlation_precip:.2f}")

"""Depicts the relationship between precipitation (in inches) and average delay in minutes with a regression line. The correlation is minimal, suggesting precipitation alone is not strongly linked to delay duration. This is likely due to the advancements in modern flight technology and air traffic control that allow flights to take off in rainy conditions."""

# Sort the data by average delay and select the top 15 weather types with the highest delays
avg_weather_delay = merged_df.groupby('Type')['Total_Delay'].mean().reset_index()
avg_weather_delay.columns = ['Type', 'Avg_Delay']
top_avg_weather_delay = avg_weather_delay.sort_values(by='Avg_Delay', ascending=False).head(15)

# Plotting
plt.figure(figsize=(12, 8))
top_avg_weather_delay.plot(kind='barh', x='Type', y='Avg_Delay', color='cornflowerblue', edgecolor='black', figsize=(12, 8))

# Improve plot aesthetics
plt.title('Top Weather Types by Average Delay Due to Weather', fontsize=16, weight='bold')
plt.xlabel('Average Delay Due to Weather (minutes)', fontsize=12)
plt.ylabel('Weather Type', fontsize=12)
plt.gca().invert_yaxis()  # Invert y-axis to have the highest delays at the top
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Show plot
plt.tight_layout()
plt.show()

"""This shows average delay durations due to weather by specific weather types, highlighting which conditions cause the most delays. Some weather types lead to significantly higher delays than others. However, due to the grouping, this is not as elucidating unless we also look at the 15 least delayed weather types."""

# Sort the data by average delay and select the top 30 weather types with the lowest delays
bottom_avg_weather_delay = avg_weather_delay.sort_values(by='Avg_Delay', ascending=True).head(30)

# Plotting
plt.figure(figsize=(12, 8))
bottom_avg_weather_delay.plot(kind='barh', x='Type', y='Avg_Delay', color='cornflowerblue', edgecolor='black', figsize=(12, 8))

# Improve plot aesthetics
plt.title('Bottom Weather Types by Average Delay Due to Weather', fontsize=16, weight='bold')
plt.xlabel('Average Delay Due to Weather (minutes)', fontsize=12)
plt.ylabel('Weather Type', fontsize=12)
plt.gca().invert_yaxis()  # Invert y-axis to have the highest delays at the top
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Show plot
plt.tight_layout()
plt.show()

"""Comparing the two, we can see all of the parameters with little to no complications, as expected lead to very little delays. As one would expect, when looking at these 30 versus the top 15 delays, this graph expressed very few weather conditions with more than three cumulative conditions that day.

Additionally, and critically to note, cold also seems to have almost no impact on delay, with nearly all cold weather patterns falling within the bottom 30 unless accompanies by storm or hail.

# Plausible Models
1. **Weather Severity Model**:
  The graphs above answered our earlier reservations about weather type and severity, and defends the assumption that the weather model is worth exploring.
   - **Objective**: To predict the average delay time based on weather severity.
   - **Independent Variable**: Weather severity level (categorized as Light, Moderate, Heavy, Severe).
   - **Dependent Variable**: Average delay time in minutes.
   - **Methodology**: A regression model could be applied, using severity levels as input to quantify the impact of different severity categories on delay times. The correlation observed in the EDA section supports this model, showing that higher severity is associated with longer delays. Outliers may be removed to enhance model accuracy, and additional features (like location or specific weather types) could be incorporated for a more nuanced model.

2. **Airline Airport Impact Model**:
  Some of the highest correlations that we've experienced come from Airline and Airport metrics, and we proved from the Airline Performance Graph that airlines with frequent delays also have longer delays, meaning that if we are able to predict based on airline, we may be able to separate out the longest delay types.
   - **Objective**: To examine the influence of situational factors such as Airline and Airport on delay duration specifically related to weather.
   - **Independent Variables**: Airline, Airport, Date, Month.
   - **Dependent Variable**: Average delay time in minutes.
   - **Methodology**: This model would use linear regression to predict the likelihood of a delay based on circumstantial factors of an individual flight. The EDA indicates minimal correlation between certain weather patterns such as precipitation alone and delay, potentially due to modern aviation adaptations. However, certain holiday seasons and weekends tend to have more flight delays. In order to track the variability of these delays, we will use these features to separate out the worst managed and best managed airlines, potentially catching the delays due to non-weather factors as well.

These observations may form the base of our model, but we may combine them and utilize other features of our data, such as origin city to create a multifaceted and more successful model!
"""

ordinal_encoder = OrdinalEncoder() # This is an encoder, used for converting categorical features in our dataset.

merged_df['Delay Due To Weather'].fillna(0.0, inplace = True) # Here we fillna to ensure we can utilize our delay data, as there are some unreported NA values.

sample_df = merged_df[merged_df['Delay Due To Weather'] > 0.0] # Here we take a sample of only values where delays exist, to properly test our data.
sample_df = sample_df.sample(n=500) # We want a sample of 500 rather than the entire set, as working with millions of data points exceeds the COLAB available ram.

encoded_columns = ordinal_encoder.fit_transform(sample_df[['Origin Airport', 'Type', 'Airline Name', 'Severity']]) # Using fit transform we will encode our categorical features into:
sample_df[['Airport_Encoded', 'Type_Encoded', 'Airline_Encoded', 'Severity_Encoded']] = encoded_columns # "Encoded" versions of the features to use in our model.

dummy_features = sample_df[['Airport_Encoded', "Type_Encoded", "Airline_Encoded", "Severity_Encoded"]] # Ascribe these encoded or "dummy features" for concatenation

merged_select = pd.concat([sample_df, dummy_features], axis=1) # Take the dummy features and merge them with the other features to make up our model.

"""Before we create a final linear regression model, reviewing some of the now encoded features for correlations with Weather Based Delay and Total Delay will help us identify how valuable, if at all, these features are to contributing to overall model success"""

X2 = merged_select[['Airline_Encoded','Type_Encoded', 'Severity_Encoded', 'Airport_Encoded', 'Month','Day Of Week', 'Delay Due To Weather', 'Total_Delay']] #We will take another set of features here for our correlation matrix, so we can view
X2 = X2.loc[:, ~X2.columns.duplicated()] # multiple relationships between the data features in one graph.

correlation_matrix = X2.corr() # Here we can create a correlation matrix, which we can plot in subsequent lines to give a visual indicator of feature correlation.

# Plot heatmap of the correlation matrix.
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.show()

X = merged_select[['Month','Day Of Week', 'Severity_Encoded', 'Delay Due To Weather']] #Identify our features and fill NA values.
X.fillna(0, inplace=True)

# Identify the target variable and split the dataset into training and testing sets.
y = sample_df['Total_Delay']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model.
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set, calculate y_prediction output.
y_pred = model.predict(X_test)

"""The correlation matrix reveals weak linear relationships among most dataset features, with values close to zero indicating minimal correlation. A moderate negative correlation (-0.65) is observed between "Type_Encoded" and "Severity_Encoded," suggesting some dependency. Overall, the lack of strong correlations highlights the need for further exploration or nonlinear modeling to uncover deeper relationships."""

results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}) # Using the y_test and y_predicted values, we can find our discrepancies between the actual values we tested on and the predicted values.
print(results.head())
correlation = np.corrcoef(y_test, y_pred)[0, 1] # Printing the correlation shows the outputs of our model.
print("Correlation between Actual and Predicted:", correlation)

"""### **Flight Delays Decoded: Insights and Future Directions**

Our deep dive into flight delays revealed a complex landscape of factors that influence travel disruptions. Through innovative data visualization and analysis, we uncovered some surprising patterns that challenge traditional assumptions about what causes flight delays.

**What We Discovered**

The journey began with an exploration of potential delay triggers, examining everything from weather conditions to airline-specific performance. Our findings paint a nuanced picture:

1. **Weather's Unpredictable Impact**
Contrary to simple expectations, weather isn't just a binary good-or-bad factor. We found that severe weather conditions like hailstorms and heavy snow do indeed cause delays, an average of 12–14 minutes. However, milder weather is more forgiving, with minimal 4–5 minute disruptions. The real story is in the details – location matters dramatically, with delay patterns varying significantly across different states. In addition, the necessity to group military air bases (tracking weather) and domestic airports (tracking flight delays) at best by state or zipcode result in certain states being more traceable than others with regard to weather pattern.

2. **Airlines: Not All Are Created Equal**
Some airlines seem to dance more gracefully with disruption than others. Frontier, for instance struggled with both frequency and duration of delays. Our analysis revealed substantial variations in how different carriers handle scheduling and operational challenges.

3. **The Correlation Conundrum**
Most interestingly, our initial linear models struggled to tell the full story. With correlation coefficients hovering near zero, it became clear that flight delays are too complex for straightforward predictions. One intriguing exception? A notable relationship between flight type and delay severity that hints at deeper underlying dynamics.

**Looking Forward: Smarter Delay Prediction**

One critical observation from our tutorial is that when testing, focusing only on delayed flights exaggerates delay durations in the model, skewing predictions when applied to the entire dataset. Conversely, including all flights dilutes the model's sensitivity to factors that predict delays. Balancing these inputs was a challenge of this tutorial and refining this would be a highly beneficial next step forward.

Future steps should consider combining weather-related features like severity, precipitation, and location data to enhance predictions. Additionally, implementing non-linear modeling methods may better capture complex interactions that our linear regression model failed to address, such as those between airline-specific performance (Figure: Delay Frequency vs. Average Delay Length) and weather conditions. By addressing these limitations, the model can better predict flight delays with accuracy and contextual relevance.


- **Non Linear Modeling**: By embracing techniques like KNN, Random Forests and Decision Trees, we can capture the impacts of certain features pertaining to flight delays that this linear model may have missed.
- **Other Data Strategies**: Further Data Analysis and real time datasets (found at the top of the tutorial) may afford us new insights into these features. By understanding the reasoning behind currently hidden factors that cause delays, we can create a model that makes travel easier.

**The Road Ahead**
For anyone using this tutorial, the best next step would be to look at additional model types and different features! Refer to the top of this tutorial for links for further exploration, inlcuding real-time datasets and different model concepts, including K-Nearest Neighbors.
"""