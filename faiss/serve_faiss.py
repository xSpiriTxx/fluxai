import faiss
import numpy as np
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Configuration
INDEX_FILE_PATH = "faiss_index_file.index"
DIMENSION = 128  # Example dimension of the vectors

# Load or create a FAISS index
try:
    index = faiss.read_index(INDEX_FILE_PATH)
    print("FAISS index loaded from disk.")
except Exception as e:
    print("Creating a new FAISS index.")
    index = faiss.IndexFlatL2(DIMENSION)

@app.post("/add_vector")
async def add_vector(request: Request):
    data = await request.json()
    vector = np.array(data["vector"], dtype=np.float32).reshape(1, -1)
    index.add(vector)

    # Save the index to disk after adding a new vector
    faiss.write_index(index, INDEX_FILE_PATH)

    return {"status": "Vector added and index saved"}

@app.post("/search")
async def search(request: Request):
    data = await request.json()
    query_vector = np.array(data["query_vector"], dtype=np.float32).reshape(1, -1)
    distances, indices = index.search(query_vector, k=5)
    return {"distances": distances.tolist(), "indices": indices.tolist()}

@app.on_event("shutdown")
def shutdown_event():
    # Save the index when the server shuts down
    faiss.write_index(index, INDEX_FILE_PATH)
    print("FAISS index saved to disk during shutdown.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
