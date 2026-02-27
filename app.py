import streamlit as st
from fpdf import FPDF
import base64

# --- PDF GENERATION CLASS ---
class ProtocolPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Guided Surgery Protocol: Osstem TS IV', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Engineered with precision by OYM Dental Lab', align='C')

def generate_protocol(dr_name, patient_name, implant_system, diameter):
    pdf = ProtocolPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Welcome Message
    pdf.cell(0, 10, f"Dear {dr_name},", ln=True)
    pdf.multi_cell(0, 10, f"It is always a pleasure collaborating with you! Enclosed is the customized drilling sequence tailored for the {implant_system} system for our patient, {patient_name}.")
    pdf.ln(5)

    # Surgical Guidelines
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "CRITICAL SURGICAL GUIDELINES:", ln=True)
    pdf.set_font("Arial", size=10)
    guidelines = [
        "1. Guide Fit: Verify seating via inspection windows.",
        "2. Drill Insertion: Insert drill completely into sleeve BEFORE starting rotation.",
        "3. Drill Speed: 800-1200 RPM with saline irrigation.",
        "4. Placement: 15-20 RPM. Final torque target: 35-45 Ncm."
    ]
    for line in guidelines:
        pdf.cell(0, 7, line, ln=True)
    
    pdf.ln(10)

    # Drilling Protocol Logic (Based on your Reference Chart)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"INDIVIDUAL DRILLING PROTOCOL: {diameter}", ln=True)
    pdf.set_font("Arial", size=11)
    
    # Example logic for 4.0mm diameter
    steps = ["Tissue Punch", "Flattening Drill", "Initial Drill", "F3.5 Drill"]
    if diameter == "4.0mm":
        steps.append("F4.0 Drill")
    elif diameter == "4.5mm":
        steps.extend(["F4.0 Drill", "F4.5 Drill"])
    
    steps.append("Implant Placement (15-20 RPM)")

    for i, step in enumerate(steps):
        pdf.cell(0, 8, f"{i+1}. {step}", ln=True)

    # Output as Bytes for Streamlit
    # We use 'S' and ensure it returns a latin-1 compatible string
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin-1')
    return pdf_output

# --- STREAMLIT UI ---
st.set_page_config(page_title="OYM Lab Generator", page_icon="🦷")

st.title("🦷 OYM Dental Lab: Protocol Generator")

col1, col2 = st.columns(2)

with col1:
    dr_name = st.text_input("Doctor Name", "Dr. Naveen")
    patient_name = st.text_input("Patient Name", "Shrey Sipani")

with col2:
    implant_system = st.selectbox("Select Implant System", ["Osstem TS IV"])
    diameter = st.selectbox("Select Diameter", ["3.5mm", "4.0mm", "4.5mm", "5.0mm"])

if st.button("🚀 Generate Surgical Protocol"):
    try:
        pdf_bytes = generate_protocol(dr_name, patient_name, implant_system, diameter)
        
        # Create Download Button
        st.download_button(
            label="Download PDF Protocol",
            data=pdf_bytes,
            file_name=f"OYM_Protocol_{patient_name}.pdf",
            mime="application/pdf"
        )
        st.success("Protocol generated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
