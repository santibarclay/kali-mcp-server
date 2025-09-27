#!/usr/bin/env python3
"""
Test the bridge connection
"""

import subprocess
import json
import time

def test_bridge():
    # Start the bridge
    process = subprocess.Popen(
        ["python3", "kali-mcp-bridge.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Test initialization
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }

    try:
        # Send initialization
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()

        # Read response
        response = process.stdout.readline()
        print(f"Init response: {response.strip()}")

        # Now try to list tools
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        process.stdin.write(json.dumps(list_request) + '\n')
        process.stdin.flush()

        response2 = process.stdout.readline()
        print(f"List response: {response2.strip()}")

    finally:
        process.terminate()

if __name__ == "__main__":
    test_bridge()