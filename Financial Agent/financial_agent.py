from phi.agent import Agent 
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo


web_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for the required information",
    model = Groq(id="llama-3.1-70b-versatile"),
    tools = [DuckDuckGo()],
    instructions=["Always include the sources with their urls"],
    show_tool_calls=True,
    markdown=True,
)



finance_agent = Agent(
    name = "Finanace Agent",
    model = Groq(id = "llama-3.1-70b-versatile"),
    tools = [
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True),
    ],
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions=["Format your response using markdown and use tables to display data where possible."],
    show_tool_calls = True,
    markdown = True,
)


multi_model_agent = Agent(
    team=[web_agent, finance_agent],
    model = Groq(id ="llama-3.1-70b-versatile"),
    instructions=["Always include the sources with their urls", "Format your response using markdown and use tables to display data where possible."],
    show_tool_calls= True,
    markdown=True
)


multi_model_agent.print_response("Summarize analyst recommendations and share the latest news for NVDA with date and time", stream=True)