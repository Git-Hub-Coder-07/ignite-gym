import streamlit as st
import pandas as pd
import sqlite3
import datetime
import qrcode
from io import BytesIO
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="IGNITE GYM & DEADLIFT",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI Styling
st.markdown("""
<style>
    .main-title { font-size: 45px; font-weight: 800; color: #FF4B4B; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 20px; text-align: center; color: #555555; margin-bottom: 30px; }
    .section-header { font-size: 28px; font-weight: 700; border-bottom: 2px solid #FF4B4B; padding-bottom: 5px; margin-top: 20px; margin-bottom: 15px; }
    .feature-card { padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE INITIALIZATION ENGINE
# ==========================================
DB_FILE = "ignite_gym.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            plan_name TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            join_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            payment_status TEXT DEFAULT 'Paid'
        )
    """)
    # Create text content tables for Blog / Offers if needed dynamically
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500", use_container_width=True)
st.sidebar.title("IGNITE GYM & DEADLIFT")
st.sidebar.markdown("*Forge Your Ultimate Version*")

navigation = st.sidebar.radio(
    "Navigate Website",
    [
        "🏠 Homepage", 
        "ℹ️ About & Gallery", 
        "📅 Schedule & Trainers", 
        "💳 Membership & Pricing", 
        "📢 Offers & Blog", 
        "📞 Contact & FAQ", 
        "🔒 Admin Panel"
    ]
)

# Membership Plan Details Configuration
PLANS = {
    "Monthly Plan": {"price": 800, "days": 30, "desc": "Access to all gym equipment & locker facilities."},
    "Quarterly Plan": {"price": 2000, "days": 90, "desc": "Access to gym + 2 sessions with general fitness trainer."},
    "Annual Plan": {"price": 7000, "days": 365, "desc": "Full year access + Personalized Diet Blueprint + Core Deadlift coaching."}
}

# ==========================================
# 4. PAGE IMPLEMENTATIONS
# ==========================================

# --- HOMEPAGE ---
if navigation == "🏠 Homepage":
    st.markdown("<div class='main-title'>IGNITE GYM & DEADLIFT</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The Premier Strength & Conditioning Facility in Town</div>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1540206351-d6465b3ac5c1?w=1200", use_container_width=True, caption="Welcome to the Zone of Iron")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><h3>🔥 High Intensity</h3>Top-tier heavy lifting equipment and dedicated deadlift platforms optimized for maximum output.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><h3>💪 Expert Coaching</h3>Certified strength coaches ready to refine your execution mechanics and prevent performance plateaus.</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><h3>⏰ Flexible Access</h3>Open 5:00 AM to 10:00 PM, structured seamlessly around your demanding work or academic schedules.</div>", unsafe_allow_html=True)

# --- ABOUT & GALLERY ---
elif navigation == "ℹ️ About & Gallery":
    st.markdown("<div class='section-header'>About Our Philosophy</div>", unsafe_allow_html=True)
    st.write(
        "Founded on the principles of raw effort and scientific recovery, IGNITE GYM & DEADLIFT caters "
        "to individuals looking to break personal records and achieve peak metabolic conditioning. "
        "Whether you are preparing for a powerlifting meet or initializing your wellness roadmap, we provide the ultimate ecosystem."
    )
    
    st.markdown("<div class='section-header'>Facility Gallery</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600", caption="Cardio & Performance Analytics Deck", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1571731956622-f1c87e487950?w=600", caption="Premium Powerlifting Platforms", use_container_width=True)

# --- SCHEDULE & TRAINERS ---
elif navigation == "📅 Schedule & Trainers":
    st.markdown("<div class='section-header'>Weekly Operational Schedule</div>", unsafe_allow_html=True)
    schedule_data = {
        "Days": ["Monday - Saturday", "Sunday"],
        "Morning Slots": ["05:00 AM - 11:00 AM", "06:00 AM - 10:00 AM"],
        "Evening Slots": ["04:00 PM - 10:00 PM", "Closed"]
    }
    st.table(pd.DataFrame(schedule_data))
    
    st.markdown("<div class='section-header'>Our Elite Training Staff</div>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.image("https://images.unsplash.com/photo-1567013127542-490d757e51fc?w=300", width=150)
        st.markdown("#### Coach Vikram Singh\n*Specialization: Competitive Powerlifting & Hypertrophy Optimization*")
    with t_col2:
        st.image("https://images.unsplash.com/photo-1548690312-e3b507d8c110?w=300", width=150)
        st.markdown("#### Coach Anjali Sharma\n*Specialization: Kinesiology & High-Intensity Metabolic Conditioning*")

# --- MEMBERSHIP & PRICING (WITH REGISTRATION & QR PAYMENT) ---
elif navigation == "💳 Membership & Pricing":
    st.markdown("<div class='section-header'>Select Your Access Architecture</div>", unsafe_allow_html=True)
    
    # Render Plan Options
    p_cols = st.columns(3)
    idx = 0
    for plan_name, details in PLANS.items():
        with p_cols[idx]:
            st.markdown(f"### {plan_name}")
            st.markdown(f"## **₹{details['price']:,}**")
            st.write(details['desc'])
            st.caption(f"Valid for {details['days']} calendar days")
        idx += 1
        
    st.markdown("<div class='section-header'>Instant Registration & Payment Pipeline</div>", unsafe_allow_html=True)
    
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("Full Name *")
        phone = st.text_input("Mobile Number (10 digits) *")
        email = st.text_input("Email Address")
        selected_plan = st.selectbox("Choose Your Membership Plan", list(PLANS.keys()))
        
        st.markdown("### Payment Step")
        price = PLANS[selected_plan]["price"]
        st.info(f"Amount Payable: **₹{price:,}**")
        
        # Dynamic UPI QR Code Generation using India's Universal Protocol
        # Replace 'ignitegym@upi' with actual registered merchant UPI ID
        upi_string = f"upi://pay?pa=ignitegym@okaxis&pn=IGNITE%20GYM%20AND%20DEADLIFT&am={price}&cu=INR"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(upi_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption="Scan this Dynamic QR using GPay, PhonePe, or Paytm to initiate Transfer.", width=250)
        
        submitted = st.form_submit_form_button("Submit Registration After Completing Payment")
        
        if submitted:
            if not name or not phone:
                st.error("Please provide both Name and Mobile Number to initialize registration.")
            else:
                # Calculations for calendar intervals
                j_date = datetime.date.today()
                exp_date = j_date + datetime.timedelta(days=PLANS[selected_plan]["days"])
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO members (name, phone, email, plan_name, amount_paid, join_date, expiry_date, payment_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, phone, email, selected_plan, price, j_date.strftime("%Y-%m-%d"), exp_date.strftime("%Y-%m-%d"), "Paid"))
                conn.commit()
                conn.close()
                
                st.success(f"💥 Welcome to the family, {name}! Your registration for the {selected_plan} has been successfully saved. Welcome to IGNITE GYM & DEADLIFT!")

# --- OFFERS & BLOG ---
elif navigation == "📢 Offers & Blog":
    st.markdown("<div class='section-header'>Current Promotional Offers</div>", unsafe_allow_html=True)
    st.success("🎉 **Monsoon Deadlift Special:** Sign up for the Annual Plan this week and receive a complimentary pair of heavy-duty lifting straps + premium shaker bottle!")
    
    st.markdown("<div class='section-header'>Ignite Educational Log (Blog)</div>", unsafe_allow_html=True)
    st.markdown("""
    #### 🏋️‍♂️ 1. The Critical Role of Latissimus Dorsi Activation in Deadlifts
    *Published by Coach Vikram* Many lifters treat the deadlift as purely a leg movement. By intentionally engaging your lats before pulling, you keep the barbell close to your center of gravity, drastically mitigating spinal shear force.
    
    #### 🥗 2. Structural Meal Compounding for Accelerated Muscle Hypertrophy
    *Published by Coach Anjali* To sustain clean mass growth, ensure a daily surplus of 300 calories, prioritizing a distribution threshold of 2.0g of protein per kilogram of body weight.
    """)

# --- CONTACT & FAQ ---
elif navigation == "📞 Contact & FAQ":
    st.markdown("<div class='section-header'>Contact Interface</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📍 Facility Address:** Plot 42, Strength Zone Layout, Sector 7,  
        Near Metro Pillar 104, New Delhi, India  
        
        **📧 Communication channels:** * **Support Email:** contact@ignitegym.in  
        * **Hotline:** +91 98765 43210  
        """)
    with col2:
        st.markdown("**🌐 Social Networks:**")
        st.markdown("[📸 Instagram](https://instagram.com) | [🎥 YouTube](https://youtube.com) | [📘 Facebook](https://facebook.com)")

    st.markdown("<div class='section-header'>Frequently Asked Questions (FAQ)</div>", unsafe_allow_html=True)
    with st.expander("Is clean drinking water and locker storage provided?"):
        st.write("Yes, fully purified water systems and individual electronic safety lockers are included across all membership packages.")
    with st.expander("Can beginners join without prior powerlifting exposure?"):
        st.write("Absolutely. Every member receives a comprehensive machinery familiarization program on Day 1 to ensure standard safety protocols.")

# ==========================================
# 5. SECURE ADMIN CONTROLLER PANEL
# ==========================================
elif navigation == "🔒 Admin Panel":
    st.markdown("<div class='section-header'>Secure Administration Console</div>", unsafe_allow_html=True)
    
    # Password Protection Input Check
    # For Production environments, pass management data securely via streamlit secrets
    admin_password = st.text_input("Provide Administrative Password Keys", type="password")
    
    if admin_password == "IgniteAdmin2026":
        st.success("Access Authorization Granted.")
        
        # Pull latest metrics from db
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM members", conn)
        conn.close()
        
        # ----------------------------------------------------
        # TAB 1: CRITICAL TRACKING - EXPIRES IN NEXT 4 DAYS
        # ----------------------------------------------------
        st.markdown("### ⚠️ Critical Membership Expiration Watch (Next 4 Days)")
        
        if not df.empty:
            df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.date
            today = datetime.date.today()
            four_days_hence = today + datetime.timedelta(days=4)
            
            # Filter condition logic
            expiring_filter = (df['expiry_date'] >= today) & (df['expiry_date'] <= four_days_hence)
            df_expiring = df[expiring_filter].copy()
            
            if not df_expiring.empty:
                df_expiring['Days Left'] = df_expiring['expiry_date'].apply(lambda x: (x - today).days)
                st.warning(f"Found {len(df_expiring)} membership(s) terminating within the next 96 hours.")
                st.dataframe(df_expiring[['id', 'name', 'phone', 'plan_name', 'expiry_date', 'Days Left']], use_container_width=True)
            else:
                st.info("No memberships are scheduled to lapse within the upcoming 4 days.")
        else:
            st.info("No registration records exist in the structural tables.")
            
        st.markdown("---")
        
        # Layout splitting operations for Management
        adm_tabs = st.tabs(["📋 View & Edit Member Base", "➕ Manual Registration Override"])
        
        # TAB: VIEW & EDIT BASE
        with adm_tabs[0]:
            if not df.empty:
                st.write("#### Master Membership Matrix")
                st.caption("Tip: You can edit values directly within the table grid below. Double click cells to update, then click the Save updates button.")
                
                # Streamlit Data Editor implementation for live row mutations
                edited_df = st.data_editor(df, num_rows="dynamic", key="member_editor", use_container_width=True)
                
                if st.button("Save Live Table Modifications"):
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        # Wipe out current matrix completely to write cleanly updated frame state
                        cursor.execute("DELETE FROM members")
                        for idx, row in edited_df.iterrows():
                            # Re-insert processed frame collection payload
                            cursor.execute("""
                                INSERT INTO members (id, name, phone, email, plan_name, amount_paid, join_date, expiry_date, payment_status)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (row['id'], row['name'], row['phone'], row['email'], row['plan_name'], row['amount_paid'], str(row['join_date']), str(row['expiry_date']), row['payment_status']))
                        conn.commit()
                        conn.close()
                        st.success("System Database Matrix refreshed successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Execution Halt Error encountered during saving sequence: {e}")
            else:
                st.info("No active records found inside the primary table.")
                
        # TAB: MANUAL REGISTRATION OVERRIDE
        with adm_tabs[1]:
            st.write("#### Direct Administrative Entry")
            with st.form("admin_manual_form"):
                m_name = st.text_input("Name")
                m_phone = st.text_input("Phone Contact")
                m_email = st.text_input("Email")
                m_plan = st.selectbox("Assign Access Tier Plan", list(PLANS.keys()))
                m_amt = st.number_input("Adjust Custom Price Applied (₹)", value=float(PLANS[m_plan]["price"]))
                m_join = st.date_input("Registration Inception Effective Date", datetime.date.today())
                m_exp = st.date_input("Membership Scheduled Termination Date", datetime.date.today() + datetime.timedelta(days=PLANS[m_plan]["days"]))
                
                manual_submit = st.form_submit_button("Force Record Injection")
                
                if manual_submit:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO members (name, phone, email, plan_name, amount_paid, join_date, expiry_date, payment_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'Paid')
                    """, (m_name, m_phone, m_email, m_plan, m_amt, m_join.strftime("%Y-%m-%d"), m_exp.strftime("%Y-%m-%d")))
                    conn.commit()
                    conn.close()
                    st.success(f"Manually injected record entry successfully for: {m_name}")
                    st.rerun()
                    
    elif admin_password != "":
        st.error("Invalid Administrative Credentials Key Provided. Access System Blocked.")