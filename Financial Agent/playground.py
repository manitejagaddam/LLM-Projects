from phi.agent import Agent 
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
import phi.api 
from phi.playground import Playground, serve_playground_app

load_dotenv()


phi.api=os.getenv("PHI_API_KEY")
# print(os.getenv("PHI_API_KEY"))

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


app = Playground(agents=[finance_agent, web_agent]).get_app()
print(app)

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)