import streamlit as st
from database.db_manager import get_store_products, add_product
from services.ai_service import generate_shop_response

st.set_page_config(page_title="مساعد التسوق الذكي", page_icon="🛍", layout="centered")

st.title("🛍 مساعد التسوق الذكي")
st.write("أهلاً بك في منصة إدارة وتسوق المنتجات.")

# اختيار المحل أو التجربة
store_id = st.sidebar.text_input("معرف المحل (Store ID)", value="store_1")

menu = st.sidebar.selectbox("القائمة الرئيسية", ["محادثة المساعد", "إدارة المنتجات"])

if menu == "محادثة المساعد":
    st.subheader(f"اسأل مساعد التسوق - {store_id}")
    
    # جلب منتجات المحل لتحويلها إلى سياق
    products = get_store_products(store_id)
    products_str = products.to_string(index=False) if not products.empty else "لا توجد منتجات مضافة بعد."
    
    user_query = st.text_input("كيف يمكنني مساعدتك اليوم في المنتجات؟")
    if st.button("إرسال السؤال"):
        if user_query:
            with st.spinner("جاري التفكير..."):
                reply = generate_shop_response(store_id, products_str, user_query)
                st.success(reply)
        else:
            st.warning("الرجاء كتابة سؤالك أولاً.")

elif menu == "إدارة المنتجات":
    st.subheader("إضافة منتج جديد للمتجر")
    with st.form("add_product_form"):
        p_name = st.text_input("اسم المنتج")
        p_price = st.number_input("السعر", min_value=0.0, format="%.2f")
        p_desc = st.text_area("وصف المنتج")
        submit = st.form_submit_button("حفظ المنتج")
        
        if submit and p_name:
            add_product(store_id, p_name, p_price, p_desc)
            st.success(f"تم إضافة المنتج '{p_name}' بنجاح!")
            
    st.divider()
    st.subheader("المنتجات الحالية في المتجر")
    current_products = get_store_products(store_id)
    st.dataframe(current_products)

