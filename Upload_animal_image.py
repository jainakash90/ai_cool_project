import base64
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
import os
import json

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
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        with open(temp_image_path, "rb") as image_file:
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


                species_data = SpeciesData(**species_dict)
                common_name = species_data.common_name

                # Create folder based on `common_name`
                filename = common_name.replace(' ', '_')
                folder_name = f"data/{filename}"
                os.makedirs(folder_name, exist_ok=True)

                # Save image to folder
                image_save_path = os.path.join(folder_name, f"{filename}.jpg")
                with open(image_save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Save species_dict as JSON to folder
                json_save_path = os.path.join(folder_name, f"{filename}.json")
                with open(json_save_path, "w") as json_file:
                    json.dump(species_dict, json_file, indent=4)

                st.success(f"Data saved in folder: {folder_name}")

                # Display extracted information
                st.success("Species information extracted successfully!")
                species_df = pd.DataFrame([species_dict])
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
