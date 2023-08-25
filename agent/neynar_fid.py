from langchain.tools import BaseTool
from typing import Any
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ.get("NEYNAR_API_KEY")

class AddressToFidTool(BaseTool):
    name = "Address to Farcaster ID"
    description = '''
    As soon as you find an address for an entity, you must use this tool next to get the associated FID.
    You will need the FID to do the next step, finding content created by this FID.
    '''

    def _run(self, custody_address: str):
        url = f"https://api.neynar.com/v1/farcaster/user-by-verification/?api_key={api_key}&address={custody_address}"
        response = requests.get(url).json()
        if "result" not in list(response.keys()):
            raise ValueError("Error while trying to find matches. Is your API key valid?")
        
        # TODO: too many tokens used so need to just create id: content pairs and have the llm analyze it and rerank in the rerank tool
        # llm chain should use the response of that and then figure out which ones to actually include in the response back
        # for match in response["matches"]:
        return response["result"]["user"]["fid"]
        return str([thread["content"] for thread in response["matches"][:10]])

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
