import streamlit as st
import pyarabic.araby as araby
import pyarabic.number as number
import mishkal.tashkeel
import qalsadi.lemmatizer
import tashaphyne.stemming

# ==========================================
# 1. إعدادات الصفحة وتنسيق الواجهة (RTL)
# ==========================================
st.set_page_config(page_title="التطبيق الشامل لمعالجة اللغة العربية", page_icon="🛠️", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif; }
    .stTextArea textarea { direction: rtl; text-align: right; font-size: 18px;}
    .css-1d391kg { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ التطبيق الشامل لمعالجة النصوص العربية")
st.write("يستخدم هذا التطبيق الحزمة الكاملة لأدوات طه زروقي (PyArabic, Qalsadi, Tashaphyne, Mishkal).")
st.divider()

# ==========================================
# 2. الشريط الجانبي (Sidebar)
# ==========================================
st.sidebar.header("أقسام المعالجة")
category = st.sidebar.selectbox("اختر القسم المطلوب:", [
    "1. التشكيل وإزالة الحركات",
    "2. التحويل والتفقيط",
    "3. التحليل الصرفي والتجذير (Stemming)",
    "4. التقطيع والاستخلاص",
    "5. متفرقات (تنسيق الشعر)"
])

# ==========================================
# 3. إدخال النص
# ==========================================
user_text = st.text_area("أدخل النص العربي أو الأرقام هنا:", height=150)

# ==========================================
# 4. المعالجة بناءً على القسم المختار
# ==========================================

# ----------------- القسم الأول: التشكيل -----------------
if category == "1. التشكيل وإزالة الحركات":
    st.subheader("التشكيل الآلي وإزالة الحركات")
    action = st.radio("اختر العملية:", ["تشكيل النص (Mishkal)", "إزالة التشكيل بالكامل (Strip)"])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            with st.spinner("جاري المعالجة..."):
                if action == "تشكيل النص (Mishkal)":
                    vocalizer = mishkal.tashkeel.TashkeelClass()
                    result = vocalizer.tashkeel(user_text)
                else:
                    result = araby.strip_tashkeel(user_text)
            st.success("النتيجة:")
            st.code(result, language="text")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الثاني: التحويل -----------------
elif category == "2. التحويل والتفقيط":
    st.subheader("تحويل الأرقام وتنميط الحروف")
    action = st.radio("اختر العملية:", [
        "التفقيط (تحويل الأرقام إلى نصوص)", 
        "تنميط النص (توحيد الهمزات والألفات)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            if action == "التفقيط (تحويل الأرقام إلى نصوص)":
                try:
                    num = int(user_text.strip())
                    result = number.int2word(num)
                    st.success("النتيجة:")
                    st.code(result, language="text")
                except ValueError:
                    st.error("الرجاء إدخال أرقام صحيحة فقط (مثال: 2024).")
            else:
                result = araby.normalize_hamza(user_text)
                result = araby.normalize_alef(result)
                st.success("النتيجة:")
                st.code(result, language="text")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الثالث: التحليل الصرفي -----------------
elif category == "3. التحليل الصرفي والتجذير (Stemming)":
    st.subheader("استخراج الجذور والتحليل الصرفي")
    action = st.radio("اختر العملية:", [
        "التجذير الخفيف (Light Stemming - Tashaphyne)", 
        "الرد إلى الأصل (Lemmatization - Qalsadi)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            words = araby.tokenize(user_text)
            results = []
            
            with st.spinner("جاري التحليل..."):
                if "Light Stemming" in action:
                    stemmer = tashaphyne.stemming.ArabicLightStemmer()
                    for w in words:
                        stem = stemmer.light_stem(w)
                        root = stemmer.get_root()
                        results.append({"الكلمة": w, "الجذع": stem, "الجذر": root})
                else:
                    lemmer = qalsadi.lemmatizer.Lemmatizer()
                    for w in words:
                        lemma = lemmer.lemmatize(w)
                        results.append({"الكلمة": w, "الأصل (Lemma)": lemma})
            
            st.success("النتيجة:")
            st.table(results)
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الرابع: التقطيع والاستخلاص -----------------
elif category == "4. التقطيع والاستخلاص":
    st.subheader("تقطيع الجمل واستخراج الكلمات")
    action = st.radio("اختر العملية:", [
        "تقطيع النص إلى جمل (Sentence Tokenize)", 
        "استخراج الحروف العربية فقط (تصفية النص)"
    ])
    
    if st.button("تنفيذ"):
        if user_text.strip():
            if "جمل" in action:
                # فصل النص إلى جمل بناءً على علامات الترقيم
                sentences = araby.sentence_tokenize(user_text)
                st.success(f"تم العثور على {len(sentences)} جملة:")
                for i, s in enumerate(sentences):
                    st.write(f"**{i+1}.** {s}")
            else:
                # فلترة الحروف العربية فقط
                result = ''.join([char for char in user_text if araby.is_arabicrange(char) or char == ' '])
                st.success("النتيجة:")
                st.code(result, language="text")
        else:
            st.warning("الرجاء إدخال نص أولاً.")

# ----------------- القسم الخامس: متفرقات (الشعر) -----------------
elif category == "5. متفرقات (تنسيق الشعر)":
    st.subheader("تنسيق الشعر العمودي")
    st.info("أدخل بيت الشعر وافصل بين الشطرين بعلامة التسطير (_) أو النجمة (*) أو الشباك (#).")
    
    if st.button("تنسيق القصيدة"):
        if user_text.strip():
            # البحث عن الفاصل لتنسيق الشعر
            separator = '_' if '_' in user_text else ('*' if '*' in user_text else '#')
            
            if separator in user_text:
                parts = user_text.split(separator)
                col1, col2 = st.columns(2)
                with col2: # الشطر الأول يميناً
                    st.markdown(f"<h4 style='text-align: center;'>{parts[0].strip()}</h4>", unsafe_allow_html=True)
                with col1: # الشطر الثاني يساراً
                    st.markdown(f"<h4 style='text-align: center;'>{parts[1].strip()}</h4>", unsafe_allow_html=True)
            else:
                st.warning("لم يتم العثور على فاصل. يرجى استخدام _ أو * أو # بين الشطرين.")
        else:
            st.warning("الرجاء إدخال بيت شعر أولاً.")
