import streamlit as st
import os
from PIL import Image, UnidentifiedImageError

# Page config
st.set_page_config(page_title="Misty Mount Photo Gallery", layout="wide")
st.title("\U0001F4F8 Misty Mount Photo Gallery")
st.markdown("""
Welcome to the Misty Mount event gallery. Use the sidebar to browse images by folder.
""")

# Constants
IMAGE_ROOT_DIR = "GROUP 2"
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

# Get subfolders (pages)
subfolders = [f.name for f in os.scandir(IMAGE_ROOT_DIR) if f.is_dir()]
selected_folder = st.sidebar.selectbox("Choose a page:", sorted(subfolders))

# Path to selected image folder
folder_path = os.path.join(IMAGE_ROOT_DIR, selected_folder)
image_files = [
    os.path.join(folder_path, file)
    for file in os.listdir(folder_path)
    if os.path.splitext(file.lower())[1] in IMAGE_EXTENSIONS
]

# Pagination setup
images_per_page = 20
page_number = st.sidebar.number_input(
    label="Page:", min_value=1, max_value=max(1, len(image_files) // images_per_page + 1), step=1, value=1
)
start_idx = (page_number - 1) * images_per_page
end_idx = start_idx + images_per_page
paginated_images = image_files[start_idx:end_idx]

# Display images in 4-column layout
if not paginated_images:
    st.warning("No images found in the selected folder.")
else:
    st.success(f"Loaded {len(paginated_images)} images from '{selected_folder}'.")
    cols = st.columns(4)

    for i, img_path in enumerate(sorted(paginated_images)):
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
                    key=f"download-{i}-{selected_folder}"
                )
        except UnidentifiedImageError:
            st.error(f"Could not load: {os.path.basename(img_path)}")
