import streamlit as st
from fpdf import FPDF
import os

# --- PROFESSIONAL PDF CLASS ---
class OYMProtocolPDF(FPDF):
    def header(self):
        # Adding Logo from your GitHub repo
        if os.path.exists("OYM.png"):
            self.image("OYM.png", 10, 8, 25)
        
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'OYM DENTAL LAB', ln=True, align='C') [cite: 19]
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Guided Surgery Protocol', ln=True, align='C') [cite: 20]
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Engineered with precision by OYM Dental Lab', align='C') [cite: 50]

def generate_protocol(dr_name, patient_name, implant_system, diameter, bone_quality):
    pdf = OYMProtocolPDF()
    pdf.add_page()
    
    # Professional Greeting
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"Dear {dr_name},\n\nIt is always a pleasure collaborating with you! [cite: 22] Enclosed is the customized drilling sequence specifically tailored for the {implant_system} system for our patient, {patient_name}. [cite: 22] We have meticulously mapped out the surgical flow below to match the physical color bands on your drills. [cite: 23]")
    pdf.ln(5)

    # Critical Surgical Guidelines [cite: 27-37]
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "CRITICAL SURGICAL GUIDELINES:", ln=True) [cite: 27]
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, 
        "1. Guide Fit: Verify seating via inspection windows. Ensure zero rocking. [cite: 28, 32]\n"
        "2. Drill Insertion: Insert drill completely into sleeve BEFORE starting rotation. [cite: 29, 33]\n"
        "3. Drill Speed: 800-1200 RPM with copious saline irrigation. [cite: 30, 35]\n"
        "4. Placement: 15-20 RPM. Final seating torque target: 35 to 45 Ncm. [cite: 31, 36]\n"
        "(Do not exceed 45 Ncm to prevent crestal bone necrosis. Use cortical tap if torque exceeds limit.) [cite: 37]"
    )
    pdf.ln(5)

    # Drilling Sequence Logic [cite: 97-154]
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"INDIVIDUAL DRILLING PROTOCOL: {implant_system} Dia. {diameter} ({bone_quality} Bone)", ln=True) [cite: 38, 39]
    pdf.set_font("Arial", size=10)

    # Sequence Logic for Osstem TS IV [cite: 105-154]
    steps = ["Tissue Punch", "Flattening Drill", "Initial Drill"]
    
    if implant_system == "Osstem TS IV":
        if diameter == "3.5mm":
            steps.extend(["2.2 Drill", "F3.5 Drill"]) [cite: 46, 47]
        elif diameter == "4.0mm":
            steps.append("F3.5 Drill") [cite: 60]
            if bone_quality != "Soft": steps.append("F4.0 Drill") [cite: 62, 115]
        elif diameter == "4.5mm":
            steps.extend(["F3.5 Drill", "F4.0 Drill"]) [cite: 133]
            if bone_quality != "Soft": steps.append("F4.5 Drill") [cite: 134, 125]
            if bone_quality == "Hard": steps.append("F4.5 Cortical") [cite: 78, 135]
        elif diameter == "5.0mm":
            steps = ["Tissue Punch", "Flattening Drill (W)", "Initial Drill (W)", "F3.5 Drill (W)", "F4.5 Drill (W)", "F5.0 Drill (W)"] [cite: 147-152]
            if bone_quality == "Hard": steps.append("F5.5 Taper (W)") [cite: 91, 153]

    for i, step in enumerate(steps, 1):
        pdf.cell(0, 7, f"  {i}. {step} (800-1200 RPM)", ln=True) [cite: 42-47]
    
    pdf.cell(0, 7, f"  {len(steps)+1}. Placement (15-20 RPM / Max 45Ncm) >> Fixture Driver", ln=True) [cite: 48, 49]

    # Elite Club Section [cite: 173-176]
    pdf.ln(10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "WELCOME TO THE OYM ELITE CLUB", ln=True, fill=True) [cite: 173]
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, f"{dr_name}, since OYM Dental Lab designed this plan, we have your digital files ready! Let us craft your final Implant Prosthesis and Zirconium Crowns. As an Elite Partner, you receive priority milling and preferred VIP rates. [cite: 174, 175, 176]\nContact: +91 88383 02454 [cite: 177]")

    return bytes(pdf.output(dest='S'))

# --- STREAMLIT UI ---
st.set_page_config(page_title="OYM Lab Generator", page_icon="🦷")

# Show logo in UI
if os.path.exists("OYM.png"):
    st.image("OYM.png", width=100)

st.title("🦷 OYM Dental Lab: Protocol Generator")

col1, col2 = st.columns(2)
with col1:
    dr_name = st.text_input("Doctor Name", "Dr. Naveen")
    patient_name = st.text_input("Patient Name", "Shrey Sipani")
    implant_system = st.selectbox("Select Implant System", ["Osstem TS IV", "Megagen AnyRidge", "Straumann BLX"])

with col2:
    diameter = st.selectbox("Select Diameter", ["3.0mm", "3.5mm", "4.0mm", "4.5mm", "5.0mm", "6.0mm"])
    bone_quality = st.selectbox("Bone Quality", ["Soft", "Normal", "Hard"])

if st.button("🚀 Generate Surgical Protocol"):
    pdf_bytes = generate_protocol(dr_name, patient_name, implant_system, diameter, bone_quality)
    st.download_button(
        label="Download Professional PDF Protocol",
        data=pdf_bytes,
        file_name=f"OYM_Protocol_{patient_name}.pdf",
        mime="application/pdf"
    )
    st.success("Protocol generated successfully!")
