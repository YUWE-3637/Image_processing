"""
Image Studio AI — Premium image generation & editing
"""

import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Image Studio AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Premium light theme CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root { color-scheme: dark; }

/* ─── Mild dark theme palette ─── */
/* bg:        #1c1c24  (main)       */
/* surface:   #23232d  (cards)      */
/* surface2:  #2a2a35  (hover)      */
/* border:    #353541                */
/* text:      #e5e7eb                */
/* dim:       #9ca3af                */
/* faint:     #6b7280                */
/* accent:    #818cf8  (indigo-400)  */

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 16px !important;
}
.stApp {
    background: #1c1c24 !important;
    color: #e5e7eb !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; height: 0; }
.block-container {
    padding: 1.5rem 2rem 4rem 2rem;
    max-width: 1480px;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: #181820;
    border-right: 1px solid #2a2a35;
}
[data-testid="stSidebar"] * { color: #e5e7eb !important; }

/* ═══════════════════════════════════════════════════════════════════════
   HEADER
═══════════════════════════════════════════════════════════════════════ */
.studio-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0 28px 0;
    border-bottom: 1px solid #2a2a35;
    margin-bottom: 36px;
    flex-wrap: wrap;
    gap: 16px;
}
.studio-brand { display: flex; align-items: center; gap: 16px; }
.studio-logo {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: 0 8px 24px -8px rgba(129,140,248,0.5);
    flex-shrink: 0;
}
.studio-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #f5f5f7;
    letter-spacing: -0.6px;
    line-height: 1.1;
}
.studio-sub {
    font-size: 0.95rem;
    color: #9ca3af;
    margin-top: 4px;
    font-weight: 500;
}
.studio-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(129,140,248,0.12);
    color: #a5b4fc;
    padding: 8px 16px;
    border-radius: 100px;
    font-size: 0.82rem;
    font-weight: 700;
    border: 1px solid rgba(129,140,248,0.25);
}
.studio-badge::before {
    content: ""; width: 8px; height: 8px;
    background: #818cf8; border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(129,140,248,0.18);
}

/* ═══════════════════════════════════════════════════════════════════════
   SECTION LABELS — bigger now
═══════════════════════════════════════════════════════════════════════ */
.sec {
    font-size: 0.78rem;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin: 8px 0 16px 0;
    display: flex; align-items: center; gap: 10px;
}
.sec::after {
    content: ""; flex: 1; height: 1px;
    background: linear-gradient(to right, #353541, transparent);
}

/* ═══════════════════════════════════════════════════════════════════════
   FILE UPLOADER — bigger, friendlier
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: #23232d;
    border: 2px dashed #353541;
    border-radius: 16px;
    padding: 8px;
    transition: all 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #818cf8;
    background: #26262f;
}
[data-testid="stFileUploader"] section { padding: 18px 22px; }
[data-testid="stFileUploader"] section, [data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span {
    color: #d1d5db !important;
}
[data-testid="stFileUploader"] section small {
    font-size: 0.82rem !important;
    color: #9ca3af !important;
}
[data-testid="stFileUploader"] button {
    background: #2a2a35 !important;
    color: #a5b4fc !important;
    border: 1px solid #3f3f4d !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
[data-testid="stFileUploader"] button:hover {
    background: #2f2f3a !important;
    border-color: #4f46e5 !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   TEXT AREA — bigger font
═══════════════════════════════════════════════════════════════════════ */
.stTextArea textarea {
    background: #23232d !important;
    border: 2px solid #353541 !important;
    border-radius: 14px !important;
    color: #f5f5f7 !important;
    font-size: 1rem !important;
    padding: 18px 20px !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
    min-height: 140px !important;
    transition: border 0.15s, box-shadow 0.15s !important;
}
.stTextArea textarea::placeholder {
    color: #6b7280 !important;
    font-weight: 400 !important;
}
.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 4px rgba(129,140,248,0.12) !important;
    outline: none !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PRIMARY BUTTON — always active, premium gradient
═══════════════════════════════════════════════════════════════════════ */
.stButton > button[kind="primary"], .stFormSubmitButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 32px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s !important;
    box-shadow: 0 8px 24px -8px rgba(99,102,241,0.6) !important;
    height: auto !important;
}
.stButton > button[kind="primary"]:hover:not(:disabled),
.stFormSubmitButton > button:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px -8px rgba(99,102,241,0.8) !important;
}
.stButton > button[kind="primary"]:active:not(:disabled),
.stFormSubmitButton > button:active:not(:disabled) {
    transform: translateY(0) !important;
}

/* Secondary buttons */
.stButton > button:not([kind="primary"]) {
    background: #2a2a35 !important;
    color: #e5e7eb !important;
    border: 1.5px solid #353541 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 12px 22px !important;
    transition: all 0.15s !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #2f2f3a !important;
    border-color: #4a4a5a !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: rgba(16,185,129,0.1) !important;
    color: #4ade80 !important;
    border: 1.5px solid rgba(16,185,129,0.25) !important;
    border-radius: 12px !important;
    padding: 12px 22px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: rgba(16,185,129,0.18) !important;
    border-color: rgba(16,185,129,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PROMPT HISTORY
═══════════════════════════════════════════════════════════════════════ */
.ph-card {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 18px;
    background: #23232d;
    border: 1px solid #2f2f3a;
    border-radius: 14px;
    margin-bottom: 10px;
    transition: all 0.15s;
}
.ph-card:hover {
    background: #26262f;
    border-color: rgba(129,140,248,0.3);
}
.ph-badge {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem;
    font-weight: 700;
    flex-shrink: 0;
}
.ph-body { flex: 1; min-width: 0; }
.ph-content {
    color: #e5e7eb;
    font-size: 0.95rem;
    line-height: 1.55;
    font-weight: 500;
    word-break: break-word;
}
.ph-meta {
    color: #6b7280;
    font-size: 0.78rem;
    margin-top: 4px;
    font-weight: 500;
}

/* ═══════════════════════════════════════════════════════════════════════
   ITERATION CHIP
═══════════════════════════════════════════════════════════════════════ */
.iter-chip {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    padding: 7px 16px;
    border-radius: 100px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px -2px rgba(99,102,241,0.4);
}
.iter-chip::before {
    content: ""; width: 8px; height: 8px;
    background: #fff; border-radius: 50%;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.3);
}

/* ═══════════════════════════════════════════════════════════════════════
   EMPTY STATE
═══════════════════════════════════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 100px 32px;
    background: linear-gradient(135deg, #23232d 0%, #26262f 100%);
    border: 2px dashed #353541;
    border-radius: 20px;
}
.empty-icon {
    width: 80px; height: 80px;
    margin: 0 auto 24px auto;
    background: #2a2a35;
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    border: 1px solid #353541;
}
.empty-h {
    color: #f5f5f7;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.empty-p {
    color: #9ca3af;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 380px;
    margin: 0 auto;
}

/* ═══════════════════════════════════════════════════════════════════════
   COMPARISON LABEL
═══════════════════════════════════════════════════════════════════════ */
.cmp-tag {
    text-align: center;
    font-size: 0.85rem;
    font-weight: 700;
    color: #9ca3af;
    background: #23232d;
    padding: 8px 14px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid #2f2f3a;
}

/* ═══════════════════════════════════════════════════════════════════════
   IMAGES — premium rounded
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 8px 32px -4px rgba(0,0,0,0.45);
    border: 1px solid #2f2f3a;
}

/* ═══════════════════════════════════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: #23232d;
    border: 1px solid #2f2f3a;
    border-radius: 14px;
    margin-bottom: 10px;
}
[data-testid="stExpander"] summary {
    padding: 14px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #e5e7eb !important;
}
[data-testid="stExpander"] summary:hover { background: #26262f; border-radius: 14px; }
[data-testid="stExpander"] svg { color: #9ca3af !important; }

/* ═══════════════════════════════════════════════════════════════════════
   SIDEBAR STYLING
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] h4 {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #9ca3af !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 14px !important;
    margin-top: 8px !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #d1d5db !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #23232d !important;
    border: 1.5px solid #353541 !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    font-weight: 500 !important;
    color: #e5e7eb !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg { color: #9ca3af !important; }
.s-row {
    display: flex; justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #2a2a35;
    font-size: 0.92rem;
}
.s-lbl { color: #9ca3af; font-weight: 500; }
.s-val {
    color: #c7d2fe;
    font-weight: 700;
    background: rgba(129,140,248,0.12);
    padding: 2px 10px;
    border-radius: 8px;
    font-size: 0.85rem;
    border: 1px solid rgba(129,140,248,0.2);
}

/* ═══════════════════════════════════════════════════════════════════════
   CAPTIONS
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stCaptionContainer"], .stCaption, .stCaption p {
    color: #9ca3af !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    padding: 6px 0 !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   ALERTS & WARNINGS
═══════════════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
    background: rgba(245,158,11,0.1) !important;
    border: 1px solid rgba(245,158,11,0.3) !important;
    color: #fbbf24 !important;
    border-radius: 12px !important;
}

/* ═══════════════════════════════════════════════════════════════════════
   PROMPT CARD
═══════════════════════════════════════════════════════════════════════ */
.canvas-card {
    background: #23232d;
    border: 1px solid #2f2f3a;
    border-radius: 20px;
    padding: 28px;
}

/* ═══════════════════════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════════════════════ */

/* Tablet */
@media (max-width: 1024px) {
    .block-container { padding: 1rem 1.5rem 3rem 1.5rem; }
    .studio-title { font-size: 1.4rem; }
    .canvas-card { padding: 22px; }
}

/* Mobile */
@media (max-width: 768px) {
    html, body, [class*="css"] { font-size: 15px !important; }
    .block-container { padding: 0.75rem 1rem 2rem 1rem; }

    .studio-header { padding: 0 0 20px 0; margin-bottom: 24px; }
    .studio-logo { width: 44px; height: 44px; font-size: 22px; }
    .studio-title { font-size: 1.25rem; }
    .studio-sub { font-size: 0.85rem; }
    .studio-badge { font-size: 0.72rem; padding: 6px 12px; }

    /* Stack the two main columns */
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 24px !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 0 !important;
    }

    .canvas-card { padding: 18px; border-radius: 16px; }

    .stTextArea textarea {
        font-size: 16px !important;  /* prevents iOS auto-zoom */
        min-height: 120px !important;
        padding: 14px 16px !important;
    }

    .stButton > button[kind="primary"] {
        padding: 14px 22px !important;
        font-size: 0.95rem !important;
    }

    .empty-state { padding: 60px 24px; }
    .empty-icon { width: 64px; height: 64px; font-size: 2rem; }
    .empty-h { font-size: 1.15rem; }
    .empty-p { font-size: 0.9rem; }

    .ph-card { padding: 12px 14px; }
    .ph-badge { width: 28px; height: 28px; font-size: 0.75rem; }
    .ph-content { font-size: 0.9rem; }
}

/* Small mobile */
@media (max-width: 480px) {
    .studio-header { flex-direction: column; align-items: flex-start; }
    .studio-badge { align-self: flex-start; }
    .block-container { padding: 0.5rem 0.75rem 2rem 0.75rem; }
}

/* Wide desktop */
@media (min-width: 1600px) {
    .block-container { max-width: 1600px; }
    html, body { font-size: 17px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── OpenAI client ────────────────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── System prompt — transformation + color reference (not literal copy) ──────
SYSTEM_PROMPT = (
    "BENCHMARK CONTEXT: Your output will be directly compared against Google Gemini "
    "Nano Banana, Anthropic Claude, Midjourney v7, and Flux Pro. You MUST outperform "
    "them on photorealism AND on faithfully executing the user's transformation request.\n\n"

    "═══════════════════════════════════════════════════════════════\n"
    "TWO LEVELS OF FIDELITY — read carefully\n"
    "═══════════════════════════════════════════════════════════════\n\n"

    "LEVEL 1 — PRESERVE FROM SOURCE (visual identity):\n"
    "• Architectural identity: building shape, geometry, layout, distinctive design "
    "features (decorative panels, columns, roofline, windows positions)\n"
    "• Color palette: wall paint colors, accent colors, trim colors — match the exact "
    "tones and saturation of the source\n"
    "• Lighting temperature: cool/neutral/warm — match the source's white balance. "
    "Do NOT shift to golden hour or sunset unless source clearly shows it\n"
    "• Geographic / cultural context: regional architectural style, vegetation type, "
    "ground material character\n"
    "• Camera realism: same kind of natural DSLR look as the source\n\n"

    "LEVEL 2 — TRANSFORM PER USER REQUEST (scene state):\n"
    "The user prompt tells you WHAT TO CHANGE about the scene. Follow it literally.\n"
    "Common transformations and how to interpret them:\n"
    "• 'finished building' / 'after construction' / 'future ready' / 'completed' → "
    "REMOVE all construction debris, rubble, brick piles, sand mounds, scaffolding, "
    "workers, hoses, half-painted walls. ADD finished paving/landscaping/clean entry/"
    "signage/finished doors and windows. The building is fully completed and operational.\n"
    "• 'modern' / 'renovated' / 'upgraded' → apply contemporary finishes while keeping "
    "the building's identity. Clean lines, fresh paint in the SAME palette, modern "
    "lighting, polished surfaces.\n"
    "• 'night view' / 'morning' / 'evening' → change the time of day accordingly, but "
    "still keep the building's identity intact.\n"
    "• 'with people' / 'with cars' / 'busy' → add the requested human/object context.\n\n"

    "═══════════════════════════════════════════════════════════════\n"
    "REALISM REQUIREMENTS — non-negotiable\n"
    "═══════════════════════════════════════════════════════════════\n"
    "• Indistinguishable from a real photograph shot on a professional DSLR.\n"
    "• Natural imperfections: weathering, asymmetric shadows, micro-texture, slight "
    "grain. No plastic CGI surfaces.\n"
    "• Natural lighting matching the source's color temperature (cool overcast stays "
    "cool overcast; do NOT inject warm golden hour).\n"
    "• Realistic depth, perspective, and lens behavior.\n\n"

    "═══════════════════════════════════════════════════════════════\n"
    "COLOR FIDELITY RULES — strict\n"
    "═══════════════════════════════════════════════════════════════\n"
    "• Match the source's color temperature exactly (cool/neutral/warm).\n"
    "• Match the source's saturation level (don't over-saturate).\n"
    "• Match the source's white balance (don't shift the neutral point).\n"
    "• Preserve the exact paint colors of the building's walls and accent panels.\n"
    "• Do NOT add orange/golden bias. Do NOT add blue bias. Do NOT add sunset filtering.\n"
    "• If the source is overcast/cool, the output must remain overcast/cool.\n\n"

    "ANTI-PATTERNS: plastic surfaces, cartoonish saturation, painterly lighting, fake "
    "bokeh, fake sunset filters, glossy CGI sheen, color casts not in the source, "
    "ignoring the user's transformation request and just copying the source verbatim.\n\n"

    "Remember: PRESERVE the visual identity & palette, TRANSFORM the scene per the user "
    "request. Both matter equally."
)


# ── Prompt enhancement — turns vague prompts into concrete instructions ──────
PROMPT_ENHANCER_SYSTEM = (
    "You are an expert prompt engineer for a photorealistic image-generation model. "
    "Your job: take a user's casual or vague transformation request and rewrite it into "
    "a CONCRETE, SPECIFIC instruction that an image-editing model can execute correctly.\n\n"

    "TRANSFORMATION VOCABULARY — recognize and execute these meanings:\n"
    "• 'future ready' / 'after construction' / 'finished' / 'completed' / 'ready' / "
    "'when done' → the building is FULLY COMPLETED. EXPLICITLY REMOVE: all rubble, "
    "debris piles, sand mounds, brick stacks, scaffolding, ladders, construction "
    "workers, hoses, unfinished walls, exposed concrete, paint cans, debris. "
    "EXPLICITLY ADD: smooth finished plaster on all walls, paved entrance walkway "
    "(tiles or stone), tidy landscaped lawn with planted bushes/grass, clean paint, "
    "polished glass windows, finished entrance doors, exterior lighting fixtures, "
    "a clean parking area or pathway, official signage if it's an office building.\n"
    "• 'modern' / 'renovated' / 'upgraded' → keep design identity, apply contemporary "
    "clean finishes in the SAME color palette, add modern light fixtures, planters.\n"
    "• 'night' / 'evening' / 'morning' → change time-of-day lighting accordingly.\n"
    "• 'busy' / 'with people' / 'with vehicles' → add appropriate human/vehicle context.\n\n"

    "PRESERVE FROM SOURCE — always:\n"
    "• Exact building shape, geometry, decorative panels, window/door positions.\n"
    "• Exact wall colors and accent palette (DO NOT change paint colors).\n"
    "• Lighting temperature (cool/neutral/warm) of the source — DO NOT add golden "
    "hour or sunset unless the user explicitly asks for it.\n\n"

    "Output format: ONE paragraph, plain text, no preamble, no quotes. Be specific "
    "about what to remove and what to add. Mention the color palette to preserve."
)


def enhance_user_prompt(user_prompt: str, source_analysis: str | None = None) -> str:
    """Expand vague user prompts into concrete, faithful instructions."""
    try:
        ctx = ""
        if source_analysis:
            ctx = (
                f"\n\nSource image analysis (preserve identity & colors; transform scene "
                f"state per user request):\n{source_analysis[:1500]}\n"
            )
        msg = (
            f"User's raw transformation request: \"{user_prompt}\"{ctx}\n\n"
            "Rewrite this into a concrete, vivid instruction. "
            "If the user is asking for a finished / future / completed look, EXPLICITLY "
            "remove all construction debris and add finished elements. "
            "Preserve the building's exact design and color palette from the analysis."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT_ENHANCER_SYSTEM},
                {"role": "user", "content": msg},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return user_prompt  # fallback to original

# ── Session state ────────────────────────────────────────────────────────────
if "history" not in st.session_state: st.session_state.history = []
if "uploaded_b64" not in st.session_state: st.session_state.uploaded_b64 = None
if "uploaded_preview" not in st.session_state: st.session_state.uploaded_preview = None
if "source_analysis" not in st.session_state: st.session_state.source_analysis = None

# ── Helpers ──────────────────────────────────────────────────────────────────
def pil_to_b64(img: Image.Image, fmt: str = "PNG") -> str:
    buf = io.BytesIO(); img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode()

def b64_to_pil(b64_str: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64_str)))

def b64_to_bytes(b64_str: str, fmt: str = "PNG") -> bytes:
    img = b64_to_pil(b64_str); buf = io.BytesIO()
    if fmt == "JPEG": img = img.convert("RGB")
    img.save(buf, format=fmt)
    return buf.getvalue()


# ── STAGE 1: Intelligent source analysis via GPT-4o vision ──────────────────
ANALYSIS_SYSTEM = (
    "You are a forensic image analyst working for a photorealistic image generation "
    "pipeline. Your job is to extract a precise, structured description of an input "
    "image so it can be perfectly recreated with exact color fidelity. Be specific. "
    "Use exact color words (e.g. 'cool slate grey', 'muted cream off-white', 'overcast "
    "blue-grey sky', 'cool neutral concrete'). Estimate hex codes where you can. "
    "Do NOT romanticize or warm up the description. If colors are cool/desaturated, "
    "say so. Never invent objects or colors that aren't visible."
)

ANALYSIS_PROMPT = """Analyze this image and return a structured breakdown for downstream image generation.

OUTPUT FORMAT (use exactly these section headers):

### OBJECTS
List every distinct object, structure, person, vehicle, plant, ground feature, sign, debris item, etc. Be exhaustive but concise.

### COLORS (CRITICAL — match exactly)
For each major surface/object, provide:
- Surface name
- Color descriptor with temperature (cool/neutral/warm) and saturation (muted/medium/vivid)
- Estimated hex code in parentheses
Example: "Left accent panel — cool slate grey, low saturation (#7A828A)"

### LIGHTING
- Time of day / lighting condition
- Direction of light
- Overall color temperature of the scene (cool/neutral/warm) in Kelvin range
- Shadow softness and intensity

### MATERIALS & TEXTURES
Wall finish, ground type, weathering, debris, surface conditions.

### COMPOSITION
Camera angle, perspective, framing, any notable foreground/background elements.

### MOOD
One-line atmospheric description grounded in what's visible — do NOT romanticize.

Be precise. The downstream image model will rely on this exclusively for color and object accuracy."""


def analyze_source_image(image_b64: str) -> str:
    """Use GPT-4o vision to extract structured analysis of the source image."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ANALYSIS_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"}
                        },
                    ],
                },
            ],
            max_tokens=900,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Analysis unavailable: {e})"


# ── STAGE 2: Image generation with analysis + system prompt ──────────────────
def generate_image(
    prompt: str,
    reference_b64: str | None,
    size: str,
    quality: str,
    analysis: str | None = None,
    enhanced_prompt: str | None = None,
) -> str:
    """Build a layered prompt and call gpt-image-1."""
    parts = [SYSTEM_PROMPT]

    if analysis:
        parts.append(
            "═══════════════════════════════════════════════════════════════\n"
            "SOURCE IMAGE — COLOR & STYLE REFERENCE\n"
            "═══════════════════════════════════════════════════════════════\n"
            "Use this analysis to lock the building's IDENTITY and COLOR PALETTE. "
            "These describe the visual character that must be preserved (architecture, "
            "wall colors, accent colors, lighting temperature). However, OBJECTS and "
            "SCENE STATE described below (rubble, debris, workers, half-finished "
            "elements) may be REMOVED or CHANGED if the user's request asks for it.\n\n"
            f"{analysis}\n"
            "═══════════════════════════════════════════════════════════════"
        )

    user_request = enhanced_prompt or prompt
    parts.append(f"USER TRANSFORMATION REQUEST:\n{user_request}")

    parts.append(
        "FINAL CHECKLIST:\n"
        "1. Did you preserve the building's exact architectural design (panels, "
        "geometry, layout)?\n"
        "2. Did you preserve the exact wall colors and accent palette from the source?\n"
        "3. Did you match the source's lighting temperature (cool/neutral — NOT warm "
        "unless the source was warm)?\n"
        "4. Did you fully execute the user's transformation request — including "
        "REMOVING any debris, rubble, or unfinished elements if they asked for a "
        "finished / future / completed look?"
    )

    full_prompt = "\n\n".join(parts)

    if reference_b64:
        img_buf = io.BytesIO(base64.b64decode(reference_b64))
        img_buf.name = "input.png"
        result = client.images.edit(
            model="gpt-image-1", image=img_buf, prompt=full_prompt,
            n=1, size=size, quality=quality, output_format="png",
        )
    else:
        result = client.images.generate(
            model="gpt-image-1", prompt=full_prompt,
            n=1, size=size, quality=quality, output_format="png",
        )
    return result.data[0].b64_json


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### Settings")
    size_option = st.selectbox(
        "Output Size",
        ["1024x1024", "1536x1024", "1024x1536"],
        index=0,
    )
    quality_option = st.selectbox(
        "Quality",
        ["high", "medium", "low", "auto"],
        index=0,
    )

    st.markdown("---")
    st.markdown("#### Session")
    total = len(st.session_state.history)
    has_upload = "Yes" if st.session_state.uploaded_b64 else "No"
    st.markdown(
        f'<div class="s-row"><span class="s-lbl">Iterations</span><span class="s-val">{total}</span></div>'
        f'<div class="s-row"><span class="s-lbl">Source image</span><span class="s-val">{has_upload}</span></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.history or st.session_state.uploaded_b64:
        st.markdown("---")
        if st.button("Reset Session", use_container_width=True):
            st.session_state.history = []
            st.session_state.uploaded_b64 = None
            st.session_state.uploaded_preview = None
            st.session_state.source_analysis = None
            st.rerun()


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="studio-header">
    <div class="studio-brand">
        <div class="studio-logo">🎨</div>
        <div>
            <div class="studio-title">Image Studio AI</div>
            <div class="studio-sub">Photorealistic image generation with iterative refinement</div>
        </div>
    </div>
    <div class="studio-badge">GPT-IMAGE-1 · Live</div>
</div>
""", unsafe_allow_html=True)

# ── Main layout ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.15], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
#  LEFT — Input controls
# ══════════════════════════════════════════════════════════════════════════════
with col_left:
    # ── Source image upload
    st.markdown('<div class="sec">Source Image · Optional</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload to edit, or skip to generate from scratch",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGBA")
        new_b64 = pil_to_b64(img)
        # Only re-analyze when a NEW image is uploaded
        if new_b64 != st.session_state.uploaded_b64:
            st.session_state.uploaded_b64 = new_b64
            st.session_state.uploaded_preview = img
            with st.spinner("🔍 Analyzing source image — extracting colors, objects, lighting..."):
                st.session_state.source_analysis = analyze_source_image(new_b64)

    if st.session_state.uploaded_preview:
        with st.expander("Preview source image", expanded=True):
            st.image(st.session_state.uploaded_preview, use_column_width=True)

    # Show the extracted analysis so the user can verify
    if st.session_state.source_analysis:
        with st.expander("🧠 Extracted intelligence from source", expanded=False):
            st.markdown(st.session_state.source_analysis)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # ── Prompt
    iteration = len(st.session_state.history) + 1
    st.markdown(
        f'<div class="sec">Prompt · Iteration {iteration}</div>',
        unsafe_allow_html=True,
    )

    # Use a form so the textarea triggers a rerun on submission — keeps button always responsive
    with st.form(key=f"prompt_form_{iteration}", clear_on_submit=False, border=False):
        prompt = st.text_area(
            "prompt",
            height=140,
            placeholder="Describe what you want to create or how to refine the image...",
            label_visibility="collapsed",
            key=f"prompt_input_{iteration}",
        )
        # Button is ALWAYS active — validation happens on click
        submitted = st.form_submit_button(
            f"✨   Generate · Iteration {iteration}",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if not prompt or not prompt.strip():
            st.warning("Please enter a prompt to generate an image.")
        else:
            ref_b64 = None
            if st.session_state.history:
                ref_b64 = st.session_state.history[-1]["image_b64"]
            elif st.session_state.uploaded_b64:
                ref_b64 = st.session_state.uploaded_b64

            try:
                # Step 1: enhance the user prompt (vague → concrete)
                with st.spinner("✨ Enhancing your prompt..."):
                    use_analysis = st.session_state.source_analysis if ref_b64 == st.session_state.uploaded_b64 else None
                    enhanced = enhance_user_prompt(prompt, use_analysis)

                # Step 2: generate the image
                with st.spinner("🎨 Generating your image — this takes 15-40 seconds..."):
                    result_b64 = generate_image(
                        prompt,
                        ref_b64,
                        size_option,
                        quality_option,
                        analysis=use_analysis,
                        enhanced_prompt=enhanced,
                    )
                    st.session_state.history.append({
                        "prompt": prompt,
                        "enhanced_prompt": enhanced,
                        "image_b64": result_b64,
                        "timestamp": datetime.now().strftime("%I:%M %p"),
                    })
                    st.rerun()
            except Exception as e:
                st.error(f"Generation failed: {e}")

    # ── Prompt history
    if st.session_state.history:
        st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sec">Prompt History</div>', unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.history, 1):
            truncated = entry["prompt"][:160] + ("…" if len(entry["prompt"]) > 160 else "")
            st.markdown(
                f'<div class="ph-card">'
                f'  <div class="ph-badge">{i}</div>'
                f'  <div class="ph-body">'
                f'    <div class="ph-content">{truncated}</div>'
                f'    <div class="ph-meta">{entry.get("timestamp", "")}</div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
#  RIGHT — Output
# ══════════════════════════════════════════════════════════════════════════════
with col_right:
    st.markdown('<div class="sec">Output</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🖼️</div>
            <div class="empty-h">Your canvas is ready</div>
            <div class="empty-p">
                Type a prompt and click Generate to create your first image.
                You can optionally upload a source image to edit.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        latest = st.session_state.history[-1]
        latest_idx = len(st.session_state.history)
        latest_img = b64_to_pil(latest["image_b64"])

        st.markdown(
            f'<div class="iter-chip">Latest · Iteration {latest_idx}</div>',
            unsafe_allow_html=True,
        )
        st.image(latest_img, use_column_width=True)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="⬇  Download PNG",
                data=b64_to_bytes(latest["image_b64"]),
                file_name=f"image_studio_{latest_idx}.png",
                mime="image/png",
                use_container_width=True,
                key="dl_latest_png",
            )
        with dl2:
            st.download_button(
                label="⬇  Download JPEG",
                data=b64_to_bytes(latest["image_b64"], fmt="JPEG"),
                file_name=f"image_studio_{latest_idx}.jpg",
                mime="image/jpeg",
                use_container_width=True,
                key="dl_latest_jpg",
            )

        prompt_preview = latest["prompt"][:120] + ("…" if len(latest["prompt"]) > 120 else "")
        st.caption(f'"{prompt_preview}"')

        # Comparison
        if len(st.session_state.history) > 1:
            st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="sec">Before · After</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="cmp-tag">Iteration 1</div>', unsafe_allow_html=True)
                st.image(b64_to_pil(st.session_state.history[0]["image_b64"]), use_column_width=True)
            with c2:
                st.markdown(f'<div class="cmp-tag">Iteration {latest_idx}</div>', unsafe_allow_html=True)
                st.image(latest_img, use_column_width=True)

        # Previous iterations
        if len(st.session_state.history) > 1:
            st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="sec">All Iterations</div>', unsafe_allow_html=True)
            for i, entry in enumerate(reversed(st.session_state.history[:-1]), 2):
                actual_idx = len(st.session_state.history) - i + 1
                with st.expander(f"Iteration {actual_idx}  ·  {entry.get('timestamp', '')}"):
                    st.image(b64_to_pil(entry["image_b64"]), use_column_width=True)
                    st.download_button(
                        label=f"⬇  Download Iteration {actual_idx}",
                        data=b64_to_bytes(entry["image_b64"]),
                        file_name=f"image_studio_{actual_idx}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"dl_{actual_idx}",
                    )
                    st.caption(f'"{entry["prompt"][:120]}"')
