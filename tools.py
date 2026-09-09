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

@tool
def web_scraper(url:str)->str:
    """Scrap and return clean text from a given url for deeper reading"""
    try:
        res=requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(res.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]

    except Exception as e:
        return f"Couldn't scrape the url web page"




print(web_scraper.invoke("https://apnews.com/hub/iran"))