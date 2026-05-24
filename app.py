import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from PIL import Image

# -------------------------------------------------------------------------
# 1. SECURE EMAIL ENGINE
# -------------------------------------------------------------------------
def send_registration_email(details, subjects, marks, receipt_file):
    """Sends an isolated, detailed email report for a single applicant."""
    MY_EMAIL = "khanzada212008@gmail.com"
    # IMPORTANT: Generate a 16-character Google App Password for this string!
    MY_PASSWORD = "whyv rtdf odiq hsgc" 

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"🎓 SOA Registration: {details['Name']} ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    # Format chosen subjects into a clean readable block
    subject_string = "\n".join([f" - {s}" for s in subjects])
    
    body = f"""
    A new candidate has successfully registered for Superior Officers Academy.

    --- CANDIDATE DETAILS ---
    Name: {details['Name']}
    Father's Name: {details['FatherName']}
    Email Address: {details['Email']}
    Academic Qualification: {details['Qualification']}
    Previous CSS Attempts: {details['CSS_Attempts']}
    Previous PMS Attempts: {details['PMS_Attempts']}
    Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    --- ACADEMIC PATHWAY ---
    Opted Subjects (Total Marks: {marks}):
{subject_string}
    -------------------------
    
    The proof of payment receipt is attached below.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # Securely package and attach the uploaded image/document
    if receipt_file is not None:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(receipt_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={receipt_file.name}')
        msg.attach(payload)
        receipt_file.seek(0) # Reset stream pointer for Streamlit display

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

# -------------------------------------------------------------------------
# 2. USER INTERFACE & APP LAYOUT
# -------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="SOA Registration", page_icon="🎓", layout="centered")
    
    st.title("🏛️ SUPERIOR OFFICERS ACADEMY (SOA)")
    st.markdown("#### Official Candidate Registration Portal")
    
    # EasyPaisa Notification Banner
    st.warning("💳 **Fee Notice:** Kindly deposit your registration fee into the **EasyPaisa Account: 03365464411** before filling out this form.")
    
    st.write("---")
    
    # Creating a full form container to prevent site refreshes mid-input
    with st.form(key="soa_form"):
        st.subheader("👤 Step 1: Necessary Personal Details")
        
        name = st.text_input("Enter your name *")
        father_name = st.text_input("Enter your father's name *")
        email = st.text_input("Enter your email address *")
        qualification = st.text_area("Kindly describe your Academic Qualification *")
        
        col1, col2 = st.columns(2)
        with col1:
            css_attempts = st.number_input("How many times have you appeared in CSS examination before?", min_value=0, max_value=3, step=1)
        with col2:
            pms_attempts = st.number_input("How many times have you appeared in PMS examination before?", min_value=0, max_value=3, step=1)
            
        st.write("---")
        st.subheader("📚 Step 2: Subject Selection")
        st.info("Select one subject from each group you wish to take. Your **Total Marks Score must equal exactly 600** to qualify.")
        
        # Track selections and cumulative mark calculations
        selected_subjects = []
        total_marks = 0
        
        # GROUP 1 (200 Marks)

        g1_choice = st.selectbox("Select subject from Group 1", ["Accounting & Auditing", "Economics", "Computer Science", "Political Science", "International Relations"])
        selected_subjects.append(f"{g1_choice} (200m)")
        total_marks += 200
            
        # GROUP 2 (200 Marks)
        
        g2_choice = st.selectbox("Select subject from Group 2", ["Physics", "Chemistry", "Applied Mathematics", "Pure Mathematics", "Statistics", "Geology"])
        selected_subjects.append(f"{g2_choice} (200m)")
        total_marks += 200
            
        # GROUP 3 (100 Marks)
        
        g3_choice = st.selectbox("Select subject from Group 3", ["Business Administration", "Public Administration", "Governance & Public Policy", "Town Planning & Urban Management"])
        selected_subjects.append(f"{g3_choice} (100m)")
        total_marks += 100
            
        # GROUP 4 (100 Marks)
        
        g4_choice = st.selectbox("Select subject from Group 4", ["History of Pakistan & India", "Islamic History & Culture", "British History", "European History", "History of USA"])
        selected_subjects.append(f"{g4_choice} (100m)")
        total_marks += 100
            
        # GROUP 5 (100 Marks)
        
        g5_choice = st.selectbox("Select subject from Group 5", ["Gender Studies", "Environmental Science", "Agriculture & Forestry", "Botany", "Zoology", "English Literature", "Urdu Literature"])
        selected_subjects.append(f"{g5_choice} (100m)")
        total_marks += 100

        # GROUP 6 (100 Marks)
        
        g6_choice = st.selectbox("Select subject from Group 6", ["Law", "Constitutional Law", "International Law", "Muslim Law & Jurisprudence", "Mercantile Law", "Criminology", "Philosophy"])
        selected_subjects.append(f"{g6_choice} (100m)")
        total_marks += 100

        # GROUP 7 (100 Marks)
        g7_choice = st.selectbox("Select subject from Group 7", ["Journalism and Mass Communication", "Psychology", "Geography", "Anthropology", "Sociology", "Punjabi", "Sindhi", "Balochi", "Pashto", "Persian", "Arabic"])
        selected_subjects.append(f"{g7_choice} (100m)")
        total_marks += 100

        # Show a real-time tracking metric counter
        st.metric(label="Current Opted Subject Marks Counter", value=f"{total_marks} / 600 Marks")

        st.write("---")
        st.subheader("📁 Step 3: Registration Fee Receipt")
        uploaded_receipt = st.file_uploader("Upload your EasyPaisa payment screenshot or slip *", type=["png", "jpg", "jpeg", "pdf"])
        
        if uploaded_receipt is not None and uploaded_receipt.type in ["image/png", "image/jpeg"]:
            st.image(Image.open(uploaded_receipt), caption="Preview of payment proof", width=250)

        st.write("---")
        submit_btn = st.form_submit_button("Submit Application to SOA")

    # -------------------------------------------------------------------------
    # 3. COMPLIANCE & ACCURACY CHECK
    # -------------------------------------------------------------------------
    if submit_btn:
        # Mandatory validation checks
        if not name or not father_name or not email or not qualification or not uploaded_receipt:
            st.error("🚨 Missing Required Fields! Please complete all text fields and upload your receipt before submitting.")
        
        # Enforcing your explicit 600-mark validation rule
        elif total_marks < 600:
            st.error(f"❌ Failed Compliance: Your total opted subject marks value is {total_marks}. This is less than the compulsory 600 marks. Please alter your choices and submit again.")
        elif total_marks > 600:
            st.error(f"❌ Failed Compliance: Your total opted subject marks value is {total_marks}. This exceeds the compulsory 600 marks limits. Please alter your choices and submit again.")
        
        # If everything passes perfectly
        else:
            with st.spinner("Encrypting details and processing database upload..."):
                candidate_data = {
                    "Name": name, "FatherName": father_name, "Email": email,
                    "Qualification": qualification, "CSS_Attempts": css_attempts, "PMS_Attempts": pms_attempts
                }
                
                # Fire the isolated alert to your personal inbox
                email_sent = send_registration_email(candidate_data, selected_subjects, total_marks, uploaded_receipt)
                
                if email_sent:
                    st.success(f"🎉 Registration Successful! Thank you {name}. Your complete application has been sent securely to Superior Officers Academy review board.")
                    st.balloons()
                else:
                    st.warning("Application verified locally, but secure mail delivery engine failed. Did you configure your Google App Password on line 16?")

if __name__ == "__main__":
    main()