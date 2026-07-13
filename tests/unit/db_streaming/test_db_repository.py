import pytest 
from src.db_streaming.db_streaming_repository import DbStreamingRepository

class TestDbStreamingRepository:
    def test_db_streaming_successed_etl_cycle(self):
        """
        Menguji aliran penuh .execute_sync() pada modul DB Streaming.
        Memastikan sirkuit utama mengembalikan True dari hulu ke hilir.
        """
        repo = DbStreamingRepository(connection="postgresql://localhost:5432/prod_db")
        status = repo.execute_sync()
        assert status is True
    
    def test_transformationn_logic_clean_and_masking_data(self):
        """
        Menguji akurasi pembersihan teks dan penyamaran data sensitif (UU PDP):
        - Status dengan spasi gaib dan huruf kecil harus bersih & kapital ("pending " -> "PENDING")
        - Kolom email harus tersamar dengan benar ("ardian.webi@gmail.com" -> "a***********@gmail.com")
        """
        repo = DbStreamingRepository(connection="postgresql://dummy_url")
        # Data tiruan (Dummy) untuk uji logika
        raw_data_dummy = [
            {
                "order_id": 88,
                "amount": 8000.0,
                "status": " failed ",
                "customer_email": "ardian.webi@gmail.com"
            }
        ]

        # Hasil yang kita harapkan secara presisi
        ekspektasi_hasil = [
            {
                "order_id":88,
                "amount": 8000.0,
                "status": "FAILED",                # Harus bersih dari spasi & kapital
                "customer_email": "a**********@gmail.com"  # Karakter ke-2 dan seterusnya diganti bintang
            }
        ]

        hasil_aktual = repo.trsf_clean_data(raw_data_dummy)
        # Memastikan output transformasi 100% cocok dengan ekspektasi bisnis
        assert hasil_aktual == ekspektasi_hasil

    def test_helper_masking_email(self):
        """
        Menguji ketahanan fungsi private _apply_email_masking jika menerima
        input string email yang tidak valid atau rusak dari database.
        """
        repo = DbStreamingRepository(connection="postgresql://dummy_url")
        email_rusak = "bukan_email_valid_tanpa_at"
        ekspektasi_fallback = "masked_user@hidden.com"
        # Memanggil fungsi private menggunakan nama aslinya
        hasil_masking = repo._apply_email_masking(email_rusak)
        assert hasil_masking == ekspektasi_fallback
