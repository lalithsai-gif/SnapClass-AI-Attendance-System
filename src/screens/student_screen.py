import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from PIL import Image
import numpy as np

def student_screen():
    
    style_background_dashboard()
    style_base_layout()

    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()
    
    st.header('Login Using FaceID',text_alignment='center')

    st.markdown("""
    <h3 style='text-align:center; color:blue;'>Position Your Face In The Center</h3>
""",unsafe_allow_html=True)

    photo_source=st.camera_input("")

    if photo_source:
        np.array(Image.open(photo_source))
    footer_dashboard()