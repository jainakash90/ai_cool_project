import base64
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define Pydantic model for species data
class SpeciesData(BaseModel):
    group: str
    binomial: str
    iucn_id_no: int
    common_name: str
    name_language: str
    iucn_category: str
    iso_a3: str
    total_area: float
    small_range: bool
    wb_datanam: str
    wb_iso: str
    datanam_area: float
    datanam_pct_area: float

# Streamlit app
def main():
    st.title("Animal Image Analyzer")
    st.write("Upload an animal image to extract species information.")

    # File uploader
    with st.sidebar.form(key="upload_form"):
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
        submit_button = st.form_submit_button(label="Submit")

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # Temporary save uploaded file
        with open("temp_image.jpg", "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        # Replace this with a URL upload mechanism (if needed)
        image_path = "temp_image.jpg"  # Placeholder

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # AI pipeline call
        with st.spinner("Analyzing the image..."):
            try:
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": "Extract the event information."},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "What's in this image?"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    response_format=SpeciesData,
                )

                event = completion.choices[0].message.parsed

                # Convert to DataFrame for display
                species_dict = event.model_dump()
                species_df = pd.DataFrame([species_dict])

                # Display extracted information
                st.success("Species information extracted successfully!")
                st.table(species_df.T)

                # Option to download the data as JSON
                st.download_button(
                    label="Download Data as JSON",
                    data=event.model_dump_json(),
                    file_name="species_data.json",
                    mime="application/json",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
