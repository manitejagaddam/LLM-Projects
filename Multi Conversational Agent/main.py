import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging


import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent


import google.generativeai as genai
import litellm


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class GeminiAutoGenFramework:
   """
   Complete AutoGen framework using free Gemini API
   Supports multi-agent conversations, code execution, and retrieval
   """
  
   def __init__(self, gemini_api_key: str):
       """Initialize with Gemini API key"""
       self.gemini_api_key = gemini_api_key
       self.setup_gemini_config()
       self.agents: Dict[str, autogen.Agent] = {}
       self.group_chats: Dict[str, GroupChat] = {}
      
   def setup_gemini_config(self):
       """Configure Gemini for AutoGen"""
       os.environ["GOOGLE_API_KEY"] = self.gemini_api_key
      
       self.llm_config = {
           "config_list": [
               {
                   "model": "gemini/gemini-1.5-flash",
                   "api_key": self.gemini_api_key,
                   "api_type": "google",
                   "temperature": 0.7,
                   "max_tokens": 4096,
               }
           ],
           "timeout": 120,
           "cache_seed": 42, 
       }
      
       self.llm_config_pro = {
           "config_list": [
               {
                   "model": "gemini/gemini-1.5-pro",
                   "api_key": self.gemini_api_key,
                   "api_type": "google",
                   "temperature": 0.5,
                   "max_tokens": 8192,
               }
           ],
           "timeout": 180,
           "cache_seed": 42,
       }
  
   def create_assistant_agent(self, name: str, system_message: str,
                            use_pro_model: bool = False) -> AssistantAgent:
       """Create a specialized assistant agent"""
       config = self.llm_config_pro if use_pro_model else self.llm_config
      
       agent = AssistantAgent(
           name=name,
           system_message=system_message,
           llm_config=config,
           human_input_mode="NEVER",
           max_consecutive_auto_reply=10,
           code_execution_config=False,
       )
      
       self.agents[name] = agent
       return agent
  
   def create_user_proxy(self, name: str = "UserProxy",
                        enable_code_execution: bool = True) -> UserProxyAgent:
       """Create user proxy agent with optional code execution"""
      
       code_config = {
           "work_dir": "autogen_workspace",
           "use_docker": False,
           "timeout": 60,
           "last_n_messages": 3,
       } if enable_code_execution else False
      
       agent = UserProxyAgent(
           name=name,
           human_input_mode="TERMINATE",
           max_consecutive_auto_reply=0,
           is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
           code_execution_config=code_config,
           system_message="""A human admin. Interact with the agents to solve tasks.
           Reply TERMINATE when the task is solved."""
       )
      
       self.agents[name] = agent
       return agent
  
   def create_research_team(self) -> Dict[str, autogen.Agent]:
       """Create a research-focused agent team"""
      
       researcher = self.create_assistant_agent(
           name="Researcher",
           system_message="""You are a Senior Research Analyst. Your role is to:
           1. Gather and analyze information on given topics
           2. Identify key trends, patterns, and insights 
           3. Provide comprehensive research summaries
           4. Cite sources and maintain objectivity
          
           Always structure your research with clear sections and bullet points.
           Be thorough but concise."""
       )
      
       analyst = self.create_assistant_agent(
           name="DataAnalyst",
           system_message="""You are a Data Analysis Expert. Your role is to:
           1. Analyze quantitative data and statistics
           2. Create data visualizations and charts
           3. Identify patterns and correlations
           4. Provide statistical insights and interpretations
          
           Use Python code when needed for calculations and visualizations.
           Always explain your analytical approach."""
       )
      
       writer = self.create_assistant_agent(
           name="Writer",
           system_message="""You are a Technical Writer and Content Strategist. Your role is to:
           1. Transform research and analysis into clear, engaging content
           2. Create well-structured reports and articles
           3. Ensure content is accessible to the target audience
           4. Maintain professional tone and accuracy
          
           Structure content with clear headings, bullet points, and conclusions."""
       )
      
       executor = self.create_user_proxy("CodeExecutor", enable_code_execution=True)
      
       return {
           "researcher": researcher,
           "analyst": analyst,
           "writer": writer,
           "executor": executor
       }
  
   def create_business_team(self) -> Dict[str, autogen.Agent]:
       """Create business analysis team"""
      
       strategist = self.create_assistant_agent(
           name="BusinessStrategist",
           system_message="""You are a Senior Business Strategy Consultant. Your role is to:
           1. Analyze business problems and opportunities
           2. Develop strategic recommendations and action plans
           3. Assess market dynamics and competitive landscape
           4. Provide implementation roadmaps
          
           Think systematically and consider multiple perspectives.
           Always provide actionable recommendations.""",
           use_pro_model=True 
       )
      
       financial_analyst = self.create_assistant_agent(
           name="FinancialAnalyst",
           system_message="""You are a Financial Analysis Expert. Your role is to:
           1. Perform financial modeling and analysis
           2. Assess financial risks and opportunities
           3. Calculate ROI, NPV, and other financial metrics
           4. Provide budget and investment recommendations
          
           Use quantitative analysis and provide clear financial insights."""
       )
      
       market_researcher = self.create_assistant_agent(
           name="MarketResearcher",
           system_message="""You are a Market Research Specialist. Your role is to:
           1. Analyze market trends and consumer behavior
           2. Research competitive landscape and positioning
           3. Identify target markets and customer segments
           4. Provide market sizing and opportunity assessment
          
           Focus on actionable market insights and recommendations."""
       )
      
       return {
           "strategist": strategist,
           "financial_analyst": financial_analyst,
           "market_researcher": market_researcher,
           "executor": self.create_user_proxy("BusinessExecutor")
       }
  
   def create_development_team(self) -> Dict[str, autogen.Agent]:
       """Create software development team"""
      
       developer = self.create_assistant_agent(
           name="SeniorDeveloper",
           system_message="""You are a Senior Software Developer. Your role is to:
           1. Write high-quality, efficient code
           2. Design software architecture and solutions
           3. Debug and optimize existing code
           4. Follow best practices and coding standards
          
           Always explain your code and design decisions.
           Focus on clean, maintainable solutions."""
       )
      
       devops = self.create_assistant_agent(
           name="DevOpsEngineer",
           system_message="""You are a DevOps Engineer. Your role is to:
           1. Design deployment and infrastructure solutions
           2. Automate build, test, and deployment processes
           3. Monitor system performance and reliability
           4. Implement security and scalability best practices
          
           Focus on automation, reliability, and scalability."""
       )
      
       qa_engineer = self.create_assistant_agent(
           name="QAEngineer",
           system_message="""You are a Quality Assurance Engineer. Your role is to:
           1. Design comprehensive test strategies and cases
           2. Identify potential bugs and edge cases
           3. Ensure code quality and performance standards
           4. Validate requirements and user acceptance criteria
          
           Be thorough and think about edge cases and failure scenarios."""
       )
      
       return {
           "developer": developer,
           "devops": devops,
           "qa_engineer": qa_engineer,
           "executor": self.create_user_proxy("DevExecutor", enable_code_execution=True)
       }
  
   def create_group_chat(self, agents: List[autogen.Agent], chat_name: str,
                        max_round: int = 10) -> GroupChat:
       """Create group chat with specified agents"""
      
       group_chat = GroupChat(
           agents=agents,
           messages=[],
           max_round=max_round,
           speaker_selection_method="round_robin",
           allow_repeat_speaker=False,
       )
      
       self.group_chats[chat_name] = group_chat
       return group_chat
  
   def run_research_project(self, topic: str, max_rounds: int = 8) -> str:
       """Run a comprehensive research project"""
      
       team = self.create_research_team()
       agents_list = [team["researcher"], team["analyst"], team["writer"], team["executor"]]
      
       group_chat = self.create_group_chat(agents_list, "research_chat", max_rounds)
       manager = GroupChatManager(
           groupchat=group_chat,
           llm_config=self.llm_config
       )
      
       initial_message = f"""
       Research Project: {topic}
      
       Please collaborate to produce a comprehensive research report following this workflow:
       1. Researcher: Gather information and key insights about {topic}
       2. DataAnalyst: Analyze any quantitative aspects and create visualizations if needed
       3. Writer: Create a well-structured final report based on the research and analysis
       4. CodeExecutor: Execute any code needed for analysis or visualization
      
       The final deliverable should be a professional research report with:
       - Executive summary
       - Key findings and insights 
       - Data analysis (if applicable)
       - Conclusions and recommendations
      
       Begin the research process now.
       """
      
       chat_result = team["executor"].initiate_chat(
           manager,
           message=initial_message,
           max_consecutive_auto_reply=0
       )
      
       return self._extract_final_result(chat_result)
  
   def run_business_analysis(self, business_problem: str, max_rounds: int = 8) -> str:
       """Run business analysis project"""
      
       team = self.create_business_team()
       agents_list = [team["strategist"], team["financial_analyst"],
                     team["market_researcher"], team["executor"]]
      
       group_chat = self.create_group_chat(agents_list, "business_chat", max_rounds)
       manager = GroupChatManager(
           groupchat=group_chat,
           llm_config=self.llm_config_pro
       )
      
       initial_message = f"""
       Business Analysis Project: {business_problem}
      
       Please collaborate to provide comprehensive business analysis following this approach:
       1. BusinessStrategist: Analyze the business problem and develop strategic framework
       2. FinancialAnalyst: Assess financial implications and create financial models
       3. MarketResearcher: Research market context and competitive landscape
       4. BusinessExecutor: Coordinate and compile final recommendations
      
       Final deliverable should include:
       - Problem analysis and root causes
       - Strategic recommendations 
       - Financial impact assessment
       - Market opportunity analysis
       - Implementation roadmap
      
       Begin the analysis now.
       """
      
       chat_result = team["executor"].initiate_chat(
           manager,
           message=initial_message,
           max_consecutive_auto_reply=0
       )
      
       return self._extract_final_result(chat_result)
  
   def run_development_project(self, project_description: str, max_rounds: int = 10) -> str:
       """Run software development project"""
      
       team = self.create_development_team()
       agents_list = [team["developer"], team["devops"], team["qa_engineer"], team["executor"]]
      
       group_chat = self.create_group_chat(agents_list, "dev_chat", max_rounds)
       manager = GroupChatManager(
           groupchat=group_chat,
           llm_config=self.llm_config
       )
      
       initial_message = f"""
       Development Project: {project_description}
      
       Please collaborate to deliver a complete software solution:
       1. SeniorDeveloper: Design architecture and write core code
       2. DevOpsEngineer: Plan deployment and infrastructure
       3. QAEngineer: Design tests and quality assurance approach
       4. DevExecutor: Execute code and coordinate implementation
      
       Deliverables should include:
       - System architecture and design
       - Working code implementation
       - Deployment configuration
       - Test cases and QA plan
       - Documentation
      
       Start development now.
       """
      
       chat_result = team["executor"].initiate_chat(
           manager,
           message=initial_message,
           max_consecutive_auto_reply=0
       )
      
       return self._extract_final_result(chat_result)
  
   def _extract_final_result(self, chat_result) -> str:
       """Extract and format final result from chat"""
       if hasattr(chat_result, 'chat_history'):
           messages = chat_result.chat_history
       else:
           messages = chat_result
      
       final_messages = []
       for msg in messages[-5:]:
           if isinstance(msg, dict) and 'content' in msg:
               final_messages.append(f"{msg.get('name', 'Agent')}: {msg['content']}")
      
       return "\n\n".join(final_messages)
  
   def get_framework_stats(self) -> Dict[str, Any]:
       """Get framework statistics"""
       return {
           "agents": list(self.agents.keys()),
           "group_chats": list(self.group_chats.keys()),
           "llm_config": {
               "model": self.llm_config["config_list"][0]["model"],
               "temperature": self.llm_config["config_list"][0]["temperature"]
           },
           "timestamp": datetime.now().isoformat()
       }
       
       
       


def demo_autogen_framework():
   """Demo the AutoGen framework"""
   print("🚀 Microsoft AutoGen + Gemini Framework Demo")
   print("=" * 60)
  
   GEMINI_API_KEY = "your-gemini-api-key-here"
  
   framework = GeminiAutoGenFramework(GEMINI_API_KEY)
  
   print("✅ Framework initialized successfully!")
   print(f"📊 Stats: {json.dumps(framework.get_framework_stats(), indent=2)}")
  
   return framework


async def run_demo_projects(framework):
   """Run demonstration projects"""
  
   print("\n🔬 Running Research Project...")
   research_result = framework.run_research_project(
       "Impact of Generative AI on Software Development in 2025"
   )
   print("Research Result (excerpt):")
   print(research_result[:500] + "..." if len(research_result) > 500 else research_result)
  
   print("\n💼 Running Business Analysis...")
   business_result = framework.run_business_analysis(
       "A mid-sized company wants to implement AI-powered customer service. "
       "They currently have 50 support staff and handle 1000 tickets daily. "
       "Budget is $500K annually."
   )
   print("Business Analysis Result (excerpt):")
   print(business_result[:500] + "..." if len(business_result) > 500 else business_result)
  
   print("\n💻 Running Development Project...")
   dev_result = framework.run_development_project(
       "Build a Python web scraper that extracts product information from e-commerce sites, "
       "stores data in a database, and provides a REST API for data access."
   )
   print("Development Result (excerpt):")
   print(dev_result[:500] + "..." if len(dev_result) > 500 else dev_result)


if __name__ == "__main__":
   print("Microsoft AutoGen + Gemini Framework Ready! 🚀")
   print("\n📦 For Google Colab, run:")
   print("!pip install pyautogen google-generativeai litellm")
   print("\n🔑 Get your free Gemini API key:")
   print("https://makersuite.google.com/app/apikey")
   print("\n🚀 Quick start:")
   print("""
# Initialize framework
# framework = GeminiAutoGenFramework("your-gemini-api-key")


# Run research project 
result = framework.run_research_project("AI Trends 2025")
print(result)


# Run business analysis
result = framework.run_business_analysis("Market entry strategy for AI startup")
print(result)


# Run development project
result = framework.run_development_project("Build a REST API for user management")
print(result)
   """)