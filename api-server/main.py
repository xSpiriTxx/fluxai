from fastapi import FastAPI, Request, HTTPException
import requests
import numpy as np

app = FastAPI()

FAISS_URL = "http://faiss-server:8081"
MODEL_SERVER_URL = "http://model-server:8501/generate"
SCRAPER_URL = "http://scraping-service:8002/scrape"

@app.post("/add-url")
async def add_url(request: Request):
    data = await request.json()
    url = data.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # Scrape the data from the URL
    scrape_response = requests.post(SCRAPER_URL, json={"url": url})
    if scrape_response.status_code != 200:
        raise HTTPException(status_code=scrape_response.status_code, detail="Error scraping the URL")
    
    scraped_content = scrape_response.json().get("content")

    # Convert scraped content to a vector (assume some_embedding_function exists)
    vector = some_embedding_function(scraped_content)

    # Add the vector to FAISS
    faiss_response = requests.post(f"{FAISS_URL}/add_vector", json={"vector": vector.tolist()})
    if faiss_response.status_code != 200:
        raise HTTPException(status_code=faiss_response.status_code, detail="Error adding vector to FAISS")
    
    return {"message": "URL data added to FAISS"}

@app.post("/remove-url")
async def remove_url(request: Request):
    data = await request.json()
    url = data.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # Here you would likely have some mechanism to identify and remove the specific vector related to the URL from FAISS.
    # This could involve storing metadata linking URLs to vectors, and then removing based on that metadata.
    # This is a placeholder implementation:
    faiss_response = requests.post(f"{FAISS_URL}/remove_vector", json={"url": url})
    if faiss_response.status_code != 200:
        raise HTTPException(status_code=faiss_response.status_code, detail="Error removing vector from FAISS")
    
    return {"message": "URL data removed from FAISS"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    input_text = data.get("input")
    
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text is required")
    
    # Convert input to a vector (assume some_embedding_function exists)
    query_vector = some_embedding_function(input_text)

    # Query FAISS for related data
    faiss_response = requests.post(f"{FAISS_URL}/search", json={"query_vector": query_vector.tolist()})
    if faiss_response.status_code != 200:
        raise HTTPException(status_code=faiss_response.status_code, detail="Error querying FAISS")

    related_data = faiss_response.json().get("indices", [])

    # Combine the retrieved data with the user's input
    combined_input = f"{related_data} {input_text}"

    # Send combined input to the model server
    model_response = requests.post(MODEL_SERVER_URL, json={"input": combined_input})
    if model_response.status_code != 200:
        raise HTTPException(status_code=model_response.status_code, detail="Error generating response from model server")

    return {"response": model_response.json().get("response")}

# Placeholder function for generating embeddings
def some_embedding_function(text):
    # Implement your text embedding here, e.g., using a pre-trained model like BERT, Sentence Transformers, etc.
    # This function should return a vector representation of the input text.
    return np.random.rand(128)  # Dummy implementation; replace with actual embedding generation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
