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
    "merah":  {"emoji": "🔴", "label": "MERAH",  "desc": "Berhenti & tarik napas",    "hex": "#FF4D4D", "glow": "rgba(255,77,77,0.5)"},
    "kuning": {"emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu", "hex": "#FFD600", "glow": "rgba(255,214,0,0.5)"},
    "hijau":  {"emoji": "🟢", "label": "HIJAU",  "desc": "Bertindak dengan bijak",    "hex": "#2ECC71", "glow": "rgba(46,204,113,0.5)"},
}

TIMER = 3

st.set_page_config(page_title="Lampu Kendali", page_icon="🚦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

*, html, body { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: #0A0A12 !important;
    font-family: 'DM Sans', sans-serif;
    color: #E8E8F0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 480px !important; margin: auto; }

/* Hide default streamlit buttons */
.stButton > button {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    width: 100% !important;
    box-shadow: none !important;
    color: transparent !important;
    font-size: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    position: absolute !important;
    opacity: 0 !important;
    cursor: pointer !important;
}

/* Noise overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.5;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

/* Card container */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2rem 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(12px);
}

/* Lampu button styling */
.lampu-wrap {
    position: relative;
    margin-bottom: 16px;
    cursor: pointer;
}

.lampu-btn {
    width: 100%;
    border-radius: 20px;
    padding: 1.4rem 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    position: relative;
    overflow: hidden;
}

.lampu-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 60%);
    pointer-events: none;
}

.lampu-merah  { background: #FF4D4D; box-shadow: 0 8px 32px rgba(255,77,77,0.4); }
.lampu-kuning { background: #FFD600; box-shadow: 0 8px 32px rgba(255,214,0,0.4); }
.lampu-hijau  { background: #2ECC71; box-shadow: 0 8px 32px rgba(46,204,113,0.4); }

.lampu-merah:hover  { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(255,77,77,0.6); }
.lampu-kuning:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(255,214,0,0.6); }
.lampu-hijau:hover  { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(46,204,113,0.6); }

.lampu-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    border: 3px solid rgba(255,255,255,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}

.lampu-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: white;
}

.lampu-kuning .lampu-label { color: #1A1A00; }
.lampu-kuning .lampu-circle { border-color: rgba(0,0,0,0.3); background: rgba(0,0,0,0.15); }

.lampu-desc {
    font-size: 0.8rem;
    opacity: 0.85;
    color: white;
    font-weight: 500;
}
.lampu-kuning .lampu-desc { color: #1A1A00; }

/* Timer bar */
.timer-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0 1.5rem;
}

/* Badge */
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #9999BB;
    text-transform: uppercase;
}

/* Situasi box */
.situasi-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 1.5rem;
    margin: 1rem 0 1.5rem;
    text-align: center;
    font-size: 1.15rem;
    font-weight: 500;
    line-height: 1.6;
    color: #E8E8F0;
    position: relative;
}

.situasi-box::before {
    content: '"';
    position: absolute;
    top: -10px;
    left: 20px;
    font-size: 4rem;
    font-family: 'Syne', sans-serif;
    color: rgba(255,255,255,0.08);
    line-height: 1;
}

/* Countdown number */
.countdown-num {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    line-height: 1;
}

/* Result pill */
.result-pill {
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}

/* Rekap item */
.rekap-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 8px;
}

/* CTA button */
.cta-wrap { position: relative; margin-top: 1rem; }
.cta-btn {
    width: 100%;
    background: linear-gradient(135deg, #6C63FF, #A855F7);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 1rem;
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    cursor: pointer;
    box-shadow: 0 8px 24px rgba(108,99,255,0.35);
    transition: transform 0.15s, box-shadow 0.15s;
}
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 14px 32px rgba(108,99,255,0.5); }
</style>
""", unsafe_allow_html=True)

# ── session state ──
for k, v in [("phase","intro"),("idx",0),("timer_start",0),("pilihan",{})]:
    if k not in st.session_state:
        st.session_state[k] = v


def mulai_situasi():
    st.session_state.phase = "countdown"
    st.session_state.timer_start = time.time()


def pilih_warna(warna):
    st.session_state.pilihan[st.session_state.idx] = warna
    st.session_state.phase = "hasil"


def situasi_berikutnya():
    st.session_state.idx += 1
    if st.session_state.idx >= len(SITUASI):
        st.session_state.phase = "selesai"
    else:
        mulai_situasi()


# ══════════════════════════
# INTRO
# ══════════════════════════
if st.session_state.phase == "intro":
    st.markdown("""
    <div style='text-align:center;padding:2rem 0 1rem;'>
        <div style='font-size:4rem;margin-bottom:0.5rem;'>🚦</div>
        <h1 style='font-size:2.2rem;margin:0;background:linear-gradient(135deg,#fff 40%,#A78BFA);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>Lampu Kendali</h1>
        <p style='color:#6B6B8A;margin-top:0.5rem;font-size:0.95rem;'>Seberapa cepat kamu bisa kendalikan diri?</p>
    </div>
    """, unsafe_allow_html=True)

    for w, info in WARNA.items():
        txt_color = "#1A1A00" if w == "kuning" else "white"
        st.markdown(f"""
        <div class='lampu-btn lampu-{w}' style='margin-bottom:12px;flex-direction:row;justify-content:flex-start;gap:14px;padding:1rem 1.4rem;'>
            <div class='lampu-circle'>{info['emoji']}</div>
            <div style='text-align:left;'>
                <div class='lampu-label'>{info['label']}</div>
                <div class='lampu-desc'>{info['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='cta-wrap'>", unsafe_allow_html=True)
    # invisible streamlit button layered on top
    if st.button("Mulai Game", key="start"):
        mulai_situasi()
        st.rerun()
    st.markdown("""
    <div style='pointer-events:none;margin-top:-2.5rem;'>
        <div class='cta-btn'>▶ &nbsp;Mulai Game</div>
    </div></div>
    """, unsafe_allow_html=True)


# ══════════════════════════
# COUNTDOWN + PILIH
# ══════════════════════════
elif st.session_state.phase in ("countdown", "pilih"):
    idx = st.session_state.idx
    elapsed = time.time() - st.session_state.timer_start
    sisa = max(0.0, TIMER - elapsed)
    pct = sisa / TIMER

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.5rem;'>
        <span class='badge'>Situasi {idx+1} / {len(SITUASI)}</span>
    </div>
    <div class='situasi-box'>{SITUASI[idx]}</div>
    """, unsafe_allow_html=True)

    # Timer
    if sisa > 0.3:
        color = "#FF4D4D" if pct < 0.4 else "#FFD600" if pct < 0.7 else "#2ECC71"
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:0.25rem;'>
            <span class='countdown-num' style='color:{color}'>{sisa:.1f}</span>
            <span style='color:#4A4A6A;font-size:0.9rem;'> detik</span>
        </div>
        <div class='timer-bar-bg'>
            <div style='background:{color};width:{pct*100:.1f}%;height:100%;border-radius:999px;
            transition:width 0.1s linear;box-shadow:0 0 10px {color};'></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='text-align:center;color:#6B6B8A;font-size:0.9rem;margin-bottom:1rem;'>Pilih lampu yang tepat:</p>", unsafe_allow_html=True)

        for warna, info in WARNA.items():
            col1, col2 = st.columns([1, 10])
            txt = "#1A1A00" if warna == "kuning" else "white"
            st.markdown(f"""
            <div class='lampu-btn lampu-{warna}' style='margin-bottom:12px;'>
                <div class='lampu-circle'>{info['emoji']}</div>
                <div class='lampu-label'>{info['label']}</div>
                <div class='lampu-desc'>{info['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(info["label"], key=f"w_{warna}_{idx}"):
                pilih_warna(warna)
                st.rerun()

        time.sleep(0.1)
        st.rerun()

    else:
        if idx not in st.session_state.pilihan:
            st.session_state.pilihan[idx] = None
        st.session_state.phase = "hasil"
        st.rerun()


# ══════════════════════════
# HASIL
# ══════════════════════════
elif st.session_state.phase == "hasil":
    idx = st.session_state.idx
    pilihan = st.session_state.pilihan.get(idx)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:0.5rem;'>
        <span class='badge'>Situasi {idx+1} / {len(SITUASI)}</span>
    </div>
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:16px;padding:1rem 1.2rem;margin-bottom:1rem;text-align:center;
    color:#6B6B8A;font-size:0.9rem;font-style:italic;'>"{SITUASI[idx]}"</div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA:
        info = WARNA[pilihan]
        txt = "#1A1A00" if pilihan == "kuning" else "white"
        st.markdown(f"""
        <div class='result-pill' style='background:{info["hex"]};
        box-shadow:0 12px 40px {info["glow"]};margin-bottom:1.5rem;'>
            <div style='font-size:3.5rem;margin-bottom:8px;'>{info['emoji']}</div>
            <div style='font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;
            color:{txt};letter-spacing:0.05em;'>{info['label']}</div>
            <div style='color:{txt};opacity:0.85;font-size:0.9rem;margin-top:4px;'>{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='result-pill' style='background:rgba(255,255,255,0.06);
        border:1px solid rgba(255,255,255,0.1);margin-bottom:1.5rem;'>
            <div style='font-size:3rem;'>⏰</div>
            <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#6B6B8A;'>Waktu habis!</div>
            <div style='color:#4A4A6A;font-size:0.85rem;margin-top:4px;'>Tidak ada pilihan</div>
        </div>
        """, unsafe_allow_html=True)

    label = "Situasi Berikutnya →" if idx < len(SITUASI) - 1 else "Lihat Hasil Akhir 🏁"
    if st.button(label, key="next"):
        situasi_berikutnya()
        st.rerun()
    st.markdown(f"""
    <div style='pointer-events:none;margin-top:-2.5rem;'>
        <div class='cta-btn'>{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════
# SELESAI
# ══════════════════════════
elif st.session_state.phase == "selesai":
    st.balloons()
    st.markdown("""
    <div style='text-align:center;padding:1.5rem 0 1rem;'>
        <div style='font-size:3rem;'>🎉</div>
        <h2 style='font-family:Syne,sans-serif;font-size:1.8rem;margin:0.25rem 0;'>Kamu keren!</h2>
        <p style='color:#6B6B8A;font-size:0.9rem;'>Ini pilihan kamu tadi</p>
    </div>
    """, unsafe_allow_html=True)

    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA:
            info = WARNA[pilihan]
            txt = "#1A1A00" if pilihan == "kuning" else "white"
            dot = f"<span style='display:inline-block;width:12px;height:12px;border-radius:50%;background:{info['hex']};margin-right:6px;vertical-align:middle;box-shadow:0 0 6px {info['glow']};'></span>"
            label_html = f"{dot}<span style='color:{info['hex']};font-weight:700;font-size:0.85rem;'>{info['label']}</span>"
        else:
            label_html = "<span style='color:#4A4A6A;font-size:0.85rem;'>⏰ Tidak menjawab</span>"

        st.markdown(f"""
        <div class='rekap-item'>
            <div style='font-size:0.75rem;color:#4A4A6A;font-weight:600;min-width:24px;text-align:center;'>{i+1}</div>
            <div style='flex:1;'>
                <div style='font-size:0.82rem;color:#9999BB;margin-bottom:3px;'>{situasi}</div>
                <div>{label_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Mulai Ulang 🔁", key="restart"):
        for key in ["phase","idx","timer_start","pilihan"]:
            del st.session_state[key]
        st.rerun()
    st.markdown("""
    <div style='pointer-events:none;margin-top:-2.5rem;'>
        <div class='cta-btn'>Mulai Ulang 🔁</div>
    </div>
    """, unsafe_allow_html=True)
