# Aplikasi POS (Point of Sale) Sederhana dengan Django

Ini adalah aplikasi kasir berbasis web sederhana yang dibangun menggunakan framework Django. Aplikasi ini dirancang untuk menangani proses transaksi penjualan dasar, manajemen produk, dan pelaporan.

## ✨ Fitur Utama

-   **Manajemen Produk**: Tambah, Edit, Hapus produk lengkap dengan kategori, harga, dan stok.
-   **Proses Transaksi**: Halaman kasir interaktif untuk menambah produk ke keranjang dan memproses pembayaran.
-   **Hitung Kembalian**: Fitur modal untuk memasukkan jumlah uang tunai dari pelanggan dan menghitung kembalian secara otomatis.
-   **Cetak Struk**: Setelah transaksi berhasil, sistem akan menghasilkan struk yang siap untuk di-print.
-   **Laporan Penjualan**: Halaman khusus untuk melihat riwayat semua transaksi yang telah terjadi.
-   **Sistem Autentikasi**: Halaman kasir dan laporan diamankan dengan sistem login.
-   **Hak Akses Pengguna**: Peran pengguna (Admin dan Kasir) dibedakan, di mana hanya Admin yang dapat melihat laporan penjualan.

## 🛠️ Teknologi yang Digunakan

-   **Backend**: Python & Django
-   **Frontend**: HTML, Bootstrap 5, JavaScript (Vanilla)
-   **Database**: SQLite (untuk development)

## 🚀 Cara Menjalankan Proyek Secara Lokal

Berikut adalah langkah-langkah untuk menjalankan proyek ini di komputermu sendiri:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/VonMatilda07/django-kasir-pos.git](https://github.com/VonMatilda07/django-kasir-pos.git)
    cd django-kasir-pos
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    # Windows
    py -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install semua dependensi yang dibutuhkan:**
    ```bash
    pip install django
    ```

4.  **Terapkan migrasi database:**
    ```bash
    py manage.py migrate
    ```

5.  **Buat akun superuser untuk bisa login:**
    ```bash
    py manage.py createsuperuser
    ```

6.  **Jalankan server development:**
    ```bash
    py manage.py runserver
    ```

7.  Buka browser dan kunjungi `http://127.0.0.1:8000/`. Kamu akan diarahkan ke halaman login.
