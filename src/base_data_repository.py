from abc import ABC, abstractmethod

class BaseDataRepository(ABC):
    """
    KONTRAK UTAMA (Abstract Base Class) - Repository Pattern.
    Menjadi cetak biru wajib untuk semua modul pengolahan data.
    Menggunakan awalan 4 karakter (exct_, trsf_, load_) sesuai kesepakatan.
    """

    @abstractmethod
    def exct_raw_data(self) -> list:
        """
        Kategori: EXTRACT
        Tugas: Mengambil data mentah dari hulu (Sensor / DB / API).
        Wajib diisi oleh kelas anak.
        """
        pass

    @abstractmethod
    def trsf_clean_data(self, raw_data: list) ->list:
        """
        Kategori: TRANSFORM
        Tugas: Membersihkan data, rumus matematika, atau kalibrasi sensor.
        Wajib diisi oleh kelas anak.
        """
        pass

    @abstractmethod
    def load_final_data(self, clean_data: list) -> bool:
        """
        Kategori: LOAD
        Tugas: Menyimpan data matang ke hilir (Storage / Delta Table).
        Wajib diisi oleh kelas anak.
        """
        pass

    def execute_sync(self) -> bool:
        """
        KONDUKTOR UTAMA (Template Method Pattern).
        Fungsi ini otomatis diwarisi oleh kelas anak (tidak abstrak).
        Tugasnya: Menjalankan siklus ETL secara berurutan dan mengamankan error.
        """
        print(f"\n⚡ [START REPO] Memulai Sinkronisasi: {self.__class__.__name__}")
        try:
            # 1. Ambil Data Mentah (Extract)
            raw_data = self.exct_raw_data()
            # 2. Olah Data Mentah jadi Bersih (Transform)
            clean_data = self.trsf_clean_data(raw_data)
            # 3. Simpan Data Bersih ke Tujuan (Load)
            save_status = self.load_final_data(clean_data)

            print(f"✅ [SUCCESS REPO] Sinkronisasi {self.__class__.__name__} Berhasil Sempurna.")
            return save_status
        except Exception as e:
            # Jika di tengah jalan ada kode kelas anak yang crash, ditangkap di sini
            print(f"❌ [REPOSITORY CRASH] Kegagalan sistem pada {self.__class__.__name__}: {str(e)}")
            return False