from src.base_data_repository import BaseDataRepository

class AdvancedCncRepository(BaseDataRepository):
    """
    IMPLEMENTASI LANJUTAN - Domain CNC Telemetry dengan Enkapsulasi Ketat.
    Menggunakan @property untuk melindungi parameter konfigurasi kritis.
    """
    def __init__(self, machine_id: str, initial_treshold: float = 46.0):
        self.machine_id = machine_id
        # Variabel internal di-hidden menggunakan double underscore (Private Attribute)
        # Tidak bisa diakses langsung dari luar sebagai .__anomaly_threshold
        self.__anomaly_treshold = float(initial_treshold)
    
    # --- 1. GERBANG GETTER ---
    @property
    def anomaly_treshold(self) -> float:
        """Gerbang membaca nilai: Mengembalikan nilai threshold privat."""
        return self.__anomaly_treshold

    # --- 2. GERBANG SETTER ---
    @anomaly_treshold.setter
    def anomaly_treshold(self, new_value: float):
        """Gerbang mengubah nilai: Wajib melalui validasi logika pabrik."""
        if not isinstance(new_value, (int, float)):
            raise TypeError("[SECURITY ALERT] Nilai threshold harus berupa angka numerik!")
        if new_value < 0.0 or new_value > 100.0:
            raise ValueError("[SECURITY ALERT] Nilai threshold harus antara 0 sampai 100!")
        print(f"⚙️ [CONFIG UPDATE] Threshold mesin {self.machine_id} berhasil diubah ke: {new_value}°C")
        self.__anomaly_treshold = float(new_value)
    
    # --- Implementasi Fungsi Wajib Sesuai Kontrak Base ---
    def exct_raw_data(self) -> list:
        return [38.5, 42.0, 46.5, 39.0]

    def trsf_clean_data(self, raw_data: list) -> list:
        # Contoh penggunaan: Menandai jika ada suhu yang melompat melewati batas threshold privat
        clean_records = []
        for temp in raw_data:
            status_log = "ANOMALY" if temp > self.anomaly_treshold else "NORMAL"
            clean_records.append({"temp":temp, "status":status_log})
        return clean_records
    def load_final_data(self, clean_data: list) -> bool:
        return True
        
