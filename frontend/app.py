import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

# Page config
st.set_page_config(
    page_title="Jaundice Detector",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# API URL - Change this to your Render URL after deployment
API_URL = os.getenv("API_URL", "http://localhost:8000")


# Header
st.markdown('<div class="main-title"><h1>🏥 Jaundice Detection System</h1><p>AI-Powered Clinical Decision Support</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Fixed: Removed use_column_width, added width parameter
    st.image("https://via.placeholder.com/300x150?text=Jaundice+AI", width=300, caption="AI-Powered Diagnosis")
    
    st.markdown("## About")
    st.info("This tool helps detect jaundice severity based on clinical parameters.")
    
    st.markdown("## Normal Ranges")
    ranges = {
        "Total Bilirubin": "< 1.2 mg/dL",
        "Direct Bilirubin": "< 0.3 mg/dL",
        "AST": "10-40 U/L",
        "ALT": "7-56 U/L",
        "Hemoglobin": "12-16 g/dL",
        "RBC Count": "4.5-5.5 millions/µL",
        "WBC Count": "4.5-11 thousands/µL",
        "Platelet Count": "150-450 thousands/µL"
    }
    
    # Create a nice table for ranges
    df_ranges = pd.DataFrame(list(ranges.items()), columns=["Parameter", "Normal Range"])
    st.table(df_ranges)
    
    st.markdown("---")
    st.markdown("### Connection Status")
    
    # Test API connection
    if st.button("🔄 Test Connection"):
        with st.spinner("Testing connection..."):
            try:
                r = requests.get(f"{API_URL}/health", timeout=2)
                if r.status_code == 200:
                    st.success("✅ Connected to API")
                else:
                    st.error("❌ API Error")
            except:
                st.error("❌ Cannot connect to API")
    
    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("""
    1. Enter patient details
    2. Click 'Analyze Patient'
    3. Review results
    4. Check recommendations
    """)

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("## 📋 Patient Data")
    
    # Basic Info in an expander
    with st.expander("Patient Demographics", expanded=True):
        age = st.number_input("Age (days)", min_value=0, max_value=36500, value=30, help="Enter patient age in days")
        age_years = age / 365
        st.caption(f"≈ {age_years:.1f} years")
    
    # Lab Results in columns
    st.markdown("### Laboratory Results")
    
    col_lab1, col_lab2 = st.columns(2)
    
    with col_lab1:
        st.markdown("#### Liver Function Tests")
        bilirubin_total = st.number_input("Total Bilirubin (mg/dL)", min_value=0.0, max_value=50.0, value=2.5, step=0.1, 
                                         help="Normal: <1.2 mg/dL")
        bilirubin_direct = st.number_input("Direct Bilirubin (mg/dL)", min_value=0.0, max_value=25.0, value=1.2, step=0.1,
                                          help="Normal: <0.3 mg/dL")
        bilirubin_indirect = bilirubin_total - bilirubin_direct
        st.caption(f"Indirect Bilirubin: {bilirubin_indirect:.2f} mg/dL")
        
        ast = st.number_input("AST (U/L)", min_value=0, max_value=1000, value=45, help="Normal: 10-40 U/L")
        alt = st.number_input("ALT (U/L)", min_value=0, max_value=1000, value=50, help="Normal: 7-56 U/L")
        alk_phosphatase = st.number_input("Alkaline Phosphatase (U/L)", min_value=0, max_value=1000, value=120,
                                         help="Normal: 30-120 U/L")
    
    with col_lab2:
        st.markdown("#### Complete Blood Count")
        hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=13.5, step=0.1,
                                    help="Normal: 12-16 g/dL")
        rbc_count = st.number_input("RBC Count (millions/µL)", min_value=0.0, max_value=10.0, value=4.5, step=0.1,
                                   help="Normal: 4.5-5.5 millions/µL")
        wbc_count = st.number_input("WBC Count (thousands/µL)", min_value=0.0, max_value=50.0, value=7.5, step=0.1,
                                   help="Normal: 4.5-11 thousands/µL")
        platelet_count = st.number_input("Platelet Count (thousands/µL)", min_value=0, max_value=1000, value=250,
                                        help="Normal: 150-450 thousands/µL")
    
    # Symptoms
    st.markdown("### Symptoms")
    symptoms = st.multiselect(
        "Select observed symptoms",
        ["Yellow skin/eyes", "Dark urine", "Pale stools", "Fatigue", 
         "Abdominal pain", "Fever", "Nausea", "Weight loss", "Itching"],
        help="Select all symptoms the patient is experiencing"
    )
    
    if symptoms:
        st.info(f"Selected symptoms: {', '.join(symptoms)}")

with col2:
    st.markdown("## 📊 Bilirubin Analysis")
    
    # Simple gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = bilirubin_total,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Bilirubin Level (mg/dL)", 'font': {'size': 16}},
        delta = {'reference': 1.2, 'increasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [0, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1.2], 'color': 'lightgreen', 'name': 'Normal'},
                {'range': [1.2, 5], 'color': 'yellow', 'name': 'Mild'},
                {'range': [5, 10], 'color': 'orange', 'name': 'Moderate'},
                {'range': [10, 20], 'color': 'red', 'name': 'Severe'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bilirubin_total
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=30))
    st.plotly_chart(fig, use_container_width=True)
    
    # Bilirubin interpretation
    st.markdown("### Interpretation")
    if bilirubin_total < 1.2:
        st.success("✅ **Normal Range** - No jaundice detected")
    elif bilirubin_total < 5:
        st.warning("⚠️ **Mild Elevation** - Suggestive of mild jaundice")
    elif bilirubin_total < 10:
        st.error("⚠️ **Moderate Elevation** - Moderate jaundice likely")
    else:
        st.error("🚨 **Severe Elevation** - Severe jaundice, immediate attention needed")
    
    # Quick reference
    with st.expander("📖 Quick Reference"):
        st.markdown("""
        **Jaundice Severity by Total Bilirubin:**
        - **Normal:** < 1.2 mg/dL
        - **Mild:** 1.2 - 5.0 mg/dL
        - **Moderate:** 5.0 - 10.0 mg/dL  
        - **Severe:** > 10.0 mg/dL
        
        **Note:** Always consider clinical context and other lab values.
        """)

# Predict button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict = st.button("🔍 Analyze Patient", use_container_width=True, type="primary")

if predict:
    with st.spinner("Analyzing patient data..."):
        # Prepare data
        patient_data = {
            "age_days": age,
            "bilirubin_total": bilirubin_total,
            "bilirubin_direct": bilirubin_direct,
            "ast": ast,
            "alt": alt,
            "alk_phosphatase": alk_phosphatase,
            "hemoglobin": hemoglobin,
            "rbc_count": rbc_count,
            "wbc_count": wbc_count,
            "platelet_count": platelet_count
        }
        
        try:
            # Call API
            response = requests.post(f"{API_URL}/predict", json=patient_data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.markdown("## 🎯 Analysis Results")
                st.markdown("---")
                
                # Results in three columns with proper visibility
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    # Diagnosis box
                    severity_class = result['severity'].lower()
                    if severity_class == 'severe':
                        st.error(f"### Diagnosis\n# {result['prediction']}")
                    elif severity_class == 'moderate':
                        st.warning(f"### Diagnosis\n# {result['prediction']}")
                    elif severity_class == 'mild':
                        st.info(f"### Diagnosis\n# {result['prediction']}")
                    else:
                        st.success(f"### Diagnosis\n# {result['prediction']}")
                
                with col_res2:
                    # Confidence box with metric and progress bar
                    confidence = int(result['confidence']*100)
                    
                    # Color code confidence
                    if confidence >= 80:
                        st.success(f"### Confidence\n# {confidence}%")
                    elif confidence >= 60:
                        st.warning(f"### Confidence\n# {confidence}%")
                    else:
                        st.error(f"### Confidence\n# {confidence}%")
                    
                    # Add progress bar
                    st.progress(result['confidence'])
                
                with col_res3:
                    # Severity box with color coding
                    severity_class = result['severity'].lower()
                    if severity_class == 'severe':
                        st.error(f"### Severity\n# {result['severity']}")
                    elif severity_class == 'moderate':
                        st.warning(f"### Severity\n# {result['severity']}")
                    elif severity_class == 'mild':
                        st.info(f"### Severity\n# {result['severity']}")
                    else:
                        st.success(f"### Severity\n# {result['severity']}")
                
                st.markdown("---")
                
                # Recommendations
                st.markdown("## 💊 Clinical Recommendations")
                
                # Create columns for recommendations
                for i, rec in enumerate(result['recommendations'], 1):
                    if result['severity'].lower() == 'severe':
                        st.error(f"**{i}.** {rec}")
                    elif result['severity'].lower() == 'moderate':
                        st.warning(f"**{i}.** {rec}")
                    elif result['severity'].lower() == 'mild':
                        st.info(f"**{i}.** {rec}")
                    else:
                        st.success(f"**{i}.** {rec}")
                
                # Patient Summary in an expander
                with st.expander("📋 View Detailed Patient Summary"):
                    col_sum1, col_sum2 = st.columns(2)
                    
                    with col_sum1:
                        st.markdown("**Patient Information**")
                        st.json({
                            "age_days": age,
                            "age_years": round(age/365, 1),
                            "bilirubin_total": bilirubin_total,
                            "bilirubin_direct": bilirubin_direct,
                            "bilirubin_indirect": round(bilirubin_total - bilirubin_direct, 2)
                        })
                    
                    with col_sum2:
                        st.markdown("**Prediction Results**")
                        st.json({
                            "diagnosis": result['prediction'],
                            "confidence": f"{result['confidence']*100:.1f}%",
                            "severity": result['severity'],
                            "probability": f"{result['probability']*100:.1f}%"
                        })
                    
                    if symptoms:
                        st.markdown("**Reported Symptoms**")
                        st.write(", ".join(symptoms))
                    
                    # Download button for report
                    report_data = {
                        "patient_data": patient_data,
                        "results": result,
                        "symptoms": symptoms
                    }
                    
                    st.download_button(
                        label="📥 Download Report (JSON)",
                        data=str(report_data),
                        file_name=f"jaundice_report_{age}days.json",
                        mime="application/json"
                    )
                    
            else:
                st.error(f"❌ API Error: Status code {response.status_code}")
                st.info("Please check if the backend server is running correctly.")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Please ensure the backend is running at: " + API_URL)
            st.info("To run locally: Open terminal in backend folder and run: uvicorn main:app --reload")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])
with col_footer2:
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 10px;'>
            <p>🏥 <b>Jaundice Detection AI-CDSS</b> | Version 1.0</p>
            <p>⚠️ <i>For clinical decision support only. Always consult healthcare providers.</i></p>
            <p>Made with ❤️ for healthcare professionals</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Auto-refresh toggle in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### Settings")
    auto_refresh = st.checkbox("Enable auto-refresh (30s)")
    if auto_refresh:
        st.experimental_rerun()