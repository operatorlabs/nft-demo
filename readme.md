## operator nft demo 

Demo uses [Operator](https://operator.io), [Reservoir](https://reservoir.tools), and [Langchain Agents](https://langchain.com) to create an NFT assistant that is capable
of retrieving information about any NFT project. 

The chat agent uses two primary tools, Operator and Reservoir. Operator is used to find the contract address of NFT's, and Reservoir is used to retrieve associated metadata. 

To modify this repo to work with other API's, run the loader.py script in the scripts folder, and then copy/paste the reservoir.py tool. Modify the name and description of this new tool, and then add it to the agents. 

## running the demo locally

To run the demo locally, you will need to install the following dependencies:

```
pip install -r requirements.txt
```

Now, load the endpoint data into Chroma. Navigate to the scripts directory and run the following command:

```
python loader.py
```

This command will embed and organize the endpoint related data into the Chroma database, which is used by the Reservoir tool to retrieve the right endpoint. 

Finally, you can navigate to the agent directory and run the following command:

```
streamlit run agent_with_ui.py
```

