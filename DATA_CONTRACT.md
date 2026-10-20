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
| customer_city | text | tidak | Nama kota asal pelanggan |
| customer_state | text | tidak | Kode negara bagian asal pelanggan |

Baris diharapkan: 99.441. Kunci alami: `customer_unique_id`.

### orders — `olist_orders_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| order_id | text | tidak | kunci alami, unik (dibuktikan: nunique=99.441 dari 99.441 baris) |
| customer_id | text | tidak | FK ke tabel customers (menunjuk ke transaksi spesifik) |
| order_status | text | tidak | nilai: delivered, shipped, canceled, invoiced, processing, approved, unavailable, created |
| order_purchase_timestamp | timestamp | tidak | Waktu pelanggan melakukan pemesanan |
| order_approved_at | timestamp | ya | Waktu pembayaran disetujui |
| order_delivered_carrier_date | timestamp | ya | Waktu paket diserahkan ke kurir |
| order_delivered_customer_date | timestamp | ya | Waktu paket sampai di tangan pembeli |
| order_estimated_delivery_date | timestamp | tidak | Estimasi waktu pengiriman dari sistem |

Baris diharapkan: 99.441. Kunci alami: `order_id`.

### order_items — `olist_order_items_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| order_id | text | tidak | Bagian dari kunci komposit, FK ke tabel orders |
| order_item_id | integer | tidak | Nomor urut item di dalam satu pesanan |
| product_id | text | tidak | FK ke tabel products |
| seller_id | text | tidak | FK ke tabel sellers |
| shipping_limit_date | timestamp | tidak | Batas waktu seller menyerahkan barang ke kurir |
| price | numeric | tidak | Harga barang per item |
| freight_value | numeric | tidak | Nilai ongkos kirim barang |

Baris diharapkan: 112.650. Kunci alami: `order_id` + `order_item_id`.

### order_payments — `olist_order_payments_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| order_id | text | tidak | FK ke tabel orders |
| payment_sequential | integer | tidak | Nomor urut metode pembayaran yang digunakan |
| payment_type | text | tidak | Jenis pembayaran (credit_card, boleto, voucher, debit_card) |
| payment_installments | integer | tidak | Jumlah cicilan pembayaran |
| payment_value | numeric | tidak | Total nominal uang yang dibayarkan |

Baris diharapkan: 103.886. Kunci alami: `order_id` + `payment_sequential`.

### order_reviews — `olist_order_reviews_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| review_id | text | tidak | ID ulasan, tidak unik mutlak karena entri kembar |
| order_id | text | tidak | FK ke tabel orders |
| review_score | integer | tidak | Skor ulasan skala 1 sampai 5 |
| review_comment_title | text | ya | Judul komentar ulasan (banyak yang kosong) |
| review_comment_message | text | ya | Pesan komentar isi ulasan konsumen |
| review_creation_date | timestamp | tidak | Waktu survei ulasan dikirim ke pembeli |
| review_answer_timestamp | timestamp | tidak | Waktu pembeli mengisi survei ulasan |

Baris diharapkan: 99.224. Kunci alami: `review_id` + `order_id`.

### products — `olist_products_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| product_id | text | tidak | kunci alami, unik (dibuktikan: nunique=32.951 dari 32.951 baris) |
| product_category_name | text | ya | Nama kategori produk dalam bahasa Portugis |
| product_name_lenght | integer | ya | Panjang karakter nama produk |
| product_description_lenght | integer | ya | Panjang karakter deskripsi produk |
| product_photos_qty | integer | ya | Jumlah foto produk yang dipajang |
| product_weight_g | integer | ya | Berat produk dalam satuan gram |
| product_length_cm | integer | ya | Panjang produk dalam satuan centimeter |
| product_height_cm | integer | ya | Tinggi produk dalam satuan centimeter |
| product_width_cm | integer | ya | Lebar produk dalam satuan centimeter |

Baris diharapkan: 32.951. Kunci alami: `product_id`.

### sellers — `olist_sellers_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| seller_id | text | tidak | kunci alami, unik (dibuktikan: nunique=3.095 dari 3.095 baris) |
| seller_zip_code_prefix | text | tidak | Wajib text agar nol di depan tidak terpotong |
| seller_city | text | tidak | Kota asal penjual |
| seller_state | text | tidak | Negara bagian asal penjual |

Baris diharapkan: 3.095. Kunci alami: `seller_id`.

### geolocation — `olist_geolocation_dataset.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| geolocation_zip_code_prefix | text | tidak | Kode pos wilayah geolokasi (wajib string) |
| geolocation_lat | numeric | tidak | Koordinat garis lintang (latitude) |
| geolocation_lng | numeric | tidak | Koordinat garis bujur (longitude) |
| geolocation_city | text | tidak | Nama kota wilayah koordinat |
| geolocation_state | text | tidak | Negara bagian koordinat |

Baris diharapkan: 1.000.163. Kunci alami: Tidak unik secara baris tunggal (kunci komposit/koordinat).

### product_category_name_translation — `product_category_name_translation.csv`

| Kolom | Tipe target | Null? | Catatan |
|---|---|---|---|
| product_category_name | text | tidak | Kunci alami, nama kategori dalam bahasa Portugis |
| product_category_name_english | text | tidak | Nama terjemahan kategori dalam bahasa Inggris |

Baris diharapkan: 71. Kunci alami: `product_category_name`.

---

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
| 9 | finance | Selisih antara nominal total cost vs payment_value | > 0.01 (242 order)| Tangani di DW | T4 `fact_orders` |
| 10| finance | Selisih keuangan bernilai fatal antara barang vs bayar | > 1.00 (84 order) | Karantina | T2 Silver Gate |

---

## 3. Aturan kualitas (gate silver)

| Tabel | Aturan | Jenis (hard/soft) | Tindakan | Ambang |
|---|---|---|---|---|
| orders | check_delivered_date | hard | Karantina baris | 2% |
| finance | check_fatal_financial_diff| hard | Karantina baris | 2% |
| customers | zip_code_must_be_text | hard | Pipeline FAIL jika int | 0% |
| reviews | review_comment_msg_fallback| soft | Isi default text | 100% |

Ambang karantina per tabel: **2%** — alasan: Menoleransi anomali minor akibat kesalahan operasional atau kegagalan sinkronisasi aplikasi kasir secara wajar di ekosistem e-commerce tanpa perlu mematikan pipa data utama perusahaan [T2].

---

## 4. Keputusan pemodelan yang mengikuti dari kontrak ini

- grain `dim_customer` = Berdasarkan `customer_unique_id` untuk mengonsolidasikan seluruh riwayat perilaku belanja pelanggan berulang [T0].
- kebijakan `fact_review` = Memilih data ulasan dengan stempel waktu terbaru (`review_answer_timestamp`) jika satu `order_id` memiliki entri ganda ulasan [T0].
- `is_late` = Flag boolean aktif di mana nilai bernilai True jika `order_delivered_customer_date` > `order_estimated_delivery_date` [T0].
- bulan lengkap = Agregasi dan analisis performa penjualan hanya dihitung dari bulan transaksi yang memiliki siklus tanggal utuh dari tanggal 1 sampai akhir bulan [T0].
