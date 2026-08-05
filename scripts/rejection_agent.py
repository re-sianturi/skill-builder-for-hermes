import json
from base_agent import call_llm, clean_json_string

class RejectionAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Rejection Simulator Agent. Simulasikan penolakan (Status: ❌ Menolak versi awal) dari setiap persona "
            "terhadap ide Tripwire kasar biasa (seperti e-book panjang atau audit rumit). Temukan pola keberatan mereka (misal: waktu, "
            "biaya, birokrasi, operasional terganggu). Output harus berupa objek JSON valid dengan key: 'penolakan' (list of dict) "
            "dan 'pola_penolakan' (dict of counts). Jangan menyertakan penjelasan lain atau format markdown codeblocks."
        )

    def run(self, core_offer, personas):
        user_prompt = f"Core Offer: {core_offer}\nPersonas: {json.dumps(personas)}"
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))
