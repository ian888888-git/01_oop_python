from typing import TypeVar, Generic, Callable, List, Dict, Any
# 1. Mendefinisikan TypeVar sebagai placeholder Generik
# 'T' bisa mewakili struktur dictionary data apa pun yang masuk ke pipeline
T = TypeVar('T')
class LogDataPipeline(Generic[T]):
    """
    SUBSTANSI: Mesin Pipeline Generik untuk memproses log e-commerce.
    Menggunakan Generic[T] agar kelas ini fleksibel menerima struktur log apa pun,
    namun tetap terkunci ketat oleh validasi tipe data dari Linter.
    """
    def __init__(self, raw_logs: List[T]):
        """
        Inisialisasi pipeline dengan daftar log mentah.
        List[T] memastikan seluruh isi list memiliki tipe data/struktur yang seragam.
        """
        self.__raw_logs: List[T] = raw_logs
    
    @property
    def raw_logs(self) -> List[T]:
        """Getter untuk membaca data log mentah di dalam memori."""
        return self.__raw_logs
    
    def trsf_execute_transformation(self, processor_callback: Callable[[T], Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        SUBSTANSI: Mengeksekusi fungsi transformasi menggunakan teknik Callback.
        PENJELASAN TYPE HINTING:
        - processor_callback: Callable[[T], Dict[str, Any]]
          Artinya: Argumen ini WAJIB berupa fungsi (callable). Fungsi tersebut 
          wajib menerima satu parameter ber-tipe 'T' dan wajib mengembalikan (return) Dictionary.
        - Return dari fungsi ini: List[Dict[str, Any]]
          Artinya: Mengembalikan daftar matriks terstruktur berupa list of dictionaries.
        """

        processed_matrix: List[Dict[str, Any]] = []
        """
        processed_matrix: List[Dict[str, Any]] = []
        Substansi: Ini adalah deklarasi penampung hasil akhir (matriks data) yang sudah bersih.
        Penjelasan Type Hinting: Kita mengunci variabel ini dengan tipe List[Dict[str, Any]]. 
        Artinya, variabel processed_matrix wajib berupa sebuah List (Array) yang di dalamnya berisi 
        Dictionary (Associative Array). Kunci dictionary tersebut harus berupa str (String), 
        sedangkan nilainya (value) boleh bertipe apa saja (Any, seperti int, float, atau string).
        """
        for log in self.__raw_logs:
            # Mengeksekusi fungsi callback yang dikirim dari luar
            transformed_record = processor_callback(log)
            processed_matrix.append(transformed_record)
        return processed_matrix
