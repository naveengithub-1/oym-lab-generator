import streamlit as st
from fpdf import FPDF
import os

# --- 1. THE BRAIN: Protocol Database ---
PROTOCOLS = {
    "Osstem TS IV": {
        "3.5mm": ["Tissue Punch", "Flatten Drill (800-1200 RPM)", "Initial Drill", "2.2 Drill", "F3.5 (13mm)", "Placement (15-20 RPM/Max 45Ncm)", "Fixture Driver"],
        "4.0mm": ["Tissue Punch", "Flatten Drill (800-1200 RPM)", "Initial Drill", "F3.5", "F4.0", "Placement (15-20 RPM/Max 45Ncm)", "Fixture Driver"],
        "5.0mm": ["Tissue Punch", "Flatten W (800-1200 RPM)", "Initial W", "F3.5 W", "F4.5 W", "F5.0 W", "F5.5 Taper (800-1200 RPM)", "Placement (15-20 RPM/Max 45Ncm)"]
    },
    "Alpha Bio Spiral": {
        "4.2mm": ["Tissue Punch", "Crestal Drill (1200 RPM)", "2.0x8 Drill", "2.0x13 Drill", "2.8x13 Drill", "3.2x13 Drill", "Placement (Max 45Ncm)"]
    }
}

# --- 2. THE WEBSITE INTERFACE ---
st.set_page_config(page_title="OYM Lab Automation", page_icon="🦷")
st.title("🦷 OYM Dental Lab: Protocol Generator")

col1, col2 = st.columns(2)
with col1:
    dr_name = st.text_input("Doctor Name", "Dr. Anath")
    patient_name = st.text_input("Patient Name", "Shrey Sipani")
with col2:
    system = st.selectbox("Select Implant System", list(PROTOCOLS.keys()))
    size = st.selectbox("Select Diameter", list(PROTOCOLS[system].keys()))

# --- 3. PDF GENERATION ENGINE ---
class OymPDF(FPDF):
    def header(self):
        self.set_fill_color(255, 215, 0)
        self.rect(10, 10, 190, 25, 'F')
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(62, 39, 35)
        self.set_xy(10, 15)
        self.cell(0, 10, 'OYM DENTAL LAB', align='C', ln=True)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 5, f'Guided Surgery Protocol: {system}', align='C', ln=True)
        self.ln(10)

if st.button("🚀 Generate Surgical Protocol"):
    pdf = OymPDF()
    pdf.add_page()
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 6, f"Dear {dr_name},\n\nEnclosed is the customized drilling sequence for {patient_name}. Flowcharts are color-coded to match your kit.")
    pdf.ln(5)
    pdf.set_fill_color(62, 39, 35)
    pdf.set_text_color(255, 215, 0)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f"  PROTOCOL: {system} {size}", fill=True, ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_text_color(40, 40, 40)
    for step in PROTOCOLS[system][size]:
        pdf.cell(0, 8, f">> {step}", ln=True)
    pdf.ln(20)
    pdf.set_fill_color(62, 39, 35)
    pdf.rect(10, pdf.get_y(), 190, 45, 'F')
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(255, 215, 0)
    pdf.cell(0, 8, "WELCOME TO THE OYM ELITE CLUB", align='C', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(180, 5, "Since OYM designed this plan, your digital files are ready! Let us craft your final Implant Prosthesis and Zirconium Crowns at VIP rates.", align='C')
    pdf.ln(10)
    pdf.set_fill_color(255, 215, 0)
    pdf.rect(10, pdf.get_y(), 190, 15, 'F')
    pdf.set_xy(10, pdf.get_y() + 3)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(62, 39, 35)
    pdf.cell(190, 8, "Contact at: +91 88383 02454", align='C', ln=True)
    pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
    st.download_button(label="📥 Download Finished PDF", data=pdf_output, file_name=f"OYM_{patient_name}.pdf")
