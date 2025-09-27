#!/usr/bin/env python3
"""
Persistent bridge for Kali Security Tools MCP Server
This script maintains a persistent connection to the Docker container
"""

import subprocess
import sys
import json
import signal
import os

class KaliMCPBridge:
    def __init__(self):
        self.docker_process = None
        self.initialized = False

    def start_docker_process(self):
        """Start a persistent Docker process"""
        try:
            cmd = ["docker", "exec", "-i", "kali-security-mcp", "python3", "server.py"]
            self.docker_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )

            # Print startup messages to stderr
            print("Kali Security Tools MCP Bridge Starting...", file=sys.stderr)
            print("Container: kali-security-mcp", file=sys.stderr)
            print("Available tools: nmap, nikto, sqlmap, wpscan, dirb, searchsploit", file=sys.stderr)

            return True
        except Exception as e:
            print(f"Failed to start Docker process: {e}", file=sys.stderr)
            return False

    def handle_request(self, request_line):
        """Handle a single MCP request"""
        if not self.docker_process:
            return None

        try:
            # Send request to Docker process
            self.docker_process.stdin.write(request_line + '\n')
            self.docker_process.stdin.flush()

            # Read response
            response = self.docker_process.stdout.readline()
            return response.strip() if response else None

        except Exception as e:
            print(f"Error handling request: {e}", file=sys.stderr)
            return None

    def run(self):
        """Main loop to handle MCP requests"""
        if not self.start_docker_process():
            sys.exit(1)

        try:
            # Read from stdin and forward to Docker process
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                response = self.handle_request(line)
                if response:
                    print(response, flush=True)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Bridge error: {e}", file=sys.stderr)
        finally:
            if self.docker_process:
                self.docker_process.terminate()

def signal_handler(signum, frame):
    print("Shutting down Kali MCP Bridge...", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    bridge = KaliMCPBridge()
    bridge.run()