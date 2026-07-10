# Enterprise ETL Pipeline Framework

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Docker Certified](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Testing Framework](https://img.shields.io/badge/test-pytest-green.svg)](https://docs.pytest.org/)

Kerangka kerja (framework) berbasis komponen modular skala besar menggunakan **Repository Design Pattern** dan arsitektur berorientasi objek (OOP) tingkat tinggi untuk standardisasi pipeline data di lingkungan manufaktur modern. Proyek ini mengimplementasikan pembatasan arsitektur menggunakan **Abstract Base Classes (ABC)** untuk menjamin konsistensi integrasi multi-studi kasus.

---

## 🏗️ Arsitektur & Pola Desain

Proyek ini menggunakan kombinasi dua pola desain utama untuk mengelola kompleksitas data:
1. **Repository Design Pattern (`BaseDataRepository`):** Memisahkan logika bisnis pengolahan data dengan detail teknis penyerapan dari hulu database/sensor. Mengunci kontrak tiga serangkai metode wajib: `.fetch_all()`, `.process_data()`, dan `.save()`.
2. **Facade/Orchestrator Pattern (`ProductionPipeline`):** Bertindak sebagai jembatan terpusat tunggal yang merajut dan mengeksekusi berbagai domain studi kasus yang tersebar di sub-folder.

---

## 📂 Struktur Direktori Proyek (Modular & Skala Besar)

Struktur di bawah ini menerapkan **Prinsip Cermin (1-to-1 Mapping)** antara folder sumber daya (`src/`) dan folder pengujian unit berdasarkan nama domain studi kasus, serta menyediakan ruang untuk ekspansi pengujian multi-layer.

```text
.
├── src/                               # 🚀 LOGIKA UTAMA PRODUKSI
│   ├── __init__.py
│   ├── base_repository.py             # Kelas induk abstrak (ABC) untuk Repository Pattern
│   │
│   ├── cnc_telemetry/                 # 🔹 Domain Studi Kasus 1: Sinyal Mesin CNC
│   │   ├── __init__.py
│   │   ├── cnc_repository.py          # Sinkronisasi data hulu-hilir CNC
│   │   └── cnc_transformer.py         # Modul rumus matematika/kalibrasi sensor CNC
│   │
│   ├── kafka_ingestion/               # 🔹 Domain Studi Kasus 2: Data Antrean Kafka (Eskalasi)
│   │   ├── __init__.py
│   │   └── kafka_repository.py
│   │
│   └── pipeline.py                    # 🎛️ Jembatan Terpusat (Orkestrator Utama / Facade)
│
├── tests/                             # 🧪 PIRAMIDA PENGUJIAN OTOMATIS
│   ├── __init__.py
│   │
│   ├── unit/                          # 📦 LAPISAN 1: UNIT TESTING (Isolasi Fungsi)
│   │   ├── __init__.py
│   │   ├── cnc_telemetry/             # Cerminan Sempurna Domain Studi Kasus 1
│   │   │   ├── test_cnc_repository.py
│   │   │   └── test_cnc_transformer.py
│   │   │
│   │   └── kafka_ingestion/           # Cerminan Sempurna Domain Studi Kasus 2
│   │       └── test_kafka_repository.py
│   │
│   ├── integration/                   # 🔗 LAPISAN 2: INTEGRATION TESTING (Hubungan Antar Modul)
│   │   ├── __init__.py
│   │   └── test_pipeline_jembatan.py  # Memastikan interaksi antar-repo di pipeline.py sinkron
│   │
│   └── e2e/                           # 🌐 LAPISAN 3: END-TO-END TESTING (Simulasi Aliran Penuh)
│       ├── __init__.py
│       └── test_full_etl_flow.py      # Menguji aliran data nyata dari raw data hingga masuk ke Storage Cloud
│
├── Dockerfile                         # Image build berbasis python:3.11-slim
├── docker-compose.yml                 # Konfigurasi lingkungan terisolasi dengan volume mapping
├── main.py                            # Titik awal eksekusi aplikasi (Bootstrap Pattern - Tetap Suci)
└── requirements.txt                   # Pustaka ketergantungan (PyTest & PyTest-Mock)