import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
#     st.markdown("""
#     <h2>Teacher Screen</h2>
# """,unsafe_allow_html=True)
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()
    

def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.header("Login using password",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='your username')
    teacher_password=st.text_input("Enter password",type='password',placeholder="your password")

    st.divider()

    btnc1,btnc2=st.columns(2)
    with btnc1:
        st.button('Login',shortcut='control+enter',icon=':material/passkey:',width='stretch')
    with btnc2:
        if st.button('Register Instead',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='register'
    footer_dashboard()


def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.header("Register Your Teacher Profile")
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='Username')
    teacher_name=st.text_input("Enter name",placeholder='Your name')
    teacher_password=st.text_input("Enter password",type='password',placeholder="Enter password")
    teacher_cnf_pass=st.text_input("Confirm Your password",placeholder='Enter password',type='password')

    st.divider()

    btnc1,btnc2=st.columns(2)
    with btnc1:
        st.button('Register',shortcut='alt+enter',type='primary',icon=':material/passkey:',width='stretch')
    with btnc2:
        if st.button('Login Instead',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='login'
        
    footer_dashboard()
    