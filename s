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