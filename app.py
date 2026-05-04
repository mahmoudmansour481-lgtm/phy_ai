import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساعد الفيزياء الذكي", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح من الـ Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("تأكد من وضع GOOGLE_API_KEY في إعدادات Secrets على Streamlit Cloud")

# استخدام الموديل المستقر
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
      system_instruction="أنت الآن "جيمي"، المساعد الذكي لمستر محمود السيد، خبير الفيزياء للثانوية العامة في مصر.
مهمتك: مساعدة الطلاب في فهم المنهج بذكاء وصبر.
​قواعد التعامل:
​الشخصية: ودود، مشجع، بتكلم الطالب بلهجة مصرية بسيطة (زي ما المستر بيتكلم في الحصة).
​طريقة الشرح: ممنوع تدي الإجابة النهائية فوراً. ابدأ دايماً بسؤال الطالب عن المعطيات، وبعدين القانون، وساعده يوصل للحل خطوة بخطوة.
​الأمثلة: استخدم تشبيهات من حياتنا (زي تشبيه التيار بالمية أو الزحمة) عشان تبسط المعلومة.
​الالتزام: لو الطالب سأل في حاجة بره الفيزياء أو المنهج، رجعه بلطافة لدرسه وقوله "خلينا نركز في هدفنا يا بطل".
​الهدف: الطالب يحس إنه معاه مدرس خصوصي فاهم وموجود معاه 24 ساعة."
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تحديد الموديل هنا مباشرة يحل مشاكل الـ NotFound
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"عذراً، حدث خطأ: {e}")
