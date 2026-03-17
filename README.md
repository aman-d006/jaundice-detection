# 🏥 Jaundice Detection AI-CDSS

<div align="center">
  
### AI-Powered Clinical Decision Support System
  
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=render)](https://jaundice-frontend.onrender.com)
[![API](https://img.shields.io/badge/API-FastAPI-blue?style=for-the-badge&logo=fastapi)](https://jaundice-backend.onrender.com)
[![Made with](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)](https://python.org)

</div>

## 📋 Overview
A clinical decision support system that helps healthcare professionals detect and assess jaundice severity instantly using patient clinical parameters.

## 🚀 Live Demo
- **Frontend:** [https://jaundice-frontend.onrender.com](https://jaundice-frontend.onrender.com)
- **Backend API:** [https://jaundice-backend.onrender.com](https://jaundice-backend-xbwq.onrender.com)
- **API Docs:** [https://jaundice-backend.onrender.com/docs](https://jaundice-backend-xbwq.onrender.com/docs)

## ✨ Features
- ✅ Instant jaundice detection & severity classification
- ✅ Clinical recommendations
- ✅ Interactive dashboard
- ✅ Report download (JSON)
- ✅ Free & accessible anywhere

## 📊 Severity Classification
| Bilirubin Level | Severity | Action |
|-----------------|----------|--------|
| < 1.2 mg/dL | None | Routine monitoring |
| 1.2 - 5.0 mg/dL | Mild | Outpatient management |
| 5.0 - 10.0 mg/dL | Moderate | Hepatology consultation |
| > 10.0 mg/dL | Severe | Immediate hospitalization |

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit (Python)
- **Visualization:** Plotly
- **Deployment:** Render

## 🚀 Quick Test
```bash
curl -X POST https://jaundice-backend.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age_days": 30,
    "bilirubin_total": 2.5,
    "bilirubin_direct": 1.2,
    "ast": 45,
    "alt": 50,
    "alk_phosphatase": 120,
    "hemoglobin": 13.5,
    "rbc_count": 4.5,
    "wbc_count": 7.5,
    "platelet_count": 250
  }'

🧪 Test Cases
Case	Bilirubin	Expected Result
Severe	15.0 mg/dL	Severe Jaundice
Moderate	7.5 mg/dL	Moderate Jaundice
Mild	2.5 mg/dL	Mild Jaundice
None	0.8 mg/dL	No Jaundice

⚠️ Disclaimer
For clinical decision support only. Always consult healthcare providers.

<div align="center"> Made with ❤️ for healthcare professionals </div> ```

