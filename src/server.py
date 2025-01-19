import os
from PIL import Image
import streamlit as st

# Define the directory where images will be stored
IMAGE_DIR = "./images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def main():
    st.title("Image Uploader & Viewer")
    
    # File Upload Section
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_path = os.path.join(IMAGE_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File {uploaded_file.name} has been uploaded successfully.")
    
    # Display Images Section
    st.subheader("Uploaded Images")
    images = os.listdir(IMAGE_DIR)
    if not images:
        st.info("No images found in the directory.")
    else:
        num_images = len(images)
        cols_per_row = 3  # Number of columns per row
        
        # Calculate the number of rows needed
        num_rows = (num_images + cols_per_row - 1) // cols_per_row
        
        for i in range(num_rows):
            cols = st.columns(cols_per_row)
            start_idx = i * cols_per_row
            end_idx = min(start_idx + cols_per_row, num_images)
            
            for j in range(end_idx - start_idx):
                image_name = images[start_idx + j]
                with open(os.path.join(IMAGE_DIR, image_name), "rb") as f:
                    img = Image.open(f)
                    img.thumbnail((200, 200))  # Resize to thumbnail size while maintaining aspect ratio
                cols[j].image(img, caption=image_name, use_container_width=True)

    # Delete Image Section
    st.subheader("Delete an Image")
    delete_option = st.selectbox("Select an image to delete", [""] + images)
    if st.button("Delete"):
        if delete_option:
            os.remove(os.path.join(IMAGE_DIR, delete_option))
            st.success(f"Image {delete_option} has been deleted successfully.")
        else:
            st.warning("Please select an image to delete.")

if __name__ == "__main__":
    main()