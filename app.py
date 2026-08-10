import streamlit as st
from database.db_manager import get_store_products, add_product
from google import genai

st.set_page_config(page_title="مساعد التسوق الذكي", page_icon="🛍", layout="centered")

# ضع مفتاح الـ API الخاص بك هنا مباشرة
API_KEY = "أدخل_مفتاحك_هنا"

def generate_shop_response(store_id, products_str, user_query):
    client = genai.Client(api_key=API_KEY)
    
    prompt = f"""
    أنت مساعد تسوق ذكي ومحترف لمتجر يحمل المعرف: {store_id}.
    هذه هي قائمة المنتجات المتاحة في المتجر حالياً:
    {products_str}
    
    بناءً على المنتجات أعلاه، أجب عن استفسار العميل التالي بطريقة دافئة ومساعدة ومنسقة:
    استفسار العميل: {user_query}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

st.title("🛍 مساعد التسوق الذكي")
st.write("أهلاً بك في منصة إدارة وتسوق المنتجات الذكية.")

# اختيار المحل أو التجربة من الشريط الجانبي
store_id = st.sidebar.text_input("معرف المحل (Store ID)", value="store_1")

menu = st.sidebar.selectbox("القائمة الرئيسية", ["محادثة المساعد", "إدارة المنتجات"])

if menu == "محادثة المساعد":
    st.subheader(f"اسأل مساعد التسوق - {store_id}")
    
    # تهيئة سجل المحادثة لكل متجر لضمان عدم ضياع الرسائل عند التبديل
    if "messages" not in st.session_state:
        st.session_state.messages = {}

    if store_id not in st.session_state.messages:
        st.session_state.messages[store_id] = []

    # جلب منتجات المحل لتحويلها إلى سياق للذكاء الاصطناعي
    products = get_store_products(store_id)
    products_str = products.to_string(index=False) if not products.empty else "لا توجد منتجات مضافة بعد."

    # عرض الرسائل السابقة في واجهة الدردشة
    for message in st.session_state.messages[store_id]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # صندوق إدخال المحادثة الحديث
    if user_query := st.chat_input("كيف يمكنني مساعدتك اليوم في المنتجات؟"):
        # تسجيل وعرض رسالة المستخدم
        st.session_state.messages[store_id].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # توليد وعرض رد الذكاء الاصطناعي
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير وتنسيق الإجابة..."):
                try:
                    reply = generate_shop_response(store_id, products_str, user_query)
                    st.markdown(reply)
                    st.session_state.messages[store_id].append({"role": "assistant", "content": reply})
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ في الاتصال بالخدمة: {e}"
                    st.error(error_msg)
                    st.session_state.messages[store_id].append({"role": "assistant", "content": error_msg})

elif menu == "إدارة المنتجات":
    st.subheader("إضافة منتج جديد للمتجر")
    with st.form("add_product_form", clear_on_submit=True):
        p_name = st.text_input("اسم المنتج")
        p_price = st.number_input("السعر", min_value=0.0, format="%.2f")
        p_desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("حفظ المنتج")
        
        if submit and p_name:
            add_product(store_id, p_name, p_price, p_desc)
            st.success(f"تم إضافة المنتج '{p_name}' بنجاح!")
            st.rerun()
            
    st.divider()
    st.subheader("المنتجات الحالية في المتجر")
    current_products = get_store_products(store_id)
    if not current_products.empty:
        st.dataframe(current_products, use_container_width=True)
    else:
        st.info("لا توجد منتجات مسجلة لهذا المتجر حالياً.")
