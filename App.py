import pandas as pd 
import numpy as np 
import pickle 
import urllib
import streamlit as st 
from PIL import Image 
import base64
import zipfile
from sklearn.ensemble import RandomForestClassifier
  
# loading in the model to predict on the data 
@st.cache(show_spinner=False, allow_output_mutation=True)
def get_classifier():
    archive = zipfile.ZipFile('model.zip', 'r')
    classifier = pickle.load(archive.open('model.pkl','r'))
    archive.close()
    
    return classifier

def prediction(issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action):   
   
    classifier = get_classifier()	
    prediction = classifier.predict( 
        [[issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action]])  
    return prediction 
 
def run_prediction():
    # the following lines create text boxes in which the user can enter  
    # the data required to make the prediction 
    issue = st.number_input("Issue (Number between 10010 to 140070)", 10010,140070) 
    case_origin = st.number_input("Case Origin (Number between 1 to 302)", 1,302) 
    case_source = st.number_input("Case Source (Number between 1 to 302)",1,302) 
    cert_reason_display = ('cert did not arise on cert or cert not granted', 'federal court conflict', 'federal court conflict and to resolve important or significant question','putative conflict','conflict between federal court and state court','state court conflict','federal court confusion or uncertainty','state court confusion or uncertainty','federal court and state court confusion or uncertainty','to resolve important or significant question','to resolve question presented','no reason given','other reason')
    cert_reason_options = list(np.arange(1,len(cert_reason_display) + 1))
    cert_reason = st.selectbox('Cert Reason', cert_reason_options, format_func=lambda x: cert_reason_display[x])
    law_type_display = ('Constitution','Constitutional Amendment','Federal Statute','Court Rules','Other','Infrequently litigated statutes','State or local law or regulation','No Legal Provision')
    law_type_options = list(np.arange(1, len(law_type_display) + 1))
    law_type = st.selectbox('Law Type',law_type_options,format_func=lambda x: law_type_display[x])
    natural_court = st.number_input("Natural Court (Number between 1301 to 1707)", 1301,1707) 
    admin_action = st.number_input("Admin Action (Number between 0 to 118)",0,118) 
      
    # the below line ensures that when the button called 'Predict' is clicked,  
    # the prediction function defined above is called to make the prediction  
    # and store it in the variable result 
    
    if st.button('Predict'):
       result = prediction(issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action) 
       #if result == 1:
        #    result = 'conservative'
       #else:
      #	    result = 'liberal'		
       st.info(issue)
       st.info(case_origin)
       st.info(case_source)
       st.info(cert_reason)
       st.info(law_type)
       st.info(natural_court)
       st.info(admin_action)
			   
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
        ["Show Instructions", "Run Prediction","Technical Overview","Moral Issues", "App Source Code","Model Source Code","About"])
    if app_mode == "App Source Code":
        st.code(get_file_content_as_string("App.py"))
    elif app_mode == "Model Source Code":
        st.write("check out this [link](https://github.com/Miriam2040/PredictSupremeCourtDecision/blob/main/Supreme_Court_Direction_Prediction.ipynb)")	
    elif app_mode == "Run Prediction":
        run_prediction()
    elif app_mode == "About":
        image = Image.open('Team.PNG')
        st.markdown("<h2 style='text-align: right;'> הצוות</h2>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown("<h2 style='text-align: right;'> הפרויקט</h2>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right;'> .הפרויקט שמוצג באתר זה בוצע במסגרת קורס בינה מלאכותית ומוסר</h6>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right;'> .רצינו לנצל את העובדה שהצוות מורכב ממומחי תוכן בעולם בינה המלאכותית וכן מעולם המשפטים</h6>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right;'> .לצורך כך לקחנו בעיה של חיזוי כיוון בית המשפט העליון בארה'ב ובנינו מודל בינה מלאכותית שיעשה זאת</h6>", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right;'> .האתר הזה מסביר את העבודה שנעשתה ומנגיש את המודל לשימוש</h6>", unsafe_allow_html=True)
    elif app_mode == "Show Instructions":
        st.header("The application includes following parts:")
        st.subheader('Run prediction:')
        st.markdown('You insert your case parameters and get model prediction for supreme court direction')

if __name__=='__main__': 
    main() 
