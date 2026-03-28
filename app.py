import streamlit as st
import time

SITUASI = [
    "Ada teman yang sengaja memancing kemarahanmu.",
    "Temanmu disindir orang lain dan sedang sedih.",
    "Ada gosip tentang dirimu menyebar.",
    "Kamu dapat pesan DM yang bikin kamu tersinggung.",
    "Ada teman yang butuh bantuan PR.",
    "Kamu kecewa karena rencana batal.",
    "Ada ajakan melakukan hal yang kamu tahu tidak benar.",
]

WARNA_CFG = {
    "merah":  {"emoji": "🔴", "label": "MERAH",  "desc": "Berhenti & tarik napas",    "bg": "#D96868", "txt": "#FBF6F6", "glow": "rgba(217,104,104,0.30)", "legend_bg": "rgba(217,104,104,0.10)", "legend_border": "rgba(217,104,104,0.22)"},
    "kuning": {"emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu", "bg": "#C8954A", "txt": "#2C1A00", "glow": "rgba(200,149,74,0.30)",  "legend_bg": "rgba(200,149,74,0.10)",  "legend_border": "rgba(200,149,74,0.22)"},
    "hijau":  {"emoji": "🟢", "label": "HIJAU",  "desc": "Bertindak dengan bijak",    "bg": "#5A7A35", "txt": "#F0F4E8", "glow": "rgba(90,122,53,0.30)",   "legend_bg": "rgba(90,122,53,0.10)",   "legend_border": "rgba(90,122,53,0.22)"},
}

TIMER   = 5
BG      = "#FBF6F2"
SURFACE = "#F0E8DF"
CARD    = "#E8DDD3"
BORDER  = "#D5C9BE"
INK     = "#2A1F14"
MUTED   = "#9A8676"
ACCENT  = "#D96868"

st.set_page_config(page_title="Lampu Kendali", page_icon="🚦", layout="centered")

# ── session state ──
for k, v in [("phase","intro"), ("idx",0), ("timer_start",0.0), ("pilihan",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

# Handle warna pilihan via query param
qp = st.query_params
if "pilih" in qp and st.session_state.phase == "countdown":
    w = qp["pilih"]
    if w in WARNA_CFG:
        st.session_state.pilihan[st.session_state.idx] = w
        st.session_state.phase = "hasil"
        st.query_params.clear()
        st.rerun()

def mulai_situasi():
    st.session_state.phase = "countdown"
    st.session_state.timer_start = time.time()

def situasi_berikutnya():
    st.session_state.idx += 1
    if st.session_state.idx >= len(SITUASI):
        st.session_state.phase = "selesai"
    else:
        mulai_situasi()

def circle_timer_svg(sisa, total):
    pct = sisa / total
    r = 40
    circ = 2 * 3.14159265 * r
    dash = circ * pct
    gap  = circ - dash
    if pct > 0.65:
        stroke = "#5A7A35"
    elif pct > 0.32:
        stroke = "#C8954A"
    else:
        stroke = "#D96868"
    return f"""
    <div style="display:flex;justify-content:center;margin:0.6rem 0 1rem;">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r="{r}" fill="none" stroke="{BORDER}" stroke-width="6"/>
        <circle cx="48" cy="48" r="{r}" fill="none"
          stroke="{stroke}" stroke-width="6" stroke-linecap="round"
          stroke-dasharray="{dash:.3f} {gap:.3f}"
          transform="rotate(-90 48 48)"/>
        <text x="48" y="52" text-anchor="middle"
          font-family="Syne,sans-serif" font-weight="800" font-size="20" fill="{stroke}">{sisa:.1f}</text>
        <text x="48" y="64" text-anchor="middle"
          font-family="sans-serif" font-size="8" fill="{MUTED}" letter-spacing="1">DTK</text>
      </svg>
    </div>"""

# ── Global CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

*, html, body {{ box-sizing: border-box; }}
html, body, [class*="css"], .stApp {{
    background-color: {BG} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {INK};
}}
#MainMenu, footer, header, [data-testid="stToolbar"] {{ visibility:hidden !important; }}
.block-container {{
    padding: 1.25rem 1.1rem 5rem !important;
    max-width: 400px !important;
    margin: 0 auto;
}}
.syne {{ font-family:'Syne',sans-serif !important; }}

/* ── Primary Streamlit buttons (CTA only) ── */
.stButton > button {{
    width: 100% !important;
    border-radius: 13px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.78rem 1rem !important;
    border: none !important;
    cursor: pointer !important;
    background: {ACCENT} !important;
    color: #FBF6F6 !important;
    box-shadow: 0 4px 14px rgba(217,104,104,0.30) !important;
    transition: box-shadow 0.15s ease !important;
}}
.stButton > button:hover {{
    box-shadow: 0 6px 20px rgba(217,104,104,0.45) !important;
    background: {ACCENT} !important;
    color: #FBF6F6 !important;
    filter: none !important;
    transform: none !important;
}}
.stButton > button:active {{
    box-shadow: 0 2px 8px rgba(217,104,104,0.25) !important;
    background: {ACCENT} !important;
    filter: brightness(0.95) !important;
    transform: none !important;
}}
.stButton > button:focus, .stButton > button:focus-visible {{
    outline: none !important;
    box-shadow: 0 0 0 2px {ACCENT}66 !important;
}}

/* ── Shared UI ── */
.badge {{
    display:inline-block;
    background:{CARD};border:1px solid {BORDER};
    border-radius:999px;padding:3px 13px;
    font-size:0.68rem;font-weight:700;letter-spacing:0.09em;
    color:{MUTED};text-transform:uppercase;
}}
.situasi-box {{
    background:{SURFACE};border:1px solid {BORDER};
    border-radius:16px;padding:1rem 1rem;
    margin:0.55rem 0 0.9rem;font-size:0.96rem;
    font-weight:600;line-height:1.55;color:{INK};text-align:center;
}}
.legend-row {{
    display:flex;align-items:center;gap:11px;
    padding:0.6rem 0.9rem;border-radius:13px;margin-bottom:7px;
}}
.result-card {{
    border-radius:18px;padding:1.4rem 1rem;
    text-align:center;margin:0.6rem 0 1rem;
}}
.rekap-row {{
    display:flex;align-items:flex-start;gap:10px;
    padding:0.6rem 0.85rem;border-radius:13px;
    background:{SURFACE};border:1px solid {BORDER};margin-bottom:6px;
}}

/* ── HTML lampu buttons (rendered via st.markdown) ── */
.lampu-btn {{
    display:block;width:100%;
    border-radius:13px;padding:0.78rem 1rem;
    font-family:'Syne',sans-serif;font-weight:800;
    font-size:0.87rem;letter-spacing:0.04em;
    border:none;cursor:pointer;
    text-align:left;margin-bottom:9px;
    text-decoration:none;
    transition: box-shadow 0.15s ease;
}}
.lampu-btn:active {{ filter:brightness(0.93); }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════
# INTRO
# ══════════════════════════════════
if st.session_state.phase == "intro":
    st.markdown(f"""
    <div style='text-align:center;padding:2rem 0 1.4rem;'>
        <div style='font-size:2.6rem;margin-bottom:0.45rem;'>🚦</div>
        <div class='syne' style='font-size:1.75rem;font-weight:800;color:{INK};margin-bottom:0.2rem;'>
            Lampu Kendali
        </div>
        <div style='color:{MUTED};font-size:0.76rem;letter-spacing:0.07em;'>
            LATIHAN PENGENDALIAN DIRI &nbsp;·&nbsp; 7 SITUASI
        </div>
    </div>
    """, unsafe_allow_html=True)

    for w, cfg in WARNA_CFG.items():
        st.markdown(f"""
        <div class='legend-row' style='background:{cfg["legend_bg"]};border:1px solid {cfg["legend_border"]};'>
            <span style='font-size:1.25rem;'>{cfg['emoji']}</span>
            <div>
                <div class='syne' style='font-size:0.82rem;font-weight:800;color:{cfg["bg"]};letter-spacing:0.06em;'>{cfg['label']}</div>
                <div style='font-size:0.73rem;color:{MUTED};margin-top:1px;'>{cfg['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("Mulai Game  ▶", key="start", use_container_width=True):
        mulai_situasi()
        st.rerun()


# ══════════════════════════════════
# COUNTDOWN + PILIH
# ══════════════════════════════════
elif st.session_state.phase == "countdown":
    idx = st.session_state.idx
    elapsed = time.time() - st.session_state.timer_start
    sisa = max(0.0, TIMER - elapsed)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.45rem;'>
        <span class='badge'>Situasi {idx+1} dari {len(SITUASI)}</span>
    </div>
    <div class='situasi-box'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if sisa > 0.1:
        st.markdown(circle_timer_svg(sisa, TIMER), unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:{MUTED};font-size:0.75rem;margin-bottom:0.65rem;letter-spacing:0.02em;'>Pilih lampu yang tepat</div>", unsafe_allow_html=True)

        # Render lampu buttons as plain HTML <a> tags — no Streamlit, no hover color change
        btn_html = ""
        for w, cfg in WARNA_CFG.items():
            btn_html += f"""
            <a href="?pilih={w}" target="_self" class="lampu-btn"
               style="background:{cfg['bg']};color:{cfg['txt']};box-shadow:0 4px 14px {cfg['glow']};">
               {cfg['emoji']}&nbsp;&nbsp;{cfg['label']}&ensp;<span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;font-size:0.78rem;opacity:0.82;">— {cfg['desc']}</span>
            </a>"""
        st.markdown(btn_html, unsafe_allow_html=True)

        time.sleep(0.1)
        st.rerun()
    else:
        if idx not in st.session_state.pilihan:
            st.session_state.pilihan[idx] = None
        st.session_state.phase = "hasil"
        st.rerun()


# ══════════════════════════════════
# HASIL
# ══════════════════════════════════
elif st.session_state.phase == "hasil":
    idx = st.session_state.idx
    pilihan = st.session_state.pilihan.get(idx)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.4rem;'>
        <span class='badge'>Situasi {idx+1} dari {len(SITUASI)}</span>
    </div>
    <div style='color:{MUTED};font-size:0.78rem;text-align:center;font-style:italic;margin-bottom:0.85rem;line-height:1.5;'>
        "{SITUASI[idx]}"
    </div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA_CFG:
        cfg = WARNA_CFG[pilihan]
        st.markdown(f"""
        <div class='result-card' style='background:{cfg["bg"]};box-shadow:0 8px 28px {cfg["glow"]};'>
            <div style='font-size:2.2rem;margin-bottom:7px;'>{cfg['emoji']}</div>
            <div class='syne' style='font-size:1.25rem;font-weight:800;color:{cfg["txt"]};letter-spacing:0.05em;'>{cfg['label']}</div>
            <div style='color:{cfg["txt"]};opacity:0.75;font-size:0.76rem;margin-top:5px;'>{cfg['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='result-card' style='background:{SURFACE};border:1px solid {BORDER};'>
            <div style='font-size:1.8rem;margin-bottom:7px;'>⏰</div>
            <div class='syne' style='font-size:1.05rem;font-weight:800;color:{MUTED};'>Waktu habis!</div>
            <div style='color:{MUTED};font-size:0.73rem;margin-top:4px;opacity:0.7;'>Tidak sempat memilih</div>
        </div>
        """, unsafe_allow_html=True)

    lbl = "Situasi Berikutnya  →" if idx < len(SITUASI) - 1 else "Lihat Rekap Akhir  →"
    if st.button(lbl, key="next", use_container_width=True):
        situasi_berikutnya()
        st.rerun()


# ══════════════════════════════════
# SELESAI
# ══════════════════════════════════
elif st.session_state.phase == "selesai":
    st.markdown(f"""
    <div style='text-align:center;padding:1.5rem 0 0.75rem;'>
        <div style='font-size:2rem;margin-bottom:0.3rem;'>🎉</div>
        <div class='syne' style='font-size:1.45rem;font-weight:800;color:{INK};margin-bottom:0.2rem;'>Selesai!</div>
        <div style='color:{MUTED};font-size:0.76rem;'>Rekap pilihan kamu</div>
    </div>
    <div style='border-top:1px solid {BORDER};margin:0.7rem 0 0.85rem;'></div>
    """, unsafe_allow_html=True)

    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA_CFG:
            cfg = WARNA_CFG[pilihan]
            dot = f"<span style='display:inline-block;width:8px;height:8px;border-radius:50%;background:{cfg['bg']};flex-shrink:0;margin-top:4px;'></span>"
            label_html = f"<span class='syne' style='color:{cfg['bg']};font-size:0.72rem;font-weight:800;letter-spacing:0.05em;'>{cfg['label']}</span>"
        else:
            dot = f"<span style='display:inline-block;width:8px;height:8px;border-radius:50%;background:{BORDER};flex-shrink:0;margin-top:4px;'></span>"
            label_html = f"<span style='color:{MUTED};font-size:0.72rem;'>Tidak menjawab</span>"

        st.markdown(f"""
        <div class='rekap-row'>
            {dot}
            <div style='flex:1;min-width:0;'>
                <div style='font-size:0.77rem;color:{MUTED};line-height:1.45;margin-bottom:3px;'>{situasi}</div>
                {label_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("🔁  Mulai Ulang", key="restart", use_container_width=True):
        for k in ["phase", "idx", "timer_start", "pilihan"]:
            del st.session_state[k]
        st.query_params.clear()
        st.rerun()
