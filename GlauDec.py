

import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
#import streamlit_authenticator as stauth

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import pdfkit

#import database as db

import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "pk_prod_WK9CBN31SQMZH8HPMD6KD8H5DFD2",
                    company_name = "grpx",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')
    
LOGGED_IN= __login__obj.build_login_ui()




if LOGGED_IN == True:
    st.sidebar.write(""" 
        # ***Profile*** 
        """)
    st.sidebar.write(" Hi ", )
    

   # st.markdown("Your Streamlit Application Begins here!")
    # st.markdown(st.session_state)


    def import_and_predict(image_data, model):
        image = ImageOps.fit(image_data, (100,100),Image.ANTIALIAS)
        image = image.convert('RGB')
        image = np.asarray(image)
        st.image(image, channels='RGB')
        image = (image.astype(np.float32) / 255.0)
        img_reshape = image[np.newaxis,...]
        prediction = model.predict(img_reshape)
        return prediction

    model = tf.keras.models.load_model('my_model2.h5')
    st.write("""
         # ***Glaucoma detector***
         """
         )
    st.write(" Hi " ,"this is a simple image classification web app to predict glaucoma through fundus image of eye")
    file = st.file_uploader("Please upload an image(jpg) file", type=["jpg"])

    if file is None:
        st.text("You haven't uploaded a jpg image file")
      
    else:
        imageI = Image.open(file)

        #file_manager = st.get_media_file_manager()
        #file_id = file_manager.add_file(file.name, file.read())
         # Get the URL of the uploaded image
        #url = file_manager.get_url(file_id)
        #sst.write("URL:", url)


        #test2
        #file_details = {"name": file.name, "type": file.type, "size": file.size}
        #file_content = file.read()
        # Get the URL of the uploaded image
        #url = st.get_uploaded_file_details(file_details)["url"]
       # st.write("URL:", url)

        prediction = import_and_predict(imageI, model)
        pred = prediction[0][0]
        if(pred > 0.5):
            st.write(
                 """
                 # **Prediction:** You eye is Healthy. Severity:Normal
                 """)
            prii="Negative"
            course = "Normal"
        
        elif(pred < 0.3):
            st.write("""
                 ## **Prediction:** You are severely affected by Glaucoma."""
                 )
            prii="Positive"
            
            course = "Severely Affected"

        

        else:
             st.write("""
                 ## **Prediction:** You are affected by Glaucoma. Please consult an ophthalmologist as soon as possible.
                 """)
             course = "Mildly Affected"
             prii="Positive"
            

             
        left, = st.columns(1)
        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        template = env.get_template("temp.html")
        form = left.form("template_form") 
        submit = form.form_submit_button("Generate PDF")

        if submit:
                 html = template.render(
                 course=course,
                 prii=prii,
                 #description=description,
                 date=date.today().strftime("%B %d, %Y"),
                 )

                 pdf = pdfkit.from_string(html, False)
                 st.balloons()

                 left.success("Your medical report is generated!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
                 left.download_button(
                     "⬇️ Download PDF",
                     data=pdf,
                     file_name="Med_report.pdf",
                     mime="application/octet-stream",
                    )
    



      
