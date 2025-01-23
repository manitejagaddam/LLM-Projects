import typer
from typing import Optional, List
from phi.agent import Agent
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType
import logging
from dotenv import load_dotenv

load_dotenv()
# from phi.utils import set_openai_api_key

# set_openai_api_key(os.getenv("OPEN_API_KEY"))
# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://www.cardiff.ac.uk/__data/assets/pdf_file/0003/123681/Recipe-Book.pdf"],
    vector_db=PgVector(table_name="recipes", db_url=db_url, search_type=SearchType.hybrid),
)

# Storage for agent sessions
storage = PgAgentStorage(table_name="pdf_agent", db_url=db_url)

# Load the knowledge base (Comment after the first successful run)
try:
    print("Loading knowledge base...")
    knowledge_base.load(upsert=True)
    print("Knowledge base loaded successfully.")
except Exception as e:
    logging.error(f"Error loading knowledge base: {e}")
    exit(1)

# PDF Agent function
def pdf_agent(new: bool = False, user: str = "user"):
    """
    Run the PDF-based AI agent.
    Args:
        new (bool): Start a new session or continue an existing one.
        user (str): User ID for session management.
    """
    session_id: Optional[str] = None

    # Retrieve existing session if available
    if not new:
        try:
            existing_sessions: List[str] = storage.get_all_session_ids(user)
            if len(existing_sessions) > 0:
                session_id = existing_sessions[0]
        except Exception as e:
            logging.error(f"Error fetching existing sessions: {e}")

    # Initialize the agent
    try:
        agent = Agent(
            session_id=session_id,
            user_id=user,
            knowledge=knowledge_base,
            storage=storage,
            show_tool_calls=True,
            read_chat_history=True,
        )

        # Print session details
        if session_id is None:
            session_id = agent.session_id
            print(f"Started a new session: {session_id}\n")
        else:
            print(f"Continuing session: {session_id}\n")

        # Run the CLI app
        agent.cli_app(markdown=True)

    except Exception as e:
        logging.error(f"Error initializing the agent: {e}")

# Main entry point
if __name__ == "__main__":
    typer.run(pdf_agent)
