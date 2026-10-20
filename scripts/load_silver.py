import os
import io
import pandas as pd
import psycopg
from datetime import datetime

# Database Credentials from your .env
DB_CONN = "host=localhost port=5432 dbname=olist user=olist password=olist_dev_only"
LOCAL_DATA_DIR = "data/raw"
OUTPUT_DQ = "outputs/dq_report.md"
OUTPUT_LOAD = "outputs/load_report.md"

os.makedirs("outputs", exist_ok=True)
print("🧼 Activating Silver Quality Gate & Loading Postgres...")

# Establish Transactional Postgres Session
with psycopg.connect(DB_CONN) as conn:
    with conn.cursor() as cur:
        # Create raw schema cleanly
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        
        # 1. Processing Orders Table with Quality Gate Verification
        df_orders = pd.read_csv(os.path.join(LOCAL_DATA_DIR, "olist_orders_dataset.csv"), dtype=str)
        total_orders = len(df_orders)
        
        # HARD RULE: If order status is delivered, customer delivery date MUST NOT be null
        is_corrupt_delivered = (df_orders['order_status'] == 'delivered') & (df_orders['order_delivered_customer_date'].isnull())
        df_quarantine = df_orders[is_corrupt_delivered].copy()
        df_quarantine['quarantine_reason'] = "Delivered status but missing actual customer arrival timestamp"
        
        # Clean data for Silver Layer load
        df_silver_orders = df_orders[~is_corrupt_delivered].copy()
        
        # Calculate validation threshold
        quarantine_pct = (len(df_quarantine) / total_orders) * 100
        verdict = "PASS+KARANTINA" if quarantine_pct <= 2.0 else "FAIL"
        
        if verdict == "FAIL":
            raise ValueError(f"CRITICAL ERROR: Orders table exceeded 2% corruption threshold ({quarantine_pct:.2f}%). Pipeline stopped.")
            
        # Fast transactional database load using COPY memory stream
        cur.execute("DROP TABLE IF EXISTS raw.orders CASCADE;")
        cur.execute("""
            CREATE TABLE raw.orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_status TEXT,
                order_purchase_timestamp TIMESTAMP,
                order_approved_at TIMESTAMP,
                order_delivered_carrier_date TIMESTAMP,
                order_delivered_customer_date TIMESTAMP,
                order_estimated_delivery_date TIMESTAMP
            );
        """)
        
        # Stream clean records straight into memory buffer
        output = io.StringIO()
        df_silver_orders.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        
        start_time = datetime.now()
        with cur.copy("COPY raw.orders FROM STDIN WITH CSV DELIMITER E'\\t' NULL ''") as copy:
            copy.write(output.read())
        duration = (datetime.now() - start_time).total_seconds()

# Save DQ Laporan Metrics
with open(OUTPUT_DQ, "w", encoding="utf-8") as f:
    f.write(f"# outputs/dq_report.md\n\n- Aturan check_delivered_date: Hard Rule\n- Verdict Orders Table: {verdict} ({quarantine_pct:.2f}% Quarantined rows)\n")

with open(OUTPUT_LOAD, "w", encoding="utf-8") as f:
    f.write(f"# outputs/load_report.md\n\n- Table raw.orders: Loaded {len(df_silver_orders)} clean rows in {duration:.4f} seconds.\n")

print("✅ Stage T2 Silver Gate executed flawlessly!")