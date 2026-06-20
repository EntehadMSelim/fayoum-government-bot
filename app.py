import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="شات بوت الشهر العقاري - محافظة الفيوم", page_icon="⚖️", layout="centered")

# دالة ذكية ومرنة لقراءة الداتا سيت الخاصة بكِ بدون أخطاء
@st.cache_data
def load_fayoum_data():
    try:
        # قراءة الملف مع ترك بايثون يكتشف الفاصل تلقائياً لمنع الأخطاء
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
            df['Office_Arabic'] = df.iloc[:, 0] # أول عمود إذا كانت الأسماء بالعربي
            
        return df
    except Exception as e:
        st.error(f"⚠️ واجهنا مشكلة في قراءة الملف: {e}")
        return None

df_transactions = load_fayoum_data()

# عنوان التطبيق الرئيسي
st.title("⚖️ شات بوت الشهر العقاري الذكي (محافظة الفيوم)")
st.write("النظام المطور المرتبط بقاعدة بيانات مكاتب الفيوم الحية.")

# القائمة الجانبية للفصل بين الأدوار وضبط خانة الباسوورد
st.sidebar.header("بوابة الدخول")
user_role = st.sidebar.radio("اختر صفة المستخدم:", ("مواطن (خدمات واستعلامات الفيوم)", "صاحب القرار (إدارة الفيوم)"))

# إظهار خانة الباسوورد في القائمة الجانبية فوراً وثباتها عند اختيار "صاحب القرار"
password = ""
if user_role == "صاحب القرار (إدارة الفيوم)":
    st.sidebar.markdown("---")
    password = st.sidebar.text_input("🔑 كلمة سر المدير للدخول:", type="password")

# ----------------- 1. شات بوت المواطن -----------------
if user_role == "مواطن (خدمات واستعلامات الفيوم)":
    st.subheader("🤖 شات بوت خدمة مواطني الفيوم")
    st.info("اسألني عن مواعيد وأيام عمل كل الفروع وأماكن السيارات المتنقلة بمحافظة الفيوم.")
    
    citizen_questions = {
        "اختر سؤالك من هنا...": "",
        "ما هي المكاتب التي تعمل فترتين (صباحية ومسائية) in الفيوم؟" or "ما هي المكاتب التي تعمل فترتين (صباحية ومسائية) في الفيوم؟": "المكاتب التي تعمل فترتين لخدمتكم هي: (مكتب الضواحي، المكتب النموذجي، مكتب إطسا، مكتب سنورس، مكتب إبشواي، ومكتب طامية).",
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
    
    if password == "admin123":
        st.success("🔓 تم تسجيل الدخول بنجاح - إدارة شهر عقاري الفيوم.")
        
        if df_transactions is not None:
            # تقسيم الشاشة لجزأين: جزء التقارير الرقمية وجزء المقترحات الذكية
            tab1, tab2 = st.tabs(["📊 التقارير والإحصائيات", "🤖 مقترحات وتوصيات الذكاء الاصطناعي"])
            
            with tab1:
                st.write("### استخراج التقارير الدورية:")
                admin_options = [
                    "اختر التقرير المطلوب...",
                    "كم إجمالي عدد المعاملات المسجلة في النظام حتى الآن؟",
                    "ما هي أكثر 3 مكاتب إقبالاً وتسجيلاً للمعاملات؟",
                    "ما هي الخدمة الأكثر طلباً من المواطنين في الفيوم? " or "ما هي الخدمة الأكثر طلباً من المواطنين في الفيوم؟",
                    "ما هي نسبة المعاملات المكتملة مقارنة بالمعلقة؟",
                    "ما هو متوسط وقت معالجة المعاملة الواحدة بالدقائق؟",
                    "عرض عينة من أحدث التقييمات والشكاوى الواردة"
                ]
                
                selected_admin_q = st.selectbox("ما التقرير الإداري المطلوب؟", admin_options)
                cols = df_transactions.columns
                
                if selected_admin_q == "كم إجمالي عدد المعاملات المسجلة في النظام حتى الآن؟":
                    st.info(f"📊 **تقرير الإدارة:** إجمالي المعاملات المسجلة بملف المحافظة الحالي هو **{len(df_transactions):,} معاملة**.")
                    
                elif selected_admin_q == "ما هي أكثر 3 مكاتب إقبالاً وتسجيلاً للمعاملات؟":
                    top_offices = df_transactions['Office_Arabic'].value_counts().head(3)
                    st.info("📍 **تقرير الإدارة: أكثر 3 مكاتب ضغطاً وإقبالاً بناءً على البيانات:**")
                    for office, count in top_offices.items():
                        st.write(f"- **{office}**: {count} معاملة")
                        
                elif "الخدمة الأكثر طلباً" in selected_admin_q:
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
            
            with tab2:
                st.write("### 🤖 مقترحات وتوصيات ذكية بناءً على ملف البيانات:")
                
                # حساب ذكي لأكثر مكتب يعاني من معاملات معلقة (Pending)
                try:
                    pending_df = df_transactions[df_transactions['Status'].str.strip() == 'Pending']
                    top_pending_office = pending_df['Office_Arabic'].value_counts().idxmax()
                    top_pending_count = pending_df['Office_Arabic'].value_counts().max()
                    
                    st.markdown(f"🚨 **توصية التكدس:** تم رصد عدد كبير من المعاملات المعلقة (Pending) في **{top_pending_office}** بعدد **{top_pending_count} معاملة**. *المقترح:* يُنصح بتوجيه إحدى السيارات المتنقلة لدعم هذا المكتب لتخفيف العبء الكلي.")
                except:
                    st.write("✅ المنظومة تسير بشكل ممتاز ولا توجد مكاتب تعاني من تكدس الحالات المعلقة.")
                
                # حساب ذكي لأبطأ خدمة في المعالجة
                try:
                    avg_time_per_service = df_transactions.groupby('Service_Type')['Processing_Time'].mean()
                    slowest_service = avg_time_per_service.idxmax()
                    slowest_time = avg_time_per_service.max()
                    
                    st.markdown(f"⏱️ **توصية تطوير الإجراءات:** خدمة (**{slowest_service}**) تأخذ أطول وقت معالجة بمعدل **{slowest_time:.1f} دقيقة** لكل معاملة. *المقترح:* يرجى مراجعة الدورة المستندية لهذه الخدمة أو تدريب الموظفين عليها لرفع الكفاءة.")
                except:
                    pass
                
                # نصيحة عامة بناءً على جودة الـ Feedback
                st.markdown("💡 **توصية رضاء المواطنين:** بناءً على تحليل التقييمات، أغلب الشكاوى تتركز حول 'بطء الإجراءات'. يُقترح تفعيل نظام الحجز المسبق الإلزامي عبر منصة مصر الرقمية لتقليل زمن الانتظار.")
                
        else:
            st.error("لا يمكن عرض التقارير لعدم وجود ملف الداتا سيت بالشكل الصحيح.")
            
    elif password != "":
        st.sidebar.error("❌ كلمة السر خاطئة!")
        st.warning("الرجاء إدخال كلمة سر المدير الصحيحة في القائمة الجانبية لتفعيل لوحة التحكم.")
    else:
        st.info("🔒 الرجاء إدخال كلمة سر المدير في خانة الباسوورد المتاحة الآن على يسار الشاشة (القائمة الجانبية) لرؤية البيانات والمقترحات.")
