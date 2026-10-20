# Starter — Tugas Besar Olist Data Platform

Isi starter ini **sengaja sedikit**: stack yang sama dengan Local Big Data Lab, pemeriksa dataset, kerangka `pipeline.py`,
dan tiga template dokumen. Sisanya kamu bangun mengikuti `TUGAS_BESAR.md`.

```
docker-compose.yml   .env.example   jupyter/Dockerfile      # stack (postgres, kafka, kafka-ui, minio, jupyter) — project name "olist"
pipeline.py                                                 # init/up/down sudah jadi; tahap lain = TODO kamu
scripts/check_dataset.py                                    # cek 9 file CSV Kaggle di data/raw
sql/00_schemas.sql                                          # hanya CREATE SCHEMA; tabel kamu yang rancang
tests/conftest.py                                           # fixture koneksi Postgres untuk test (skip kalau stack mati)
docs/DATA_CONTRACT_TEMPLATE.md  RUNBOOK_TEMPLATE.md  EVALUATION_EVIDENCE_TEMPLATE.md
```

Langkah pertama:

```
pip install -r requirements.txt
python pipeline.py init
python pipeline.py up --build        # pertama kali: build image jupyter (±2–3 menit)
# unduh dataset Kaggle → data/raw/
python scripts/check_dataset.py
```

Lalu buka `TUGAS_BESAR.md` → Tahap 0.

### 📌 Tahap T0 — Pertanyaan Analisis "Salah Secara Diam-Diam" (Silent Error)
Tiga temuan data kotor yang jika tidak ditangani akan membuat hasil analisis Q1–Q4 salah secara diam-diam tanpa memicu eror sistem:

1. **Kasus Pemotongan Angka Nol pada Kode Pos (Tabel `customers` & `geolocation`)**
   - **Mekanisme Salah:** Kode pos di wilayah Sao Paulo diawali dengan angka nol (misal: `01003`). Jika dibaca sebagai *Integer*, angka nol akan dihapus komputer menjadi `1003`.
   - **Dampak Bisnis:** Saat melakukan operasi `JOIN` untuk memetakan wilayah geografi penjualan terlaris (Q1), data `1003` tidak akan pernah cocok (*miss-match*) dengan master data geolokasi asli (`01003`). Hasilnya, omzet dari wilayah terkaya di Brazil akan hilang dari dashboard, membuat keputusan ekspansi logistik salah total secara diam-diam.

2. **Kasus 775 Pesanan Gantung Tanpa Item Belanjaan (Tabel `orders` vs `order_items`)**
   - **Mekanisme Salah:** Ada 775 ID nota belanja gantung yang masuk ke sistem akibat *payment timeout* sehingga tidak memiliki detail barang di tabel item.
   - **Dampak Bisnis:** Jika tim analis menghitung rata-rata nilai transaksi (*Average Order Value* / AOV) menggunakan total baris tabel `orders` sebagai pembagi rumus agregasi `SUM(price) / COUNT(order_id)`, nilai penyebut menjadi terlalu besar. Angka performa pendapatan perusahaan di dashboard akan terdistorsi menjadi lebih rendah dari aslinya, memicu kepanikan manajemen yang salah kaprah.

3. **Kasus Duplikasi Pasangan `order_id` di Tabel Ulasan (Tabel `order_reviews`)**
   - **Mekanisme Salah:** Terdapat 2.965 transaksi di mana satu pesanan memiliki lebih dari satu baris ulasan karena pembeli mengulas beberapa produk sekaligus dalam satu paket kiriman.
   - **Dampak Bisnis:** Jika tabel `orders` di-join langsung dengan `order_reviews` tanpa agregasi string di hulu, baris transaksi tersebut akan melipatgandakan dirinya sendiri (*Multiplication Effect*). Saat fungsi `SUM(payment_value)` dijalankan, nominal omzet tahunan perusahaan di dashboard akan menggelembung jauh lebih besar dari uang asli yang masuk ke rekening bank perusahaan.
