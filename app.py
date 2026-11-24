import streamlit as st
from supabase import create_client
from pathlib import Path
import uuid
import time
import engine

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="CLIPER AI",
    page_icon="🎬",
    layout="wide"
)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

SITE_URL = "https://cliper-ai-alfymantduy3dpvahsapppx.streamlit.app/"
FOOTER = "CLIPER AI © 2026 | Created by Raihan Zaki"

# =========================
# SESSION
# =========================
defaults = {
    "language": "Indonesia",
    "access_token": None,
    "refresh_token": None,
    "user_id": None,
    "user_email": None,
    "full_name": None,
    "page": "Dashboard",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# LANGUAGE
# =========================
TEXT = {
    "Indonesia": {
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "videos": "Hasil Video",
        "about": "Tentang",
        "welcome": "Selamat datang di CLIPER AI",
        "subtitle": "Ubah video panjang menjadi klip pendek secara otomatis dengan AI.",
        "total": "Total Video",
        "active": "Subtitle",
        "format": "Format",
        "quick": "Akses Cepat",
        "start": "Mulai Membuat Klip",
        "upload": "Upload Video",
        "count": "Jumlah Klip",
        "duration": "Durasi Klip (detik)",
        "process": "Mulai Proses Video",
        "processing": "Sedang memproses video...",
        "download": "Download Video",
        "empty": "Belum ada video. Mulai proses video pertamamu!",
        "description": "CLIPER AI adalah aplikasi AI untuk memotong video panjang menjadi klip pendek dengan subtitle otomatis.",
        "logout": "Keluar",
        "login": "Masuk",
        "register": "Daftar Akun",
        "email": "Alamat Email",
        "password": "Password",
        "name": "Nama Lengkap",
        "login_btn": "Masuk ke Akun",
        "register_btn": "Buat Akun",
        "auth_title": "Selamat Datang di CLIPER AI",
        "auth_desc": "Masuk atau daftar untuk mulai membuat klip video dengan AI.",
        "choose": "Pilih menu",
        "processing_done": "Proses selesai!",
        "processing_error": "Terjadi kesalahan:",
        "invalid_email": "Masukkan email yang valid.",
        "password_short": "Password minimal 6 karakter.",
        "name_required": "Nama lengkap harus diisi.",
        "library": "Perpustakaan Video",
        "no_file": "Silakan upload video terlebih dahulu.",
        "about_title": "Tentang CLIPER AI",
        "language": "Bahasa",
        "my_account": "Akun aktif",
        "confirm_password": "Konfirmasi Password",
        "password_mismatch": "Password dan konfirmasi tidak sama.",
        "video_help": "Format video: MP4, MOV, MKV, AVI.",
        "check_email": "Pendaftaran berhasil. Silakan cek email untuk verifikasi akun sebelum login.",
        "login_success": "Login berhasil!",
        "register_success": "Akun berhasil dibuat!",
        "logout_success": "Kamu telah keluar dari akun.",
        "upload_error": "Terjadi kesalahan saat upload atau memproses video."
    },
    "English": {
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "videos": "My Videos",
        "about": "About",
        "welcome": "Welcome to CLIPER AI",
        "subtitle": "Turn long videos into short clips automatically with AI.",
        "total": "Total Videos",
        "active": "Subtitles",
        "format": "Format",
        "quick": "Quick Access",
        "start": "Start Creating Clips",
        "upload": "Upload Video",
        "count": "Number of Clips",
        "duration": "Clip Duration (seconds)",
        "process": "Start Video Processing",
        "processing": "Processing video...",
        "download": "Download Video",
        "empty": "No videos yet. Start processing your first video!",
        "description": "CLIPER AI is an AI application that turns long videos into short clips with automatic subtitles.",
        "logout": "Log Out",
        "login": "Login",
        "register": "Create Account",
        "email": "Email Address",
        "password": "Password",
        "name": "Full Name",
        "login_btn": "Sign In",
        "register_btn": "Create Account",
        "auth_title": "Welcome to CLIPER AI",
        "auth_desc": "Sign in or create an account to start making AI video clips.",
        "choose": "Choose a menu",
        "processing_done": "Processing completed!",
        "processing_error": "An error occurred:",
        "invalid_email": "Please enter a valid email.",
        "password_short": "Password must be at least 6 characters.",
        "name_required": "Full name is required.",
        "library": "Video Library",
        "no_file": "Please upload a video first.",
        "about_title": "About CLIPER AI",
        "language": "Language",
        "my_account": "Active account",
        "confirm_password": "Confirm Password",
        "password_mismatch": "Passwords do not match.",
        "video_help": "Supported formats: MP4, MOV, MKV, AVI.",
        "check_email": "Registration successful. Please check your email to verify your account before logging in.",
        "login_success": "Login successful!",
        "register_success": "Account created successfully!",
        "logout_success": "You have logged out.",
        "upload_error": "An error occurred while uploading or processing the video."
    }
}

def tr(key):
    return TEXT[st.session_state.language][key]

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: #090d18;
    color: #f1f5f9;
}
[data-testid="stSidebar"] {
    background: #101827;
    border-right: 1px solid #263449;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #f8fafc;
}
p, label, span {
    color: #cbd5e1;
}
div[data-testid="stMetric"] {
    background: #131f32;
    border: 1px solid #263449;
    padding: 18px;
    border-radius: 14px;
}
div.stButton > button {
    background: #2563eb;
    color: white;
    border: 0;
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #1d4ed8;
    color: white;
}
div[data-testid="stFileUploader"] {
    background: #111c2e;
    border: 1px dashed #475569;
    border-radius: 12px;
    padding: 12px;
}
.card {
    background: #111c2e;
    border: 1px solid #263449;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}
.app-footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 24px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SUPABASE
# =========================
try:
    config = {
        "url": st.secrets["supabase"]["url"],
        "key": st.secrets["supabase"]["publishable_key"]
    }
    supabase = create_client(config["url"], config["key"])
except Exception:
    st.error("Supabase connection error. Check Streamlit Secrets.")
    st.stop()

def clear_auth():
    for key in [
        "access_token",
        "refresh_token",
        "user_id",
        "user_email",
        "full_name"
    ]:
        st.session_state[key] = None

def restore_session():
    access = st.session_state.access_token
    refresh = st.session_state.refresh_token

    if not access or not refresh:
        return

    try:
        response = supabase.auth.set_session(access, refresh)
        session = response.session
        user = response.user

        if session:
            st.session_state.access_token = session.access_token
            st.session_state.refresh_token = session.refresh_token

        if user:
            st.session_state.user_id = str(user.id)
            st.session_state.user_email = user.email
            metadata = getattr(user, "user_metadata", {}) or {}
            st.session_state.full_name = metadata.get("full_name", "")
    except Exception:
        clear_auth()

def save_auth(response):
    session = response.session
    user = response.user

    if not session or not user:
        return False

    st.session_state.access_token = session.access_token
    st.session_state.refresh_token = session.refresh_token
    st.session_state.user_id = str(user.id)
    st.session_state.user_email = user.email

    metadata = getattr(user, "user_metadata", {}) or {}
    st.session_state.full_name = metadata.get("full_name", "")
    return True

restore_session()

# =========================
# USER STORAGE
# =========================
def get_user_folder():
    folder = RESULTS / st.session_state.user_id
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def get_user_videos():
    folder = get_user_folder()
    videos = list(folder.glob("*/*_FINAL.mp4"))
    videos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return videos

# =========================
# FOOTER
# =========================
def show_footer():
    st.markdown(
        f'<div class="app-footer">{FOOTER}</div>',
        unsafe_allow_html=True
    )

# =========================
# AUTH SCREEN
# =========================
if not st.session_state.user_id:

    st.markdown("<br>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.5, 1])

    with center:
        st.markdown(
            "<h1 style='text-align:center'>🎬 CLIPER AI</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align:center'>{tr('auth_title')}</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align:center;color:#94a3b8'>{tr('auth_desc')}</p>",
            unsafe_allow_html=True
        )

        choice = st.radio(
            tr("choose"),
            [tr("login"), tr("register")],
            horizontal=True
        )

        if choice == tr("login"):
            with st.form("login_form"):
                email = st.text_input(tr("email"))
                password = st.text_input(
                    tr("password"),
                    type="password"
                )
                submitted = st.form_submit_button(
                    tr("login_btn"),
                    use_container_width=True
                )

            if submitted:
                if not email.strip() or "@" not in email:
                    st.error(tr("invalid_email"))
                elif len(password) < 6:
                    st.error(tr("password_short"))
                else:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email.strip(),
                            "password": password
                        })
                        if save_auth(response):
                            st.success(tr("login_success"))
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(tr("check_email"))
                    except Exception as e:
                        st.error(f"Login gagal: {str(e)}")

        else:
            with st.form("register_form"):
                full_name = st.text_input(tr("name"))
                email = st.text_input(tr("email"))
                password = st.text_input(
                    tr("password"),
                    type="password"
                )
                confirm = st.text_input(
                    tr("confirm_password"),
                    type="password"
                )
                submitted = st.form_submit_button(
                    tr("register_btn"),
                    use_container_width=True
                )

            if submitted:
                if not full_name.strip():
                    st.error(tr("name_required"))
                elif not email.strip() or "@" not in email:
                    st.error(tr("invalid_email"))
                elif len(password) < 6:
                    st.error(tr("password_short"))
                elif password != confirm:
                    st.error(tr("password_mismatch"))
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": full_name.strip()
                                },
                                "email_redirect_to": SITE_URL
                            }
                        })

                        if response.session and save_auth(response):
                            st.success(tr("register_success"))
                            st.rerun()
                        else:
                            st.success(tr("check_email"))
                    except Exception as e:
                        st.error(f"Registrasi gagal: {str(e)}")

        show_footer()

    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("# 🎬 CLIPER AI")
    st.caption("AI Video Clipping Platform")
    st.divider()

    st.selectbox(
        tr("language"),
        ["Indonesia", "English"],
        key="language"
    )

    st.divider()
    st.markdown(f"**{tr('my_account')}**")
    st.write(st.session_state.user_email)

    if st.session_state.full_name:
        st.caption(st.session_state.full_name)

    st.divider()

    menu_items = [
        tr("dashboard"),
        tr("clipper"),
        tr("videos"),
        tr("about")
    ]

    selected = st.radio(
        tr("choose"),
        menu_items,
        key="menu_selection"
    )
    st.session_state.page = selected

    st.divider()

    if st.button(tr("logout"), use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        clear_auth()
        st.rerun()

# =========================
# DASHBOARD
# =========================
page = st.session_state.page
videos = get_user_videos()

if page == tr("dashboard"):

    st.title(f"👋 {tr('welcome')}")
    st.write(tr("subtitle"))

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(tr("total"), len(videos))
    with c2:
        st.metric(tr("active"), "ACTIVE")
    with c3:
        st.metric(tr("format"), "9:16")

    st.markdown("---")
    st.subheader(tr("quick"))

    a, b = st.columns(2)

    with a:
        st.markdown(
            f"<div class='card'><h3>🎬 AI Clipper</h3>"
            f"<p>{tr('subtitle')}</p></div>",
            unsafe_allow_html=True
        )
        if st.button(tr("start"), use_container_width=True):
            st.session_state.page = tr("clipper")
            st.rerun()

    with b:
        st.markdown(
            f"<div class='card'><h3>📁 {tr('videos')}</h3>"
            f"<p>{tr('library')}</p></div>",
            unsafe_allow_html=True
        )
        if st.button(tr("videos"), use_container_width=True):
            st.session_state.page = tr("videos")
            st.rerun()

    st.markdown("---")
    st.subheader(tr("library"))

    if videos:
        for video in videos[:3]:
            st.write(f"🎥 {video.name}")
    else:
        st.info(tr("empty"))

    show_footer()

# =========================
# AI CLIPPER
# =========================
elif page == tr("clipper"):

    st.title("🎬 AI Clipper")
    st.write(tr("subtitle"))
    st.markdown("---")

    uploaded_file = st.file_uploader(
        tr("upload"),
        type=["mp4", "mov", "mkv", "avi"],
        help=tr("video_help")
    )

    col1, col2 = st.columns(2)

    with col1:
        clip_count = st.slider(
            tr("count"), 1, 10, 5
        )

    with col2:
        duration = st.slider(
            tr("duration"), 15, 90, 45
        )

    if uploaded_file:
        st.video(uploaded_file)

        if st.button(tr("process"), use_container_width=True):
            user_folder = get_user_folder()
            run_folder = user_folder / uuid.uuid4().hex
            run_folder.mkdir(parents=True, exist_ok=True)

            suffix = Path(uploaded_file.name).suffix or ".mp4"
            input_path = run_folder / f"source{suffix}"

            try:
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(*args):
                    for item in args:
                        if isinstance(item, (int, float)):
                            progress_bar.progress(
                                max(0, min(100, int(item)))
                            )
                        elif isinstance(item, str):
                            status_text.info(item)

                with st.spinner(tr("processing")):
                    output_paths = engine.process_video(
                        str(input_path),
                        clip_count=clip_count,
                        duration=duration,
                        progress=update_progress,
                        output_dir=run_folder
                    )

                progress_bar.progress(100)
                status_text.success(tr("processing_done"))
                st.balloons()

                for path in output_paths:
                    path = Path(path)

                    if path.exists():
                        st.markdown(f"### 🎥 {path.name}")
                        st.video(str(path))

                        with open(path, "rb") as f:
                            st.download_button(
                                f"{tr('download')} - {path.name}",
                                data=f.read(),
                                file_name=path.name,
                                mime="video/mp4",
                                key=f"download_{path.name}"
                            )

            except Exception as e:
                st.error(f"{tr('processing_error')} {str(e)}")

            finally:
                try:
                    if input_path.exists():
                        input_path.unlink()
                except Exception:
                    pass

    else:
        st.info(tr("no_file"))

    show_footer()

# =========================
# VIDEO LIBRARY
# =========================
elif page == tr("videos"):

    st.title(f"📁 {tr('videos')}")
    st.write(tr("library"))
    st.markdown("---")

    videos = get_user_videos()

    if not videos:
        st.info(tr("empty"))
    else:
        for index, video in enumerate(videos):
            with st.container(border=True):
                st.markdown(f"### 🎬 {video.name}")
                st.caption(
                    time.strftime(
                        "%d-%m-%Y %H:%M",
                        time.localtime(video.stat().st_mtime)
                    )
                )

                st.video(str(video))

                with open(video, "rb") as f:
                    st.download_button(
                        tr("download"),
                        data=f.read(),
                        file_name=video.name,
                        mime="video/mp4",
                        key=f"library_download_{index}"
                    )

    show_footer()

# =========================
# ABOUT
# =========================
elif page == tr("about"):

    st.title(f"ℹ️ {tr('about_title')}")

    st.markdown(
        f"""
        <div class="card">
            <h2>🎬 CLIPER AI</h2>
            <p>{tr('description')}</p>
            <hr>
            <p><b>Features</b></p>
            <ul>
                <li>AI video moment detection</li>
                <li>Automatic subtitles</li>
                <li>Vertical 9:16 video format</li>
                <li>Personal video library</li>
                <li>Secure user authentication</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    show_footer()
