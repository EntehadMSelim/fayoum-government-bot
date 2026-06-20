import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="شات بوت الشهر العقاري - محافظة الفيوم", page_icon="⚖️", layout="centered")

# دالة ذكية ومرنة لقراءة الداتا سيت بدون أخطاء
@st.cache_data
def load_fayoum_data():
    try:
        # قراءة الملف مع ترك بايثون يكتشف الفاصل تلقائياً (sep=None) لمنع الـ ParserError
        df = pd.read_csv("fayoum_clean_dataset.csv", sep=None, engine='python', encoding="utf-8")
        
        # قاموس لترجمة أسماء المكاتب من الإنجليزية للعربية لتظهر بشكل احترافي للمدير
        office_translation = {
            "Youssef El-Seddik Office": "مكتب يوسف الصديق",
            "Fayoum University Office": "مكتب توثيق جامعة الفيوم",
            "Fayoum Model Office": "مكتب الفيوم النموذجي",
            "Itsaa Office": "مكتب إطسا",
            "Al-Breid El-Gon Office": "مكتب البريد العام / المقار الأخرى",
            "Senores Office": "مكتب سنورس",
            "Tamiya Office": "مكتب طامية",
            "El Fayoum Al-Dawahy Office": "مكتب الضواحي",
            "Abshaway Office": "مكتب إبشواي",
            "Unknown": "مكتب غير محدد / سيارات متنقلة"
        }
        if 'Office' in df.columns:
            df['Office_Arabic'] = df['Office'].map(office_translation).fillna(df['Office'])
        else:
            # إذا كانت أسماء الأعمدة بالعربي في ملفكِ أصلاً
            df['Office_Arabic'] = df.iloc[:, 0] # أول عمود
            
        return df
    except Exception as e:
        st.error(f"⚠️ واجهنا مشكلة في قراءة الملف: {e}")
        return None

df_transactions = load_fayoum_data()

# عنوان التطبيق الرئيسي
st.title("⚖️ شات بوت الشهر العقاري الذكي (محافظة الفيوم)")
st.write("النظام المطور المرتبط بقاعدة بيانات مكاتب الفيوم الحية.")

# القائمة الجانبية للفصل بين الأدوار
st.sidebar.header("بوابة الدخول")
user_role = st.sidebar.radio("اختر صفة المستخدم:", ("مواطن (خدمات واستعلامات الفيوم)", "صاحب القرار (إدارة الفيوم)"))

# ----------------- 1. شات بوت المواطن -----------------
if user_role == "مواطن (خدمات واستعلامات الفيوم)":
    st.subheader("🤖 شات بوت خدمة مواطني الفيوم")
    st.info("اسألني عن مواعيد وأيام عمل مكاتب الفيوم الـ 12 والسيارات المتنقلة.")
    
    citizen_questions = {
        "اختر سؤالك من هنا...": "",
        "ما هي المكاتب التي تعمل فترتين (صباحية ومسائية) في الفيوم؟": "المكاتب التي تعمل فترتين لخدمتكم هي: (مكتب الضواحي، المكتب النموذجي، مكتب إطسا، مكتب سنورس، مكتب إبشواي، ومكتب طامية).",
        "ما هي مواعيد وأيام عمل مكتب توثيق نادي القضاة بالفيوم؟": "مكتب توثيق نادي القضاة يعمل طوال أيام الأسبوع، ما عدا يومي الإثنين والثلاثاء.",
        "ما هي مواعيد وأيام عمل مكتب توثيق جامعة الفيوم؟": "مكتب توثيق جامعة الفيوم مخصص للعمل يومي الإثنين والثلاثاء فقط من كل أسبوع.",
        "ما هي مكاتب الفترة المسائية فقط في الفيوم؟": "المكاتب المخصصة للفترة المسائية فقط هي: (مكتب توثيق فرع أورانج، ومكتب توثيق نادي المحافظة).",
        "ما هي أرقام وأسماء سيارات التوثيق المتنقلة بالفيوم؟": "تتوفر بالمحافظة سيارتان: (السيارة المتنقلة رقم 25) و (سيارة خدمات مصر رقم 21).",
        "كيف يمكنني حجز موعد في أي مكتب بالفيوم؟": "يمكنك الحجز مسبقاً عبر تطبيق 'أرقم الرقمي' أو بوابة مصر الرقمية لتفادي الزحام قبل التوجه للمكتب.",
        "كم تبلغ رسوم توثيق عقد بيع سيارة؟": "تحسب الرسوم بناءً على موديل السيارة، سنة الصنع، وعدد السلندرات وفقاً لجدول الرسوم المحدث بالمحافظة.",
        "الأوراق المطلوبة لتوثيق عقد بيع شقة أو أرض بالفيوم؟": "سند ملكية البائع (عقد مسجل)، بطاقات الرقم القومي للطرفين سارية، وعقد البيع الابتدائي المراد توثيقه."
    }
    
    selected_q = st.selectbox("اختر سؤالك المعتاد:", list(citizen_questions.keys()))
    if selected_q != "اختر سؤالك من هنا...":
        st.success(f"**الرد:** {citizen_questions[selected_q]}")

# ----------------- 2. شات بوت المدير -----------------
elif user_role == "صاحب القرار (إدارة الفيوم)":
    st.subheader("📊 لوحة تحكم ومتابعة مكاتب الفيوم (تحليل البيانات الحية)")
    
    password = st.text_input("الرجاء إدخال كلمة سر المدير للدخول:", type="password")
    
    if password == "admin123":
        st.success("تم تسجيل الدخول بنجاح - إدارة شهر عقاري الفيوم.")
        
        if df_transactions is not None:
            admin_options = [
                "اختر التقرير المطلوب...",
                "كم إجمالي عدد المعاملات المسجلة في النظام حتى الآن؟",
                "ما هي أكثر 3 مكاتب إقبالاً وتسجيلاً للمعاملات؟",
                "ما هي الخدمة الأكثر طلباً من المواطنين في الفيوم؟",
                "ما هي نسبة المعاملات المكتملة مقارنة بالمعلقة؟",
                "ما هو متوسط وقت معالجة المعاملة الواحدة بالدقائق؟",
                "عرض عينة من أحدث التقييمات والشكاوى الواردة"
            ]
            
            selected_admin_q = st.selectbox("ما التقرير الإداري المستخرج من الداتا سيت؟", admin_options)
            
            # محاولة قراءة أسماء الأعمدة ديناميكياً لتفادي أي خطأ في التسمية
            cols = df_transactions.columns
            
            if selected_admin_q == "كم إجمالي عدد المعاملات المسجلة في النظام حتى الآن؟":
                st.info(f"📊 **تقرير الإدارة:** إجمالي المعاملات المسجلة بملف المحافظة الحالي هو **{len(df_transactions):,} معاملة**.")
                
            elif selected_admin_q == "ما هي أكثر 3 مكاتب إقبالاً وتسجيلاً للمعاملات؟":
                top_offices = df_transactions['Office_Arabic'].value_counts().head(3)
                st.info("📍 **تقرير الإدارة: أكثر 3 مكاتب ضغطاً وإقبالاً بناءً على البيانات:**")
                for office, count in top_offices.items():
                    st.write(f"- **{office}**: {count} معاملة")
                    
            elif selected_admin_q == "ما هي الخدمة الأكثر طلباً من المواطنين في الفيوم؟":
                serv_col = 'Service_Type' if 'Service_Type' in cols else cols[1]
                top_service = df_transactions[serv_col].value_counts().idxmax()
                top_service_count = df_transactions[serv_col].value_counts().max()
                st.info(f"🔍 **تقرير الإدارة:** الخدمة الأكثر طلباً هي (**{top_service}**) بإجمالي **{top_service_count} طلب**.")
                
            elif selected_admin_q == "ما هي نسبة المعاملات المكتملة مقارنة بالمعلقة؟":
                stat_col = 'Status' if 'Status' in cols else cols[2]
                status_counts = df_transactions[stat_col].value_counts()
                st.info("🔄 **تقرير حالة المنظومة:**")
                for status, count in status_counts.items():
                    percentage = (count / len(df_transactions)) * 100
                    st.write(f"- حالة (**{status}**): {count} معاملة بنسبة ({percentage:.1f}%)")
                    
            elif selected_admin_q == "ما هو متوسط وقت معالجة المعاملة الواحدة بالدقائق؟":
                time_col = 'Processing_Time' if 'Processing_Time' in cols else (cols[3] if len(cols)>3 else None)
                if time_col and pd.api.types.is_numeric_dtype(df_transactions[time_col]):
                    avg_time = df_transactions[time_col].mean()
                    st.info(f"⏱️ **تقرير الأداء الكلي:** متوسط وقت إنجاز المعاملة الواحدة هو **{avg_time:.1f} دقيقة**.")
                else:
                    st.warning("⚠️ عمود وقت المعالجة غير موجود أو يحتوي على نصوص بدلاً من الأرقام.")
                
            elif selected_admin_q == "عرض عينة من أحدث التقييمات والشكاوى الواردة":
                feed_col = 'Feedback' if 'Feedback' in cols else cols[-1]
                feedbacks = df_transactions[df_transactions[feed_col].astype(str).str.lower() != 'no feedback'][feed_col].tail(5).tolist()
                st.warning("⚠️ **آخر 5 آراء وشكاوى تم رصدها من المواطنين:**")
                if feedbacks:
                    for fb in feedbacks:
                        st.write(f"💬 {fb}")
                else:
                    st.write("لا توجد شكاوى أو تقييمات سلبية حالياً.")
        else:
            st.error("لا يمكن عرض التقارير لعدم وجود ملف الداتا سيت بالشكل الصحيح.")
            
    elif password != "":
        st.error("كلمة السر خاطئة! صلاحية الوصول خاصة بإدارة الفيوم فقط.")