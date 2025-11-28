# GeoViz Pro - Visualisasi Reservoir 3D

**Tugas Pemetaan Bawah Permukaan IF-A**

## List Kontributor

-   [Muhammad Luqmaan - 123230070]
-   [Salman Faris - 123230024]

**Peta Struktur Interaktif & Pemodelan Kontak Fluida**

Website ini adalah aplikasi berbasis Streamlit yang dirancang untuk visualisasi 3D model reservoir bawah permukaan. Aplikasi ini memungkinkan pengguna untuk memasukkan data koordinat, memvisualisasikan peta kontur 2D, dan menghasilkan model permukaan 3D dengan bidang kontak fluida interaktif (Gas-Oil Contact dan Water-Oil Contact).

## Fitur

-   **Input Data Interaktif**: Tambahkan titik koordinat (X, Y, Z) dengan mudah melalui sidebar.
-   **Pemetaan Kontur 2D**: Visualisasikan struktur reservoir dengan garis kontur 2D dan zona fluida (Gas Cap, Oil Zone, Aquifer).
-   **Pemodelan Permukaan 3D**: Jelajahi reservoir dalam 3D dengan permukaan medan dan bidang GOC/WOC yang dapat disesuaikan.
-   **Kontrol Kontak Fluida**: Sesuaikan level Gas-Oil Contact (GOC) dan Water-Oil Contact (WOC) secara dinamis.
-   **Manajemen Data**: Reset data atau muat dataset demo untuk pengujian cepat.

## Instalasi

1.  **Clone repositori** (jika ada):
    ```bash
    git clone <repository-url>
    cd 3d-map
    ```

2.  **Instal dependensi**:
    Pastikan Anda telah menginstal Python, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan

1.  **Jalankan aplikasi**:
    ```bash
    streamlit run app.py
    ```

2.  **Input Data**:
    -   Gunakan panel **Input Koordinat** di sidebar untuk menambahkan titik.
    -   Atau, buka **Pengaturan Data** dan klik **Load Data Demo**.

3.  **Eksplorasi**:
    -   Pindah antara tab **Peta Kontur 2D**, **Model 3D**, dan **Data Mentah** untuk melihat visualisasi yang berbeda.
    -   Sesuaikan slider **Gas-Oil Contact** dan **Water-Oil Contact** di sidebar untuk melihat bagaimana mereka berpotongan dengan struktur reservoir.

## Dependensi

-   [Streamlit](https://streamlit.io/)
-   [Pandas](https://pandas.pydata.org/)
-   [Plotly](https://plotly.com/python/)
-   [NumPy](https://numpy.org/)
-   [SciPy](https://scipy.org/)
