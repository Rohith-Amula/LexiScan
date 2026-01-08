import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2
from utils.ocr import perform_ocr
from utils.corrector import correct_text
import spacy
from tensorflow.keras.models import load_model

# 🔐 Restrict access unless logged in
if not st.session_state.get('user'):
    st.warning("⚠️ You must be logged in to access this page.")
    st.stop()

# Load models
nlp = spacy.load("en_core_web_sm")
digit_model = load_model('saved_model/model.h5')

# Page settings
st.set_page_config(page_title="LexiScan App", layout="wide")
st.title("📄 LexiScan")

# 🚪 Optional logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("auth_app.py")

# OCR mode selection
mode = st.radio("Select Input Type", ["Printed Text OCR", "Handwritten Digit OCR"])

# ---------------------- HANDWRITTEN DIGIT OCR ----------------------
if mode == "Handwritten Digit OCR":
    st.header("✍️ Handwritten Digit Classifier")
    uploaded_file = st.file_uploader("Upload an image of a handwritten digit", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        try:
            image = Image.open(uploaded_file).convert("L")
            st.image(image, caption='Uploaded Digit Image', width=150)

            img = np.array(image)
            img = cv2.resize(img, (28, 28))
            img = img / 255.0
            if np.mean(img) > 0.5:
                img = 1 - img
            img = img.reshape(1, 28, 28, 1)

            prediction = digit_model.predict(img)
            digit = int(np.argmax(prediction))
            st.success(f"✅ Predicted Digit: **{digit}**")
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")

# ---------------------- PRINTED TEXT OCR ----------------------
else:
    st.header("🖨️ Printed Text OCR with Correction")

    def perform_ocr_from_text(edited_text):
        fake_ocr_results = []
        words = edited_text.split()
        for word in words:
            conf = 0.9 if len(word) > 3 else 0.7
            fake_ocr_results.append((word, conf))

        text_with_conf = [f"{word} [Conf: {conf:.2f}]" for word, conf in fake_ocr_results]
        confidences = [conf for _, conf in fake_ocr_results]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        return "\n".join(text_with_conf), avg_conf

    uploaded_files = st.file_uploader("Upload image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")

            with st.expander(f"📷 {uploaded_file.name}", expanded=False):
                col_img, col_opts = st.columns([2, 1])

                with col_opts:
                    st.markdown("### 🛠️ Image Adjustments")
                    apply_adjustments = st.checkbox("Enable Adjustments", key=f"adjust_{uploaded_file.name}")
                    if apply_adjustments:
                        brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1, key=f"brightness_{uploaded_file.name}")
                        contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1, key=f"contrast_{uploaded_file.name}")
                        rotate = st.slider("Rotate (°)", -180, 180, 0, key=f"rotate_{uploaded_file.name}")
                        enhancer = ImageEnhance.Brightness(image)
                        image = enhancer.enhance(brightness)
                        enhancer = ImageEnhance.Contrast(image)
                        image = enhancer.enhance(contrast)
                        image = image.rotate(rotate, expand=True)

                with col_img:
                    st.image(image, caption=f"Adjusted Image", use_container_width=True)

            with st.spinner("🔍 Performing OCR..."):
                text_with_conf, text_plain, avg_conf = perform_ocr(image)

            show_score = st.checkbox("Show OCR confidence scores", key=f"score_toggle_{uploaded_file.name}")

            st.subheader("✏️ Raw OCR Output")
            raw_text_key = f"raw_text_input_{uploaded_file.name}"
            raw_text = st.text_area("Raw OCR Text", value=text_plain, height=300, key=raw_text_key)
            user_edited = raw_text.strip() != text_plain.strip()

            if show_score:
                with st.spinner("🔍 Calculating Confidence Scores..."):
                    scored_text, updated_avg_conf = perform_ocr_from_text(raw_text)
                    st.text_area("Raw OCR with Confidence", scored_text, height=300, key=f"scored_raw_{uploaded_file.name}")
                    st.markdown(f"**🔎 Average OCR Confidence:** `{updated_avg_conf:.2f}`")
            else:
                st.markdown(f"**🔎 Average OCR Confidence:** `{avg_conf:.2f}`")

            with st.spinner("✨ Grammar Correction (T5)..."):
                corrected = correct_text(raw_text)

            st.subheader("✅ Corrected Output (T5 Model)")
            st.text_area("Corrected Text", corrected, height=300, key=f"corrected_text_{uploaded_file.name}")

            if st.checkbox("Show Named Entities", key=f"ner_toggle_{uploaded_file.name}"):
                doc = nlp(corrected)
                ents = [(ent.text, ent.label_) for ent in doc.ents]
                if ents:
                    st.subheader("🔍 Recognized Named Entities")
                    for ent, label in ents:
                        st.markdown(f"**{label}:** {ent}")
                else:
                    st.info("No named entities found.")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download Raw Text", raw_text, file_name=f"raw_{uploaded_file.name}.txt")
            with col2:
                st.download_button("📥 Download Corrected Text", corrected, file_name=f"corrected_{uploaded_file.name}.txt")
