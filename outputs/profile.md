# outputs/profile.md — HASIL PROFILING OTOMATIS

Dokumen ini dihasilkan secara otomatis oleh kode `profiler_engine.py`.

### Tabel: olist_customers_dataset
- **Total Baris:** 99441
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| customer_id | 0.00% | YA | 99441 |
| customer_unique_id | 0.00% | TIDAK | 96096 |
| customer_zip_code_prefix | 0.00% | TIDAK | 14994 |
| customer_city | 0.00% | TIDAK | 4119 |
| customer_state | 0.00% | TIDAK | 27 |

### Tabel: olist_geolocation_dataset
- **Total Baris:** 1000163
- **Duplikat Persis:** 261831

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| geolocation_zip_code_prefix | 0.00% | TIDAK | 19015 |
| geolocation_lat | 0.00% | TIDAK | 717372 |
| geolocation_lng | 0.00% | TIDAK | 717615 |
| geolocation_city | 0.00% | TIDAK | 8011 |
| geolocation_state | 0.00% | TIDAK | 27 |

### Tabel: olist_orders_dataset
- **Total Baris:** 99441
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| order_id | 0.00% | YA | 99441 |
| customer_id | 0.00% | YA | 99441 |
| order_status | 0.00% | TIDAK | 8 |
| order_purchase_timestamp | 0.00% | TIDAK | 98875 |
| order_approved_at | 0.16% | TIDAK | 90733 |
| order_delivered_carrier_date | 1.79% | TIDAK | 81018 |
| order_delivered_customer_date | 2.98% | TIDAK | 95664 |
| order_estimated_delivery_date | 0.00% | TIDAK | 459 |

### Tabel: olist_order_items_dataset
- **Total Baris:** 112650
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| order_id | 0.00% | TIDAK | 98666 |
| order_item_id | 0.00% | TIDAK | 21 |
| product_id | 0.00% | TIDAK | 32951 |
| seller_id | 0.00% | TIDAK | 3095 |
| shipping_limit_date | 0.00% | TIDAK | 93318 |
| price | 0.00% | TIDAK | 5968 |
| freight_value | 0.00% | TIDAK | 6999 |

### Tabel: olist_order_payments_dataset
- **Total Baris:** 103886
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| order_id | 0.00% | TIDAK | 99440 |
| payment_sequential | 0.00% | TIDAK | 29 |
| payment_type | 0.00% | TIDAK | 5 |
| payment_installments | 0.00% | TIDAK | 24 |
| payment_value | 0.00% | TIDAK | 29077 |

### Tabel: olist_order_reviews_dataset
- **Total Baris:** 99224
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| review_id | 0.00% | TIDAK | 98410 |
| order_id | 0.00% | TIDAK | 98673 |
| review_score | 0.00% | TIDAK | 5 |
| review_comment_title | 88.34% | TIDAK | 4527 |
| review_comment_message | 58.70% | TIDAK | 36159 |
| review_creation_date | 0.00% | TIDAK | 636 |
| review_answer_timestamp | 0.00% | TIDAK | 98248 |

### Tabel: olist_products_dataset
- **Total Baris:** 32951
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| product_id | 0.00% | YA | 32951 |
| product_category_name | 1.85% | TIDAK | 73 |
| product_name_lenght | 1.85% | TIDAK | 66 |
| product_description_lenght | 1.85% | TIDAK | 2960 |
| product_photos_qty | 1.85% | TIDAK | 19 |
| product_weight_g | 0.01% | TIDAK | 2204 |
| product_length_cm | 0.01% | TIDAK | 99 |
| product_height_cm | 0.01% | TIDAK | 102 |
| product_width_cm | 0.01% | TIDAK | 95 |

### Tabel: olist_sellers_dataset
- **Total Baris:** 3095
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| seller_id | 0.00% | YA | 3095 |
| seller_zip_code_prefix | 0.00% | TIDAK | 2246 |
| seller_city | 0.00% | TIDAK | 611 |
| seller_state | 0.00% | TIDAK | 23 |

### Tabel: product_category_name_translation
- **Total Baris:** 71
- **Duplikat Persis:** 0

| Kolom | Null % | Unik / Tidak | Jumlah Unik (Nunique) |
|---|---|---|---|
| product_category_name | 0.00% | YA | 71 |
| product_category_name_english | 0.00% | YA | 71 |

