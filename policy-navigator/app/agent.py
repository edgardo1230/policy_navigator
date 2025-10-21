import os

from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.agents import SequentialAgent
from google.adk.tools import VertexAiSearchTool
from bs4 import BeautifulSoup
from markdown import markdown
from policy_navigator.app.instructions import ROOT_INSTRUCTIONS

load_dotenv()

# MODEL ="gemini-2.0-flash"
# MODEL ="gemini-2.0-flash-001"
MODEL = "gemini-2.5-flash"

CONTENT_CONFIG = types.GenerateContentConfig(
    temperature=0.0, # More deterministic output
    max_output_tokens=None,
)

LOCATION = os.getenv('LOCATION')
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
COLLECTION_ID = os.getenv('COLLECTION_ID')
CYMBAL_SEARCH_APP = os.getenv('CYMBAL_SEARCH_APP')
POLICY_NAVIGATOR_APP = os.getenv('POLICY_NAVIGATOR_APP')

cymbal_search_engine = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}/engines/{CYMBAL_SEARCH_APP}"
policy_navigator_search_engine = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}/engines/{POLICY_NAVIGATOR_APP}"
# cymbal_search_engine = "projects/317128714165/locations/us/collections/default_collection/engines/cymbal-search-engine_1752700499166" \

search_data_tool = VertexAiSearchTool(search_engine_id=cymbal_search_engine)
policy_navigator_tool = VertexAiSearchTool(search_engine_id=policy_navigator_search_engine)

def format_appeal_letter(letter: str) -> str:
    md = markdown(letter)
    appeal_letter = ''.join(BeautifulSoup(md, features='html.parser').findAll(text=True))
    return appeal_letter

root_agent = LlmAgent(
    model=MODEL,
    name='policy_navigator_agent',
    description="An AI agent to answer questions based on clinical guidelines, HR policies, or compliance documents.",
    instruction=ROOT_INSTRUCTIONS.strip(),
    tools=[
        search_data_tool,
    ],
    generate_content_config=CONTENT_CONFIG,
)
