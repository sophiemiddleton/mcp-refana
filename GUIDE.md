#!/usr/bin/env python3
"""
MCP-Refana Server: Comprehensive Guide

This tool demonstrates how to use the mcp-refana MCP server for agentic
refana analysis workflows with real dataset discovery.
"""

def print_guide():
    guide = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   MCP-REFANA: Comprehensive Guide                          ║
╚════════════════════════════════════════════════════════════════════════════╝

## Overview

The mcp-refana server provides 10 Model Context Protocol (MCP) tools that enable
agents to discover real Mu2e datasets and perform analysis workflows without
manual file management.

Key Features:
  • Real dataset discovery via SAM definitions
  • Automatic data preparation for analysis
  • Cut-and-count analysis workflow
  • ML-based event selection
  • Physics sensitivity calculations
  • Dataset summaries and comparisons

────────────────────────────────────────────────────────────────────────────

## MCP Tools (10 Total)

### Data Discovery Tools (3)

1. list_available_datasets()
   Purpose: Discover all available SAM dataset definitions
   Params: None
   Returns: List of dataset definitions with descriptions
   
   Example:
   ├─ ensembleMDS3c: MDS3c Reference Ensemble
   ├─ ensembleMDS3cMix1BB: MDS3c with specific background mix
   ├─ oot_ensembleMDS3c: Out-of-time overlays
   └─ dio_ensembleMDS3c: Decay-in-orbit background

2. get_dataset_info(defname, location)
   Purpose: Get metadata about a specific dataset
   Params:
     • defname: SAM definition name (e.g., 'ensembleMDS3c')
     • location: File location ('disk', 'tape', 'scratch', 'nersc')
   Returns: File count, size estimate, availability status
   
   Example Response:
     {
       "file_count": 450,
       "estimated_size_gb": 225.0,
       "location": "disk",
       "ready_for_analysis": true
     }

3. create_dataset_filelist(defname, location, max_files, output_path)
   Purpose: Generate a filelist for analysis
   Params:
     • defname: SAM definition name
     • location: File location
     • max_files: (optional) Limit to first N files
     • output_path: (optional) Custom output path
   Returns: Path to generated filelist
   
   Example Response:
     {
       "filelist_path": "/tmp/filelist_ensembleMDS3c_xyz.txt",
       "total_files": 100,
       "ready_for_refana": true
     }

### Analysis Tools (7)

4. healthcheck()
   Purpose: Check server status and readiness
   Params: None
   Returns: Server status
   
5. count_signal_background(mom_list, time_list, mc_list, mom_range, time_range, sign)
   Purpose: Extract signal/background events in kinematic region
   Params:
     • mom_list, time_list, mc_list: Event data
     • mom_range, time_range: Selection windows [min, max]
     • sign: 'minus' (electron) or 'plus' (positron)
   Returns: Signal/background counts and fractions
   
6. analyze_cuts(cut_definitions, sign)
   Purpose: Configure analysis cuts
   Params:
     • cut_definitions: Dict of cut criteria
     • sign: 'minus' or 'plus'
   Returns: Analyzer status
   
7. compute_sensitivity(s_expected, b_expected, b_sys_uncertainty, exposure, efficiency)
   Purpose: Compute physics sensitivity metrics
   Params:
     • s_expected: Expected signal events
     • b_expected: Expected background events
     • b_sys_uncertainty: Background systematic uncertainty
     • exposure, efficiency: (optional) For normalization
   Returns: Asimov significance, CLs limits, Feldman-Cousins intervals
   
   Example Response:
     {
       "asimov_z": 3.2,
       "discovery_ready": true,
       "cls_upper_limit_95cl": 125.0,
       "feldman_cousins_90cl": [28.0, 58.0]
     }
   
8. initialize_ml_selector()
   Purpose: Set up BDT-based event selector
   Params: None
   Returns: Available features and labels
   
   Available Features:
     • reco_momentum
     • reco_time
     • t0_error
     • n_active_hits
     • n_st_hits
     • n_opa_hits
     • closest_crv_distance
   
9. get_cut_efficiency(cuts_applied, n_total, n_surviving)
   Purpose: Calculate efficiency metrics for cuts
   Params:
     • cuts_applied: Dict describing cuts
     • n_total: Events before cuts
     • n_surviving: Events after cuts
   Returns: Efficiency and rejection power
   
10. summarize_analysis(dataset_name, sign, n_events_processed, signal_count, 
                       background_count, ml_score_mean)
    Purpose: Generate analysis summary
    Params: Dataset info and event counts
    Returns: Summary with statistics

────────────────────────────────────────────────────────────────────────────

## Getting Started

### 1. Activate Environment & Start Server

  # Activate Mu2e analysis environment
  source /exp/mu2e/app/users/sophie/agentic-examples/hep-env/bin/activate
  
  # Start mcp-refana server
  cd /exp/mu2e/app/users/sophie/agentic-examples/mcp-refana
  mcp-refana-server --transport stdio

### 2. Example: Discover & Analyze a Dataset

  # Step 1: List available datasets
  $ tool_call(list_available_datasets)
  → Returns: [ensembleMDS3c, ensembleMDS3cMix1BB, oot_ensembleMDS3c, ...]
  
  # Step 2: Get dataset info
  $ tool_call(get_dataset_info, defname='ensembleMDS3c', location='disk')
  → Returns: 450 files, 225 GB, ready for analysis
  
  # Step 3: Create filelist
  $ tool_call(create_dataset_filelist, defname='ensembleMDS3c', 
              location='disk', max_files=100)
  → Returns: /tmp/filelist_ensembleMDS3c_xyz.txt
  
  # Step 4: Analyze with refana
  $ python process.py --file /tmp/filelist_ensembleMDS3c_xyz.txt
  
  # Step 5: Compute sensitivity
  $ tool_call(compute_sensitivity, s_expected=42, b_expected=58, 
              b_sys_uncertainty=5.8)
  → Returns: Z=3.2σ (discovery!), 95% CL limit: 125 events

────────────────────────────────────────────────────────────────────────────

## Integration with HEP-Multiagent

To use mcp-refana with the HEP-multiagent framework:

### 1. Configure MCP Server Registration

Edit HEP-multiagent config:

  # In HEP-multiagent/src/hep_multiagent/config.py
  MCP_SERVERS = {
      "refana": {
          "command": ["bash", "-c",
              "source /exp/mu2e/app/users/sophie/agentic-examples/hep-env/bin/activate && "
              "cd /exp/mu2e/app/users/sophie/agentic-examples/mcp-refana && "
              "mcp-refana-server --transport stdio"
          ],
          "description": "Mu2e refana analysis with dataset discovery",
      }
  }

### 2. Create Refana Worker

  # In HEP-multiagent/src/hep_multiagent/workers/refana.py
  
  from hep_multiagent.agent import Agent
  
  class RefanaWorker(Agent):
      """Worker for refana dataset analysis"""
      
      tools = ["list_available_datasets", "get_dataset_info", 
               "create_dataset_filelist", "count_signal_background",
               "compute_sensitivity"]
      
      async def analyze_dataset(self, defname: str, queries: list[str]):
          # 1. Discover dataset
          # 2. Prepare filelist
          # 3. Run analysis
          # 4. Compute sensitivity
          # 5. Return results

### 3. Use in Workflows

  # Submit agentic workflow
  $ python agent.py --query "Using ensembleMDS3c, find the signal region significance"
  
  The agent will:
    1. Call list_available_datasets() → confirm dataset exists
    2. Call get_dataset_info() → verify dataset properties
    3. Call create_dataset_filelist() → prepare data
    4. Run refana analysis on prepared filelist
    5. Call compute_sensitivity() → calculate Z-score
    6. Return results and plots

────────────────────────────────────────────────────────────────────────────

## Testing

Run included test scripts:

  # Test tool registration
  $ python test_server.py
  
  # Test dataset discovery
  $ python test_dataset_discovery.py
  
  # Show end-to-end workflow
  $ python workflow_example.py

────────────────────────────────────────────────────────────────────────────

## Supported Natural Language Queries

With agents using mcp-refana:

✓ "What datasets are available?"
✓ "How many files in ensembleMDS3c?"
✓ "Using ensembleMDS3c, analyze the signal region"
✓ "What's the significance of the MDS3c analysis?"
✓ "Compare sensitivities across MDS3c datasets"
✓ "Train ML selector on ensembleMDS3cMix1BB"
✓ "Find the optimal momentum/time cut for MDS3c"
✓ "Generate plots for the cosmic background study"

────────────────────────────────────────────────────────────────────────────

## Architecture

  User Query
       ↓
  HEP-Multiagent
       ↓
  Refana Worker Agent
       ↓
  ┌─────────────────────────────────────┐
  │  MCP-Refana Server (10 tools)       │
  │  ┌─────────────────────────────┐    │
  │  │ Data Discovery (3)          │    │
  │  │ • list_available_datasets   │    │
  │  │ • get_dataset_info          │    │
  │  │ • create_dataset_filelist   │    │
  │  ├─────────────────────────────┤    │
  │  │ Analysis Tools (7)          │    │
  │  │ • count_signal_background   │    │
  │  │ • analyze_cuts              │    │
  │  │ • compute_sensitivity       │    │
  │  │ • initialize_ml_selector    │    │
  │  │ • get_cut_efficiency        │    │
  │  │ • summarize_analysis        │    │
  │  │ • healthcheck               │    │
  │  └─────────────────────────────┘    │
  └─────────────────────────────────────┘
       ↓
  Real Refana Code
  • Count.py (event counting)
  • Analyze.py (cut application)
  • MLSelect.py (BDT selection)
  • SensitivityAnalyzer.py (physics metrics)
       ↓
  SAM Dataset Access
  (Real Mu2e data via SAM definitions)

────────────────────────────────────────────────────────────────────────────

## Next Steps

1. Test server with included test scripts
2. Configure HEP-multiagent integration
3. Create refana worker agent
4. Test with real SAM datasets
5. Deploy for production use

For questions or issues, refer to:
  • workflow_example.py - Complete workflow demonstration
  • README.md - Server documentation
  • run_reference_analysis.py - Underlying refana infrastructure

════════════════════════════════════════════════════════════════════════════
"""
    print(guide)


if __name__ == "__main__":
    print_guide()
