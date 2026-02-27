import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
import io
from datetime import datetime

# =========================
# LUXURY COLOR PALETTE
# =========================
GOLD = colors.HexColor("#D4AF37")
DARK_BROWN = colors.HexColor("#1A120B")
MID_BROWN = colors.HexColor("#3B2F2F")

# =========================
# STREAMLIT DARK BROWN THEME
# =========================
st.markdown("""
    <style>
    .stApp {
        background-color: #0F0A06;
        color: #D4AF37;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] div {
        background-color: #2A1F1A !important;
        color: #D4AF37 !important;
    }
    .stButton>button {
        background-color: #3B2F2F;
        color: #D4AF37;
        border-radius: 8px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# IMPLANT DATABASE
# =========================
IMPLANT_DATABASE = {
    "Nobel": {
        "types": ["CC", "Trilobe", "Zygoma", "Parallel"],
        "drills": {
            "3.5": ["Round Drill", "2.0 Twist", "3.5 Final"],
            "4.3": ["Round Drill", "2.0 Twist", "3.5 Drill", "4.3 Final"]
        }
    },
    "Osstem": {
        "types": ["TSIV", "TSIII"],
        "drills": {
            "3.5": ["Tissue Punch", "Flatten", "2.2 Pilot", "3.5 Final"],
            "4.0": ["Tissue Punch", "Flatten", "2.2 Pilot", "3.5", "4.0 Final"]
        }
    },
    "Megagen": {
        "types": ["AnyRidge", "Anyone"],
        "drills": {
            "4.0": ["Marking", "2.0", "3.5", "4.0 Final"],
            "5.0": ["Marking", "2.0", "4.0", "5.0 Final"]
        }
    }
}

# =========================
# RPM & TORQUE LOGIC
# =========================
def get_rpm_torque(stage, bone):

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

# =========================
# PDF GENERATOR
# =========================
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

    # HEADER
    try:
        elements.append(Image("OYM.png", width=1.8*inch, height=1.8*inch))
    except:
        pass

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("OYM ELITE GUIDED SURGERY PROTOCOL", gold_title))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Doctor: {data['doctor']}", normal_gold))
    elements.append(Paragraph(f"Patient: {data['patient']}", normal_gold))
    elements.append(Paragraph(f"Date: {datetime.today().strftime('%d-%m-%Y')}", normal_gold))
    elements.append(Spacer(1, 20))

    # SURGICAL GUIDELINES
    elements.append(Paragraph("CRITICAL SURGICAL GUIDELINES", gold_title))
    elements.append(Spacer(1, 10))

    guidelines = [
        "• Ensure passive guide seating.",
        "• Insert drill fully before activation.",
        "• Maintain 800–1200 RPM with irrigation.",
        "• Do not exceed 45 Ncm.",
        "• Use cortical tap in D1 bone."
    ]

    for g in guidelines:
        elements.append(Paragraph(g, normal_gold))
        elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 20))

    # IMPLANT TABLES
    for site in data["sites"]:

        elements.append(Paragraph(
            f"Tooth {site['tooth']} | {site['system']} {site['type']} | "
            f"{site['diameter']} x {site['length']} mm | Bone: {site['bone']}",
            gold_title
        ))
        elements.append(Spacer(1, 10))

        drills = IMPLANT_DATABASE[site["system"]]["drills"].get(site["diameter"], [])

        if site["bone"] == "D1":
            drills = drills + ["Cortical Tap"]

        drills = drills + ["Implant Placement"]

        table_data = [["Step", "Instrument", "RPM", "Torque"]]

        for i, drill in enumerate(drills):
            rpm, torque = get_rpm_torque(drill, site["bone"])
            table_data.append([str(i+1), drill, rpm, torque])

        table = Table(table_data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), MID_BROWN),
            ('TEXTCOLOR', (0,0), (-1,0), GOLD),
            ('GRID', (0,0), (-1,-1), 0.5, GOLD),
            ('TEXTCOLOR', (0,1), (-1,-1), GOLD),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 25))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# =========================
# UI
# =========================
st.image("OYM.png", width=150)

st.title("OYM BLACK & GOLD ELITE SURGICAL PROTOCOL")

doctor = st.text_input("Doctor Name")
patient = st.text_input("Patient Name")

if "sites" not in st.session_state:
    st.session_state.sites = []

if st.button("Add Implant Site"):
    st.session_state.sites.append({})

for i in range(len(st.session_state.sites)):

    st.markdown(f"### Implant Site {i+1}")

    tooth = st.text_input("Tooth Number", key=f"tooth{i}")
    system = st.selectbox("Implant Company", list(IMPLANT_DATABASE.keys()), key=f"sys{i}")

    implant_type = st.selectbox(
        "Implant Type",
        IMPLANT_DATABASE[system]["types"],
        key=f"type{i}"
    )

    diameter = st.selectbox(
        "Diameter",
        list(IMPLANT_DATABASE[system]["drills"].keys()),
        key=f"dia{i}"
    )

    length = st.text_input("Length (mm)", key=f"len{i}")
    bone = st.selectbox("Bone Density", ["D1", "D2", "D3", "D4"], key=f"bone{i}")

    st.session_state.sites[i] = {
        "tooth": tooth,
        "system": system,
        "type": implant_type,
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
