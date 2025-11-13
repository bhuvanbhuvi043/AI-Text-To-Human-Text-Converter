@echo off
cd /d "C:\zetiify-poc\AI_Text_To_Human_Text_Converter"
call venv\Scripts\activate
start "" "http://localhost:8501"
streamlit run app.py --server.port 8501
pause
