@echo off
REM Startup script for Phase 3 implementation

echo Installing dependencies...
pip install -r requirements.txt

echo Starting Phase 3 Agent-Based Chatbot Architecture...
python phase3_main.py