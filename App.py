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
        st.markdown("<h4 style='text-align: right;'>השתמשנו בדאטה שנמצא באתר בית המשפט העליון בארצות הברית מכיון שאילו נתונים פתוחים ומותרים לשימוש. הדאטה מכיל רשומות של משפטים שהתקיימו ותיוג של כיוון המשפט - ליברלי מול שמרני </h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>בתחילה, עברנו על הדאטה וסיננו את הפיצ'רים היכולים להשפיע על הטיה כדוגמת שם השופט, כתובות וכו'.כך שכל הפ'יצרים שנשארו אינם מצביעים על אוכלוסיה מסוימת ולכן לא יכולה להיות הטיה במודל. לאחר מכן, בחרנו פיצ'רים רלוונטים באמצעות שיטת פיצ'ר סלקשן</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>חילקנו את הדאטה לאימון וטסט כך שסט האימון הכיל כ33% מסך הדאטה שלנו </h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> לאחר מכן, הרצנו מספר מודלים על מנת למצוא את המודל הטוב ביותר עבור הבעיה שלנו, ומצאנו כי זהו מודל של עצי החלטה ראנדום פורסט </h4>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: right;'>הסבר על המודל ראנדום פורסט</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> זהו מודל אנסמבל של אלגוריתמי עצי החלטה. העיקרון בשיטה זו היא שכל עץ החלטה לומד על סאמפל אחר של הדאטה, ומתפצל לפי תת קבוצה של הפיצ'רים. כל עץ החלטה נותן חיזוי משלו, ולבסוף המודל (ראנדום פורסט) נותן חיזוי לפי החיזוי המירבי של כלל העצים, כלומר אם רוב העצים קבעו כי ההחלטה היא כיוון ליברלי, אזי ההחלטה הסופית של האלגוריתם היא כיוון ליברלי</h4>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: right;'>מדוע בחרנו במודל זה</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'> מודל זה גם סיפק את התוצאות הטובות ביותר מבחינת דיוק, וגם מודלים מסוג עצי החלטה מאוד טובים בתחום הסברת המודל, כלומר אנו יכולים בקלות יחסית להבין כיצד המודל קיבל את ההחלטה הסופית שלו</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>האפשרות להסביר את המודל היא קריטית, שכן, לראייתנו, אין משמעות למודל שמקבל החלטה ואינו מנמק אותה</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>האתר שלנו מאפשר ללקוח להזין את הנתונים הנדרשים ולקבל תוצאה על כיוון בית המשפט</h4>", unsafe_allow_html=True)
	st.markdown("<h3 style='text-align: right;'>תוצאות</h3>", unsafe_allow_html=True)
	st.markdown("<h4 style='text-align: right;'>.אירי שאימנו את המודל של סט האימון בדקנו את ביצועיו באמצעות סט הטסט</h4>", unsafe_allow_html=True)
    elif app_mode == "Moral Issues":
        st.markdown("<h2 style='text-align: right;'>אצלנו הזכויות שלך מוגנות</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>המערכת שלנו, המבוססת על בינה מלאכותית היא ייחודית בנוף שכן היא תוצר של שילוב בין שני עולמות תוכן מרתקים, מדעי המחשב ומשפטים. כך, יחד יצרנו עבורכם את המערכת האיכותית והמדויקת ביותר וזאת ללא פשרות על הזכויות שלכם. המערכת תעזור לאוכלוסיית עורכי הדין לחזות את גישתו של בית המשפט העליון בארצות הברית, ליברלי או שמרני, זאת על ידי הכנסת מספר פרמטרים למערכת. לאחר מספר רגעים תוכלו לדעת בדיוק כיצד עליכם לעבוד על כתב התביעה או כתב ההגנה שלכם ואיזה טענות ייקחו את הלקוח שלכם אל עבר הניצחון</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>בית המשפט העליון בארצות הברית מורכב מתשעה שופטים, כאשר המטרה של המערכת שלנו היא להבין כיצד הם יפסקו בכל מקרה ומקרה, האם הפסיקה תהיה שמרנית? פסיקה בהתאם לחוק או שמא ליברלית? על ידי אקטיביזם שיפוטי, כאשר בית המשפט רואה עצמו כמגן על זכויות אדם(1)</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>העולם הטכנולוגי בכלל ומערכות בינה מלאכותית בפרט מביאים עימם קדימות, חידוש, ייעול ואפשרויות פורצות דרך אשר עשויות לחסוך זמן ומשאבים.  לצד זה אנו מודעים לסיכונים לפגיעה בזכויות מהותית בחיי האנושות. לכן כדי שתוכלו להרגיש בטוחים, טרם השימוש במערכת לחיזוי גישתו של בית המשפט, נציג בפינכם את התהליך המשפטי שעברה המערכת שלנו בצמוד להליך הפיתוח, כאשר השמירה על זכויותיכם היוותה ערך עליון עבורנו לאורך כל הדרך. תחילה סקרנו את כלל הבעיות המשפטיות והמוסריות אשר עשויות להיפגע בעת השימוש במערכת, וצמצמנו את הפגיעה ככל הניתן, תוך שמירה על הדיוק ויעילות התוצר</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>להלן הזכויות שחרטו על דגלנו כדי להפוך את המערכת למוסרית ולהגן עליכם בכל תרחיש אפשרי, התמקדנו בחוקי הממשל הפדרלי בארצות הברית, לאור העובדה שהמערכת שלנו מותאמת לבית המשפט העליון, אך נבהיר גם כיצד החוק פועל במדינת ישראל</h4>", unsafe_allow_html=True)
        col1, col2, col3= st.beta_columns(3)
        if col1.button('הטיה'):
              st.markdown("<h3 style='text-align: right;'>הטיה</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'> .הטיה אלגוריתמית היא מצב בו ישנו זיהוי במישרין או בעקיפין של מידע ביחס למגדר, גזע, נטייה מינית וכו' והתוצאה המופקת מושפעת מגורמים אלה. ההטיה עשויה להגרם בעקבות הקלט המוזן למערכת המכיל טעויות בסוג המידע המוזן או בעקבות שימוש במשתני ניבוי מפלים. מערכות אלה עשויות להחריף הטיה הקיימת בחברה, כיוון שהנתונים משקפים למעשה הטיה קיימת(2).  ניתן לראות מקרים רבים ברחבי העולם, בהם ניתן להצביע על מספר דוגמות של הטיה כזו אשר נגרמה עקב השימוש במערכות בינה מלאכותית</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בהחלטות שיפוטיות – מערכת המשפט בארצות הברית משתמשת במערכות המבוססות על בינה מלאכותית. אותן מערכות מדרגות את רמת הסיכון העתידית של פושע, זאת כדי לסייע לשופט לקבל החלטה בנוגע לעונש הראוי. מחקרים בתחום מראים כיצד מערכות אלה מפלות על בסיס גזע(3)</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בהעסקה – חברות שונות משתמשות במערכות המבוססות על בינה מלאכותית כדי לבצע הליכי מיוון לעובדים, ניכר כי השימוש בבינה מלאכותית בתחומים אלה מובילה להפליה על רקע גזע ומין. לעיתים ההפליה אינה נוצרת במכוון אלא משקפת את האפליה הקיימת במציאות(4)</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה בשירות – בנקים וגופים מלווים, משתמשים לעיתים במערכות בינה מלאכותית כדי לנבע את ההחזר הפוטנציאלי של לווים(5),  גם כאן ניתן לראות כי לעיתים מרחשת אפליה בין גברים ונשים(6)</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפליה במחירים – ישנם מוצרים כמו טיסות וביטוחים אשר עשויים להיות מתומחרים באופן שונה עקב פרמטרים מסוימים (רכישות קודמות, מיקום המשתמש, המכשיר ממנו מתבצעת הקניה וכו') שהלוקח אינו מודע לקיומם. כך נוצרת הטיה על בסיס מעמד כלכלי(7)</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הטיה במידע – עשויה להיווצר הטיה בתפיסת המציאות אצל אדם, זאת כיוון שהרשת מספקת לאדם תוכן הרלוונטי עבורו בלבד, כך מתחזק הקיטוב באוכלוסייה(8)</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אפקטיביות – ההצלחה של מערכות בינה מלאכותית עשויה להשתנות בין אוכלוסיות שונות(9).   כדוגמה נוכל לדון במערכות לזיהוי פנים, אשר תוצאותיה אפקטיביות פחות כאשר עסקינן בשחורים והיספנים בהשוואה לבני אדם לבנים(10)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ארצות הברית</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הזכות לשוויון מעוגנת בחוקה של ארצות הברית, בתיקון מספר 14, המבטיח כי כל אזרח שנולד או התאזרח בארצות הברית ונתון לשיפוטה, הוא אזרח ארצות הברית ואזרח של המדינה בה הוא גר. מדינה לא תחוקק ולא תאכוף חוק שיגביל את הזכויות ואת החסיונות של אזרחי ארצות הברית. מדינה לא תשלול מאדם את חייו, חירותו וקניינו, בלי הליך משפטי נאות, ולא תשלול מכל אדם שבתחום שיפוטה הגנה שווה על ידי החוקים(11).  חשוב לציין שלא ניתן למצוא את המילים 'נשים', 'מין' או 'גזע' בחוקה של ארצות הברית, אך אם זאת נראה כי במהלך השנים בית המשפט העליון מתייחס ל'הגנה שווה על ידי החוקים' כהגנה מפני הפליה על רקע של גזע או מין(12).  דוגמה לכך ניתן לראות בפסקי דינה של השופטת בדימוס רות גינזבורג ז'ל(13)(14)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ישראל</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הזכות לשוויון הוכרה כחלק מעקרונות היסוד של השיטה במדינת ישראל, והיא שואבת את מקור סמכותה עוד ממגילת העצמאות, בה נכתב כי 'מדינת ישראל תקיים שוויון זכויות חברתי ומדיני גמור לכל אזרחיה בלי הבדלי דת, גזע ומין'(15),  בנוסף הזכות לשוויון קיבלה דרך הפסיקה מעמד חוקתי על ידי מודל הביניים, לפיו הזכות לכבוד המנויה בחוק יסוד: כבוד האדם וחירותו כוללת גם היבטים של הזכות לשוויון המגשימים את תכלית חוק היסוד(16)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>לכם זה לא יקרה</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>כדי למנוע סיטואציה בה המערכת שלנו, המבוססת כאמור על בינה מלאכותית, תפגע בזכות לשוויון של כל אדם, המעוגנת בחוקה של ארצות הברית ובחוק יסוד: כבוד האדם וחירותו, ישנם משתנים שהושמטו באופן מכוון מהמערכת. שכן הנותנים על בסיסם ביצעה המערכת שלנו את הליך הלמידה כוללת משתנים רבים, היוצרים יחד תמונה כללית לגבי פסיקתו של בית המשפט בארצות הברית בהתאם לכל מקרה – ליברלי או שמרני. לאחר בדיקות רבות הצלחנו לבודד משתנים מהותיים כמו: מין של התובע, הנתבע והשופטים, שמות הצדדים, גזע וכתובות המגורים אשר עשויים להעיד על מצב סוציואקונומי. זאת ללא פגיעה באיכות ודיוק התוצאה המתקבלת</h4>", unsafe_allow_html=True)
              st.write("--------------------------------------------------------------")
              st.write("פורום לתשתיות לאומיות  למחקר ופיתוח ועדת בינה מלאכותית ומדע הנתונים (2020)(2)")
              st.write("(3)רועי גולדשמידט אפליה אלגוריתמית במערכות המבוססות על בינה מלאכותית (הכנסת, מרכז המחקר והמידע, 2020)", unsafe_allow_html=True)
              st.write("(4)שם")
              st.write("(5)שם")
              st.write("(6)[link](https://www.geektime.co.il/discrimination-in-ai-ml)")
              st.write("(7)גולדשמידט, לעיל ה'ש 3")
              st.write("(8)שם")
              st.write("(9)שם")
              st.write("(10)ועדת בינה מלאכותית ומדע הנתונים, לעיל ה'ש 2")
              st.write("(11)U.S. CONST. amend. XIV")
              st.write("(12)Robin Bleiweis, The Equal Rights Amendment: What You Need to Know, CENTER FOR AMERICAN PROGRESS (Jan. 29, 2020)")
              st.write("(13)Reed v. Reed, 404 U.S. 71 (November 22, 1971)")
              st.write("(14)Frontiero v. Richardson, 411 U.S. 677 (May 14, 1973")
              st.write("(15)בג'ץ 6427/02 התנועה לאיכות השלטון בישראל נ' הכנסת, פ'ד סא(1) 619, פס' 26 לפסק דינו של השופט ברק (2005)")
              st.write("(16)אהרן ברק כבוד האדם – הזכות החוקתית ובנותיה 668 (2014)")
        if col2.button('פרטיות'):
              st.markdown("<h3 style='text-align: right;'>פרטיות</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>זכותו של אדם לפרטיות קשורה בין היתר לכיבוד האוטונומיה שלו ויכולתו לבחור כיצד לפעול בחייו. כאשר עסקינן בפרטיות במידע, במרכז עומדת זכותו של אדם לשלוט או להשפיע על המידע אודותיו. בעידן הנוכחי בו איסוף המידע אודותינו מתרחשת בכל רגע, ברחבי העולם כולו, ללא שליטה וכמעט ללא הגבלה. המידע הנאסף עשוי לשמש יסוד להפקת מידע אודות אדם ללא קשר בהכרח למקור. בנוסף ניתן להשתמש במידע להשפעה לא הוגנת על הפרט. לכן עולים אתגרים רבים להגנה על הזכות לפרטיות של הפרט. בדומה לכך פועלות מערכות הבינה המלאכותית, הן מבוססות על עיבוד נתונים, ממקורות שונים, לעיתים תוך ניתוק מההקשר המקורי בגינו הוא נאסף. בנוסף המערכות מסיקות מסקנות, מקבלות החלטות ומבצעות פעולות על בסיס מידע זה. כך נוצר סיכון מהותי לפגיעה בזכות לפרטיות(2)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ארצות הברית</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>ניתן לראות כי הזכות לפרטיות לא מעוגנת באופן חד משמעי בחוקה של ארצות הברית, אם זאת התיקון התשיעי לחוקה קובע כי אין לפרש את החוקה המונה זכויות אדם אשר ראוי להגן עליהם כרשימה סגורה(3).   ואכן ניתן לראות כי במהלך השנים נעשה שימוש בתיקון זה כדי לבסס את ההגנה על הפרטיות של הפרט. בנוסף החוקה של ארצות הברית מכילה הגנה משמעותית מפני חיפוש בלתי סביר, שזו היא כאמור נגזרת של הזכות לפרטיות ובית המשפט העליון הרחיב את ההכרה בזכות זו למלוא היקפה של הזכות(4).  חשוב לציין כי הרבה מן המדינות בארצות הברית לא הסתפקו בהחלה פדרלית ועיגנו את הזכות לפרטיות על כל גווניה בחוקה המדינית. בעניינו חשוב לציין את עניין כץ(5)  בו נקבע כי פעולות הממשל מוגבלות במקום בו יש לפרט 'ציפיה סבירה' לפרטיות. הזכות לפרטיות מתבטאת גם בזכותו של אדם לאוטונומיה של הפרט, כאשר ההחלטה הראשונה בתחום התקבלה בעניין  גריסוולד נגד קונטיקט בו נקבע כי לא ניתן לאסור על מכירה של אמצעי מניעה, פסק דין זה קבע כי הזכות לפרטיות מעוגנת בחוקה של ארצות הברית(6).  בנוסף הפסיקה האמריקאית הכירה בפרטיות נזיקית אשר מטרתה העיקרית היא מניעה של זליגת המידע של הפרט, זכות זו אינה ייחודית ליחסי אזרח־שלטון, אלא זכות אזרחית(7)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ישראל</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>הזכות לפרטיות לא הוכרה תחילה ע'י בית המשפט(8),  אך נראה תפנית בסוף שנות ה-70 בעניין קטלן(9).  בהמשך בשנת 1981 חוקק חוק הגנה הפרטיות(10),  אשר קובע כי פגיעה בפרטיות מהווה עבירה פלילית ועוולה אזרחית, ובית המשפט קבע כי הזכות לפרטיות היא זכות יסוד שאין לפגוע בה(11).  מאוחר יותר הזכות לפרטיות קיבלה  עיגון רשמי כזכות יסוד מכוח חוק יסוד: כבוד האדם וחירותו, כאשר סעיף 7 לחוק קובע</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>כל אדם זכאי לפרטיות ולצנעת חייו</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אין נכנסים לרשות היחיד של אדם ללא הסכמתו</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אין עורכים חיפוש ברשות היחיד של אדם, על גופו בגופו או בכליו</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>אין פוגעים בסוד שיחו של אדם, בכתביו או ברשומותיו</h4>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>בעניינו רלוונטי לדון בזכות לפרטיות במידע, קיימת הסכמה כללית כי לבני האדם ישנה ציפייה לגיטימית שמידע על חייהם האישיים לא יהיה חשוף לעייני כל(12).  התפתחותו של העידן הטכנולוגי מחריפה את בעיית המידע, וניתן לראות אזכור לכך בפסקותיו של בית המשפט העליון, כאשר השופטת בייניש מדגישה את משנה הזהירות שיש לנקוט, כאשר התקדמות הטכנולוגיה מובילה לפגיעה בזכות לפרטיות(13).  בנוסף ניתן לראות אזכור לחשיבותה של הזכות לפרטיות בעניין האיכונים(14),  הנשיאה חיות מאזכרת את הש' סולברג באמרו: ' המשטר הדמוקרטי דורש אף הוא את קיומה של הזכות לפרטיות. קיומו של מרחב חיים פרטי שלא נמצא תחת עינה הפקוחה של המדינה, הוא הכרחי לקיומה של חברה פלורליסטית המעניקה דרור למגוון הקולות בקִרבּה'. חשוב לציין כי על אף עיגונה של הזכות לפרטיות בחוק הגנת הפרטיות(15),  אשר מונה 11 מעשים אשר יחשבו לפגיעה בזכות ובנוסף עיגונה בחוק יסוד, הדגיש בית המשפט כי היקפה של הזכות אינו מוגדר ומשתנה בהתאם למציאות(16)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>לכם זה לא יקרה</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>נראה כי הזכות לפרטיות מעוגנת בחוקה הפדרלית של ארצות הברית, אומנם לא באופן ישר, אך העיגון הוכר על ידי פסיקתו של בית המשפט. יתר על כן ישנה הגנה חוקית במסגרת המדינות השונות בארצות הברית כפי שתואר לעיל. גם בישראל הזכות לפרטיות זכתה לעיגון בחוק ההגנה על הפרטיות ובחוק יסוד: כבוד האדם וחירותו. כדי למנוע סיטואציה בה המערכת שלנו פוגעת בזכות לפרטיות הן של המשמשים והן של פרטי הצדדים והשופטים בפסקי הדין על בסיסם ייצרו את מודל הבינה המלאכותית, הושמטו פרטים אשר עשויים לייצור פגיעה שכזו. כך השמטנו את שמות הצדדים, כתובות המגורים ושמות השופטים. חשוב לציין כי השמירה על פרטיות הלקוחות שלנו לא פגעה בדיוק ובאיכות התוצר</h4>", unsafe_allow_html=True)
              st.write("--------------------------------------------------------------")
              st.write("דין וחשבון ועדת משנה של המיזם הלאומי למערכות נבונות בנושא אתיקה ורגולציה של בינה מלאכותית (2019)(2)")
              st.write("(3)U.S. CONST. amend. IX", unsafe_allow_html=True)
              st.write("(4)דין וחשבון הועדה להגנה מפני פגיעה בצנעת הפרט (1976)")
              st.write("(5)Katz v. U.S., 389 U.S. 347 (1967)")
              st.write("(6)Griswold v. Connecticut, 381 U.S. 479 (1965)")
              st.write("(7)Warren & Brandeis, 'The Right to Privacy', 4 Harv. L. Rev. 193 (1890)")
              st.write("(8)ע'א 68/56 הלן רבינוביץ נ' יצחק מירלין, פד'י יא 1224 (1957)")
              st.write("(9)בג'ץ 355/79 קטלן נ' שירות בתי הסוהר, פ'ד לד(3) 294, 308 (1980)")
              st.write("(10)חוק הגנת הפרטיות, התש'א–1981")
              st.write("(11)בג'ץ 3815/90 גילת נ' שר המשטרה, פ'ד מה(3) 414 (1991)")
              st.write("(12)רות פלאטו־שנער 'הכספת הבנקאית באספקלריית הזכות לפרטיות' קריית המשפט א 279 (התשס'א)")
              st.write("(13)עש'מ 6843/01 בן דוד נ' נציב שירות המדינה, פ'ד נו(2) 918, 923 (2002)")
              st.write("(14)בג'צ  2109/20 עו'ד שחר בן מאיר נ' ראש הממשלה (פורסם באר'ש, 26.4.2020)")
              st.write("(15)בחוק הגנת הפרטיות, לעיל ה'ש 10")
              st.write("(16)בג'ץ 2481/93 דיין נ' וילק, מפקד מחוז ירושלים, פ'ד מח(2) 456 (1994)")
        if col3.button('לשון הרע'):
              st.markdown("<h3 style='text-align: right;'>לשון הרע</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>כאשר עסקינן בדיני לשון הרע, ניתן לראות את הצורך לאזן בין שני ערכים בסייסים באנושות, הזכות לכבוד אל מול חופש הביטוי. איזון זה משתנה בין חברה לחברה, ובין מערכות משפט שונות. אי לכך דיני לשון הרע הם תחום דימי ומתפתח, וניתן לראות את ניסיון ההשפעה על נקודת איזון זו מצידו של בית המשפט והמחוקק(2)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ארצות הברית</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>מקורם של דיני לשון הרע בארצות הברית הוא מהמשפט המקובל, הנקלט ביבשת אמריקה עוד בתקופת השלטון הבריטי. לאחר ייסודה של ארצות הברית והחוקה הפדרלית ניתן לראות שינוי, שכן התיקון הראשון לחוקה קובע הגנה מהותית על הזכות לחופש הביטוי. האיזון בין הזכות לחופש הביטוי לבין הזכות לשם טוב הוא סוגיה מהותית המשתנה בין שיטות משפט שונות. כאמור ניכר כי בארצות הברית, כאשר אין חשש לאלימות, זכותו של אדם לחופש הביטוי גוברת. עם זאת ניתן לראות כי עידן האינטרנט מביא עימו שינוי, כאשר ישנה עלייה במספר ההליכים הפליליים כאשר עסקינן בהוצאת דיבה באינטרנט, זאת בעזרת חוקים מדיניים שניתן למצוא במספר מדינות (בקולורדו, בפלורידה, באיידהו, בקנזס, בלואיזיאנה, במישיגן במינסוטה, במונטנה, בניו-המפשייר, בניו-מקסיקו, בצפון קרולינה, בצפון דקוטה, באוקלהומה, ביוטה, בווירג'יניה, בוושינגטון ובוויסקונסין, וכן בפורטו ריקו ובאיי הבתולה)(3)</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>ישראל</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>כבוד האדם ושמו הטוב חשובים לאדם כחיים עצמם. הם יקרים לנו ולרוב יותר מכל נכס אחר'(4).  בישראל ניתן לראות כי זכותו של אדם לשמו הטוב מעוגנת בחוק איסור לשון הרע(5),  אשר מהווה עוולה פלילית מכוח סעיף 6 ועוולה אזרחית מכוח סעיף 7. חשוב לציין כי בעידן האינטרנט ישנה חשיבות מיוחדת להגנה על הזכות לשם טוב, כאשר בית המשפט דן רבות במאפייניו הייחודיים של האינטרנט בהקשר של חופש הביטוי(6).  בנוסף ניתן לראות כי הפסיקה העניקה לזכות לשם טוב עיגון בחוד יסוד: כבוד האדם חירותו, שכן שמו הטוב של אדם טבוע אינהרנטית במושג כבוד האדם(7)'</h4>", unsafe_allow_html=True)
              st.markdown("<h3 style='text-align: right;'>לכם זה לא יקרה</h3>", unsafe_allow_html=True)
              st.markdown("<h4 style='text-align: right;'>בעניינו עשויה להיוולד עילת תביעה בגין לשון הרע מקרב השופטים, שכן הפלט מהמערכת שלנו עשוי 'לקטלג' את השופטים כשמרנים או ליברלים, 'קטלוג' נוסף עשוי להתרחש לשופטים הדנו בפסקי הדין על בסיסם מערכת הבינה המלאכותית שיצרנו למדה כצדי להעניק בסופו של דבר את התשובה הנכונה והמדויקת ביותר. כדי למנוע סיטואציה שכזו, הושמטו שמות השופטים מן המערכת, זאת ללא פגיעה בדיוק ואיכות התוצאה. השמטה זו אינה מתיישבת עם השכל היישר, שכן אינטואיטיבית אנו סבורים כי התוצאה השיפוטית, ליברלית או שמרנית תלויה באופן ישיר בהרכב השופטים, אך במהלך ההיסטוריה ראינו לא מעט פסיקות הפוכות מהצפוי, על אף שיוכו של שופט לקבוצה מסוימת. כך ראינו כי השמטת שמות השופטים לא משפיעה על דיוק התוצאה</h4>", unsafe_allow_html=True)
              st.write("--------------------------------------------------------------")
              st.write("בועז שנור 'אמת, שקר ומה שביניהם – התפתחויות בשיני לשון הרע בשנת תשע'ב' דין ודברים ח 197, 198 (התשע'ד)(2)")
              st.write("(3)תמר גדרון 'מפת תיירות הדיבה העולמית ודיני לשון הרע בישראל' המשפט טו 469, 400 (התשע'א)")
              st.write("(4)ע'א 214/89 אבנרי נ' שפירא, פ'ד מג(3) 840, 856 (1989)")
              st.write("(5)חוק איסור לשון הרע, התשכ'ה–1965")
              st.write("(6)רע'א 4447/07 מור נ' ברק אי.טי.סי. [1995] החברה לשרותי בזק בינלאומיים בע'מ, פ'ד סג(3) 664 (2010)")
              st.write("(7)רע'א 1239/19 שאול נ' חברת ניידלי תקשורת בע'מ, פס' 5–6 לפסק דינה של השופטת וילנר (פורסם באר'ש, 8.1.2020)")
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
        st.markdown("<h4 style='text-align: right;'>פרויקט זה בוצע במסגרת הקורס בינה מלאכותית ומוסר. רצינו לנצל את העובדה שהצוות מורכב ממומחי תוכן בעולם הבינה המלאכותית וכן מעולם המשפטים. לצורן כך לקחנו בעיה של חיזוי כיוון בית המשפט העליון בארה'ב ובנינו מודל בינה מלאכותית שיחזה זאת. האתר הזה מסביר את העבודה שנעשתה ומנגיש את המודל לשימוש</h4>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: right;'> על מקומה של הבינה המלאכותית בארצות הברית</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>ארצות הברית פועלת בשנים האחרונות במספר ערוצים כדי לקדם את היתרונות של טכנולוגית הבינה מלאכותית לצד התייחסותה לאתגרים האתיים. זאת כדי לאפשר לארצות הברית להמשיך ולהתברג כמעצמה בתחום הבינה המלאכותית</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>תחילה, ארצות הברית הפעילה מספר מחקרים שתפקידם הוא מיקסום השילוב בין טכנולוגיה ומוסר. כך כבר בשנת 2018, דארפ'א במסגרת תוכנית הסברתית, ניסתה לעזור למשתמשים להבין את אופן קבלת ההחלטות של מערכות הבינה המלאכותית, זאת ללא פגיעה ברמת הביצוע של המערכות. בנוסף ניתן לראות מחקר של הקרן הלאומית למדע יחד עם אמזון, שמטרתו היא מיקוד בהוגנות מערכות הבינה המלאכותית, ולשם כך הם חקרו מספר סוגיות: שקיפות, הסברתיות, אחריות, פוטנציאל להטיה, השפעות שליליות, התקדמות אלגוריתמית ויעדי הגינות(1)</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>באוקטובר 2019 פרסמה הוועדה המייעצת לחדשנות וביטחו המלצות לשימוש אתי בבינה מלאכותית. ההמלצות כוללות חמישה עקרונות אתיים לייצור טכנולוגיות המבוססות על בינה מלאכותית: אחריות, שוויון, יכולות מעקב והבנה של הטכנולוגיה, אמינות ויכולת משילות. בנוסף המסמך מספק המלצות בתחום בניהן: הרחבת המחקר להטמעה ראויה של עקרונות אתיים, השקעה במחקר, הגדרת מדדים לאמינות מערכות בינה מלאכותית, יצירת טכניקות להערכה של מערכות בינה מלאכותית, ומחקר ספציפי בתחומי האבטחה(2)</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: right;'>מאוחר יותר בתחילת שנת 2020 פורסמו קווים מנחים לרגולציה על מערכות בינה מלאכותית, על ידי הבית הלבן. כאשר במרכז עמד הרצון ליצור גישות אמינות לאימות מערכות המבוססות על בינה מלאכותית. הקווים המנחים כוללים מספר עקרונות אשר צריכים לבסס את הרגולציה בתחום: אמון הציבור בבינה מלאכותית, שיתוף הציבור, יושרה מדעית ואיכות מידע, הערכת וניהול סיכונים, עלות ותועלת, גמישות, הוגנות ואי אפליה, גילוי נאות ושקיפות להגברת אמון הציבור, בטיחות וביטחון ותיאום בין סוכנויות. לצד העקרונות הרגולטורים ישנם עקרונות לא רגולטורים להטמעת הבינה המלאכותית בצורה הטובה ביותר: יצירת תוכניות וניסויים לשם פיתוח סטנדרטים וולונטריים  שיאפשרו ניהול סיכוני פיתוח באופן אדפטיבי יותר. לקראת סוף אותה שנה פרסמו הנחיות לממשל הפדרלי כדי לאפשר שימוש אמין במערכות בינה מלאכותית(3)</h4>", unsafe_allow_html=True)
        st.write("--------------------------------------------------------------") 
        st.write("(1) Dr. Matt Turek, Explainable Artificial Intelligence (XAI), DARPA [link](https://www.darpa.mil/program/explainable-artificial-intelligence)")
        st.write("(2) 'AI Principles: Recommendations on the Ethical Use of Artificial Intelligence by the Department of Defense', Defense Innovation Board, October 2019.")
        st.write("(3) Russell T. Vought, Memorandum for the Heads of Executive Departments and Agencies [link](https://www.whitehouse.gov/wp-content/uploads/2020/01/Draft-OMB-Memo-on-Regulation-of-AI-1-7-19.pdf)")
    elif app_mode == "Show Instructions":
        st.header("The application includes following parts:")
        st.subheader('Run Prediction:')
        st.markdown('You insert your case parameters and get model prediction for supreme court direction. Here is video demo:')
        video_file = open('RunPredictionDemo.mp4', 'rb')
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
