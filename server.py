#!/usr/bin/env python3
"""
Kali Linux Security Tools MCP Server
Educational penetration testing tools for controlled environments only.
"""

import subprocess
import json
import re
import ipaddress
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import asyncio
import os

from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Kali Security Tools")

def sanitize_target(target: str) -> str:
    """Sanitize and validate target input"""
    # Remove dangerous characters
    target = re.sub(r'[;&|`$(){}[\]<>]', '', target)

    # Validate IP or domain format
    try:
        # Try to parse as IP address
        ipaddress.ip_address(target)
        return target
    except ValueError:
        # If not IP, validate domain format
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', target):
            return target
        else:
            raise ValueError(f"Invalid target format: {target}")

def sanitize_port_range(port_range: str) -> str:
    """Sanitize port range input"""
    if not re.match(r'^[0-9,-]+$', port_range):
        raise ValueError("Invalid port range format")
    return port_range

def run_command(cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
    """Execute command with timeout and return structured result"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(cmd)
        }

@mcp.tool()
def nmap_scan(
    target: str,
    ports: Optional[str] = None,
    scan_type: str = "syn",
    timing: str = "3",
    service_detection: bool = False,
    os_detection: bool = False
) -> str:
    """
    Perform network port scanning with nmap

    Args:
        target: Target IP address or hostname
        ports: Port specification (e.g., "80,443", "1-1000")
        scan_type: Type of scan (syn, tcp, udp)
        timing: Timing template (0-5, where 0 is slowest and 5 is fastest)
        service_detection: Enable service version detection
        os_detection: Enable OS detection
    """
    try:
        target = sanitize_target(target)

        cmd = ["nmap"]

        # Scan type
        if scan_type == "syn":
            cmd.append("-sS")
        elif scan_type == "tcp":
            cmd.append("-sT")
        elif scan_type == "udp":
            cmd.append("-sU")

        # Timing
        cmd.extend(["-T", timing])

        # Port specification
        if ports:
            ports = sanitize_port_range(ports)
            cmd.extend(["-p", ports])

        # Service detection
        if service_detection:
            cmd.append("-sV")

        # OS detection
        if os_detection:
            cmd.append("-O")

        cmd.append(target)

        result = run_command(cmd, timeout=600)

        if result["success"]:
            return f"NMAP SCAN RESULTS:\n{result['stdout']}"
        else:
            return f"NMAP SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def nikto_scan(target: str, port: str = "80", ssl: bool = False) -> str:
    """
    Perform web vulnerability scanning with Nikto

    Args:
        target: Target IP address or hostname
        port: Target port (default: 80)
        ssl: Use SSL/HTTPS connection
    """
    try:
        target = sanitize_target(target)
        port = sanitize_port_range(port)

        cmd = ["nikto", "-h", f"{target}:{port}"]

        if ssl:
            cmd.append("-ssl")

        result = run_command(cmd, timeout=900)

        if result["success"]:
            return f"NIKTO SCAN RESULTS:\n{result['stdout']}"
        else:
            return f"NIKTO SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def sqlmap_test(
    url: str,
    data: Optional[str] = None,
    cookie: Optional[str] = None,
    risk: str = "1",
    level: str = "1"
) -> str:
    """
    Test for SQL injection vulnerabilities with sqlmap

    Args:
        url: Target URL
        data: POST data string
        cookie: Cookie string
        risk: Risk level (1-3)
        level: Test level (1-5)
    """
    try:
        # Basic URL validation
        if not re.match(r'^https?://', url):
            raise ValueError("URL must start with http:// or https://")

        cmd = ["sqlmap", "-u", url, "--batch", "--risk", risk, "--level", level]

        if data:
            cmd.extend(["--data", data])

        if cookie:
            cmd.extend(["--cookie", cookie])

        result = run_command(cmd, timeout=1200)

        if result["success"]:
            return f"SQLMAP TEST RESULTS:\n{result['stdout']}"
        else:
            return f"SQLMAP TEST FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def wpscan_scan(url: str, enumerate: str = "p,t,u") -> str:
    """
    Scan WordPress sites with WPScan

    Args:
        url: WordPress site URL
        enumerate: What to enumerate (p=plugins, t=themes, u=users)
    """
    try:
        # Basic URL validation
        if not re.match(r'^https?://', url):
            raise ValueError("URL must start with http:// or https://")

        cmd = ["wpscan", "--url", url, "--enumerate", enumerate, "--format", "cli"]

        result = run_command(cmd, timeout=900)

        if result["success"]:
            return f"WPSCAN RESULTS:\n{result['stdout']}"
        else:
            return f"WPSCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def dirb_scan(
    url: str,
    wordlist: Optional[str] = None,
    extensions: Optional[str] = None
) -> str:
    """
    Directory and file brute forcing with dirb

    Args:
        url: Target URL
        wordlist: Path to custom wordlist (optional)
        extensions: File extensions to search for (e.g., "php,html,txt")
    """
    try:
        # Basic URL validation
        if not re.match(r'^https?://', url):
            raise ValueError("URL must start with http:// or https://")

        cmd = ["dirb", url]

        # Use custom wordlist if provided
        if wordlist:
            wordlist_path = Path(f"/home/pentest/wordlists/{wordlist}")
            if wordlist_path.exists():
                cmd.append(str(wordlist_path))
            else:
                return f"Error: Wordlist '{wordlist}' not found in /home/pentest/wordlists/"

        # Add extensions
        if extensions:
            cmd.extend(["-X", extensions])

        result = run_command(cmd, timeout=900)

        if result["success"]:
            return f"DIRB SCAN RESULTS:\n{result['stdout']}"
        else:
            return f"DIRB SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def searchsploit_search(search_term: str, exact_match: bool = False) -> str:
    """
    Search for exploits using searchsploit

    Args:
        search_term: Software/service to search for
        exact_match: Use exact matching
    """
    try:
        # Sanitize search term
        search_term = re.sub(r'[;&|`$(){}[\]<>]', '', search_term)

        cmd = ["searchsploit", search_term]

        if exact_match:
            cmd.append("--exact")

        result = run_command(cmd, timeout=60)

        if result["success"]:
            return f"SEARCHSPLOIT RESULTS:\n{result['stdout']}"
        else:
            return f"SEARCHSPLOIT FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}"

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_wordlists() -> str:
    """List available wordlists for directory brute forcing"""
    try:
        wordlists_dir = Path("/home/pentest/wordlists")
        if wordlists_dir.exists():
            wordlists = [f.name for f in wordlists_dir.iterdir() if f.is_file()]
            if wordlists:
                return f"Available wordlists:\n" + "\n".join(f"- {wl}" for wl in sorted(wordlists))
            else:
                return "No custom wordlists found. Using default dirb wordlists."
        else:
            return "Wordlists directory not found. Using default dirb wordlists."
    except Exception as e:
        return f"Error listing wordlists: {str(e)}"

if __name__ == "__main__":
    print("Starting Kali Security Tools MCP Server", file=sys.stderr)
    print("Available tools: nmap, nikto, sqlmap, wpscan, dirb, searchsploit", file=sys.stderr)
    print("WARNING: Use only for educational purposes in controlled environments!", file=sys.stderr)

    mcp.run()