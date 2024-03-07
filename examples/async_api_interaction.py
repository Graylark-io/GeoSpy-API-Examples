import aiohttp
import asyncio
import time
import base64
import logging
from aiohttp import ClientTimeout

# Configuration variables
BASE_URL = "https://dev.geospy.ai"  # Base URL of the GeoSpy API
ROUTE = "/predict"  # Specific endpoint route for predictions
API_KEY = "YOUR_API_KEY"  # Your API key for authentication, replace with actual key
ENDPOINT_URL = BASE_URL + ROUTE  # Full endpoint URL
CONCURRENT_REQUESTS = 2  # Max number of requests to be sent concurrently
TOTAL_REQUESTS = 4  # Total number of requests to send
REQUEST_INTERVAL = 0.01  # Time in seconds to wait between each batch of concurrent requests
MAX_RETRIES = 5  # Max number of retry attempts for each request
RETRY_BACKOFF = 2  # Factor to determine delay between retries (exponential backoff)
TIMEOUT_SECONDS = 30  # Timeout in seconds for each request

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def encode_image_to_base64(path_to_image: str) -> str:
    """Encode an image file to a base64 string for transmission over HTTP."""
    with open(path_to_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

async def send_request(session, image_base64: str, request_number: int) -> dict:
    """
    Asynchronously sends a single POST request to the specified API endpoint.

    Implements retry logic with exponential backoff in case of failure, and logs the outcome of each request.

    Args:
        session: The aiohttp session used for HTTP requests.
        image_base64: Base64-encoded string of the image.
        request_number: Identifier for the request, used for logging.

    Returns:
        A dictionary containing the response data or an error message.
    """
    payload = {
        "inputs": {"image": image_base64},
        "top_k": 5,  # Optional, specifies the number of top results to return
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    # Retry logic with exponential backoff
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with session.post(ENDPOINT_URL, headers=headers, json=payload, timeout=ClientTimeout(total=TIMEOUT_SECONDS)) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"Request {request_number}: Success")
                    return result
                else:
                    logging.error(f"Request {request_number}: Failed with status {response.status}")
                    if attempt == MAX_RETRIES:
                        return {"error": f"HTTP error {response.status}"}
        except aiohttp.ClientError as e:
            logging.error(f"Request {request_number}: Attempt {attempt} failed with error: {e}")
            if attempt == MAX_RETRIES:
                return {"error": "ClientError or Timeout"}
        await asyncio.sleep(RETRY_BACKOFF ** (attempt - 1))

async def main():
    """Encodes an image to base64 and sends multiple asynchronous POST requests to the API."""
    path_to_image = 'sample_images/bar.jpg'  # Adjust path as necessary
    image_base64 = await encode_image_to_base64(path_to_image)
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, image_base64, i + 1) for i in range(TOTAL_REQUESTS)]
        for i in range(0, len(tasks), CONCURRENT_REQUESTS):
            chunk = tasks[i:i + CONCURRENT_REQUESTS]
            await asyncio.gather(*chunk)
            await asyncio.sleep(REQUEST_INTERVAL)  # Enforces rate limit

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    logging.info(f"Execution time: {end_time - start_time} seconds")
