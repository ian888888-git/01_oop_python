from src.base_data_repository import BaseDataRepository

class CncRepository(BaseDataRepository):
    """
    IMPLEMENTASI NYATA (Concrete Class) - Domain CNC Telemetry.
    Patuh 100% pada BaseDataRepository dan menggunakan konvensi prefix 4 karakter.
    """
    def __init__(self, machine_id: str, default_value: float = 24.0, offset: float = 1.5):
        """
        Inisialisasi parameter fisik mesin CNC.
        - machine_id: ID unik mesin (misal: CNC-01)
        - default_fill: Angka pengganti jika sensor putus (None)
        - calibration_offset: Nilai akurasi tambahan untuk kalibrasi fisik sensor
        """
        self.machine_id = machine_id
        self.default_value = default_value
        self.offset = offset
    
    def exct_raw_data(self) -> list:
        """
        Kategori: EXTRACT
        Simulasi menyerap data arus streaming suhu spindle dari sensor fisik.
        Sengaja disisipkan nilai 'None' untuk mensimulasikan gangguan jaringan pabrik.
        """
        print(f"   [CNC-EXTRACT] Menarik log suhu dari mesin {self.machine_id}...")
        # Simulasi data mentah: Ada data normal, data None (rusak), dan data normal lagi
        return [38.5, None, 40.2, None, 41.8]
    
    def trsf_clean_data(self, raw_data: list) -> list:
        """
        Kategori: TRANSFORM
        Melakukan pembersihan data ganda (Imputasi) + Kalibrasi nilai offset fisik.
        """
        print("   [CNC-TRANSFORM] Memulai proses imputasi data None & kalibrasi offset...")
        clean_records = []
        for item_data in raw_data:
            if item_data is None:
                # Jika data kosong/None, ganti dengan nilai default ruangan (tidak ditambah offset)
                clean_records.append(self.default_value)
            else:
                # Jika data ada, lakukan kalibrasi matematika dengan menambahkan nilai offset
                calibrated_value = item_data + self.offset
                # Membulatkan 1 angka di belakang koma agar presisi data terjaga
                clean_records.append(round(calibrated_value, 1))
        return clean_records
    
    def load_final_data(self, clean_data: list) -> bool:
        """
        Kategori: LOAD
        Simulasi mengunci data matang ke target penyimpanan akhir (Delta Table DBFS).
        """
        print("   [CNC-LOAD] Sukses mengunci data terkalibrasi {clean_data} ke Lakehouse...")
        # Mengembalikan True menandakan proses I/O penyimpanan sukses tanpa hambatan 
        return True