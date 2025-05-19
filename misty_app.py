import streamlit as st
from PIL import Image, UnidentifiedImageError
import os

st.title("📸 Company Event Photo Gallery")

# Set your image directory
IMAGE_DIR = "GROUP 2"

# Get image files
image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
image_files = [
    os.path.join(IMAGE_DIR, file)
    for file in os.listdir(IMAGE_DIR)
    if os.path.splitext(file.lower())[1] in image_extensions
]

if not image_files:
    st.warning("No images found.")
else:
    st.success(f"Loaded {len(image_files)} images from the event.")

    # Create a 4-column layout
    cols = st.columns(4)

    for i, img_path in enumerate(sorted(image_files)):
        col = cols[i % 4]  # Rotate through the 4 columns

        try:
            img = Image.open(img_path)
            with col:
                st.image(img, caption=os.path.basename(img_path), use_container_width=True)

                with open(img_path, "rb") as file:
                    img_bytes = file.read()

                st.download_button(
                    label="⬇️ Download",
                    data=img_bytes,
                    file_name=os.path.basename(img_path),
                    mime="image/jpeg",
                    key=f"download-{i}"  # Ensure unique keys
                )
        except UnidentifiedImageError:
            st.error(f"Could not load: {os.path.basename(img_path)}")
