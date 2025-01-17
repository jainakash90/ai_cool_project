import streamlit as st
import os
import json
import pandas as pd
from PIL import Image

def main():
    st.title("Dashboard - Animal Details")

    # Get available folders (common names)
    base_dir = "data"
    if not os.path.exists(base_dir):
        st.warning("No data available. Please upload an image first.")
        return

    common_names = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    if common_names:
        selected_name = st.selectbox("Select an animal by common name", common_names)

        # Paths for image and JSON
        folder_path = os.path.join(base_dir, selected_name)
        image_path = os.path.join(folder_path, f"{selected_name}.jpg")
        json_path = os.path.join(folder_path, f"{selected_name}.json")
        
        # Display image and details
        col1, col2 = st.columns(2)
        with col2:
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    species_details = json.load(f)
                st.table(species_details)
        with col1:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=selected_name.replace("_", " "), use_container_width=True)

    else:
        st.warning("No common names available. Upload an image to add data.")

if __name__ == "__main__":
    main()
