# Enterprise ETL Pipeline Framework

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Docker Certified](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Testing Framework](https://img.shields.io/badge/test-pytest-green.svg)](https://docs.pytest.org/)

Kerangka kerja (framework) berbasis komponen modular dan arsitektur berorientasi objek (OOP) tingkat tinggi untuk standardisasi pipeline data telemetri di lingkungan manufaktur. Proyek ini mengimplementasikan pembatasan arsitektur menggunakan **Abstract Base Classes (ABC)** untuk menjamin konsistensi hulu-ke-hilir, serta dilengkapi dengan enkapsulasi ganda dan metode *debugging/logging reflection* standar industri cloud.

---

## 🏗️ Arsitektur & Pola Desain

Proyek ini dibangun di atas tiga pilar utama konsep OOP Python modern:
1. **Callable Objects (`__call__`):** Mengubah kelas pemroses menjadi entitas yang dapat dieksekusi langsung sebagai fungsi tunggal untuk efisiensi perulangan data streaming (Kafka/CDC).
2. **Object Logging Standard (`__str__` vs `__repr__`):** Memberikan transparansi mutlak pada status parameter internal objek ketika terjadi kegagalan (*crash*) pada klaster produksi cloud (Databricks).
3. **Abstraksi Ketat (`BaseDataPipeline`):** Mengunci arsitektur tim agar patuh pada tiga serangkai metode standar industri: `.extract()`, `.transform()`, dan `.load()`.

---

## 📂 Struktur Direktori Proyek

```text
.
├── src/
│   ├── base_pipeline.py            # Kelas induk abstrak (ABC) & Template Method Pattern
│   ├── cnc_pipeline_component.py   # Kelas anak realisasi konkrit pemrosesan telemetri
│   └── pipeline.py                 # Orkestrator utama (Production Pipeline Facade)
├── tests/
│   └── test_base_pipeline.py       # Unit testing pengunci arsitektur OOP & fail-early system
├── Dockerfile                      # Image build berbasis python:3.11-slim
├── docker-compose.yml              # Konfigurasi lingkungan terisolasi dengan volume mapping
├── main.py                         # Titik awal eksekusi aplikasi (Bootstrap Pattern)
├── README.md                       # Dokumentasi teknis proyek
└── requirements.txt                # Pustaka ketergantungan (PyTest & PyTest-Mock)