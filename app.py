import streamlit as st
import time

# ══════════════════════════════════
# DATA
# ══════════════════════════════════
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
    "merah":  {
        "emoji": "🔴", "label": "MERAH",  "desc": "Berhenti & tarik napas",
        "bg": "#C0392B", "bg_light": "#F9EBEA", "txt": "#FDFEFE",
        "glow": "rgba(192,57,43,0.35)", "border": "rgba(192,57,43,0.30)",
    },
    "kuning": {
        "emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu",
        "bg": "#D4861A", "bg_light": "#FEF9E7", "txt": "#1A0A00",
        "glow": "rgba(212,134,26,0.35)", "border": "rgba(212,134,26,0.30)",
    },
    "hijau":  {
        "emoji": "🟢", "label": "HIJAU",  "desc": "Bertindak dengan bijak",
        "bg": "#1E8449", "bg_light": "#EAFAF1", "txt": "#F0FFF6",
        "glow": "rgba(30,132,73,0.35)", "border": "rgba(30,132,73,0.30)",
    },
}

TIMER = 5   # detik per situasi

# ══════════════════════════════════
# PALETTE
# ══════════════════════════════════
BG       = "#F7F3EF"
SURFACE  = "#EDE7E0"
CARD     = "#E3D9CF"
BORDER   = "#CEC0B2"
INK      = "#1E1410"
MUTED    = "#8C7B6E"
ACCENT   = "#C0392B"

# ══════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════
st.set_page_config(
    page_title="Lampu Kendali",
    page_icon="🚦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════
defaults = {
    "phase": "intro",
    "idx": 0,
    "timer_start": 0.0,
    "pilihan": {},
    "pending_warna": None,  # simpan pilihan warna sebelum pindah phase
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════
# HELPERS
# ══════════════════════════════════
def mulai_situasi():
    st.session_state.phase = "countdown"
    st.session_state.timer_start = time.time()
    st.session_state.pending_warna = None

def pilih_warna(w):
    """Callback saat tombol warna ditekan."""
    st.session_state.pending_warna = w

def proses_pilihan():
    """Dipanggil di awal loop countdown untuk memproses pilihan yang masuk."""
    if st.session_state.pending_warna is not None:
        st.session_state.pilihan[st.session_state.idx] = st.session_state.pending_warna
        st.session_state.pending_warna = None
        st.session_state.phase = "hasil"

def situasi_berikutnya():
    st.session_state.idx += 1
    if st.session_state.idx >= len(SITUASI):
        st.session_state.phase = "selesai"
    else:
        mulai_situasi()

def reset_game():
    for k in list(defaults.keys()):
        st.session_state[k] = defaults[k]
    # reset pilihan juga
    st.session_state.pilihan = {}

# ══════════════════════════════════
# CIRCLE TIMER SVG
# ══════════════════════════════════
def circle_timer_svg(sisa: float, total: float) -> str:
    pct = max(0.0, sisa / total)
    r = 38
    circ = 2 * 3.14159265 * r
    dash = circ * pct
    gap  = circ - dash + 0.001   # avoid zero gap glitch

    if pct > 0.65:
        stroke = "#1E8449"
    elif pct > 0.32:
        stroke = "#D4861A"
    else:
        stroke = "#C0392B"

    sisa_text = f"{sisa:.0f}"
    return f"""
<div style="display:flex;justify-content:center;margin:0.5rem 0 0.9rem;">
  <svg width="88" height="88" viewBox="0 0 88 88" xmlns="http://www.w3.org/2000/svg">
    <circle cx="44" cy="44" r="{r}" fill="none" stroke="{BORDER}" stroke-width="5.5"/>
    <circle cx="44" cy="44" r="{r}" fill="none"
      stroke="{stroke}" stroke-width="5.5" stroke-linecap="round"
      stroke-dasharray="{dash:.4f} {gap:.4f}"
      transform="rotate(-90 44 44)"/>
    <text x="44" y="49" text-anchor="middle"
      font-family="'DM Serif Display',serif" font-weight="700"
      font-size="22" fill="{stroke}">{sisa_text}</text>
    <text x="44" y="61" text-anchor="middle"
      font-family="'DM Sans',sans-serif" font-size="8"
      fill="{MUTED}" letter-spacing="1.5">DTK</text>
  </svg>
</div>"""

# ══════════════════════════════════
# PROGRESS BAR HTML
# ══════════════════════════════════
def progress_html(idx: int, total: int) -> str:
    dots = ""
    for i in range(total):
        p = st.session_state.pilihan.get(i)
        if p and p in WARNA_CFG:
            col = WARNA_CFG[p]["bg"]
            dots += f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{col};margin:0 2.5px;'></span>"
        elif i < idx:
            dots += f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{BORDER};margin:0 2.5px;'></span>"
        elif i == idx:
            dots += f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{ACCENT};margin:0 2.5px;box-shadow:0 0 0 2.5px {ACCENT}44;'></span>"
        else:
            dots += f"<span style='display:inline-block;width:9px;height:9px;border-radius:2.5px;background:{BORDER};opacity:0.4;margin:0 2.5px;'></span>"
    return f"<div style='text-align:center;margin-bottom:0.7rem;'>{dots}</div>"

# ══════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;600;700&display=swap');

*, html, body {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"], .stApp {{
    background-color: {BG} !important;
    font-family: 'DM Sans', sans-serif !important;
    color: {INK} !important;
}}

/* Sembunyikan elemen Streamlit default */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"] {{
    display: none !important;
    visibility: hidden !important;
}}

.block-container {{
    padding: 1.5rem 1.2rem 5rem !important;
    max-width: 420px !important;
    margin: 0 auto !important;
}}

/* Typografi */
.serif  {{ font-family: 'DM Serif Display', serif !important; }}
.badge  {{
    display: inline-block;
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    color: {MUTED};
    text-transform: uppercase;
}}

/* Kartu situasi */
.situasi-box {{
    background: {SURFACE};
    border: 1.5px solid {BORDER};
    border-radius: 18px;
    padding: 1.1rem 1.2rem;
    margin: 0.55rem 0 0.8rem;
    font-size: 1.02rem;
    font-weight: 500;
    line-height: 1.6;
    color: {INK};
    text-align: center;
    font-style: italic;
}}

/* Tombol CTA Streamlit */
div[data-testid="stButton"] > button {{
    width: 100% !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.80rem 1rem !important;
    border: none !important;
    cursor: pointer !important;
    background: {ACCENT} !important;
    color: #FEFEFE !important;
    box-shadow: 0 4px 16px rgba(192,57,43,0.28) !important;
    transition: box-shadow 0.15s, transform 0.12s !important;
    margin-top: 0.3rem !important;
}}
div[data-testid="stButton"] > button:hover {{
    box-shadow: 0 7px 22px rgba(192,57,43,0.42) !important;
    transform: translateY(-1px) !important;
    color: #FEFEFE !important;
    background: {ACCENT} !important;
}}
div[data-testid="stButton"] > button:active {{
    transform: translateY(0px) !important;
    box-shadow: 0 2px 8px rgba(192,57,43,0.22) !important;
    filter: brightness(0.94) !important;
}}
div[data-testid="stButton"] > button:focus,
div[data-testid="stButton"] > button:focus-visible {{
    outline: 2px solid {ACCENT}88 !important;
    outline-offset: 2px !important;
    box-shadow: 0 4px 16px rgba(192,57,43,0.28) !important;
}}

/* Tombol warna lampu — override ke masing-masing warna */
div[data-testid="stButton"].btn-merah  > button {{ background: #C0392B !important; box-shadow: 0 4px 14px rgba(192,57,43,0.35) !important; }}
div[data-testid="stButton"].btn-kuning > button {{ background: #D4861A !important; color: #1A0A00 !important; box-shadow: 0 4px 14px rgba(212,134,26,0.35) !important; }}
div[data-testid="stButton"].btn-hijau  > button {{ background: #1E8449 !important; box-shadow: 0 4px 14px rgba(30,132,73,0.35) !important; }}

/* Kartu hasil */
.result-card {{
    border-radius: 20px;
    padding: 1.6rem 1.1rem;
    text-align: center;
    margin: 0.6rem 0 1rem;
}}

/* Rekap baris */
.rekap-row {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 0.65rem 0.9rem;
    border-radius: 14px;
    background: {SURFACE};
    border: 1px solid {BORDER};
    margin-bottom: 7px;
}}

/* Legend row di intro */
.legend-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.7rem 1rem;
    border-radius: 14px;
    margin-bottom: 8px;
}}

/* Divider */
.divider {{
    border: none;
    border-top: 1.5px solid {BORDER};
    margin: 0.8rem 0;
}}

/* Timeout badge */
.timeout-card {{
    background: {SURFACE};
    border: 1.5px dashed {BORDER};
    border-radius: 18px;
    padding: 1.4rem;
    text-align: center;
    margin: 0.6rem 0 1rem;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════
# PHASE: INTRO
# ══════════════════════════════════
if st.session_state.phase == "intro":
    st.markdown(f"""
    <div style='text-align:center;padding:2.2rem 0 1.5rem;'>
        <div style='font-size:3rem;margin-bottom:0.55rem;letter-spacing:-2px;'>🚦</div>
        <div class='serif' style='font-size:2rem;color:{INK};margin-bottom:0.18rem;'>
            Lampu Kendali
        </div>
        <div style='color:{MUTED};font-size:0.72rem;letter-spacing:0.10em;font-weight:600;'>
            LATIHAN PENGENDALIAN DIRI &nbsp;·&nbsp; {len(SITUASI)} SITUASI
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='color:{MUTED};font-size:0.82rem;text-align:center;margin-bottom:1rem;'>Kamu punya <strong style='color:{INK}'>{TIMER} detik</strong> untuk memilih respons yang tepat di setiap situasi.</p>", unsafe_allow_html=True)

    for w, cfg in WARNA_CFG.items():
        st.markdown(f"""
        <div class='legend-row' style='background:{cfg["bg_light"]};border:1.5px solid {cfg["border"]};'>
            <span style='font-size:1.4rem;'>{cfg['emoji']}</span>
            <div>
                <div class='serif' style='font-size:0.88rem;color:{cfg["bg"]};letter-spacing:0.03em;'>{cfg['label']}</div>
                <div style='font-size:0.74rem;color:{MUTED};margin-top:1px;'>{cfg['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("Mulai Game  ▶", key="btn_start"):
        mulai_situasi()
        st.rerun()


# ══════════════════════════════════
# PHASE: COUNTDOWN
# ══════════════════════════════════
elif st.session_state.phase == "countdown":
    # Proses pilihan yang masuk dari tombol
    proses_pilihan()
    if st.session_state.phase == "hasil":
        st.rerun()

    idx = st.session_state.idx
    elapsed = time.time() - st.session_state.timer_start
    sisa = max(0.0, TIMER - elapsed)

    # Header + progress
    st.markdown(progress_html(idx, len(SITUASI)), unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.4rem;'>
        <span class='badge'>Situasi {idx + 1} dari {len(SITUASI)}</span>
    </div>
    <div class='situasi-box'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if sisa > 0.05:
        # Timer SVG
        st.markdown(circle_timer_svg(sisa, TIMER), unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center;color:{MUTED};font-size:0.74rem;"
            f"margin-bottom:0.7rem;letter-spacing:0.02em;font-weight:500;'>"
            f"Pilih lampu yang paling tepat untukmu</div>",
            unsafe_allow_html=True
        )

        # Tombol warna — pakai st.button dengan callback (reliable, tidak ada query param)
        for w, cfg in WARNA_CFG.items():
            col_label = f"{cfg['emoji']}  {cfg['label']}  —  {cfg['desc']}"
            if st.button(col_label, key=f"btn_{w}_{idx}", on_click=pilih_warna, args=(w,)):
                pass  # on_click sudah handle

        # Auto-refresh tiap 0.25 detik untuk update timer
        time.sleep(0.25)
        st.rerun()
    else:
        # Waktu habis
        if idx not in st.session_state.pilihan:
            st.session_state.pilihan[idx] = None
        st.session_state.phase = "hasil"
        st.rerun()


# ══════════════════════════════════
# PHASE: HASIL
# ══════════════════════════════════
elif st.session_state.phase == "hasil":
    idx = st.session_state.idx
    pilihan = st.session_state.pilihan.get(idx)

    st.markdown(progress_html(idx, len(SITUASI)), unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.4rem;'>
        <span class='badge'>Situasi {idx + 1} dari {len(SITUASI)}</span>
    </div>
    <div style='color:{MUTED};font-size:0.83rem;text-align:center;font-style:italic;
        margin-bottom:0.9rem;line-height:1.55;padding:0 0.3rem;'>
        "{SITUASI[idx]}"
    </div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA_CFG:
        cfg = WARNA_CFG[pilihan]
        st.markdown(f"""
        <div class='result-card' style='background:{cfg["bg"]};box-shadow:0 10px 32px {cfg["glow"]};'>
            <div style='font-size:2.4rem;margin-bottom:8px;'>{cfg['emoji']}</div>
            <div class='serif' style='font-size:1.35rem;color:{cfg["txt"]};letter-spacing:0.03em;'>
                {cfg['label']}
            </div>
            <div style='color:{cfg["txt"]};opacity:0.78;font-size:0.77rem;margin-top:6px;font-weight:500;'>
                {cfg['desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='timeout-card'>
            <div style='font-size:2rem;margin-bottom:8px;'>⏰</div>
            <div class='serif' style='font-size:1.1rem;color:{MUTED};'>Waktu habis!</div>
            <div style='color:{MUTED};font-size:0.75rem;margin-top:5px;opacity:0.75;'>
                Tidak sempat memilih — coba lebih cepat
            </div>
        </div>
        """, unsafe_allow_html=True)

    lbl = "Situasi Berikutnya  →" if idx < len(SITUASI) - 1 else "Lihat Rekap Akhir  🏁"
    if st.button(lbl, key="btn_next"):
        situasi_berikutnya()
        st.rerun()


# ══════════════════════════════════
# PHASE: SELESAI
# ══════════════════════════════════
elif st.session_state.phase == "selesai":
    # Hitung statistik
    total = len(SITUASI)
    counts = {"merah": 0, "kuning": 0, "hijau": 0, "timeout": 0}
    for i in range(total):
        p = st.session_state.pilihan.get(i)
        if p in WARNA_CFG:
            counts[p] += 1
        else:
            counts["timeout"] += 1

    st.markdown(f"""
    <div style='text-align:center;padding:1.6rem 0 0.9rem;'>
        <div style='font-size:2.2rem;margin-bottom:0.35rem;'>🎉</div>
        <div class='serif' style='font-size:1.55rem;color:{INK};margin-bottom:0.15rem;'>
            Selesai!
        </div>
        <div style='color:{MUTED};font-size:0.74rem;font-weight:600;letter-spacing:0.06em;'>
            REKAP PILIHAN KAMU
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Statistik ringkas
    stat_html = "<div style='display:flex;gap:8px;margin-bottom:1rem;'>"
    for w in ["merah", "kuning", "hijau"]:
        cfg = WARNA_CFG[w]
        stat_html += f"""
        <div style='flex:1;text-align:center;background:{cfg["bg_light"]};
            border:1.5px solid {cfg["border"]};border-radius:14px;padding:0.65rem 0.4rem;'>
            <div style='font-size:1.1rem;'>{cfg['emoji']}</div>
            <div class='serif' style='font-size:1.35rem;color:{cfg["bg"]};'>{counts[w]}</div>
            <div style='font-size:0.62rem;color:{MUTED};font-weight:600;letter-spacing:0.06em;'>{cfg['label']}</div>
        </div>"""
    stat_html += "</div>"
    st.markdown(stat_html, unsafe_allow_html=True)

    # Rekap per situasi
    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA_CFG:
            cfg = WARNA_CFG[pilihan]
            dot = f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{cfg['bg']};flex-shrink:0;margin-top:4px;'></span>"
            label_html = f"<span class='serif' style='color:{cfg['bg']};font-size:0.75rem;letter-spacing:0.04em;'>{cfg['emoji']} {cfg['label']}</span>"
        else:
            dot = f"<span style='display:inline-block;width:9px;height:9px;border-radius:3px;border:1.5px dashed {MUTED};flex-shrink:0;margin-top:4px;'></span>"
            label_html = f"<span style='color:{MUTED};font-size:0.73rem;'>⏰ Tidak menjawab</span>"

        st.markdown(f"""
        <div class='rekap-row'>
            {dot}
            <div style='flex:1;min-width:0;'>
                <div style='font-size:0.78rem;color:{MUTED};line-height:1.5;margin-bottom:3px;'>
                    {situasi}
                </div>
                {label_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("🔁  Mulai Ulang", key="btn_restart"):
        reset_game()
        st.rerun()
