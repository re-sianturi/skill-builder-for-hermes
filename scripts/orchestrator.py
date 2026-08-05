#!/usr/bin/env python3
import os
import sys
import json
import argparse
from mcp_helper import deep_pain_research, market_price_research

# Import modular agents
from intake_agent import IntakeAgent
from persona_agent import PersonaAgent
from rejection_agent import RejectionAgent
from synthesis_agent import SynthesisAgent
from validation_agent import QAValidationAgent
from funnel_ascent_agent import FunnelAscentAgent
from exporter_agent import ExporterAgent

ARTIFACTS_DIR = "/home/ubuntu/projects/tripwire/artifacts"
STATE_FILE = "/home/ubuntu/projects/tripwire/artifacts/state.json"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"current_step": 0, "core_offer": "", "target_market": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def save_artifact(name, data):
    path = os.path.join(ARTIFACTS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[Artifact] Saved {name}.json")
    return data

def read_artifact(name):
    path = os.path.join(ARTIFACTS_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def orchestrate(core_offer, target_market, resume=False, force_step=None):
    state = load_state()
    
    if resume and state.get("core_offer"):
        core_offer = state["core_offer"]
        target_market = state["target_market"]
        print(f"[Orchestrator] Resuming pipeline for: '{core_offer}'")
    else:
        state = {
            "current_step": 0,
            "core_offer": core_offer,
            "target_market": target_market
        }
        save_state(state)
        print(f"[Orchestrator] Starting fresh pipeline for: '{core_offer}'")

    steps = {
        0: "Intake & Search Query Generation",
        1: "Deep Pain Market Research",
        2: "Persona Mapping & Enriched Search",
        3: "Rejection Simulator",
        4: "Friction-Minimized Synthesis",
        5: "Competitor Price Recon & Ascent Funnel",
        6: "QA Loop Validation & Fixer",
        7: "Final Export Document"
    }

    start_step = force_step if force_step is not None else state["current_step"]

    # Step 0: Intake and Intent Parsing
    if start_step <= 0:
        print("\n=== STEP 0: INTAKE & INTENT GENERATION ===")
        intake_agent = IntakeAgent()
        intake_data = intake_agent.run(core_offer, target_market)
        save_artifact("0_intents", intake_data)
        save_artifact("1_intake", intake_data)
        
        if not intake_data.get("ready", False):
            print("[Error] Intake verification failed. Stop.")
            return
            
        state["current_step"] = 1
        save_state(state)

    # Step 1: Deep Pain Research
    if start_step <= 1:
        print("\n=== STEP 1: DEEP PAIN MARKET RESEARCH ===")
        intents = read_artifact("0_intents")
        pain_results = []
        for query in intents.get("search_queries", {}).get("deep_pain", []):
            print(f"Searching: '{query}'")
            res = deep_pain_research(query, limit=3)
            if res and res.get("results"):
                pain_results.extend(res["results"])
        if not pain_results:
            fallback = f"regulasi kendala operasional masalah hukum {core_offer} {target_market} Indonesia"
            res = deep_pain_research(fallback, limit=5)
            pain_results = res.get("results", []) if res else []
            
        save_artifact("1_5_market_research", {"source": "multi_query_search", "results": pain_results})
        state["current_step"] = 2
        save_state(state)

    # Step 2: Persona Mapping & Deep Research Enriched
    if start_step <= 2:
        print("\n=== STEP 2: PERSONA MAPPING & ENRICHED SEARCH ===")
        pain_results = read_artifact("1_5_market_research")["results"]
        persona_agent = PersonaAgent()
        personas_data = persona_agent.run(core_offer, target_market, pain_results)
        
        # Enriched persona-specific lookup
        enriched_personas = []
        for persona in personas_data.get("personas", []):
            p_name = persona.get("name")
            p_industry = persona.get("industry")
            p_pain = ", ".join(persona.get("pain_points", []))
            p_hidden = persona.get("hidden_problem", "")
            
            query_pain = f"masalah kecurangan operasional {p_industry} {p_pain} Indonesia"
            query_hidden = f"kebocoran biaya payroll {p_industry} {p_hidden}"
            
            print(f"Deep researching persona '{p_name}' ({p_industry})...")
            p_pain_res = deep_pain_research(query_pain, limit=2)
            p_hidden_res = market_price_research(query_hidden, limit=2)
            
            persona["deep_research_evidence"] = {
                "pain_evidence": p_pain_res.get("results", []) if p_pain_res else [],
                "hidden_evidence": p_hidden_res.get("results", []) if p_hidden_res else []
            }
            enriched_personas.append(persona)
            
        personas_data["personas"] = enriched_personas
        save_artifact("2_personas", personas_data)
        state["current_step"] = 3
        save_state(state)

    # Step 3: Rejection Simulation
    if start_step <= 3:
        print("\n=== STEP 3: REJECTION SIMULATOR ===")
        personas_data = read_artifact("2_personas")
        rejection_agent = RejectionAgent()
        rejection_data = rejection_agent.run(core_offer, personas_data)
        save_artifact("3_rejection", rejection_data)
        state["current_step"] = 4
        save_state(state)

    # Step 4: Friction-Minimized Synthesis
    if start_step <= 4:
        print("\n=== STEP 4: FRICTION-MINIMIZED SYNTHESIS ===")
        personas_data = read_artifact("2_personas")
        rejection_data = read_artifact("3_rejection")
        synthesis_agent = SynthesisAgent()
        synthesis_data = synthesis_agent.run(personas_data, rejection_data, core_offer)
        save_artifact("4_synthesis", synthesis_data)
        state["current_step"] = 5
        save_state(state)

    # Step 5: Competitor Pricing & Funnel Ascent
    if start_step <= 5:
        print("\n=== STEP 5: PRICING & FUNNEL ASCENT ===")
        intents = read_artifact("0_intents")
        synthesis_data = read_artifact("4_synthesis")
        
        # 5.1 Competitor Pricing Recon
        price_results = []
        for query in intents.get("search_queries", {}).get("pricing_recon", []):
            print(f"Searching price: '{query}'")
            res = market_price_research(query, limit=3)
            if res and res.get("results"):
                price_results.extend(res["results"])
        if not price_results:
            fallback = f"biaya paket harga {core_offer} Indonesia"
            res = market_price_research(fallback, limit=5)
            price_results = res.get("results", []) if res else []
        save_artifact("4_5_price_research", {"source": "multi_query_price", "results": price_results})

        # 5.2 Funnel Ascent
        ascent_results = []
        for query in intents.get("search_queries", {}).get("funnel_ascent", []):
            print(f"Searching funnel: '{query}'")
            res = deep_pain_research(query, limit=3)
            if res and res.get("results"):
                ascent_results.extend(res["results"])
        
        ascent_agent = FunnelAscentAgent()
        ascent_data = ascent_agent.run(synthesis_data, core_offer, ascent_results)
        save_artifact("4_7_funnel_ascent", ascent_data)

        # 5.3 Newsjacking Hook Recon
        news_results = []
        for query in intents.get("search_queries", {}).get("newsjacking", []):
            print(f"Searching news: '{query}'")
            res = market_price_research(query, limit=2)
            if res and res.get("results"):
                news_results.extend(res["results"])
        save_artifact("4_8_news_recon", {"source": "multi_query_news", "results": news_results})

        state["current_step"] = 6
        save_state(state)

    # Step 6: QA Validation Loop
    if start_step <= 6:
        print("\n=== STEP 6: QA LOOP VALIDATION & FIXER ===")
        synthesis_data = read_artifact("4_synthesis")
        price_results = read_artifact("4_5_price_research")["results"]
        
        recs = synthesis_data.get("recommendations", [])
        tripwire_proposal = recs[0] if recs else synthesis_data
        
        validation_agent = QAValidationAgent()
        validation_data = validation_agent.run(tripwire_proposal, core_offer, target_market, price_results)
        save_artifact("5_validation", validation_data)

        attempts = 0
        while not validation_data.get("overall_pass", False) and attempts < 2:
            attempts += 1
            print(f"[QA] Failed. Triggering Fixer Attempt {attempts}...")
            tripwire_proposal = validation_agent.fix(tripwire_proposal, validation_data)
            validation_data = validation_agent.run(tripwire_proposal, core_offer, target_market, price_results)
            save_artifact(f"5_validation_retry_{attempts}", validation_data)

        save_artifact("5_validated_tripwire", tripwire_proposal)
        state["current_step"] = 7
        save_state(state)

    # Step 7: Final Export
    if start_step <= 7:
        print("\n=== STEP 7: FINAL EXPORT DOCUMENT ===")
        intake_data = read_artifact("1_intake")
        personas_data = read_artifact("2_personas")
        rejection_data = read_artifact("3_rejection")
        synthesis_data = read_artifact("4_synthesis")
        ascent_data = read_artifact("4_7_funnel_ascent")
        validation_data = read_artifact("5_validation")
        news_data = read_artifact("4_8_news_recon")["results"]

        exporter_agent = ExporterAgent()
        final_markdown = exporter_agent.run(
            intake_data, personas_data, rejection_data,
            synthesis_data, ascent_data, validation_data, news_data
        )
        
        output_path = "/home/ubuntu/projects/tripwire/final-tripwire-funnel.md"
        with open(output_path, "w") as f:
            f.write(final_markdown)
        print(f"\n[Done] Pipeline finished! Output path: {output_path}")
        
        # Reset state upon completion
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="World-Class Tripwire & Funnel Orchestrator")
    parser.add_argument("--core", help="Core Offer description")
    parser.add_argument("--target", help="Target market niche")
    parser.add_argument("--resume", action="store_true", help="Resume pipeline from saved state")
    parser.add_argument("--step", type=int, default=None, help="Force execute starting from specific step (0-7)")
    args = parser.parse_args()

    if not args.resume and not (args.core and args.target):
        parser.error("Parameters --core and --target are required unless running with --resume")

    orchestrate(args.core, args.target, resume=args.resume, force_step=args.step)
