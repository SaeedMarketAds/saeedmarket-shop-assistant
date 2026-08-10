import os
import google.generativeai as genai

# ضع مفتاح الـ API الخاص بك هنا مباشرة بين علامتي التنصيص
GEMINI_API_KEY = "AIzaSy_ضع_مفتاحك_هنا"

# إعداد المفتاح للمكتبة
genai.configure(api_key=GEMINI_API_KEY)

def generate_shop_response(store_name, products_str, user_query):
    # استخدام النموذج بطريقة مستقرة ومباشرة
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    أنت مساعد تسوق ذكي ومحترف لمتجر يحمل المعرف: {store_name}.
    هذه هي قائمة المنتجات المتاحة في المتجر حالياً:
    {products_str}
    
    بناءً على المنتجات أعلاه، أجب عن استفسار العميل التالي بطريقة دافئة ومساعدة ومنسقة:
    استفسار العميل: {user_query}
    """
    
    response = model.generate_content(prompt)
    return response.text
