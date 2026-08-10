import os
from google import genai

# ضع مفتاح الـ API الخاص بك هنا بين علامتي التنصيص بدلاً من os.getenv
api_key = "AIzaSy..."  # ضع مفتاحك هنا

client = genai.Client(api_key=api_key)

def generate_shop_response(store_name, products_str, user_query):
    prompt = f"""
    أنت رد ذكي للعميل بناءً على منتجات المتجر: {store_name}
    المنتجات المتاحة:
    {products_str}
    
    سؤال العميل: {user_query}
    """
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text
