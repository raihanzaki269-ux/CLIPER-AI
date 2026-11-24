
import streamlit as st
from pathlib import Path
import tempfile
import engine

st.set_page_config(
    page_title="CLIPER AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
UPLOADS = ROOT / "uploads"
RESULTS.mkdir(exist_ok=True)
UPLOADS.mkdir(exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #080b14;
    --panel: #111827;
    --panel2: #151e30;
    --border: #27334a;
    --blue: #4285ff;
    --purple: #865cff;
    --text: #f4f6ff;
    --muted: #98a5bd;
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: #e8edff;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: var(--text) !important;
    font-weight: 800 !important;
}

p, label {
    color: var(--muted);
}

.hero {
    background: linear-gradient(120deg, #172b50, #29205b 60%, #171d39);
    border: 1px solid #46518c;
    border-radius: 24px;
    padding: 38px;
    margin-bottom: 28px;
    box-shadow: 0 15px 50px #00000050;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 48px);
    color: white !important;
    margin: 8px 0;
    letter-spacing: -1.5px;
}

.hero p {
    color: #c5d2f5 !important;
    font-size: 15px;
}

.eyebrow {
    color: #9eaeff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.metric-card {
    background: linear-gradient(145deg, #18243a, #111827);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 23px;
    min-height: 125px;
    box-shadow: 0 8px 25px #00000025;
}

.metric-title {
    color: #9eacc6;
    font-size: 12px;
    font-weight: 700;
}

.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
    margin-top: 12px;
}

.section-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
}

.quick-card {
    background: linear-gradient(145deg, #17233a, #111827);
    border: 1px solid #34415f;
    border-radius: 19px;
    padding: 24px;
    min-height: 155px;
}

.quick-card h3 {
    font-size: 19px;
}

div[data-testid="stFileUploader"] {
    background: #111b2d;
    border: 1px dashed #667eea;
    border-radius: 17px;
    padding: 20px;
}

.stButton button,
.stDownloadButton button {
    background: linear-gradient(100deg, #426bff, #865cff);
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 800;
    transition: 0.2s;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(100deg, #6285ff, #a17cff);
    color: white;
    border: 0;
    transform: translateY(-1px);
}

div[data-baseweb="select"] > div {
    background: #18243a;
    border-color: #34415f;
}

.stRadio label {
    color: #e8edff !important;
}

hr {
    border-color: var(--border);
}

.small-note {
    color: #7888a5;
    font-size: 12px;
}

[data-testid="stMetric"] {
    background: #151e30;
    border: 1px solid #27334a;
    padding: 15px;
    border-radius: 14px;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #426bff, #a17cff);
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }
    .hero {
        padding: 25px 20px;
        border-radius: 18px;
    }
    .metric-card {
        padding: 15px;
        min-height: 105px;
    }
    .metric-value {
        font-size: 23px;
    }
    .section-card {
        padding: 17px;
    }
}
</style>
""", unsafe_allow_html=True)


def get_final_videos():
    return sorted(
        RESULTS.glob("*_FINAL.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )


with st.sidebar:
    st.markdown("""
    <div style="padding:15px 5px 20px;">
        <div style="font-size:29px;font-weight:900;letter-spacing:-1px;">
            <span style="color:#6e8cff;">✦</span>
            <span style="color:white;">CLIPER</span>
            <span style="color:#9b7cff;">AI</span>
        </div>
        <div style="font-size:10px;letter-spacing:2px;color:#8292b5;">
            INTELLIGENT VIDEO CLIPPING
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Dashboard", "AI Clipper", "Hasil Video", "Tentang"]
    )

    st.divider()

    st.markdown("""
    <div style="padding:10px 0;">
        <div style="font-size:11px;color:#8292b5;letter-spacing:1px;">
            CREATED BY
        </div>
        <div style="font-weight:800;margin-top:5px;">Raihan Zaki</div>
        <div style="font-size:12px;color:#8292b5;">
            Founder & Developer
        </div>
    </div>
    """, unsafe_allow_html=True)


if page == "Dashboard":
    videos = get_final_videos()

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">WELCOME TO YOUR WORKSPACE</div>
        <h1>Create More. Edit Less.</h1>
        <p>Turn long videos into engaging short-form content with the power of AI.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎬 TOTAL VIDEO CLIPS</div>
            <div class="metric-value">{len(videos)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">💬 AUTO SUBTITLES</div>
            <div class="metric-value">ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">📱 VIDEO FORMAT</div>
            <div class="metric-value">9:16</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("⚡ Quick Access")

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="quick-card">
            <h3>🎬 AI Clipper</h3>
            <p>Automatically find interesting moments and create short videos.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("OPEN AI CLIPPER →", use_container_width=True):
            st.session_state["menu_page"] = "AI Clipper"
            st.rerun()

    with b:
        st.markdown("""
        <div class="quick-card">
            <h3>📁 Video Library</h3>
            <p>Watch and download your processed video clips.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("VIEW MY VIDEOS →", use_container_width=True):
            st.session_state["menu_page"] = "Hasil Video"
            st.rerun()

    st.caption("CLIPER AI • DARK PROFESSIONAL EDITION")


elif page == "AI Clipper":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">AI VIDEO CREATION</div>
        <h1>AI Video Clipper</h1>
        <p>Upload your video. Let AI find the best moments.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📤 Upload your video",
        type=["mp4", "mov", "mkv", "avi"],
        help="Maksimal 200 MB"
    )

    if uploaded_file:
        st.success(f"Video siap diproses: {uploaded_file.name}")
        st.video(uploaded_file)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("⚙️ Processing Settings")

    col1, col2 = st.columns(2)

    with col1:
        jumlah_clip = st.selectbox(
            "Jumlah clip",
            [3, 5, 10, 15, 20],
            index=1
        )

    with col2:
        durasi = st.selectbox(
            "Durasi setiap clip (detik)",
            [15, 30, 45, 60, 90],
            index=2
        )

    st.info(
        f"Konfigurasi: {jumlah_clip} clips • {durasi} detik • Vertical 9:16"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button(
        "🚀 GENERATE VIDEO CLIPS",
        use_container_width=True,
        disabled=uploaded_file is None
    ):
        progress_bar = st.progress(0)
        status = st.empty()

        try:
            suffix = Path(uploaded_file.name).suffix.lower() or ".mp4"

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                dir=UPLOADS
            ) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                source_path = Path(temp_file.name)

            def update_progress(message):
                status.info(message)
                msg = message.lower()

                if "transkrip" in msg:
                    progress_bar.progress(10)
                elif "menganalisis" in msg:
                    progress_bar.progress(25)
                elif "membuat video" in msg:
                    progress_bar.progress(45)
                elif "subtitle video" in msg:
                    progress_bar.progress(65)
                elif "memasang subtitle" in msg:
                    progress_bar.progress(80)

            with st.spinner("CLIPER AI is processing your video..."):
                output_videos = engine.process_video(
                    source_path,
                    clip_count=jumlah_clip,
                    duration=durasi,
                    progress=update_progress
                )

            progress_bar.progress(100)

            status.success(
                f"Berhasil! {len(output_videos)} video sudah dibuat."
            )

            st.session_state["latest_outputs"] = [
                str(p) for p in output_videos
            ]

            try:
                source_path.unlink()
            except OSError:
                pass

            st.rerun()

        except Exception as error:
            progress_bar.empty()
            status.error(f"Proses gagal: {error}")

    latest = st.session_state.get("latest_outputs", [])

    if latest:
        st.divider()
        st.subheader("🎉 Latest Generated Videos")

        for video in latest:
            path = Path(video)

            if path.exists():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader(path.name)
                st.video(str(path))

                with open(path, "rb") as f:
                    st.download_button(
                        "⬇️ DOWNLOAD VIDEO",
                        data=f,
                        file_name=path.name,
                        mime="video/mp4",
                        key="latest_" + path.name,
                        use_container_width=True
                    )

                st.markdown('</div>', unsafe_allow_html=True)


elif page == "Hasil Video":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR VIDEO LIBRARY</div>
        <h1>My Video Clips</h1>
        <p>Watch and download your generated videos.</p>
    </div>
    """, unsafe_allow_html=True)

    videos = get_final_videos()

    if videos:
        for i, video in enumerate(videos, 1):
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader(f"CLIP {i:02d} — {video.stem}")

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.video(str(video))

                with col2:
                    size_mb = video.stat().st_size / (1024 * 1024)
                    st.metric("File Size", f"{size_mb:.1f} MB")
                    st.caption("MP4 • Vertical 9:16")

                    with open(video, "rb") as f:
                        st.download_button(
                            "⬇️ DOWNLOAD VIDEO",
                            data=f,
                            file_name=video.name,
                            mime="video/mp4",
                            key=video.name,
                            use_container_width=True
                        )

                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Belum ada video final. Silakan buat clip terlebih dahulu.")


elif page == "Tentang":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">ABOUT THE PLATFORM</div>
        <h1>CLIPER AI</h1>
        <p>Intelligent Video Clipping Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h3>🚀 Our Vision</h3>
        <p>Membantu kreator mengubah video panjang menjadi konten pendek dengan lebih mudah dan efisien.</p>
        <h3>✨ Platform Features</h3>
        <p>• AI video moment analysis berbasis transkrip</p>
        <p>• Automatic video clipping</p>
        <p>• Word-by-word subtitles</p>
        <p>• Vertical video format 9:16</p>
        <p>• Video preview and download</p>
        <br>
        <h3>👨‍💻 Founder & Developer</h3>
        <p><b>Raihan Zaki</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("CLIPER AI © 2026")
