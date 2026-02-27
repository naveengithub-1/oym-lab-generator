import streamlit as st
from fpdf import FPDF
import os

# --- SYSTEM & DRILL DATA ---
# Expand this dictionary to 10+ companies as needed
SYSTEM_DATA = {
    "Osstem TS IV": {
        "colors": {"2.2": (144, 238, 144), "F3.5": (255, 255, 153), "F4.0": (173, 216, 230), "F4.5": (255, 182, 193), "F5.0": (200, 160, 255)},
        "base_drills": ["Tissue Punch", "Flatten Drill", "Initial Drill"]
    },
    "Megagen AnyRidge": {"colors": {}, "base_drills": ["Guide Drill", "2.0 Drill"]},
    "Straumann BLX": {"colors": {}, "base_drills": ["Needle Drill", "2.2 Drill"]}
}

class OYM_PDF(FPDF):
    def header(self):
        # OYM Branding Header [cite: 2, 35, 78, 146]
        self.set_fill_color(255, 215, 0)
        self.rect(0, 0, 210, 30, 'F')
        
        # Logo Logic - Path check
        logo_path = "OYM.png" 
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 5, 20)
        
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 18)
        self.set_xy(0, 8)
        self.cell(210, 8, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(210, 5, 'Guided Surgery Protocol', ln=True, align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()} | Engineered with precision by OYM Dental Lab', align='C') [cite: 33, 76, 142, 161]

    def draw_drill_step(self, text, x, y, color=(255, 250, 205)):
        self.set_fill_color(*color)
        self.rect(x, y, 35, 12, 'FD')
        self.set_xy(x, y + 2)
        self.set_font('Arial', 'B', 8)
        self.multi_cell(35, 4, text, align='C')

def generate_pdf(data):
    pdf = OYM_PDF()
    
    # --- PAGE 1: PROTOCOL & GUIDELINES ---
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"Dear {data['dr_name']},", ln=True) [cite: 4]
    pdf.multi_cell(0, 6, f"Enclosed is the customized drilling sequence for {data['patient_name']}. Flowcharts are color-coded to match your {data['system']} drills.") [cite: 5, 6]
    
    # Guidelines [cite: 10-20]
    pdf.ln(5)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(180, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "  CRITICAL SURGICAL GUIDELINES:", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    g_lines = ["1. Guide Fit: Verify seating via windows.", "2. Drill Insertion: Insert BEFORE rotation.", "3. Speed: 800-1200 RPM with irrigation.", "4. Torque: 35-45 Ncm target."]
    for line in g_lines: pdf.cell(0, 6, f"  {line}", ln=True)

    # --- PAGE 2: DRILLING SEQUENCE ---
    pdf.add_page()
    pdf.set_fill_color(60, 40, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"  SITE: Tooth {data['tooth']} | {data['system']} {data['type']} {data['dia']} x {data['length']}", ln=True, fill=True) [cite: 22, 37, 49, 62]
    
    # Logic for Sequence
    pdf.ln(10)
    x, y = 15, pdf.get_y()
    steps = SYSTEM_DATA[data['system']]['base_drills'] + [f"F{data['dia']}"]
    
    for i, step in enumerate(steps):
        pdf.draw_drill_step(f"{step}\n800-1200 RPM", x + (i % 4 * 45), y + (i // 4 * 18))
        if i < len(steps)-1 and (i+1)%4 != 0:
            pdf.set_xy(x + (i % 4 * 45) + 36, y + (i // 4 * 18) + 4)
            pdf.cell(8, 5, ">>")

    # --- PAGE 3: QA & ELITE CLUB ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "POST-SURGICAL QUALITY ASSURANCE", ln=True) [cite: 148, 149]
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, "[ ] Guide seating verified. [ ] Sleeve offsets 10.5mm.", ln=True) [cite: 150, 151]
    
    pdf.ln(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "WELCOME TO THE OYM ELITE CLUB", ln=True, fill=True) [cite: 156]
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 6, f"Dr. {data['dr_name']}, we have patient digital files ready for Zirconium Crowns.\nContact: +91 88383 02454") [cite: 157, 158, 160]

    return bytes(pdf.output(dest='S'))

# --- STREAMLIT UI ---
st.set_page_config(page_title="OYM Lab Pro", layout="wide")
st.title("🦷 OYM Dental Lab: Professional Protocol")

with st.sidebar:
    st.header("Patient Info")
    dr = st.text_input("Doctor Name", "Dr. Naveen")
    pt = st.text_input("Patient Name", "Shrey Sipani")
    
    st.header("Implant Specs")
    sys = st.selectbox("Company", list(SYSTEM_DATA.keys()))
    i_type = st.text_input("Implant Type", "TS IV")
    tooth = st.text_input("Tooth #", "14")
    dia = st.selectbox("Diameter", ["3.5", "4.0", "4.5", "5.0"])
    length = st.selectbox("Length", ["8.5mm", "10mm", "11.5mm", "13mm"])

if st.button("🚀 Generate Full Multi-Page Protocol"):
    data = {"dr_name": dr, "patient_name": pt, "system": sys, "type": i_type, "tooth": tooth, "dia": dia, "length": length}
    pdf_bytes = generate_pdf(data)
    st.download_button("Download Pro PDF", data=pdf_bytes, file_name=f"OYM_{pt}.pdf")
