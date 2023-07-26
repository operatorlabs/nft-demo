## operator nft demo 

Demo uses [Operator](https://operator.io), [Reservoir](https://reservoir.tools), and [Langchain Agents](https://langchain.com) to create an NFT assistant that is capable
of retrieving information about any NFT project. 

The chat agent uses two primary tools, Operator and Reservoir. Operator is used find the contract address of NFT's, and Reservoir is used to retrieve associated metadata. 

To modify this repo to work with other API's, run the loader.py script in the scripts folder, and then copy/paste the reservoir.py tool. Modify the name and description of this new tool, and then add it to the agents. 

## running the demo locally

Navigate to the agent directory and run the following command:

```
streamlit run agent_with_ui.py
```

