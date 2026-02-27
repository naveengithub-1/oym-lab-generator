import streamlit as st
from fpdf import FPDF

# --- PDF GENERATION CLASS ---
class ProtocolPDF(FPDF):
    def header(self):
        # Logo or Lab Name
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Guided Surgery Protocol: Osstem TS IV', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Engineered with precision by OYM Dental Lab', align='C')

def generate_protocol(dr_name, patient_name, implant_system, diameter, bone_quality):
    pdf = ProtocolPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header details
    pdf.cell(0, 10, f"Dear {dr_name},", ln=True)
    pdf.multi_cell(0, 10, f"Enclosed is the customized drilling sequence tailored for the {implant_system} system for our patient, {patient_name}.")
    pdf.ln(5)

    # Critical Guidelines from Source [cite: 10-20]
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "CRITICAL SURGICAL GUIDELINES:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, "1. Guide Fit: Verify seating via inspection windows.\n"
                         "2. Drill Insertion: Insert drill completely into sleeve BEFORE starting rotation.\n"
                         "3. Drill Speed: 800-1200 RPM with copious saline irrigation.\n"
                         "4. Placement: 15-20 RPM. Final seating torque target: 35 to 45 Ncm.")
    pdf.ln(5)

    # Drilling Sequence Logic from Reference Chart [cite: 80-144]
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"DRILLING PROTOCOL: {diameter} ({bone_quality} Bone)", ln=True)
    pdf.set_font("Arial", size=11)
    
    # Logic based on diameter and bone quality
    steps = ["Tissue Punch", "Flattening Drill", "Initial Drill", "F3.5 Drill"]
    
    if diameter == "4.0mm":
        if bone_quality != "Soft": steps.append("F4.0 Drill")
    elif diameter == "4.5mm":
        steps.append("F4.0 Drill")
        if bone_quality != "Soft": steps.append("F4.5 Drill")
        if bone_quality == "Hard": steps.append("F4.5 Cortical")
    elif diameter == "5.0mm":
        steps = ["Tissue Punch", "Flattening Drill (W)", "Initial Drill (W)", "F3.5 Drill (W)", "F4.5 Drill (W)", "F5.0 Drill (W)"]
        if bone_quality == "Hard": steps.append("F5.5 Taper/Drill")

    steps.append("Implant Placement (Fixture Driver)")

    for i, step in enumerate(steps, 1):
        pdf.cell(0, 8, f"{i}. {step}", ln=True)

    # FIX: Convert bytearray to bytes
    return bytes(pdf.output(dest='S'))

# --- STREAMLIT UI ---
st.set_page_config(page_title="OYM Lab Generator", page_icon="🦷")
st.title("🦷 OYM Dental Lab: Protocol Generator")

col1, col2 = st.columns(2)
with col1:
    dr_name = st.text_input("Doctor Name", "Dr. Naveen")
    patient_name = st.text_input("Patient Name", "Shrey Sipani")
with col2:
    diameter = st.selectbox("Select Diameter", ["3.5mm", "4.0mm", "4.5mm", "5.0mm"])
    bone_quality = st.selectbox("Bone Quality", ["Soft", "Normal", "Hard"])

if st.button("🚀 Generate Surgical Protocol"):
    try:
        pdf_bytes = generate_protocol(dr_name, patient_name, "Osstem TS IV", diameter, bone_quality)
        
        st.download_button(
            label="Download PDF Protocol",
            data=pdf_bytes,
            file_name=f"OYM_Protocol_{patient_name}.pdf",
            mime="application/pdf"
        )
        st.success("Protocol ready for download!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
