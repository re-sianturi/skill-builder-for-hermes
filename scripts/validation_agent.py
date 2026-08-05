import json
from base_agent import call_llm, clean_json_string

class QAValidationAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah QA Loop & Fixer Agent. Anda menguji usulan tripwire terpilih terhadap 12-Point Guideline. "
            "Gunakan data harga kompetitor yang disediakan untuk memvalidasi kelayakan harga dan value tripwire. "
            "Berikan evaluasi bertipe boolean (pass/fail) untuk tiap poin. Jika ada poin yang gagal (fail), berikan rekomendasi perbaikan (Fixer). "
            "Output harus berupa objek JSON valid dengan key: 'checklist' (dict of bool & notes), 'overall_pass' (bool), 'fixes' (list). "
            "Jangan menyertakan penjelasan lain atau format markdown codeblocks."
        )

    def run(self, tripwire, core_offer, target_market, price_data):
        user_prompt = f"Tripwire Usulan: {json.dumps(tripwire)}\nCore Offer: {core_offer}\nTarget: {target_market}\nData Kompetitor & Harga Pasar: {json.dumps(price_data)}"
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))

    def fix(self, tripwire, validation_result):
        fixer_prompt = (
            f"Tripwire Proposal: {json.dumps(tripwire)}\nValidation Result: {json.dumps(validation_result)}\n"
            f"Fix the tripwire to address the fails. Output WAJIB JSON valid dengan skema tripwire yang sama. "
            f"Pastikan harga tripwire murah dan merupakan tawaran entry-level berisiko rendah (di bawah Rp 500.000)."
        )
        res = call_llm(
            "Anda adalah Fixer Agent. Perbaiki tripwire proposal berdasarkan kegagalan checklist QA agar lolos 12-point. "
            "Format output Anda WAJIB JSON valid dengan skema tripwire yang sama. Jangan gunakan markdown codeblocks atau kata pengantar, "
            "langsung keluarkan string mentah JSON valid.", 
            fixer_prompt
        )
        return json.loads(clean_json_string(res))
