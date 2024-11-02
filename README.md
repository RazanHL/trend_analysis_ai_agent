📈 **Multi-Keyword Trend Analysis with LangChain AI Agents**

Welcome to the Multi-Keyword Trend Analysis app! This application leverages AI agents powered by LangChain, integrated with Mistral from Hugging Face, to retrieve and visualize trending data from Google Trends and DuckDuckGo search results based on user queries.

🎯 **Purpose**

This app enables users to:

Analyze trends of multiple keywords using Google Trends API.
Visualize interest levels over time for a comparative view of keyword popularity.
Retrieve real-time web search data for the latest insights.
Whether you’re researching industry trends, comparing interest in programming languages, or simply exploring data for decision-making, this app offers a user-friendly interface with powerful insights!

🛠️ **Features**

**Multi-Keyword Trend Analysis:** Input multiple keywords to analyze and visualize their interest levels over the last 3 months.

**Web Search:** Retrieve related search information for keywords using DuckDuckGo API for a broad view of current relevance and popularity.

**Visualization:** Automatically generated, interactive charts display interest over time.


🚀 **Technologies Used**

**LangChain:** To create and manage AI agents for specific tasks.

**Streamlit:** For building a simple, interactive UI.

**Hugging Face Mistral Model:** To handle NLP tasks for processing user queries.

**Google Trends API (pytrends):** For retrieving interest data for keywords.

**DuckDuckGo API:** For fetching web search results.

**Plotly:** For generating interactive charts to visualize trends data.


🧩 **Getting Started**

Prerequisites
Python 3.7+
Hugging Face API token: Necessary for accessing the Mistral model on Hugging Face.
Google Trends API (pytrends): Install via pip install pytrends.
Other dependencies: Streamlit, Plotly, LangChain, etc.

**Enter Keywords:** Enter multiple keywords separated by commas (e.g., Python, JavaScript, PHP) into the input box to fetch their trend data and web search results.

**View Trends:** The app will retrieve the trend data, display a comparative chart, and generate a summary of the latest interest levels for each keyword. Additionally, any related web search information is displayed to give broader context.


📊 **Example Output**

Trend Analysis Chart: A line chart comparing the interest over time for each keyword.
Latest Interest Summary: Displays the most recent interest levels for each keyword.
Web Search Insights: Provides related, up-to-date information from DuckDuckGo to supplement trends data.
🤖** Agent Logic**
This app uses a LangChain AI agent to dynamically select the appropriate tool based on user input:

GoogleTrendSearch: Retrieves and visualizes trend data for the given keywords.
TrendWebSearch: Uses DuckDuckGo to gather additional context and recent developments related to the keywords.
