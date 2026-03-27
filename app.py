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
    "merah": {"emoji": "🔴", "label": "MERAH", "desc": "Berhenti & tarik napas", "bg": "#ef4444", "text": "white"},
    "kuning": {"emoji": "🟡", "label": "KUNING", "desc": "Hati-hati & evaluasi dulu", "bg": "#eab308", "text": "#1e293b"},
    "hijau": {"emoji": "🟢", "label": "HIJAU", "desc": "Bertindak dengan bijak", "bg": "#22c55e", "text": "white"},
}

TIMER = 3

st.set_page_config(page_title="Lampu Kendali", page_icon="🚦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stButton > button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    border: none !important;
    transition: transform 0.1s !important;
}
.stButton > button:hover { transform: scale(1.03); }
</style>
""", unsafe_allow_html=True)

# ── session state ──
if "phase" not in st.session_state:
    st.session_state.phase = "intro"  # intro | countdown | pilih | hasil | selesai
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "timer_start" not in st.session_state:
    st.session_state.timer_start = 0
if "pilihan" not in st.session_state:
    st.session_state.pilihan = {}  # idx -> warna


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


# ══════════════════════════════════════════
# INTRO
# ══════════════════════════════════════════
if st.session_state.phase == "intro":
    st.markdown("<h1 style='text-align:center;font-size:3rem;'>🚦</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;font-weight:900;'>Lampu Kendali</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b;'>Latihan pengendalian diri dalam situasi sehari-hari</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for w, info in WARNA.items():
        st.markdown(f"""
        <div style='background:{info["bg"]};color:{info["text"]};border-radius:12px;
        padding:0.75rem 1.2rem;margin-bottom:8px;display:flex;align-items:center;gap:12px;'>
            <span style='font-size:1.5rem'>{info["emoji"]}</span>
            <div>
                <div style='font-weight:800;font-size:1rem'>{info["label"]}</div>
                <div style='font-size:0.85rem;opacity:0.9'>{info["desc"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶️ Mulai Game", use_container_width=True, type="primary"):
        mulai_situasi()
        st.rerun()


# ══════════════════════════════════════════
# COUNTDOWN + PILIH
# ══════════════════════════════════════════
elif st.session_state.phase in ("countdown", "pilih"):
    idx = st.session_state.idx
    situasi = SITUASI[idx]
    elapsed = time.time() - st.session_state.timer_start
    sisa = max(0.0, TIMER - elapsed)

    # Nomor situasi
    st.markdown(f"<p style='text-align:center;color:#94a3b8;font-weight:600;'>Situasi {idx+1} dari {len(SITUASI)}</p>", unsafe_allow_html=True)

    # Kotak situasi
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#667eea,#764ba2);color:white;
    border-radius:20px;padding:2rem 1.5rem;text-align:center;margin:0.5rem 0 1.5rem;'>
        <div style='font-size:1.25rem;font-weight:700;line-height:1.5'>"{situasi}"</div>
    </div>
    """, unsafe_allow_html=True)

    # Timer
    if sisa > 0:
        pct = sisa / TIMER
        color = "#ef4444" if pct < 0.4 else "#eab308" if pct < 0.7 else "#22c55e"
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:0.5rem;'>
            <span style='font-size:2.5rem;font-weight:900;color:{color}'>{sisa:.1f}</span>
            <span style='color:#94a3b8;font-size:1rem;'> detik</span>
        </div>
        <div style='background:#e2e8f0;border-radius:999px;height:10px;margin-bottom:1.5rem;'>
            <div style='background:{color};width:{pct*100:.1f}%;height:10px;border-radius:999px;transition:width 0.1s;'></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Pilih lampu yang tepat:**")
        cols = st.columns(3)
        for i, (warna, info) in enumerate(WARNA.items()):
            with cols[i]:
                st.markdown(f"""
                <button onclick="" style='width:100%;background:{info["bg"]};color:{info["text"]};
                border:none;border-radius:14px;padding:1rem 0.5rem;font-size:0.95rem;
                font-weight:800;cursor:pointer;'>
                {info["emoji"]}<br>{info["label"]}
                </button>
                """, unsafe_allow_html=True)
                if st.button(info["emoji"] + " " + info["label"], key=warna, use_container_width=True):
                    pilih_warna(warna)
                    st.rerun()

        time.sleep(0.1)
        st.rerun()

    else:
        # Timer habis, belum pilih
        if idx not in st.session_state.pilihan:
            st.session_state.pilihan[idx] = None
        st.session_state.phase = "hasil"
        st.rerun()


# ══════════════════════════════════════════
# HASIL
# ══════════════════════════════════════════
elif st.session_state.phase == "hasil":
    idx = st.session_state.idx
    situasi = SITUASI[idx]
    pilihan = st.session_state.pilihan.get(idx)

    st.markdown(f"<p style='text-align:center;color:#94a3b8;font-weight:600;'>Situasi {idx+1} dari {len(SITUASI)}</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#f1f5f9;border-radius:16px;padding:1rem 1.5rem;
    text-align:center;margin-bottom:1rem;color:#475569;font-size:0.95rem;font-style:italic;'>
        "{situasi}"
    </div>
    """, unsafe_allow_html=True)

    if pilihan and pilihan in WARNA:
        info = WARNA[pilihan]
        st.markdown(f"""
        <div style='background:{info["bg"]};color:{info["text"]};border-radius:20px;
        padding:2rem;text-align:center;margin-bottom:1.5rem;'>
            <div style='font-size:3rem'>{info["emoji"]}</div>
            <div style='font-size:1.5rem;font-weight:900;margin:0.25rem 0'>{info["label"]}</div>
            <div style='font-size:1rem;opacity:0.9'>{info["desc"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#f1f5f9;border-radius:20px;padding:2rem;text-align:center;margin-bottom:1.5rem;'>
            <div style='font-size:2rem'>⏰</div>
            <div style='font-size:1.1rem;font-weight:700;color:#64748b'>Waktu habis!</div>
            <div style='color:#94a3b8;font-size:0.9rem'>Tidak ada pilihan yang dipilih</div>
        </div>
        """, unsafe_allow_html=True)

    label_btn = "➡️ Situasi Berikutnya" if idx < len(SITUASI) - 1 else "🏁 Lihat Hasil Akhir"
    if st.button(label_btn, use_container_width=True, type="primary"):
        situasi_berikutnya()
        st.rerun()


# ══════════════════════════════════════════
# SELESAI
# ══════════════════════════════════════════
elif st.session_state.phase == "selesai":
    st.balloons()
    st.markdown("<h2 style='text-align:center;font-weight:900;'>🎉 Selesai!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#64748b;'>Ini pilihan kamu tadi:</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for i, situasi in enumerate(SITUASI):
        pilihan = st.session_state.pilihan.get(i)
        if pilihan and pilihan in WARNA:
            info = WARNA[pilihan]
            badge = f"<span style='background:{info['bg']};color:{info['text']};border-radius:8px;padding:2px 10px;font-weight:700;font-size:0.8rem;'>{info['emoji']} {info['label']}</span>"
        else:
            badge = "<span style='background:#e2e8f0;color:#94a3b8;border-radius:8px;padding:2px 10px;font-size:0.8rem;'>⏰ Tidak menjawab</span>"

        st.markdown(f"""
        <div style='border:1px solid #e2e8f0;border-radius:12px;padding:0.75rem 1rem;margin-bottom:8px;'>
            <div style='color:#94a3b8;font-size:0.75rem;font-weight:600;margin-bottom:4px;'>SITUASI {i+1}</div>
            <div style='font-size:0.9rem;color:#334155;margin-bottom:6px;'>{situasi}</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔁 Mulai Ulang", use_container_width=True):
        for key in ["phase", "idx", "timer_start", "pilihan"]:
            del st.session_state[key]
        st.rerun()
