import streamlit as st
from PIL import Image, UnidentifiedImageError
import os

st.set_page_config(page_title="📸 Event Photo Gallery", layout="wide")
st.title("📸 Company Event Photo Gallery")

# Constants
BASE_DIR = "GROUP 2"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

# Get all image folders
@st.cache_data
def get_folders(base_dir):
    return sorted([f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))])

# Get image files from selected folder
@st.cache_data
def load_images_from_folder(folder_path):
    return sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.splitext(f.lower())[1] in IMAGE_EXTENSIONS
    ])

# UI - Folder selector
folders = get_folders(BASE_DIR)
selected_folder = st.sidebar.selectbox("📁 Select Album", folders)
folder_path = os.path.join(BASE_DIR, selected_folder)

# Load images
image_files = load_images_from_folder(folder_path)

# Show image count
if not image_files:
    st.warning("🚫 No images found in this folder.")
else:
    st.success(f"📷 Loaded {len(image_files)} images from '{selected_folder}'.")

    # Display in columns
    cols = st.columns(4)

    for i, img_path in enumerate(image_files):
        col = cols[i % 4]
        with col:
            try:
                # Use thumbnail to reduce memory
                img = Image.open(img_path)
                img.thumbnail((600, 600))

                st.image(img, caption=os.path.basename(img_path), use_container_width=True)

                with open(img_path, "rb") as file:
                    img_bytes = file.read()

                st.download_button(
                    label="⬇️ Download",
                    data=img_bytes,
                    file_name=os.path.basename(img_path),
                    mime="image/jpeg",
                    key=f"{selected_folder}-{i}"
                )
            except UnidentifiedImageError:
                st.error(f"⚠️ Can't load: {os.path.basename(img_path)}")
