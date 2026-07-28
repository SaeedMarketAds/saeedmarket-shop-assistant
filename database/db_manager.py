import pandas as pd
import os

DB_PATH = "database/products.csv"

def init_db():
    """تهيئة ملف البيانات إذا لم يكن موجوداً"""
    if not os.path.exists("database"):
        os.makedirs("database")
    if not os.path.exists(DB_PATH):
        df = pd.DataFrame(columns=["store_id", "product_name", "price", "description"])
        df.to_csv(DB_PATH, index=False)

def get_store_products(store_id):
    """جلب منتجات محل معين"""
    init_db()
    df = pd.read_csv(DB_PATH)
    store_df = df[df['store_id'] == store_id]
    return store_df

def add_product(store_id, name, price, description):
    """إضافة منتج جديد للمحل"""
    init_db()
    df = pd.read_csv(DB_PATH)
    new_row = {"store_id": store_id, "product_name": name, "price": price, "description": description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DB_PATH, index=False)
