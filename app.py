import streamlit as st
import streamlit.components.v1 as components
import json
import random
import math
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# CONFIG EMAIL
# =========================

EMAIL_SENDER = "erfmdl095@gmail.com"
EMAIL_PASSWORD = "yrneeqbjdjtvuail"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# =========================
# CONFIG STREAMLIT
# =========================

st.set_page_config(
    page_title="Anniversaire Laora",
    layout="centered"
)

# =========================
# FONCTIONS
# =========================

def load_colors():
    with open("colors.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_colors(colors):
    with open("colors.json", "w", encoding="utf-8") as f:
        json.dump(colors, f, ensure_ascii=False, indent=4)

# =========================
# ENVOI EMAIL
# =========================

def send_email(receiver_email, color):

    subject = "Votre couleur"

    body = f"""
Bonjour,

Votre couleur attribuée est :

{color}

Merci !
"""

    msg = MIMEMultipart()

    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(
        EMAIL_SENDER,
        EMAIL_PASSWORD
    )

    server.send_message(msg)

    server.quit()

# =========================
# TITRE
# =========================

st.title("🎡 Roue des couleurs")

st.write("Entrez votre email puis lancez la roue.")

email = st.text_input("Email")

# =========================
# RESET
# =========================

if st.button("🔄 Réinitialiser les couleurs"):

    default_colors = [
        "Rouge tomate",
        "Orange carotte",
        "Jaune citron",
        "Jaune moutarde",
        "Vert avocat",
        "Vert menthe",
        "Vert pistache",
        "Marron chocolat",
        "Beige café latte",
        "Rose fraise",
        "Violet raisin",
        "Blanc crème",
        "Noir réglisse",
        "Bleu myrtille",
        "Rouge bordeaux"
    ]

    save_colors(default_colors)

    st.success("Couleurs réinitialisées.")

    st.rerun()

# =========================
# CHARGEMENT
# =========================

colors = load_colors()

if len(colors) == 0:
    st.error("Toutes les couleurs ont été attribuées.")
    st.stop()

# =========================
# BOUTON
# =========================

if st.button("🎲 Lancer la roue"):

    if email == "":
        st.error("Veuillez entrer un email.")
        st.stop()

    # =========================
    # CHOIX ALEATOIRE
    # =========================

    selected_color = random.choice(colors)

    winner_index = colors.index(selected_color)

    total_segments = len(colors)

    angle_per_segment = 360 / total_segments

    # =========================
    # ANGLE FINAL
    # =========================

    target_angle = (
        3600 +
        (
            270
            - (winner_index * angle_per_segment)
            - (angle_per_segment / 2)
        )
    )

    # =========================
    # COULEURS VISUELLES
    # =========================

    wheel_colors = [
        "#D62828",
        "#F77F00",
        "#F4D35E",
        "#D4A017",
        "#6A994E",
        "#2EC4B6",
        "#93C572",
        "#5C3A21",
        "#C8A27A",
        "#FF4F79",
        "#6F2DA8",
        "#FFF4E6",
        "#1C1C1C",
        "#4F6DDE",
        "#7B112C"
    ]

    # =========================
    # SEGMENTS
    # =========================

    gradient_parts = []

    for i in range(total_segments):

        start = i * angle_per_segment
        end = (i + 1) * angle_per_segment

        gradient_parts.append(
            f"{wheel_colors[i % len(wheel_colors)]} {start}deg {end}deg"
        )

    gradient_css = ", ".join(gradient_parts)

    # =========================
    # LABELS
    # =========================

    labels_html = ""

    radius = 170

    for i, color in enumerate(colors):

        angle = (i * angle_per_segment) + (angle_per_segment / 2)

        rad = math.radians(angle)

        x = 250 + radius * math.cos(rad)
        y = 250 + radius * math.sin(rad)

        labels_html += f"""
        <div
            style="
                position:absolute;
                left:{x}px;
                top:{y}px;

                transform:
                    translate(-50%, -50%)
                    rotate({angle + 90}deg);

                font-weight:bold;
                font-size:16px;
                color:black;

                z-index:50;
            "
        >
            {color}

        </div>
        """

    # =========================
    # HTML
    # =========================

    html_code = f"""

    <html>

    <head>

    <style>

    body {{
        text-align:center;
        font-family:Arial;
        background:#f0f0f0;
    }}

    .container {{
        position:relative;
        width:500px;
        height:500px;
        margin:auto;
    }}

    .wheel {{

        position:relative;

        width:500px;
        height:500px;

        border-radius:50%;

        border:12px solid #222;

        overflow:hidden;

        background:
        conic-gradient(
            {gradient_css}
        );

        animation: spin 6s cubic-bezier(0.17,0.67,0.12,0.99) forwards;
    }}

    @keyframes spin {{

        from {{
            transform: rotate(0deg);
        }}

        to {{
            transform: rotate({target_angle}deg);
        }}
    }}

    .pointer {{

        width:0;
        height:0;

        border-left:25px solid transparent;
        border-right:25px solid transparent;
        border-top:50px solid red;

        position:absolute;

        left:225px;
        top:-10px;

        z-index:100;
    }}

    .result {{

        margin-top:30px;

        font-size:48px;
        font-weight:bold;

        color:green;

        opacity:0;

        animation: showResult 1s forwards;
        animation-delay:6s;
    }}

    @keyframes showResult {{

        from {{
            opacity:0;
        }}

        to {{
            opacity:1;
        }}
    }}

    </style>

    </head>

    <body>

    <div class="container">

        <div class="pointer"></div>

        <div class="wheel">

            {labels_html}

        </div>

    </div>

    <div class="result">
        🎉 {selected_color}
    </div>

    </body>

    </html>

    """

    components.html(html_code, height=750)

    # =========================
    # EMAIL
    # =========================

    try:

        send_email(email, selected_color)

        st.success(
            f"Couleur attribuée : {selected_color}"
        )

    except Exception as e:

        st.error(f"Erreur email : {e}")

    # =========================
    # SUPPRESSION DEFINITIVE
    # =========================

    colors.remove(selected_color)

    save_colors(colors)
