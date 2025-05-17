import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import time

st.title("Olympics Dataset Analytics")

nav = st.sidebar.radio("Navigation", ['Home', 'Exploratory Data Analysis',
                                      'Data Preprocessing', 'Trends', 'Prediction', 'Stress'])

if nav == 'Home':
    st.image("https://upload.wikimedia.org/wikipedia/commonsQ/thumb/5/5c/Olympic_rings_without_rims.svg/640px-Olympic_rings_without_rims.svg.png", width=800)
    st.write("The main theme of this app is to perform data analytics on Olympic datasets (namely Athlete Events and Athlete BMI datasets)...")

    if st.button('Load Main/Athlete Events dataset'):
        st.write('Loaded successfully! Can perform analysis on it by following this flowchart')
        st.graphviz_chart('''
        digraph {
        Home -> ExploratoryDataAnalysis
        ExploratoryDataAnalysis -> DataPreprocessing
        DataPreprocessing -> Trends
        Trends -> Prediction
        DataPreprocessing -> Prediction
        }
        ''')

    if st.button('Load Athlete BMI dataset'):
        st.write('Loaded successfully! Can perform predictions on it')
        st.graphviz_chart('''
        digraph {
        Home -> Prediction
        }
        ''')

data = pd.read_csv('athlete_events.csv')
p = pd.DataFrame(data)

if nav == 'Exploratory Data Analysis':
    st.header('Exploratory Data Analysis')

    if st.checkbox("Show Dataset"):
        st.write(p)

    if st.checkbox("Show first 5 values of the Dataset"):
        st.dataframe(p.head())

    if st.checkbox("Get the total number of Rows and Columns"):
        st.write(p.shape)

    if st.checkbox("Show the Statistical Information Of the Columns/Attributes"):
        st.write(p.describe())

    if st.checkbox("Null Values in columns"):
        d = pd.DataFrame(p.isnull().sum()).transpose()
        st.write(d)

    st.subheader("Columns with Null Values")
    null_columns = p.columns[p.isnull().any()]
    for col in null_columns:
        if st.checkbox(f"Show athletes with null values in '{col}'"):
            null_athletes = p[p[col].isnull()]['Name']
            st.write(f"Athletes with null values in '{col}':")
            st.write(null_athletes.reset_index(drop=True))

if nav == 'Data Preprocessing':
    st.header('Data Preprocessing')

    if st.checkbox("Remove Null Values in Age Column"):
        p['Age'] = p['Age'].fillna(p.Age.mean())
        st.dataframe(p)

    if st.checkbox("Remove Null Values in Height Column"):
        p['Height'] = p['Height'].fillna(p.Height.mean())
        st.dataframe(p)

    if st.checkbox("Remove Null Values in Weight Column"):
        p['Weight'] = p['Weight'].fillna(p.Weight.mean())
        st.dataframe(p)

    if st.checkbox('Convert Medals to Numeric datatype and Remove Null Values'):
        p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3})
        p['Medal'] = p['Medal'].fillna(0)
        st.write(p)

    if st.checkbox("Updated Null Values"):
        d = pd.DataFrame(p.isnull().sum()).transpose()
        st.write(d)

    if st.checkbox("Remove redundant column"):
        p = p.drop(['Games'], axis=1)
        st.write(p)

    if st.button("Final Dataset"):
        st.write(p)

if nav == 'Trends':
    st.header('Trends')

    if st.checkbox("Analyze the relationship between the Height and Weights of an athlete"):
        graph = st.selectbox("What kind of Plot do you want?", ['Scatter Plot', 'Histogram'])
        if graph == 'Histogram':
            fig = px.histogram(p, x=p.Height, color=p.Weight)
            st.write(fig)
        if graph == 'Scatter Plot':
            plt.scatter(p['Height'], p['Weight'])
            plt.xlabel('Height')
            plt.ylabel('Weight')
            plt.title('Height Vs Weight')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

    if st.checkbox('Approximate Number of Males And Females Participated in the Olympics'):
        p['Sex'].value_counts().plot.bar()
        st.pyplot()

    if st.checkbox("Determine the Participation trend in the Summer and Winter Seasons"):
        fig = px.histogram(p, x=p.Season, color=p.Sex, barmode="group")
        st.write(fig)

    if st.checkbox('Women Participation over the years'):
        y = p[p['Sex'] == 'F']
        fig = px.histogram(y, x='Year')
        st.write(fig)

    if st.checkbox('Number of Medals Won by M and F'):
        p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
        fig = px.histogram(p, x=p.Sex, color=p.Medal)
        st.write(fig)

    if st.checkbox("Athletes with Most Medals"):
        p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
        df = pd.get_dummies(p['Medal']).drop([0], axis=1)
        df['Name'] = p['Name']
        df['Total'] = df[1] + df[2] + df[3]
        f = df.groupby(df['Name'])['Total'].sum().sort_values(ascending=False).head(10)
        x = pd.DataFrame(f)
        st.write(x)

    if st.checkbox("Countries with Most Medals"):
        p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
        df = pd.get_dummies(p['Medal']).drop([0], axis=1)
        df['Team'] = p['Team']
        df['Total'] = df[1] + df[2] + df[3]
        f = df.groupby(df['Team'])['Total'].sum().sort_values(ascending=False)
        k = f.head(10)
        k = pd.DataFrame(k.index.values)
        st.write(k)

    st.subheader("Find whether your country is in the Zero-Medal list?")
    x = st.text_input('Enter')
    if st.checkbox('Show'):
        if x not in f.index.values:
            st.write('Country not listed in the dataset')
        else:
            st.write('Medals:', f[x])

    if st.checkbox("Countries winning the most Gold medals in a specific year"):
        number = st.number_input('Insert the Leap Year', 1896.00, 2016.00, step=4.00)
        max_year = int(number)
        if st.button('Show'):
            team_list = p[(p.Year == max_year) & (p.Medal == 'Gold')].Team
            if len(team_list) != 0:
                sns.barplot(x=team_list.value_counts().head(),
                            y=team_list.value_counts().head().index)
                st.pyplot()
            else:
                st.write('Enter valid year')

if nav == 'Prediction':
    st.header('Prediction')

    st.subheader('Predict the Weight of an athlete with his/her Height')
    model = LinearRegression()
    p['Height'] = p['Height'].fillna(p.Height.mean())
    p['Weight'] = p['Weight'].fillna(p.Weight.mean())
    x = np.array(p['Height']).reshape(-1, 1)
    y = np.array(p['Weight']).reshape(-1, 1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    model.fit(x_train, y_train)
    t = st.number_input('Enter the Height')
    t = np.array(t).reshape(-1, 1)
    d = model.predict(t)
    if st.button('Predict Weight'):
        st.write(d)

    st.subheader('Predict the suitable Sport with the BMI values')
    data = pd.read_csv('athlete_bmi_dataset.csv')
    k = pd.DataFrame(data)

    if st.checkbox("Show Athlete BMI Dataset"):
        st.dataframe(k)
        st.write("Note:")
        q = {"Value": ['1', '2', '3', '4'],
             "Corresponding Sport": ['Marathon', 'Basketball', 'Rugby', 'Shot Put']}
        st.write(pd.DataFrame(q))

    model1 = LinearRegression()
    j = np.array(k['BMI']).reshape(-1, 1)
    l = np.array(k['Sport']).reshape(-1, 1)
    j_train, j_test, l_train, l_test = train_test_split(j, l, test_size=0.3)
    model1.fit(j_train, l_train)
    t = st.number_input('Enter BMI')
    t = np.array(t).reshape(-1, 1)
    d = model1.predict(t)
    d = d * 10
    d = np.round(d)

    if st.button('Results'):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.001)
            my_bar.progress(percent_complete + 1)

        if d in range(0, 12):
            st.write('Definitely Marathon')
        elif d in range(12, 19):
            st.write('Marathon, But also suitable for Basketball')
        elif d in range(19, 23):
            st.write('Definitely Basketball')
        elif d in range(23, 27):
            st.write('Basketball, But also suitable for Rugby')
        elif d in range(27, 33):
            st.write('Definitely Rugby')
        elif d in range(33, 38):
            st.write('Rugby, can also try shot put')
        else:
            st.write('Opt for Shot Put')

elif nav == 'Stress':
    st.header("Stress Analysis")
    st.write("This page is currently empty. You can add functionality or visualizations here.")
