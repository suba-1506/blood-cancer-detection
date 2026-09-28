import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# ---------------- PAGE CONFIG ----------------
st.markdown("""
<style>
.banner{
    width:100vw;
    height:80px;
    margin-left:calc(-50vw + 50%);
    
}

.banner img{
    width:100%;
    height:80px;
    object-fit:cover;
}
</style>

<div class="banner">
    <img src="https://as1.ftcdn.net/jpg/01/44/16/88/1000_F_144168825_deLkQDhrSUTV9eZPq80LGplWK28kVsUy.jpg">
</div>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Blood Cancer Detection System",
    page_icon="🩸",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stToolbar"]{
    display:none;
}

.stApp{
    background: linear-gradient(
        135deg,
        #071426 0%,
        #0B1F3A 50%,
        #102C54 100%
    );
}

html, body, [class*="css"]{
    color:white;
}

[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
}

[data-testid="stMetric"]{
    background: rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.15);
    border-radius:15px;
    padding:15px;
}

.block-container{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#EAF4FF;margin-top:0px;'>
     Blood Cancer Detection System
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center;color:#AFC7E8;'>
    Clinical Decision Support Platform
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- MODEL ----------------

import gdown

MODEL_PATH = "blood_cancer_model.keras"

if not os.path.exists(MODEL_PATH):

    file_id = "1xEwmazqNAjtGy-iLp1ZJg2SxuyGg2inh"

    url = f"https://drive.google.com/file/d/1xEwmazqNAjtGy-iLp1ZJg2SxuyGg2inh/view?usp=sharing"

    gdown.download(
        url,
        MODEL_PATH,
        quiet=False
    )

model = tf.keras.models.load_model(
    MODEL_PATH
)
# ---------------- PATIENT DETAILS ----------------

st.subheader("Patient Information")

col_a, col_b = st.columns(2)

with col_a:
    patient_name = st.text_input("Patient Name")
    patient_id = st.text_input("Patient ID")

with col_b:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

st.markdown("---")

# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Blood Smear Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            image,
            caption="Uploaded Blood Smear Image",
            use_container_width=True
        )

    # Prediction

    img = image.resize((224, 224))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    pred = float(prediction[0][0])

    if pred < 0.5:
        result = "Leukemia"
        confidence = (1 - pred) * 100
    else:
        result = "Healthy"
        confidence = pred * 100

    with col2:

        st.subheader("Diagnosis Report")

        if result == "Leukemia":
            st.error(f"Diagnosis : {result}")
        else:
            st.success(f"Diagnosis : {result}")

        st.metric(
            "Confidence Score",
            f"{confidence:.2f}%"
        )

        # ---------------- PDF REPORT ----------------

        os.makedirs(
            "BloodCancerProject/reports",
            exist_ok=True
        )

        pdf_file = (
            "BloodCancerProject/reports/"
            "BloodCancer_Report.pdf"
        )

        report_id = (
            "BC-" +
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        c = canvas.Canvas(pdf_file)

        # Header

        c.setFont("Helvetica-Bold", 20)
        c.drawString(
            160,
            800,
            "BLOOD CANCER REPORT"
        )

        c.setFont("Helvetica", 12)

        c.drawString(
            50,
            770,
            f"Report ID : {report_id}"
        )

        c.drawString(
            350,
            770,
            f"Date : {datetime.now().strftime('%d-%m-%Y')}"
        )

        # Patient Information

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            730,
            "Patient Information"
        )

        c.setFont("Helvetica", 12)

        c.drawString(
            50,
            705,
            f"Patient Name : {patient_name}"
        )

        c.drawString(
            50,
            685,
            f"Patient ID : {patient_id}"
        )

        c.drawString(
            50,
            665,
            f"Age : {age}"
        )

        c.drawString(
            250,
            665,
            f"Gender : {gender}"
        )

        # Test Information

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            625,
            "Test Information"
        )

        c.setFont("Helvetica", 12)

        c.drawString(
            50,
            600,
            "Test Name : Blood Cancer Screening"
        )

        c.drawString(
            50,
            580,
            "Sample Type : Blood Smear Image"
        )

        # Result

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            540,
            "AI Analysis Result"
        )

        c.setFont("Helvetica", 12)

        c.drawString(
            50,
            515,
            f"Diagnosis : {result}"
        )

        c.drawString(
            50,
            495,
            f"Confidence Score : {confidence:.2f}%"
        )

        # Recommendation

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            450,
            "Recommendation"
        )

        c.setFont("Helvetica", 12)

        if result == "Leukemia":

            c.drawString(
                50,
                425,
                "Consult a hematologist for further evaluation."
            )

            c.drawString(
                50,
                405,
                "Additional laboratory tests are recommended."
            )

        else:

            c.drawString(
                50,
                425,
                "No significant leukemia indicators detected."
            )

            c.drawString(
                50,
                405,
                "Continue routine health monitoring."
            )

        # Signature Area

        c.line(
            50,
            250,
            220,
            250
        )

        c.drawString(
            70,
            230,
            "Authorized Signature"
        )

        c.line(
            320,
            250,
            500,
            250
        )

        c.drawString(
            350,
            230,
            "Laboratory Seal Area"
        )

        c.save()

        with open(pdf_file, "rb") as pdf:

            st.download_button(
                "📄 Download PDF Report",
                data=pdf,
                file_name="BloodCancer_Report.pdf",
                mime="application/pdf"
            )

    st.markdown("---")

    if result == "Leukemia":

        st.warning(
            "Possible abnormal blood cell patterns detected. "
            "Please consult a medical professional."
        )

    else:

        st.info(
            "No strong leukemia indicators detected. "
            "Regular monitoring is recommended."
        )

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Blood Cancer Detection using Deep Learning"
)
