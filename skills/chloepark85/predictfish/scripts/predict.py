#!/usr/bin/env python3
"""PredictFish CLI - Project success prediction using MiroFish"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from mirofish_client import MiroFishClient
from seed_generator import generate_seed, validate_project_info
from report_parser import parse_report, format_prediction_result


def cmd_status(args):
    """Check MiroFish connection status"""
    client = MiroFishClient()
    result = client.health_check()
    
    if result["status"] == "ok":
        print(f"✅ MiroFish API: {result['url']}")
        print("   Status: Connected")
        return 0
    else:
        print(f"❌ MiroFish API: {client.base_url}")
        print(f"   Error: {result['message']}")
        print("\n💡 Start MiroFish with: docker-compose up mirofish")
        return 1


def cmd_predict(args):
    """Run project success prediction"""
    project_info = {
        "name": args.name,
        "description": args.description,
        "target": args.target,
        "market": args.market
    }
    
    is_valid, error = validate_project_info(project_info)
    if not is_valid:
        print(f"❌ Validation error: {error}")
        return 1
    
    client = MiroFishClient()
    health = client.health_check()
    if health["status"] != "ok":
        print(f"❌ Cannot connect to MiroFish: {health['message']}")
        return 1
    
    print(f"🔮 PredictFish: {args.name}")
    print(f"📍 MiroFish API: {client.base_url}\n")
    
    try:
        # Step 1: Generate seed document
        print("[1/7] 🌱 Generating seed document...")
        seed = generate_seed(
            name=args.name,
            description=args.description,
            target=args.target,
            market=args.market,
            rounds=args.rounds
        )
        
        sim_requirement = (
            f"Simulate market reaction to '{args.name}': "
            f"1) Potential customer adoption rate "
            f"2) Competitive positioning "
            f"3) Success probability (0-100) "
            f"4) Key risk factors "
            f"5) Improvement suggestions"
        )
        
        if args.verbose:
            print(f"\n--- Seed Document ---\n{seed}\n--- End ---\n")
        
        # Step 2: Create project & generate ontology
        print("[2/7] 📋 Creating project & analyzing ontology...")
        project_result = client.create_project(seed, args.name, sim_requirement)
        project_data = project_result.get("data", {})
        project_id = project_data.get("project_id")
        
        if not project_id:
            print(f"❌ Failed to create project: {project_result}")
            return 1
        print(f"      Project ID: {project_id}")
        
        if args.verbose:
            ontology = project_data.get("ontology", {})
            print(f"      Entities: {len(ontology.get('entity_types', []))}")
            print(f"      Edges: {len(ontology.get('edge_types', []))}")
        
        # Step 3: Build knowledge graph
        print("[3/7] 🕸️  Building knowledge graph...")
        graph_result = client.build_graph(project_id)
        task_id = graph_result.get("data", {}).get("task_id")
        
        if task_id:
            print(f"      Task ID: {task_id}")
            print("      ⏳ Waiting for graph build...")
            client.wait_for_task(task_id, timeout=180)
            print("      ✅ Graph built")
        
        # Step 4: Generate profiles (need graph_id)
        print(f"[4/7] 👥 Generating agent profiles...")
        prep = client.prepare_simulation(project_id)
        graph_id = prep.get("graph_id")
        if not graph_id:
            print(f"❌ No graph_id found for project {project_id}")
            return 1
        print(f"      Graph ID: {graph_id}")
        profiles_result = client.generate_profiles(graph_id)
        print(f"      ✅ Profiles generated")
        
        # Step 5: Create & prepare simulation
        print(f"[5/7] 🏃 Creating simulation...")
        create_result = client.create_simulation(project_id, graph_id)
        simulation_id = create_result.get("data", {}).get("simulation_id")
        if not simulation_id:
            print(f"❌ Failed to create simulation: {create_result}")
            return 1
        print(f"      Simulation ID: {simulation_id}")
        
        print("      ⏳ Preparing simulation (LLM generating config)...")
        client.prepare_sim(simulation_id)
        client.wait_for_prepare(simulation_id, timeout=300)
        print("      ✅ Preparation complete")
        
        # Step 6: Run simulation
        print(f"[6/7] ⏳ Running swarm intelligence simulation...")
        client.start_simulation(simulation_id)
        client.wait_for_simulation(simulation_id, timeout=1800)
        print("      ✅ Simulation completed")
        
        # Step 7: Generate report
        print("[7/7] 📊 Generating prediction report...")
        report_result = client.generate_report(simulation_id, project_id)
        report_data = report_result.get("data", {})
        report_id = report_data.get("report_id")
        
        if report_id:
            report_full = client.get_report(report_id)
            parsed = parse_report(report_full)
        else:
            parsed = parse_report(report_result)
        
        print("\n" + "=" * 60)
        print(format_prediction_result(parsed))
        print("=" * 60)
        
        if args.output:
            output_path = Path(args.output)
            output_data = {
                "project": project_info,
                "prediction": parsed,
                "project_id": project_id,
                "simulation_id": simulation_id,
                "report_id": report_id
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_report(args):
    """Retrieve existing report"""
    client = MiroFishClient()
    try:
        print(f"📊 Fetching report: {args.report_id}")
        report_data = client.get_report(args.report_id)
        parsed = parse_report(report_data)
        print("\n" + "=" * 60)
        print(format_prediction_result(parsed))
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="PredictFish - Predict project success using MiroFish swarm intelligence"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    subparsers.add_parser("status", help="Check MiroFish API status")
    
    predict_parser = subparsers.add_parser("predict", help="Run success prediction")
    predict_parser.add_argument("--name", required=True, help="Project name")
    predict_parser.add_argument("--description", required=True, help="Project description")
    predict_parser.add_argument("--target", default="일반 사용자", help="Target customer segment")
    predict_parser.add_argument("--market", default="미정의 시장", help="Market info")
    predict_parser.add_argument("--rounds", type=int, default=20, help="Simulation rounds")
    predict_parser.add_argument("--output", "-o", help="Save results to JSON file")
    predict_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    report_parser = subparsers.add_parser("report", help="Retrieve existing report")
    report_parser.add_argument("report_id", help="Report ID to retrieve")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {"status": cmd_status, "predict": cmd_predict, "report": cmd_report}
    return commands.get(args.command, lambda a: 1)(args)


if __name__ == "__main__":
    sys.exit(main())
