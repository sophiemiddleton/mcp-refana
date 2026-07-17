# MCP Refana Server

Model Context Protocol (MCP) server for Mu2e refana analysis workflows. Exposes core analysis functions as MCP tools for integration with agentic frameworks.

## Environment Setup

This project requires the Mu2e analysis environment. On Mu2e gpvm's, activate the environment first:

```bash
source /cvmfs/mu2e.opensciencegrid.org/env/ana/current/bin/activate
```

This provides:
- `pyutils` - Python interface to EventNtuple
- `uproot` - ROOT file handling
- `awkward` - Ragged array support
- `numpy`, `scipy`, `scikit-learn`, `xgboost`, `matplotlib`

## Features

- **Event Counting**: Signal/background extraction in kinematic regions
- **Cut Analysis**: Definition and application of analysis cuts
- **Sensitivity Computation**: Discovery significance, CLs limits, Feldman-Cousins intervals
- **ML Selection**: BDT-based signal/background discrimination setup
- **Analysis Summaries**: Dataset-level analysis results

## Installation

```bash
# Activate Mu2e analysis environment
source /cvmfs/mu2e.opensciencegrid.org/env/ana/current/bin/activate

# Install mcp-refana in development mode
cd mcp-refana
pip install -e .
```

## Running the Server

**Important**: Always activate the Mu2e environment before running.

```bash
# Source Mu2e environment
source /cvmfs/mu2e.opensciencegrid.org/env/ana/current/bin/activate

# Start server with stdio transport (default)
mcp-refana-server --transport stdio
```

Or with HTTP transport:

```bash
source /cvmfs/mu2e.opensciencegrid.org/env/ana/current/bin/activate
mcp-refana-server --transport streamable-http
```

## Available Tools

### `healthcheck()`
Returns server status.

### `count_signal_background(mom_list, time_list, mc_list, mom_range, time_range, sign)`
Extract signal and background event counts in a defined kinematic window.

**Parameters:**
- `mom_list`: Reconstructed momentum values
- `time_list`: Reconstructed time values  
- `mc_list`: MC truth labels
- `mom_range`: [min, max] momentum window
- `time_range`: [min, max] time window
- `sign`: "minus" (electrons) or "plus" (positrons)

**Returns:** Signal/background counts and statistics

### `analyze_cuts(cut_definitions, sign)`
Initialize analysis cut configuration.

### `compute_sensitivity(s_expected, b_expected, b_sys_uncertainty, exposure, efficiency)`
Compute physics sensitivity metrics:
- Asimov significance Z
- 95% CLs upper limit
- 90% Feldman-Cousins confidence interval

### `initialize_ml_selector()`
Set up machine learning event selector.

### `get_cut_efficiency(cuts_applied, n_total, n_surviving)`
Calculate efficiency metrics for applied cuts.

### `summarize_analysis(dataset_name, sign, n_events_processed, signal_count, background_count, ml_score_mean)`
Generate analysis summary for a dataset.

## Integration with HEP-Multiagent

Register this server in the multiagent's `config.py`:

```python
"refana": {
    "command": ["mcp-refana-server", "--transport", "stdio"],
    "description": "Mu2e refana analysis server",
}
```

Then use in worker nodes for agentic analysis workflows.

## Architecture

```
src/mcp_refana/
├── __init__.py
├── server.py              # FastMCP server setup
└── mcp_tools/
    ├── __init__.py
    └── refana_wrappers.py # Tool definitions wrapping refana code
```

The server wraps the core refana analysis classes (Count, Analyze, MLSelect, SensitivityAnalyzer) as MCP tools, making them accessible to agents via tool calls.

## Dependencies

- **mcp**: Model Context Protocol framework
- **refana**: Core analysis code (count, analyze, ML selection, sensitivity)
- **numpy, scipy**: Numerical computing
- **scikit-learn, xgboost**: Machine learning
- **uproot, awkward**: ROOT file handling
- **matplotlib**: Visualization

## Development

Run tests:
```bash
pytest tests/
```

Format code:
```bash
ruff check . --fix
```

## Contact

Sophie Middleton, Huma Jafree
