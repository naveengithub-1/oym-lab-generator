import streamlit as st
from fpdf import FPDF
import os

class OYMProtocolPDF(FPDF):
    def header(self):
        # Adding OYM Brand Identity
        if os.path.exists("OYM.png"):
            self.image("OYM.png", 10, 8, 25)
        
        # Yellow header box to match OYM branding
        self.set_fill_color(255, 215, 0)
        self.rect(40, 10, 160, 20, 'F')
        self.set_font('Arial', 'B', 18)
        self.set_xy(40, 12)
        self.cell(160, 10, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.set_x(40)
        self.cell(160, 5, 'Guided Surgery Protocol', ln=True, align='C')
        self.ln(15)

    def draw_drill_box(self, text, x, y, color):
        # Creates the color-coded flowchart boxes found in your PDF
        self.set_fill_color(*color)
        self.rect(x, y, 35, 12, 'FD')
        self.set_xy(x, y)
        self.set_font('Arial', 'B', 8)
        self.multi_cell(35, 6, text, align='C')

def generate_pro_protocol(data):
    pdf = OYMProtocolPDF()
    pdf.add_page()
    
    # Header Information
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"Dear {data['dr_name']},", ln=True)
    pdf.multi_cell(0, 7, f"Enclosed is the customized drilling sequence tailored for the {data['implant_system']} system for our patient, {data['patient_name']}. The flowcharts below are color-coded to match the physical bands on your drills.")
    pdf.ln(5)

    # Critical Guidelines Section [cite: 23-28, 51-61]
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(180, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "  CRITICAL SURGICAL GUIDELINES:", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 6, 
        "1. Guide Fit: Verify seating via inspection windows. Ensure zero rocking before proceeding.\n"
        "2. Drill Insertion: Insert drill completely into sleeve BEFORE starting rotation.\n"
        "3. Drill Speed: 800-1200 RPM with copious saline irrigation.\n"
        "4. Placement: 15-20 RPM. Final torque: 35 to 45 Ncm. Do not exceed 45 Ncm.\n"
        "5. Sleeve Offset: All offsets calibrated to 10.5mm (Bone Level).")
    pdf.ln(10)

    # Individual Drilling Flowchart Section [cite: 63-116]
    pdf.set_fill_color(60, 40, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"  SITE: Tooth {data['tooth_no']} | {data['implant_system']} Dia. {data['diameter']} ({data['bone_quality']} Bone)", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # Dynamic Drill Sequence Logic [cite: 64-115, 122-182]
    steps = ["Tissue Punch", "Flatten Drill", "Initial Drill"]
    if data['implant_system'] == "Osstem TS IV":
        if data['diameter'] == "3.5mm": steps.extend(["2.2 Drill", "F3.5 Drill"])
        elif data['diameter'] == "4.0mm": steps.extend(["F3.5 Drill", "F4.0 Drill"])
        elif data['diameter'] == "5.0mm": steps = ["Tissue Punch", "Flatten W", "Initial W", "F3.5 W", "F4.5 W", "F5.0 W"]
    
    # Draw Flowchart (2 rows)
    x_start, y_start = 10, pdf.get_y()
    colors = [(255, 250, 205), (255, 250, 205), (255, 250, 205), (255, 250, 205)]
    
    for i, step in enumerate(steps):
        col = i % 4
        row = i // 4
        pdf.draw_drill_box(step + "\n(800-1200 RPM)", x_start + (col * 45), y_start + (row * 20), colors[0])
    
    pdf.set_y(y_start + 45)

    # Elite Club Section [cite: 37-40, 197-201]
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "WELCOME TO THE OYM ELITE CLUB", ln=True, fill=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, f"Dr. {data['dr_name']}, we already have your patient's digital files ready! Let us craft your final Implant Prosthesis and Zirconium Crowns with priority milling and VIP rates.\nContact: +91 88383 02454")

    return bytes(pdf.output(dest='S'))

# --- STREAMLIT UI ---
st.set_page_config(page_title="OYM Lab Generator", page_icon="🦷")

if os.path.exists("OYM.png"):
    st.image("OYM.png", width=120)

st.title("🦷 OYM Dental Lab: Protocol Generator")

with st.expander("Clinical Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        dr_name = st.text_input("Doctor Name", "Dr. Naveen")
        patient_name = st.text_input("Patient Name", "Shrey Sipani")
        tooth_no = st.text_input("Tooth Number (e.g., 14, 25)", "14")
    with col2:
        implant_system = st.selectbox("Implant System", ["Osstem TS IV", "Megagen AnyRidge", "Straumann BLX"])
        diameter = st.selectbox("Diameter", ["3.5mm", "4.0mm", "4.5mm", "5.0mm"])
        bone_quality = st.selectbox("Bone Quality", ["Soft", "Normal", "Hard"])

if st.button("🚀 Generate Surgical Protocol"):
    data = {"dr_name": dr_name, "patient_name": patient_name, "tooth_no": tooth_no, 
            "implant_system": implant_system, "diameter": diameter, "bone_quality": bone_quality}
    pdf_bytes = generate_pro_protocol(data)
    st.download_button("Download High-Quality PDF", data=pdf_bytes, file_name=f"OYM_{patient_name}.pdf", mime="application/pdf")
