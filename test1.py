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
    page_title="Olympic Analytics Dashboard",
    page_icon="🏅",
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
</style>
""", unsafe_allow_html=True)

st.title("🏅 Olympic Analytics + Biometric Monitoring")

# Navigation sidebar
nav = st.sidebar.radio("**Navigation**", [
    '🏠 Home', 
    '💓 Stress-O2-Pulse Monitoring'
])



# Home Page
if nav == '🏠 Home':
    # col1= st.columns([1])
    
    # with col1:
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
    
    
    
    
    
# Biometric Monitoring Page
elif nav == '💓 Stress-O2-Pulse Monitoring':
    st.header("💓 Athlete Biometric Monitoring")
    
    # Athlete Information Section
    with st.expander("🧑 Athlete Information", expanded=True):
        with st.form("athlete_form"):
            cols = st.columns(3)
            with cols[0]:
                name = st.text_input("Full Name", placeholder="e.g., Michael Phelps")
            with cols[1]:
                age = st.number_input("Age", min_value=12, max_value=80, value=25)
            with cols[2]:
                gender = st.radio("Gender", ["Male", "Female", "Other"])
            
            if st.form_submit_button("💾 Save Athlete Info"):
                st.session_state.athlete = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.success("Athlete information saved!")

    # Display saved athlete info
    if 'athlete' in st.session_state:
        st.markdown(f"""
        <div class="session-info">
            <h4>Current Session</h4>
            <table>
                <tr><td><strong>Athlete:</strong></td><td>{st.session_state.athlete['name']}</td></tr>
                <tr><td><strong>Age:</strong></td><td>{st.session_state.athlete['age']}</td></tr>
                <tr><td><strong>Gender:</strong></td><td>{st.session_state.athlete['gender']}</td></tr>
                <tr><td><strong>Started:</strong></td><td>{st.session_state.athlete['timestamp']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter athlete information before starting monitoring")
        st.stop()

    # Biometric Monitoring Section
    st.subheader("📊 Real-Time Monitoring")
    
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
                                    <h3>GSR</h3>
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
                    <tr><td><strong>Final GSR:</strong></td><td>{final_gsr} µS (Baseline: {baseline_gsr:.1f} µS)</td></tr>
                    <tr><td><strong>Final Pulse:</strong></td><td>{final_pulse} BPM (Baseline: {baseline_pulse:.1f} BPM)</td></tr>
                    <tr><td><strong>Final Oxygen:</strong></td><td>{final_oxygen}% (Baseline: {baseline_oxygen:.1f}%)</td></tr>
                    <tr><td><strong>Duration:</strong></td><td>{total_duration} seconds</td></tr>
                    <tr><td><strong>Data Points:</strong></td><td>{len(st.session_state.biometrics['time'])} readings</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            # Prepare data for download
            session_data = pd.DataFrame({
                'Athlete': [st.session_state.athlete['name']] * len(st.session_state.biometrics['time']),
                'Age': [st.session_state.athlete['age']] * len(st.session_state.biometrics['time']),
                'Gender': [st.session_state.athlete['gender']] * len(st.session_state.biometrics['time']),
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(st.session_state.biometrics['time']),
                'Time_Elapsed': st.session_state.biometrics['time'],
                'GSR': st.session_state.biometrics['gsr'],
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
                'Metric': ['GSR', 'Heart Rate', 'Oxygen Saturation'],
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
                    f"processed_biometrics_{st.session_state.athlete['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            with col2:
                st.download_button(
                    "📋 Download Raw Data (CSV)",
                    raw_data_df.to_csv(index=False),
                    f"raw_biometrics_{st.session_state.athlete['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            with col3:
                st.download_button(
                    "📊 Download Summary Report (CSV)",
                    summary_df.to_csv(index=False),
                    f"summary_biometrics_{st.session_state.athlete['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        finally:
            if 'ser' in st.session_state:
                st.session_state.ser.close()
                del st.session_state.ser
                st.warning("Disconnected from device")

