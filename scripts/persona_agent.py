import json
from base_agent import call_llm, clean_json_string

class PersonaAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Persona Mapping Agent. Tugas Anda adalah membuat MINIMAL 5 target persona terperinci sesuai B2B/SME track "
            "untuk industri UMKM spesifik (contoh: 1. Klinik Estetika/Pratama, 2. Salon Eyelash & Beauty, 3. Resto & Cafe, 4. Barbershop Premium, "
            "5. Toko Retail/Batik). Setiap persona WAJIB memiliki detail: profile (nama, perusahaan, industri, lokasi, penghasilan, perangkat), "
            "cara berpikir, pain points (keluhan operasional), HIDDEN PROBLEM (masalah tersembunyi seperti kebocoran payroll/kecurangan tim), "
            "challenge (pertanyaan evaluasi), keberatan spesifik, dan status ('❌ Menolak versi awal'). Output WAJIB berupa objek JSON valid: "
            "{\"personas\": [{\"name\": \"...\", \"company\": \"...\", \"industry\": \"...\", \"location\": \"...\", \"income\": \"...\", "
            "\"device\": \"...\", \"thinking\": \"...\", \"pain_points\": [], \"hidden_problem\": \"...\", \"challenge\": \"...\", "
            "\"objection\": \"...\", \"status\": \"❌ Menolak versi awal\"}]}. Jangan gunakan markdown codeblocks."
        )

    def run(self, core_offer, target_market, search_data):
        user_prompt = (
            f"Buatkan MINIMAL 5 persona terperinci untuk 5 industri UMKM berbeda yang relevan dengan:\n"
            f"Target Market: {target_market}\nCore Offer: {core_offer}\nData Pasar Lapangan: {json.dumps(search_data)}\n\n"
            f"Pastikan Anda memanfaatkan data keluhan operasional riil dari lapangan untuk mengekstrak pain points dan hidden problem."
        )
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))
