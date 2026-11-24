
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

# =========================
# LANGUAGE TRANSLATIONS
# =========================

LANGUAGES = {
    "Indonesia 🇮🇩": "id",
    "English 🇬🇧": "en"
}

TEXT = {
    "id": {
        "menu": "MENU UTAMA",
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "videos": "Hasil Video",
        "about": "Tentang",
        "created": "DIBUAT OLEH",
        "founder": "Founder & Developer",
        "welcome": "SELAMAT DATANG DI WORKSPACE",
        "hero_title": "Berkarya Lebih. Edit Lebih Sedikit.",
        "hero_desc": "Ubah video panjang menjadi konten pendek menarik dengan bantuan AI.",
        "total_clips": "TOTAL VIDEO CLIP",
        "subtitles": "SUBTITLE OTOMATIS",
        "active": "AKTIF",
        "format": "FORMAT VIDEO",
        "quick": "⚡ Akses Cepat",
        "quick_clipper": "🎬 AI Clipper",
        "quick_clipper_desc": "Temukan momen menarik dan buat video pendek secara otomatis.",
        "quick_library": "📁 Koleksi Video",
        "quick_library_desc": "Tonton dan unduh video yang sudah kamu proses.",
        "open_clipper": "BUKA AI CLIPPER →",
        "view_videos": "LIHAT VIDEO SAYA →",
        "upload_title": "Unggah video kamu. Biarkan AI menemukan momen terbaik.",
        "upload": "📤 Unggah video",
        "ready": "Video siap diproses",
        "settings": "⚙️ Pengaturan Pemrosesan",
        "clip_count": "Jumlah clip",
        "duration": "Durasi setiap clip (detik)",
        "configuration": "Konfigurasi",
        "vertical": "Vertikal 9:16",
        "generate": "🚀 BUAT VIDEO CLIP",
        "processing": "CLIPER AI sedang memproses video kamu...",
        "success": "Berhasil! Video sudah dibuat.",
        "failed": "Proses gagal",
        "latest": "🎉 Video Terbaru",
        "download": "⬇️ UNDUH VIDEO",
        "library_title": "Video Saya",
        "library_desc": "Tonton dan unduh video hasil pemrosesan kamu.",
        "file_size": "Ukuran File",
        "no_videos": "Belum ada video final. Silakan buat clip terlebih dahulu.",
        "about_title": "Tentang CLIPER AI",
        "vision": "🚀 Visi Kami",
        "vision_desc": "Membantu kreator mengubah video panjang menjadi konten pendek dengan lebih mudah dan efisien.",
        "features": "✨ Fitur Platform",
        "feature1": "Analisis momen video menggunakan AI",
        "feature2": "Pemotongan video otomatis",
        "feature3": "Subtitle per kata secara otomatis",
        "feature4": "Format video vertikal 9:16",
        "feature5": "Pratinjau dan unduh video",
        "language": "🌐 PILIH BAHASA",
        "language_note": "Bahasa dapat diganti kapan saja.",
        "caption": "CLIPER AI • EDISI PROFESIONAL",
        "max_size": "Ukuran maksimal 200 MB",
        "clip_ready": "Video siap diproses",
    },
    "en": {
        "menu": "MAIN MENU",
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "videos": "My Videos",
        "about": "About",
        "created": "CREATED BY",
        "founder": "Founder & Developer",
        "welcome": "WELCOME TO YOUR WORKSPACE",
        "hero_title": "Create More. Edit Less.",
        "hero_desc": "Turn long videos into engaging short-form content with the power of AI.",
        "total_clips": "TOTAL VIDEO CLIPS",
        "subtitles": "AUTO SUBTITLES",
        "active": "ACTIVE",
        "format": "VIDEO FORMAT",
        "quick": "⚡ Quick Access",
        "quick_clipper": "🎬 AI Clipper",
        "quick_clipper_desc": "Automatically find interesting moments and create short videos.",
        "quick_library": "📁 Video Library",
        "quick_library_desc": "Watch and download your processed videos.",
        "open_clipper": "OPEN AI CLIPPER →",
        "view_videos": "VIEW MY VIDEOS →",
        "upload_title": "Upload your video. Let AI find the best moments.",
        "upload": "📤 Upload your video",
        "ready": "Video ready to process",
        "settings": "⚙️ Processing Settings",
        "clip_count": "Number of clips",
        "duration": "Clip duration (seconds)",
        "configuration": "Configuration",
        "vertical": "Vertical 9:16",
        "generate": "🚀 GENERATE VIDEO CLIPS",
        "processing": "CLIPER AI is processing your video...",
        "success": "Success! Your videos have been created.",
        "failed": "Processing failed",
        "latest": "🎉 Latest Generated Videos",
        "download": "⬇️ DOWNLOAD VIDEO",
        "library_title": "My Video Clips",
        "library_desc": "Watch and download your generated videos.",
        "file_size": "File Size",
        "no_videos": "No final videos yet. Please create clips first.",
        "about_title": "About CLIPER AI",
        "vision": "🚀 Our Vision",
        "vision_desc": "Helping creators turn long videos into short-form content more easily and efficiently.",
        "features": "✨ Platform Features",
        "feature1": "AI-powered video moment analysis",
        "feature2": "Automatic video clipping",
        "feature3": "Automatic word-by-word subtitles",
        "feature4": "Vertical 9:16 video format",
        "feature5": "Video preview and download",
        "language": "🌐 SELECT LANGUAGE",
        "language_note": "You can change the language anytime.",
        "caption": "CLIPER AI • DARK PROFESSIONAL EDITION",
        "max_size": "Maximum file size: 200 MB",
        "clip_ready": "Video is ready to process",
    }
}

if "language" not in st.session_state:
    st.session_state.language = "id"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

lang = st.session_state.language
t = TEXT[lang]

# =========================
# CUSTOM DESIGN
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #080b14;
    --panel: #111827;
    --border: #27334a;
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

.metric-card, .quick-card, .section-card {
    background: linear-gradient(145deg, #18243a, #111827);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 23px;
    margin-bottom: 18px;
    box-shadow: 0 8px 25px #00000025;
}

.metric-card {
    min-height: 125px;
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

.quick-card {
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

.stButton button, .stDownloadButton button {
    background: linear-gradient(100deg, #426bff, #865cff);
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 800;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: linear-gradient(100deg, #6285ff, #a17cff);
    color: white;
    border: 0;
}

div[data-baseweb="select"] > div {
    background: #18243a;
    border-color: #34415f;
}

hr {
    border-color: var(--border);
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


def go_to(page):
    st.session_state.page = page


# =========================
# SIDEBAR
# =========================

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

    st.markdown(f"**{t['language']}**")

    language_choice = st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
        index=0 if lang == "id" else 1,
        label_visibility="collapsed"
    )

    new_lang = LANGUAGES[language_choice]

    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

    st.caption(t["language_note"])

    st.divider()

    st.markdown(f"**{t['menu']}**")

    pages = [
        t["dashboard"],
        t["clipper"],
        t["videos"],
        t["about"]
    ]

    page_map = {
        t["dashboard"]: "Dashboard",
        t["clipper"]: "AI Clipper",
        t["videos"]: "Hasil Video",
        t["about"]: "Tentang"
    }

    reverse_map = {v: k for k, v in page_map.items()}

    current_label = reverse_map.get(
        st.session_state.page,
        t["dashboard"]
    )

    selected_page = st.radio(
        "WORKSPACE",
        pages,
        index=pages.index(current_label),
        label_visibility="collapsed"
    )

    st.session_state.page = page_map[selected_page]

    st.divider()

    st.markdown(f"""
    <div style="padding:10px 0;">
        <div style="font-size:11px;color:#8292b5;letter-spacing:1px;">
            {t['created']}
        </div>
        <div style="font-weight:800;margin-top:5px;">Raihan Zaki</div>
        <div style="font-size:12px;color:#8292b5;">
            {t['founder']}
        </div>
    </div>
    """, unsafe_allow_html=True)


page = st.session_state.page

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    videos = get_final_videos()

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">{t['welcome']}</div>
        <h1>{t['hero_title']}</h1>
        <p>{t['hero_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎬 {t['total_clips']}</div>
            <div class="metric-value">{len(videos)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💬 {t['subtitles']}</div>
            <div class="metric-value">{t['active']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📱 {t['format']}</div>
            <div class="metric-value">9:16</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader(t["quick"])

    a, b = st.columns(2)

    with a:
        st.markdown(f"""
        <div class="quick-card">
            <h3>{t['quick_clipper']}</h3>
            <p>{t['quick_clipper_desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            t["open_clipper"],
            use_container_width=True,
            on_click=go_to,
            args=("AI Clipper",)
        )

    with b:
        st.markdown(f"""
        <div class="quick-card">
            <h3>{t['quick_library']}</h3>
            <p>{t['quick_library_desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            t["view_videos"],
            use_container_width=True,
            on_click=go_to,
            args=("Hasil Video",)
        )

    st.caption(t["caption"])


# =========================
# AI CLIPPER
# =========================

elif page == "AI Clipper":

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">AI VIDEO CREATION</div>
        <h1>AI Clipper</h1>
        <p>{t['upload_title']}</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        t["upload"],
        type=["mp4", "mov", "mkv", "avi"],
        help=t["max_size"]
    )

    if uploaded_file:
        st.success(f"{t['ready']}: {uploaded_file.name}")
        st.video(uploaded_file)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader(t["settings"])

    col1, col2 = st.columns(2)

    with col1:
        jumlah_clip = st.selectbox(
            t["clip_count"],
            [3, 5, 10, 15, 20],
            index=1
        )

    with col2:
        durasi = st.selectbox(
            t["duration"],
            [15, 30, 45, 60, 90],
            index=2
        )

    st.info(
        f"{t['configuration']}: {jumlah_clip} clips • "
        f"{durasi} seconds • {t['vertical']}"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button(
        t["generate"],
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

                if "transkrip" in msg or "transcrib" in msg:
                    progress_bar.progress(10)
                elif "menganalisis" in msg or "analyz" in msg:
                    progress_bar.progress(25)
                elif "membuat video" in msg or "creating video" in msg:
                    progress_bar.progress(45)
                elif "subtitle video" in msg:
                    progress_bar.progress(65)
                elif "memasang subtitle" in msg:
                    progress_bar.progress(80)

            with st.spinner(t["processing"]):
                output_videos = engine.process_video(
                    source_path,
                    clip_count=jumlah_clip,
                    duration=durasi,
                    progress=update_progress
                )

            progress_bar.progress(100)

            status.success(
                f"{t['success']} ({len(output_videos)} clips)"
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
            status.error(f"{t['failed']}: {error}")

    latest = st.session_state.get("latest_outputs", [])

    if latest:
        st.divider()
        st.subheader(t["latest"])

        for video in latest:
            path = Path(video)

            if path.exists():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader(path.name)
                st.video(str(path))

                with open(path, "rb") as f:
                    st.download_button(
                        t["download"],
                        data=f,
                        file_name=path.name,
                        mime="video/mp4",
                        key="latest_" + path.name,
                        use_container_width=True
                    )

                st.markdown('</div>', unsafe_allow_html=True)


# =========================
# VIDEO LIBRARY
# =========================

elif page == "Hasil Video":

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">YOUR VIDEO LIBRARY</div>
        <h1>{t['library_title']}</h1>
        <p>{t['library_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    videos = get_final_videos()

    if videos:
        for i, video in enumerate(videos, 1):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader(f"CLIP {i:02d} — {video.stem}")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.video(str(video))

            with col2:
                size_mb = video.stat().st_size / (1024 * 1024)
                st.metric(t["file_size"], f"{size_mb:.1f} MB")
                st.caption("MP4 • Vertical 9:16")

                with open(video, "rb") as f:
                    st.download_button(
                        t["download"],
                        data=f,
                        file_name=video.name,
                        mime="video/mp4",
                        key=video.name,
                        use_container_width=True
                    )

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(t["no_videos"])


# =========================
# ABOUT
# =========================

elif page == "Tentang":

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">ABOUT THE PLATFORM</div>
        <h1>CLIPER AI</h1>
        <p>{t['about_title']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-card">
        <h3>{t['vision']}</h3>
        <p>{t['vision_desc']}</p>

        <h3>{t['features']}</h3>
        <p>• {t['feature1']}</p>
        <p>• {t['feature2']}</p>
        <p>• {t['feature3']}</p>
        <p>• {t['feature4']}</p>
        <p>• {t['feature5']}</p>

        <br>
        <h3>👨‍💻 {t['founder']}</h3>
        <p><b>Raihan Zaki</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("CLIPER AI © 2026")
