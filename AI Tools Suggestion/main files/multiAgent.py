import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

# Setup model client
open_router_model_client = OpenAIChatCompletionClient(
    base_url="https://openrouter.ai/api/v1",
    model="deepseek/deepseek-r1-0528:free",
    api_key=OPEN_ROUTER_API_KEY,
    model_info={
        "family": "deepseek",
        "vision": True,
        "function_calling": True,
        "json_output": False
    }
)



# 🛠️ Tools Matcher
tools_fetcher = AssistantAgent(
    name="tools_fetcher",
    model_client=open_router_model_client,
    system_message="""
You are an expert tool recommender for developers.

Given a clarified query, suggest ONLY the most relevant tools or APIs that help solve the problem.

Return output in this format:
Recommended Tools:
- Tool 1
- Tool 2
- Tool 3

Do NOT explain or justify. Do NOT recommend LLMs. Only give tool names.
""".strip()
)

# 🤖 LLM Selector
llm_fetcher = AssistantAgent(
    name="llm_fetcher",
    model_client=open_router_model_client,
    system_message="""
You are an expert LLM selector.

Given the clarified query and tool list, suggest only the best LLMs or models suited for the task.

Output format:
Recommended LLMs:
- LLM 1
- LLM 2

Do NOT explain or add descriptions. Just model names.
""".strip()
)


# 🔍 Clarifying Agent
clarifying_agent = AssistantAgent(
    name="clarifying_agent",
    model_client=open_router_model_client,
    system_message="""
You are a smart dev assistant.

Your job is to ask up to 2 clarifying questions to refine the user's vague or broad query. Do NOT suggest tools or LLMs yet.

Respond in this format:
Clarifying Questions:
1. <question 1>
2. <question 2>
""".strip()
)

# (Optional) 🧠 Coordinator Agent (if needed for context bridging between agents later)
# You can add this later if tools/LLMs need memory of clarifier context across loops.

# 🔄 Team RoundRobin Loop
team = RoundRobinGroupChat(
    participants=[tools_fetcher, llm_fetcher, clarifying_agent],
    max_turns=3
)


# Test Function
async def test_team():
    task = TextMessage(
        content='''i want to build a sportness apllication which can track my fitness journey
        ''',
        source='user'
    )

    result = await team.run(task=task)

    print("\n=== FINAL OUTPUT ===")
    for message in result.messages:
        print(f"\n[{message.source.upper()}]:\n{message.content}")


if __name__ == "__main__":
    asyncio.run(test_team())
