import json
from base_agent import call_llm, clean_json_string

class FunnelAscentAgent:
    def __init__(self):
        self.system_prompt = (
            "Anda adalah Funnel Ascent Architect. Tugas Anda adalah memetakan jembatan logis dari Tripwire ke Core Offer "
            "hingga Upsell/Order Bump berdasarkan riset pola funnel industri (Exa). Output harus berupa objek JSON valid "
            "dengan key: 'order_bump', 'core_offer_transition', 'upsell_offer'. Format JSON valid tanpa markdown codeblocks."
        )

    def run(self, tripwire, core_offer, ascent_data):
        user_prompt = f"Tripwire Valid: {json.dumps(tripwire)}\nCore Offer: {core_offer}\nData Riset Funnel Exa: {json.dumps(ascent_data)}"
        res = call_llm(self.system_prompt, user_prompt)
        return json.loads(clean_json_string(res))
