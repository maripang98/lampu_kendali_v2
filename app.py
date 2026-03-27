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

WARNA = {
    "merah":  {"emoji": "🔴", "label": "MERAH",  "desc": "Berhenti & tarik napas",    "hex": "#C0504A", "glow": "rgba(192,80,74,0.4)",   "txt": "#FBF6F6"},
    "kuning": {"emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu", "hex": "#D4A85A", "glow": "rgba(212,168,90,0.4)",  "txt": "#2C2010"},
    "hijau":  {"emoji": "🟢", "label": "HIJAU",  "desc": "Bertindak dengan bijak",    "hex": "#6A7E3F", "glow": "rgba(106,126,63,0.4)",  "txt": "#F0F4E8"},
}

TIMER = 3
BG      = "#FBF6F6"
SURFACE = "#F2EBE4"
CARD    = "#EDE4DB"
BORDER  = "#D9CFC6"
INK     = "#2C2218"
MUTED   = "#9A8878"
ACCENT  = "#D96868"

st.set_page_config(page_title="Lampu Kendali", page_icon="🚦", layout="centered")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

*, html, body {{ box-sizing: border-box; }}

html, body, [class*="css"], .stApp {{
    background-color: {BG} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: {INK};
}}

#MainMenu, footer, header, [data-testid="stToolbar"] {{ visibility: hidden !important; }}

.block-container {{
    padding: 1.5rem 1.25rem 5rem !important;
    max-width: 420px !important;
    margin: 0 auto;
}}

.syne {{ font-family: 'Syne', sans-serif !important; }}

/* ── Buttons ── */
.stButton {{ width: 100% !important; }}
.stButton > button {{
    width: 100% !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.8rem 1rem !important;
    border: none !important;
    cursor: pointer !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    filter: brightness(1.06) !important;
}}
.stButton > button:active {{
    transform: scale(0.97) !important;
    filter: brightness(0.92) !important;
}}
.stButton > button[kind="primary"] {{
    background: {ACCENT} !important;
    color: #FBF6F6 !important;
    box-shadow: 0 5px 18px rgba(217,104,104,0.35) !important;
}}

/* Lampu buttons */
.btn-merah .stButton > button  {{ background: #D96868 !important; color: #FBF6F6 !important; box-shadow: 0 5px 18px rgba(217,104,104,0.38) !important; }}
.btn-kuning .stButton > button {{ background: #C8954A !important; color: #2C2010 !important; box-shadow: 0 5px 18px rgba(200,149,74,0.38) !important; }}
.btn-hijau .stButton > button  {{ background: #6A7E3F !important; color: #F0F4E8 !important; box-shadow: 0 5px 18px rgba(106,126,63,0.38) !important; }}
.btn-merah .stButton > button:hover  {{ box-shadow: 0 8px 26px rgba(217,104,104,0.55) !important; }}
.btn-kuning .stButton > button:hover {{ box-shadow: 0 8px 26px rgba(200,149,74,0.55) !important; }}
.btn-hijau .stButton > button:hover  {{ box-shadow: 0 8px 26px rgba(106,126,63,0.55) !important; }}

/* ── UI Elements ── */
.badge {{
    display: inline-block;
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: {MUTED};
    text-transform: uppercase;
}}
.situasi-box {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 1.1rem 1rem;
    margin: 0.6rem 0 1.25rem;
    font-size: 0.98rem;
    font-weight: 600;
    line-height: 1.55;
    color: {INK};
    text-align: center;
}}
.legend-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.65rem 1rem;
    border-radius: 14px;
    margin-bottom: 8px;
}}
.result-card {{
    border-radius: 20px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 0.75rem 0 1rem;
}}
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
</style>
""", unsafe_allow_html=True)

# ── session state ──
for k, v in [("phase","intro"),("idx",0),("timer_start",0.0),("pilihan",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

def mulai_situasi():
    st.session_state.phase = "countdown"
    st.session_state.timer_start = time.time()

def pilih_warna(w):
    st.session_state.pilihan[st.session_state.idx] = w
    st.session_state.phase = "hasil"

def situasi_berikutnya():
    st.session_state.idx += 1
    if st.session_state.idx >= len(SITUASI):
        st.session_state.phase = "selesai"
    else:
        mulai_situasi()

def circle_timer(sisa, total):
    pct = sisa / total
    r = 42
    circ = 2 * 3.14159 * r
    dash = circ * pct
    gap  = circ - dash
    # color shifts from olive-green → amber → rose as time runs out
    if pct > 0.6:
        stroke = "#6A7E3F"
    elif pct > 0.3:
        stroke = "#C8954A"
    else:
        stroke = "#D96868"
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;margin:0.5rem 0 1.1rem;">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r="{r}" fill="none" stroke="{BORDER}" stroke-width="7"/>
        <circle cx="55" cy="55" r="{r}" fill="none"
          stroke="{stroke}" stroke-width="7"
          stroke-linecap="round"
          stroke-dasharray="{dash:.2f} {gap:.2f}"
          transform="rotate(-90 55 55)"
          style="transition: stroke-dasharray 0.1s linear, stroke 0.3s ease;"/>
        <text x="55" y="59" text-anchor="middle"
          font-family="Syne, sans-serif" font-weight="800" font-size="22"
          fill="{stroke}">{sisa:.1f}</text>
        <text x="55" y="72" text-anchor="middle"
          font-family="Plus Jakarta Sans, sans-serif" font-size="9"
          fill="{MUTED}">detik</text>
      </svg>
    </div>
    """


# ══════════════════════════════════
# INTRO
# ══════════════════════════════════
if st.session_state.phase == "intro":
    st.markdown(f"""
    <div style='text-align:center;padding:2rem 0 1.5rem;'>
        <div style='font-size:2.8rem;margin-bottom:0.5rem;'>🚦</div>
        <div class='syne' style='font-size:1.8rem;font-weight:800;color:{INK};margin-bottom:0.25rem;'>
            Lampu Kendali
        </div>
        <div style='color:{MUTED};font-size:0.8rem;letter-spacing:0.04em;'>
            LATIHAN PENGENDALIAN DIRI · 7 SITUASI
        </div>
    </div>
    """, unsafe_allow_html=True)

    configs = [
        ("#D96868", "rgba(217,104,104,0.12)", "rgba(217,104,104,0.25)", "#FBF6F6", "merah"),
        ("#C8954A", "rgba(200,149,74,0.12)",  "rgba(200,149,74,0.25)",  "#2C2010",  "kuning"),
        ("#6A7E3F", "rgba(106,126,63,0.12)",  "rgba(106,126,63,0.25)",  "#F0F4E8",  "hijau"),
    ]
    for (color, bg, border_c, txt, key) in configs:
        info = WARNA[key]
        st.markdown(f"""
        <div class='legend-row' style='background:{bg};border:1px solid {border_c};'>
            <span style='font-size:1.3rem;'>{info['emoji']}</span>
            <div>
                <div class='syne' style='font-size:0.83rem;font-weight:800;color:{color};letter-spacing:0.06em;'>{info['label']}</div>
                <div style='font-size:0.75rem;color:{MUTED};margin-top:1px;'>{info['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("▶  Mulai Game", key="start", type="primary", use_container_width=True):
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
    <div style='text-align:center;margin-bottom:0.5rem;'>
        <span class='badge'>Situasi {idx+1} dari {len(SITUASI)}</span>
    </div>
    <div class='situasi-box'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if sisa > 0.15:
        st.markdown(circle_timer(sisa, TIMER), unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:{MUTED};font-size:0.78rem;margin-bottom:0.75rem;letter-spacing:0.03em;'>Pilih lampu yang tepat ↓</div>", unsafe_allow_html=True)

        for warna, info in WARNA.items():
            st.markdown(f"<div class='btn-{warna}'>", unsafe_allow_html=True)
            if st.button(f"{info['emoji']}  {info['label']}  —  {info['desc']}", key=f"w_{warna}_{idx}", use_container_width=True):
                pilih_warna(warna)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

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
    <div style='color:{MUTED};font-size:0.8rem;text-align:center;font-style:italic;margin-bottom:0.9rem;'>
        "{SITUASI[idx]}"
    </div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA:
        info = WARNA[pilihan]
        btn_colors = {"merah": "#D96868", "kuning": "#C8954A", "hijau": "#6A7E3F"}
        bg = btn_colors[pilihan]
        st.markdown(f"""
        <div class='result-card' style='background:{bg};box-shadow:0 10px 32px {info["glow"]};'>
            <div style='font-size:2.4rem;margin-bottom:6px;'>{info['emoji']}</div>
            <div class='syne' style='font-size:1.3rem;font-weight:800;color:{info["txt"]};letter-spacing:0.05em;'>
                {info['label']}
            </div>
            <div style='color:{info["txt"]};opacity:0.78;font-size:0.78rem;margin-top:5px;'>{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='result-card' style='background:{SURFACE};border:1px solid {BORDER};'>
            <div style='font-size:2rem;margin-bottom:6px;'>⏰</div>
            <div class='syne' style='font-size:1.1rem;font-weight:800;color:{MUTED};'>Waktu habis!</div>
            <div style='color:{BORDER};font-size:0.75rem;margin-top:3px;'>Tidak sempat memilih</div>
        </div>
        """, unsafe_allow_html=True)

    lbl = "Situasi Berikutnya  →" if idx < len(SITUASI) - 1 else "Lihat Hasil Akhir  🏁"
    if st.button(lbl, key="next", type="primary", use_container_width=True):
        situasi_berikutnya()
        st.rerun()


# ══════════════════════════════════
# SELESAI
# ══════════════════════════════════
elif st.session_state.phase == "selesai":
    st.balloons()
    st.markdown(f"""
    <div style='text-align:center;padding:1.5rem 0 0.75rem;'>
        <div style='font-size:2.2rem;'>🎉</div>
        <div class='syne' style='font-size:1.5rem;font-weight:800;color:{INK};margin:0.3rem 0;'>Kamu keren!</div>
        <div style='color:{MUTED};font-size:0.78rem;'>Rekap pilihan kamu</div>
    </div>
    <div style='border-top:1px solid {BORDER};margin:0.75rem 0;'></div>
    """, unsafe_allow_html=True)

    btn_colors = {"merah": "#D96868", "kuning": "#C8954A", "hijau": "#6A7E3F"}

    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA:
            info = WARNA[pilihan]
            bg = btn_colors[pilihan]
            dot = f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{bg};flex-shrink:0;margin-top:3px;'></span>"
            warna_html = f"<span class='syne' style='color:{bg};font-size:0.73rem;font-weight:800;letter-spacing:0.05em;'>{info['label']}</span>"
        else:
            dot = f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{BORDER};flex-shrink:0;margin-top:3px;'></span>"
            warna_html = f"<span style='color:{MUTED};font-size:0.73rem;'>Tidak menjawab</span>"

        st.markdown(f"""
        <div class='rekap-row'>
            {dot}
            <div style='flex:1;min-width:0;'>
                <div style='font-size:0.78rem;color:{MUTED};line-height:1.4;margin-bottom:3px;'>{situasi}</div>
                {warna_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("🔁  Mulai Ulang", key="restart", type="primary", use_container_width=True):
        for k in ["phase", "idx", "timer_start", "pilihan"]:
            del st.session_state[k]
        st.rerun()
