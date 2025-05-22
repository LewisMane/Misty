import streamlit as st
from PIL import Image, UnidentifiedImageError
import os

st.set_page_config(page_title="📸 Photo Gallery", layout="wide")
st.title("📸 Company Event Photo Gallery")

# Path to your main image directory
BASE_DIR = "GROUP 2"

# Automatically detect all folders
folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]

# Sidebar folder selector
selected_folder = st.sidebar.selectbox("📁 Select Image Folder", sorted(folders))

# Full path to selected folder
selected_path = os.path.join(BASE_DIR, selected_folder)

# Supported image formats
image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

# Collect image paths
image_files = [
    os.path.join(selected_path, file)
    for file in os.listdir(selected_path)
    if os.path.splitext(file.lower())[1] in image_extensions
]

if not image_files:
    st.warning("No images found in this folder.")
else:
    st.success(f"Loaded {len(image_files)} images from '{selected_folder}'.")

    cols = st.columns(4)

    for i, img_path in enumerate(sorted(image_files)):
        col = cols[i % 4]
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
                    key=f"download-{selected_folder}-{i}"
                )
        except UnidentifiedImageError:
            st.error(f"Could not load: {os.path.basename(img_path)}")
