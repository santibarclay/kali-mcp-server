#!/usr/bin/env python3
"""
Native MCP Server for Kali Linux Security Tools
Using the official MCP Python SDK instead of FastMCP
"""

import asyncio
import subprocess
import json
import re
import ipaddress
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Initialize MCP server
server = Server("kali-security-tools")


def sanitize_target(target: str) -> str:
    """Sanitize and validate target input"""
    target = re.sub(r'[;&|`$(){}[\]<>]', '', target)
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', target):
            return target
        else:
            raise ValueError(f"Invalid target format: {target}")


def sanitize_port_range(port_range: str) -> str:
    """Sanitize port range input"""
    if not re.match(r'^[0-9,-]+$', port_range):
        raise ValueError("Invalid port range format")
    return port_range


async def run_command(cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
    """Execute command with timeout and return structured result"""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )

            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode('utf-8'),
                "stderr": stderr.decode('utf-8'),
                "command": " ".join(cmd)
            }
        except asyncio.TimeoutError:
            process.kill()
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


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available security tools"""
    return [
        Tool(
            name="nmap_scan",
            description="Perform network port scanning with nmap",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target IP address or hostname"},
                    "ports": {"type": "string", "description": "Port specification (e.g., '80,443', '1-1000')"},
                    "scan_type": {"type": "string", "enum": ["syn", "tcp", "udp"], "default": "syn"},
                    "timing": {"type": "string", "enum": ["0", "1", "2", "3", "4", "5"], "default": "3"},
                    "service_detection": {"type": "boolean", "default": False},
                    "os_detection": {"type": "boolean", "default": False}
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="nikto_scan",
            description="Perform web vulnerability scanning with Nikto",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target IP address or hostname"},
                    "port": {"type": "string", "default": "80", "description": "Target port"},
                    "ssl": {"type": "boolean", "default": False, "description": "Use SSL/HTTPS connection"}
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="searchsploit_search",
            description="Search for exploits using searchsploit",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {"type": "string", "description": "Software/service to search for"},
                    "exact_match": {"type": "boolean", "default": False, "description": "Use exact matching"}
                },
                "required": ["search_term"]
            }
        ),
        Tool(
            name="list_wordlists",
            description="List available wordlists for directory brute forcing",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ffuf_fuzz",
            description="Fast web fuzzer for directory/file discovery and parameter fuzzing",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target URL (use FUZZ placeholder for fuzzing point)"},
                    "wordlist": {"type": "string", "default": "/usr/share/dirb/wordlists/common.txt", "description": "Wordlist file path"},
                    "extensions": {"type": "string", "description": "File extensions to test (e.g., 'php,html,js')"},
                    "threads": {"type": "integer", "default": 40, "description": "Number of threads"},
                    "filter_status": {"type": "string", "description": "Filter HTTP status codes (e.g., '404,403')"}
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="gobuster_dir",
            description="Directory/file brute forcer using Go",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target URL"},
                    "wordlist": {"type": "string", "default": "/usr/share/dirb/wordlists/common.txt", "description": "Wordlist file path"},
                    "extensions": {"type": "string", "description": "File extensions to test (e.g., 'php,html,js')"},
                    "threads": {"type": "integer", "default": 10, "description": "Number of threads"},
                    "status_codes": {"type": "string", "default": "200,204,301,302,307,401,403", "description": "Positive status codes"}
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="httpx_probe",
            description="Fast HTTP probe for discovering live hosts and services",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target URL or host"},
                    "ports": {"type": "string", "description": "Port list (e.g., '80,443,8080')"},
                    "follow_redirects": {"type": "boolean", "default": True, "description": "Follow HTTP redirects"},
                    "title": {"type": "boolean", "default": True, "description": "Extract page titles"},
                    "tech_detect": {"type": "boolean", "default": True, "description": "Detect technologies"}
                },
                "required": ["target"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""

    if name == "nmap_scan":
        try:
            target = sanitize_target(arguments["target"])
            cmd = ["nmap"]

            # Scan type
            scan_type = arguments.get("scan_type", "syn")
            if scan_type == "syn":
                cmd.append("-sS")
            elif scan_type == "tcp":
                cmd.append("-sT")
            elif scan_type == "udp":
                cmd.append("-sU")

            # Timing
            timing = arguments.get("timing", "3")
            cmd.extend(["-T", timing])

            # Port specification
            ports = arguments.get("ports")
            if ports:
                ports = sanitize_port_range(ports)
                cmd.extend(["-p", ports])

            # Service detection
            if arguments.get("service_detection", False):
                cmd.append("-sV")

            # OS detection
            if arguments.get("os_detection", False):
                cmd.append("-O")

            cmd.append(target)

            result = await run_command(cmd, timeout=600)

            if result["success"]:
                return [TextContent(type="text", text=f"NMAP SCAN RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"NMAP SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "nikto_scan":
        try:
            target = sanitize_target(arguments["target"])
            port = sanitize_port_range(arguments.get("port", "80"))

            cmd = ["nikto", "-h", f"{target}:{port}", "-maxtime", "180", "-timeout", "8"]

            if arguments.get("ssl", False):
                cmd.append("-ssl")

            result = await run_command(cmd, timeout=600)

            if result["success"]:
                return [TextContent(type="text", text=f"NIKTO SCAN RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"NIKTO SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "searchsploit_search":
        try:
            search_term = re.sub(r'[;&|`$(){}[\]<>]', '', arguments["search_term"])

            cmd = ["searchsploit", search_term]

            if arguments.get("exact_match", False):
                cmd.append("--exact")

            result = await run_command(cmd, timeout=60)

            if result["success"]:
                return [TextContent(type="text", text=f"SEARCHSPLOIT RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"SEARCHSPLOIT FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "list_wordlists":
        try:
            wordlists_dir = Path("/home/pentest/wordlists")
            if wordlists_dir.exists():
                wordlists = [f.name for f in wordlists_dir.iterdir() if f.is_file()]
                if wordlists:
                    return [TextContent(type="text", text=f"Available wordlists:\n" + "\n".join(f"- {wl}" for wl in sorted(wordlists)))]
                else:
                    return [TextContent(type="text", text="No custom wordlists found. Using default dirb wordlists.")]
            else:
                return [TextContent(type="text", text="Wordlists directory not found. Using default dirb wordlists.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing wordlists: {str(e)}")]

    elif name == "ffuf_fuzz":
        try:
            target = arguments["target"]
            # Basic URL validation
            if not target.startswith(("http://", "https://")):
                target = f"http://{target}"

            wordlist = arguments.get("wordlist", "/usr/share/dirb/wordlists/common.txt")
            threads = arguments.get("threads", 40)

            cmd = ["ffuf", "-u", target, "-w", wordlist, "-t", str(threads), "-c"]

            # Add extensions if specified
            extensions = arguments.get("extensions")
            if extensions:
                cmd.extend(["-e", extensions])

            # Filter status codes if specified
            filter_status = arguments.get("filter_status")
            if filter_status:
                cmd.extend(["-fc", filter_status])

            result = await run_command(cmd, timeout=300)

            if result["success"]:
                return [TextContent(type="text", text=f"FFUF FUZZING RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"FFUF FUZZING FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "gobuster_dir":
        try:
            target = arguments["target"]
            # Basic URL validation
            if not target.startswith(("http://", "https://")):
                target = f"http://{target}"

            wordlist = arguments.get("wordlist", "/usr/share/dirb/wordlists/common.txt")
            threads = arguments.get("threads", 10)
            status_codes = arguments.get("status_codes", "200,204,301,302,307,401,403")

            cmd = ["gobuster", "dir", "-u", target, "-w", wordlist, "-t", str(threads), "-s", status_codes, "-q"]

            # Add extensions if specified
            extensions = arguments.get("extensions")
            if extensions:
                cmd.extend(["-x", extensions])

            result = await run_command(cmd, timeout=300)

            if result["success"]:
                return [TextContent(type="text", text=f"GOBUSTER DIRECTORY SCAN RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"GOBUSTER DIRECTORY SCAN FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "httpx_probe":
        try:
            target = arguments["target"]

            cmd = ["httpx", "-u", target, "-silent"]

            # Add ports if specified
            ports = arguments.get("ports")
            if ports:
                cmd.extend(["-p", ports])

            # Follow redirects
            if arguments.get("follow_redirects", True):
                cmd.append("-fr")

            # Extract titles
            if arguments.get("title", True):
                cmd.append("-title")

            # Technology detection
            if arguments.get("tech_detect", True):
                cmd.append("-tech-detect")

            result = await run_command(cmd, timeout=120)

            if result["success"]:
                return [TextContent(type="text", text=f"HTTPX PROBE RESULTS:\n{result['stdout']}")]
            else:
                return [TextContent(type="text", text=f"HTTPX PROBE FAILED:\nError: {result.get('stderr', result.get('error', 'Unknown error'))}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    print("Starting Kali Security Tools MCP Server (Native)", file=sys.stderr)
    print("Available tools: nmap_scan, nikto_scan, searchsploit_search, list_wordlists, ffuf_fuzz, gobuster_dir, httpx_probe", file=sys.stderr)
    print("WARNING: Use only for educational purposes in controlled environments!", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())