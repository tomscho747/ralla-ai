from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import moondream as md
import threading
import logging
import os
from time import time

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configurable parameters
MODEL_NAME = os.getenv('MODEL_NAME', 'moondream-0_5b-int8.mf')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Thread-safe model instance
model_lock = threading.Lock()
model_instance = None

def get_model():
    global model_instance
    if model_instance is None:
        with model_lock:
            if model_instance is None:  # Double-checked locking
                logging.info("Loading model...")
                model_instance = md.vl(model=MODEL_NAME)
    return model_instance

@app.route('/query', methods=['POST'])
def query():
    start_time = time()
    try:
        logging.info("Processing request...")
        model = get_model()

        # Check if a query is provided
        if 'query' not in request.form:
            logging.warning("Query not provided.")
            return jsonify({'error': 'Query is required'}), 400

        query = request.form['query']

        # Check if an image is provided
        if 'image' not in request.files:
            logging.warning("Image not provided.")
            return jsonify({'error': 'An image is required'}), 400

        image_file = request.files['image']

        try:
            # Load and validate the image
            with Image.open(image_file.stream) as image:
                image.verify()  # Validate that it is a proper image

            # Reload the image after verification for processing
            image_file.stream.seek(0)
            with Image.open(image_file.stream) as image:
                encoded_image = model.encode_image(image)

            # Query the model with the image
            answer = model.query(encoded_image, query)["answer"]

        except UnidentifiedImageError:
            logging.error("Invalid image file provided.")
            return jsonify({'error': 'Invalid image file'}), 400

        end_time = time()
        logging.info("Request processed successfully.")
        return jsonify({'answer': answer, 'processing_time': end_time - start_time})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/caption', methods=['POST'])
def caption():
    start_time = time()
    try:
        logging.info("Processing request...")
        model = get_model()

        # Check if an image is provided
        if 'image' not in request.files:
            logging.warning("Image not provided.")
            return jsonify({'error': 'An image is required'}), 400

        image_file = request.files['image']

        try:
            # Load and validate the image
            with Image.open(image_file.stream) as image:
                image.verify()  # Validate that it is a proper image

            # Reload the image after verification for processing
            image_file.stream.seek(0)
            with Image.open(image_file.stream) as image:
                encoded_image = model.encode_image(image)

            # Query the model with the image
            answer = model.caption(encoded_image)["caption"]

        except UnidentifiedImageError:
            logging.error("Invalid image file provided.")
            return jsonify({'error': 'Invalid image file'}), 400

        end_time = time()
        logging.info("Request processed successfully.")
        return jsonify({'answer': answer, 'processing_time': end_time - start_time})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/detect', methods=['POST'])
def detect():
    start_time = time()
    try:
        logging.info("Processing request...")
        model = get_model()

        # Check if a query is provided
        if 'query' not in request.form:
            logging.warning("Query not provided.")
            return jsonify({'error': 'Query is required'}), 400

        query = request.form['query']

        # Check if an image is provided
        if 'image' not in request.files:
            logging.warning("Image not provided.")
            return jsonify({'error': 'An image is required'}), 400

        image_file = request.files['image']

        try:
            # Load and validate the image
            with Image.open(image_file.stream) as image:
                image.verify()  # Validate that it is a proper image

            # Reload the image after verification for processing
            image_file.stream.seek(0)
            with Image.open(image_file.stream) as image:
                encoded_image = model.encode_image(image)

            # Query the model with the image
            answer = model.detect(encoded_image, query)["objects"]

        except UnidentifiedImageError:
            logging.error("Invalid image file provided.")
            return jsonify({'error': 'Invalid image file'}), 400

        end_time = time()
        logging.info("Request processed successfully.")
        return jsonify({'answer': answer, 'processing_time': end_time - start_time})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/point', methods=['POST'])
def point():
    start_time = time()
    try:
        logging.info("Processing request...")
        model = get_model()

        # Check if a query is provided
        if 'query' not in request.form:
            logging.warning("Query not provided.")
            return jsonify({'error': 'Query is required'}), 400

        query = request.form['query']

        # Check if an image is provided
        if 'image' not in request.files:
            logging.warning("Image not provided.")
            return jsonify({'error': 'An image is required'}), 400

        image_file = request.files['image']

        try:
            # Load and validate the image
            with Image.open(image_file.stream) as image:
                image.verify()  # Validate that it is a proper image

            # Reload the image after verification for processing
            image_file.stream.seek(0)
            with Image.open(image_file.stream) as image:
                encoded_image = model.encode_image(image)

            # Query the model with the image
            answer = model.point(encoded_image, query)["points"]

        except UnidentifiedImageError:
            logging.error("Invalid image file provided.")
            return jsonify({'error': 'Invalid image file'}), 400

        end_time = time()
        logging.info("Request processed successfully.")
        return jsonify({'answer': answer, 'processing_time': end_time - start_time})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info(f"Starting server on {HOST}:{PORT}...")
    app.run(host=HOST, port=PORT)