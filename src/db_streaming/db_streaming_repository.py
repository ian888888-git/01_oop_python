import re 
from src.base_data_repository import BaseDataRepository

class DbStreamingRepository(BaseDataRepository):
    """
    IMPLEMENTASI NYATA (Concrete Class) - Domain Database Streaming (CDC).
    Menangani standardisasi data tekstual dan enkapsulasi privasi (Data Masking).
    Patuh 100% pada kesepakatan prefix 4 karakter (exct_, trsf_, load_).
    """

    def __init__(self, connection: str):
        """
        Inisialisasi koneksi logis ke database sumber.
        - connection_string: URL/Kredensial database (misal: postgresql://...)
        """
        self.connection = connection
    
    def exct_raw_data(self) -> list:
        """
        Kategori: EXTRACT
        Simulasi menangkap log transaksi secara real-time dari database hulu (OLTP).
        Sengaja membawa data teks status yang berantakan dan email dalam bentuk teks polos.
        """
        print(f"    [DB-EXRACT] Membaca log transaksi dari {self.connection}...")

        # Mengembalikan data mentah dalam bentuk list of dictionaries
        return [
            {
                "order_id":1001,
                "amount":100000.00,
                "status":"pending",
                "costumer_email":"murayama@example.com"
            },
                        {
                "order_id":1002,
                "amount":200000.00,
                "status":"SUCCESS",
                "costumer_email":"toyama@example.com"
            }
        ]
    
    def trsf_clean_data(self, raw_data: list) -> list:
        """
        Kategori: TRANSFORM
        Melakukan penataan teks (Text Normalization) dan penyaranan email (Data Masking).
        """
        print("   [DB-TRANSFORM] Memulai standardisasi status transaksi & masking data sensitif...")
        processed_records = []
        for record in raw_data:
            # Membuat salinan dict agar tidak merusak data mentah asli
            clean_record = record.copy()
            # 1. Standardisasi Status: Hapus spasi di ujung-ujung (.strip()) + Paksa huruf besar (.upper())
            clean_record["status"] = clean_record["status"].strip().upper()
            # 2. Data Masking Email: Ubah "ardian.webi@gmail.com" -> "a*****@gmail.com"
            raw_email = clean_record["costumer_email"]
            clean_email = self._apply_email_masking(raw_email)
            processed_records.append(clean_record)
        
        return processed_records
    
    def load_final_data(self, clean_data: list) -> bool:
        """
        Kategori: LOAD
        Simulasi menulis data transaksi yang sudah patuh privasi ke Delta Table Cloud Lakehouse.
        """
        print("   [DB-LOAD] Sukses mengamankan {len(clean_data)} baris data CDC ke Lakehouse....")
    
    def _apply_email_masking(self, email: str) -> str:
        """
        Fungsi Helper Internal (Private Method):
        Mengubah karakter email menjadi anonim demi mematuhi regulasi UU PDP / GDPR.
        """
        try:
            name_part, domain_part = email.split("@")
            if len(name_part) <= 1:
                masked_name = "*"
            else:
                # Mengambil huruf pertama, sisanya diganti bintang sepanjang karakter nama tersebut
                masked_name = name_part[0] + "*" * (len(name_part) - 1)
            return f"{masked_name}@{domain_part}"
        except Exception:
            # Jika format email rusak/tidak valid, kembalikan nilai default aman
            return "masked_user@hidden.com"