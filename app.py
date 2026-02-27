import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
import io
from datetime import datetime

# -----------------------------
# LUXURY COLORS
# -----------------------------
BLACK = colors.HexColor("#000000")
GOLD = colors.HexColor("#D4AF37")

# -----------------------------
# IMPLANT DATABASE
# -----------------------------
IMPLANT_DATABASE = {

    "Osstem TSIV": {
        "3.5": ["Tissue Punch", "Flatten Drill", "Initial Drill", "2.2 Pilot", "3.5 Final"],
        "4.0": ["Tissue Punch", "Flatten Drill", "Initial Drill", "2.2 Pilot", "3.5 Drill", "4.0 Final"],
        "5.0": ["Tissue Punch", "Flatten Drill", "Initial Drill", "3.5 Drill", "4.5 Drill", "5.0 Final"]
    },

    "Nobel Active": {
        "3.5": ["Round Drill", "2.0 Twist Drill", "3.5 Twist Drill"],
        "4.3": ["Round Drill", "2.0 Twist Drill", "3.5 Twist Drill", "4.3 Final Drill"]
    },

    "Megagen AnyRidge": {
        "4.0": ["Marking Drill", "2.0 Drill", "3.5 Drill", "4.0 Final Drill"],
        "5.0": ["Marking Drill", "2.0 Drill", "4.0 Drill", "5.0 Final Drill"]
    },

    "Alpha Bio SPI": {
        "3.75": ["Pilot Drill", "3.2 Drill", "3.75 Final Drill"],
        "4.2": ["Pilot Drill", "3.2 Drill", "3.75 Drill", "4.2 Final Drill"]
    }
}

# -----------------------------
# RPM & TORQUE LOGIC
# -----------------------------
def get_rpm_and_torque(stage, bone):

    if stage == "Implant Placement":

        if bone == "D1":
            return "15 RPM", "Max 35 Ncm"
        if bone == "D2":
            return "20 RPM", "35–45 Ncm"
        if bone == "D3":
            return "25 RPM", "30–40 Ncm"
        if bone == "D4":
            return "30 RPM", "25–35 Ncm"

    return "800–1200 RPM", "-"

# -----------------------------
# PDF GENERATOR
# -----------------------------
def generate_pdf(data):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    gold_title = ParagraphStyle(
        'GoldTitle',
        parent=styles['Heading1'],
        textColor=GOLD
    )

    normal_gold = ParagraphStyle(
        'NormalGold',
        parent=styles['Normal'],
        textColor=GOLD
    )

    # ---------------- COVER PAGE ----------------
    try:
        elements.append(Image("OYM.png", width=2*inch, height=2*inch))
    except:
        pass

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("OYM ELITE GUIDED SURGERY PROTOCOL", gold_title))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Doctor: {data['doctor']}", normal_gold))
    elements.append(Paragraph(f"Patient: {data['patient']}", normal_gold))
    elements.append(Paragraph(f"Date: {datetime.today().strftime('%d-%m-%Y')}", normal_gold))
    elements.append(PageBreak())

    # ---------------- GUIDELINES ----------------
    elements.append(Paragraph("CRITICAL SURGICAL GUIDELINES", gold_title))
    elements.append(Spacer(1, 15))

    guidelines = [
        "• Verify passive and stable guide seating before drilling.",
        "• Insert drill fully into sleeve BEFORE activation.",
        "• Maintain 800–1200 RPM with copious irrigation.",
        "• Do not exceed 45 Ncm to prevent crestal bone necrosis.",
        "• Use cortical tap in D1 bone density."
    ]

    for g in guidelines:
        elements.append(Paragraph(g, normal_gold))
        elements.append(Spacer(1, 8))

    elements.append(PageBreak())

    # ---------------- EACH IMPLANT SITE ----------------
    for site in data["sites"]:

        elements.append(Paragraph(
            f"Tooth {site['tooth']} | {site['system']} | "
            f"{site['diameter']} x {site['length']} mm | Bone: {site['bone']}",
            gold_title
        ))
        elements.append(Spacer(1, 12))

        drills = IMPLANT_DATABASE.get(site["system"], {}).get(site["diameter"], [])

        # Hard bone auto cortical tap
        if site["bone"] == "D1":
            drills = drills + ["Cortical Tap"]

        drills = drills + ["Implant Placement"]

        table_data = [["Step", "Instrument", "RPM", "Torque"]]

        for i, drill in enumerate(drills):
            rpm, torque = get_rpm_and_torque(drill, site["bone"])
            table_data.append([str(i+1), drill, rpm, torque])

        table = Table(table_data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GOLD),
            ('TEXTCOLOR', (0,0), (-1,0), BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, GOLD),
            ('TEXTCOLOR', (0,1), (-1,-1), GOLD),
        ]))

        elements.append(table)
        elements.append(PageBreak())

    # ---------------- QA PAGE ----------------
    elements.append(Paragraph("POST SURGICAL QUALITY CONTROL", gold_title))
    elements.append(Spacer(1, 20))

    qa = [
        "[  ] Guide seating verified",
        "[  ] Sleeve offset confirmed",
        "[  ] Final torque recorded",
        "[  ] Implant primary stability confirmed"
    ]

    for item in qa:
        elements.append(Paragraph(item, normal_gold))
        elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Lab Director Signature: ____________________", normal_gold))
    elements.append(Paragraph("Surgeon Signature: ____________________", normal_gold))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="OYM Elite Protocol", layout="wide")

st.title("🦷 OYM BLACK & GOLD ELITE SURGICAL PROTOCOL")

doctor = st.text_input("Doctor Name")
patient = st.text_input("Patient Name")

if "sites" not in st.session_state:
    st.session_state.sites = []

if st.button("Add Implant Site"):
    st.session_state.sites.append({})

for i in range(len(st.session_state.sites)):

    st.markdown(f"### Implant Site {i+1}")

    tooth = st.text_input("Tooth Number", key=f"tooth{i}")
    system = st.selectbox("Implant System", list(IMPLANT_DATABASE.keys()), key=f"sys{i}")
    diameter = st.selectbox("Diameter", ["3.5", "4.0", "4.3", "5.0"], key=f"dia{i}")
    length = st.text_input("Length (mm)", key=f"len{i}")
    bone = st.selectbox("Bone Density", ["D1", "D2", "D3", "D4"], key=f"bone{i}")

    st.session_state.sites[i] = {
        "tooth": tooth,
        "system": system,
        "diameter": diameter,
        "length": length,
        "bone": bone
    }

if st.button("Generate OYM Elite PDF"):

    payload = {
        "doctor": doctor,
        "patient": patient,
        "sites": st.session_state.sites
    }

    pdf = generate_pdf(payload)

    st.download_button(
        "Download OYM Elite Protocol",
        pdf,
        file_name=f"{patient}_OYM_Elite_Protocol.pdf",
        mime="application/pdf"
    )
