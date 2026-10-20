import os
import hashlib
import json
from datetime import datetime
import boto3
from dotenv import load_dotenv

# Membaca konfigurasi rahasia langsung dari file .env proyek lu
load_dotenv()

MINIO_URL = "http://localhost:9000"
# Jika di .env nama variabelnya berbeda, kode di bawah otomatis mengambil fallback minioadmin
ACCESS_KEY = (
    os.getenv("MINIO_ACCESS_KEY") or os.getenv("MINIO_ROOT_USER") or "minioadmin"
)
SECRET_KEY = (
    os.getenv("MINIO_SECRET_KEY") or os.getenv("MINIO_ROOT_PASSWORD") or "minioadmin"
)
BUCKET_NAME = "bronze"
LOCAL_DATA_DIR = "data/raw"
OUTPUT_REPORT = "outputs/bronze_report.md"

print(f"🔑 Mencoba masuk ke MinIO menggunakan Access Key: {ACCESS_KEY}")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

try:
    s3_client.create_bucket(Bucket=BUCKET_NAME)
except Exception:
    pass

csv_files = [f for f in os.listdir(LOCAL_DATA_DIR) if f.endswith(".csv")]
report_lines = [
    "# outputs/bronze_report.md — BRONZE INGESTION REPORT\n\n",
    "| File | Status | Baris | Ukuran (MB) | Waktu Ingest |\n",
    "|---|---|---|---|---|\n",
]

print("🚀 Memproses pemindahan file mentah ke MinIO Bronze Bucket...")

for file_name in csv_files:
    local_path = os.path.join(LOCAL_DATA_DIR, file_name)
    file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
    table_name = file_name.replace(".csv", "")

    # Hitung MD5 checksum untuk verifikasi Idempotensi mutlak
    hasher = hashlib.md5()
    with open(local_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    current_md5 = hasher.hexdigest()

    with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
        row_count = sum(1 for _ in f) - 1

    ingest_date = datetime.now().strftime("%Y-%m-%d")
    object_key = f"olist/{table_name}/ingest_date={ingest_date}/{file_name}"
    manifest_key = f"olist/{table_name}/manifest.json"

    status = "uploaded"

    try:
        old_manifest_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=manifest_key)
        old_manifest = json.loads(old_manifest_obj["Body"].read().decode("utf-8"))
        if old_manifest["latest_checksum"] == current_md5:
            status = "unchanged"
    except Exception:
        old_manifest = {"latest_checksum": "", "history": []}

    if status == "uploaded":
        s3_client.upload_file(local_path, BUCKET_NAME, object_key)
        new_manifest = {
            "table_name": table_name,
            "latest_checksum": current_md5,
            "latest_object": object_key,
            "history": old_manifest["history"]
            + [
                {
                    "waktu_ingest": datetime.now().isoformat(),
                    "checksum": current_md5,
                    "ukuran_bytes": os.path.getsize(local_path),
                    "jumlah_baris": row_count,
                    "object_location": object_key,
                }
            ],
        }
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=manifest_key,
            Body=json.dumps(new_manifest, indent=2),
        )
        print(f"✅ [UPLOADED] {file_name} berhasil dikirim.")
    else:
        print(f"⏭️ [UNCHANGED] {file_name} dilewati.")

    report_lines.append(
        f"| {file_name} | {status} | {row_count:,} | {file_size_mb:.2f} | {datetime.now().strftime('%H:%M:%S')} |\n"
    )

os.makedirs("outputs", exist_ok=True)
with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
    f.writelines(report_lines)
print("🎯 Tahap T1 Bronze selesai dengan sukses!")
