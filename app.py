pip install streamlit reportlab
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether
import io
from datetime import datetime

# -----------------------------
# PREMIUM COLOR PALETTE
# -----------------------------
BLACK = colors.HexColor("#000000")
GOLD = colors.HexColor("#D4AF37")
LIGHT_GOLD = colors.HexColor("#F5E6B3")

# -----------------------------
# ADVANCED IMPLANT DATABASE
# -----------------------------
IMPLANT_DATABASE = {

    "Osstem TSIV": {
        "drills": {
            "3.5": ["Tissue Punch", "Flatten Drill", "Initial Drill",
                    "2.2 Pilot", "3.5 Final"],
            "4.0": ["Tissue Punch", "Flatten Drill", "Initial Drill",
                    "2.2 Pilot", "3.5 Drill", "4.0 Final"],
            "5.0": ["Tissue Punch", "Flatten Drill", "Initial Drill",
                    "3.5 Drill", "4.5 Drill", "5.0 Final"]
        }
    },

    "Nobel Active": {
        "drills": {
            "3.5": ["Round Drill", "2.0 Twist", "3.5 Twist"],
            "4.3": ["Round Drill", "2.0 Twist", "3.5 Twist", "4.3 Final"]
        }
    },

    "Megagen AnyRidge": {
        "drills": {
            "4.0": ["Marking Drill", "2.0 Drill", "3.5 Drill", "4.0 Final"],
            "5.0": ["Marking Drill", "2.0 Drill", "4.0 Drill", "5.0 Final"]
        }
    },

    "Alpha Bio SPI": {
        "drills": {
            "3.75": ["Pilot Drill", "3.2 Drill", "3.75 Final"],
            "4.2": ["Pilot Drill", "3.2 Drill", "3.75 Drill", "4.2 Final"]
        }
    }
}

# -----------------------------
# BONE LOGIC
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
# PDF BUILDER
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

    # COVER PAGE
    elements.append(Image("/mnt/data/OYM.png", width=2*inch, height=2*inch))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("OYM ELITE GUIDED SURGERY PROTOCOL", gold_title))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Doctor: {data['doctor']}", normal_gold))
    elements.append(Paragraph(f"Patient: {data['patient']}", normal_gold))
    elements.append(Paragraph(f"Date: {datetime.today().strftime('%d-%m-%Y')}", normal_gold))
    elements.append(PageBreak())

    # GUIDELINES PAGE
    elements.append(Paragraph("CRITICAL SURGICAL GUIDELINES", gold_title))
    elements.append(Spacer(1, 15))

    guidelines = [
        "• Verify passive and stable guide seating.",
        "• Insert drill fully into sleeve BEFORE activation.",
        "• Maintain 800–1200 RPM with copious irrigation.",
        "• Never exceed 45 Ncm to avoid crestal necrosis.",
        "• Use cortical tap in D1 bone."
    ]

    for g in guidelines:
        elements.append(Paragraph(g, normal_gold))
        elements.append(Spacer(1, 8))

    elements.append(PageBreak())

    # EACH SITE PROTOCOL
    for site in data["sites"]:

        elements.append(Paragraph(
            f"Tooth {site['tooth']} | {site['system']} | "
            f"{site['diameter']} x {site['length']} | Bone: {site['bone']}",
            gold_title
        ))
        elements.append(Spacer(1, 12))

        drills = IMPLANT_DATABASE[site["system"]]["drills"].get(site["diameter"], [])

        if site["bone"] == "D1":
            drills.append("Cortical Tap")

        drills.append("Implant Placement")

        table_data = [["Step", "Instrument", "RPM", "Torque"]]

        for i, drill in enumerate(drills):
            rpm, torque = get_rpm_and_torque(drill, site["bone"])
            table_data.append([str(i+1), drill, rpm, torque])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GOLD),
            ('TEXTCOLOR', (0,0), (-1,0), BLACK),
            ('GRID', (0,0), (-1,-1), 0.5, GOLD),
            ('TEXTCOLOR', (0,1), (-1,-1), GOLD),
            ('BACKGROUND', (0,1), (-1,-1), BLACK)
        ]))

        elements.append(table)
        elements.append(PageBreak())

    # QA PAGE
    elements.append(Paragraph("POST SURGICAL QUALITY CONTROL", gold_title))
    elements.append(Spacer(1, 20))

    qa = [
        "[  ] Guide seating verified",
        "[  ] Sleeve offset confirmed",
        "[  ] Final torque recorded",
        "[  ] Implant stability confirmed"
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

st.set_page_config(page_title="OYM Elite Surgical Protocol", layout="wide")

st.title("🦷 OYM BLACK & GOLD ELITE PROTOCOL")

doctor = st.text_input("Doctor Name")
patient = st.text_input("Patient Name")

if "sites" not in st.session_state:
    st.session_state.sites = []

if st.button("Add Implant Site"):
    st.session_state.sites.append({})

for i in range(len(st.session_state.sites)):
    st.markdown(f"### Implant Site {i+1}")
    tooth = st.text_input("Tooth", key=f"tooth{i}")
    system = st.selectbox("System", list(IMPLANT_DATABASE.keys()), key=f"sys{i}")
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

if st.button("Generate Luxury Protocol PDF"):

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
