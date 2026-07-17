#!/bin/bash
# Run mcp-refana server with Mu2e analysis environment activated

# Activate Mu2e analysis environment
source /cvmfs/mu2e.opensciencegrid.org/env/ana/current/bin/activate

# Run the server with provided arguments (default to stdio)
TRANSPORT="${1:---transport stdio}"
mcp-refana-server $TRANSPORT
