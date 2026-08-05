import json
from base_agent import call_llm

class ExporterAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Final Exporter Agent. Buatlah dokumen markdown lengkap yang siap pakai berdasarkan seluruh rangkaian "
            "artifact yang telah tervalidasi. Dokumen Anda wajib terperinci, mendalam (panjang, minimal 1500 kata), dan secara eksplisit "
            "menyertakan bukti temuan riset lapangan (deep_research_evidence) yang ada pada setiap data persona. Jangan menyederhanakan "
            "data atau meringkas penjelasan.\n\n"
            "Wajib memuat struktur berikut secara persis:\n"
            "1. FONDASI BISNIS & CORE OFFER: Jelaskan detail layanan utama, fitur utama, dan struktur harganya.\n"
            "2. TARGET MARKET & BREAKDOWN INDUSTRI: Jelaskan 5 industri UMKM yang disasar.\n"
            "3. DETAIL 5 PERSONA: Jabarkan ke-5 persona secara lengkap dalam format terpisah (Nama, Perusahaan, Industri, Lokasi, "
            "Penghasilan, Perangkat, Cara Berpikir, Pain Points, Hidden Problem, Challenge, Keberatan Spesifik, Status Penolakan). "
            "Pada setiap persona wajib dicantumkan sub-bagian 'Rujukan Riset Lapangan (Exa/Tavily)' yang berisi ringkasan snippet "
            "dan link URL dari deep_research_evidence secara eksplisit.\n"
            "4. ALUR FUNNEL PENJUALAN PERFORMANCE MARKETING: Petakan alur visualnya (menggunakan format teks terstruktur/ASCII flow).\n"
            "5. RINCIAN FUNNEL OFFERS: Bagian ini harus dipecah sangat detail. Untuk masing-masing dari 5 persona, jabarkan daftar opsi "
            "ide Tripwire spesifik yang ditawarkan (Judul, Bentuk Output/Deliverables Nyata, Estimasi Effort [Less / Medium / High Effort], "
            "Deskripsi Cara Kerja, Harga dan Value). Setelah opsi per persona dijabarkan, tampilkan rekomendasi satu Tripwire Utama "
            "terpilih yang paling lolos validasi, diikuti dengan detail Order Bump (deskripsi, harga add-on), Core Offer (mekanisme perpindahan "
            "dari tripwire), dan Upsell Offer (layanan VIP onboarding/setup premium, harga).\n"
            "6. WORKFLOW NURTURING & SCRIPT COPY: Berikan naskah tulisan template WhatsApp/Email follow-up otomatis untuk H+0, H+1, dan H+3.\n"
            "7. CHECKLIST VALIDASI 12-POINT: Tampilkan dalam format tabel evaluasi.\n\n"
            "Output Anda adalah teks markdown lengkap."
        )

    def run(self, intake, personas, rejection, synthesis, ascent, validation, news_data):
        user_prompt = (
            f"Tolong susun penawaran tripwire final secara sangat terperinci dan detail dari seluruh artifact berikut:\n"
            f"Intake: {json.dumps(intake)}\nPersonas: {json.dumps(personas)}\nRejection: {json.dumps(rejection)}\n"
            f"Synthesis: {json.dumps(synthesis)}\nFunnel Ascent: {json.dumps(ascent)}\n"
            f"Validation: {json.dumps(validation)}\nNewsjacking Hook: {json.dumps(news_data)}"
        )
        return call_llm(self.system_prompt, user_prompt)
