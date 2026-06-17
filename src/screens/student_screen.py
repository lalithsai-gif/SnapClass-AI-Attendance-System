import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from PIL import Image
import numpy as np
import time
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject
from src.pipelines.face_pipeline import predict_attendance,get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()


    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()

    with st.spinner('Loading Your Enrolled Subjects....'):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)

    stats_map={}

    for log in logs:
        sid=log['student_id']

        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        
        stats_map[sid]['total']+=1

        if log.get('is_present'):
            stats_map[sid]['attended']+=1
    
    cols=st.columns(2)

    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']

        stats=stats_map.get(sid,{"total":0,"attended":0})

        def unenroll_btn(sid=sid,sub=sub):
            if st.button("Unenroll from this course",key=f"unenroll_{sid}",type='tertiary',width='stretch',icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id,sid)
                st.toast(f"Unenrolled from {sub['name']} successfully")
                st.rerun()

        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    {'📆','Total',stats['total']},
                    {'✅','Attended',stats['attended']}
                ],
                footer_callback=unenroll_btn
            )

    footer_dashboard()

def student_screen():
    
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

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

    show_registration=False

    if photo_source:
        img=np.array(Image.open(photo_source))

        with st.spinner('AI is Scanning...'):
            detected,all_ids,num_faces=predict_attendance(img)

            if num_faces==0:
                st.warning('Face not Found')
            elif num_faces>1:
                st.warning('Multiple faces Found')
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']),None)

                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration=True
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name=st.text_input("Enter Your Name",placeholder='E.g. Lalith Dabbiru')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your voice for only attendance")

            audio_data=None

            try:
                audio_data=st.audio_input('Record a short phrase like I am present , My name is Rohit.')
            except Exception:
                st.error('Audio data Failed!')
            
            if st.button('Create Account',type='primary'):
                if new_name:
                    with st.spinner('Creating Profile.....'):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embeddings(audio_data.read())

                            response_data=create_student(new_name,face_embeddings=face_emb,voice_embeddings=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f"Profile created! Hi {new_name}")
                                st.rerun()
                            else:
                                st.error("Couldn't capture your facial features for registration")
                else:
                    st.warning('Please enter your name!')

    footer_dashboard()