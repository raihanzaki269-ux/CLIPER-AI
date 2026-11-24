import streamlit as st
import tempfile
import uuid
from pathlib import Path
from supabase import create_client
import engine

# =========================
# APP CONFIGURATION
# =========================
st.set_page_config(
    page_title="CLIPER AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

SITE_URL = "https://cliper-ai-alfymantduy3dpvahsapppx.streamlit.app/"

# =========================
# SESSION STATE
# =========================
defaults = {
    "language": "Indonesia",
    "access_token": None,
    "refresh_token": None,
    "user": None,
    "latest_outputs": [],
    "auth_page": "Login",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# LANGUAGE
# =========================
LANG = {
    "Indonesia": {
        "login": "Masuk",
        "register": "Daftar Akun",
        "logout": "Keluar",
        "email": "Alamat Email",
        "password": "Kata Sandi",
        "full_name": "Nama Lengkap",
        "login_title": "Masuk ke CLIPER AI",
        "register_title": "Buat Akun CLIPER AI",
        "login_button": "Masuk",
        "register_button": "Daftar Sekarang",
        "no_account": "Belum punya akun?",
        "have_account": "Sudah punya akun?",
        "check_email": "Pendaftaran berhasil. Silakan cek email untuk verifikasi akun sebelum login.",
        "login_success": "Berhasil masuk!",
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "library": "Hasil Video",
        "about": "Tentang",
        "welcome": "SELAMAT DATANG DI WORKSPACE ANDA",
        "headline": "Buat Lebih Banyak. Edit Lebih Sedikit.",
        "total": "Total Video Clip",
        "subtitle": "Subtitle Otomatis",
        "format": "Format Video",
        "quick": "Akses Cepat",
        "create": "Buat Clip Baru",
        "my_videos": "Video Saya",
        "upload": "Upload Video",
        "clip_count": "Jumlah Clip",
        "duration": "Durasi Setiap Clip (detik)",
        "process": "Mulai Proses AI",
        "processing": "AI sedang menganalisis video. Mohon tunggu...",
        "done": "Proses selesai!",
        "download": "Download Video",
        "preview": "Preview Video",
        "empty": "Belum ada video. Silakan buat clip terlebih dahulu.",
        "about_text": "CLIPER AI adalah aplikasi pemotong video otomatis berbasis AI.",
        "account": "Akun",
        "language": "Bahasa",
        "login_error": "Email atau kata sandi salah. Silakan coba lagi.",
        "signup_error": "Pendaftaran gagal. Periksa kembali data Anda.",
        "auth_error": "Tidak dapat terhubung ke layanan akun. Periksa konfigurasi Secrets.",
        "processing_error": "Terjadi kesalahan saat memproses video.",
        "name_required": "Nama lengkap wajib diisi.",
        "email_required": "Email wajib diisi.",
        "password_required": "Kata sandi minimal 6 karakter.",
        "file_type": "Silakan upload file video MP4, MOV, atau MKV.",
        "file_help": "Format yang didukung: MP4, MOV, MKV",
        "profile": "Profil Pengguna",
        "storage_note": "Catatan: video saat ini disimpan sementara di server aplikasi. Video dapat hilang ketika server dimulai ulang.",
    },
    "English": {
        "login": "Login",
        "register": "Create Account",
        "logout": "Logout",
        "email": "Email Address",
        "password": "Password",
        "full_name": "Full Name",
        "login_title": "Login to CLIPER AI",
        "register_title": "Create Your CLIPER AI Account",
        "login_button": "Login",
        "register_button": "Create Account",
        "no_account": "Don't have an account?",
        "have_account": "Already have an account?",
        "check_email": "Registration successful. Please check your email to verify your account before logging in.",
        "login_success": "Successfully logged in!",
        "dashboard": "Dashboard",
        "clipper": "AI Clipper",
        "library": "My Videos",
        "about": "About",
        "welcome": "WELCOME TO YOUR WORKSPACE",
        "headline": "Create More. Edit Less.",
        "total": "Total Video Clips",
        "subtitle": "Auto Subtitles",
        "format": "Video Format",
        "quick": "Quick Access",
        "create": "Create New Clip",
        "my_videos": "My Videos",
        "upload": "Upload Video",
        "clip_count": "Number of Clips",
        "duration": "Clip Duration (seconds)",
        "process": "Start AI Processing",
        "processing": "AI is analyzing your video. Please wait...",
        "done": "Processing completed!",
        "download": "Download Video",
        "preview": "Video Preview",
        "empty": "No videos yet. Create your first clip.",
        "about_text": "CLIPER AI is an AI-powered automatic video clipping application.",
        "account": "Account",
        "language": "Language",
        "login_error": "Incorrect email or password. Please try again.",
        "signup_error": "Registration failed. Please check your information.",
        "auth_error": "Unable to connect to the account service. Check your Secrets configuration.",
        "processing_error": "An error occurred while processing the video.",
        "name_required": "Full name is required.",
        "email_required": "Email is required.",
        "password_required": "Password must contain at least 6 characters.",
        "file_type": "Please upload an MP4, MOV, or MKV video.",
        "file_help": "Supported formats: MP4, MOV, MKV",
        "profile": "User Profile",
        "storage_note": "Note: videos are currently stored temporarily on the app server. They may disappear when the server restarts.",
    }
}

def tr(key):
    return LANG[st.session_state.language][key]

# =========================
# SUPABASE CONNECTION
# =========================
@st.cache_resource
def get_supabase_config():
    return {
        "url": st.secrets["supabase"]["url"],
        "key": st.secrets["supabase"]["publishable_key"],
    }

try:
    config = get_supabase_config()
    supabase = create_client(config["url"], config["key"])
except Exception:
    st.error("Supabase configuration error. Please check Streamlit Secrets.")
    st.stop()

# Restore the user's session on each rerun.
if (
    st.session_state.access_token
    and st.session_state.refresh_token
    and st.session_state.user is None
):
    try:
        auth_response = supabase.auth.set_session(
            st.session_state.access_token,
            st.session_state.refresh_token
        )
        st.session_state.user = auth_response.user
        if auth_response.session:
            st.session_state.access_token = auth_response.session.access_token
            st.session_state.refresh_token = auth_response.session.refresh_token
    except Exception:
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.user = None

# =========================
# DARK PROFESSIONAL STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: #080d18;
    color: #f1f5f9;
}
[data-testid="stSidebar"] {
    background: #101827;
    border-right: 1px solid #263247;
}
.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}
h1, h2, h3 {
    color: #f8fafc;
}
p, label, span {
    color: #cbd5e1;
}
div[data-testid="stMetric"] {
    background: #111c2e;
    border: 1px solid #263750;
    padding: 18px;
    border-radius: 14px;
}
.stButton > button {
    background: #2563eb;
    color: white;
    border: 0;
    border-radius: 9px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}
.stButton > button:hover {
    background: #1d4ed8;
    color: white;
}
div[data-testid="stFileUploader"] {
    background: #111c2e;
    border: 1px dashed #3b4d68;
    border-radius: 12px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# AUTHENTICATION PAGE
# =========================
def show_auth():
    st.markdown("<h1 style='text-align:center'>🎬 CLIPER AI</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#94a3b8'>INTELLIGENT VIDEO CLIPPING</p>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.3, 1])

    with center:
        st.selectbox(
            tr("language"),
            ["Indonesia", "English"],
            key="language"
        )

        st.markdown("---")

        auth_choice = st.radio(
            "Account",
            [tr("login"), tr("register")],
            horizontal=True,
            label_visibility="collapsed"
        )

        if auth_choice == tr("login"):
            st.subheader(tr("login_title"))

            with st.form("login_form"):
                email = st.text_input(tr("email"))
                password = st.text_input(tr("password"), type="password")
                submitted = st.form_submit_button(
                    tr("login_button"),
                    use_container_width=True
                )

            if submitted:
                if not email.strip():
                    st.warning(tr("email_required"))
                elif not password:
                    st.warning(tr("password_required"))
                else:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email.strip(),
                            "password": password
                        })

                        if response.session:
                            st.session_state.access_token = response.session.access_token
                            st.session_state.refresh_token = response.session.refresh_token
                            st.session_state.user = response.user
                            st.session_state.latest_outputs = []
                            st.success(tr("login_success"))
                            st.rerun()
                        else:
                            st.error(tr("login_error"))
                    except Exception:
                        st.error(tr("login_error"))

        else:
            st.subheader(tr("register_title"))

            with st.form("register_form"):
                full_name = st.text_input(tr("full_name"))
                email = st.text_input(tr("email"))
                password = st.text_input(tr("password"), type="password")
                submitted = st.form_submit_button(
                    tr("register_button"),
                    use_container_width=True
                )

            if submitted:
                if not full_name.strip():
                    st.warning(tr("name_required"))
                elif not email.strip():
                    st.warning(tr("email_required"))
                elif len(password) < 6:
                    st.warning(tr("password_required"))
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {"full_name": full_name.strip()},
                                "email_redirect_to": SITE_URL
                            }
                        })

                        if response.session:
                            st.session_state.access_token = response.session.access_token
                            st.session_state.refresh_token = response.session.refresh_token
                            st.session_state.user = response.user
                            st.success(tr("login_success"))
                            st.rerun()
                        else:
                            st.success(tr("check_email"))
                    except Exception:
                        st.error(tr("signup_error"))

        st.markdown("---")
        st.caption("CLIPER AI © 2026")

# =========================
# LOGIN GATE
# =========================
if st.session_state.user is None:
    show_auth()
    st.stop()

user = st.session_state.user
user_id = str(user.id)

# Every user gets a separate folder.
USER_ROOT = RESULTS / user_id
USER_ROOT.mkdir(parents=True, exist_ok=True)

def get_user_videos():
    videos = list(USER_ROOT.glob("*/*_FINAL.mp4"))
    videos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return videos

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("# 🎬 CLIPER AI")
    st.caption("INTELLIGENT VIDEO CLIPPING")
    st.divider()

    st.selectbox(
        tr("language"),
        ["Indonesia", "English"],
        key="language"
    )

    pages = [
        tr("dashboard"),
        tr("clipper"),
        tr("library"),
        tr("about")
    ]

    page = st.radio("MENU", pages, label_visibility="collapsed")

    st.divider()
    st.caption(tr("profile"))
    st.write(user.email or "User")

    if st.button(tr("logout"), use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.user = None
        st.session_state.latest_outputs = []
        st.rerun()

# =========================
# DASHBOARD
# =========================
if page == tr("dashboard"):
    videos = get_user_videos()

    st.caption(tr("welcome"))
    st.title(tr("headline"))
    st.write("CLIPER AI — Your personal AI video workspace.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(tr("total"), len(videos))
    with col2:
        st.metric(tr("subtitle"), "ACTIVE")
    with col3:
        st.metric(tr("format"), "9:16")

    st.markdown("---")
    st.subheader(tr("quick"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎬 AI Clipper")
        st.write("Automatically find interesting moments and create short videos.")
        if st.button(tr("create"), use_container_width=True):
            st.session_state["go_to_clipper"] = True
            st.rerun()

    with col2:
        st.markdown("### 📁 " + tr("my_videos"))
        st.write("View and download your processed clips.")
        if st.button(tr("my_videos"), use_container_width=True):
            st.session_state["go_to_library"] = True
            st.rerun()

    st.caption(tr("storage_note"))

# =========================
# AI CLIPPER
# =========================
elif page == tr("clipper") or st.session_state.get("go_to_clipper", False):
    st.session_state["go_to_clipper"] = False

    st.title("🎬 AI Clipper")
    st.write("Upload a long video and let AI find interesting moments.")

    uploaded_file = st.file_uploader(
        tr("upload"),
        type=["mp4", "mov", "mkv"],
        help=tr("file_help")
    )

    col1, col2 = st.columns(2)

    with col1:
        clip_count = st.number_input(
            tr("clip_count"),
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )

    with col2:
        duration = st.number_input(
            tr("duration"),
            min_value=15,
            max_value=90,
            value=45,
            step=5
        )

    if uploaded_file is not None:
        st.video(uploaded_file)

        if st.button(tr("process"), use_container_width=True):
            extension = Path(uploaded_file.name).suffix.lower()

            if extension not in [".mp4", ".mov", ".mkv"]:
                st.error(tr("file_type"))
            else:
                run_dir = USER_ROOT / uuid.uuid4().hex
                run_dir.mkdir(parents=True, exist_ok=True)
                input_path = run_dir / f"uploaded_video{extension}"

                try:
                    with open(input_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    with st.spinner(tr("processing")):
                        output_paths = engine.process_video(
                            str(input_path),
                            clip_count=int(clip_count),
                            duration=int(duration),
                            output_dir=str(run_dir)
                        )

                    st.session_state.latest_outputs = [
                        str(p) for p in output_paths
                    ]

                    st.success(tr("done"))

                except Exception as error:
                    st.error(tr("processing_error"))
                    st.exception(error)

                finally:
                    try:
                        if input_path.exists():
                            input_path.unlink()
                    except Exception:
                        pass

    # Show the latest clips from this user's session.
    latest = [
        Path(p) for p in st.session_state.latest_outputs
        if Path(p).exists() and USER_ROOT in Path(p).parents
    ]

    if latest:
        st.markdown("---")
        st.subheader("🎉 " + tr("done"))

        for index, video_path in enumerate(latest, start=1):
            st.markdown(f"### Clip {index}")
            st.video(str(video_path))

            with open(video_path, "rb") as video_file:
                st.download_button(
                    label=f"{tr('download')} {index}",
                    data=video_file.read(),
                    file_name=video_path.name,
                    mime="video/mp4",
                    key=f"download_latest_{index}"
                )

# =========================
# VIDEO LIBRARY
# =========================
elif page == tr("library") or st.session_state.get("go_to_library", False):
    st.session_state["go_to_library"] = False

    st.title("📁 " + tr("library"))

    videos = get_user_videos()

    if not videos:
        st.info(tr("empty"))
    else:
        st.write(f"{len(videos)} video clip(s)")

        for index, video_path in enumerate(videos, start=1):
            with st.container():
                st.markdown(f"### Clip {index}")
                st.video(str(video_path))

                with open(video_path, "rb") as video_file:
                    st.download_button(
                        tr("download"),
                        data=video_file.read(),
                        file_name=video_path.name,
                        mime="video/mp4",
                        key=f"library_download_{index}"
                    )

                st.divider()

    st.caption(tr("storage_note"))

# =========================
# ABOUT
# =========================
elif page == tr("about"):
    st.title("ℹ️ " + tr("about"))
    st.markdown("## CLIPER AI")
    st.write(tr("about_text"))

    st.markdown("""
    ### Features
    - AI-powered video moment detection
    - Automatic short video creation
    - Word-by-word subtitles
    - Vertical video format (9:16)
    - Personal user accounts
    - Indonesian and English interface
    """)

    st.caption("Created with Streamlit and AI technology.")
