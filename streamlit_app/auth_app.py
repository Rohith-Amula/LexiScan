import streamlit as st
from firebase_config import auth
import re

st.set_page_config(page_title="Login | LexiScan", layout="centered")
st.title("🔐 LexiScan - Login & Signup")

# Function to check password strength
def is_strong_password(password):
    return len(password) >= 6

# Keep user session
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Tabs for Login and Signup
tabs = st.tabs(["🔑 Login", "📝 Signup"])

# ------------- LOGIN -------------
with tabs[0]:
    st.subheader("🔐 Login to your account")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(login_email, login_password)
            st.session_state['user'] = user
            st.success("✅ Login successful!")
            st.switch_page("pages/app.py")  # make sure app.py is in same Streamlit multipage folder if used
        except Exception as e:
            try:
                error_message = e.response.json()['error']['message']
            except:
                error_message = str(e)
            st.error(f"❌ Login failed: {error_message}")

# ------------- SIGNUP -------------
with tabs[1]:
    st.subheader("📝 Create a new account")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")

    if st.button("Signup"):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", signup_email):
            st.warning("📧 Please enter a valid email address.")
        elif not is_strong_password(signup_password):
            st.warning("🔒 Password should be at least 6 characters long.")
        else:
            try:
                user = auth.create_user_with_email_and_password(signup_email, signup_password)
                st.success("🎉 Signup successful! Please log in.")
            except Exception as e:
                try:
                    error_message = e.response.json()['error']['message']
                except:
                    error_message = str(e)
                st.error(f"❌ Signup failed: {error_message}")
