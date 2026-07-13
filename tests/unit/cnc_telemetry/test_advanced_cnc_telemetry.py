import pytest 
from src.cnc_telemetry.advanced_cnc_repository import AdvancedCncRepository

class TestAdvancedCncRepository:
    def test_jalur_getter_harus_bisa_membaca_nilai_konfigurasi_awal(self):
        """
        SUBSTANSI: Menguji sirkuit AKSES BACA (Getter / Cek Saldo).
        Memastikan sistem bisa menarik data dari brankas internal tanpa mengubahnya.
        """
        repo = AdvancedCncRepository("CNC-ADV-01", 50.0)
        # Fokus: Memastikan fungsi pembacaan mengembalikan angka yang benar
        assert repo.anomaly_treshold == 50.0
    
    def test_jalur_setter_harus_bisa_mengubah_dan_menimpa_nilai_dengan_data_baru(self):
        """
        SUBSTANSI: Menguji sirkuit PROSES UPDATE (Setter / Setor Tunai).
        Memastikan variabel privat di memori berhasil ditimpa oleh angka baru yang lolos validasi.
        """
        repo = AdvancedCncRepository("CNC-ADV-02", 50.0)
        # AKTIVITAS 1: Memicu fungsi Setter untuk menimpa memori (50.0 -> 65.5)
        repo.anomaly_treshold = 65.5 
        # AKTIVITAS 2: Memastikan nilai di dalam memori baru memang sudah berubah
        assert repo.anomaly_treshold == 65.5
    
    def test_gerbang_validasi_setter_wajib_menolak_dan_melempar_error_jika_angka_ekstrem(self):
        """
        SUBSTANSI: Verifikasi Barikade Keamanan Batas Angka (Value Validation).
        Memastikan satpam @setter langsung memblokir dan melemparkan 'ValueError' 
        jika ada penyusup yang mencoba memasukkan angka di luar rentang aman (0 - 100°C).
        """
        # 1. Siapkan objek dengan batas normal awal
        repo = AdvancedCncRepository("CNC-ADV-03", 50.0)
        # 2. Uji batas atas: Mencoba menyusupkan suhu ekstrem 150.0°C (Harus Terblokir)
        with pytest.raises(ValueError) as info_error:
            repo.anomaly_treshold = 150.0
        # Memastikan teks pesan peringatan dari pabrik keluar dengan tepat
        assert "Nilai threshold harus antara 0 sampai 100" in str(info_error.value)

    def test_gerbang_validasi_setter_wajib_menolak_dan_melempar_error_jika_tipe_data_bukan_numerik(self):
        """
        SUBSTANSI: Verifikasi Barikade Tipe Data (Type Validation).
        Memastikan satpam @setter langsung melempar 'TypeError' jika mendeteksi 
        input data selain angka (seperti String), mencegah kerusakan fatal pada perhitungan ETL.
        """
        # 1. Siapkan objek dengan batas normal awal
        repo = AdvancedCncRepository("CNC-ADV-04", 50.0)
        # 2. Uji tipe data: Mencoba memasukkan teks String (Harus Terblokir)
        with pytest.raises(TypeError) as info_error:
            repo.anomaly_treshold = "DELAPAN PULUH DELAPAN"
        # Memastikan pesan proteksi tipe data keluar dengan tepat
        assert "harus berupa angka numerik" in str(info_error.value)