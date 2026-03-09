import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime


# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('careermatrix_pro.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT, position TEXT, status TEXT,
        salary INTEGER, date_applied TEXT, notes TEXT, last_updated TEXT)''')
   
    c.execute('''CREATE TABLE IF NOT EXISTS resume (
        id INTEGER PRIMARY KEY,
        full_name TEXT, email TEXT, phone TEXT,
        summary TEXT, experience TEXT, skills TEXT)''')
    conn.commit()
    conn.close()


def save_resume(name, email, phone, summary, exp, skills):
    conn = sqlite3.connect('careermatrix_pro.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO resume (id, full_name, email, phone, summary, experience, skills)
                 VALUES (1, ?, ?, ?, ?, ?, ?)''', (name, email, phone, summary, exp, skills))
    conn.commit()
    conn.close()


def get_resume():
    conn = sqlite3.connect('careermatrix_pro.db')
    df = pd.read_sql_query("SELECT * FROM resume WHERE id = 1", conn)
    conn.close()
    # Returns None if no resume exists, otherwise returns the Series
    return df.iloc[0] if not df.empty else None


def add_job(company, position, status, salary, date, notes):
    conn = sqlite3.connect('careermatrix_pro.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute('INSERT INTO jobs (company, position, status, salary, date_applied, notes, last_updated) VALUES (?,?,?,?,?,?,?)',
              (company, position, status, salary, str(date), notes, now))
    conn.commit()
    conn.close()


def get_jobs():
    conn = sqlite3.connect('careermatrix_pro.db')
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


# --- UI & CSS ---
st.set_page_config(page_title="CareerMatrix Elite", layout="wide", page_icon="💼")


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .resume-preview {
        background: white; color: black; padding: 30px;
        border-radius: 8px; border: 1px solid #eee;
        font-family: 'Georgia', serif; line-height: 1.5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stMetric { background: #1e2130; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)


def main():
    init_db()
    st.title("🚀 CareerMatrix Elite")


    tab1, tab2 = st.tabs(["📊 Job Matrix", "📄 Resume Builder"])


    # --- TAB 1: JOB TRACKER ---
    with tab1:
        with st.sidebar:
            st.header("New Application")
            with st.form("job_form", clear_on_submit=True):
                c_name = st.text_input("Company")
                p_name = st.text_input("Role")
                stat = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected"])
                sal = st.number_input("Salary ($)", value=0)
                date = st.date_input("Applied Date")
                note = st.text_area("Notes")
                if st.form_submit_button("Sync to Matrix"):
                    if c_name and p_name:
                        add_job(c_name, p_name, stat, sal, date, note)
                        st.rerun()


        df = get_jobs()
        if not df.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Apps", len(df))
            m2.metric("Interviews", len(df[df['status'] == 'Interviewing']))
            m3.metric("Offers", len(df[df['status'] == 'Offer']))
            st.dataframe(df.sort_values(by='id', ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No job data found. Add your first application!")


    # --- TAB 2: RESUME BUILDER ---
    with tab2:
        res_data = get_resume()
       
        # FIXED LOGIC: Explicitly checking if res_data is not None
        has_data = res_data is not None
       
        col_ed, col_pre = st.columns([1, 1])
       
        with col_ed:
            st.subheader("Edit Profile")
            with st.form("resume_form"):
                r_name = st.text_input("Full Name", value=res_data['full_name'] if has_data else "")
                r_email = st.text_input("Email", value=res_data['email'] if has_data else "")
                r_phone = st.text_input("Phone", value=res_data['phone'] if has_data else "")
                r_summary = st.text_area("Summary", value=res_data['summary'] if has_data else "", height=100)
                r_exp = st.text_area("Experience", value=res_data['experience'] if has_data else "", height=150)
                r_skills = st.text_area("Skills", value=res_data['skills'] if has_data else "", height=80)
               
                if st.form_submit_button("💾 Save Profile"):
                    save_resume(r_name, r_email, r_phone, r_summary, r_exp, r_skills)
                    st.success("Profile Saved!")
                    st.rerun()


        with col_pre:
            st.subheader("Document Preview")
            if r_name:
                resume_html = f"""
                <div class="resume-preview" id="resume-print">
                    <h1 style="text-align:center; border-bottom: 2px solid #333;">{r_name}</h1>
                    <p style="text-align:center;">{r_email} | {r_phone}</p>
                    <h4>Professional Summary</h4>
                    <p>{r_summary}</p>
                    <h4>Experience</h4>
                    <p style="white-space: pre-line;">{r_exp}</p>
                    <h4>Technical Skills</h4>
                    <p>{r_skills}</p>
                </div>
                """
                st.markdown(resume_html, unsafe_allow_html=True)
               
                # Bonus: Print/Save Button
                st.button("🖨️ Print to PDF (Ctrl+P)", on_click=lambda: st.write("Tip: Use your browser's print feature to save as PDF!"))
            else:
                st.warning("Enter your name to generate preview.")


if __name__ == "__main__":
    main()
