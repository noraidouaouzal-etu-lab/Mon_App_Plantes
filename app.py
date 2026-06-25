import streamlit as st
import numpy as np
from PIL import Image
import io
import base64
import time
import os
import re

# ─── Page Config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="AI Plant Disease Detection | FSBM",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg-deep:      #060d0a;
    --bg-mid:       #0c1a12;
    --bg-card:      rgba(15, 30, 20, 0.75);
    --accent-green: #22c55e;
    --accent-lime:  #84cc16;
    --accent-teal:  #14b8a6;
    --text-primary: #e8f5e9;
    --text-muted:   #7aab88;
    --border:       rgba(34, 197, 94, 0.18);
    --glow:         rgba(34, 197, 94, 0.12);
    --radius:       16px;
    --radius-sm:    10px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(34,197,94,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(20,184,166,0.05) 0%, transparent 60%),
        var(--bg-deep) !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

section[data-testid="stSidebar"] { display: none !important; }

/* Fixed Logo */
.logo-fixed {
    position: fixed;
    top: 18px;
    left: 18px;
    z-index: 9999;
}
.logo-fixed img {
    height: 64px;
    width: auto;
    filter: drop-shadow(0 2px 12px rgba(34,197,94,0.35));
    border-radius: 8px;
    transition: transform .3s ease, filter .3s ease;
}
.logo-fixed:hover img {
    transform: scale(1.08) rotate(-1deg);
    filter: drop-shadow(0 4px 20px rgba(34,197,94,0.6));
}

.block-container {
    padding: 3rem 2.5rem 2rem 2.5rem !important;
    max-width: 1280px !important;
}

/* Header */
.header-wrap {
    text-align: center;
    padding: 2.5rem 1rem 2rem 1rem;
    margin-bottom: 1.5rem;
}
.header-tag {
    display: inline-block;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--accent-green);
    background: rgba(34,197,94,.1);
    border: 1px solid rgba(34,197,94,.25);
    border-radius: 20px;
    padding: .25rem .85rem;
    margin-bottom: 1rem;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    margin: 0 0 .6rem 0;
    background: linear-gradient(135deg, #a7f3d0 0%, var(--accent-green) 50%, var(--accent-teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
}
.header-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Cards */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 4px 32px var(--glow);
    transition: box-shadow .3s ease;
}
.card:hover { box-shadow: 0 6px 40px rgba(34,197,94,.18); }
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent-green);
    margin: 0 0 1rem 0;
    letter-spacing: .02em;
}

/* Upload placeholder */
.upload-placeholder {
    border: 2px dashed rgba(34,197,94,.28);
    border-radius: var(--radius-sm);
    text-align: center;
    padding: 2.5rem 1rem;
    color: var(--text-muted);
    background: rgba(34,197,94,.03);
}
.upload-icon { font-size: 2.8rem; margin-bottom: .6rem; }

[data-testid="stFileUploader"] {
    background: rgba(34,197,94,.04) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stFileUploadDropzone"] {
    border: 1px dashed rgba(34,197,94,.35) !important;
    border-radius: var(--radius-sm) !important;
    background: transparent !important;
}

/* Tips */
.tips-card { background: rgba(20,184,166,.07) !important; border-color: rgba(20,184,166,.2) !important; }
.tips-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: .55rem; }
.tips-list li { font-size: .88rem; color: var(--text-muted); line-height: 1.5; }

/* Primary button */
button[kind="primary"], [data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #16a34a 0%, var(--accent-green) 100%) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: #fff !important;
    padding: .7rem 2rem !important;
    box-shadow: 0 0 20px rgba(34,197,94,.3) !important;
    transition: box-shadow .3s ease, transform .2s ease !important;
    letter-spacing: .02em !important;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 32px rgba(34,197,94,.55) !important;
    transform: translateY(-1px) !important;
}

/* Analyzing */
.analyzing-box {
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: 1rem 1.2rem;
    background: rgba(34,197,94,.06);
    border: 1px solid rgba(34,197,94,.2);
    border-radius: var(--radius-sm);
    margin-top: .8rem;
    font-size: .95rem;
    color: var(--accent-green);
}
.pulse-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--accent-green);
    flex-shrink: 0;
    animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.4; transform:scale(.65); }
}

/* Badge */
.badge {
    display: inline-block;
    font-size: .8rem;
    font-weight: 600;
    border-radius: 20px;
    padding: .28rem .9rem;
    margin-bottom: 1.1rem;
    letter-spacing: .03em;
}

/* Result card */
.result-card { animation: fadeUp .45s ease forwards; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
.result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .85rem;
    margin-bottom: 1.2rem;
}
.result-item {
    background: rgba(255,255,255,.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: .85rem;
    display: flex;
    flex-direction: column;
    gap: .3rem;
}
.result-label {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.result-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* Confidence bar */
.confidence-block { margin-bottom: 1.1rem; }
.conf-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: .88rem;
    color: var(--text-muted);
    margin-bottom: .45rem;
}
.conf-pct {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}
.conf-bar-bg {
    height: 8px;
    background: rgba(255,255,255,.08);
    border-radius: 99px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width .8s cubic-bezier(.4,0,.2,1);
    box-shadow: 0 0 10px currentColor;
}

/* Explanation & Recommendation */
.explanation-box, .reco-box {
    border-radius: var(--radius-sm);
    padding: .9rem 1rem;
    margin-bottom: .85rem;
}
.explanation-box { background: rgba(255,255,255,.03); border: 1px solid var(--border); }
.reco-box        { background: rgba(34,197,94,.06);  border: 1px solid rgba(34,197,94,.22); }
.exp-label, .reco-label {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 0 0 .4rem 0;
}
.exp-text, .reco-text {
    font-size: .9rem;
    color: var(--text-primary);
    line-height: 1.65;
    margin: 0;
}

/* Voice card */
.voice-card { background: rgba(20,184,166,.07) !important; border-color: rgba(20,184,166,.22) !important; }
.voice-caption {
    font-size: .78rem;
    color: var(--text-muted);
    text-align: center;
    margin-top: .5rem;
    margin-bottom: 0;
}
[data-testid="stAudio"] { width: 100% !important; margin-top: .5rem; }

/* Placeholder right */
.placeholder-right {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 3rem 1.5rem !important;
}
.ph-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.ph-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 .5rem 0;
}
.ph-sub {
    font-size: .92rem;
    color: var(--text-muted);
    max-width: 320px;
    line-height: 1.6;
    margin: 0 0 2rem 0;
}
.stats-row { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.stat-box {
    background: rgba(34,197,94,.07);
    border: 1px solid rgba(34,197,94,.2);
    border-radius: var(--radius-sm);
    padding: .9rem 1.4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .25rem;
}
.stat-num { font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:var(--accent-green); }
.stat-lbl { font-size:.72rem; color:var(--text-muted); letter-spacing:.06em; text-transform:uppercase; }

/* Alert */
.alert-warn {
    background: rgba(234,179,8,.08);
    border: 1px solid rgba(234,179,8,.3);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    color: #fbbf24;
    font-size: .9rem;
    margin-bottom: 1.5rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    font-size: .8rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    letter-spacing: .02em;
}

[data-testid="stSpinner"] > div { border-top-color: var(--accent-green) !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: rgba(34,197,94,.3); border-radius: 99px; }
[data-testid="stImage"] img { border-radius: var(--radius-sm); }

@media (max-width: 768px) {
    .block-container { padding: 4.5rem 1rem 1rem !important; }
    .result-grid { grid-template-columns: 1fr; }
    .logo-fixed img { height: 48px; }
    .stats-row { gap: .6rem; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Heavy imports (after page config)
# ═══════════════════════════════════════════════════════════════════════════════
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from gtts import gTTS

# ═══════════════════════════════════════════════════════════════════════════════
# Disease knowledge base
# ═══════════════════════════════════════════════════════════════════════════════
DISEASE_INFO = {
    "Apple___Apple_scab": {
        "plant": "Pommier", "disease": "Tavelure du Pommier", "healthy": False,
        "explanation": "Maladie fongique causée par Venturia inaequalis. Provoque des taches brunes ou verdâtres sur les feuilles et les fruits, réduisant leur qualité marchande.",
        "recommendation": "Appliquez des fongicides à base de cuivre au printemps. Ramassez et détruisez les feuilles mortes. Favorisez une bonne aération entre les arbres.",
    },
    "Apple___Black_rot": {
        "plant": "Pommier", "disease": "Pourriture Noire", "healthy": False,
        "explanation": "Champignon Botryosphaeria obtusa responsable de taches foliaires annelées, de chancres sur les branches et de la pourriture des fruits.",
        "recommendation": "Taillez et brûlez les branches infectées. Appliquez un fongicide homologué pendant la saison de croissance. Évitez les blessures mécaniques sur l'écorce.",
    },
    "Apple___Cedar_apple_rust": {
        "plant": "Pommier", "disease": "Rouille Gymnosporange", "healthy": False,
        "explanation": "Maladie à cycle bipartite entre les genévriers et les pommiers. Provoque des taches orange vif sur les feuilles pouvant entraîner une défoliation.",
        "recommendation": "Retirez les genévriers proches si possible. Utilisez des variétés résistantes. Appliquez des fongicides préventifs au débourrement.",
    },
    "Apple___healthy": {
        "plant": "Pommier", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de pommier analysée ne présente aucun signe de maladie.",
        "recommendation": "Continuez les bonnes pratiques : arrosage régulier, taille annuelle et fertilisation équilibrée.",
    },
    "Blueberry___healthy": {
        "plant": "Myrtillier", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de myrtillier ne présente aucun symptôme pathologique.",
        "recommendation": "Maintenez un sol acide (pH 4.5–5.5) et assurez un arrosage régulier.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "plant": "Cerisier", "disease": "Oïdium", "healthy": False,
        "explanation": "Champignon Podosphaera clandestina recouvrant les feuilles d'un duvet blanc poudreux. Entraîne une distorsion des pousses et une réduction du rendement.",
        "recommendation": "Appliquez du soufre mouillable ou des fongicides systémiques. Évitez l'excès d'azote et favorisez la circulation d'air.",
    },
    "Cherry_(including_sour)___healthy": {
        "plant": "Cerisier", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de cerisier est saine et ne montre aucun signe de maladie.",
        "recommendation": "Assurez une taille régulière et un sol bien drainé.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant": "Maïs", "disease": "Tache Grise (Cercospora)", "healthy": False,
        "explanation": "Causée par Cercospora zeae-maydis, cette maladie produit des lésions rectangulaires gris-brun entre les nervures, réduisant la surface photosynthétique.",
        "recommendation": "Utilisez des variétés tolérantes. Effectuez une rotation des cultures. Appliquez des fongicides à base de strobilurine si nécessaire.",
    },
    "Corn_(maize)___Common_rust_": {
        "plant": "Maïs", "disease": "Rouille Commune", "healthy": False,
        "explanation": "Puccinia sorghi forme des pustules brun-rouge sur les deux faces des feuilles. Les épidémies sévères peuvent réduire significativement le rendement.",
        "recommendation": "Semez des variétés résistantes. Appliquez des fongicides en cas d'infection précoce avant la floraison.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant": "Maïs", "disease": "Helminthosporiose", "healthy": False,
        "explanation": "Exserohilum turcicum provoque de longues lésions elliptiques gris-vertes à brun-tan pouvant dépasser 15 cm.",
        "recommendation": "Pratiquez la rotation des cultures. Utilisez des hybrides résistants et appliquez des fongicides si nécessaire.",
    },
    "Corn_(maize)___healthy": {
        "plant": "Maïs", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de maïs est saine.",
        "recommendation": "Maintenez une fertilisation adaptée et une irrigation régulière.",
    },
    "Grape___Black_rot": {
        "plant": "Vigne", "disease": "Pourriture Noire de la Vigne", "healthy": False,
        "explanation": "Guignardia bidwellii cause des taches brun-rougeâtre sur les feuilles et une pourriture des baies qui deviennent noires et desséchées.",
        "recommendation": "Taillez pour améliorer l'aération. Retirez les débris infectés. Appliquez des fongicides du débourrement jusqu'à la véraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "plant": "Vigne", "disease": "Esca (Rougeot Parasitaire)", "healthy": False,
        "explanation": "Complexe fongique vasculaire dégradant le bois. Provoque des marbrures foliaires et peut conduire à la mort subite du pied.",
        "recommendation": "Protégez les plaies de taille avec une pâte cicatrisante fongicide. Supprimez et brûlez les parties atteintes.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant": "Vigne", "disease": "Brûlure Foliaire", "healthy": False,
        "explanation": "Pseudocercospora vitis provoque des taches angulaires brun foncé, une défoliation prématurée et un affaiblissement général de la plante.",
        "recommendation": "Améliorez la ventilation de la parcelle. Appliquez un fongicide à base de cuivre en prévention.",
    },
    "Grape___healthy": {
        "plant": "Vigne", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de vigne analysée est en parfaite santé.",
        "recommendation": "Continuez les traitements préventifs habituels et maintenez une taille soignée.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant": "Oranger", "disease": "HLB – Verdissement des Agrumes", "healthy": False,
        "explanation": "Maladie bactérienne transmise par un psylle. Provoque une chlorose asymétrique, des fruits déformés et aboutit à la mort de l'arbre.",
        "recommendation": "Aucun traitement curatif. Supprimez et détruisez les arbres atteints. Contrôlez le vecteur et utilisez des plants certifiés sains.",
    },
    "Peach___Bacterial_spot": {
        "plant": "Pêcher", "disease": "Tache Bactérienne", "healthy": False,
        "explanation": "Xanthomonas arboricola pv. pruni provoque des taches aqueuses puis nécrotiques sur les feuilles et des chancres sur les rameaux.",
        "recommendation": "Appliquez des bactéricides cupriques à la chute des feuilles et au printemps. Choisissez des variétés moins sensibles.",
    },
    "Peach___healthy": {
        "plant": "Pêcher", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de pêcher est saine.",
        "recommendation": "Assurez des traitements fongiques préventifs et une taille annuelle.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "plant": "Poivron", "disease": "Tache Bactérienne du Poivron", "healthy": False,
        "explanation": "Xanthomonas euvesicatoria crée des lésions aqueuses virant au brun sur les feuilles et les fruits.",
        "recommendation": "Utilisez des semences certifiées saines. Appliquez du cuivre + mancozèbe en préventif. Évitez l'irrigation par aspersion.",
    },
    "Pepper,_bell___healthy": {
        "plant": "Poivron", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de poivron est saine.",
        "recommendation": "Maintenez une irrigation régulière et une fertilisation équilibrée en potassium.",
    },
    "Potato___Early_blight": {
        "plant": "Pomme de Terre", "disease": "Alternariose (Mildiou Précoce)", "healthy": False,
        "explanation": "Alternaria solani produit des taches brunes concentriques en cible sur les vieilles feuilles.",
        "recommendation": "Appliquez des fongicides chlorothalonil ou mancozèbe dès les premiers symptômes. Pratiquez la rotation.",
    },
    "Potato___Late_blight": {
        "plant": "Pomme de Terre", "disease": "Mildiou (Phytophthora)", "healthy": False,
        "explanation": "Phytophthora infestans peut détruire une parcelle entière en quelques jours par temps humide et frais.",
        "recommendation": "Appliquez des fongicides systémiques (métalaxyl-M) à titre préventif. Détruisez les repousses et les débris de culture.",
    },
    "Potato___healthy": {
        "plant": "Pomme de Terre", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de pomme de terre est saine.",
        "recommendation": "Continuez les traitements préventifs et veillez à une bonne rotation des cultures.",
    },
    "Raspberry___healthy": {
        "plant": "Framboisier", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de framboisier est saine.",
        "recommendation": "Taillez les cannes après récolte et maintenez un sol frais et bien drainé.",
    },
    "Soybean___healthy": {
        "plant": "Soja", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de soja est saine.",
        "recommendation": "Assurez une inoculation rhizobienne et une fertilisation phosphatée adaptée.",
    },
    "Squash___Powdery_mildew": {
        "plant": "Courge", "disease": "Oïdium de la Courge", "healthy": False,
        "explanation": "Podosphaera xanthii recouvre les feuilles d'un mycélium blanc poudreux, provoquant chlorose et flétrissement.",
        "recommendation": "Appliquez du bicarbonate de potassium, du soufre ou un fongicide systémique. Favorisez la ventilation.",
    },
    "Strawberry___Leaf_scorch": {
        "plant": "Fraisier", "disease": "Brûlure Foliaire du Fraisier", "healthy": False,
        "explanation": "Diplocarpon earlianum crée de petites taches pourpres évoluant vers un centre brun clair donnant l'aspect de feuilles brûlées.",
        "recommendation": "Retirez et détruisez les feuilles infectées. Appliquez des fongicides après la récolte. Utilisez des variétés résistantes.",
    },
    "Strawberry___healthy": {
        "plant": "Fraisier", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de fraisier est saine.",
        "recommendation": "Renouvelez la plantation tous les 3–4 ans et maintenez un paillage propre.",
    },
    "Tomato___Bacterial_spot": {
        "plant": "Tomate", "disease": "Tache Bactérienne de la Tomate", "healthy": False,
        "explanation": "Xanthomonas spp. provoque de petites taches aqueuses brun-noir entourées d'un halo jaune, pouvant conduire à une défoliation importante.",
        "recommendation": "Traitez avec des bactéricides cupriques. Évitez l'arrosage par aspersion. Utilisez des semences certifiées.",
    },
    "Tomato___Early_blight": {
        "plant": "Tomate", "disease": "Alternariose de la Tomate", "healthy": False,
        "explanation": "Alternaria solani produit des taches brunes concentriques caractéristiques commençant sur les feuilles âgées.",
        "recommendation": "Supprimez les feuilles basses infectées. Appliquez du mancozèbe ou du chlorothalonil. Évitez l'humidité stagnante.",
    },
    "Tomato___Late_blight": {
        "plant": "Tomate", "disease": "Mildiou de la Tomate", "healthy": False,
        "explanation": "Phytophthora infestans crée des lésions huileuses vert-brun qui noircissent rapidement. Se propage très vite par temps frais et humide.",
        "recommendation": "Appliquez des fongicides systémiques en préventif. Aérez les cultures et évitez l'arrosage le soir. Détruisez les plantes très atteintes.",
    },
    "Tomato___Leaf_Mold": {
        "plant": "Tomate", "disease": "Moisissure Foliaire", "healthy": False,
        "explanation": "Passalora fulva produit des taches jaune-vert sur la face supérieure et un duvet olive à brun sur la face inférieure des feuilles.",
        "recommendation": "Réduisez l'humidité relative en aérant la serre. Appliquez des fongicides (chlorothalonil, mancozèbe).",
    },
    "Tomato___Septoria_leaf_spot": {
        "plant": "Tomate", "disease": "Septoriose de la Tomate", "healthy": False,
        "explanation": "Septoria lycopersici provoque de petites taches circulaires à centre gris-blanc et bordure brun foncé, conduisant à une défoliation sévère.",
        "recommendation": "Retirez les feuilles infectées. Évitez les éclaboussures d'eau. Appliquez du chlorothalonil ou du cuivre régulièrement.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "plant": "Tomate", "disease": "Acarien Tétranyque (Araignée Rouge)", "healthy": False,
        "explanation": "Tetranychus urticae cause une décoloration stipulée bronzée des feuilles puis leur desséchement. Infestation rapide par temps chaud et sec.",
        "recommendation": "Augmentez l'humidité ambiante. Appliquez des acaricides ou introduisez des acariens prédateurs. Évitez le stress hydrique.",
    },
    "Tomato___Target_Spot": {
        "plant": "Tomate", "disease": "Tache en Cible", "healthy": False,
        "explanation": "Corynespora cassiicola crée des lésions rondes concentriques brun foncé pouvant affecter feuilles, tiges et fruits.",
        "recommendation": "Appliquez des fongicides à base de mancozèbe ou de fluxapyroxad. Supprimez les débris végétaux et pratiquez la rotation des cultures.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "plant": "Tomate", "disease": "Virus de l'Enroulement Jaune (TYLCV)", "healthy": False,
        "explanation": "Transmis par Bemisia tabaci (aleurode). Provoque un enroulement et un jaunissement des jeunes feuilles et un rabougrissement de la plante.",
        "recommendation": "Contrôlez les aleurodes avec des insecticides ou des filets insect-proof. Utilisez des variétés résistantes (gène Ty). Détruisez les plantes très atteintes.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "plant": "Tomate", "disease": "Virus de la Mosaïque de la Tomate (ToMV)", "healthy": False,
        "explanation": "Virus très persistant transmis mécaniquement. Provoque une mosaïque vert clair/foncé sur les feuilles et une distorsion des fruits.",
        "recommendation": "Aucun traitement chimique. Utilisez des semences certifiées, désinfectez les outils. Privilégiez les variétés résistantes (Tm-2²).",
    },
    "Tomato___healthy": {
        "plant": "Tomate", "disease": "Plante Saine", "healthy": True,
        "explanation": "La feuille de tomate analysée ne présente aucun symptôme de maladie.",
        "recommendation": "Continuez les bonnes pratiques : arrosage à la base, taille des gourmands, fertilisation équilibrée et traitements préventifs.",
    },
}

def format_class_name(raw: str):
    parts = raw.split("___", 1)
    plant_raw = parts[0].replace("_", " ").replace(",", "").strip().title()
    disease_raw = parts[1].replace("_", " ").strip().title() if len(parts) > 1 else "Inconnue"
    disease_raw = re.sub(r"\s+", " ", disease_raw).rstrip()
    if disease_raw.lower() in ("healthy", "saine"):
        disease_raw = "Plante Saine"
    return plant_raw, disease_raw

# ═══════════════════════════════════════════════════════════════════════════════
# Model & prediction
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "MODELE_FINAL_96percent.keras"
    if not os.path.exists(model_path):
        return None
    try:
        # First try: safe_mode=False lets Keras deserialize the Lambda(preprocess_input) layer
        return tf.keras.models.load_model(
            model_path,
            custom_objects={"preprocess_input": preprocess_input},
            safe_mode=False,
        )
    except Exception:
        try:
            # Second try: compile=False as fallback
            return tf.keras.models.load_model(
                model_path,
                custom_objects={"preprocess_input": preprocess_input},
                compile=False,
                safe_mode=False,
            )
        except Exception as e:
            st.error(f"Échec du chargement du modèle : {e}")
            return None

@st.cache_data(show_spinner=False)
def get_class_names():
    return [
        "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
        "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew",
        "Cherry_(including_sour)___healthy", "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Corn_(maize)___Common_rust_", "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
        "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Grape___healthy", "Orange___Haunglongbing_(Citrus_greening)",
        "Peach___Bacterial_spot", "Peach___healthy", "Pepper,_bell___Bacterial_spot",
        "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
        "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
        "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot",
        "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
    ]

def preprocess_image(image, target_size=(224, 224)):
    # The model already has Lambda(preprocess_input) as its first layer,
    # so pass raw [0-255] float values — do NOT call preprocess_input again.
    img = image.convert("RGB").resize(target_size)
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    return arr

def predict(model, image):
    class_names = get_class_names()
    processed = preprocess_image(image)
    preds = model.predict(processed, verbose=0)
    idx = int(np.argmax(preds[0]))
    confidence = float(preds[0][idx]) * 100
    raw_class = class_names[idx] if idx < len(class_names) else f"Class_{idx}"
    return raw_class, confidence

# ═══════════════════════════════════════════════════════════════════════════════
# Voice
# ═══════════════════════════════════════════════════════════════════════════════
def generate_voice(plant, disease, confidence, recommendation):
    is_healthy = "saine" in disease.lower() or "healthy" in disease.lower()
    if is_healthy:
        text = (
            f"Analyse terminée. La plante détectée est {plant}. "
            f"La feuille est en bonne santé, avec une confiance de {confidence:.0f} pourcent. "
            "Continuez à prendre soin de vos plantes."
        )
    else:
        text = (
            f"Analyse terminée. La plante détectée est {plant}. "
            f"Maladie identifiée : {disease}, avec une confiance de {confidence:.0f} pourcent. "
            f"Recommandation : {recommendation}"
        )
    tts = gTTS(text=text, lang="fr", slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════
def get_logo_b64():
    path = "fsbm.png"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def confidence_badge(confidence, is_healthy):
    if is_healthy:
        color, label = "#22c55e", "✅ Saine"
    elif confidence >= 80:
        color, label = "#ef4444", "🦠 Maladie détectée"
    elif confidence >= 50:
        color, label = "#f97316", "⚠️ Probable"
    else:
        color, label = "#eab308", "❓ Faible confiance"
    return f'<span class="badge" style="background:{color}22;color:{color};border:1px solid {color}66">{label}</span>'

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # Fixed logo
    logo_b64 = get_logo_b64()
    if logo_b64:
        st.markdown(
            f'<div class="logo-fixed"><img src="data:image/png;base64,{logo_b64}" alt="FSBM Logo"/></div>',
            unsafe_allow_html=True,
        )

    # Header
    st.markdown(
        """
        <div class="header-wrap">
            <div class="header-tag">Deep Learning · Computer Vision</div>
            <h1 class="header-title">🌿 AI Plant Disease Detection</h1>
            <p class="header-sub">Système intelligent de reconnaissance des maladies des plantes par Deep Learning</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load model
    with st.spinner("Chargement du modèle EfficientNet…"):
        model = load_model()

    if model is None:
        st.markdown(
            '<div class="alert-warn">⚠️ Modèle introuvable. Placez <code>MODELE_FINAL_96percent.keras</code> dans le même dossier que <code>app.py</code>.</div>',
            unsafe_allow_html=True,
        )

    # Two columns
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📁 Téléverser une image</p>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            label="",
            type=["jpg", "jpeg", "png", "webp"],
            help="Formats acceptés : JPG, JPEG, PNG, WEBP",
        )

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Image chargée", width="stretch")
        else:
            st.markdown(
                '<div class="upload-placeholder"><div class="upload-icon">🌿</div>'
                '<p>Glissez-déposez une image de feuille ici<br/><small>JPG · PNG · WEBP · max 10 MB</small></p></div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card tips-card">
                <p class="card-title">💡 Conseils pour une meilleure précision</p>
                <ul class="tips-list">
                    <li>📸 Photographiez la feuille en lumière naturelle</li>
                    <li>🔍 Assurez-vous que la feuille occupe 70 % de l'image</li>
                    <li>🚫 Évitez les arrière-plans chargés</li>
                    <li>✂️ Utilisez une seule feuille par photo</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        if uploaded and model:
            image = Image.open(uploaded)

            if st.button("🔬 Analyser la maladie", width="stretch", type="primary"):
                with st.spinner(""):
                    st.markdown(
                        '<div class="analyzing-box"><div class="pulse-dot"></div>'
                        '<span>Intelligence Artificielle en cours d\'analyse…</span></div>',
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.6)
                    raw_class, confidence = predict(model, image)

                info = DISEASE_INFO.get(raw_class, {})
                plant = info.get("plant", format_class_name(raw_class)[0])
                disease = info.get("disease", format_class_name(raw_class)[1])
                explanation = info.get("explanation", "Aucune information supplémentaire disponible.")
                recommendation = info.get("recommendation", "Consultez un agronome local.")
                is_healthy = info.get("healthy", False)

                badge_html = confidence_badge(confidence, is_healthy)
                result_color = "#22c55e" if is_healthy else ("#ef4444" if confidence >= 80 else "#f97316")

                st.markdown(
                    f"""
                    <div class="card result-card" style="border-top:3px solid {result_color}">
                        <p class="card-title">🧬 Résultat de l'analyse</p>
                        {badge_html}
                        <div class="result-grid">
                            <div class="result-item">
                                <span class="result-label">🌱 Plante</span>
                                <span class="result-value">{plant}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">🦠 Maladie</span>
                                <span class="result-value">{disease}</span>
                            </div>
                        </div>
                        <div class="confidence-block">
                            <div class="conf-header">
                                <span>📊 Confiance</span>
                                <span class="conf-pct">{confidence:.1f}%</span>
                            </div>
                            <div class="conf-bar-bg">
                                <div class="conf-bar-fill" style="width:{confidence:.1f}%;background:{result_color}"></div>
                            </div>
                        </div>
                        <div class="explanation-box">
                            <p class="exp-label">📋 Description</p>
                            <p class="exp-text">{explanation}</p>
                        </div>
                        <div class="reco-box">
                            <p class="reco-label">💡 Recommandation</p>
                            <p class="reco-text">{recommendation}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown('<div class="card voice-card">', unsafe_allow_html=True)
                st.markdown('<p class="card-title">🔊 Écouter le diagnostic</p>', unsafe_allow_html=True)

                with st.spinner("Génération de l'audio…"):
                    audio_bytes = generate_voice(plant, disease, confidence, recommendation)

                st.audio(audio_bytes, format="audio/mp3")
                st.markdown(
                    f'<p class="voice-caption">Diagnostic vocal en français · {plant} · {disease}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        elif uploaded and model is None:
            st.markdown(
                '<div class="card"><p class="card-title">⚠️ Modèle non chargé</p>'
                "<p>Impossible d'effectuer l'analyse sans le modèle.</p></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="card placeholder-right">
                    <div class="ph-icon">🤖</div>
                    <p class="ph-title">En attente d'une image…</p>
                    <p class="ph-sub">Téléversez une photo de feuille dans le panneau de gauche,
                    puis cliquez sur <strong>Analyser</strong>.</p>
                    <div class="stats-row">
                        <div class="stat-box">
                            <span class="stat-num">96%</span>
                            <span class="stat-lbl">Précision</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-num">38</span>
                            <span class="stat-lbl">Classes</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-num">14</span>
                            <span class="stat-lbl">Espèces</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="footer">
            🌱 FS Ben M'Sik · Système de détection des maladies des plantes par IA
            &nbsp;|&nbsp; Université Hassan II de Casablanca
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()