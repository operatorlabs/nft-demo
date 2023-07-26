## NFT Agent using Operator, Reservoir, Chroma, and Langchain Agents

This agent demo uses [Operator](https://operator.io), [Reservoir](https://reservoir.tools), and [Langchain Agents](https://langchain.com) to create an NFT assistant that is capable
of retrieving information about any NFT project. 

The chat agent uses two primary tools, Operator and Reservoir. Operator is used to find the contract address of NFT's, and Reservoir is used to retrieve associated metadata. 

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

## adding new tools 

To modify this repo to work with other API's:
1. download the openapi.json spec associated with the API
2. add the spec to the schemas directory
3. run the loader.py script in the scripts folder
4. copy/paste the reservoir.py tool, then modify the name and description of the tool
5. add the tool to the agent you are using, whether that is the agent_with_ui.py or the agent.py file.

```
import your_tool

tools = [OperatorTool(), ReservoirTool(), # add your tool here]
```

6. run the agent depending on which agent you are using.
