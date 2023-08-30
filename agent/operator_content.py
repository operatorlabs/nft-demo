from langchain.tools import BaseTool
from typing import Any, Optional
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ.get("OPERATOR_API_KEY")

class ContentTool(BaseTool):
    name = "Operator Content Search"
    description = '''
    Use this tool when you need to look up casts (posts) and other content on the Farcaster social network.
    IMPORTANT NOTES TO FOLLOW:
    1. if the user has asked about casts by a specific author, you must have found the author's farcaster username and associated FID first.
    2. you must evaluate the result from this tool to see if all the casts are actually relevant to the user's query.
    '''

    def _run(self, query: str, fid: Optional[int] = None):

        url = "https://api.operator.io/content/"
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": api_key
        }
        data = {
            "query": query
        }
        if fid:
            data.update({"fid": int(fid)})
        response = requests.post(url, headers=headers, json=data).json()
        if "matches" not in list(response.keys()):
            raise ValueError("Error while trying to find matches. Is your API key valid?")
        
        # TODO: too many tokens used so need to just create id: content pairs and have the llm analyze it and rerank in the rerank tool
        # llm chain should use the response of that and then figure out which ones to actually include in the response back
        condensed_data = []
        for match in response["matches"]:
            condensed_data.append({
                "thread_id": match["hash"],
                "casts_in_thread": [{x["hash"]: x["content"], "author_fid": int(x["metadata"]["user_fid"])} for x in match["casts"]]
            })


        return condensed_data[:50]

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
