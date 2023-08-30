from langchain.tools import BaseTool
from typing import Any, List
import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
api_key = os.environ.get("NEYNAR_SQL_API_KEY")

class SearchInChannelTool(BaseTool):
    name = "Search in channel"
    description = '''
    Use this tool to search for content specific to a channel. You must provide a channel URL as the parameter channel_url.
    '''

    def _run(self, query: str, channel_url: str):
        url = 'https://data.hubs.neynar.com/api/queries/15/results'
        params = {'api_key': api_key}
        payload = {
            "max_age": 1800,
            "parameters": {
                "query": query,
                "channel_url": channel_url
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, params=params, headers=headers, json=payload).json()
        if "query_result" not in list(response.keys()):
            if "job" not in list(response.keys()):
                raise ValueError("Error while trying to find matches. Is your API key valid?")
            else:
                time.sleep(1)
                response = requests.post(url, params=params, headers=headers, json=payload).json()
                if "query_result" not in list(response.keys()):
                    raise ValueError("Error while trying to find matches. Is your API key valid?")
                
        rows = response["query_result"]["data"]["rows"]
        result = []
        for row in rows:
            result.append({
                "hash": row["hash"],
                "updated_at": row["updated_at"],
                "author_fid": row["fid"],
                "content": row["text"]
            })
        return result

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
