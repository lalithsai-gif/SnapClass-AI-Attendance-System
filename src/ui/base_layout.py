import streamlit as st

def style_background_home():

    st.markdown("""
    <style>
                .stApp{
                    background: #5865F2 !important;
                }  
    </style>
    """,unsafe_allow_html=True)

def style_background_dashboard():

    st.markdown("""
    <style>
                .stApp{
                    background: #E0E3FF !important;
                }  
    </style>
    """,unsafe_allow_html=True)

def style_base_layout():

    st.markdown("""
    <style>
            #MainMenu,footer,header{
                visibility: hidden;
            }
            
            .block-container{
                padding-top:0rem !important
            }
    </style>
    """,unsafe_allow_html=True)