import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Sistem Operasional - Nusa Putra", layout="wide")

# ==========================================
# 2. CSS MINIMALIS (KONTRAS TINGGI)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Login Box */
    .login-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08);
        border-top: 8px solid #800000;
        margin-top: 10vh;
        text-align: center;
    }

    /* Sidebar Maroon */
    [data-testid="stSidebar"] { background-color: #800000 !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* Tombol: Kontras Font Putih di Background Maroon */
    div.stButton > button {
        background-color: #800000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Card Dashboard */
    .metric-card {
        background-color: #fcfcfc;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #eeeeee;
        border-left: 5px solid #800000;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATA & SESSION
# ==========================================
if 'db' not in st.session_state:
    st.session_state.db = {
        "OB": ["Rafi", "Budi", "Siti", "Ahmad"],
        "Area": ["Rektorat", "Laboratorium", "Perpustakaan", "Kantin"],
        "Shift": ["Pagi (07:00 - 12:00)", "Siang (13:00 - 17:00)"],
        "Penugasan": [],
        "Absensi": []
    }

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# ==========================================
# 4. HALAMAN LOGIN
# ==========================================
if not st.session_state.logged_in:
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("<h2 style='color:#800000 !important; margin-bottom:0;'>NUSA PUTRA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666 !important; font-size:12px;'>SISTEM OPERASIONAL</p>", unsafe_allow_html=True)
        
        u = st.text_input("ID User")
        p = st.text_input("Password", type="password")
        
        if st.button("MASUK"):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Gagal Login")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. DASHBOARD UTAMA
# ==========================================
else:
    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>ADMIN PANEL</h3>", unsafe_allow_html=True)
        menu = option_menu(
            menu_title=None,
            options=["Dashboard", "Data", "Plotting Tugas", "Absensi", "Keluar"],
            icons=["grid", "database", "clipboard-plus", "clock", "box-arrow-left"],
            styles={"nav-link-selected": {"background-color": "#5a0000"}}
        )

    if menu == "Dashboard":
        st.title("Ringkasan Hari Ini")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="metric-card"><h2>{len(st.session_state.db["OB"])}</h2><p>Personel OB</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><h2>{len(st.session_state.db["Penugasan"])}</h2><p>Tugas Berjalan</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><h2>{len(st.session_state.db["Absensi"])}</h2><p>Absensi Masuk</p></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Daftar Penugasan")
        if st.session_state.db["Penugasan"]:
            st.table(pd.DataFrame(st.session_state.db["Penugasan"]))
        else:
            st.info("Belum ada penugasan hari ini.")

    elif menu == "Data":
        st.title("Data")
        t1, t2, t3 = st.tabs(["Nama OB", "Lokasi Area", "Waktu Shift"])
        with t1:
            # Hanya menampilkan Nama OB sesuai permintaan
            st.table(pd.DataFrame({"Nama OB": st.session_state.db["OB"]}))
        with t2:
            st.table(pd.DataFrame({"Nama Area": st.session_state.db["Area"]}))
        with t3:
            st.table(pd.DataFrame({"Shift": st.session_state.db["Shift"]}))

    elif menu == "Plotting Tugas":
        st.title("Plotting Tugas")
        with st.form("tugas_form", clear_on_submit=True):
            ob = st.selectbox("Pilih OB", st.session_state.db["OB"])
            area = st.selectbox("Pilih Area", st.session_state.db["Area"])
            shift = st.selectbox("Pilih Shift", st.session_state.db["Shift"])
            if st.form_submit_button("Simpan Penugasan"):
                st.session_state.db["Penugasan"].append({
                    "Nama OB": ob, "Area": area, "Shift": shift, "Status": "Proses"
                })
                st.success("Tugas berhasil disimpan.")

    elif menu == "Absensi":
        st.title("Absensi")
        with st.form("absen_form", clear_on_submit=True):
            abs_ob = st.selectbox("Nama OB", st.session_state.db["OB"])
            status = st.radio("Status", ["Hadir", "Izin", "Sakit"], horizontal=True)
            if st.form_submit_button("Catat Absensi"):
                st.session_state.db["Absensi"].append({
                    "Nama OB": abs_ob, "Jam": datetime.now().strftime("%H:%M"), "Status": status
                })
                st.success("Absensi berhasil dicatat.")
        
        if st.session_state.db["Absensi"]:
            st.table(pd.DataFrame(st.session_state.db["Absensi"]))

    elif menu == "Keluar":
        st.session_state.logged_in = False
        st.rerun()