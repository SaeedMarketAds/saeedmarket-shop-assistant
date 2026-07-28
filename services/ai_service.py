import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def generate_shop_response(store_name, products_context, user_query):
    """توليد رد ذكي للعميل بناءً على منتجات المتجر"""
    prompt = f"""
    انت مساعد تسوق ذكي ومحترف لمتجر "{store_name}".
    معلومات المنتجات المتوفرة لديك:
    {products_context}
    
    سؤال العميل: {user_query}
    
    أجب باحترافية، وساعد العميل في اختيار المنتج المناسب من القائمة أعلاه فقط.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال بالخدمة: {e}"
