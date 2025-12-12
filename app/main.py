import subprocess
import threading
import time
from dotenv import load_dotenv

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(['uvicorn', 'app.backend.api:app', '--host', '127.0.0.1', '--port', '9999'], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Backend server failed to start: {e}")
        raise CustomException("Backend server failed to start", error_detail=e)
    
def run_frontend():
    try:
        logger.info("Starting frontend server...")
        subprocess.run(['streamlit', 'run', 'app/frontend/ui.py'], check=True)
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Backend server failed to start: {e}")
        raise CustomException("failed to start frontend", error_detail=e)
    
if __name__=="__main__":
    try:
        logger.info("Starting Multi AI Agent Application...")
        threading.Thread(target=run_backend).start()
        # Wait for a few seconds to ensure the backend starts before the frontend
        time.sleep(2)
        run_frontend()
    except CustomException as e:
        logger.exception(f"CustomException occured : {str(e)}")
