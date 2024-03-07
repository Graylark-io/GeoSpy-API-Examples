# GeoSpy AI API Overview

Welcome to the GeoSpy AI API, an innovative solution by Graylark Technologies designed to revolutionize the way we interact with geolocation data through images. This RESTful API harnesses the power of advanced machine learning models to analyze image content and predict geographical locations with remarkable accuracy.

## Key Features

- **Geographical Location Prediction**: Utilize AI to deduce the likely geographical coordinates based on the visual content of an image. 
- **Image Analysis**: The accuracy of the predictions may vary based on a variety of factors, such as image quality, context present in the image, and the presence of unique regional characteristics such as architecture, vegetation, and landmarks. GeoSpy works best in outdoor settings that contain some cues about the location. This can be something as simple as a skyline, grass, or a type of asphalt.
- **Region-Specific Characteristics Recognition**: The AI model is trained to recognize region-specific characteristics and patterns, enabling it to make informed predictions about the location of an image. We are continuously improving the model to enhance its accuracy and expand its capabilities in specific regions and contexts.

## Usage Guide

To start leveraging the GeoSpy AI API, follow these simple steps:

1. **Subscription**: Navigate to the [pricing page](https://dev.geospy.ai/docs/routes/~pricing) and select a plan that suits your needs. 
2. **API Key**: Upon subscription, you will receive an API key. Safeguard this key as it will authenticate your requests to the GeoSpy API.
3. **Implementation**: Refer to the source code samples on GitHub for examples on how to integrate the API into your projects.

## Support

Should you have any questions or require assistance, our support team is readily available. You can reach us via email at support@graylark.io or send us a direct message on Slack.

## Technical Details

### Base URL

```arduino
https://dev.geospy.ai
```

### Authentication

API Keys: Your API key is crucial for accessing the GeoSpy API. Here's how you manage and use your API key:

```markdown
My API Key: **************************************2e8cc743
```

Note: This API key is for demonstration purposes. Replace it with your actual API key received upon subscription.

### Endpoints

- **Image Geolocate Predict (POST /predict)**: This endpoint accepts a base64 encoded image string and returns a set of possible geographical locations.

### Data Returned

- `geo_predictions`: An array of objects containing:
  - `coordinates`: Latitude and longitude array.
  - `score`: A float representing the prediction's quality score relative to other predictions.
  - `similarity_score_1km`: A double indicating the similarity between the image's features and known characteristics within a 1-kilometer radius of the predicted point.

### Security

API Key Protection: Ensure your API key is included in the request header for authentication:

```makefile
Authorization: Bearer YOUR_API_KEY
```

### Query Parameters

- `image`: (Required) The base64-encoded image string.
- `top_k`: (Optional) The number of top location predictions to return. The default is 5, but up to 50 predictions can be requested.

By integrating the GeoSpy AI API into your projects, you unlock a new dimension of geolocation capabilities, enriching your applications with the power of AI-driven location inference.

This Markdown document is ready to be added to a GitHub repository, a documentation site, or included in your project as a README.md file to provide users and developers with essential information about the GeoSpy AI API.

# GeoSpy AI API Examples

This repository provides a collection of examples demonstrating the use of the GeoSpy AI API, developed by Graylark Technologies. The GeoSpy AI API leverages advanced machine learning techniques to predict the geographical location of a photo based on its pixel data.

## Repository Structure

The repository is organized as follows:

```plaintext
├── README.md
├── examples
│   ├── async_api_interaction.py # Demonstrates asynchronous interaction with the API
│   ├── basic_usage.py # A basic example of API interaction
│   ├── geospy.ipynb # Jupyter notebook with detailed API usage examples
│   └── sample_images # Sample images for testing and demonstration
│       ├── Arizona.jpg
│       ├── NYC.jpg
│       ├── This_Is_Not_Paris.jpg
│       ├── bar.jpg
│       └── house.jpg
└── requirements.txt # Required Python packages for running the examples
```

## Getting Started

To run the examples in this repository, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`.
2. **Install Dependencies**: Navigate to the cloned repository and install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Obtain an API Key**: To use the GeoSpy AI API, you need an API key. Visit the GeoSpy API documentation to sign up for an API key.
4. **Explore the Examples**: Navigate to the examples directory. Here, you will find Python scripts and a Jupyter notebook that demonstrate various ways to interact with the GeoSpy AI API. Replace the placeholder API key in the examples with your own API key.
5. **Run the Examples**: You can run the Python scripts directly from your terminal or open the Jupyter notebook (geospy.ipynb) in JupyterLab or Jupyter Notebook to interact with the API.

## Support

For any inquiries or support questions, please contact us at support@graylark.io or reach out via Slack.

## Contributing
We welcome contributions to this repository! Please feel free to submit pull requests with enhancements, new examples, or bug fixes.

Thank you for exploring the GeoSpy AI API with us!
