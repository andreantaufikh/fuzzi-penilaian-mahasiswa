# 🎓 Sistem Penilaian Mahasiswa Menggunakan Logika Fuzzy (Kasus 1)

Repository ini berisi implementasi **Kasus 1: Penilaian Mahasiswa** menggunakan **Logika Fuzzy (Fuzzy Logic)** dengan antarmuka web interaktif berbasis **Streamlit**. Proyek ini dibuat untuk memenuhi Tugas Praktikum Logika Fuzzy (Dosen Pengampu: Pak Indrawan).

## 📊 Detail Studi Kasus 1
- **Variabel Input:** Nilai Ujian (skala $0 - 100$)
- **Himpunan Fuzzy (Output Keanggotaan):**
  - **Rendah** (Domain: $0 - 60$)
  - **Sedang** (Domain: $40 - 80$)
  - **Tinggi** (Domain: $60 - 100$)

---

## 📐 Fungsi Keanggotaan & Rumus Matematis

### 1. Kategori Rendah
$$
\mu_{\text{Rendah}}(x) = \begin{cases} 
1, & \text{jika } x \le 40 \\
\frac{60 - x}{60 - 40}, & \text{jika } 40 < x < 60 \\
0, & \text{jika } x \ge 60
\end{cases}
$$

### 2. Kategori Sedang
$$
\mu_{\text{Sedang}}(x) = \begin{cases}
0, & \text{jika } x \le 40 \text{ atau } x \ge 80 \\
\frac{x - 40}{60 - 40}, & \text{jika } 40 < x < 60 \\
\frac{80 - x}{80 - 60}, & \text{jika } 60 \le x < 80
\end{cases}
$$

### 3. Kategori Tinggi
$$
\mu_{\text{Tinggi}}(x) = \begin{cases}
0, & \text{jika } x \le 60 \\
\frac{x - 60}{80 - 60}, & \text{jika } 60 < x < 80 \\
1, & \text{jika } x \ge 80
\end{cases}
$$

---

## 🚀 Fitur Utama Aplikasi
1. **Teori & Konsep:** Menampilkan visualisasi grafik fungsi keanggotaan menggunakan *Plotly* yang interaktif serta penjelasan rumus LaTeX.
2. **Perhitungan Individu (Traceability):** Uji coba nilai satu mahasiswa secara interaktif dengan visualisasi garis potong grafik dan penjelasan langkah demi langkah substitusi rumus (*step-by-step trace*).
3. **Data Kelompok (Tabel & Bulk):**
   - Tabel interaktif (`st.data_editor`) untuk menambah, mengedit, atau menghapus data mahasiswa secara langsung.
   - Fitur upload file CSV untuk memproses data mahasiswa secara massal.
   - Fitur unduh hasil kalkulasi dalam bentuk file CSV.
   - Visualisasi grafik batang distribusi kategori mahasiswa dan diagram sebaran keanggotaan.

---

## 💻 Cara Menjalankan Aplikasi Secara Lokal

### 1. Kloning Repository
```bash
git clone <url-repository-anda>
cd Logika_fuzzi (Penilaian mahasiswa)
```

### 2. Buat & Aktifkan Virtual Environment (Opsional tetapi Direkomendasikan)
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Streamlit
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di browser Anda pada alamat `http://localhost:8501`.

---

## 🌐 Cara Deploy ke Streamlit Sharing

1. **Upload ke GitHub:**
   - Buat repository baru di GitHub.
   - Push folder ini (`app.py`, `requirements.txt`, `README.md`) ke repository GitHub Anda.

2. **Deploy di Streamlit Community Cloud:**
   - Kunjungi [share.streamlit.io](https://share.streamlit.io/).
   - Login menggunakan akun GitHub Anda.
   - Klik button **"New app"**.
   - Pilih repository, branch, dan tentukan file utama yaitu `app.py`.
   - Klik **"Deploy!"**. Aplikasi Anda akan aktif dalam beberapa menit secara gratis.
