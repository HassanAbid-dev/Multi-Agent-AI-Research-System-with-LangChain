from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from tavily import TavilyClient 
from rich import print
import requests
import os
load_dotenv()


tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """Search the web for recent and reliable information on topic.Return Titles, Urls and snippets."""
    results=tavily.search(query=query,max_results=5)
    out=[]

    for r in results["results"]:
        out.append(
            f"Title:{r["title"]}\nURl:{r["url"]}\nContent:{r["content"][:300]}"
        )
    return "\n-----\n".join(out)



print(web_search.invoke("what are the latest news on war."))