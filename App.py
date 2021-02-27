import pandas as pd 
import numpy as np 
import pickle 
import urllib
import streamlit as st 
from PIL import Image 
import base64
import zipfile
import sklearn

  
# loading in the model to predict on the data 

archive = zipfile.ZipFile('model.zip', 'r')
classifier = pickle.loads(archive.open('model.pkl').read())
archive.close()

def prediction(issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action):   
   
    prediction = classifier.predict( 
        [[issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action]]) 
    print(prediction) 
    return prediction 
      
def run_prediction():
    # the following lines create text boxes in which the user can enter  
    # the data required to make the prediction 
    issue = st.text_input("Issue", "Type Here") 
    case_origin = st.text_input("Case Origin", "Type Here") 
    case_source = st.text_input("Case Source", "Type Here") 
    cert_reason_display = ('cert did not arise on cert or cert not granted', 'federal court conflict', 'federal court conflict and to resolve important or significant question','putative conflict','conflict between federal court and state court','state court conflict','federal court confusion or uncertainty','state court confusion or uncertainty','federal court and state court confusion or uncertainty','to resolve important or significant question','to resolve question presented','no reason given','other reason')
    cert_reason_options = list(range(len(cert_reason_display)))
    cert_reason = st.selectbox('Cert Reason', cert_reason_options, format_func=lambda x: cert_reason_display[x])
    law_type_display = ('Constitution','Constitutional Amendment','Federal Statute','Court Rules','Other','Infrequently litigated statutes','State or local law or regulation','No Legal Provision')
    law_type_options = list(range(len(law_type_display)))
    law_type = st.selectbox('Law Type',law_type_options,format_func=lambda x: law_type_display[x])
    natural_court = st.text_input("Natural Court", "Type Here") 
    admin_action = st.text_input("Admin Action", "Type Here") 
    result ="" 
      
    # the below line ensures that when the button called 'Predict' is clicked,  
    # the prediction function defined above is called to make the prediction  
    # and store it in the variable result 
    if st.button("Predict"): 
        result = prediction(issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action) 
        if result == 1:
             result = 'conservative'
        else:
             result = 'liberal'		
    st.success('US supreme court direction will be {}'.format(result)) 


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/Miriam2040/PredictSupremeCourtDecision/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")
	
# this is the main function in which we define our webpage  
def main(): 
    image = Image.open('Court.jpg')
    st.image(image, use_column_width=True)
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to",
        ["Show Instructions", "Run Prediction","Technical Overview","Moral Issues", "Show App Source Code","Show Model Source Code","About"])
    if app_mode == "Show App Source Code":
        st.code(get_file_content_as_string("App.py"))
    elif app_mode == "Show Model Source Code":
        st.code(get_file_content_as_string("Supreme_Court_Direction_Prediction.ipynb")) 	
    elif app_mode == "Run Prediction":
        run_prediction()
      
   
     
if __name__=='__main__': 
    main() 
