async def process_batch(batch):
    image_tasks = []
    request_ids = []

    for request_id, request in batch:
        for message in request.messages:
            if message.role == "user":
                for content in message.content:
                    if content["type"] == "image_url":
                        image_tasks.append(fetch_image(content["image_url"]))
                        request_ids.append(request_id)

    # Process all images asynchronously
    images = await asyncio.gather(*image_tasks)

    # Run detection
    answers = []
    for img in images:
        with torch.no_grad():
            answer = moondream.detect(img, tokenizer=tokenizer)  # Adjust this call as per your model API
        answers.append(answer)

    # Send back results
    for i, request_id in enumerate(request_ids):
        response = ChatResponse(choices=[{"text": answers[i]}])
        response_map[request_id] = response
