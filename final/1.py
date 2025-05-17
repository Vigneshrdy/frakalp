import streamlit as st
import pandas as pd
import numpy as np
import time
import serial
import serial.tools.list_ports
from datetime import datetime
import plotly.express as px
import qrcode
from io import BytesIO
import base64

# Configure page
st.set_page_config(
    page_title="Health Biometric Dashboard",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .st-emotion-cache-1v0mbdj {
        border-radius: 10px;
    }
    .session-info {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .highlight-box {
        background-color: #fffacd;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .bmi-result {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .underweight { color: #3498db; }
    .normal { color: #2ecc71; }
    .overweight { color: #f39c12; }
    .obese { color: #e74c3c; }
    .qr-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px 0;
    }
    .user-table {
        width: 100%;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Health Biometric Monitoring")

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Navigation sidebar
nav = st.sidebar.radio("**Navigation**", [
    '🏠 Home', 
    '💓 Stress-O2-Pulse Monitoring',
    '⚖️ BMI Calculator'
])

# Home Page
if nav == '🏠 Home':
    st.write("""
        ## Intelligent Health & Biometric Monitoring Platform
**Gain meaningful insights into your health with smart tracking tools:**
- Track your Body Mass Index (BMI) over time with easy-to-read visuals  
- Compare BMI across age, gender, and lifestyle patterns  
- Connect wearable devices for automatic, real-time data  

**Stay informed with key biometric monitoring:**
- Detect stress levels through skin response (GSR)  
- Monitor blood oxygen (SpO₂) and heart rate in real time  
- Get alerts when your health metrics go outside normal ranges  
    """)

# BMI Calculator Page
elif nav == '⚖️ BMI Calculator':
    st.header("⚖️ BMI Calculator & Health Recommendation")
    
    # Initialize session state for multiple users
    if 'bmi_users' not in st.session_state:
        st.session_state.bmi_users = []
    
    # User Information Section
    with st.expander("🧑 Add New User Information", expanded=True):
        with st.form("bmi_form"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Full Name", placeholder="e.g., John Smith", key="bmi_name")
                age = st.number_input("Age", min_value=12, max_value=80, value=25, key="bmi_age")
                gender = st.radio("Gender", ["Male", "Female", "Other"], key="bmi_gender")
            with cols[1]:
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, key="bmi_height")
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, key="bmi_weight")
                
            if st.form_submit_button("📊 Add User Data"):
                user_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.bmi_users.append(user_data)
                st.success("User data added successfully!")
    
    # Display all users and their BMI data
    if st.session_state.bmi_users:
        st.markdown("### All User BMI Data")
        
        # Calculate BMI for all users
        for i, user in enumerate(st.session_state.bmi_users):
            bmi = user['weight'] / ((user['height']/100) ** 2)
            
            # BMI Categories
            if bmi < 18.5:
                category = "Underweight"
                category_class = "underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
                category_class = "normal"
            elif 25 <= bmi < 30:
                category = "Overweight"
                category_class = "overweight"
            else:
                category = "Obese"
                category_class = "obese"
            
            # Display results for each user
            with st.expander(f"User {i+1}: {user['name']}", expanded=False):
                st.markdown(f"""
                <div class="metric-card" style="
                    background: linear-gradient(145deg, #ff7e5f, #feb47b);
                    border-left: 5px solid #ff4d1c;
                    color: #2d3436;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                ">
                    <h2 style="color: #2d3436; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);">BMI Results</h2>
                    <div class="bmi-result {category_class}" style="font-size: 26px; font-weight: 800; margin: 15px 0;">
                        {bmi:.1f} - {category}
                    </div>
                    <table style="color: #2d3436; font-weight: 500;">
                        <tr><td><strong>Name:</strong></td><td>{user['name']}</td></tr>
                        <tr><td><strong>Age:</strong></td><td>{user['age']}</td></tr>
                        <tr><td><strong>Gender:</strong></td><td>{user['gender']}</td></tr>
                        <tr><td><strong>Height:</strong></td><td>{user['height']} cm</td></tr>
                        <tr><td><strong>Weight:</strong></td><td>{user['weight']} kg</td></tr>
                        <tr><td><strong>Recorded:</strong></td><td>{user['timestamp']}</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # Download button for individual user
                user_df = pd.DataFrame([user])
                csv_data = user_df.to_csv(index=False)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label=f"💾 Download {user['name']}'s Data",
                        data=csv_data,
                        file_name=f"{user['name']}_bmi_data.csv",
                        mime="text/csv",
                        key=f"download_{i}"
                    )
                
                with col2:
                    # Generate QR code for download
                    qr_data = f"data:text/csv;base64,{base64.b64encode(csv_data.encode()).decode()}"
                    qr_img = generate_qr_code(qr_data)
                    
                    st.markdown("""
                    <div class="qr-container">
                        <h4>Scan to download</h4>
                        <img src="data:image/png;base64,{qr_img}" width="150">
                    </div>
                    """.format(qr_img=qr_img), unsafe_allow_html=True)
        
        # Download all users data
        st.markdown("### Download All Users Data")
        all_users_df = pd.DataFrame(st.session_state.bmi_users)
        all_csv_data = all_users_df.to_csv(index=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="💾 Download All Users Data",
                data=all_csv_data,
                file_name="all_users_bmi_data.csv",
                mime="text/csv"
            )
        
        with col2:
            # Generate QR code for all users download
            qr_data_all = f"data:text/csv;base64,{base64.b64encode(all_csv_data.encode()).decode()}"
            qr_img_all = generate_qr_code(qr_data_all)
            
            st.markdown("""
            <div class="qr-container">
                <h4>Scan to download all</h4>
                <img src="data:image/png;base64,{qr_img_all}" width="150">
            </div>
            """.format(qr_img_all=qr_img_all), unsafe_allow_html=True)
        
        # Clear all data button
        if st.button("🧹 Clear All User Data"):
            st.session_state.bmi_users = []
            st.experimental_rerun()
    
    else:
        st.info("Please add user information using the form above")

# Biometric Monitoring Page
elif nav == '💓 Stress-O2-Pulse Monitoring':
    st.header("🏥 Real-Time Biometric Monitoring")
    st.write("""
    Monitor physiological data in real-time:
    - GSR (Stress Levels)
    - Heart Rate (Pulse)
    - Blood Oxygen Saturation (SpO₂)
    """)
    
    # Initialize session state for monitoring control
    if 'monitoring_active' not in st.session_state:
        st.session_state.monitoring_active = False
    if 'serial_conn' not in st.session_state:
        st.session_state.serial_conn = None
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {
            'Time': [],
            'GSR': [],
            'Pulse': [],
            'Oxygen': []
        }
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {
            'name': '',
            'session_start': ''
        }
    
    # User information form
    with st.expander("🧑 Enter User Information", expanded=True):
        user_name = st.text_input("Name for this session", key="stress_user_name")
        if st.button("💾 Save User Info"):
            st.session_state.user_info = {
                'name': user_name,
                'session_start': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("User information saved!")
    
    if st.session_state.user_info['name']:
        st.markdown(f"""
        <div class="session-info">
            <h4>Current Session</h4>
            <table>
                <tr><td><strong>User:</strong></td><td>{st.session_state.user_info['name']}</td></tr>
                <tr><td><strong>Started:</strong></td><td>{st.session_state.user_info['session_start']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    # Port selection
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    
    if not available_ports:
        st.warning("No serial ports detected. Please connect your Arduino.")
    else:
        selected_port = st.selectbox("Select Arduino Port", available_ports)
        
        # Create layout elements
        col1, col2, col3 = st.columns(3)
        gsr_placeholder = col1.empty()
        pulse_placeholder = col2.empty()
        o2_placeholder = col3.empty()
        
        status_placeholder = st.empty()
        chart_placeholder = st.empty()
        raw_data_expander = st.expander("View Raw Serial Data")
        raw_data_placeholder = raw_data_expander.empty()
        
        # Start/Stop buttons
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.monitoring_active:
                if st.button("▶ Start Real-Time Monitoring"):
                    try:
                        st.session_state.serial_conn = serial.Serial(selected_port, 9600, timeout=1)
                        st.session_state.monitoring_active = True
                        st.session_state.start_time = time.time()
                        st.session_state.metrics = {
                            'Time': [],
                            'GSR': [],
                            'Pulse': [],
                            'Oxygen': []
                        }
                        st.success(f"🔗 Connected to {selected_port}")
                    except serial.SerialException as e:
                        st.error(f"❌ Connection Error: {str(e)}")
            else:
                if st.button("⏹ Stop Monitoring"):
                    st.session_state.monitoring_active = False
                    if st.session_state.serial_conn and st.session_state.serial_conn.is_open:
                        st.session_state.serial_conn.close()
                    st.warning("🔌 Monitoring stopped")
        
        # Monitoring loop (only when active)
        if st.session_state.monitoring_active and st.session_state.serial_conn:
            try:
                if st.session_state.serial_conn.in_waiting > 0:
                    line = st.session_state.serial_conn.readline().decode('utf-8').strip()
                    raw_data_placeholder.text(line)
                    
                    # Process GSR data
                    if line.startswith("GSR="):
                        try:
                            gsr_value = int(line.split('=')[1].split()[0])
                            st.session_state.metrics['GSR'].append(gsr_value)
                            st.session_state.metrics['Time'].append(time.time() - st.session_state.start_time)
                            
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
                            st.session_state.metrics['Pulse'].append(pulse_value)
                            pulse_placeholder.metric(
                                "Heart Rate", 
                                f"{pulse_value} BPM",
                                help="Beats per minute - Normal range: 60-100 BPM"
                            )
                        except:
                            pass
                    
                    # Process O2 data
                    elif line.startswith("O2:"):
                        try:
                            o2_value = float(line.split(':')[1].replace('%',''))
                            st.session_state.metrics['Oxygen'].append(o2_value)
                            o2_placeholder.metric(
                                "SpO₂", 
                                f"{o2_value}%",
                                help="Blood oxygen saturation - Normal range: 95-100%"
                            )
                        except:
                            pass
                    
                    # Update chart periodically
                    if len(st.session_state.metrics['Time']) > 1 and len(st.session_state.metrics['Time']) % 5 == 0:
                        # Create DataFrame from the collected metrics
                        df = pd.DataFrame({
                            'Time': st.session_state.metrics['Time'],
                            'GSR': st.session_state.metrics['GSR'],
                            'Pulse': st.session_state.metrics['Pulse'][:len(st.session_state.metrics['Time'])],
                            'Oxygen': st.session_state.metrics['Oxygen'][:len(st.session_state.metrics['Time'])]
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
                                max(st.session_state.metrics['GSR']) * 1.2 if st.session_state.metrics['GSR'] else 100,
                                max(st.session_state.metrics['Pulse']) * 1.2 if st.session_state.metrics['Pulse'] else 100,
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
                        
                        chart_placeholder.plotly_chart(fig, use_container_width=True)
                
            except serial.SerialException as e:
                st.error(f"❌ Connection lost: {str(e)}")
                st.session_state.monitoring_active = False
                if st.session_state.serial_conn and st.session_state.serial_conn.is_open:
                    st.session_state.serial_conn.close()
        
        # Data download after stopping
        if not st.session_state.monitoring_active and len(st.session_state.metrics['Time']) > 0:
            # Create DataFrame with user info and metrics
            df = pd.DataFrame(st.session_state.metrics)
            df['User'] = st.session_state.user_info['name']
            df['Session Start'] = st.session_state.user_info['session_start']
            df['Session End'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            csv_data = df.to_csv(index=False)
            filename = f"{st.session_state.user_info['name']}_biometric_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Biometric Data",
                    csv_data,
                    filename,
                    "text/csv"
                )
            
            with col2:
                # Generate QR code for download
                qr_data = f"data:text/csv;base64,{base64.b64encode(csv_data.encode()).decode()}"
                qr_img = generate_qr_code(qr_data)
                
                st.markdown("""
                <div class="qr-container">
                    <h4>Scan to download</h4>
                    <img src="data:image/png;base64,{qr_img}" width="150">
                </div>
                """.format(qr_img=qr_img), unsafe_allow_html=True)
            
            # Option to clear data
            if st.button("🧹 Clear Collected Data"):
                st.session_state.metrics = {
                    'Time': [],
                    'GSR': [],
                    'Pulse': [],
                    'Oxygen': []
                }