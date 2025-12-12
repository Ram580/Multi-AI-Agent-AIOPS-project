import streamlit as st
import requests

from app.config.settings import settings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent" , layout="centered")
st.title("Multi AI Agent using LangGraph")

system_prompt = st.text_area("define the AI Agent's persona: ", height=100)
selected_model = st.selectbox("Select your preffered AI Model", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query : " , height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Get Response"):
    if not user_query.strip():
        st.warning("Please enter a message before submitting.")
    else:
        payload = {
            "model_name": selected_model,
            "system_prompt": system_prompt,
            "messeges": [user_query],
            "allow_search": allow_web_search
        }
        
        try:
            logger.info(f"Sending request to backend")
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                agent_response = response.json().get("response", "")
                logger.info(f"Received response from backend successfully")
                
                st.success("Response from AI Agent:")
                st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
                
            else:
                error_message = f"API Error {response.status_code}: {response.text}"
                st.error(error_message)
                logger.error(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"Error communicating with the API: {e}"
            st.error(error_message)
            logger.error(error_message)
            
        except Exception as e:
            custom_exc = CustomException("An unexpected error occurred while sending the request to backend", error_detail=e)
            st.error(str(custom_exc))
            logger.error(str(custom_exc))