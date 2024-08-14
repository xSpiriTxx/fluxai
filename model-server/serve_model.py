import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fastapi import FastAPI, Request

# Retrieve the API token from the environment variable
# token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# if token is None:
#     raise ValueError("Hugging Face API token not found in environment variables.")

# print(f"Using Hugging Face API token: {token}")

app = FastAPI()

# Model ID for LLaMA
# model_id = "meta-llama/Meta-Llama-3-8B"
model_id = "EleutherAI/gpt-j-6B"

# Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
# model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, token=token, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    input_text = data.get("input")
    
    if not input_text:
        return {"error": "Input text is required"}
    
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    # Generate text using the model
    outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)
    
    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {"response": generated_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
