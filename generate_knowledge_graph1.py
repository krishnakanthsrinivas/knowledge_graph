from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from pyvis.network import Network

from dotenv import load_dotenv
import os
import asyncio


# Load .env
load_dotenv()

# Get GROQ API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize FREE LLM (Llama-3-70B or 8B)
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"      # You can also use: llama3-8b-8192
)

# Graph transformer using Groq LLM
graph_transformer = LLMGraphTransformer(llm=llm)


# ---------------------- GRAPH EXTRACTION ----------------------
async def extract_graph_data(text):
    """
    Asynchronously extracts graph data from input text using Groq LLM.
    """
    documents = [Document(page_content=text)]
    graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_documents


# ---------------------- GRAPH VISUALIZATION ----------------------
def visualize_graph(graph_documents):
    """
    Visualizes a knowledge graph using PyVis.
    """
    net = Network(
        height="1200px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#222222",
        font_color="white",
        filter_menu=True,
        cdn_resources="remote",
    )

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    node_dict = {node.id: node for node in nodes}

    valid_edges = []
    valid_node_ids = set()

    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            net.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue

    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except:
            continue

    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)

    output_file = "knowledge_graph.html"
    try:
        net.save_graph(output_file)
        print(f"Graph saved to {os.path.abspath(output_file)}")
        return net
    except Exception as e:
        print(f"Error saving graph: {e}")
        return None



# ---------------------- MAIN PIPELINE FUNCTION ----------------------
def generate_knowledge_graph(text):
    """
    Run extraction + visualization using FREE GROQ API.
    """
    graph_documents = asyncio.run(extract_graph_data(text))
    net = visualize_graph(graph_documents)
    return net
