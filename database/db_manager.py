import pandas as pd
import os
import streamlit as st

DB_PATH = "database/products.csv"

def init_db():
    """تهيئة مجلد البيانات والملف مع ترميز UTF-8 لدعم العربية"""
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(DB_PATH):
        df = pd.DataFrame(columns=["store_id", "product_name", "price", "description"])
        df.to_csv(DB_PATH, index=False, encoding='utf-8-sig')

@st.cache_data(ttl=600)  # تخزين مؤقت لتحسين الأداء
def load_data():
    """قراءة ملف CSV"""
    if not os.path.exists(DB_PATH):
        init_db()
    return pd.read_csv(DB_PATH, encoding='utf-8-sig')

def save_data(df):
    """حفظ البيانات مع الترميز الصحيح ومسح الكاش"""
    df.to_csv(DB_PATH, index=False, encoding='utf-8-sig')
    st.cache_data.clear()

def get_store_products(store_id):
    df = load_data()
    if 'store_id' not in df.columns:
        return pd.DataFrame(columns=["store_id", "product_name", "price", "description"])
    return df[df['store_id'].astype(str) == str(store_id)]

def add_product(store_id, name, price, description):
    try:
        price = float(price)
    except (ValueError, TypeError):
        raise ValueError("السعر يجب أن يكون رقماً")
    
    df = load_data()
    new_row = {
        "store_id": str(store_id),
        "product_name": str(name).strip(),
        "price": price,
        "description": str(description).strip()
    }
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    save_data(df)
    return new_row

def delete_product(store_id, product_name):
    df = load_data()
    filtered_df = df[~((df['store_id'].astype(str) == str(store_id)) & 
                       (df['product_name'].astype(str) == str(product_name)))]
    if len(filtered_df) == len(df):
        return False
    save_data(filtered_df)
    return True
