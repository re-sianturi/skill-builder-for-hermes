import json
from base_agent import call_llm, clean_json_string

class IntakeAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Search Intent Extractor & Intake Agent. Tugas Anda adalah membedah Core Offer dan Target Market "
            "menggunakan kerangka 5W 1H (What, Who, Why, Where, When, How) untuk menghasilkan keyword pencarian yang bersih, "
            "relevan, dan tajam (maksimal 3-4 kata per query). Klasifikasikan tipe bisnis menjadi 'B2B' atau 'B2C' untuk "
            "menyesuaikan gaya penulisan dan query. Output WAJIB berupa objek JSON valid dengan key: 'classification', "
            "'analysis_5w1h' (dict dengan key: 'what', 'who', 'why', 'where', 'when', 'how'), 'search_queries' (dict dengan key: "
            "'deep_pain' [list berisi 3 query spesifik], 'pricing_recon' [list berisi 2 query], 'newsjacking' [list berisi 2 query], "
            "'funnel_ascent' [list berisi 2 query]), dan 'ready' (bool). Jangan gunakan markdown codeblocks atau penjelasan tambahan."
        )

    def run(self, core_offer, target_market):
        user_prompt = f"Bedah input berikut:\nCore Offer: {core_offer}\nTarget Market: {target_market}"
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))
