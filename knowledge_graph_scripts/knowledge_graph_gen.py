#!/usr/bin/env python
"""
Utilizing gpt-3.5-turbo model from OpenAI this script will auth in to their API to run \
text in the ./text_file folder. Ensure utils.py is within the folder to pull from. 

Author: Shayon Keating
Date: February 23, 2024
"""

# !pip install networkx matplotlib
# !pip install openai
# !pip install requests


# import reqs
import requests
import os
import re
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from openai import OpenAI
from utils import read_api_key

# Global Constants API endpoint, API key, prompt text
text_files = './text_files'
api_key_file_path = './auth/api_key.txt'
api_key = read_api_key(api_key_file_path)
prompt_text = """Based on the given prompt, identify and enumerate all possible connections, then compile a summary of updates. 
For each update involving a connection, format it as [ENTITY 1, CONNECTION, ENTITY 2]. This connection is directional, 
indicating the sequence is significant.
Example:
prompt: The Sun generates solar energy and is also responsible for Vitamin D production.
updates:
[["Sun", "generates", "solar energy"], ["Sun", "responsible for", "Vitamin D"]]
prompt: $prompt
updates:"""
client = OpenAI(api_key = api_key) # Initialize the OpenAI client with your API key


def call_gpt_api(prompt_text):
    """
    Function will make an API call to OpenAIs API for gpt-3.5-turbo
    
    Args: prompt text
    
    Ouptut: api response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response)
        return response
    except Exception as e:
        print("Error:", e)
        return None


def preparing_data_for_graph(api_response):
    """
    Function will take previous api reseponse and correctly parse through it preparing it for creating a \
    knowledge graph
    
    Args: api_response
    
    Ouptut: parsed data returning a dataframe and relational labels
    """
    if api_response is None:
        print("API response is None. Exiting function.")
        return None, None
    
    try:
        # Accessing the 'content' from the API response
        response_text = api_response.choices[0].message.content

        # Remove enumeration and prepare the content for JSON parsing
        cleaned_content = re.sub(r'\d+\.\s+', '', response_text)  # Remove leading numbers and spaces
        cleaned_content = '[' + ','.join(cleaned_content.split('\n')) + ']' 
        structured_data = json.loads(cleaned_content)

        # Remove one level of nesting from structured_data in linked list
        # Each item should be a list with three elements: source, relation, target
        structured_data = [item[0] for item in structured_data if isinstance(item, list) and len(item) > 0]

        # Extract source, target, and relations while ensuring list has enough elements
        source = [item[0] for item in structured_data if len(item) > 2]
        target = [item[2] for item in structured_data if len(item) > 2]
        relations = [item[1] for item in structured_data if len(item) > 2]

        # Create DataFrame from the extracted elements
        kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
        relation_labels = dict(zip(zip(kg_df.source, kg_df.target), kg_df.edge))

        return kg_df, relation_labels
    except Exception as e:
        print(f"Error processing API response: {e}")
        return None, None


# Graph Creation Function
def create_graph(df, rel_labels):
    """
    Function takes previous dataframe and relational labels and creates a knowledge graph
    
    Args: previous dataframe and relational labels
    
    Ouptut: graph image saved to the save path
    """
    G = nx.from_pandas_edgelist(df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    plt.figure(figsize=(12, 12), dpi=100)  # Increased DPI for better resolution

    pos = nx.spring_layout(G, k=0.5)  # Adjust layout parameters
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', width=2, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=rel_labels, font_color='red')

    save_path = os.path.join('text_files', 'graph_image.png')
    plt.savefig(save_path)  # Save the figure before showing it
    plt.show()  # Show the plot
    plt.close()  # Close the figure to ensure clean state for next plot

    print(f"Graph image saved to: {save_path}")


# Graph Creation Function
def main(text_file_path):
    """
    Main function that will open the text file from the video/audio file and then utilize the call_gpt_api \
    function, then if the api_response is correct it will prep the data for the graph and then \
    create the graph and output it.
    
    Args: text file pathway and the pathway should contain the text file
    
    Ouptut: graph image
    """
    with open(text_file_path, 'r') as file:
        kb_text = file.read()
    global prompt_text
    prompt_text = prompt_text.replace("$prompt", kb_text)

    api_response = call_gpt_api(prompt_text)  # call gpt function
    if api_response:
        df, rel_labels = preparing_data_for_graph(api_response)  # build the data graph
        
        # Toss an error if no graph is made cause dict is empty
        if df is not None and rel_labels is not None:
            create_graph(df, rel_labels)
        else:
            print("Data preparation failed. Unable to create graph.")
    else:
        print("API call failed. Unable to process the text file.")


def start(directory_path):
    """
    Starts the main function and locates the .txt file if it exists
    
    Args: text file path
    
    Ouptut: graph image saved to the save path
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            # Construct the full path to the text file
            text_file_path = os.path.join(directory_path, filename)
            # Call the main function for each text file
            main(text_file_path)