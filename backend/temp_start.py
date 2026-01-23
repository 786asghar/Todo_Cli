import os
import sys
import subprocess

# Set environment variables
os.environ['OPEN_ROUTER_API_KEY'] = 'test_key'
os.environ['OPEN_ROUTER_URL'] = 'https://openrouter.ai/api/v1/chat/completions'

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the FastAPI app
from src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)