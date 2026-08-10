import os
import streamlit as st
from google import genai

def get_gemini_client():
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        raise ValueError("لم يتم العثور على مفتاح API. يرجى إضافته في إعدادات Secrets على منصة Streamlit.")
        
    return genai.Client(api_key=api_key)

def generate_shop_response(store_id, products_str, user_query):
    client = get_gemini_client()
    
    prompt = f"""
    أنت مساعد تسوق ذكي ومحترف لمتجر يحمل المعرف: {store_id}.
    هذه هي قائمة المنتجات المتاحة في المتجر حالياً:
    {products_str}
    
    بناءً على المنتجات أعلاه، أجب عن استفسار العميل التالي بطريقة دافئة ومساعدة ومنسقة:
    استفسار العميل: {user_query}
    """
    
    # استخدام النموذج الصحيح والمدعوم
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt
    )
    return response.text
