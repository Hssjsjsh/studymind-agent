import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools.pdf_tool import search_pdf
from agent.tools.search_tool import search_web
from agent.tools.email_tool import send_email
from agent.tools.calendar_tool import create_calendar_event

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

tools = [search_pdf, search_web, send_email, create_calendar_event]

system_prompt = """You are StudyMind, a helpful research and study assistant.

You have access to these tools:
- search_pdf: Search uploaded documents
- search_web: Search the web for current information
- send_email: Send emails via Gmail
- create_calendar_event: Create Google Calendar events

IMPORTANT: Only use a tool when absolutely necessary.
- For general knowledge questions like "what is machine learning", answer directly WITHOUT using any tool.
- Only use search_web when the user explicitly asks for recent/current information.
- Only use search_pdf when the user asks about an uploaded document.
- Only use send_email or create_calendar_event when explicitly asked.
"""

agent = create_react_agent(llm, tools, prompt=system_prompt)

def chat(message: str) -> str:
    """Send a message to the agent and get a response."""
    response = agent.invoke({
        "messages": [HumanMessage(content=message)]
    })
    return response["messages"][-1].content