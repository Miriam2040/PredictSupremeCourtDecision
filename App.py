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
    cert_reason_options = list(range(len(cert_reason_display) + 1))
    cert_reason = st.selectbox('Cert Reason', cert_reason_options, format_func=lambda x: cert_reason_display[x - 1])
    law_type_display = ('Constitution','Constitutional Amendment','Federal Statute','Court Rules','Other','Infrequently litigated statutes','State or local law or regulation','No Legal Provision')
    law_type_options =  list(range(len(law_type_display) + 1))
    law_type = st.selectbox('Law Type',law_type_options,format_func=lambda x: law_type_display[x - 1])
    natural_court = st.number_input("Natural Court (Number between 1301 to 1707)", 1301,1707) 
    admin_action = st.number_input("Admin Action (Number between 0 to 118)",0,118) 
      
    # the below line ensures that when the button called 'Predict' is clicked,  
    # the prediction function defined above is called to make the prediction  
    # and store it in the variable result 
    
    if st.button('Predict'):
       result = prediction(issue, case_origin, case_source, cert_reason,law_type,natural_court,admin_action) 
       if result == 1:
            result = 'conservative'
       else:
      	    result = 'liberal'		
		
       st.info('US supreme court direction will be {}'.format(result)) 


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
    elif app_mode == "Technical Overview":
        image = Image.open('tech_review.png')
        st.markdown("<h2 style='text-align: right;'>תיאור טכני</h2>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown("<h4 style='text-align: right;'>השתמשנו בדאטה שנמצא באתר בית המשפט העליון בארצות הברית. הדאטה מכיל רשומות של משפטים שהתקיימו ותיוג של כיוון המשפט - ליברלי מול שמרני </h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>בתחילה, עברנו על הדאטה וסיננו את הפיצ'רים היכולים להשפיע על ביאס כדוגמת שם השופט, כתובות וכו'. לאחר מכן, בחרנו פיצ'רים רלוונטים באמצעות שיטת פיצ'ר סלקשן</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>חילקנו את הדאטה לטריין וטסט כך שהטסט סט הכיל כ33% מסך הדאטה שלנו </h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> לאחר מכן, הרצנו מספר מודלים על מנת למצוא את המודל הטוב ביותר עבור הבעיה שלנו, ומצאנו כי זהו מודל של עצי החלטה ראנדום פורסט </h4>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: right;'>הסבר על המודל ראנדום פורסט</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> זהו מודל אנסמבל של אלגוריתמי עצי החלטה. העיקרון בשיטה זו היא שכל עץ החלטה לומד על סאמפל אחר של הדאטה, ומתפצל לפי תת קבוצה של הפיצ'רים. כל עץ החלטה נותן חיזוי משלו, ולבסוף המודל (ראנדום פורסט) נותן חיזוי לפי החיזוי המירבי של כלל העצים, כלומר אם רוב העצים קבעו כי ההחלטה היא כיוון ליברלי, אזי ההחלטה הסופית של האלגוריתם היא כיוון ליברלי</h4>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: right;'>מדוע בחרנו במודל זה</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> מודל זה גם סיפק את התוצאות הטובות ביותר מבחינת דיוק, וגם מודלים מסוג עצי החלטה מאוד טובים בתחום הסברת המודל, כלומר אנו יכולים בקלות יחסית להבין כיצד המודל קיבל את ההחלטה הסופית שלו</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>האפשרות להסביר את המודל היא קריטית, שכן, לראייתנו, אין משמעות למודל שמקבל החלטה ואינו מנמק אותה</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>האתר שלנו מאפשר ללקוח להזין את הנתונים הנדרשים ולקבל תוצאה על כיוון בית המשפט</h4>", unsafe_allow_html=True)
	
    elif app_mode == "Moral Issues":
        st.markdown("<h2 style='text-align: right;'>אצלנו הזכויות שלך מוגנות</h2>", unsafe_allow_html=True)
	st.markdown("<h4 style='text-align: right;'>המערכת שלנו, המבוססת על בינה מלאכותית היא ייחודית בנוף שכן היא תוצר של שילוב בין שני עולמות תוכן מרתקים, מדעי המחשב ומשפטים. כך, יחד יצרנו עבורכם את המערכת האיכותית והמדויקת ביותר וזאת ללא פשרות על הזכויות שלכם. המערכת תעזור לאוכלוסיית עורכי הדין לחזות את גישתו של בית המשפט העליון בארצות הברית, ליברלי או שמרני, זאת על ידי הכנסת מספר פרמטרים למערכת. לאחר מספר רגעים תוכלו לדעת בדיוק כיצד עליכם לעבוד על כתב התביעה או כתב ההגנה שלכם ואיזה טענות ייקחו את הלקוח שלכם אל עבר הניצחון. </h2>", unsafe_allow_html=True)
    elif app_mode == "Model Source Code":
        st.write("Model training source code is here: [link](https://github.com/Miriam2040/PredictSupremeCourtDecision/blob/main/Supreme_Court_Direction_Prediction.ipynb)")	
    elif app_mode == "Run Prediction":
        run_prediction()
    elif app_mode == "About":
        image = Image.open('Team.PNG')
        st.markdown("<h2 style='text-align: right;'> הצוות</h2>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown("<h2 style='text-align: right;'> הפרויקט</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> .הפרויקט שמוצג באתר זה בוצע במסגרת קורס בינה מלאכותית ומוסר</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> .רצינו לנצל את העובדה שהצוות מורכב ממומחי תוכן בעולם בינה המלאכותית וכן מעולם המשפטים</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> .לצורך כך לקחנו בעיה של חיזוי כיוון בית המשפט העליון בארה'ב ובנינו מודל בינה מלאכותית שיעשה זאת</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> .האתר הזה מסביר את העבודה שנעשתה ומנגיש את המודל לשימוש</h4>", unsafe_allow_html=True)
    elif app_mode == "Show Instructions":
        st.header("The application includes following parts:")
        st.subheader('Run prediction:')
        st.markdown('You insert your case parameters and get model prediction for supreme court direction. Here is video demo:')
        video_file = open('RunPredictionDemo.webm', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        st.subheader('Technical Overview:')
        st.markdown('Explanation about technical aspects and work done during ML model creation')
        st.subheader('Moral Issues:')
        st.markdown('Explanation about moral issues involved in this project')
        st.subheader('App Source Code:')
        st.markdown('This application source code')
        st.subheader('Model Source Code:')
        st.markdown('ML model training notebook link')
        st.subheader('About:')
        st.markdown('Details about this project')

if __name__=='__main__': 
    main() 
