from langchain.tools import BaseTool
from typing import Any
import os
from dotenv import load_dotenv
import operatorio

load_dotenv()

api_key = os.getenv("OPERATOR_API_KEY")

class OperatorTool(BaseTool):
    name = "Operator Address Search"
    description = '''
    Use this tool when you need to find the right address for a specific project.
    Possible options for entity_type are nft, identity, wallet, contract, and token.
    Use the full name of the blockchain in question, i.e. "Ethereum" instead of "ETH".
    Default to Ethereum if no blockchain is specified. Search for names as is, do not attempt to interpret spelling errors.
    '''

    def _run(self, search: str, blockchain: str, entity_type: operatorio.EntityType):

        # Initialize the OperatorSearchAPI with the retrieved API key
        api = operatorio.OperatorSearchAPI(api_key)

        # Define a query to search for the task
        query = operatorio.Query(
            query=search, # Query for "query"
            blockchain=blockchain, # Query for given blockchainç
            entity_type=entity_type, # Query for given entity type
            query_by=[] # Query by all fields (default)
        )
        
        # Use the OperatorSearchAPI to perform the search
        entities = api.search(query)

        # Return the top result's address
        return entities.matches[0].address if entities.matches else None

    def _arun(self, task: Any):
        raise NotImplementedError("This tool does not support async")
