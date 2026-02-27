import streamlit as st
from fpdf import FPDF
import os

# --- 1. COMPREHENSIVE IMPLANT DATABASE ---
# This dictionary handles the specific drilling logic and colors for 10 companies.
SYSTEM_CONFIG = {
    "Osstem TS IV": {"base": ["Tissue Punch", "Flatten Drill", "Initial Drill"], "color": (255, 215, 0)},
    "Megagen AnyRidge": {"base": ["Guide Drill", "2.0 Drill", "3.3 Drill"], "color": (0, 102, 204)},
    "Straumann BLX": {"base": ["Needle Drill", "2.2 Drill", "2.8 Drill"], "color": (128, 128, 128)},
    "Nobel Biocare N1": {"base": ["OsseoDirector", "OsseoShaper"], "color": (204, 0, 0)},
    "Zimmer Biomet T3": {"base": ["Precision Drill", "2.0mm Drill"], "color": (0, 153, 76)},
    "BioHorizons Tapered": {"base": ["1.5mm Drill", "2.0mm Drill"], "color": (255, 128, 0)},
    "Dentsply Astra": {"base": ["Guide Drill", "2.0 Drill"], "color": (102, 0, 204)},
    "MIS C1/V3": {"base": ["Marking Drill", "2.0 Drill"], "color": (0, 204, 204)},
    "Dentium SuperLine": {"base": ["Guide Drill", "2.2 Drill"], "color": (153, 76, 0)},
    "Hiossen ET III": {"base": ["Initial Drill", "2.0 Drill"], "color": (255, 153, 204)}
}

class OYM_Protocol_PDF(FPDF):
    def __init__(self, logo_exists):
        super().__init__()
        self.logo_exists = logo_exists

    def header(self):
        # Professional Yellow Header
        self.set_fill_color(255, 215, 0)
        self.rect(0, 0, 210, 35, 'F')
        
        # Logo Logic: If OYM.png is missing, it uses text so it won't error out
        if self.logo_exists:
            self.image("OYM.png", 10, 8, 20)
        else:
            self.set_font('Arial', 'B', 15)
            self.set_xy(10, 12)
            self.cell(20, 10, "OYM")

        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 20)
        self.set_xy(40, 10)
        self.cell(160, 10, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 11)
        self.set_x(40)
        self.cell(160, 5, 'Guided Surgery Protocol: Elite Partner Program', ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120)
        self.cell(0, 10, f'Page {self.page_no()} | Precision Engineering by OYM Dental Lab', align='C')

def generate_full_protocol(data):
    # Check if logo exists to prevent app crash
    logo_exists = os.path.exists("OYM.png")
    pdf = OYM_Protocol_PDF(logo_exists)
    pdf.set_auto_page_break(auto=True, margin=15)

    # [cite_start]PAGE 1: CLINICAL GUIDELINES [cite: 10-20]
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Dear {data['dr_name']},", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, f"Enclosed is the customized drilling sequence for {data['patient_name']}. Flowcharts are color-coded to match the physical bands on your drills.")
    
    pdf.ln(5)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(180, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "  CRITICAL SURGICAL GUIDELINES:", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    guidelines = [
        [cite_start]"1. Guide Fit: Verify seating via inspection windows. Zero rocking. [cite: 15]",
        "2. [cite_start]Drill Insertion: Insert drill completely BEFORE starting rotation. [cite: 16]",
        "3. [cite_start]Drill Speed: 800-1200 RPM with copious saline irrigation. [cite: 18]",
        "4. Placement: 15-20 RPM. [cite_start]Target torque: 35-45 Ncm. [cite: 19]",
        "5. [cite_start]Sleeve Offset: Calibrated to 10.5mm (Bone Level). [cite: 151]"
    ]
    for line in guidelines:
        pdf.cell(0, 6, f"  {line}", ln=True)

    # [cite_start]PAGE 2: DRILLING SEQUENCE FLOWCHART [cite: 21-33]
    pdf.add_page()
    pdf.set_fill_color(60, 40, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    header_text = f"  SITE: Tooth {data['tooth']} | {data['system']} {data['type']} {data['dia']} x {data['length']} ({data['bone']} Bone)"
    pdf.cell(0, 10, header_text, ln=True, fill=True)
    
    pdf.ln(10)
    # Sequence Logic
    sys_info = SYSTEM_CONFIG.get(data['system'])
    drills = sys_info['base'] + [f"{data['dia']} Drill"]
    if data['bone'] == "Hard": drills.append("Cortical Tap")

    # Draw Boxes
    x, y = 15, pdf.get_y()
    for i, drill in enumerate(drills):
        pdf.set_fill_color(255, 250, 205)
        pdf.rect(x + (i%4*45), y + (i//4*20), 38, 14, 'FD')
        pdf.set_xy(x + (i%4*45), y + (i//4*20) + 2)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 8)
        pdf.multi_cell(38, 4, f"{drill}\n800-1200 RPM", align='C')
        if i < len(drills)-1 and (i+1)%4 != 0:
            pdf.set_xy(x + (i%4*45) + 38, y + (i//4*20) + 5)
            pdf.cell(7, 5, ">>")

    # [cite_start]PAGE 3: QA & ELITE CLUB [cite: 148-160]
    pdf.add_page()
    pdf.set_text_color(0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "POST-SURGICAL & QUALITY ASSURANCE", ln=True)
    pdf.set_font("Arial", size=10)
    [cite_start]pdf.cell(0, 8, "[ ] Guide seating verified on printed models. [cite: 150]", ln=True)
    [cite_start]pdf.cell(0, 8, "[ ] Sleeve offsets calibrated to 10.5mm. [cite: 151]", ln=True)
    
    pdf.ln(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "WELCOME TO THE OYM ELITE CLUB", ln=True, fill=True)
    pdf.set_font("Arial", size=10)
    [cite_start]pdf.multi_cell(0, 6, f"Dr. {data['dr_name']}, we have your patient's digital files ready! Let us craft your final Implant Prosthesis and Zirconium Crowns with VIP rates. [cite: 157-159]\nContact: +91 88383 02454")

    return bytes(pdf.output(dest='S'))

# --- 2. STREAMLIT INTERFACE ---
st.set_page_config(page_title="OYM Lab Generator", layout="wide")

with st.sidebar:
    st.header("Patient Info")
    dr = st.text_input("Doctor Name", "Dr. Naveen")
    pt = st.text_input("Patient Name", "Shrey Sipani")
    
    st.divider()
    st.header("Implant Specs")
    sys = st.selectbox("Company", list(SYSTEM_CONFIG.keys()))
    i_type = st.text_input("Implant Type (e.g. TS IV)", "TS IV")
    tooth = st.text_input("Tooth #", "14")
    dia = st.selectbox("Diameter", ["3.5mm", "4.0mm", "4.5mm", "5.0mm"])
    length = st.selectbox("Length", ["7mm", "8.5mm", "10mm", "11.5mm", "13mm"])
    bone = st.selectbox("Bone Quality", ["Normal", "Hard", "Soft"])

st.title("🦷 OYM Dental Lab: Professional Protocol")
if st.button("🚀 Generate Full Multi-Page Protocol"):
    data = {"dr_name": dr, "patient_name": pt, "system": sys, "type": i_type, 
            "tooth": tooth, "dia": dia, "length": length, "bone": bone}
    pdf_bytes = generate_full_protocol(data)
    st.download_button("Download High-Quality PDF", data=pdf_bytes, file_name=f"OYM_{pt}.pdf")
