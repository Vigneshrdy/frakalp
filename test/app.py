# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import plotly.express as px
# import seaborn as sns
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# import time
# import serial  # Import pyserial for serial communication

# st.title("Olympics Dataset Analytics")

# nav = st.sidebar.radio("Navigation", ['Home', 'Exploratory Data Analysis',
#                                       'Data Preprocessing', 'Trends', 'Prediction', 'Stress'])

# if nav == 'Home':
#     st.image("https://upload.wikimedia.org/wikipedia/commonsQ/thumb/5/5c/Olympic_rings_without_rims.svg/640px-Olympic_rings_without_rims.svg.png", width=800)
#     st.write("The main theme of this app is to perform data analytics on Olympic datasets (namely Athlete Events and Athlete BMI datasets)...")

#     if st.button('Load Main/Athlete Events dataset'):
#         st.write('Loaded successfully! Can perform analysis on it by following this flowchart')
#         st.graphviz_chart('''
#         digraph {
#         Home -> ExploratoryDataAnalysis
#         ExploratoryDataAnalysis -> DataPreprocessing
#         DataPreprocessing -> Trends
#         Trends -> Prediction
#         DataPreprocessing -> Prediction
#         }
#         ''')

#     if st.button('Load Athlete BMI dataset'):
#         st.write('Loaded successfully! Can perform predictions on it')
#         st.graphviz_chart('''
#         digraph {
#         Home -> Prediction
#         }
#         ''')

# data = pd.read_csv('athlete_events.csv')
# p = pd.DataFrame(data)

# if nav == 'Exploratory Data Analysis':
#     st.header('Exploratory Data Analysis')

#     if st.checkbox("Show Dataset"):
#         st.write(p)

#     if st.checkbox("Show first 5 values of the Dataset"):
#         st.dataframe(p.head())

#     if st.checkbox("Get the total number of Rows and Columns"):
#         st.write(p.shape)

#     if st.checkbox("Show the Statistical Information Of the Columns/Attributes"):
#         st.write(p.describe())

#     if st.checkbox("Null Values in columns"):
#         d = pd.DataFrame(p.isnull().sum()).transpose()
#         st.write(d)

#     st.subheader("Columns with Null Values")
#     null_columns = p.columns[p.isnull().any()]
#     for col in null_columns:
#         if st.checkbox(f"Show athletes with null values in '{col}'"):
#             null_athletes = p[p[col].isnull()]['Name']
#             st.write(f"Athletes with null values in '{col}':")
#             st.write(null_athletes.reset_index(drop=True))

# if nav == 'Data Preprocessing':
#     st.header('Data Preprocessing')

#     if st.checkbox("Remove Null Values in Age Column"):
#         p['Age'] = p['Age'].fillna(p.Age.mean())
#         st.dataframe(p)

#     if st.checkbox("Remove Null Values in Height Column"):
#         p['Height'] = p['Height'].fillna(p.Height.mean())
#         st.dataframe(p)

#     if st.checkbox("Remove Null Values in Weight Column"):
#         p['Weight'] = p['Weight'].fillna(p.Weight.mean())
#         st.dataframe(p)

#     if st.checkbox('Convert Medals to Numeric datatype and Remove Null Values'):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3})
#         p['Medal'] = p['Medal'].fillna(0)
#         st.write(p)

#     if st.checkbox("Updated Null Values"):
#         d = pd.DataFrame(p.isnull().sum()).transpose()
#         st.write(d)

#     if st.checkbox("Remove redundant column"):
#         p = p.drop(['Games'], axis=1)
#         st.write(p)

#     if st.button("Final Dataset"):
#         st.write(p)

# if nav == 'Trends':
#     st.header('Trends')

#     if st.checkbox("Analyze the relationship between the Height and Weights of an athlete"):
#         graph = st.selectbox("What kind of Plot do you want?", ['Scatter Plot', 'Histogram'])
#         if graph == 'Histogram':
#             fig = px.histogram(p, x=p.Height, color=p.Weight)
#             st.write(fig)
#         if graph == 'Scatter Plot':
#             plt.scatter(p['Height'], p['Weight'])
#             plt.xlabel('Height')
#             plt.ylabel('Weight')
#             plt.title('Height Vs Weight')
#             st.set_option('deprecation.showPyplotGlobalUse', False)
#             st.pyplot()

#     if st.checkbox('Approximate Number of Males And Females Participated in the Olympics'):
#         p['Sex'].value_counts().plot.bar()
#         st.pyplot()

#     if st.checkbox("Determine the Participation trend in the Summer and Winter Seasons"):
#         fig = px.histogram(p, x=p.Season, color=p.Sex, barmode="group")
#         st.write(fig)

#     if st.checkbox('Women Participation over the years'):
#         y = p[p['Sex'] == 'F']
#         fig = px.histogram(y, x='Year')
#         st.write(fig)

#     if st.checkbox('Number of Medals Won by M and F'):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         fig = px.histogram(p, x=p.Sex, color=p.Medal)
#         st.write(fig)

#     if st.checkbox("Athletes with Most Medals"):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         df = pd.get_dummies(p['Medal']).drop([0], axis=1)
#         df['Name'] = p['Name']
#         df['Total'] = df[1] + df[2] + df[3]
#         f = df.groupby(df['Name'])['Total'].sum().sort_values(ascending=False).head(10)
#         x = pd.DataFrame(f)
#         st.write(x)

#     if st.checkbox("Countries with Most Medals"):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         df = pd.get_dummies(p['Medal']).drop([0], axis=1)
#         df['Team'] = p['Team']
#         df['Total'] = df[1] + df[2] + df[3]
#         f = df.groupby(df['Team'])['Total'].sum().sort_values(ascending=False)
#         k = f.head(10)
#         k = pd.DataFrame(k.index.values)
#         st.write(k)

#     st.subheader("Find whether your country is in the Zero-Medal list?")
#     x = st.text_input('Enter')
#     if st.checkbox('Show'):
#         if x not in f.index.values:
#             st.write('Country not listed in the dataset')
#         else:
#             st.write('Medals:', f[x])

#     if st.checkbox("Countries winning the most Gold medals in a specific year"):
#         number = st.number_input('Insert the Leap Year', 1896.00, 2016.00, step=4.00)
#         max_year = int(number)
#         if st.button('Show'):
#             team_list = p[(p.Year == max_year) & (p.Medal == 'Gold')].Team
#             if len(team_list) != 0:
#                 sns.barplot(x=team_list.value_counts().head(),
#                             y=team_list.value_counts().head().index)
#                 st.pyplot()
#             else:
#                 st.write('Enter valid year')

# if nav == 'Prediction':
#     st.header('Prediction')

#     st.subheader('Predict the Weight of an athlete with his/her Height')
#     model = LinearRegression()
#     p['Height'] = p['Height'].fillna(p.Height.mean())
#     p['Weight'] = p['Weight'].fillna(p.Weight.mean())
#     x = np.array(p['Height']).reshape(-1, 1)
#     y = np.array(p['Weight']).reshape(-1, 1)
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
#     model.fit(x_train, y_train)
#     t = st.number_input('Enter the Height')
#     t = np.array(t).reshape(-1, 1)
#     d = model.predict(t)
#     if st.button('Predict Weight'):
#         st.write(d)

#     st.subheader('Predict the suitable Sport with the BMI values')
#     data = pd.read_csv('athlete_bmi_dataset.csv')
#     k = pd.DataFrame(data)

#     if st.checkbox("Show Athlete BMI Dataset"):
#         st.dataframe(k)
#         st.write("Note:")
#         q = {"Value": ['1', '2', '3', '4'],
#              "Corresponding Sport": ['Marathon', 'Basketball', 'Rugby', 'Shot Put']}
#         st.write(pd.DataFrame(q))

#     model1 = LinearRegression()
#     j = np.array(k['BMI']).reshape(-1, 1)
#     l = np.array(k['Sport']).reshape(-1, 1)
#     j_train, j_test, l_train, l_test = train_test_split(j, l, test_size=0.3)
#     model1.fit(j_train, l_train)
#     t = st.number_input('Enter BMI')
#     t = np.array(t).reshape(-1, 1)
#     d = model1.predict(t)
#     d = d * 10
#     d = np.round(d)

#     if st.button('Results'):
#         my_bar = st.progress(0)
#         for percent_complete in range(100):
#             time.sleep(0.001)
#             my_bar.progress(percent_complete + 1)

#         if d in range(0, 12):
#             st.write('Definitely Marathon')
#         elif d in range(12, 19):
#             st.write('Marathon, But also suitable for Basketball')
#         elif d in range(19, 23):
#             st.write('Definitely Basketball')
#         elif d in range(23, 27):
#             st.write('Basketball, But also suitable for Rugby')
#         elif d in range(27, 33):
#             st.write('Definitely Rugby')
#         elif d in range(33, 38):
#             st.write('Rugby, can also try shot put')
#         else:
#             st.write('Opt for Shot Put')

# elif nav == 'Stress':
#     st.header("Stress Analysis")
#     st.write("This page displays stress levels from the connected sensor.")

#     # Serial port configuration
#     try:
#         ser = serial.Serial('COM', 9600, timeout=1)  # Replace 'COM3' with your Arduino's port
#         ser.flush()

#         if st.button("Start Monitoring"):
#             st.write("Reading data from the sensor...")
#             stress_levels = []

#             # Continuously read data from the serial port
#             for i in range(10):  # Adjust the range for the number of readings
#                 if ser.in_waiting > 0:
#                     line = ser.readline().decode('utf-8').strip()
#                     st.write(f"Raw Data: {line}")   

#                     # Parse the stress level from the serial output
#                     try:
#                         stress_level = int(line.split('=')[1].split()[0])  # Extract stress value
#                         stress_levels.append(stress_level)
#                         st.write(f"Stress Level: {stress_level}")
#                     except (IndexError, ValueError):
#                         st.write("Invalid data received. Skipping...")

#             # Display the stress levels as a bar chart
#             if stress_levels:
#                 stress_data = pd.DataFrame({
#                     'Reading': range(1, len(stress_levels) + 1),
#                     'Stress Level': stress_levels
#                 })
#                 st.bar_chart(stress_data.set_index('Reading'))

#     except serial.SerialException:
#         st.error("Could not connect to the serial port. Ensure the Arduino is connected and the correct port is specified.")
































# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import plotly.express as px
# import seaborn as sns
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# import time
# import serial
# import serial.tools.list_ports

# st.title("Olympics Dataset Analytics")

# nav = st.sidebar.radio("Navigation", ['Home', 'Exploratory Data Analysis',
#                                     'Data Preprocessing', 'Trends', 'Prediction', 'Stress'])

# if nav == 'Home':
#     st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/640px-Olympic_rings_without_rims.svg.png", width=800)
#     st.write("The main theme of this app is to perform data analytics on Olympic datasets (namely Athlete Events and Athlete BMI datasets)...")

#     if st.button('Load Main/Athlete Events dataset'):
#         st.write('Loaded successfully! Can perform analysis on it by following this flowchart')
#         st.graphviz_chart('''
#         digraph {
#         Home -> ExploratoryDataAnalysis
#         ExploratoryDataAnalysis -> DataPreprocessing
#         DataPreprocessing -> Trends
#         Trends -> Prediction
#         DataPreprocessing -> Prediction
#         }
#         ''')

#     if st.button('Load Athlete BMI dataset'):
#         st.write('Loaded successfully! Can perform predictions on it')
#         st.graphviz_chart('''
#         digraph {
#         Home -> Prediction
#         }
#         ''')

# data = pd.read_csv('athlete_events.csv')
# p = pd.DataFrame(data)

# if nav == 'Exploratory Data Analysis':
#     st.header('Exploratory Data Analysis')

#     if st.checkbox("Show Dataset"):
#         st.write(p)

#     if st.checkbox("Show first 5 values of the Dataset"):
#         st.dataframe(p.head())

#     if st.checkbox("Get the total number of Rows and Columns"):
#         st.write(p.shape)

#     if st.checkbox("Show the Statistical Information Of the Columns/Attributes"):
#         st.write(p.describe())

#     if st.checkbox("Null Values in columns"):
#         d = pd.DataFrame(p.isnull().sum()).transpose()
#         st.write(d)

#     st.subheader("Columns with Null Values")
#     null_columns = p.columns[p.isnull().any()]
#     for col in null_columns:
#         if st.checkbox(f"Show athletes with null values in '{col}'"):
#             null_athletes = p[p[col].isnull()]['Name']
#             st.write(f"Athletes with null values in '{col}':")
#             st.write(null_athletes.reset_index(drop=True))

# if nav == 'Data Preprocessing':
#     st.header('Data Preprocessing')

#     if st.checkbox("Remove Null Values in Age Column"):
#         p['Age'] = p['Age'].fillna(p.Age.mean())
#         st.dataframe(p)

#     if st.checkbox("Remove Null Values in Height Column"):
#         p['Height'] = p['Height'].fillna(p.Height.mean())
#         st.dataframe(p)

#     if st.checkbox("Remove Null Values in Weight Column"):
#         p['Weight'] = p['Weight'].fillna(p.Weight.mean())
#         st.dataframe(p)

#     if st.checkbox('Convert Medals to Numeric datatype and Remove Null Values'):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3})
#         p['Medal'] = p['Medal'].fillna(0)
#         st.write(p)

#     if st.checkbox("Updated Null Values"):
#         d = pd.DataFrame(p.isnull().sum()).transpose()
#         st.write(d)

#     if st.checkbox("Remove redundant column"):
#         p = p.drop(['Games'], axis=1)
#         st.write(p)

#     if st.button("Final Dataset"):
#         st.write(p)

# if nav == 'Trends':
#     st.header('Trends')

#     if st.checkbox("Analyze the relationship between the Height and Weights of an athlete"):
#         graph = st.selectbox("What kind of Plot do you want?", ['Scatter Plot', 'Histogram'])
#         if graph == 'Histogram':
#             fig = px.histogram(p, x=p.Height, color=p.Weight)
#             st.write(fig)
#         if graph == 'Scatter Plot':
#             plt.scatter(p['Height'], p['Weight'])
#             plt.xlabel('Height')
#             plt.ylabel('Weight')
#             plt.title('Height Vs Weight')
#             st.set_option('deprecation.showPyplotGlobalUse', False)
#             st.pyplot()

#     if st.checkbox('Approximate Number of Males And Females Participated in the Olympics'):
#         p['Sex'].value_counts().plot.bar()
#         st.pyplot()

#     if st.checkbox("Determine the Participation trend in the Summer and Winter Seasons"):
#         fig = px.histogram(p, x=p.Season, color=p.Sex, barmode="group")
#         st.write(fig)

#     if st.checkbox('Women Participation over the years'):
#         y = p[p['Sex'] == 'F']
#         fig = px.histogram(y, x='Year')
#         st.write(fig)

#     if st.checkbox('Number of Medals Won by M and F'):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         fig = px.histogram(p, x=p.Sex, color=p.Medal)
#         st.write(fig)

#     if st.checkbox("Athletes with Most Medals"):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         df = pd.get_dummies(p['Medal']).drop([0], axis=1)
#         df['Name'] = p['Name']
#         df['Total'] = df[1] + df[2] + df[3]
#         f = df.groupby(df['Name'])['Total'].sum().sort_values(ascending=False).head(10)
#         x = pd.DataFrame(f)
#         st.write(x)

#     if st.checkbox("Countries with Most Medals"):
#         p['Medal'] = p.Medal.replace({'Gold': 1, 'Silver': 2, 'Bronze': 3}).fillna(0)
#         df = pd.get_dummies(p['Medal']).drop([0], axis=1)
#         df['Team'] = p['Team']
#         df['Total'] = df[1] + df[2] + df[3]
#         f = df.groupby(df['Team'])['Total'].sum().sort_values(ascending=False)
#         k = f.head(10)
#         k = pd.DataFrame(k.index.values)
#         st.write(k)

#     st.subheader("Find whether your country is in the Zero-Medal list?")
#     x = st.text_input('Enter')
#     if st.checkbox('Show'):
#         if x not in f.index.values:
#             st.write('Country not listed in the dataset')
#         else:
#             st.write('Medals:', f[x])

#     if st.checkbox("Countries winning the most Gold medals in a specific year"):
#         number = st.number_input('Insert the Leap Year', 1896.00, 2016.00, step=4.00)
#         max_year = int(number)
#         if st.button('Show'):
#             team_list = p[(p.Year == max_year) & (p.Medal == 'Gold')].Team
#             if len(team_list) != 0:
#                 sns.barplot(x=team_list.value_counts().head(),
#                             y=team_list.value_counts().head().index)
#                 st.pyplot()
#             else:
#                 st.write('Enter valid year')

# if nav == 'Prediction':
#     st.header('Prediction')

#     st.subheader('Predict the Weight of an athlete with his/her Height')
#     model = LinearRegression()
#     p['Height'] = p['Height'].fillna(p.Height.mean())
#     p['Weight'] = p['Weight'].fillna(p.Weight.mean())
#     x = np.array(p['Height']).reshape(-1, 1)
#     y = np.array(p['Weight']).reshape(-1, 1)
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
#     model.fit(x_train, y_train)
#     t = st.number_input('Enter the Height')
#     t = np.array(t).reshape(-1, 1)
#     d = model.predict(t)
#     if st.button('Predict Weight'):
#         st.write(d)

#     st.subheader('Predict the suitable Sport with the BMI values')
#     data = pd.read_csv('athlete_bmi_dataset.csv')
#     k = pd.DataFrame(data)

#     if st.checkbox("Show Athlete BMI Dataset"):
#         st.dataframe(k)
#         st.write("Note:")
#         q = {"Value": ['1', '2', '3', '4'],
#              "Corresponding Sport": ['Marathon', 'Basketball', 'Rugby', 'Shot Put']}
#         st.write(pd.DataFrame(q))

#     model1 = LinearRegression()
#     j = np.array(k['BMI']).reshape(-1, 1)
#     l = np.array(k['Sport']).reshape(-1, 1)
#     j_train, j_test, l_train, l_test = train_test_split(j, l, test_size=0.3)
#     model1.fit(j_train, l_train)
#     t = st.number_input('Enter BMI')
#     t = np.array(t).reshape(-1, 1)
#     d = model1.predict(t)
#     d = d * 10
#     d = np.round(d)

#     if st.button('Results'):
#         my_bar = st.progress(0)
#         for percent_complete in range(100):
#             time.sleep(0.001)
#             my_bar.progress(percent_complete + 1)

#         if d in range(0, 12):
#             st.write('Definitely Marathon')
#         elif d in range(12, 19):
#             st.write('Marathon, But also suitable for Basketball')
#         elif d in range(19, 23):
#             st.write('Definitely Basketball')
#         elif d in range(23, 27):
#             st.write('Basketball, But also suitable for Rugby')
#         elif d in range(27, 33):
#             st.write('Definitely Rugby')
#         elif d in range(33, 38):
#             st.write('Rugby, can also try shot put')
#         else:
#             st.write('Opt for Shot Put')

# elif nav == 'Stress':
#     st.header("🧠 Real-time Stress Monitoring")
#     st.write("Connect your Arduino with GSR sensor to monitor stress levels")
    
#     # Get available ports
#     available_ports = [port.device for port in serial.tools.list_ports.comports()]
    
#     if not available_ports:
#         st.warning("No serial ports found. Connect your Arduino and try again.")
#     else:
#         selected_port = st.selectbox("Select Arduino Port", available_ports)
        
#         if st.button("🚀 Start Stress Monitoring"):
#             try:
#                 ser = serial.Serial(selected_port, 9600, timeout=1)
#                 st.success(f"✅ Connected to {selected_port}")
                
#                 # Create placeholders
#                 gsr_placeholder = st.empty()
#                 stress_placeholder = st.empty()
#                 chart_placeholder = st.empty()
#                 raw_data_placeholder = st.empty()
                
#                 gsr_values = []
#                 timestamps = []
#                 start_time = time.time()
                
#                 # Monitoring loop
#                 while True:
#                     if ser.in_waiting > 0:
#                         line = ser.readline().decode('utf-8').strip()
#                         raw_data_placeholder.code(f"Raw: {line}")
                        
#                         # Process GSR data
#                         if line.startswith("GSR="):
#                             try:
#                                 gsr_value = int(line.split('=')[1].split()[0])
#                                 current_time = time.time() - start_time
                                
#                                 # Update data lists
#                                 gsr_values.append(gsr_value)
#                                 timestamps.append(current_time)
                                
#                                 # Update metrics
#                                 gsr_placeholder.metric("GSR Value", f"{gsr_value} µS")
                                
#                                 # Determine stress level
#                                 if gsr_value <= 100:
#                                     stress_level = "😊 Low Stress"
#                                     stress_color = "green"
#                                 elif gsr_value <= 200:
#                                     stress_level = "😐 Moderate Stress"
#                                     stress_color = "orange"
#                                 else:
#                                     stress_level = "😨 High Stress" 
#                                     stress_color = "red"
                                
#                                 stress_placeholder.metric("Stress Level", stress_level)
                                
#                                 # Update chart every 3 readings
#                                 if len(gsr_values) % 3 == 0:
#                                     chart_data = pd.DataFrame({
#                                         'Time (s)': timestamps,
#                                         'GSR (µS)': gsr_values
#                                     })
#                                     fig = px.line(chart_data, x='Time (s)', y='GSR (µS)', 
#                                                  title='Real-time Stress Monitoring',
#                                                  labels={'GSR (µS)': 'GSR Value (µS)'})
#                                     fig.update_layout(yaxis_range=[0, max(gsr_values)*1.2])
#                                     chart_placeholder.plotly_chart(fig)
                                
#                             except (IndexError, ValueError):
#                                 continue
                                
#             except serial.SerialException as e:
#                 st.error(f"❌ Connection failed: {str(e)}")
#                 st.info("Make sure:")
#                 st.info("1. Arduino is properly connected")
#                 st.info("2. No other program is using the serial port")
#                 st.info("3. Correct port is selected")
#             finally:
#                 if 'ser' in locals() and ser.is_open:
#                     ser.close()
#                     st.warning("🔌 Connection closed")





































import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import time
import serial
import serial.tools.list_ports

st.title("Olympics Dataset Analytics + Biometric Monitoring")

# Navigation sidebar
nav = st.sidebar.radio("Navigation", [
    'Home', 
    'Exploratory Data Analysis',
    'Data Preprocessing', 
    'Trends', 
    'Prediction', 
    'Biometric Monitoring'
])

# Home Page
if nav == 'Home':
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/640px-Olympic_rings_without_rims.svg.png", 
             width=800)
    st.write("""
    This app combines Olympic athlete data analytics with real-time biometric monitoring.
    - Explore historical athlete data
    - Predict athlete performance
    - Monitor real-time stress, heart rate, and oxygen levels
    """)

    if st.button('Load Main Dataset (Athlete Events)'):
        st.write('Athlete events dataset loaded successfully!')
        st.graphviz_chart('''
        digraph {
            Home -> ExploratoryDataAnalysis
            ExploratoryDataAnalysis -> DataPreprocessing
            DataPreprocessing -> Trends
            Trends -> Prediction
            DataPreprocessing -> Prediction
        }
        ''')

    if st.button('Load Athlete BMI Dataset'):
        st.write('BMI dataset loaded successfully for predictions!')
        st.graphviz_chart('''
        digraph {
            Home -> Prediction
        }
        ''')

# Load data
data = pd.read_csv('athlete_events.csv')
p = pd.DataFrame(data)

# Exploratory Data Analysis
if nav == 'Exploratory Data Analysis':
    st.header('Exploratory Data Analysis')
    
    # [Previous EDA code remains exactly the same]
    # ... (include all your existing EDA code here)

# Data Preprocessing
if nav == 'Data Preprocessing':
    st.header('Data Preprocessing')
    
    # [Previous preprocessing code remains exactly the same]
    # ... (include all your existing preprocessing code here)

# Trends
if nav == 'Trends':
    st.header('Trends Analysis')
    
    # [Previous trends code remains exactly the same]
    # ... (include all your existing trends code here)

# Prediction
if nav == 'Prediction':
    st.header('Performance Prediction')
    
    # [Previous prediction code remains exactly the same]
    # ... (include all your existing prediction code here)

# Biometric Monitoring - Updated Version
elif nav == 'Biometric Monitoring':
    st.header("🏥 Real-Time Athlete Biometric Monitoring")
    st.write("""
    Monitor athletes' physiological data in real-time:
    - GSR (Stress Levels)
    - Heart Rate (Pulse)
    - Blood Oxygen Saturation (SpO₂)
    """)
    
    # Port selection
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    
    if not available_ports:
        st.warning("No serial ports detected. Please connect your Arduino.")
    else:
        selected_port = st.selectbox("Select Arduino Port", available_ports)
        
        if st.button("▶ Start Real-Time Monitoring"):
            try:
                ser = serial.Serial(selected_port, 9600, timeout=1)
                st.success(f"🔗 Connected to {selected_port}")
                
                # Create layout
                col1, col2, col3 = st.columns(3)
                gsr_placeholder = col1.empty()
                pulse_placeholder = col2.empty()
                o2_placeholder = col3.empty()
                
                status_placeholder = st.empty()
                chart_placeholder = st.empty()
                raw_data_expander = st.expander("View Raw Serial Data")
                
                # Data storage
                metrics = {
                    'Time': [],
                    'GSR': [],
                    'Pulse': [],
                    'Oxygen': []
                }
                
                start_time = time.time()
                
                # Monitoring loop
                while True:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        raw_data_expander.write(line)
                        
                        # Process GSR data
                        if line.startswith("GSR="):
                            try:
                                gsr_value = int(line.split('=')[1].split()[0])
                                metrics['GSR'].append(gsr_value)
                                metrics['Time'].append(time.time() - start_time)
                                
                                # Update display
                                gsr_placeholder.metric(
                                    "GSR (µS)", 
                                    f"{gsr_value}",
                                    help="Galvanic Skin Response - Higher values indicate more stress"
                                )
                                
                                # Classify stress
                                if gsr_value <= 100:
                                    status_placeholder.success("😊 Low Stress")
                                elif gsr_value <= 200:
                                    status_placeholder.warning("😐 Moderate Stress")
                                else:
                                    status_placeholder.error("😨 High Stress")
                                    
                            except Exception as e:
                                st.warning(f"GSR parsing error: {str(e)}")
                        
                        # Process Pulse data
                        elif line.startswith("Pulse:"):
                            try:
                                pulse_value = int(line.split(':')[1])
                                metrics['Pulse'].append(pulse_value)
                                pulse_placeholder.metric(
                                    "Heart Rate", 
                                    f"{pulse_value} BPM",
                                    help="Beats per minute - Normal range: 60-100 BPM"
                                )
                            except:
                                continue
                        
                        # Process O2 data
                        elif line.startswith("O2:"):
                            try:
                                o2_value = float(line.split(':')[1].replace('%',''))
                                metrics['Oxygen'].append(o2_value)
                                o2_placeholder.metric(
                                    "SpO₂", 
                                    f"{o2_value}%",
                                    help="Blood oxygen saturation - Normal range: 95-100%"
                                )
                            except:
                                continue
                        
                        # Update chart periodically
                        if len(metrics['Time']) % 5 == 0 and len(metrics['Time']) > 10:
                            # Create DataFrame from the collected metrics
                            df = pd.DataFrame({
                                'Time': metrics['Time'],
                                'GSR': metrics['GSR'],
                                'Pulse': metrics['Pulse'][:len(metrics['Time'])],
                                'Oxygen': metrics['Oxygen'][:len(metrics['Time'])]
                            })
                            
                            # Create interactive plot
                            fig = px.line(
                                df, 
                                x='Time', 
                                y=['GSR', 'Pulse', 'Oxygen'],
                                title='Real-Time Biometric Trends',
                                labels={'value': 'Measurement', 'variable': 'Metric'},
                                color_discrete_sequence=['blue', 'red', 'green']
                            )
                            
                            # Configure plot appearance
                            fig.update_layout(
                                yaxis_range=[0, max(
                                    max(metrics['GSR']) * 1.2 if metrics['GSR'] else 100,
                                    max(metrics['Pulse']) * 1.2 if metrics['Pulse'] else 100,
                                    100  # Max for Oxygen
                                )],
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ),
                                hovermode="x unified"
                            )
                            
                            # Customize lines
                            fig.update_traces(
                                line=dict(width=2),
                                selector=dict(name='GSR')
                            )
                            fig.update_traces(
                                line=dict(width=2.5),
                                selector=dict(name='Pulse')
                            )
                            
                            chart_placeholder.plotly_chart(fig, use_container_width=True)
                
            except serial.SerialException as e:
                st.error(f"❌ Connection Error: {str(e)}")
                st.info("""
                **Troubleshooting Tips:**
                1. Ensure Arduino is properly connected
                2. Close any other programs using the serial port
                3. Try a different USB port
                4. Restart the Arduino
                """)
            
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
            
            finally:
                if 'ser' in locals() and ser.is_open:
                    ser.close()
                    st.warning("🔌 Disconnected from Arduino")
                    if len(metrics['Time']) > 0:
                        st.download_button(
                            "📥 Download Biometric Data",
                            pd.DataFrame(metrics).to_csv(index=False),
                            "biometric_data.csv",
                            "text/csv"
                        )  












