import streamlit as st
import pandas as pd
import numpy as np
import time
import serial
import serial.tools.list_ports
from datetime import datetime
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="Health & Biometric Dashboard",
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
</style>
""", unsafe_allow_html=True)

st.title("Health & Biometric Monitoring")

# Navigation sidebar
nav = st.sidebar.radio("**Navigation**", [
    '🏠 Home', 
    '💓 Biometric Stress Detection',
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

# Biometric Stress Detection Page
elif nav == '💓 Biometric Stress Detection':
    st.header("💓 Biometric Stress Detection")
    
    # User Information Section
    with st.expander("🧑 User Information", expanded=True):
        with st.form("user_form"):
            cols = st.columns(3)
            with cols[0]:
                name = st.text_input("Full Name", placeholder="e.g., John Smith")
            with cols[1]:
                age = st.number_input("Age", min_value=12, max_value=80, value=25)
            with cols[2]:
                gender = st.radio("Gender", ["Male", "Female", "Other"])
            
            if st.form_submit_button("💾 Save User Info"):
                st.session_state.user = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.success("User information saved!")

    # Display saved user info
    if 'user' in st.session_state:
        st.markdown(f"""
        <div class="session-info">
            <h4>Current Session</h4>
            <table>
                <tr><td><strong>User:</strong></td><td>{st.session_state.user['name']}</td></tr>
                <tr><td><strong>Age:</strong></td><td>{st.session_state.user['age']}</td></tr>
                <tr><td><strong>Gender:</strong></td><td>{st.session_state.user['gender']}</td></tr>
                <tr><td><strong>Started:</strong></td><td>{st.session_state.user['timestamp']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter user information before starting monitoring")
        st.stop()

    # Biometric Monitoring Section
    st.subheader("📊 Real-Time Stress Monitoring")
    
    # Device Connection
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        st.error("No serial devices detected. Please connect your sensor device.")
        st.stop()
    
    port = st.selectbox("Select Device Port", ports)
    
    if st.button("▶ Start Monitoring Session", type="primary"):
        try:
            # Initialize connection
            ser = serial.Serial(port, 9600, timeout=1)
            st.session_state.ser = ser
            st.success(f"Connected to {port}")
            
            # Initialize data storage
            if 'biometrics' not in st.session_state:
                st.session_state.biometrics = {
                    'time': [],
                    'gsr': [],
                    'pulse': [],
                    'oxygen': [],
                    'raw_data': []
                }
            
            # Create real-time display
            st.divider()
            
            # Metrics display
            col1, col2, col3 = st.columns(3)
            with col1:
                gsr_card = st.empty()
            with col2:
                pulse_card = st.empty()
            with col3:
                oxygen_card = st.empty()
            
            status_card = st.empty()
            chart = st.empty()
            raw_data_expander = st.expander("📝 Raw Device Data")
            raw_data_container = raw_data_expander.empty()
            
            # Monitoring loop
            start_time = time.time()
            baseline_duration = 5  # 5 seconds for baseline
            reading_duration = 10   # 10 seconds for readings
            total_duration = baseline_duration + reading_duration
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Baseline phase
            status_text.text("🔵 Baseline measurement in progress (5 seconds)...")
            baseline_start = time.time()
            baseline_values = {'gsr': [], 'pulse': [], 'oxygen': []}
            raw_data_list = []
            
            while time.time() < baseline_start + baseline_duration:
                # Update progress
                elapsed = time.time() - start_time
                progress = min(elapsed / total_duration, 1.0)
                progress_bar.progress(progress)
                
                # Read serial data for baseline
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    raw_data_list.append(line)
                    st.session_state.biometrics['raw_data'].append(line)
                    
                    # Process different metrics for baseline
                    if line.startswith("GSR="):
                        try:
                            gsr = int(line.split('=')[1].split()[0])
                            baseline_values['gsr'].append(gsr)
                        except:
                            continue
                    
                    elif line.startswith("Pulse:"):
                        try:
                            pulse = int(line.split(':')[1])
                            baseline_values['pulse'].append(pulse)
                        except:
                            continue
                    
                    elif line.startswith("O2:"):
                        try:
                            oxygen = float(line.split(':')[1].replace('%', ''))
                            baseline_values['oxygen'].append(oxygen)
                        except:
                            continue
                
                # Update raw data display
                raw_data_container.text("\n".join(raw_data_list[-20:]))  # Show last 20 lines
                time.sleep(0.1)
            
            # Calculate baseline averages
            baseline_gsr = np.mean(baseline_values['gsr']) if baseline_values['gsr'] else 0
            baseline_pulse = np.mean(baseline_values['pulse']) if baseline_values['pulse'] else 0
            baseline_oxygen = np.mean(baseline_values['oxygen']) if baseline_values['oxygen'] else 0
            
            # Reading phase
            status_text.text("🔴 Active monitoring in progress (10 seconds)...")
            reading_start = time.time()
            
            while time.time() < reading_start + reading_duration:
                # Update progress
                elapsed = time.time() - start_time
                progress = min(elapsed / total_duration, 1.0)
                progress_bar.progress(progress)
                remaining = max(0, total_duration - elapsed)
                status_text.text(f"Time remaining: {int(remaining)} seconds")
                
                # Read serial data
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    raw_data_list.append(line)
                    st.session_state.biometrics['raw_data'].append(line)
                    
                    # Process different metrics
                    if line.startswith("GSR="):
                        try:
                            gsr = int(line.split('=')[1].split()[0])
                            st.session_state.biometrics['gsr'].append(gsr)
                            st.session_state.biometrics['time'].append(elapsed)
                            
                            with gsr_card.container():
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>GSR (Stress)</h3>
                                    <h1>{gsr} µS</h1>
                                    <p>Baseline: {baseline_gsr:.1f} µS</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Stress assessment
                                if abs(gsr - baseline_gsr) < 50:
                                    status_card.success("😊 Normal Stress Levels")
                                elif abs(gsr - baseline_gsr) < 150:
                                    status_card.warning("😐 Elevated Stress")
                                else:
                                    status_card.error("😨 High Stress Alert")
                        
                        except:
                            continue
                    
                    elif line.startswith("Pulse:"):
                        try:
                            pulse = int(line.split(':')[1])
                            st.session_state.biometrics['pulse'].append(pulse)
                            
                            with pulse_card.container():
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>Heart Rate</h3>
                                    <h1>{pulse} BPM</h1>
                                    <p>Baseline: {baseline_pulse:.1f} BPM</p>
                                </div>
                                """, unsafe_allow_html=True)
                        except:
                            continue
                    
                    elif line.startswith("O2:"):
                        try:
                            oxygen = float(line.split(':')[1].replace('%', ''))
                            st.session_state.biometrics['oxygen'].append(oxygen)
                            
                            with oxygen_card.container():
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>Oxygen Saturation</h3>
                                    <h1>{oxygen}%</h1>
                                    <p>Baseline: {baseline_oxygen:.1f}%</p>
                                </div>
                                """, unsafe_allow_html=True)
                        except:
                            continue
                
                # Update raw data display
                raw_data_container.text("\n".join(raw_data_list[-20:]))
                
                # Update chart every 2 seconds
                if len(st.session_state.biometrics['time']) > 1 and time.time() % 2 < 0.1:
                    df = pd.DataFrame({
                        'Time': st.session_state.biometrics['time'],
                        'GSR': st.session_state.biometrics['gsr'],
                        'Pulse': st.session_state.biometrics['pulse'][:len(st.session_state.biometrics['time'])],
                        'Oxygen': st.session_state.biometrics['oxygen'][:len(st.session_state.biometrics['time'])]
                    })
                    
                    fig = px.line(df, x='Time', y=['GSR', 'Pulse', 'Oxygen'],
                                title='Real-Time Biometrics',
                                labels={'value': 'Measurement', 'variable': 'Metric'},
                                color_discrete_map={
                                    'GSR': '#1f77b4',
                                    'Pulse': '#ff7f0e', 
                                    'Oxygen': '#2ca02c'
                                })
                    
                    # Add baseline reference lines
                    fig.add_hline(y=baseline_gsr, line_dash="dot", line_color="#1f77b4", 
                                  annotation_text=f"GSR Baseline: {baseline_gsr:.1f}", 
                                  annotation_position="bottom right")
                    fig.add_hline(y=baseline_pulse, line_dash="dot", line_color="#ff7f0e", 
                                  annotation_text=f"Pulse Baseline: {baseline_pulse:.1f}")
                    fig.add_hline(y=baseline_oxygen, line_dash="dot", line_color="#2ca02c", 
                                  annotation_text=f"O2 Baseline: {baseline_oxygen:.1f}")
                    
                    fig.update_layout(
                        yaxis_range=[0, max(
                            max(st.session_state.biometrics['gsr'] + [100]),
                            max(st.session_state.biometrics['pulse'] + [100]),
                            100
                        )],
                        legend=dict(orientation="h", y=1.1),
                        hovermode="x unified"
                    )
                    
                    chart.plotly_chart(fig, use_container_width=True)
                
                time.sleep(0.1)
            
            # Session complete
            st.balloons()
            st.success("Monitoring session completed!")
            
            # Calculate summary statistics
            final_gsr = st.session_state.biometrics['gsr'][-1] if st.session_state.biometrics['gsr'] else 0
            final_pulse = st.session_state.biometrics['pulse'][-1] if st.session_state.biometrics['pulse'] else 0
            final_oxygen = st.session_state.biometrics['oxygen'][-1] if st.session_state.biometrics['oxygen'] else 0
            
            # Display summary in a highlight box
            st.markdown(f"""
            <div class="highlight-box">
                <h3>📋 Session Summary</h3>
                <table>
                    <tr><td><strong>Final GSR (Stress):</strong></td><td>{final_gsr} µS (Baseline: {baseline_gsr:.1f} µS)</td></tr>
                    <tr><td><strong>Final Pulse:</strong></td><td>{final_pulse} BPM (Baseline: {baseline_pulse:.1f} BPM)</td></tr>
                    <tr><td><strong>Final Oxygen:</strong></td><td>{final_oxygen}% (Baseline: {baseline_oxygen:.1f}%)</td></tr>
                    <tr><td><strong>Duration:</strong></td><td>{total_duration} seconds</td></tr>
                    <tr><td><strong>Data Points:</strong></td><td>{len(st.session_state.biometrics['time'])} readings</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Prepare data for download
            session_data = pd.DataFrame({
                'User': [st.session_state.user['name']] * len(st.session_state.biometrics['time']),
                'Age': [st.session_state.user['age']] * len(st.session_state.biometrics['time']),
                'Gender': [st.session_state.user['gender']] * len(st.session_state.biometrics['time']),
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(st.session_state.biometrics['time']),
                'Time_Elapsed': st.session_state.biometrics['time'],
                'GSR_Stress': st.session_state.biometrics['gsr'],
                'Heart_Rate': st.session_state.biometrics['pulse'],
                'Oxygen_Saturation': st.session_state.biometrics['oxygen'],
                'Baseline_GSR': [baseline_gsr] * len(st.session_state.biometrics['time']),
                'Baseline_Heart_Rate': [baseline_pulse] * len(st.session_state.biometrics['time']),
                'Baseline_Oxygen': [baseline_oxygen] * len(st.session_state.biometrics['time'])
            })
            
            # Create a second DataFrame for raw data
            raw_data_df = pd.DataFrame({
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(st.session_state.biometrics['raw_data']),
                'Raw_Data': st.session_state.biometrics['raw_data']
            })
            
            # Create a summary DataFrame
            summary_df = pd.DataFrame({
                'Metric': ['GSR (Stress)', 'Heart Rate', 'Oxygen Saturation'],
                'Baseline': [baseline_gsr, baseline_pulse, baseline_oxygen],
                'Final_Reading': [final_gsr, final_pulse, final_oxygen],
                'Change': [final_gsr - baseline_gsr, final_pulse - baseline_pulse, final_oxygen - baseline_oxygen],
                'Percent_Change': [
                    ((final_gsr - baseline_gsr)/baseline_gsr)*100 if baseline_gsr != 0 else 0,
                    ((final_pulse - baseline_pulse)/baseline_pulse)*100 if baseline_pulse != 0 else 0,
                    ((final_oxygen - baseline_oxygen)/baseline_oxygen)*100 if baseline_oxygen != 0 else 0
                ]
            })
            
            # Create download buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "💾 Download Processed Data (CSV)",
                    session_data.to_csv(index=False),
                    f"stress_biometrics_{st.session_state.user['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            with col2:
                st.download_button(
                    "📋 Download Raw Data (CSV)",
                    raw_data_df.to_csv(index=False),
                    f"raw_biometrics_{st.session_state.user['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            with col3:
                st.download_button(
                    "📊 Download Summary Report (CSV)",
                    summary_df.to_csv(index=False),
                    f"stress_summary_{st.session_state.user['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        finally:
            if 'ser' in st.session_state:
                st.session_state.ser.close()
                del st.session_state.ser
                st.warning("Disconnected from device")

# BMI Calculator Page
elif nav == '⚖️ BMI Calculator':
    st.header("⚖️ BMI Calculator & Health Recommendation")
    
    # User Information Section
    with st.expander("🧑 User Information", expanded=True):
        with st.form("bmi_form"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Full Name", placeholder="e.g., Jane Doe", key="bmi_name")
                age = st.number_input("Age", min_value=12, max_value=80, value=25, key="bmi_age")
                gender = st.radio("Gender", ["Male", "Female", "Other"], key="bmi_gender")
            with cols[1]:
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, key="bmi_height")
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, key="bmi_weight")
                
            if st.form_submit_button("📊 Calculate BMI"):
                st.session_state.bmi_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
    
    # Calculate and display BMI if data is available
    if 'bmi_data' in st.session_state:
        user = st.session_state.bmi_data
        bmi = user['weight'] / ((user['height']/100) ** 2)
        st.session_state.bmi_data['bmi'] = bmi
        
        # BMI Categories
        if bmi < 18.5:
            category = "Underweight"
            category_class = "underweight"
            recommended_sports = ["Gymnastics", "Diving", "Figure Skating", "Long-distance running"]
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            category_class = "normal"
            recommended_sports = ["Swimming", "Tennis", "Volleyball", "Basketball", "Soccer"]
        elif 25 <= bmi < 30:
            category = "Overweight"
            category_class = "overweight"
            recommended_sports = ["Weightlifting", "Rowing", "Rugby", "Judo", "Shot put"]
        else:
            category = "Obese"
            category_class = "obese"
            recommended_sports = ["Super Heavyweight Boxing", "Powerlifting", "Sumo wrestling"]
        
        st.session_state.bmi_data['category'] = category
        st.session_state.bmi_data['recommended_sports'] = ", ".join(recommended_sports)
        
        # Display results
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
            <tr><td><strong>Height:</strong></td><td>{user['height']} cm</td></tr>
            <tr><td><strong>Weight:</strong></td><td>{user['weight']} kg</td></tr>
            <tr><td><strong>Recommended Activities:</strong></td><td style="font-weight: 600;">{", ".join(recommended_sports)}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
        
        # BMI Categories card with completely different color scheme
        st.markdown(f"""
    <div class="metric-card" style="
        background: linear-gradient(145deg, #a1c4fd, #c2e9fb);
        border-left: 5px solid #4a90e2;
        color: #1a237e;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    ">
        <h3 style="color: #1a237e; border-bottom: 2px solid rgba(26,35,126,0.2); padding-bottom: 8px;">BMI Categories</h3>
        <ul style="color: #0d47a1; font-weight: 500;">
            <li><span class="underweight" style="color: #3498db; font-weight: 600;">Underweight</span>: BMI < 18.5</li>
            <li><span class="normal" style="color: #2ecc71; font-weight: 600;">Normal weight</span>: BMI 18.5–24.9</li>
            <li><span class="overweight" style="color: #f39c12; font-weight: 600;">Overweight</span>: BMI 25–29.9</li>
            <li><span class="obese" style="color: #e74c3c; font-weight: 600;">Obese</span>: BMI ≥ 30</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
        
        # Add stress data if available
        if 'biometrics' in st.session_state:
            avg_gsr = np.mean(st.session_state.biometrics['gsr']) if st.session_state.biometrics['gsr'] else None
            avg_pulse = np.mean(st.session_state.biometrics['pulse']) if st.session_state.biometrics['pulse'] else None
            avg_oxygen = np.mean(st.session_state.biometrics['oxygen']) if st.session_state.biometrics['oxygen'] else None
            
            st.session_state.bmi_data['avg_gsr'] = avg_gsr
            st.session_state.bmi_data['avg_pulse'] = avg_pulse
            st.session_state.bmi_data['avg_oxygen'] = avg_oxygen
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>Biometric Data (from Stress Monitoring)</h3>
                <table>
                    <tr><td><strong>Average GSR (Stress):</strong></td><td>{avg_gsr:.1f} µS</td></tr>
                    <tr><td><strong>Average Pulse:</strong></td><td>{avg_pulse:.1f} BPM</td></tr>
                    <tr><td><strong>Average Oxygen:</strong></td><td>{avg_oxygen:.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        # Save to CSV button
        st.markdown("### Save Results")
        st.write("Download your BMI data including any available biometric measurements:")
        
        # Create DataFrame
        df = pd.DataFrame([st.session_state.bmi_data])
        
        # Download CSV
        st.download_button(
            label="💾 Download BMI Data (CSV)",
            data=df.to_csv(index=False),
            file_name=f"{user['name']}.csv",
            mime="text/csv"
        )
        
        # Also show the data
        with st.expander("View Data to be Saved"):
            st.dataframe(df)
    
    else:
        st.info("Please enter your information and click 'Calculate BMI' to see results")