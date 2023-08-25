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
    IMPORTANT: if the user has asked about casts by a specific author, you must have found the author's farcaster username and associated FID first.
    '''

    def _run(self, query: str, fid: Optional[int]):

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
                "casts_in_thread": [{x["hash"]: x["content"]} for x in match["casts"]]
            })


        return condensed_data
        return str([thread["content"] for thread in response["matches"][:10]])

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
