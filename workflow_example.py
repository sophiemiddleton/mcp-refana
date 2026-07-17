#!/usr/bin/env python3
"""
Example: End-to-end workflow using mcp-refana dataset discovery + analysis tools.

This demonstrates how a user query like:
  "Using dataset ensembleMDS3c, analyze the signal region"
  
Gets handled by the MCP server in coordinated steps.
"""

import sys
from pathlib import Path

# Add mcp-refana to path
refana_path = Path(__file__).parent / "src"
sys.path.insert(0, str(refana_path))

# Mock imports
sys.modules['pyutils'] = __import__('types').ModuleType('pyutils')
sys.modules['pyutils.pymcutil'] = __import__('types').ModuleType('pymcutil')
sys.modules['pyutils.pylogger'] = __import__('types').ModuleType('pylogger')
sys.modules['pyutils.pycut'] = __import__('types').ModuleType('pycut')
sys.modules['pyutils.pyvector'] = __import__('types').ModuleType('pyvector')
sys.modules['pyutils.pyselect'] = __import__('types').ModuleType('pyselect')
sys.modules['pyutils.pyplot'] = __import__('types').ModuleType('pyplot')
sys.modules['pyutils.pyprint'] = __import__('types').ModuleType('pyprint')
sys.modules['pyutils.pyprocess'] = __import__('types').ModuleType('pyprocess')


def print_step(step_num, title):
    """Print step header."""
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*70}")


def print_agent_call(tool_name, params):
    """Print agent tool call."""
    print(f"\n  → Agent calls: {tool_name}()")
    for key, value in params.items():
        print(f"    - {key}: {value}")


def print_tool_response(response):
    """Print tool response."""
    print(f"\n  ← Tool returns:")
    for key, value in response.items():
        if isinstance(value, dict):
            print(f"    {key}:")
            for k, v in value.items():
                print(f"      - {k}: {v}")
        elif isinstance(value, list) and len(value) > 2:
            print(f"    {key}: [{value[0]}, {value[1]}, ...]  ({len(value)} items)")
        else:
            print(f"    {key}: {value}")


def main():
    """Demonstrate end-to-end workflow."""
    
    print("="*70)
    print("MCP-Refana: End-to-End Workflow Example")
    print("="*70)
    
    print("""
USER QUERY:
  "Using dataset ensembleMDS3c, analyze the signal region"

MCP REFANA SERVER ORCHESTRATES:
""")
    
    # Step 1: Discover available datasets
    print_step(1, "Discover Available Datasets")
    print_agent_call("list_available_datasets", {})
    print_tool_response({
        "status": "success",
        "datasets": {
            "ensembleMDS3c": "MDS3c Reference Ensemble",
            "ensembleMDS3cMix1BB": "MDS3c with 1% BB background",
            "oot_ensembleMDS3c": "Out-of-time overlays",
            "dio_ensembleMDS3c": "Decay-in-orbit background",
        },
        "total_definitions": 4,
    })
    
    print("\n  ✓ Agent confirms 'ensembleMDS3c' exists")
    
    # Step 2: Get dataset information
    print_step(2, "Get Dataset Information")
    print_agent_call("get_dataset_info", {
        "defname": "ensembleMDS3c",
        "location": "disk",
    })
    print_tool_response({
        "status": "success",
        "definition": "ensembleMDS3c",
        "location": "disk",
        "file_count": 450,
        "estimated_size_gb": 225.0,
        "ready_for_analysis": True,
    })
    
    print("\n  ✓ Dataset has 450 files (225 GB), ready for analysis")
    
    # Step 3: Create analysis filelist
    print_step(3, "Prepare Data for Analysis")
    print_agent_call("create_dataset_filelist", {
        "defname": "ensembleMDS3c",
        "location": "disk",
        "max_files": 100,  # Use subset for faster analysis
    })
    print_tool_response({
        "status": "success",
        "definition": "ensembleMDS3c",
        "filelist_path": "/tmp/filelist_ensembleMDS3c_abc123.txt",
        "total_files": 100,
        "ready_for_refana": True,
        "next_step": "Use with refana: python process.py --file /tmp/filelist_ensembleMDS3c_abc123.txt",
    })
    
    print("\n  ✓ Created filelist with 100 files at /tmp/filelist_ensembleMDS3c_abc123.txt")
    
    # Step 4: Configure analysis cuts
    print_step(4, "Configure Analysis Cuts")
    print_agent_call("analyze_cuts", {
        "cut_definitions": {
            "momentum_min": 103.0,
            "momentum_max": 105.0,
            "time_min": 400.0,
            "time_max": 600.0,
        },
        "sign": "minus",
    })
    print_tool_response({
        "status": "success",
        "analyzer_initialized": True,
        "sign": "minus",
        "message": "Analyzer ready for cut application",
    })
    
    print("\n  ✓ Analysis cuts configured for signal region")
    
    # Step 5: Count signal and background
    print_step(5, "Perform Event Counting")
    print_agent_call("count_signal_background", {
        "mom_list": "[103.5, 104.2, 104.8, ...]",
        "time_list": "[450, 520, 580, ...]",
        "mc_list": "[168, 168, 0, ...]",
        "mom_range": [103.0, 105.0],
        "time_range": [400.0, 600.0],
        "sign": "minus",
    })
    print_tool_response({
        "status": "success",
        "signal_count": 42,
        "background_count": 58,
        "total_count": 100,
        "signal_fraction": 0.42,
        "kinematic_window": {
            "momentum_range": [103.0, 105.0],
            "time_range": [400.0, 600.0],
        },
    })
    
    print("\n  ✓ Signal region: 42 signal, 58 background events")
    
    # Step 6: Compute sensitivity
    print_step(6, "Compute Physics Sensitivity")
    print_agent_call("compute_sensitivity", {
        "s_expected": 42,
        "b_expected": 58,
        "b_sys_uncertainty": 5.8,  # 10% systematics
    })
    print_tool_response({
        "status": "success",
        "significance": {
            "asimov_z": 3.2,
            "discovery_ready": True,
        },
        "limits": {
            "cls_upper_limit_95cl": 125.0,
        },
        "confidence_intervals": {
            "feldman_cousins_lower_90cl": 28.0,
            "feldman_cousins_upper_90cl": 58.0,
        },
    })
    
    print("\n  ✓ Sensitivity: Z=3.2σ (discovery-ready)")
    print("    95% CL limit: 125 signal events")
    
    # Step 7: Generate summary
    print_step(7, "Generate Analysis Summary")
    print_agent_call("summarize_analysis", {
        "dataset_name": "ensembleMDS3c (disk, 100 files)",
        "sign": "minus",
        "n_events_processed": 500000,
        "signal_count": 42,
        "background_count": 58,
        "ml_score_mean": 0.72,
    })
    print_tool_response({
        "status": "success",
        "dataset": "ensembleMDS3c",
        "event_counts": {
            "processed": 500000,
            "signal": 42,
            "background": 58,
            "signal_fraction": 0.42,
        },
        "ml_metrics": {
            "bdt_score_mean": 0.72,
        },
    })
    
    print("\n  ✓ Analysis complete")
    
    # Final summary
    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    
    print("""
✓ Dataset discovered: ensembleMDS3c
✓ Data prepared: 100 files, 500K events
✓ Analysis performed: Signal region selected
✓ Results:
    • Signal events: 42
    • Background: 58
    • Significance: 3.2σ (discovery)
    • 95% CLs limit: 125 events

KEY BENEFITS:
  1. User asks natural language query
  2. Agent coordinates multiple MCP tools
  3. Dataset discovery is automatic
  4. Data preparation is handled
  5. Analysis results are summarized
  6. Workflow is reproducible

ENABLED QUERIES:
  • "Using ensembleMDS3c, plot momentum distribution"
  • "What's the sensitivity of oot_ensembleMDS3c?"
  • "Compare signal regions across MDS3c datasets"
  • "Train ML selector on ensembleMDS3cMix1BB"
""")
    
    print("="*70)
    print("Ready for deployment with HEP-Multiagent!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
