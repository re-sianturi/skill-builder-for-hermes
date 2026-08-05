import json
from base_agent import call_llm, clean_json_string

class SynthesisAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Friction Minimizer Agent. Tugas Anda adalah merumuskan rekomendasi Tripwire spesifik untuk masing-masing dari "
            "5 persona yang telah dipetakan, berdasarkan pain points, hidden problems, dan tantangan mereka. Tripwire harus berupa produk "
            "berisiko sangat rendah, bernilai tinggi, murah (di bawah Rp 100.000) untuk memicu pembelian pertama, BUKAN paket layanan bulanan utama. "
            "Untuk SETIAP persona, berikan minimal 1-2 opsi ide Tripwire dengan mencantumkan: Judul, Bentuk Output (deliverables nyata), Tingkat Effort "
            "(Less Effort / Medium Effort / High Effort), dan penjelasan bagaimana tripwire tersebut memicu kesadaran akan hidden problem mereka. "
            "Output harus berupa objek JSON valid dengan key: 'specs' dan 'recommendations' (list of dict, di mana tiap dict merepresentasikan "
            "rekomendasi tripwire dan memiliki key: 'persona_name', 'title', 'deliverables' [array of string], 'effort_level', 'estimated_price', "
            "'hidden_problem_trigger'). Jangan menyertakan penjelasan lain atau format markdown codeblocks."
        )

    def run(self, personas, rejection_patterns, core_offer):
        user_prompt = f"Data Persona: {json.dumps(personas)}\nPola Penolakan: {json.dumps(rejection_patterns)}\nCore Offer: {core_offer}"
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))
