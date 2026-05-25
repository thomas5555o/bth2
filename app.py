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

EMAIL_SENDER = "laaaaaora30ans@gmail.com"
EMAIL_PASSWORD = "ryiodbeucswsoduu"

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

    with open(
        "colors.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def save_colors(colors):

    with open(
        "colors.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            colors,
            f,
            ensure_ascii=False,
            indent=4
        )

# =========================
# EMAIL
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

    msg.attach(
        MIMEText(body, "plain")
    )

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )

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
 
st.write(
    "Entrez votre email puis lancez la roue."
)

email = st.text_input("Email")

# =========================
# RESET
# =========================



# =========================
# CHARGEMENT
# =========================

colors = load_colors()

if len(colors) == 0:

    st.error(
        "Toutes les couleurs ont été attribuées."
    )

    st.stop()

# =========================
# COULEURS VISUELLES
# =========================

wheel_colors_map = {
    "Rouge": "#F54927",
    "Bleu": "#2B8DED",
    "Vert": "#52ED2B",
    "Jaune": "#EDEA2B",
    "Rose": "#FF0F77",
    "Orange": "#FF830F",
    "Violet": "#B50085",
    "Noir": "#080708",
    "Blanc": "#FFFFFF",
    "Chocolat": "#803A05",
    "Beige": "#E8D5C8",
    "Gris": "#A6A6A6",
    "Turquoise": "#05EAF2",
    "Bordeaux": "#A10630",
    "Doré": "#FFDB6B"
}

# =========================
# BOUTON
# =========================

if st.button("🎲 Lancer la roue"):

    if email == "":

        st.error(
            "Veuillez entrer un email."
        )

        st.stop()

    # =========================
    # CHOIX ALEATOIRE
    # =========================

    selected_color = random.choice(colors)
    if selected_color =="Rouge": 
        text_selected_color="Bravo! Il te sera impossible de passer inaperçu. Prépare toi à attirer l'attention toute la soirée."
    if selected_color =="Bleu": 
        text_selected_color="Bravo! Tu viens officiellement d'être accepté au village des Schtroumpfs"
    if selected_color =="Vert": 
        text_selected_color="Chanceux(se). Tu es désormais responsable des bonnes vibes de la soirée."
    if selected_color =="Jaune": 
        text_selected_color="Ta mission : être plus lumineux(se) que les lumières de la salle."
    if selected_color =="Rose": 
        text_selected_color="Le Rose t'a choisi. Cette couleur exige un minimun de glamour. Prépare toi!"
    if selected_color =="Orange": 
        text_selected_color="Bravo. Energie et bonne humeur. Tu es officiellement chargé de réveiller la piste de danse."
    if selected_color =="Violet": 
        text_selected_color="Sacré Challenge. Epate-moi!"
    if selected_color =="Noir": 
        text_selected_color="Noir c'est Noir, il n'y a plus d'espoir. Tu seras clairement le plus chic de la soirée ... J'espère pour toi."
    if selected_color =="Blanc": 
        text_selected_color="Maintenant le vrai défi : Ne pas te salir de la soirée."
    if selected_color =="Chocolat": 
        text_selected_color="Impossible de ne pas t'aimer. Je te laisse relever le défi!"
    if selected_color =="Beige": 
        text_selected_color="Plus qu'à être une crème toute la soirée (surtout avec moi)"
    if selected_color =="Gris": 
        text_selected_color="Bravo! Tu es officiellement entre le noir trop sérieux et le blanc trop risqué."
    if selected_color =="Turquoise": 
        text_selected_color="Ambiance vacances au bord de la piscine même si on est juste dans un salon."
    if selected_color =="Bordeaux": 
        text_selected_color="Prouve moi que tu es comme le vin, que tu te bonifies"
    if selected_color =="Doré": 
        text_selected_color="Ton objectif : Briller plus que la déco. On saura que tu auras tout essayé."

        
        

    winner_index = colors.index(
        selected_color
    )

    total_segments = len(colors)

    angle_per_segment = 360 / total_segments

    # =========================
    # ANGLE FINAL
    # =========================
    # 0° CSS = haut
    # la flèche est en haut
    # on tourne la roue dans le sens horaire
    # donc on inverse l’angle

    center_angle = (
        winner_index * angle_per_segment
        + angle_per_segment / 2
    )

    target_angle = (
        3600 - center_angle
    )

    # =========================
    # SEGMENTS
    # =========================

    gradient_parts = []

    for i, color_name in enumerate(colors):

        start = i * angle_per_segment
        end = (i + 1) * angle_per_segment

        gradient_parts.append(
            f"""
            {wheel_colors_map[color_name]}
            {start}deg
            {end}deg
            """
        )

    gradient_css = ",".join(
        gradient_parts
    )

    # =========================
    # LABELS
    # =========================

    labels_html = ""

    radius = 170

    for i, color in enumerate(colors):

        # centre du segment
        angle = (
            i * angle_per_segment
            + angle_per_segment / 2
        )

        # conversion trigonométrique
        # CSS :
        # 0° = haut
        #
        # trigonométrie :
        # 0° = droite
        #
        # donc -90°

        rad = math.radians(
            angle - 90
        )

        x = 250 + radius * math.cos(rad)
        y = 250 + radius * math.sin(rad)

        labels_html += f"""
        <div
            style="
                position:absolute;

                left:{x}px;
                top:{y}px;

                width:140px;

                text-align:center;

                transform:
                    translate(-50%, -50%)
                    rotate({angle}deg);

                font-weight:bold;
                font-size:15px;
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

        animation:
            spin 6s
            cubic-bezier(
                0.17,
                0.67,
                0.12,
                0.99
            )
            forwards;
    }}

    @keyframes spin {{

        from {{
            transform: rotate(0deg);
        }}

        to {{
            transform:
                rotate({target_angle}deg);
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

        font-size:25px;
        font-weight:bold;

        color:green;

        opacity:0;

        animation:
            showResult 1s forwards;

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
        🎉 Verdict : {selected_color}\n ,\n {text_selected_color}
    </div>

    </body>

    </html>

    """

    components.html(
        html_code,
        height=750
    )

    # =========================
    # EMAIL
    # =========================

    try:

        send_email(
            email,
            selected_color
        )

        st.success(
            f"{selected_color} "
       
        )

    except Exception as e:

        st.error(
            f"Erreur email : {e}"
        )

    # =========================
    # SUPPRESSION DEFINITIVE
    # =========================

    colors.remove(selected_color)

    save_colors(colors)
