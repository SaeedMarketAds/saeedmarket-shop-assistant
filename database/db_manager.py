import pandas as pd
import os
import streamlit as st  # لإضافة التخزين المؤقت (cache)

DB_PATH = "database/products.csv"

def init_db():
    """تهيئة مجلد البيانات والملف مع ترميز UTF-8 لدعم العربية"""
    os.makedirs("database", exist_ok=True)  # اختصار للتحقق وإنشاء المجلد
    if not os.path.exists(DB_PATH):
        # إنشاء DataFrame فارغ مع تحديد الأعمدة
        df = pd.DataFrame(columns=["store_id", "product_name", "price", "description"])
        # استخدام utf-8-sig لضمان قراءة العربية في جميع البيئات
        df.to_csv(DB_PATH, index=False, encoding='utf-8-sig')

# دالة مساعدة لقراءة الملف (مع التخزين المؤقت لتحسين الأداء في Streamlit)
@st.cache_data(ttl=600)  # تخزين النتائج مؤقتاً لمدة 10 دقائق
def load_data():
    """قراءة ملف CSV مع دعم الترميز العربي"""
    if not os.path.exists(DB_PATH):
        init_db()  # تأكد من وجود الملف
    # استخدام utf-8-sig بدلاً من الافتراضي لتجنب أخطاء 'ascii'
    return pd.read_csv(DB_PATH, encoding='utf-8-sig')

def save_data(df):
    """حفظ البيانات مع الترميز الصحيح"""
    df.to_csv(DB_PATH, index=False, encoding='utf-8-sig')
    # مسح الكاش بعد التعديل لتحديث البيانات المعروضة
    st.cache_data.clear()

def get_store_products(store_id):
    """جلب منتجات محل معين مع التعامل مع حالة عدم وجود المنتجات"""
    df = load_data()
    # التأكد من وجود العمود store_id لتجنب خطأ KeyError
    if 'store_id' not in df.columns:
        return pd.DataFrame(columns=["store_id", "product_name", "price", "description"])
    # تصفية المنتجات حسب store_id (مع تحويل المعرف إلى نص لتجنب مشاكل الأنواع)
    store_df = df[df['store_id'].astype(str) == str(store_id)]
    return store_df

def add_product(store_id, name, price, description):
    """إضافة منتج جديد للمحل مع التحقق من صحة المدخلات"""
    # التحقق من أن السعر رقمي
    try:
        price = float(price)
    except (ValueError, TypeError):
        raise ValueError("السعر يجب أن يكون رقماً صحيحاً أو عشرياً")
    
    # تحميل البيانات الحالية
    df = load_data()
    
    # إنشاء الصف الجديد
    new_row = {
        "store_id": str(store_id),  # توحيد النوع كنص
        "product_name": str(name).strip(),
        "price": price,
        "description": str(description).strip()
    }
    
    # إضافة الصف (استخدام concat آمن)
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # حفظ البيانات
    save_data(df)
    
    # إرجاع المنتج المضاف للتأكيد
    return new_row

# --- دالة إضافية مفيدة: حذف منتج ---
def delete_product(store_id, product_name):
    """حذف منتج معين من محل معين"""
    df = load_data()
    # تصفية الصفوف التي لا تطابق المعايير
    filtered_df = df[~((df['store_id'].astype(str) == str(store_id)) & 
                       (df['product_name'].astype(str) == str(product_name)))]
    if len(filtered_df) == len(df):
        return False  # لم يتم العثور على المنتج للحذف
    save_data(filtered_df)
    return True
