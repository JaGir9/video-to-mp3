# Universal Video to Audio Converter

Simple batch converter berbasis **Python + FFmpeg** untuk mengekstrak audio dari semua file video yang terdeteksi di folder `Video/`.

Tool ini tidak bergantung pada daftar ekstensi tertentu. Selama file dapat dibaca oleh FFmpeg dan memiliki video stream, file akan dideteksi secara otomatis.

## Fitur

- Batch convert semua video dalam satu folder
- Deteksi file video menggunakan `ffprobe`
- Mendukung berbagai format/container yang didukung FFmpeg
- Pilihan output:
  - MP3 320 kbps
  - WAV PCM Lossless
  - FLAC Lossless
  - AAC 320 kbps
  - M4A AAC 320 kbps
  - OGG Vorbis
  - OPUS 256 kbps
- Nama file asli dipertahankan
- Output dipisahkan otomatis berdasarkan format
- Mencegah overwrite jika nama output sudah ada
- Menampilkan jumlah file berhasil dan gagal
- Tidak memerlukan package Python tambahan

## Struktur Folder

```text
video-to-mp3/
├── convert.py
├── README.md
├── LICENSE
├── .gitignore
└── Video/
    ├── video-01.mp4
    ├── video-02.mkv
    └── ...
```

Folder output dibuat otomatis sesuai format yang dipilih:

```text
MP3/
WAV/
FLAC/
AAC/
M4A/
OGG/
OPUS/
```

## Requirements

- Python 3.8 atau lebih baru
- FFmpeg
- FFprobe (biasanya sudah termasuk bersama instalasi FFmpeg)

Cek instalasi:

```bash
python --version
ffmpeg -version
ffprobe -version
```

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/JaGir9/video-to-mp3.git
cd video-to-mp3
```

### 2. Install FFmpeg

#### Windows

Download FFmpeg dari situs resmi:

https://ffmpeg.org/download.html

Setelah diekstrak, tambahkan folder `bin` FFmpeg ke Windows `PATH`.

Contoh:

```text
C:\ffmpeg\bin
```

Tutup dan buka kembali Command Prompt/PowerShell, kemudian cek:

```powershell
ffmpeg -version
ffprobe -version
```

Jika menggunakan Winget:

```powershell
winget install Gyan.FFmpeg
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Fedora

```bash
sudo dnf install ffmpeg
```

#### macOS

Dengan Homebrew:

```bash
brew install ffmpeg
```

## Cara Menggunakan

### 1. Masukkan video

Simpan semua file video ke folder:

```text
Video/
```

Contoh:

```text
Video/
├── movie.mp4
├── clip.mkv
├── recording.mov
└── sample.webm
```

### 2. Jalankan script

Windows:

```powershell
python convert.py
```

Linux/macOS:

```bash
python3 convert.py
```

### 3. Pilih format audio

Menu:

```text
[1] MP3  - 320 kbps
[2] WAV  - PCM Lossless
[3] FLAC - Lossless
[4] AAC  - 320 kbps
[5] M4A  - AAC 320 kbps
[6] OGG  - Vorbis High Quality
[7] OPUS - 256 kbps
```

Masukkan angka, misalnya:

```text
1
```

Semua video akan dikonversi ke MP3.

## Contoh

Input:

```text
Video/
├── video1.mp4
├── video2.mkv
└── video3.mov
```

Jika memilih MP3:

```text
MP3/
├── video1.mp3
├── video2.mp3
└── video3.mp3
```

Jika memilih FLAC:

```text
FLAC/
├── video1.flac
├── video2.flac
└── video3.flac
```

## Dukungan Format Video

Script tidak menggunakan whitelist ekstensi. Deteksi dilakukan berdasarkan stream video dengan FFprobe.

Artinya format/container seperti berikut umumnya dapat digunakan jika didukung build FFmpeg Anda:

`MP4`, `MKV`, `MOV`, `AVI`, `WEBM`, `M4V`, `FLV`, `WMV`, `MPEG`, `MPG`, `TS`, `MTS`, `M2TS`, `3GP`, dan lainnya.

Dukungan aktual mengikuti kemampuan FFmpeg yang terinstall.

## Catatan Kualitas

Mengubah video ke format lossless seperti WAV atau FLAC tidak dapat meningkatkan kualitas audio sumber. Format tersebut hanya mencegah kompresi lossy tambahan pada hasil output.

Untuk penggunaan umum, MP3 320 kbps atau M4A/AAC biasanya sudah sangat baik.

## Troubleshooting

### FFmpeg tidak ditemukan

Jika muncul:

```text
ERROR: ffmpeg tidak ditemukan.
```

Pastikan FFmpeg sudah terinstall dan tersedia pada environment `PATH`.

### Folder Video kosong

Pastikan file berada langsung di:

```text
Video/
```

Versi saat ini tidak melakukan recursive scan ke subfolder.

### Video tanpa audio

Video yang tidak memiliki audio stream tidak dapat menghasilkan file audio yang valid dan akan tercatat sebagai gagal.

## Update Repository

Jika sebelumnya sudah clone repository:

```bash
git pull origin main
```

## License

Project ini menggunakan MIT License. Lihat file [LICENSE](LICENSE).

## Disclaimer

Gunakan tool ini hanya pada media yang Anda miliki atau yang Anda memiliki izin untuk memproses. Pengguna bertanggung jawab terhadap kepatuhan hak cipta dan ketentuan penggunaan media masing-masing.
