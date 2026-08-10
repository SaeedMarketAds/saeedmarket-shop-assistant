import os
from google import genai

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
    
    # تم تصحيح النموذج إلى gemini-2.0-flash
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )
    return response.text
