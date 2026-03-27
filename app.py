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
    "merah":  {"emoji": "🔴", "label": "MERAH",  "desc": "Berhenti & tarik napas",    "hex": "#FF4D4D", "glow": "rgba(255,77,77,0.45)"},
    "kuning": {"emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu", "hex": "#F5C400", "glow": "rgba(245,196,0,0.45)"},
    "hijau":  {"emoji": "🟢", "label": "HIJAU",  "desc": "Bertindak dengan bijak",    "hex": "#22C55E", "glow": "rgba(34,197,94,0.45)"},
}

TIMER = 3

st.set_page_config(page_title="Lampu Kendali", page_icon="🚦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

*, html, body { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: #08080F !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #E2E2EE;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }

.block-container {
    padding: 1.5rem 1.25rem 5rem !important;
    max-width: 430px !important;
    margin: 0 auto;
}

.syne { font-family: 'Syne', sans-serif !important; }

/* ── All streamlit buttons: base style ── */
.stButton { width: 100% !important; }
.stButton > button {
    width: 100% !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.8rem 1rem !important;
    border: none !important;
    cursor: pointer !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
    filter: brightness(0.9) !important;
}

/* Primary (CTA) buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C6FFF 0%, #B06EFF 100%) !important;
    box-shadow: 0 6px 20px rgba(124,111,255,0.4) !important;
    color: white !important;
}

/* Lampu buttons - using CSS class wrappers */
.btn-merah .stButton > button {
    background: #FF4D4D !important;
    box-shadow: 0 6px 22px rgba(255,77,77,0.45) !important;
    color: white !important;
}
.btn-kuning .stButton > button {
    background: #F5C400 !important;
    box-shadow: 0 6px 22px rgba(245,196,0,0.45) !important;
    color: #1a1200 !important;
}
.btn-hijau .stButton > button {
    background: #22C55E !important;
    box-shadow: 0 6px 22px rgba(34,197,94,0.45) !important;
    color: white !important;
}
.btn-merah .stButton > button:hover  { box-shadow: 0 10px 30px rgba(255,77,77,0.65) !important; }
.btn-kuning .stButton > button:hover { box-shadow: 0 10px 30px rgba(245,196,0,0.65) !important; }
.btn-hijau .stButton > button:hover  { box-shadow: 0 10px 30px rgba(34,197,94,0.65) !important; }

/* ── Misc ── */
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #7777AA;
    text-transform: uppercase;
}
.situasi-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 1.1rem 1rem;
    margin: 0.6rem 0 1rem;
    font-size: 1rem;
    font-weight: 500;
    line-height: 1.55;
    color: #D8D8EE;
    text-align: center;
}
.timer-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
    margin: 0.4rem 0 1rem;
}
.result-card {
    border-radius: 20px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 0.75rem 0 1rem;
}
.rekap-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 0.65rem 0.9rem;
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.055);
    margin-bottom: 7px;
}
.legend-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.65rem 1rem;
    border-radius: 14px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── session state ──
for k, v in [("phase", "intro"), ("idx", 0), ("timer_start", 0.0), ("pilihan", {})]:
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


# ══════════════════════════════════
# INTRO
# ══════════════════════════════════
if st.session_state.phase == "intro":
    st.markdown("""
    <div style='text-align:center;padding:1.75rem 0 1.25rem;'>
        <div style='font-size:3rem;margin-bottom:0.4rem;'>🚦</div>
        <div class='syne' style='font-size:1.85rem;font-weight:800;
            background:linear-gradient(130deg,#ffffff 35%,#A78BFA 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            margin-bottom:0.3rem;'>Lampu Kendali</div>
        <div style='color:#55557A;font-size:0.82rem;'>Latihan pengendalian diri — 7 situasi</div>
    </div>
    """, unsafe_allow_html=True)

    for w, info in WARNA.items():
        st.markdown(f"""
        <div class='legend-row' style='background:{info["hex"]}1A;border:1px solid {info["hex"]}33;'>
            <span style='font-size:1.4rem;'>{info['emoji']}</span>
            <div>
                <div class='syne' style='font-size:0.85rem;font-weight:800;color:{info["hex"]};
                    letter-spacing:0.06em;'>{info['label']}</div>
                <div style='font-size:0.76rem;color:#7777AA;margin-top:1px;'>{info['desc']}</div>
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
    pct = sisa / TIMER

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.5rem;'>
        <span class='badge'>Situasi {idx+1} dari {len(SITUASI)}</span>
    </div>
    <div class='situasi-box'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if sisa > 0.15:
        color = "#FF4D4D" if pct < 0.4 else "#F5C400" if pct < 0.7 else "#22C55E"
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:0.3rem;'>
            <span class='syne' style='font-size:2.6rem;font-weight:800;color:{color};'>{sisa:.1f}</span>
            <span style='color:#44446A;font-size:0.8rem;'> dtk</span>
        </div>
        <div class='timer-bar-bg'>
            <div style='background:{color};width:{pct*100:.1f}%;height:100%;
            border-radius:999px;box-shadow:0 0 8px {color};'></div>
        </div>
        <div style='text-align:center;color:#55557A;font-size:0.78rem;margin-bottom:0.6rem;'>
            Pilih lampu yang tepat ↓
        </div>
        """, unsafe_allow_html=True)

        for warna, info in WARNA.items():
            st.markdown(f"<div class='btn-{warna}'>", unsafe_allow_html=True)
            if st.button(
                f"{info['emoji']}  {info['label']}  —  {info['desc']}",
                key=f"w_{warna}_{idx}",
                use_container_width=True
            ):
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
    <div style='color:#44446A;font-size:0.8rem;text-align:center;
    font-style:italic;margin-bottom:0.75rem;'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA:
        info = WARNA[pilihan]
        txt = "#1a1200" if pilihan == "kuning" else "white"
        st.markdown(f"""
        <div class='result-card' style='background:{info["hex"]};box-shadow:0 10px 36px {info["glow"]};'>
            <div style='font-size:2.5rem;margin-bottom:6px;'>{info['emoji']}</div>
            <div class='syne' style='font-size:1.35rem;font-weight:800;color:{txt};
                letter-spacing:0.05em;'>{info['label']}</div>
            <div style='color:{txt};opacity:0.82;font-size:0.8rem;margin-top:4px;'>{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='result-card' style='background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.09);'>
            <div style='font-size:2.2rem;margin-bottom:6px;'>⏰</div>
            <div class='syne' style='font-size:1.1rem;font-weight:800;color:#55557A;'>Waktu habis!</div>
            <div style='color:#33334A;font-size:0.78rem;margin-top:3px;'>Tidak sempat memilih</div>
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
    st.markdown("""
    <div style='text-align:center;padding:1.25rem 0 0.75rem;'>
        <div style='font-size:2.2rem;'>🎉</div>
        <div class='syne' style='font-size:1.5rem;font-weight:800;margin:0.3rem 0;'>Kamu keren!</div>
        <div style='color:#55557A;font-size:0.8rem;'>Rekap pilihan kamu</div>
    </div>
    <div style='border-top:1px solid rgba(255,255,255,0.07);margin:0.75rem 0;'></div>
    """, unsafe_allow_html=True)

    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA:
            info = WARNA[pilihan]
            dot = f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:{info['hex']};box-shadow:0 0 5px {info['glow']};flex-shrink:0;margin-top:3px;'></span>"
            warna_html = f"<span class='syne' style='color:{info['hex']};font-size:0.75rem;font-weight:800;letter-spacing:0.05em;'>{info['label']}</span>"
        else:
            dot = "<span style='display:inline-block;width:9px;height:9px;border-radius:50%;background:#22223A;flex-shrink:0;margin-top:3px;'></span>"
            warna_html = "<span style='color:#33334A;font-size:0.75rem;'>Tidak menjawab</span>"

        st.markdown(f"""
        <div class='rekap-row'>
            {dot}
            <div style='flex:1;min-width:0;'>
                <div style='font-size:0.78rem;color:#6666AA;line-height:1.4;margin-bottom:3px;'>{situasi}</div>
                {warna_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    if st.button("🔁  Mulai Ulang", key="restart", type="primary", use_container_width=True):
        for k in ["phase", "idx", "timer_start", "pilihan"]:
            del st.session_state[k]
        st.rerun()
