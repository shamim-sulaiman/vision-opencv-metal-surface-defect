import os
import numpy as np
from PIL import Image
from utils.defect_detector import detect_defect
import streamlit as st

#st.set_page_config(page_title="Metal Defect Detector", page_icon="🔬", layout="wide")

st.title("🔬 Metal Surface Defect Detection using OpenCV")
with st.expander("📘 About This App", expanded=False):
    st.markdown("""
This interactive web app demonstrates **surface defect detection** using the [Northeastern University (NEU) Metal Surface Defect Dataset](https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data), a well-known benchmark dataset for visual inspection in industrial settings.

🔍 **How it works:**
- You can select from six defect types (e.g. scratches, inclusion, patches).
- Choose any image sample from the dataset.
- The image is processed in real time using **OpenCV** to highlight detected defect areas.

🔬 **Detection Modes:**
- `Canny`: Classic edge detection using gradients (with adjustable thresholds).
- `Adaptive`: Thresholding that adapts to local brightness variations.
- `Otsu`: Automatic global thresholding based on histogram analysis.
- `Morph`: Morphological gradient detection — great for capturing shape outlines.

📁 **Dataset Used:**  
[NEU Metal Surface Defects Data on Kaggle](https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data)  
*(Downloaded and organized locally into subfolders like `scratches`, `patches`, etc.)*

""")
    st.markdown("""
    <span style='font-size: 13px; color: gray;'>
        💡 Built by <b>Shamim Sulaiman</b> as part of a machine vision project to demonstrate OpenCV logic, dataset handling, and Streamlit dashboards for defect classification and detection.
    </span>
    """, unsafe_allow_html=True)

# === Dataset path ===
base_path = "dataset"

# === Load available defect classes ===
categories = sorted([d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])
selected_category = st.sidebar.selectbox("🗂️ Select Defect Type", categories)

# === Load images from selected category ===
image_files = sorted([
    f for f in os.listdir(os.path.join(base_path, selected_category))
    if f.lower().endswith(('.bmp', '.jpg', '.jpeg', '.png'))
])
selected_image = st.sidebar.selectbox("🖼️ Choose Image", image_files)

# === Load image ===
image_path = os.path.join(base_path, selected_category, selected_image)
image = Image.open(image_path).convert("RGB")
image_np = np.array(image)

# === Sidebar parameters ===
st.sidebar.markdown("### 🔧 Detection Settings")
detection_mode = st.sidebar.selectbox("Detection Mode", ["canny", "adaptive", "otsu", "morph"])

if detection_mode == "canny":
    canny_low = st.sidebar.slider("Canny Low Threshold", 0, 255, 30)
    canny_high = st.sidebar.slider("Canny High Threshold", 0, 255, 150)
    processed_image, contour_count, edge_image = detect_defect(
        image_np, mode="canny", canny_low=canny_low, canny_high=canny_high
    )

elif detection_mode == "adaptive":
    block_size = st.sidebar.slider("Block Size (odd)", 3, 31, 11, step=2)
    c_value = st.sidebar.slider("C Value", 0, 10, 2)
    processed_image, contour_count, edge_image = detect_defect(
        image_np, mode="adaptive", block_size=block_size, c_value=c_value
    )

else:
    # For otsu or morph – no extra sliders needed
    processed_image, contour_count, edge_image = detect_defect(
        image_np, mode=detection_mode
    )


# === Side-by-side display ===
col1, col2, col3 = st.columns(3)

with col1:
    st.image(image, width=300, caption="Original")

with col2:
    st.image(processed_image, width=300, caption="With Bounding Boxes")

with col3:
    st.image(edge_image, width=300, caption="Raw Edge/Threshold Output")

# === Footer ===
st.markdown("""
        <hr>
        <div style="text-align: center; font-size: 12px; color: gray;">
            © 2025 Shamim Sulaiman<br>
            Released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT License</a>
        </div>
    """, unsafe_allow_html=True)
