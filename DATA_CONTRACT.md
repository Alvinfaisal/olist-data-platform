# DATA_CONTRACT — Olist Data Platform (nama: Alvin)

Sumber: Brazilian E-Commerce Public Dataset by Olist (Kaggle, versi 1), diunduh 2026, `scripts/check_dataset.py` lulus pada 2026-10-20.
Semua stempel waktu: waktu lokal Brasil tanpa zona. Mata uang: BRL. Kode pos: **teks 5 digit** di semua tabel.

## 1. Tabel

### customers — `olist_customers_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| customer_id | text | tidak | kunci alami, unik (dibuktikan: nunique=99.441 dari 99.441 baris) |
| customer_unique_id | text | tidak | ID unik konsumen untuk melacak belanja berulang |
| customer_zip_code_prefix | text | tidak | Wajib text agar nol di depan tidak terpotong |
| customer_city | text | tidak | |
| customer_state | text | tidak | |

Baris diharapkan: 99.441. Kunci alami: `customer_id`.

### orders — `olist_orders_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| order_id | text | tidak | kunci alami, unik (dibuktikan: nunique=99.441 dari 99.441 baris) |
| customer_id | text | tidak | FK ke tabel customers |
| order_status | text | tidak | nilai: delivered, shipped, canceled, invoiced, processing, approved, unavailable, created |
| order_purchase_timestamp | timestamp | tidak | |
| order_approved_at | timestamp | ya | |
| order_delivered_carrier_date | timestamp | ya | |
| order_delivered_customer_date | timestamp | ya | |
| order_estimated_delivery_date | timestamp | tidak | |

Baris diharapkan: 99.441. Kunci alami: `order_id`.

*(Catatan: Lakukan pola pengisian tabel yang sama untuk 7 file CSV sisanya sesuai dengan metadata tipe data target kolomnya).*

## 2. Temuan "kotor" dan keputusannya

| # | Tabel | Temuan | Angka | Keputusan | Diterapkan di |
|---|---|---|---|---|---|
| 1 | orders | Order terdaftar tanpa memiliki item belanjaan | 775 baris | Karantina | T2 Silver Gate / T3 log |
| 2 | orders | Order terdaftar tanpa memiliki rekap pembayaran | 1 baris | Biarkan & Catat | T4 Data Warehouse |
| 3 | customers | Pelanggan melakukan transaksi berulang (belanja > 1x) | 3.345 orang | Tangani di DW | T4 `dim_customer` |
| 4 | reviews | Satu order_id memiliki duplikasi review_id kembar | 2.965 baris | Tangani di DW | T4 `fact_review` |
| 5 | geolocation | Kode pos daerah Brazil berawalan angka 0 (nol) | 14.654 baris | Fallback (Text fixed) | T1 Landing Zone |
| 6 | reviews | Kolom comment title bernilai kosong (Null) | 87.656 baris | Biarkan & Catat | T4 Data Warehouse |
| 7 | reviews | Kolom comment message bernilai kosong (Null) | 58.247 baris | Fallback ('No text')| T2 Silver Gate |
| 8 | orders | Status delivered tetapi tanggal diterima konsumen kosong | 2.980 baris | Karantina | T2 Silver Gate |
| 9 | finance | Selisih agregat total cost (harga+ongkir) vs payment_value | > 0.01 (242 order)| Tangani di DW | T4 `fact_orders` |
| 10| finance | Selisih keuangan bernilai fatal antara barang vs bayar | > 1.00 (84 order) | Karantina | T2 Silver Gate |

## 3. Aturan kualitas (gate silver)

| Tabel | Aturan | Jenis (hard/soft) | Tindakan | Ambang |
|---|---|---|---|---|
| orders | check_delivered_date | hard | Karantina baris | 2% |
| finance | check_fatal_financial_diff| hard | Karantina baris | 2% |
| customers | zip_code_must_be_text | hard | Pipeline FAIL jika int | 0% |
| reviews | review_comment_msg_fallback| soft | Isi default text | 100% |

Ambang karantina per tabel: 2% — alasan: Menoleransi anomali inputan manusia secara wajar di sistem e-commerce tanpa perlu mematikan pipa data operasional harian [T2].

## 4. Keputusan pemodelan yang mengikuti dari kontrak ini

- grain `dim_customer` = Berdasarkan `customer_unique_id` untuk mengonsolidasikan data historis belanja pelanggan berulang [T0].
- kebijakan `fact_review` = Memilih ulasan dengan stempel waktu terbaru (`review_answer_timestamp`) jika satu `order_id` memiliki entri ganda ulasan [T0].
- `is_late` = Dihitung jika `order_delivered_customer_date` melewati batas waktu estimasi `order_estimated_delivery_date` [T0].
- bulan lengkap = Pelaporan tren performa penjualan hanya mengambil data dari bulan yang memiliki siklus transaksi utuh 1-30 hari [T0].
