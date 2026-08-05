# Tripwire & Funnel Offer Generator (Modular Edition)

Sistem otomatisasi berbasis multi-agen untuk meriset, mensimulasikan, dan memvalidasi penawaran Tripwire & Funnel digital marketing (performance marketing) dengan data lapangan riil menggunakan Exa & Tavily API.

---

## 1. STRUKTUR PROYEK & AGENT DECOUPLING

Sistem ini memisahkan tanggung jawab logika ke dalam modul-modul agen spesialis di bawah `/home/ubuntu/projects/tripwire/scripts/`:

*   `base_agent.py`: Utility LLM global, pembersihan string JSON, dan penanganan model `llama-3.3-70b`.
*   `mcp_helper.py`: Integrasi API Exa, Tavily, dan fallback ScraperAPI Google Search.
*   `intake_agent.py`: Membedah search intent (5W1H) untuk menghasilkan query riset yang bersih.
*   `persona_agent.py`: Memetakan minimal 5 persona UMKM spesifik lengkap dengan data *deep pain* operasional.
*   `rejection_agent.py`: Mensimulasikan keberatan dan pola penolakan persona terhadap tripwire generik.
*   `synthesis_agent.py`: Merumuskan rekomendasi tripwire spesifik per persona berdasarkan deliverables dan tingkat effort.
*   `funnel_ascent_agent.py`: Merancang transisi logis dari Tripwire -> Order Bump -> Core Offer -> Upsell.
*   `validation_agent.py`: Melakukan validasi otomatis terhadap 12-Point Guideline dengan model perbaikan (QA Fixer).
*   `exporter_agent.py`: Menggabungkan seluruh temuan menjadi berkas laporan akhir markdown terperinci.
*   `orchestrator.py`: Pengendali utama alur eksekusi (state machine) pipeline.

---

## 2. STATE MANAGEMENT & STATEFUL RESUME

Untuk menghindari pemborosan kuota API pencarian (Exa/Tavily) dan token LLM saat terjadi interupsi atau kegagalan model di tengah jalan, sistem mengimplementasikan pelacakan state menggunakan:
`/home/ubuntu/projects/tripwire/artifacts/state.json`

### Cara Kerja:
Setiap langkah yang berhasil diselesaikan akan memperbarui nilai `"current_step"` di dalam `state.json` dan menyimpan data antara di dalam `/home/ubuntu/projects/tripwire/artifacts/`. Jika eksekusi terhenti, Anda dapat melanjutkan dari langkah terakhir tanpa mengulang pencarian internet dari awal.

---

## 3. PANDUAN PENGGUNAAN CLI

Masuk ke direktori kerja:
`cd /home/ubuntu/projects/tripwire/scripts`

### A. Memulai Pipeline Baru
Jalankan perintah dengan parameter `--core` (deskripsi produk/jasa utama Anda) dan `--target` (niche target pasar spesifik):
```bash
python3 orchestrator.py --core "Aplikasi Absensi hadr.biz.id Rp10.000/staf/bulan" --target "Owner UMKM Jasa & Retail staf 3+"
```

### B. Melanjutkan Pipeline yang Terhenti (Stateful Resume)
Gunakan flag `--resume` untuk membaca status terakhir dari `state.json`:
```bash
python3 orchestrator.py --resume
```

### C. Memaksa Berjalan dari Langkah Tertentu (Debugging)
Gunakan flag `--step` (nilai 0 s.d 7) untuk menguji ulang langkah spesifik:
```bash
# Contoh: Mengulang tahap sintesis penawaran (Step 4) saja
python3 orchestrator.py --step 4
```

---

## 4. ALUR TAHAPAN PIPELINE (0 - 7)

```
[0: Intake/Intent] -> [1: Pain Research] -> [2: Persona Mapping] -> [3: Rejection Sim]
                                                                          │
[7: final-tripwire-funnel.md] <- [6: QA Loop] <- [5: Price/Ascent] <- [4: Synthesis]
```

1.  **Step 0 (Intake)**: Menerima input dan memetakan 4 kategori search queries bersih (pain, pricing, newsjacking, ascent).
2.  **Step 1 (Deep Pain)**: Menelusuri kendala hukum & operasional di Indonesia menggunakan Exa.
3.  **Step 2 (Persona)**: Memetakan 5 target persona riil dan memperkaya data dengan lookup spesifik per industri.
4.  **Step 3 (Rejection)**: Menganalisis alasan mengapa target menolak penawaran mentah biasa.
5.  **Step 4 (Synthesis)**: Merumuskan opsi tripwire per persona berdasarkan tingkat usaha:
    *   *Less Effort*: Lembar kerja Excel instan, checklist SOP PDF.
    *   *Medium Effort*: Form audit mandiri, video panduan setup pendek.
    *   *High Effort*: Mini-audit semi-manual, sesi setup langsung.
6.  **Step 5 (Recon & Ascent)**: Memetakan harga kompetitor via Tavily dan memformulasikan jembatan funnel ke Core Offer.
7.  **Step 6 (QA & Fixer)**: Menguji usulan Tripwire Utama terhadap 12 kriteria rigid. Jika gagal, dijalankan agen perbaikan hingga maksimal 2 kali percobaan.
8.  **Step 7 (Final Export)**: Menghasilkan dokumen laporan terperinci (>1500 kata) di `/home/ubuntu/projects/tripwire/final-tripwire-funnel.md`.

---

## 5. DOKUMENTASI MULTI-BAHASA (MULTI-LANGUAGE DOCUMENTATION)

### 🇬🇧 English UK (Default)
#### Project Goal & Outcome
The **Tripwire & Funnel Offer Generator** is a high-converting, challenge-driven marketing framework designed to lower **Cost Per Acquisition (CPA)** in digital advertising (performance marketing) by turning cold traffic into first-time buyers through low-friction front-end offers (Tripwires) before ascending them into high-ticket Core Offers.

#### Technical Specs for AI Agents & Scrapers
*   **Module Type:** Multi-agent pipeline orchestrator.
*   **Data Flow:** Sequential JSON states stored at `/artifacts/*.json`.
*   **Search Integration:** Context-aware retrieval with Google search fallbacks via `mcp_helper.py`.
*   **QA Checklist:** Rigid 12-point checks with dynamic correction.

---

### 🇮🇩 Bahasa Indonesia
#### Tujuan Proyek & Output
Sistem ini memecahkan masalah mahalnya **CPA (Biaya Akuisisi Prospek)** iklan berbayar dengan merumuskan penawaran Tripwire yang tak bisa ditolak oleh target pasar, mengubah status dari prospek pasif menjadi pembeli serius yang siap membeli Core Offer dan Upsell retainer Anda.

#### Spesifikasi Teknis untuk AI Agent & Scraper
*   **Model Kerja:** Eksekusi stateful berbasis state.json untuk pemulihan instan.
*   **Struktur Sintesis:** Rekomendasi dibagi menjadi 3 kategori tingkat usaha (*Less, Medium, High Effort*).
*   **Sumber Riset:** Exa (pencarian regulasi & masalah hukum) + Tavily (pencarian harga pasar & kompetitor).

---

### 🇩🇪 Deutsch (German)
#### Projektziel & Ergebnisse
Der **Tripwire & Funnel Offer Generator** ist ein datengestütztes System zur Optimierung von **Kundenakquisekosten (CAC)** im Performance-Marketing. Kalter Traffic wird durch risikoarme Einstiegsangebote (Tripwires) in aktive Käufer konvertiert, um den Übergang zum Core-Retainer-Angebot und Upsell-Stufen barrierefrei zu gestalten.

#### Technische Spezifikationen für KI-Scraper
*   **Modultyp:** Sequentieller Multi-Agenten-Pipeline-Orchestrator.
*   **Daten-Pipeline:** Artefakte werden unter `/artifacts/` im JSON-Format gespeichert.
*   **Qualitätskontrolle:** 12-Punkte-Validierung mit automatisiertem Korrekturschleifen-Fixer.
