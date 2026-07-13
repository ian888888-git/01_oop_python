import pytest 
from typing import Dict, Any
from src.analytics.log_pipeline import LogDataPipeline

# --- FUNGSI CALLBACK TIRUAN (MOCK PROCESSOR) UNTUK LOG KLIK ---
def mock_click_log_processor(raw_log: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fungsi penentu callback yang mematuhi kontrak Callable[[T], Dict[str, Any]].
    Mengubah status ip address menjadi anonim dan membersihkan nama event.
    """
    return {
        "event_name": raw_log["event"].strip().upper(),
        "ip_address": "xxx.xxx.xxx" if "ip" in raw_log else "0.0.0.0",
        "product_id": raw_log.get("product_id", 0)
    }

class TestLogDataPipeline:
    def test_jalur_generik_harus_bisa_menyimpan_dan_membaca_log_mentah_pada_inisialisasi(self):
        """
        SUBSTANSI: Verifikasi Penampung Generik (Generic Storage Verification).
        Memastikan placeholder tipe data mampu mengunci dan mengembalikan daftar log mentah 
        secara utuh melalui fungsi Getter properti tanpa merusak strukturnya.
        """
        raw_click_data = [
            {"event": " click_cart ", "ip": "192.168.1.1", "product_id": 101},
            {"event": "view_page", "ip": "192.168.1.2", "product_id": 102}
        ]

        # Menginisialisasi kelas Generik khusus untuk menangani list of dictionaries data klik
        pipeline = LogDataPipeline(raw_logs=raw_click_data)
        assert pipeline.raw_logs == raw_click_data
    
    def test_jalur_callable_callback_harus_sukses_mengeksekusi_transformasi_matriks_log(self):
        """
        SUBSTANSI: Verifikasi Eksekusi Callback Kompleks (Callable Executive Verification).
        Memastikan fungsi pipeline mampu menerima fungsi luar (callback), mengeksekusinya 
        pada setiap baris data secara berurutan, dan menghasilkan matriks keluaran yang sesuai.
        """
        raw_click_data = [
            {"event": " click_product  ", "ip": "10.0.0.1", "product_id": 555}
        ]

        ekspektasi_hasil_matrix = [
            {"event_name": "CLICK_PRODUCT", "ip_address": "xxx.xxx.xxx", "product_id": 555}
        ]

        pipeline = LogDataPipeline(raw_logs=raw_click_data)

        # Mengirimkan fungsi 'mock_click_log_processor' sebagai argumen Callable ke dalam pipeline
        hasil_aktual = pipeline.trsf_execute_transformation(mock_click_log_processor)

        # SINKRONISASI TOTAL: Memastikan output akhir 100% identik dengan spesifikasi bisnis
        assert hasil_aktual == ekspektasi_hasil_matrix