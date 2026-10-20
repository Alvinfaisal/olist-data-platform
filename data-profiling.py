import pandas as pd
import os

# Tentukan folder dataset aktif (Opsi 1: notebooks/raw atau data/raw)
folder_path = "data/raw"
output_profile = "outputs/profile.md"

os.makedirs("outputs", exist_ok=True)

print("⏳ Menjalankan Inspeksi Forensik Dataset Olist secara Otomatis...")

# Load semua data dengan dtype=str untuk menghindari jebakan kode pos berawalan 0
df_cust = pd.read_csv(
    os.path.join(folder_path, "olist_customers_dataset.csv"), dtype=str
)
df_geo = pd.read_csv(
    os.path.join(folder_path, "olist_geolocation_dataset.csv"), dtype=str
)
df_orders = pd.read_csv(
    os.path.join(folder_path, "olist_orders_dataset.csv"), dtype=str
)
df_items = pd.read_csv(
    os.path.join(folder_path, "olist_order_items_dataset.csv"), dtype=str
)
df_payments = pd.read_csv(
    os.path.join(folder_path, "olist_order_payments_dataset.csv"), dtype=str
)
df_reviews = pd.read_csv(
    os.path.join(folder_path, "olist_order_reviews_dataset.csv"), dtype=str
)
df_products = pd.read_csv(
    os.path.join(folder_path, "olist_products_dataset.csv"), dtype=str
)
df_sellers = pd.read_csv(
    os.path.join(folder_path, "olist_sellers_dataset.csv"), dtype=str
)
df_trans = pd.read_csv(
    os.path.join(folder_path, "product_category_name_translation.csv"), dtype=str
)

# --- PROFILING AUTOMATION FOR DATASET PROFILE.MD ---
datasets = {
    "olist_customers_dataset": df_cust,
    "olist_geolocation_dataset": df_geo,
    "olist_orders_dataset": df_orders,
    "olist_order_items_dataset": df_items,
    "olist_order_payments_dataset": df_payments,
    "olist_order_reviews_dataset": df_reviews,
    "olist_products_dataset": df_products,
    "olist_sellers_dataset": df_sellers,
    "product_category_name_translation": df_trans,
}

md_profile = "# outputs/profile.md — HASIL PROFILING OTOMATIS\n\n"
md_profile += (
    "Dokumen ini dihasilkan secara otomatis oleh kode `profiler_engine.py`.\n\n"
)

for name, df in datasets.items():
    total_rows = len(df)
    exact_dup = df.duplicated().sum()
    md_profile += f"### Tabel: {name}\n"
    md_profile += f"- **Total Baris:** {total_rows}\n"
    md_profile += f"- **Duplikat Persis:** {exact_dup}\n\n"
    md_profile += "| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |\n"
    md_profile += "|---|---|---|---|\n"
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / total_rows) * 100
        is_uniq = "YA" if df[col].nunique() == total_rows else "TIDAK"
        md_profile += f"| {col} | {null_pct:.2f}% | {is_uniq} | {df[col].nunique()} |\n"
    md_profile += "\n"

with open(output_profile, "w", encoding="utf-8") as f:
    f.write(md_profile)

print("✅ Sukses! File outputs/profile.md telah dihasilkan murni dari kode.")

# --- HITUNG DAFATAR 10 TEMUAN KOTOR UNTUK DATA_CONTRACT ---
print("\n🔍 menghitung 10 Angka Temuan Kotor untuk DATA_CONTRACT.md:")

# 1. Pelanggan unik vs berulang
cust_uniq = df_cust["customer_unique_id"].nunique()
repeat_cust = (df_cust["customer_unique_id"].value_counts() > 1).sum()
print(f"1. Pelanggan Unik: {cust_uniq} | Pelanggan Berulang: {repeat_cust}")

# 2. Order tanpa item
order_no_item = len(df_orders[~df_orders["order_id"].isin(df_items["order_id"])])
print(f"2. Order tanpa item: {order_no_item}")

# 3. Order tanpa pembayaran
order_no_pay = len(df_orders[~df_orders["order_id"].isin(df_payments["order_id"])])
print(f"3. Order tanpa pembayaran: {order_no_pay}")

# 4. Review duplikat order_id
review_dup_order = df_reviews.duplicated(subset=["order_id"]).sum()
print(f"4. Duplikat order_id di tabel review: {review_dup_order}")

# 5. Kode pos berawalan 0 di geolocation
geo_zero_prefix = df_geo["geolocation_zip_code_prefix"].str.startswith("0").sum()
print(f"5. Kode pos berawalan nol (0) di geo: {geo_zero_prefix}")

# 6. Null di judul review
review_title_null = df_reviews["review_comment_title"].isnull().sum()
print(f"6. Missing value judul review: {review_title_null}")

# 7. Null di pesan review
review_msg_null = df_reviews["review_comment_message"].isnull().sum()
print(f"7. Missing value pesan review: {review_msg_null}")

# 8. Delivered tapi tanggal terima null
delivered_null_date = len(
    df_orders[
        (df_orders["order_status"] == "delivered")
        & (df_orders["order_delivered_customer_date"].isnull())
    ]
)
print(f"8. Status delivered tapi tanggal terima kosong: {delivered_null_date}")

# 9 & 10. Selisih hitung keuangan
df_items["price"] = df_items["price"].astype(float)
df_items["freight_value"] = df_items["freight_value"].astype(float)
df_payments["payment_value"] = df_payments["payment_value"].astype(float)

item_cost = (
    df_items.groupby("order_id")
    .apply(lambda x: (x["price"] + x["freight_value"]).sum())
    .reset_index(name="total_cost")
)
pay_cost = df_payments.groupby("order_id")["payment_value"].sum().reset_index()
df_finance = pd.merge(item_cost, pay_cost, on="order_id")
df_finance["diff"] = (df_finance["total_cost"] - df_finance["payment_value"]).abs()

print(
    f"9. Transaksi dengan selisih Bayar vs Harga > 0.01: {len(df_finance[df_finance['diff'] > 0.01])}"
)
print(
    f"10. Transaksi dengan selisih Bayar vs Harga > 1.00: {len(df_finance[df_finance['diff'] > 1.00])}"
)
