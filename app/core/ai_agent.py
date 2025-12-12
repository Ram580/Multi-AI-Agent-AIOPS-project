from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent     
from langchain_core.messages.ai import AIMessage
 

from app.config.settings import settings


def get_response_from_ai_agents(llm_id:str='openai/gpt-oss-120b', query:str='hi', allow_search=False, system_prompt=None):
    if llm_id not in settings.ALLOWED_MODEL_NAMES:
        raise ValueError(f"Model {llm_id} is not allowed.")
    
    llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name=llm_id)

    tools = [TavilySearchResults(api_key=settings.TAVILY_API_KEY, max_results=2)] if allow_search else []


    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        # state_modifier=system_prompt
    )
    
    state = {"messages": query}

    response = agent.invoke(state)
    messages = response.get("messages", [])

    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
    
