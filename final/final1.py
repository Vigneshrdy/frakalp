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
    page_title=" Dashboard",
    # page_icon="🏅",
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

st.title("Health Biometric Monitoring")

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

elif nav == '⚖️ BMI Calculator':
    st.header("⚖️ BMI Calculator & Sport Recommendation")
    
    # User Information Section
    with st.expander("🧑 User Information", expanded=True):
        with st.form("bmi_form"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Full Name", key="bmi_name")
                age = st.number_input("Age", min_value=12, max_value=80, key="bmi_age")
                gender = st.radio("Gender", ["Male", "Female", "Other"], key="bmi_gender")
            with cols[1]:
                height = st.number_input("Height (cm)", min_value=100, max_value=250, key="bmi_height")
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200,  key="bmi_weight")
                
            if st.form_submit_button("📊 Calculate BMI"):
                st.session_state.bmi_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    
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
            # recommended_sports = ["Gymnastics", "Diving", "Figure Skating", "Long-distance running"]
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            category_class = "normal"
            # recommended_sports = ["Swimming", "Tennis", "Volleyball", "Basketball", "Soccer"]
        elif 25 <= bmi < 30:
            category = "Overweight"
            category_class = "overweight"
            # recommended_sports = ["Weightlifting", "Rowing", "Rugby", "Judo", "Shot put"]
        else:
            category = "Obese"
            category_class = "obese"
            # recommended_sports = ["Super Heavyweight Boxing", "Powerlifting", "Sumo wrestling"]
        
        st.session_state.bmi_data['category'] = category
        # st.session_state.bmi_data['recommended_sports'] = ", ".join(recommended_sports)
        
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
                    <tr><td><strong>Average GSR:</strong></td><td>{avg_gsr:.1f} µS</td></tr>
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
# Biometric Monitoring Page
elif nav == '💓 Stress-O2-Pulse Monitoring':
    st.header("🏥 Real-Time Biometric Monitoring")
    st.write("""
    Monitor data in real-time:
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