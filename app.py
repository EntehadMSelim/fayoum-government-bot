import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="شات بوت الشهر العقاري الذكي - الفيوم", page_icon="🤖", layout="centered")

# دمج الـ API Key الخاص بكِ مباشرة لتفعيل الذكاء الاصطناعي (Gemini)
API_KEY = "AQ.Ab8RN6JZK8npfsOCkkWcwfKMhR8LOQeQtxyp4d-NP8ndTOW3zA"
genai.configure(api_key=API_KEY)

# دالة مرنة وقوية لقراءة الداتا سيت الخاصة بكِ
@st.cache_data
def load_fayoum_data():
    try:
        df = pd.read_csv("fayoum_clean_dataset.csv", sep=None, engine='python', encoding="utf-8")
        office_translation = {
            "Youssef El-Seddik Office": "مكتب يوسف الصديق",
            "Fayoum University Office": "مكتب توثيق جامعة الفيوم",
            "Fayoum Model Office": "مكتب الفيوم النموذجي",
            "Itsaa Office": "مكتب إطسا",
            "Al-Breid El-Gon Office": "مكتب البريد العام",
            "Senores Office": "مكتب سنورس",
            "Tamiya Office": "مكتب طامية",
            "El Fayoum Al-Dawahy Office": "مكتب الضواحي",
            "Abshaway Office": "مكتب إبشواي"
        }
        if 'Office' in df.columns:
            df['Office_Arabic'] = df['Office'].map(office_translation).fillna(df['Office'])
        else:
            df['Office_Arabic'] = df.iloc[:, 0]
        return df
    except Exception as e:
        st.error(f"⚠️ مشكلة في قراءة ملف البيانات: {e}")
        return None

df_transactions = load_fayoum_data()

# عنوان التطبيق الرئيسي
st.title("⚖️ مساعد الشهر العقاري الذكي المدعوم بـ Gemini")
st.write("شات بوت تفاعلي حقيقي يعتمد على فهم النصوص وتحليل البيانات لايف بمحافظة الفيوم.")

# القائمة الجانبية للفصل بين الأدوار
st.sidebar.header("⚙️ بوابة الدخول")
user_role = st.sidebar.radio("اختر صفة المستخدم:", ("مواطن (استعلامات الفيوم)", "صاحب القرار (إدارة الفيوم)"))

# باسوورد المدير الثابت في القائمة الجانبية لمنع الاختفاء
password = ""
if user_role == "صاحب القرار (إدارة الفيوم)":
    st.sidebar.markdown("---")
    password = st.sidebar.text_input("🔒 كلمة سر المدير:", type="password")

# ----------------- 1. شات بوت المواطن الذكي (محادثة حرة) -----------------
if user_role == "مواطن (استعلامات الفيوم)":
    st.subheader("🤖 اسأل ذكاء اصطناعي حقيقي عن خدمات الفيوم")
    st.info("اكتبي أي سؤال بالعامية المصرية حول مواعيد الفروع، السيارات المتنقلة، أو الأوراق المطلوبة وسيجيبك الذكاء الاصطناعي فوراً.")
    
    # سياق معرفي لتوجيه ذكاء Gemini للرد بدقة كابن البلد في الفيوم
    fayoum_context = """
    أنت مساعد ذكي مخصص لخدمة مواطني محافظة الفيوم في الشهر العقاري. معلوماتك الأساسية هي:
    - المكاتب التي تعمل فترتين (صباحي ومسائي): الضواحي، النموذجي، إطسا، سنورس، إبشواي، طامية.
    - مكتب نادي القضاة يعمل طوال الأسبوع عدا الإثنين والثلاثاء.
    - مكتب جامعة الفيوم يعمل الإثنين والثلاثاء فقط.
    - مكاتب فترة مسائية فقط: فرع أورانج، ونادي المحافظة.
    - السيارات المتنقلة بالفيوم: سيارة 25، وسيارة خدمات مصر 21.
    - ينصح دائماً بالحجز عبر تطبيق أرقم الرقمي أو بوابة مصر الرقمية.
    أجب على أسئلة المواطن بلغة عامية مصرية مهذبة ومختصرة بناءً على هذه المعلومات.
    """
    
    citizen_query = st.text_input("اكتبي سؤالكِ هنا بكل حرية (مثال: عايزة أعمل توثيق شقة، أو إيه مواعيد مكتب جامعة الفيوم؟)...")
    
    if citizen_query:
        with st.spinner("🤖 جاري التفكير والرد..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                full_prompt = f"{fayoum_context}\n\nسؤال المواطن: {citizen_query}\nالرد:"
                response = model.generate_content(full_prompt)
                st.success(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

# ----------------- 2. شات بوت المدير المتحدث مع البيانات (تحليل ومقترحات حرة) -----------------
elif user_role == "صاحب القرار (إدارة الفيوم)":
    st.subheader("📊 لوحة تحليل البيانات الذكية للمديرين")
    
    if password == "admin123":
        st.success("🔓 تم تسجيل الدخول بنجاح - إدارة شهر عقاري الفيوم.")
        
        if df_transactions is not None:
            st.write("### 💬 ناقشي واطلبي مقترحات وتوصيات من الذكاء الاصطناعي بناءً على ملفكِ:")
            st.caption("أمثلة لأسئلة حرة: (اقترح لي خطة لتخفيف التكدس بناءً على الحالات المعلقة؟ / ما هي الخدمة الأكثر تعطيلاً للعمل؟ / لخص لي كفاءة المكاتب الحالية)")
            
            # تجهيز ملخص الأرقام الحية من الداتا سيت ليمسكها الذكاء الاصطناعي ويحللها
            total_rows = len(df_transactions)
            office_counts = df_transactions['Office_Arabic'].value_counts().to_string()
            status_counts = df_transactions['Status'].value_counts().to_string()
            
            data_context = f"""
            أنت مستشار إداري وخبير تحليل بيانات لشهر عقاري الفيوم. أمامك ملخص الأرقام الحقيقية والحية من ملف البيانات الحالي:
            - إجمالي المعاملات المسجلة بالمحافظة: {total_rows} معاملة.
            - حجم المعاملات والإقبال التراكمي في كل مكتب:
            {office_counts}
            - حالات المعاملات الحالية في المنظومة (مكتملة أو معلقة):
            {status_counts}
            
            بناءً على هذه الأرقام والبيانات الحقيقية، قم بالإجابة على استفسارات المدير، واقترح عليه حلولاً تنظيمية وتوصيات ذكية لتطوير فروع الفيوم بشكل ممتاز.
            """
            
            admin_query = st.text_input("اكتبي سؤالكِ الإداري أو اطلبي مقترحات التطوير هنا:")
            
            if admin_query:
                with st.spinner("📊 جاري رصد الأرقام وصياغة التوصيات الذكية..."):
                    try:
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        full_prompt = f"{data_context}\n\nسؤال المدير: {admin_query}\nالتقرير والمقترحات الإدارية:"
                        response = model.generate_content(full_prompt)
                        st.info(response.text)
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء التحليل: {e}")
        else:
            st.error("ملف البيانات غير موجود أو لم يتم قراءته بشكل صحيح.")
            
    elif password != "":
        st.sidebar.error("❌ كلمة السر خاطئة!")
