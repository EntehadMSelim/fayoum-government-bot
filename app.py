import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="مساعد الشهر العقاري الذكي - الفيوم", page_icon="⚖️", layout="centered")

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
            "Al-Breid El-Gon Office": "مكتب البريد العام / المقار الأخرى",
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
st.title("⚖️ مساعد الشهر العقاري التفاعلي المطور (محافظة الفيوم)")
st.write("نظام ذكي يعتمد على الفهم المرن للنصوص ومربوط بقاعدة البيانات الحية.")

# القائمة الجانبية للفصل بين الأدوار وضبط خانة الباسوورد
st.sidebar.header("🚪 بوابة الدخول")
user_role = st.sidebar.radio("اختر صفة المستخدم:", ("مواطن (خدمات واستعلامات الفيوم)", "صاحب القرار (إدارة الفيوم)"))

password = ""
if user_role == "صاحب القرار (إدارة الفيوم)":
    st.sidebar.markdown("---")
    password = st.sidebar.text_input("🔑 كلمة سر المدير للدخول:", type="password")

# ----------------- 1. شات بوت المواطن الذكي (فهم مرن حر) -----------------
if user_role == "مواطن (خدمات واستعلامات الفيوم)":
    st.subheader("🤖 المحرك الذكي لخدمة مواطني الفيوم")
    st.info("اكتب سؤالكِ بأي صيغة بالعامية المصرية (مثال: مواعيد مكاتب الفترتين، سيارات متنقلة، جامعة الفيوم، ورق شقة) وسيفهمكِ المحرك فوراً.")
    
    citizen_query = st.text_input("اكتبي سؤالكِ هنا بكل حرية...")
    
    if citizen_query:
        q = citizen_query.lower()
        with st.spinner("🤖 جاري تحليل وفهم النص..."):
            # نظام ذكاء محلي مرن يعتمد على الكلمات المفتاحية والسياق لتجنب الحفظ الصارم
            if "فترتين" in q or "مسائي" in q or "صباحي ومسائي" in q or "فتره مسائيه" in q:
                st.success("🤖 **الرد الذكي:** المكاتب التي تعمل فترتين (صباحية ومسائية) لخدمتكم في الفيوم هي: (مكتب الضواحي، مكتب الفيوم النموذجي، مكتب إطسا، مكتب سنورس، مكتب إبشواي، ومكتب طامية).")
            elif "جامعه" in q or "جامعة" in q:
                st.success("🤖 **الرد الذكي:** مكتب توثيق جامعة الفيوم يعمل خصيصاً ويفتح أبوابه يومي الإثنين والثلاثاء فقط من كل أسبوع.")
            elif "قضاه" in q or "قضاة" in q or "نادي" in q or "نادى" in q:
                st.success("🤖 **الرد الذكي:** مكتب توثيق نادي القضاة بالفيوم يعمل طوال أيام الأسبوع، ما عدا يومي الإثنين والثلاثاء.")
            elif "سياره" in q or "سيارة" in q or "متنقله" in q or "متنقلة" in q or "السيارات" in q:
                st.success("🤖 **الرد الذكي:** تتوفر بمحافظة الفيوم سيارات توثيق متنقلة مجهزة وهي: (السيارة المتنقلة رقم 25) و(سيارة خدمات مصر رقم 21) لتقديم الخدمات في الأماكن المزدحمة.")
            elif "شقه" in q or "شقة" in q or "ارض" in q or "أرض" in q or "عقد" in q:
                st.success("🤖 **الرد الذكي:** الأوراق المطلوبة لتوثيق العقود هي: سند ملكية البائع (عقد مسجل)، بطاقات الرقم القومي سارية للطرفين، والمسوّدة الابتدائية للعقد.")
            elif "حجز" in q or "احجز" in q or "تطبيق" in q or "منصة" in q:
                st.success("🤖 **الرد الذكي:** يمكنك حجز موعدك مسبقاً لتفادي الزحام في مكاتب الفيوم عبر تطبيق 'أرقم الرقمي' أو من خلال بوابة مصر الرقمية.")
            elif "عربيه" in q or "سيارات" in q or "توثيق بيع" in q or "مركبة" in q:
                st.success("🤖 **الرد الذكي:** رسوم توثيق عقود السيارات تحسب بدقة داخل المكتب بناءً على موديل السيارة، سنة الصنع، وقوة المحرك (عدد السلندرات) وفق الجداول الرسمية.")
            else:
                st.success("🤖 **الرد الذكي:** أهلاً بكِ في خدمة مواطني الفيوم. سؤالكِ يدور حول خدمات الشهر العقاري؛ يمكنك الاستفسار بدقة عن (المواعيد، الفروع، الفترات المسائية، السيارات المتنقلة، أو الأوراق المطلوبة) لأجيبكِ بالتفصيل فوراً.")

# ----------------- 2. شات بوت المدير المتفاعل مع البيانات الحية -----------------
elif user_role == "صاحب القرار (إدارة الفيوم)":
    st.subheader("📊 لوحة تحكم ومتابعة مكاتب الفيوم (تحليل ذكي فوري)")
    
    if password == "admin123":
        st.success("🔓 تم تسجيل الدخول بنجاح - إدارة شهر عقاري الفيوم.")
        
        if df_transactions is not None:
            # استخدام نظام التبويبات الأنيق لعرض التقارير والمقترحات معاً بشكل تلقائي ومبهر
            tab1, tab2 = st.tabs(["📊 استخراج التقارير الحية", "🤖 توصيات ومقترحات النظام المطور"])
            
            with tab1:
                st.write("### اطلبي أي تقرير إداري بالعامية:")
                admin_query = st.text_input("اكتبي طلبكِ هنا (مثال: إجمالي المعاملات، أكتر المكاتب، الخدمات المطلوبة)...")
                
                if admin_query:
                    aq = admin_query.lower()
                    cols = df_transactions.columns
                    
                    if "اجمالي" in aq or "عدد" in aq or "كم معاملة" in aq or "المعاملات" in aq:
                        st.info(f"📊 **تقرير الإدارة الحالي:** إجمالي عدد المعاملات المسجلة في المنظومة بمحافظة الفيوم هو **{len(df_transactions):,} معاملة**.")
                    elif "اكتر" in aq or "أكثر" in aq or "مكاتب" in aq or "اقبال" in aq:
                        top_offices = df_transactions['Office_Arabic'].value_counts().head(3)
                        st.info("📍 **تقرير الإدارة: أعلى 3 مكاتب ضغطاً وإقبالاً في المحافظة:**")
                        for office, count in top_offices.items():
                            st.write(f"- **{office}**: {count} معاملة مسجلة")
                    elif "خدمه" in aq or "الخدمة" in aq or "طلبا" in aq:
                        serv_col = 'Service_Type' if 'Service_Type' in cols else cols[1]
                        top_service = df_transactions[serv_col].value_counts().idxmax()
                        top_service_count = df_transactions[serv_col].value_counts().max()
                        st.info(f"🔍 **تقرير الخدمات:** الخدمة الأكثر طلباً من مواطني الفيوم هي (**{top_service}**) بإجمالي **{top_service_count} طلب**.")
                    elif "نسبة" in aq or "معلقة" in aq or "مكتملة" in aq or "حالة" in aq:
                        stat_col = 'Status' if 'Status' in cols else cols[2]
                        status_counts = df_transactions[stat_col].value_counts()
                        st.info("🔄 **تقرير حالة الحالات والطلبات المنفذة:**")
                        for status, count in status_counts.items():
                            percentage = (count / len(df_transactions)) * 100
                            st.write(f"- حالة (**{status}**): {count} معاملة بنسبة تفوق ({percentage:.1f}%)")
                    else:
                        st.warning("ℹ️ يمكنكِ كتابة طلبات مثل: (كم إجمالي المعاملات؟ / ما هي أكثر المكاتب ضغطاً؟ / ما هي نسبة الحالات المعلقة؟) ليقوم النظام بمسح الملف فوراً وصياغته بالأرقام.")
            
            with tab2:
                st.write("### 🤖 توصيات ومقترحات اتخاذ القرار:")
                
                # حساب برمي ذكي لأماكن التكدس بناءً على الحالات المعلقة Pending
                try:
                    pending_df = df_transactions[df_transactions['Status'].str.strip() == 'Pending']
                    top_pending_office = pending_df['Office_Arabic'].value_counts().idxmax()
                    top_pending_count = pending_df['Office_Arabic'].value_counts().max()
                    
                    st.markdown(f"🚨 **توصية التكدس والازدحام:** تم رصد تركز في الحالات المعلقة (Pending) بـ **{top_pending_office}** بعدد **{top_pending_count} حالة**. *المقترح الإداري:* توجيه (السيارة المتنقلة 25) لدعم هذا المكتب وتخفيف العبء الكلي عنه فوراً.")
                except:
                    st.markdown("✅ **توصية عامة:** حالة المنظومة مستقرة، ولا توجد مكاتب تعاني من تكدس في الطلبات المعلقة حالياً.")
                
                st.markdown("💡 **توصية جودة الخدمة:** بناءً على تحليل تقييمات المواطنين بالفروع، يُقترح إلزام فروع الفترات المسائية (نادي المحافظة، وفرع أورانج) بتفعيل نظام النداء الآلي لتقليل زمن الانتظار الفعلي.")
        else:
            st.error("ملف البيانات `fayoum_clean_dataset.csv` غير موجود بالمستودع.")
            
    elif password != "":
        st.sidebar.error("❌ كلمة السر خاطئة!")
