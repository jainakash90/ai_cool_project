# Animal Image App

Welcome to the **Animal Image App**! This app allows users to explore and learn about animals using images and descriptions generated with the power of OpenAI and Streamlit.

## Features

- **Animal Image Upload**: Upload an animal image to know details.
- **Detailed Descriptions**: Get detailed, AI-generated descriptions for each animal.
- **Interactive Interface**: Enjoy a user-friendly interface powered by Streamlit.

## Technologies Used

- **Framework**: Streamlit
- **AI**: OpenAI API (for descriptions and image generation)
- **Backend**: Python

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jainakash90/animal-image-app.git
   cd animal-image-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following variables:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ```

4. Start the application:
   ```bash
   streamlit run animal_image_app.py
   ```

5. Open the app in your browser at the URL provided in the terminal (e.g., `http://localhost:8501`).

## Usage

1. Launch the app using the command above.
2. Use the image upload box to upload animal image of your choice.
3. View the uploaded image and detailed description of the animal.
4. Explore more animals by repeating the process.

Thank you for using the Animal Image App! 🐾
