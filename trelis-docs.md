🧠 FastAPI Image+Text AI Inference Server
This FastAPI application serves a batch-based AI inference endpoint that supports multi-modal inputs (text + images), using the Moondream2 model from Hugging Face.

✨ Features
Accepts user prompts with optional image URLs.

Batches incoming requests for efficient GPU usage.

Uses Hugging Face Transformers (AutoTokenizer, AutoModelForCausalLM).

Automatically fetches and decodes remote images.

Asynchronously processes incoming requests via background threading and asyncio.

📦 Requirements
Python 3.8+

PyTorch (with GPU support)

FastAPI

httpx

transformers

Pillow

Install dependencies:

bash
Copy
Edit
pip install fastapi[all] transformers torch httpx pillow
⚙️ Environment Variables
Variable	Description	Default
BATCH_SIZE	Number of requests to process in a single batch	5
BATCH_TIMEOUT	Max wait time (in seconds) before batch is processed	1.0
MODEL_ID	Hugging Face model ID	vikhyatk/moondream2
REVISION	Model revision to pull	2024-04-02
HF_HUB_ENABLE_HF_TRANSFER	Hugging Face setting for efficient loading	1

🧠 Model
Model ID: vikhyatk/moondream2

Capability: Multi-modal (Text + Image) chat-style model

Tokenizer: Loaded from same Hugging Face repo

Device: CUDA (GPU required)

📥 API Endpoint
POST /chat/completions
Handles a chat completion request with text and optional images.

🔤 Request Body
json
Copy
Edit
{
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "What’s happening in this image?" },
        { "type": "image_url", "image_url": "https://example.com/image.jpg" }
      ]
    }
  ]
}
role: Currently supports only "user".

content: A list of items. Can be text or image_url.

✅ Response
json
Copy
Edit
{
  "choices": [
    {
      "text": "It looks like a dog playing in a park."
    }
  ]
}
🧵 Internal Architecture
Startup Phase: Loads model and tokenizer on GPU and starts a background processing thread.

Queue-Based Processing:

Incoming requests are queued (Queue).

Background thread collects requests and forms a batch.

Uses asyncio.run() to asynchronously fetch images and pass data to the model.

Model Inference:

Fetches remote images using httpx.

Passes prompts and images to moondream.batch_answer(...).

Response Mapping:

Each request has a unique ID and is matched to its response via a global map.

🛠️ Development
Run locally
bash
Copy
Edit
uvicorn app:app --reload
Replace app:app with the actual filename if different.

🧪 Example Test
bash
Copy
Edit
curl -X POST http://localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "messages": [
          {
            "role": "user",
            "content": [
              { "type": "text", "text": "Describe this image" },
              { "type": "image_url", "image_url": "https://example.com/cat.jpg" }
            ]
          }
        ]
      }'
🧹 TODO / Improvements
Add support for multiple user/assistant message turns

Handle image fetch failures more gracefully

Extend batching to support more complex input aggregation

Add support for max_tokens, temperature, etc.

