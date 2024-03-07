import aiohttp
import asyncio
import base64
import logging
from aiohttp import ClientTimeout

# Configure logging to display the date, log level, and message.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration parameters for the API request.
API_KEY = "YOUR_API_KEY"  # Placeholder for your actual API key.
BASE_URL = "https://dev.geospy.ai"  # The base URL of the GeoSpy API.
ROUTE = "/predict"  # The specific route on the API for predictions.
ENDPOINT_URL = BASE_URL + ROUTE  # Full URL constructed from base and route.
IMAGE_PATHS = ["sample_images/bar.jpg", "sample_images/Arizona.jpg"]  # Paths to the images to be sent to the API.

# Set a custom timeout for aiohttp session to avoid hanging requests.
custom_timeout = ClientTimeout(total=60)  # 60 seconds timeout for API requests.

async def encode_image_to_base64(path_to_image: str) -> str:
    """
    Encodes an image file to a base64 string.

    This function reads the file in binary mode and encodes its content into a base64 string,
    which is suitable for JSON payloads in HTTP requests.

    Args:
        path_to_image: A string path to the image file.

    Returns:
        A base64 encoded string of the image.
    """
    with open(path_to_image, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

async def send_request(session, image_base64: str, image_path: str) -> None:
    """
    Asynchronously sends a POST request to the GeoSpy API with a base64-encoded image.

    This function constructs a JSON payload containing the encoded image and other parameters,
    then sends it to the GeoSpy API endpoint. It handles both successful and unsuccessful
    responses, logging the outcomes appropriately.

    Args:
        session: The aiohttp.ClientSession object for making HTTP requests.
        image_base64: The base64-encoded string of the image.
        image_path: The file path of the image being sent, used for logging purposes.
    """
    payload = {
        "inputs": {"image": image_base64},
        "top_k": 5,  # Number of top predictions to return, assuming the API supports this parameter.
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}',  # Authorization header with the API key.
        'Content-Type': 'application/json',
    }

    try:
        async with session.post(ENDPOINT_URL, json=payload, headers=headers, timeout=custom_timeout) as response:
            if response.status == 200:
                result = await response.json()
                logging.info(f"Success for {image_path}: {result}")
            else:
                logging.error(f"Failed for {image_path} with status code: {response.status}, Message: {await response.text()}")
    except Exception as e:
        logging.error(f"An error occurred for {image_path}: {e}")

async def main():
    """
    Main function to encode images and send asynchronous requests to the GeoSpy API.

    This function iterates over a list of image paths, encodes each to base64, and sends them
    as separate requests to the API. It implements a simple form of rate limiting by
    pausing for one second between initiating each request.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_path in IMAGE_PATHS:
            image_base64 = await encode_image_to_base64(image_path)
            task = asyncio.create_task(send_request(session, image_base64, image_path))
            tasks.append(task)
            await asyncio.sleep(1)  # Pause to implement simple rate limiting.
        await asyncio.gather(*tasks)

# Entry point of the script.
if __name__ == "__main__":
    asyncio.run(main())
