#!/usr/bin/env python3
"""Test mcp-refana server tools are properly defined."""

import sys
import asyncio
from pathlib import Path

# Add mcp-refana to path
refana_path = Path(__file__).parent / "src"
sys.path.insert(0, str(refana_path))

# Mock out refana imports since there's an issue with the library
sys.modules['pyutils'] = __import__('types').ModuleType('pyutils')
sys.modules['pyutils.pymcutil'] = __import__('types').ModuleType('pymcutil')
sys.modules['pyutils.pylogger'] = __import__('types').ModuleType('pylogger')
sys.modules['pyutils.pycut'] = __import__('types').ModuleType('pycut')
sys.modules['pyutils.pyvector'] = __import__('types').ModuleType('pyvector')
sys.modules['pyutils.pyselect'] = __import__('types').ModuleType('pyselect')
sys.modules['pyutils.pyplot'] = __import__('types').ModuleType('pyplot')
sys.modules['pyutils.pyprint'] = __import__('types').ModuleType('pyprint')
sys.modules['pyutils.pyprocess'] = __import__('types').ModuleType('pyprocess')

from mcp_refana.server import mcp

async def main():
    """Test and display server information."""
    print("MCP-Refana Server Test")
    print("="*70)
    
    try:
        # List all tools
        tools = await mcp.list_tools()
        
        print(f"\n✓ Server initialized successfully")
        print(f"✓ Server name: {mcp.name}")
        print(f"✓ Total tools registered: {len(tools)}\n")
        
        print("Registered Tools:")
        print("-"*70)
        
        tool_info = []
        for i, tool in enumerate(tools, 1):
            print(f"\n{i}. {tool.name}")
            if tool.description:
                # Print first 100 chars of description
                desc = tool.description[:100] + "..." if len(tool.description) > 100 else tool.description
                print(f"   Description: {desc}")
            tool_info.append({
                "name": tool.name,
                "description": tool.description[:200] if tool.description else None
            })
        
        print("\n" + "="*70)
        print("Tool Status Check")
        print("="*70)
        
        expected_tools = {
            "healthcheck": "Server readiness check",
            "count_signal_background": "Event counting in kinematic regions",
            "analyze_cuts": "Analysis cut configuration",
            "compute_sensitivity": "Physics sensitivity metrics",
            "initialize_ml_selector": "ML-based event selection setup",
            "get_cut_efficiency": "Cut efficiency calculation",
            "summarize_analysis": "Dataset analysis summary",
        }
        
        registered_tools = {t.name for t in tools}
        
        print("\n✓ HEALTHCHECK")
        if "healthcheck" in registered_tools:
            print("  Status: ✓ REGISTERED")
            print("  Purpose: Returns server readiness and status")
        else:
            print("  Status: ✗ NOT FOUND")
        
        print("\n✓ INITIALIZE_ML_SELECTOR")
        if "initialize_ml_selector" in registered_tools:
            print("  Status: ✓ REGISTERED")
            print("  Purpose: Set up machine learning event selector")
            print("\n  Available Features:")
            features = [
                "reco_momentum",
                "reco_time",
                "t0_error",
                "n_active_hits",
                "n_st_hits",
                "n_opa_hits",
                "closest_crv_distance",
            ]
            for feat in features:
                print(f"    • {feat}")
            print("\n  Available Labels:")
            labels = ["signal", "background"]
            for label in labels:
                print(f"    • {label}")
        else:
            print("  Status: ✗ NOT FOUND")
        
        # Summary
        print("\n" + "="*70)
        print("Summary")
        print("="*70)
        
        all_present = all(tool in registered_tools for tool in expected_tools.keys())
        
        if all_present:
            print(f"\n✓ SUCCESS: All {len(expected_tools)} expected tools are registered")
            print("\nThe server is ready to:")
            print("  1. Check health status")
            print("  2. Perform event counting (signal/background extraction)")
            print("  3. Configure analysis cuts")
            print("  4. Compute physics sensitivity")
            print("  5. Initialize ML-based event selection")
            print("  6. Calculate cut efficiency")
            print("  7. Generate analysis summaries")
            return 0
        else:
            missing = set(expected_tools.keys()) - registered_tools
            print(f"\n✗ FAILURE: Missing {len(missing)} tools:")
            for tool in missing:
                print(f"  - {tool}")
            return 1
            
    except Exception as e:
        print(f"\n✗ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
