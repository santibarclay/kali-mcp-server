#!/usr/bin/env python3
"""
Test script to debug MCP communication issues
"""

import subprocess
import json
import time

def send_mcp_request(request):
    """Send a JSON-RPC request to the MCP server"""
    cmd = ["docker", "exec", "-i", "kali-security-mcp", "python3", "server.py"]

    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send the request
        stdout, stderr = process.communicate(input=json.dumps(request) + '\n', timeout=10)

        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        print(f"Return code: {process.returncode}")

        return stdout, stderr

    except subprocess.TimeoutExpired:
        process.kill()
        print("Request timed out")
        return None, "Timeout"
    except Exception as e:
        print(f"Error: {e}")
        return None, str(e)

def test_mcp_flow():
    """Test the complete MCP initialization and tool usage flow"""
    print("=== Testing MCP Server Communication ===")

    # Step 1: Initialize
    print("\n1. Testing initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }

    stdout, stderr = send_mcp_request(init_request)

    # Step 2: Try to list tools (this may not work due to session issues)
    print("\n2. Testing tool listing...")
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    stdout2, stderr2 = send_mcp_request(list_request)

if __name__ == "__main__":
    test_mcp_flow()