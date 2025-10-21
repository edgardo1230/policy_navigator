import vertexai
import os
from vertexai import agent_engines
from dotenv import load_dotenv

class App:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
        self.GOOGLE_CLOUD_LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
        self.LOCATION = os.environ["LOCATION"]
        self.PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
        self.COLLECTION_ID  = os.environ["COLLECTION_ID"]
        self.CYMBAL_SEARCH_APP = os.environ["CYMBAL_SEARCH_APP"]       

    def set_up(self):

        import os

        os.environ["GOOGLE_CLOUD_PROJECT"] = self.GOOGLE_CLOUD_PROJECT
        os.environ["GOOGLE_CLOUD_LOCATION"] = self.GOOGLE_CLOUD_LOCATION
        os.environ["LOCATION"] = self.LOCATION
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.GOOGLE_CLOUD_PROJECT
        os.environ["COLLECTION_ID"] = self.COLLECTION_ID
        os.environ["CYMBAL_SEARCH_APP"] = self.CYMBAL_SEARCH_APP

        from agent import root_agent
        ROOT_AGENT=root_agent # the name of the root agent in agent.py
        
        from vertexai.preview.reasoning_engines import AdkApp

        self.app = AdkApp(
            agent=ROOT_AGENT,
            enable_tracing=True,
        )
    def create_session(self, **kw_args):
        return self.app.create_session(**kw_args)
    
    def delete_session(self, **kw_args):
        return self.app.delete_session(**kw_args)
    
    def list_sessions(self, **kw_args):
        return self.app.list_sessions(**kw_args)
    
    def get_session(self, **kw_args):
        return self.app.get_session(**kw_args)
    
    def streaming_agent_run_with_events(self, **kw_args):
        return self.app.streaming_agent_run_with_events(**kw_args)
    
    def stream_query(self, **kw_args):
        return self.app.stream_query(**kw_args)
        
    def register_operations(self):
        return {
            "": [
                "get_session",
                "list_sessions",
                "create_session",
                "delete_session",
            ],
            "stream": [
                "streaming_agent_run_with_events",
                "stream_query",
                ],
        }
        

def deploy_agent_engine_app():
    load_dotenv() 

    GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
    GOOGLE_CLOUD_LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
    STAGING_BUCKET = "gs://qwiklabs-gcp-00-11f32592afd9-hcls-agent-engine-deploy"
    AGENT_DISPLAY_NAME = "Revenue Cycle Advisor"
    AGENT_DESCRIPTION = "Review a denied claim and generate an appeal letter to contest the claim."
  
    vertexai.init(
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    with open('requirements.txt', 'r') as file:
        reqs = file.read().splitlines()

    agent_config =  {
        "agent_engine" : App(),
        "display_name" : AGENT_DISPLAY_NAME,
        "description" : AGENT_DESCRIPTION,
        "requirements": "requirements.txt",
        "extra_packages": [
            "agent.py",
        ],
    }

    existing_agents=list(agent_engines.list(filter=f'display_name="{AGENT_DISPLAY_NAME}"'))

    if existing_agents:
         print("Number of existing agents found for {AGENT_DISPLAY_NAME}:" + str(len(list(existing_agents))))
         print(existing_agents[0].resource_name)
    #     print(existing_agents[1].resource_name)
        
    if existing_agents:
      #update the existing agent
      remote_app = agent_engines.update(resource_name=existing_agents[0].resource_name,**agent_config)
    else:
      #create a new agent
      remote_app = agent_engines.create(**agent_config)
    
    return None


if __name__ == "__main__":
    deploy_agent_engine_app()

