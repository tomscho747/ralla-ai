
# POST `${BASE_URL}/v1/chat/completions`

This endpoint sends a chat-style interaction to the **Qwen2.5-VL-3B-Instruct** model, supporting **multimodal inputs** such as text and image URLs.

---

## 🔐 Headers

```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

---

## 📥 Request Body

```json
{
  "model": "Qwen2.5-VL-3B-Instruct",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://modelscope.oss-cn-beijing.aliyuncs.com/resource/qwen.png"
          }
        },
        {
          "type": "text",
          "text": "What is the text in the illustrate?"
        }
      ]
    }
  ]
}
```

### 🧾 Request Field Definitions

| Field                | Type       | Required | Description                                                                 |
|---------------------|------------|----------|-----------------------------------------------------------------------------|
| `model`             | string     | ✅       | The model name to use (e.g., `"Qwen2.5-VL-3B-Instruct"`).                   |
| `messages`          | array      | ✅       | An array of message objects simulating a conversation.                     |
| `role`              | string     | ✅       | Role of the message sender (`"system"`, `"user"`, or `"assistant"`).       |
| `content`           | string or array | ✅  | Can be a plain string or an array of multimodal content.                   |
| `type`              | string     | ✅       | `"image_url"` for image input or `"text"` for plain text input.            |
| `image_url.url`     | string     | ✅ (if type is image) | A public URL to an image (e.g. PNG, JPG).                                  |
| `text`              | string     | ✅ (if type is text)  | The user query or instruction in plain text.                               |

---

## 📤 Example Response

```json
{
  "id": "chatcmpl-eedff2261ece402798453c6740497bd4",
  "object": "chat.completion",
  "created": 1751329548,
  "model": "Qwen2.5-VL-3B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": null,
        "content": "The text in the illustration reads \"TONGYI Qwen.\"",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 73,
    "completion_tokens": 15,
    "total_tokens": 88,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null,
  "kv_transfer_params": null
}
```

### 🧾 Response Field Definitions

| Field                        | Type       | Description                                                                 |
|-----------------------------|------------|-----------------------------------------------------------------------------|
| `id`                        | string     | Unique ID for the completion session.                                      |
| `object`                    | string     | Type of object returned (`"chat.completion"`).                             |
| `created`                   | integer    | Unix timestamp of when the request was processed.                          |
| `model`                     | string     | Model used for the completion.                                             |
| `choices`                   | array      | List of generated responses.                                               |
| `choices[].index`           | integer    | Index of the current choice (useful if multiple outputs are requested).    |
| `choices[].message.role`    | string     | Role of the responder (`"assistant"`).                                     |
| `choices[].message.content` | string     | The actual text response from the model.                                   |
| `choices[].message.reasoning_content` | string\|null | Any intermediate reasoning (null if not applicable).              |
| `choices[].tool_calls`      | array      | List of tool calls made by the model, if any (empty if none).             |
| `choices[].logprobs`        | object\|null | Log probabilities of token predictions (null if not returned).           |
| `choices[].finish_reason`   | string     | Reason the generation stopped (e.g., `"stop"`, `"length"`, etc.).         |
| `choices[].stop_reason`     | string\|null | Further explanation of stop condition (if any).                           |
| `usage.prompt_tokens`       | integer    | Number of tokens in the input prompt.                                     |
| `usage.completion_tokens`   | integer    | Number of tokens in the model’s reply.                                    |
| `usage.total_tokens`        | integer    | Sum of prompt and completion tokens.                                      |
| `usage.prompt_tokens_details` | object\|null | More granular token details (optional).                                |
| `prompt_logprobs`           | object\|null | Token-level log probabilities for prompt (optional).                   |
| `kv_transfer_params`        | object\|null | Internal use (e.g., for model state transfer).                            |

---

### 💬 Extracted Content from Image

> **"The text in the illustration reads 'TONGYI Qwen.'"**
