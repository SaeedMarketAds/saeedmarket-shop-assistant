import os
import google.generativeai as genai

# قراءة المفتاح من متغير البيئة (آمن)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_shop_response(store_name, products_str, user_query):
    prompt = f"""
    أنت مساعد تسوق ذكي ومحترف لمتجر يحمل المعرف: {store_name}
    هذه هي قائمة المنتجات المتاحة في المتجر حالياً:
    {products_str}
    
    بناءً على المنتجات أعلاه، أجب عن استفسار العميل التالي بطريقة دافئة ومساعدة ومنسقة:
    استفسار العميل: {user_query}
    """
    
    response = client.models.generate_content(
        model="gemini-3.1-flash", 
        contents=prompt
    )
    return response.text
