from langchain.tools import BaseTool
from typing import Any, List, Optional
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ.get("NEYNAR_API_KEY")

class FollowedByFidTool(BaseTool):
    name = "Find accounts followed by FID"
    description = '''
    Useful for when you need to figure out what accounts are followed by another user's FID.
    You must pass in the FID in as the 'fid' parameter when using this tool.
    If you want to check if one FID follows a set of FIDs, pass in the set of FIDs you want to check  as the 'fids_to_check' parameter.
    '''

    def _run(self, fid: str, fids_to_check: Optional[List[str]] = None):
        url = f"https://api.neynar.com/v1/farcaster/following/?api_key={api_key}&fid={fid}"
        response = requests.get(url).json()
        if "result" not in list(response.keys()):
            raise ValueError("Error while trying to find matches. Is your API key valid?")
        
        # TODO: it should be by follower count when implemented
        # users = [{"fid": x["fid"], "followerCount": } for x in response["result"]["users"]]

        users = response["result"]["users"]
        sorted_by_followers = sorted(users, key = lambda e: e["followerCount"], reverse=True)

        if fids_to_check:
            following = set(x["fid"] for x in sorted_by_followers)
            to_check = set(fids_to_check)
            return [x for x in following.intersection(to_check)]
        else:
            return [x["fid"] for x in sorted_by_followers[:500]]

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
