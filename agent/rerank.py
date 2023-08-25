from langchain.tools import BaseTool
from typing import Any
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ.get("OPERATOR_API_KEY")

class ContentTool(BaseTool):
    name = "Operator Content Search"
    description = '''
    Use this tool when you need to look up casts (posts) and other content on the Farcaster social network.
    '''

    def _run(self, query: str):

        url = "https://api.operator.io/content/"
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": api_key
        }
        data = {
            "query": query
        }
        
        response = requests.post(url, headers=headers, json=data).json()
        if "matches" not in list(response.keys()):
            raise ValueError("Error while trying to find matches. Is your API key valid?")

        return response["matches"]

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
