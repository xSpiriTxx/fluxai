from fastapi import FastAPI, Request, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.post("/scrape")
async def scrape(request: Request):
    data = await request.json()
    url = data.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch the URL")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text_content = soup.get_text()
    
    # In a real application, you might want to process or store the scraped data here.
    # For now, we just return the text content.
    return {"content": text_content}

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "Scraper is running"}
