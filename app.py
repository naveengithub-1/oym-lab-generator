import streamlit as st
from fpdf import FPDF
import os

# --- COLOR MAPPING FOR OSSTEM TS IV ---
DRILL_COLORS = {
    "Tissue Punch": (240, 240, 240),  # Grey/White
    "Flatten Drill": (220, 220, 220), # Grey
    "Initial Drill": (255, 255, 255), # White
    "2.2 Drill": (144, 238, 144),    # Light Green 
    "F3.5 Drill": (255, 255, 153),   # Yellow 
    "F4.0 Drill": (173, 216, 230),   # Light Blue 
    "F4.5 Drill": (255, 182, 193),   # Pink/Red 
    "F5.0 Drill": (200, 160, 255),   # Purple 
    "DEFAULT": (255, 250, 205)       # Cream
}

class OYMProtocolPDF(FPDF):
    def header(self):
        # Yellow header box
        self.set_fill_color(255, 215, 0)
        self.rect(40, 10, 160, 20, 'F')
        
        # Logo placeholder (Ensure OYM.png is in your directory)
        if os.path.exists("OYM.png"):
            self.image("OYM.png", 10, 8, 25)
        
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 18)
        self.set_xy(40, 12)
        self.cell(160, 10, 'OYM DENTAL LAB', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.set_x(40)
        self.cell(160, 5, 'Guided Surgery Protocol', ln=True, align='C')
        self.ln(15)

    def draw_drill_box(self, text, x, y, drill_name):
        # Determine color based on drill name
        color = DRILL_COLORS.get(drill_name.split("\n")[0], DRILL_COLORS["DEFAULT"])
        self.set_fill_color(*color)
        
        # Draw the box
        self.rect(x, y, 38, 14, 'FD')
        self.set_xy(x, y + 2)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 0, 0)
        self.multi_cell(38, 4, text, align='C')

    def draw_arrow(self, x, y):
        # Draw the ">>" symbol between boxes
        self.set_font('Arial', 'B', 12)
        self.set_text_color(150, 150, 150)
        self.set_xy(x, y + 4)
        self.cell(7, 5, ">>", align='C')

def generate_pro_protocol(data, sites):
    pdf = OYMProtocolPDF()
    pdf.add_page()
    
    # Intro [cite: 4, 5]
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Dear {data['dr_name']},", ln=True)
    pdf.multi_cell(0, 6, f"Enclosed is the customized drilling sequence tailored for the Osstem TS IV system for our patient, {data['patient_name']}. The flowcharts below are color-coded to match the physical bands on your drills.")
    pdf.ln(5)

    # Guidelines Section [cite: 10-20]
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(180, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "  CRITICAL SURGICAL GUIDELINES:", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=8)
    pdf.multi_cell(0, 5, 
        "1. Guide Fit: Verify seating via inspection windows. Ensure zero rocking before proceeding.\n"
        "2. Drill Insertion: Insert drill completely into sleeve BEFORE starting rotation.\n"
        "3. Drill Speed: 800-1200 RPM with copious saline irrigation.\n"
        "4. Placement: 15-20 RPM. Final torque: 35 to 45 Ncm. Do not exceed 45 Ncm.\n"
        "5. Sleeve Offset: All offsets calibrated to 10.5mm (Bone Level).")
    pdf.ln(5)

    # Site Sections
    for site in sites:
        pdf.set_fill_color(60, 40, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 9, f"  SITE: Tooth {site['tooth']} | Osstem TS IV Dia. {site['dia']} ({site['bone']} Bone)", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

        # Logic for drill list [cite: 23-31, 38-47]
        drills = ["Tissue Punch", "Flatten Drill", "Initial Drill"]
        if site['dia'] == "3.5mm": drills += ["2.2 Drill", "F3.5 Drill"]
        elif site['dia'] == "4.0mm": drills += ["F3.5 Drill", "F4.0 Drill"]
        
        x_start, y_start = 10, pdf.get_y()
        
        for idx, drill in enumerate(drills):
            # Calculate grid position (4 boxes per row)
            col = idx % 4
            row = idx // 4
            curr_x = x_start + (col * 47)
            curr_y = y_start + (row * 18)
            
            # Draw Box
            pdf.draw_drill_box(f"{drill}\n(800-1200 RPM)", curr_x, curr_y, drill)
            
            # Draw Arrow if not the last item in a row or sequence
            if idx < len(drills) - 1 and col < 3:
                pdf.draw_arrow(curr_x + 39, curr_y)
        
        pdf.set_y(curr_y + 20)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(0, 10, f"  >> Placement (15-20 RPM / Max 45Ncm) >> Fixture Driver", ln=True)
        pdf.ln(5)

    # Footer / Elite Club [cite: 156-160]
    pdf.set_y(-55)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "WELCOME TO THE OYM ELITE CLUB", ln=True, fill=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 5, f"Dr. {data['dr_name']}, we already have your patient's digital files ready! Let us craft your final Implant Prosthesis and Zirconium Crowns with priority milling and VIP rates.\nContact: +91 88383 02454")

    return bytes(pdf.output(dest='S'))

# --- STREAMLIT UI ---
st.title("🦷 OYM Dental Lab: Protocol Generator")

# Inputs
dr_name = st.sidebar.text_input("Doctor Name", "Dr. Naveen")
patient_name = st.sidebar.text_input("Patient Name", "Shrey Sipani")
tooth = st.sidebar.text_input("Tooth #", "14")
dia = st.sidebar.selectbox("Diameter", ["3.5mm", "4.0mm", "4.5mm", "5.0mm"])
bone = st.sidebar.selectbox("Bone Quality", ["Hard", "Normal", "Soft"])

if st.button("🚀 Generate PDF with Color Coding"):
    data = {"dr_name": dr_name, "patient_name": patient_name}
    sites = [{"tooth": tooth, "dia": dia, "bone": bone}]
    pdf_bytes = generate_pro_protocol(data, sites)
    st.download_button("Download High-Quality PDF", data=pdf_bytes, file_name=f"OYM_{patient_name}.pdf")
