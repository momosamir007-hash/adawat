import streamlit as st
import adawat.adaat as adaat

# ==========================================
# 1. إعدادات الصفحة وتنسيق الواجهة (RTL)
# ==========================================
st.set_page_config(page_title="أدوات معالجة اللغة العربية", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif; }
    .stTextArea textarea { direction: rtl; text-align: right; font-size: 18px;}
    .css-1d391kg { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ التطبيق الشامل لمكتبة أدوات (Adawat)")
st.write("تم بناء هذا التطبيق ليتوافق 100% مع الكود المصدري الأصلي للمكتبة.")
st.divider()

# ==========================================
# 2. الشريط الجانبي (Sidebar)
# ==========================================
st.sidebar.header("أقسام المعالجة")
category = st.sidebar.selectbox("اختر القسم المطلوب:", [
    "1. التشكيل (Tashkeel)",
    "2. التحويل والنقحرة (Transformation)",
    "3. التحليل والتجزئة (Analysis)",
    "4. الاستخلاص (Extraction)",
    "5. متفرقات (Divers)"
])

# ==========================================
# 3. واجهة الإدخال
# ==========================================
user_text = st.text_area("أدخل النص أو الرقم هنا:", height=150)

# ==========================================
# 4. المعالجة بناءً على القسم المختار
# ==========================================

# ----------------- 1. التشكيل -----------------
if category == "1. التشكيل (Tashkeel)":
    st.subheader("التشكيل والتحكم بالحركات")
    action = st.radio("اختر العملية:", [
        "تشكيل النص (Tashkeel)", 
        "تشكيل مع اقتراحات (Tashkeel2)",
        "اختزال الحركات (Reduce Tashkeel)", 
        "إزالة التشكيل بالكامل (Strip Harakat)"
    ])
    
    last_mark = st.checkbox("تفعيل تشكيل أواخر الكلمات", value=True)
    mark_val = "1" if last_mark else "0"
    
    if st.button("تنفيذ"):
        if user_text.strip():
            with st.spinner("جاري المعالجة..."):
                if "تشكيل النص" in action:
                    result = adaat.tashkeel_text(user_text, mark_val)
                    st.success("النتيجة:")
                    st.code(result, language="text")
                elif "تشكيل مع اقتراحات" in action:
                    result = adaat.tashkeel2(user_text, mark_val)
                    st.success("النتيجة (بيانات القاموس):")
                    st.write(result)
                elif "اختزال" in action:
                    result = adaat.reduced_tashkeel_text(user_text)
                    st.success("النتيجة:")
                    st.code(result, language="text")
                elif "إزالة" in action:
                    result = adaat.DoAction(user_text, "StripHarakat")
                    st.success("النتيجة:")
                    st.code(result, language="text")
        else:
            st.warning("أدخل نصاً أولاً.")

# ----------------- 2. التحويل -----------------
elif category == "2. التحويل والنقحرة (Transformation)":
    st.subheader("تحويل النصوص والأرقام")
    action = st.radio("اختر العملية:", [
        "نقحرة إلى اللاتينية (Romanize)", 
        "تعريب نص لاتيني (Arabize)", 
        "التفقيط: تحويل رقم لنص (Num2Word)",
        "تنميط النص (Normalize)",
        "فك التشابك (Unshape)",
        "قلب النص (Inverse)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            if "Romanize" in action:
                result = adaat.romanize(user_text)
            elif "Arabize" in action:
                result = adaat.arabize(user_text)
            elif "Num2Word" in action:
                result = adaat.number2letters(user_text)
            elif "Normalize" in action:
                result = adaat.normalize(user_text)
            elif "Unshape" in action:
                result = adaat.DoAction(user_text, "Unshape")
            elif "Inverse" in action:
                result = adaat.inverse(user_text)
                # دالة inverse تعيد قائمة أحياناً، نجمعها كنص
                if isinstance(result, list): result = " ".join(result)
            
            st.success("النتيجة:")
            st.code(result, language="text")
        else:
            st.warning("أدخل نصاً أو رقماً أولاً.")

# ----------------- 3. التحليل -----------------
elif category == "3. التحليل والتجزئة (Analysis)":
    st.subheader("التحليل الصرفي وتصنيف الكلمات")
    action = st.radio("اختر العملية:", [
        "تحليل صرفي خفيف (Light Stemming)", 
        "تجزئة لكلمات (Tokenize)", 
        "تصنيف الكلمات (Wordtag)",
        "توليد أشكال الكلمة (Affixate)",
        "تقطيع النص لجمل قصيرة (Chunk)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            with st.spinner("جاري التحليل..."):
                if "Light Stemming" in action:
                    result = adaat.light_stemmer(user_text)
                    st.table(result)
                elif "Tokenize" in action:
                    result = adaat.tokenize(user_text)
                    st.write(result)
                elif "Wordtag" in action:
                    result = adaat.wordtag(user_text)
                    st.table(result)
                elif "Affixate" in action:
                    result = adaat.affixate(user_text)
                    st.write(result)
                elif "Chunk" in action:
                    result = adaat.chunksplit(user_text)
                    for i, chunk in enumerate(result):
                        st.write(f"**قطعة {i+1}:** {chunk}")
        else:
            st.warning("أدخل نصاً أولاً.")

# ----------------- 4. الاستخلاص -----------------
elif category == "4. الاستخلاص (Extraction)":
    st.subheader("استخلاص البيانات والكيانات من النص")
    action = st.radio("اختر العملية:", [
        "المتلازمات اللفظية (Collocations)", 
        "المسميات والأعلام (Named Entities)", 
        "العبارات العددية (Numbered)",
        "اكتشاف اللغات (Language Detect)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            if "Collocations" in action:
                result = adaat.show_collocations(user_text)
                st.markdown(result, unsafe_allow_html=True)
            elif "Named Entities" in action:
                result = adaat.extractNamed(user_text)
                st.markdown(result, unsafe_allow_html=True)
            elif "Numbered" in action:
                result = adaat.extractNumbered(user_text)
                st.markdown(result, unsafe_allow_html=True)
            elif "Language" in action:
                result = adaat.segment_language(user_text)
                st.table([{"اللغة": lang, "النص": txt} for lang, txt in result])
        else:
            st.warning("أدخل نصاً أولاً.")

# ----------------- 5. متفرقات -----------------
elif category == "5. متفرقات (Divers)":
    st.subheader("تنسيق الشعر وتوليد نصوص")
    action = st.radio("اختر العملية:", [
        "تنسيق شعر عمودي (Poetry)", 
        "نص عشوائي (Random Text)"
    ])
    
    if st.button("تنفيذ"):
        if "Poetry" in action:
            if user_text.strip():
                # دالة justify_poetry تعتمد على التاب (\t) كفاصل بين الشطرين
                st.info("ملاحظة: تأكد من استخدام زر (Tab) في الكيبورد للفصل بين الشطر الأول والثاني.")
                result = adaat.justify_poetry(user_text)
                for row in result:
                    if len(row) >= 2:
                        col1, col2 = st.columns(2)
                        with col2: st.markdown(f"<h4 style='text-align:center;'>{row[0]}</h4>", unsafe_allow_html=True)
                        with col1: st.markdown(f"<h4 style='text-align:center;'>{row[1]}</h4>", unsafe_allow_html=True)
            else:
                st.warning("أدخل بيت الشعر أولاً.")
        elif "Random" in action:
            result = adaat.random_text()
            st.success("نص عشوائي للتجربة:")
            st.code(result, language="text")
