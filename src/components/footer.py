import streamlit as st

def footer_home():
    st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px;">
                <p style="font-weight:bold; color:yellow;">Created by Lalith with ❤️</p>
            </div>
    """
                ,unsafe_allow_html=True)
    
def footer_dashboard():
    st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px;">
                <p style="font-weight:bold; color:black;">Created by Lalith with ❤️</p>
            </div>
    """
                ,unsafe_allow_html=True)