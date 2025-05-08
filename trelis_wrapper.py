from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Union
from PIL import Image
from io import BytesIO
import httpx
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from queue import Queue, Empty
from threading import Thread
import asyncio
import os
import time

# Environment Variables
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 5))
BATCH_TIMEOUT = float(os.getenv('BATCH_TIMEOUT', 1.0))
MODEL_ID = os.getenv('MODEL_ID', "vikhyatk/moondream2")
HF_HUB_ENABLE_HF_TRANSFER = os.getenv("HF_HUB_ENABLE_HF_TRANSFER", "1")
REVISION = os.getenv("REVISION", '2024-04-02')

app = FastAPI()

class Message(BaseModel):
    role: str
    content: List[Dict[str, Union[str, int]]]

class ChatRequest(BaseModel):
    messages: List[Message]
    # max_tokens: int

class ChatResponse(BaseModel):
    choices: List[Dict[str, str]]

request_queue = Queue()
response_map = {}

@app.on_event("startup")
async def startup_event():
    global tokenizer, moondream, thread
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)
    device = 'cuda'
    moondream = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=REVISION,
        trust_remote_code=True
    ).to(device=device)
    moondream.eval()

    thread = Thread(target=process_requests, daemon=True)
    thread.start()

@app.post("/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    request_id = id(request)
    request_queue.put((request_id, request))
    while True:
        await asyncio.sleep(0.1)
        if request_id in response_map:
            response = response_map.pop(request_id)
            if isinstance(response, Exception):
                raise HTTPException(status_code=500, detail=str(response))
            return response

async def fetch_image(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))

def process_requests():
    while True:
        try:
            batch = []
            start_time = time.time()
            while len(batch) < BATCH_SIZE and (time.time() - start_time) < BATCH_TIMEOUT:
                try:
                    request_id, request = request_queue.get(timeout=BATCH_TIMEOUT - (time.time() - start_time))
                    batch.append((request_id, request))
                except Empty:
                    continue
            if batch:
                asyncio.run(process_batch(batch))
        except Exception as e:
            print(f"Error processing batch: {e}")

async def process_batch(batch):
    image_tasks = []
    prompts = []
    request_ids = []
    for request_id, request in batch:
        request_ids.append(request_id)
        for message in request.messages:
            if message.role == "user":
                for content in message.content:
                    if content["type"] == "image_url":
                        image_tasks.append(fetch_image(content["image_url"]))
                    elif content["type"] == "text":
                        prompts.append(content["text"])
    
    images = await asyncio.gather(*image_tasks)
    answers = moondream.batch_answer(images=images, prompts=prompts, tokenizer=tokenizer)
    
    for i, request_id in enumerate(request_ids):
        response = ChatResponse(choices=[{"text": answers[i]}])
        response_map[request_id] = response
