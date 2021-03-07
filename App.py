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
        st.markdown("<h4 style='text-align: right;'>המערכת שלנו, המבוססת על בינה מלאכותית היא ייחודית בנוף שכן היא תוצר של שילוב בין שני עולמות תוכן מרתקים, מדעי המחשב ומשפטים. כך, יחד יצרנו עבורכם את המערכת האיכותית והמדויקת ביותר וזאת ללא פשרות על הזכויות שלכם. המערכת תעזור לאוכלוסיית עורכי הדין לחזות את גישתו של בית המשפט העליון בארצות הברית, ליברלי או שמרני, זאת על ידי הכנסת מספר פרמטרים למערכת. לאחר מספר רגעים תוכלו לדעת בדיוק כיצד עליכם לעבוד על כתב התביעה או כתב ההגנה שלכם ואיזה טענות ייקחו את הלקוח שלכם אל עבר הניצחון</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>בית המשפט העליון בארצות הברית מורכב מתשעה שופטים, כאשר המטרה של המערכת שלנו היא להבין כיצד הם יפסקו בכל מקרה ומקרה, האם הפסיקה תהיה שמרנית? פסיקה בהתאם לחוק או שמא ליברלית? על ידי אקטיביזם שיפוטי, כאשר בית המשפט רואה עצמו כמגן על זכויות אדם(1)</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>העולם הטכנולוגי בכלל ומערכות בינה מלאכותית בפרט מביאים עימם קדימות, חידוש, ייעול ואפשרויות פורצות דרך אשר עשויות לחסוך זמן ומשאבים.  לצד זה אנו מודעים לסיכונים לפגיעה בזכויות מהותית בחיי האנושות. לכן כדי שתוכלו להרגיש בטוחים, טרם השימוש במערכת לחיזוי גישתו של בית המשפט, נציג בפינכם את התהליך המשפטי שעברה המערכת שלנו בצמוד להליך הפיתוח, כאשר השמירה על זכויותיכם היוותה ערך עליון עבורנו לאורך כל הדרך. תחילה סקרנו את כלל הבעיות המשפטיות והמוסריות אשר עשויות להיפגע בעת השימוש במערכת, וצמצמנו את הפגיעה ככל הניתן, תוך שמירה על הדיוק ויעילות התוצר</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>להלן הזכויות שחרטו על דגלנו כדי להפוך את המערכת למוסרית ולהגן עליכם בכל תרחיש אפשרי, התמקדנו בחוקי הממשל הפדרלי בארצות הברית, לאור העובדה שהמערכת שלנו מותאמת לבית המשפט העליון, אך נבהיר גם כיצד החוק פועל במדינת ישראל</h4>", unsafe_allow_html=True)
        col1, col2, col3= st.beta_columns(3)
        if col1.button('הטיה'):
              st.markdown("<h4 style='text-align: right;'>הטיה אלגוריתמית היא מצב בו ישנו זיהוי במישרין או בעקיפין של מידע ביחס למגדר, גזע, נטייה מינית וכו' והתוצאה המופקת מושפעת מגורמים אלה. ההטיה עשויה להגרם בעקבות הקלט המוזן למערכת המכיל טעויות בסוג המידע המוזן או בעקבות שימוש במשתני ניבוי מפלים. מערכות אלה עשויות להחריף הטיה הקיימת בחברה, כיוון שהנתונים משקפים למעשה הטיה קיימת.  ניתן לראות מקרים רבים ברחבי העולם, בהם ניתן להצביע על מספר דוגמות של הטיה כזו אשר נגרמה עקב השימוש במערכות בינה מלאכותית</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בהחלטות שיפוטיות – מערכת המשפט בארצות הברית משתמשת במערכות המבוססות על בינה מלאכותית. אותן מערכות מדרגות את רמת הסיכון העתידית של פושע, זאת כדי לסייע לשופט לקבל החלטה בנוגע לעונש הראוי. מחקרים בתחום מראים כיצד מערכות אלה מפלות על בסיס גזע</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בהעסקה – חברות שונות משתמשות במערכות המבוססות על בינה מלאכותית כדי לבצע הליכי מיוון לעובדים, ניכר כי השימוש בבינה מלאכותית בתחומים אלה מובילה להפליה על רקע גזע ומין. לעיתים ההפליה אינה נוצרת במכוון אלא משקפת את האפליה הקיימת במציאות</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בשירות – בנקים וגופים מלווים, משתמשים לעיתים במערכות בינה מלאכותית כדי לנבע את ההחזר הפוטנציאלי של לווים,  גם כאן ניתן לראות כי לעיתים מרחשת אפליה בין גברים ונשים</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה במחירים – ישנם מוצרים כמו טיסות וביטוחים אשר עשויים להיות מתומחרים באופן שונה עקב פרמטרים מסוימים (רכישות קודמות, מיקום המשתמש, המכשיר ממנו מתבצעת הקניה וכו') שהלוקח אינו מודע לקיומם. כך נוצרת הטיה על בסיס מעמד כלכלי</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הטיה במידע – עשויה להיווצר הטיה בתפיסת המציאות אצל אדם, זאת כיוון שהרשת מספקת לאדם תוכן הרלוונטי עבורו בלבד, כך מתחזק הקיטוב באוכלוסייה</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפקטיביות – ההצלחה של מערכות בינה מלאכותית עשויה להשתנות בין אוכלוסיות שונות.   כדוגמה נוכל לדון במערכות לזיהוי פנים, אשר תוצאותיה אפקטיביות פחות כאשר עסקינן בשחורים והיספנים בהשוואה לבני אדם לבנים</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ארצות הברית</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הזכות לשוויון מעוגנת בחוקה של ארצות הברית, בתיקון מספר 14, המבטיח כי כל אזרח שנולד או התאזרח בארצות הברית ונתון לשיפוטה, הוא אזרח ארצות הברית ואזרח של המדינה בה הוא גר. מדינה לא תחוקק ולא תאכוף חוק שיגביל את הזכויות ואת החסיונות של אזרחי ארצות הברית. מדינה לא תשלול מאדם את חייו, חירותו וקניינו, בלי הליך משפטי נאות, ולא תשלול מכל אדם שבתחום שיפוטה הגנה שווה על ידי החוקים.  חשוב לציין שלא ניתן למצוא את המילים 'נשים', 'מין' או 'גזע' בחוקה של ארצות הברית, אך אם זאת נראה כי במהלך השנים בית המשפט העליון מתייחס ל'הגנה שווה על ידי החוקים' כהגנה מפני הפליה על רקע של גזע או מין.  דוגמה לכך ניתן לראות בפסקי דינה של השופטת בדימוס רות גינזבורג ז'ל</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ישראל</h3>", unsafe_allow_html=True)
	      st.markdown("<h4 style='text-align: right;'>הזכות לשוויון הוכרה כחלק מעקרונות היסוד של השיטה במדינת ישראל, והיא שואבת את מקור סמכותה עוד ממגילת העצמאות, בה נכתב כי 'מדינת ישראל תקיים שוויון זכויות חברתי ומדיני גמור לכל אזרחיה בלי הבדלי דת, גזע ומין',  בנוסף הזכות לשוויון קיבלה דרך הפסיקה מעמד חוקתי על ידי מודל הביניים, לפיו הזכות לכבוד המנויה בחוק יסוד: כבוד האדם וחירותו כוללת גם היבטים של הזכות לשוויון המגשימים את תכלית חוק היסוד</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>לכם זה לא יקרה</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>כדי למנוע סיטואציה בה המערכת שלנו, המבוססת כאמור על בינה מלאכותית, תפגע בזכות לשוויון של כל אדם, המעוגנת בחוקה של ארצות הברית ובחוק יסוד: כבוד האדם וחירותו, ישנם משתנים שהושמטו באופן מכוון מהמערכת. שכן הנותנים על בסיסם ביצעה המערכת שלנו את הליך הלמידה כוללת משתנים רבים, היוצרים יחד תמונה כללית לגבי פסיקתו של בית המשפט בארצות הברית בהתאם לכל מקרה – ליברלי או שמרני. לאחר בדיקות רבות הצלחנו לבודד משתנים מהותיים כמו: מין של התובע, הנתבע והשופטים, שמות הצדדים, גזע וכתובות המגורים אשר עשויים להעיד על מצב סוציואקונומי. זאת ללא פגיעה באיכות ודיוק התוצאה המתקבלת</h4>", unsafe_allow_html=True)
        col2.button('פרטיות')
        col3.button('לשון הרע')
        st.markdown('<style>.button{background-color: Blue;}</style>',unsafe_allow_html=True)
        col11, col22= st.beta_columns(2)
        if col22.button('אך תחילה עלינו להבין את מקומה של הבינה המלאכותית בארצות הברית'):
             st.markdown("<h4 style='text-align: right;'>ארצות הברית פועלת בשנים האחרונות במספר ערוצים כדי לקדם את היתרונות של טכנולוגית הבינה מלאכותית לצד התייחסותה לאתגרים האתיים. זאת כדי לאפשר לארצות הברית להמשיך ולהתברג כמעצמה בתחום הבינה המלאכותית</h4>", unsafe_allow_html=True)
             st.markdown("<h4 style='text-align: right;'>תחילה, ארצות הברית הפעילה מספר מחקרים שתפקידם הוא מיקסום השילוב בין טכנולוגיה ומוסר. כך כבר בשנת 2018, דארפ'א במסגרת תוכנית הסברתית, ניסתה לעזור למשתמשים להבין את אופן קבלת ההחלטות של מערכות הבינה המלאכותית, זאת ללא פגיעה ברמת הביצוע של המערכות. בנוסף ניתן לראות מחקר של הקרן הלאומית למדע יחד עם אמזון, שמטרתו היא מיקוד בהוגנות מערכות הבינה המלאכותית, ולשם כך הם חקרו מספר סוגיות: שקיפות, הסברתיות, אחריות, פוטנציאל להטיה, השפעות שליליות, התקדמות אלגוריתמית ויעדי הגינות</h4>", unsafe_allow_html=True)
             st.markdown("<h4 style='text-align: right;'>באוקטובר 2019 פרסמה הוועדה המייעצת לחדשנות וביטחון (Defense Innovation board) המלצות לשימוש אתי בבינה מלאכותית. ההמלצות כוללות חמישה עקרונות אתיים לייצור טכנולוגיות המבוססות על בינה מלאכותית: אחריות, שוויון, יכולות מעקב והבנה של הטכנולוגיה, אמינות ויכולת משילות. בנוסף המסמך מספק המלצות בתחום בניהן: הרחבת המחקר להטמעה ראויה של עקרונות אתיים, השקעה במחקר, הגדרת מדדים לאמינות מערכות בינה מלאכותית, יצירת טכניקות להערכה של מערכות בינה מלאכותית, ומחקר ספציפי בתחומי האבטחה</h4>", unsafe_allow_html=True)
             st.markdown("<h4 style='text-align: right;'>מאוחר יותר בתחילת שנת 2020 פורסמו קווים מנחים לרגולציה על מערכות בינה מלאכותית, על ידי הבית הלבן. כאשר במרכז עמד הרצון ליצור גישות אמינות לאימות מערכות המבוססות על בינה מלאכותית. הקווים המנחים כוללים מספר עקרונות אשר צריכים לבסס את הרגולציה בתחום: אמון הציבור בבינה מלאכותית, שיתוף הציבור, יושרה מדעית ואיכות מידע, הערכת וניהול סיכונים, עלות ותועלת, גמישות, הוגנות ואי אפליה, גילוי נאות ושקיפות להגברת אמון הציבור, בטיחות וביטחון ותיאום בין סוכנויות. לצד העקרונות הרגולטורים ישנם עקרונות לא רגולטורים להטמעת הבינה המלאכותית בצורה הטובה ביותר: יצירת תוכניות וניסויים לשם פיתוח סטנדרטים וולונטריים  שיאפשרו ניהול סיכוני פיתוח באופן אדפטיבי יותר. לקראת סוף אותה שנה פרסמו הנחיות לממשל הפדרלי כדי לאפשר שימוש אמין במערכות בינה מלאכותית</h4>", unsafe_allow_html=True)
        st.write("--------------------------------------------------------------")
        st.write("(1) About the Court, SUPREME COURT OF THE UNITED STATES [link](https://www.supremecourt.gov/about/about.aspx)")
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
