import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from pytrends.request import TrendReq
import plotly.graph_objects as go
import os 
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

# Initializing Google Trends
pytrends = TrendReq(hl='en-US', tz=360)
os.environ["HUGGINGFACEHUB_API_TOKEN"] ="add api token" 

DuckDuck_result = DuckDuckGoSearchResults(handle_tool_error=True, handle_validation_error=True)

# Function to fetch trends data for multiple keywords
def fetch_trends_data(queries):
    pytrends.build_payload(queries, timeframe='today 3-m')  # Last 3 months
    data = pytrends.interest_over_time()
    
    if data.empty:
        return {"Error": "No trends data found for these queries."}
    
    data = data.reset_index()
    print(data)
    return data

# Tool to retrieve and display trends data
def trend_search_tool(queries):
    try:
        trends_data = fetch_trends_data(queries)
        if isinstance(trends_data, dict) and "Error" in trends_data:
            return trends_data["Error"]
        fig = go.Figure()
        
        # Add each query's trend data to the chart
        for query in queries:
            fig.add_trace(go.Scatter(
                x=trends_data['date'], 
                y=trends_data[query],
                mode='lines+markers',
                name=query
            ))

        fig.update_layout(
            title="Trend Analysis",
            xaxis_title="Date",
            yaxis_title="Interest Level",
            legend_title="Keywords"
        )
        
        # Display chart in Streamlit
        st.plotly_chart(fig)
        
        # Output trends data and description
        trend_descriptions = []
        for query in queries:
            recent_interest = trends_data[query].iloc[-1]
            trend_descriptions.append(f"The most recent interest level in '{query}' is {recent_interest}.\n")
        
        return {"trends_data": trends_data, "description": " | ".join(trend_descriptions)}
    
    except Exception as e:
        return str(e)

trend_tools = [Tool(
    name="TrendWebSearch",
    func=DuckDuck_result,
    description="Search the web to analyze the trends of user query."
    ),
    Tool(
    name="GoogleTrendSearch",
    func=trend_search_tool,
    description="Fetches trends data from Google Trends based on a given query."
    ),
]

prompt_template = """
You are an intelligent assistant equipped with tools to either search the web or retrieve trend data based on user queries.
Your task is to carefully analyze the query and decide the best tool to respond effectively.

Here are your tools:
- **TrendSearch**: Use this tool to retrieve Google Trends data for topics, keywords, or trending analyses. This tool is ideal for queries related to trends, popularity, or comparisons over time.
- **WebSearch**: Use this tool for general web searches when the user needs the latest information, definitions, or current events not related to trend analysis.

Response Guidelines:
1. **Start with Thought**: Reflect briefly on the user's query and determine which tool to use.
2. **Specify Action**: Choose `TrendSearch` for trends or `WebSearch` for general searches, using `Action: [Tool Name]`.
3. **After Action**: Wait for the tool's result, then analyze or summarize the findings in a helpful and insightful response to the user.

Begin!

{input}
"""

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-Nemo-Instruct-2407",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.5,
    repetition_penalty=1.03,
)

agent=initialize_agent(
    llm=llm,
    agent="zero-shot-react-description",
    tools=trend_tools,
    verbose=True,
    max_iteration=3,
    max_execution_time=600,
    prompt_template=PromptTemplate.from_template(prompt_template),
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

# Streamlit UI for multiple keyword input
st.title("Multi-Keyword Trend Analysis with Google Trends")

# User input for multiple keywords
query_input = st.text_input("Enter topics to analyze trends (separate by commas, e.g., 'Python, JavaScript, php'):")

if query_input:
    # Splitting user input into a list of queries
    queries = [q.strip() for q in query_input.split(",")]
    trend_search_tool(queries)
    response = agent.invoke(query_input)
    
    st.write(response)