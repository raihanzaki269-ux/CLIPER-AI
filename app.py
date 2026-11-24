
import streamlit as st
from pathlib import Path
import tempfile
import engine

st.set_page_config(
    page_title="CLIPER AI",
    page_icon="🌊",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #061827;
    color: #edfaff;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #092b43, #061827);
    border-right: 1px solid #164b67;
}
[data-testid="stSidebar"] * { color: #e7f8ff !important; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
h1, h2, h3 {
    color: #f0fbff !important;
    font-weight: 800 !important;
}
p, label { color: #b6d1df; }
.hero {
    background: linear-gradient(115deg, #0b3d5c, #087ea4, #06415d);
    padding: 35px;
    border-radius: 22px;
    border: 1px solid #268bab;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px #00101d80;
}
.hero h1 {
    font-size: 42px;
    margin: 0;
    color: white !important;
}
.hero p { color: #d8f5ff !important; font-size: 16px; }
.metric-card {
    background: linear-gradient(145deg, #103650, #0a263b);
    border: 1px solid #1c607e;
    border-radius: 16px;
    padding: 22px;
    min-height: 115px;
}
.metric-title { color: #9fc9db; font-size: 13px; }
.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}
.section-card {
    background: #0b263a;
    border: 1px solid #164b67;
    padding: 23px;
    border-radius: 18px;
    margin-bottom: 20px;
}
div[data-testid="stFileUploader"] {
    background: #0d3048;
    border: 1px dashed #35a9cc;
    border-radius: 15px;
    padding: 18px;
}
.stButton button, .stDownloadButton button {
    background: linear-gradient(100deg, #087ea4, #19a9c9);
    color: white;
    border: 0;
    border-radius: 11px;
    font-weight: 700;
    min-height: 43px;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: #25b8d7;
    color: white;
    border: 0;
}
div[data-baseweb="select"] > div {
    background: #103650;
    border-color: #1c607e;
}
hr { border-color: #164b67; }
.small-note { color: #83aebe; font-size: 12px; }
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
    <div style="padding:12px 5px 20px;">
        <div style="font-size:32px;font-weight:800;color:#43c9e5;">
            🌊 CLIPER AI
        </div>
        <div style="font-size:12px;color:#9fc9db;">
            INTELLIGENT VIDEO CLIPPING
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    page = st.radio(
        "MAIN MENU",
        ["Dashboard", "AI Clipper", "Hasil Video", "Tentang"]
    )
    st.divider()

    st.markdown("""
    <div style="padding:10px 0;">
        <div style="font-size:12px;color:#83aebe;">CREATED BY</div>
        <b>Raihan Zaki</b>
        <div style="font-size:12px;color:#83aebe;">Founder & Developer</div>
    </div>
    """, unsafe_allow_html=True)


if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <div style="font-size:13px;letter-spacing:2px;color:#b9efff;">
            WELCOME TO YOUR WORKSPACE
        </div>
        <h1>Video Creation, Simplified.</h1>
        <p>Ubah video panjang menjadi konten pendek yang menarik dengan CLIPER AI.</p>
    </div>
    """, unsafe_allow_html=True)

    videos = get_final_videos()
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
    st.subheader("🚀 Quick Access")
    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="section-card">
            <h3>🎞️ AI Clipper</h3>
            <p>Upload video dan buat beberapa clip secara otomatis.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="section-card">
            <h3>📂 Hasil Video</h3>
            <p>Lihat, putar, dan download video hasil pemrosesan.</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption("CLIPER AI • Ocean Blue Edition")


elif page == "AI Clipper":
    st.title("🎬 AI Video Clipper")
    st.write("Upload video untuk memulai proses pembuatan clip.")

    uploaded_file = st.file_uploader(
        "Pilih video yang ingin diproses",
        type=["mp4", "mov", "mkv", "avi"],
        help="Maksimal 200 MB"
    )

    if uploaded_file:
        st.success(f"Video berhasil dipilih: {uploaded_file.name}")
        st.video(uploaded_file)

    st.subheader("⚙️ Pengaturan Video")
    col1, col2 = st.columns(2)

    with col1:
        jumlah_clip = st.selectbox(
            "Jumlah clip", [3, 5, 10, 15, 20], index=1
        )

    with col2:
        durasi = st.selectbox(
            "Durasi setiap clip (detik)",
            [15, 30, 45, 60, 90],
            index=2
        )

    st.info(
        f"Pengaturan: {jumlah_clip} clip • {durasi} detik • Format 9:16"
    )

    if st.button(
        "🚀 MULAI PROSES VIDEO",
        use_container_width=True,
        disabled=uploaded_file is None
    ):
        progress_bar = st.progress(0)
        status = st.empty()

        try:
            suffix = Path(uploaded_file.name).suffix.lower()
            if not suffix:
                suffix = ".mp4"

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                dir=UPLOADS
            ) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                source_path = Path(temp_file.name)

            def update_progress(message):
                status.info(message)
                if "transkrip" in message.lower():
                    progress_bar.progress(10)
                elif "menganalisis" in message.lower():
                    progress_bar.progress(25)
                elif "membuat video" in message.lower():
                    progress_bar.progress(45)
                elif "subtitle video" in message.lower():
                    progress_bar.progress(65)
                elif "memasang subtitle" in message.lower():
                    progress_bar.progress(80)

            with st.spinner("CLIPER AI sedang bekerja..."):
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
        st.subheader("Hasil Pemrosesan Terbaru")
        for video in latest:
            path = Path(video)
            if path.exists():
                st.video(str(path))
                with open(path, "rb") as f:
                    st.download_button(
                        "⬇️ Download " + path.name,
                        data=f,
                        file_name=path.name,
                        mime="video/mp4",
                        key="latest_" + path.name
                    )


elif page == "Hasil Video":
    st.title("📂 Hasil Video")
    st.write("Semua video final yang sudah berhasil dibuat.")

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
                    st.metric("Ukuran File", f"{size_mb:.1f} MB")
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

                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada video final. Silakan buat clip terlebih dahulu.")


elif page == "Tentang":
    st.title("🌊 Tentang CLIPER AI")

    st.markdown("""
    <div class="hero">
        <h1>CLIPER AI</h1>
        <p>Intelligent Video Clipping Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <h3>Visi Kami</h3>
        <p>Membantu kreator mengubah video panjang menjadi konten pendek dengan lebih mudah dan efisien.</p>
        <h3>Fitur Platform</h3>
        <p>• AI video moment analysis berbasis transkrip</p>
        <p>• Automatic video clipping</p>
        <p>• Word-by-word subtitles</p>
        <p>• Vertical video format 9:16</p>
        <p>• Video preview and download</p>
        <br>
        <h3>Founder & Developer</h3>
        <p><b>Raihan Zaki</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("CLIPER AI © 2026")
