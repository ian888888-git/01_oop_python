import pytest 
from src.base_data_repository import BaseDataRepository
from src.cnc_telemetry.cnc_repository import CncRepository

class TestCncTelemetryRepository:
    def test_abstract_contract(self):
        """
        Memastikan hukum Python (ABC) bekerja:
        BaseDataRepository bersifat abstrak dan TIDAK BOLEH diinstansiasi langsung.
        """
        with pytest.raises(TypeError):
            BaseDataRepository()
    
    def test_etl_cycle_success(self):
        """
        Menguji aliran penuh .execute_sync() pada modul CNC.
        Memastikan fungsi mengembalikan True jika semua proses aman.
        """
        repo = CncRepository(machine_id="CNC-01")
        status = repo.execute_sync()
        assert status is True
    
    def test_transformation_logic_for_imputation_calibration(self):
        """
        Menguji ketepatan rumus matematika di trsf_clean_data:
        - Angka normal harus ditambah offset (38.5 + 1.5 = 40.0)
        - Angka None harus diganti default_fill (25.0) TANPA ditambah offset
        """
        # Inisialisasi dengan parameter uji khusus
        repo = CncRepository(
            machine_id="CNC-01",
            default_value=25.0,
            offset=1.5
        )
        raw_data_dummy = [38.5, None, 40.2]
        data_calibrated_expectation = [40.0, 25.0, 41.7]
        actual_data = repo.trsf_clean_data(raw_data_dummy)
        # Memastikan hasil perhitungan matematis 100% akurat
        assert actual_data == data_calibrated_expectation
    
    def test_abc_class_protection(self):
        """
        Memastikan jika ada engineer lain membuat repositori baru tetapi lupa
        menuliskan salah satu fungsi wajib (misal: load_final_data), Python akan memblokirnya.
        """
        class RepositoryCacat(BaseDataRepository):
            def exct_raw_data(self): return []
            def trsf_clean_data(self, data): return data
            # load_final_data sengaja dikosongkan/lupa ditulis
        
        with pytest.raises(TypeError) as info_error:
            objek_cacat = RepositoryCacat()
        assert "abstract method load_final_data" in str(info_error.value)
