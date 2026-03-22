import streamlit as st
import adawat.adaat

# ==========================================
# 1. إعدادات الصفحة وتنسيق الواجهة (RTL)
# ==========================================
st.set_page_config(page_title="تطبيق مكتبة أدوات الشامل", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    /* توجيه النصوص من اليمين لليسار */
    .stApp { direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif; }
    .stTextArea textarea { direction: rtl; text-align: right; font-size: 18px;}
    .css-1d391kg { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ التطبيق الشامل لمكتبة أدوات (Adawat)")
st.write("هذا التطبيق يجمع كل خصائص مكتبة أدوات لمعالجة النصوص العربية.")
st.divider()

# ==========================================
# 2. الشريط الجانبي (Sidebar) لاختيار الأقسام
# ==========================================
st.sidebar.header("أقسام المعالجة")
category = st.sidebar.selectbox("اختر القسم المطلوب:", [
    "1. التشكيل وإزالته (Tashkeel)",
    "2. التحويل والنقحرة (Transformation)",
    "3. التحليل والتوليد (Analysis & Generation)",
    "4. الاستخلاص (Extraction)",
    "5. متفرقات (Divers)"
])

# ==========================================
# 3. واجهة إدخال النص الرئيسي
# ==========================================
user_text = st.text_area("أدخل النص العربي (أو اللاتيني حسب نوع العملية):", height=150)

# ==========================================
# 4. المعالجة بناءً على القسم المختار
# ==========================================

# ----------------- القسم الأول: التشكيل -----------------
if category == "1. التشكيل وإزالته (Tashkeel)":
    st.subheader("تشكيل النص وإزالة الحركات")
    tashkeel_action = st.radio("اختر العملية:", [
        "تشكيل النص (Tashkeel)", 
        "اختزال الحركات (Reduce)", 
        "إزالة التشكيل (Strip)"
    ])
    
    last_mark = st.checkbox("تفعيل تشكيل أواخر الكلمات (الإعراب)", value=True)
    
    if st.button("تنفيذ العملية"):
        if user_text.strip():
            try:
                if tashkeel_action == "تشكيل النص (Tashkeel)":
                    result = adawat.adaat.tashkeel_text(user_text, last_mark)
                elif tashkeel_action == "اختزال الحركات (Reduce)":
                    result = getattr(adawat.adaat, 'reduce', lambda x: "الوظيفة قيد التطوير")(user_text)
                elif tashkeel_action == "إزالة التشكيل (Strip)":
                    result = getattr(adawat.adaat, 'strip', lambda x: "الوظيفة قيد التطوير")(user_text)
                
                st.success("النتيجة:")
                st.code(result, language="text")
            except AttributeError as e:
                st.error(f"عذراً، الدالة غير متوفرة بهذا الاسم الدقيق في النسخة الحالية: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الثاني: التحويل -----------------
elif category == "2. التحويل والنقحرة (Transformation)":
    st.subheader("تحويل النصوص والنقحرة")
    trans_action = st.radio("اختر العملية:", [
        "نقحرة إلى اللاتينية (Romanize)", 
        "تعريب نص لاتيني (Arabize)", 
        "قلب النص (Inverse)", 
        "التفقيط: تحويل الأرقام لنصوص (Numbers to words)",
        "تنميط النص (Normalize)",
        "فك تشابك الحروف (Unshape)"
    ])
    
    if st.button("تنفيذ العملية"):
        if user_text.strip():
            try:
                # استخدام getattr لتجنب توقف التطبيق إذا اختلف اسم الدالة برمجياً عن الوثائق
                if "Romanize" in trans_action:
                    result = adawat.adaat.romanize(user_text)
                elif "Arabize" in trans_action:
                    result = adawat.adaat.arabize(user_text)
                elif "Inverse" in trans_action:
                    result = adawat.adaat.inverse(user_text)
                elif "Numbers to words" in trans_action:
                    result = adawat.adaat.numbers_to_words(user_text)
                elif "Normalize" in trans_action:
                    result = adawat.adaat.normalize(user_text)
                elif "Unshape" in trans_action:
                    result = adawat.adaat.unshape(user_text)
                
                st.success("النتيجة:")
                st.code(result, language="text")
            except AttributeError as e:
                st.error(f"عذراً، الدالة غير متوفرة بهذا الاسم الدقيق في النسخة الحالية: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الثالث: التحليل -----------------
elif category == "3. التحليل والتوليد (Analysis & Generation)":
    st.subheader("التحليل الصرفي وتجزئة الكلمات")
    analysis_action = st.radio("اختر العملية:", [
        "تحليل صرفي (Stem)", 
        "تجزئة النص إلى كلمات (Tokenize)", 
        "تصنيف الكلمات (Wordtag)", 
        "توليد أشكال الكلمة (Affixate)"
    ])
    
    if st.button("تنفيذ العملية"):
        if user_text.strip():
            try:
                if "Stem" in analysis_action:
                    result = adawat.adaat.stem(user_text)
                elif "Tokenize" in analysis_action:
                    result = adawat.adaat.tokenize(user_text)
                elif "Wordtag" in analysis_action:
                    result = adawat.adaat.wordtag(user_text)
                elif "Affixate" in analysis_action:
                    result = adawat.adaat.affixate(user_text)
                
                st.success("النتيجة:")
                st.write(result) # نستخدم write لأن النتيجة قد تكون قائمة (List)
            except AttributeError as e:
                st.error(f"عذراً، الدالة غير متوفرة بهذا الاسم الدقيق في النسخة الحالية: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الرابع: الاستخلاص -----------------
elif category == "4. الاستخلاص (Extraction)":
    st.subheader("استخلاص البيانات من النص")
    extract_action = st.radio("اختر العملية:", [
        "استخلاص المتلازمات اللفظية (Collocation)", 
        "كشف اللغات في النص (Language)", 
        "استخلاص المسميات (Named Entities)", 
        "استخلاص العبارات العددية (Numbered Clauses)"
    ])
    
    if st.button("تنفيذ العملية"):
        if user_text.strip():
            try:
                if "Collocation" in extract_action:
                    result = adawat.adaat.collocation(user_text)
                elif "Language" in extract_action:
                    result = adawat.adaat.language(user_text)
                elif "Named" in extract_action:
                    result = adawat.adaat.named(user_text)
                elif "Numbered" in extract_action:
                    result = adawat.adaat.numbered(user_text)
                
                st.success("النتيجة:")
                st.write(result)
            except AttributeError as e:
                st.error(f"عذراً، الدالة غير متوفرة بهذا الاسم الدقيق في النسخة الحالية: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الخامس: متفرقات -----------------
elif category == "5. متفرقات (Divers)":
    st.subheader("وظائف إضافية")
    misc_action = st.radio("اختر العملية:", [
        "ضبط قصيدة شعرية (Poetry)", 
        "توليد نص عشوائي (Random Text)"
    ])
    
    if st.button("تنفيذ العملية"):
        try:
            if "Poetry" in misc_action:
                if user_text.strip():
                    result = adawat.adaat.poetry(user_text)
                    st.success("النتيجة:")
                    st.code(result, language="text")
                else:
                    st.warning("الرجاء إدخال أبيات الشعر أولاً.")
            elif "Random" in misc_action:
                result = getattr(adawat.adaat, 'random_text', getattr(adawat.adaat, 'random', lambda: "الوظيفة غير متاحة"))()
                st.success("نص عشوائي:")
                st.code(result, language="text")
        except AttributeError as e:
            st.error(f"عذراً، الدالة غير متوفرة بهذا الاسم الدقيق في النسخة الحالية: {e}")
