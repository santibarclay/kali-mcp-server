# Kali Linux Security Tools MCP Server

A Model Context Protocol (MCP) server that provides access to Kali Linux penetration testing tools through Claude Desktop.

⚠️ **For educational purposes and authorized testing only**

## Tools

| Tool | Description |
|------|-------------|
| `nmap_scan` | Network port scanning and service detection |
| `nikto_scan` | Web vulnerability scanning (traditional apps) |
| `searchsploit_search` | Search exploit database |
| `list_wordlists` | List available wordlists |
| `httpx_probe` | Fast HTTP probe for discovering live hosts and services |
| `gobuster_dir` | Directory/file brute forcer optimized for modern web apps |
| `ffuf_fuzz` | Fast web fuzzer for directory discovery and parameter fuzzing |

## Quick Start

1. **Start the container:**
   ```bash
   docker-compose up --build -d
   ```

2. **Add to Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "kali-security": {
         "command": "docker",
         "args": ["exec", "-i", "kali-security-mcp", "python3", "server_native.py"],
         "env": {}
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Usage Examples

- "Scan httpbin.org port 80 with nmap"
- "Run nikto scan on http://httpbin.org" (traditional web apps)
- "Use httpx to probe localhost:3001"
- "Run gobuster directory scan on http://localhost:3001"
- "Use ffuf to fuzz http://localhost:3001/FUZZ"
- "Search for Apache exploits"
- "List available wordlists"

## Requirements

- Docker and Docker Compose
- Claude Desktop

## Security Features

- Containerized execution
- Input sanitization
- Non-root user
- Command timeouts

## Notes

- **Traditional vs Modern Apps**:
  - **Nikto**: Best for traditional web apps (PHP/Apache/Nginx)
  - **Modern SPAs**: Use httpx, gobuster, and ffuf for better results with React/Angular/Vue apps
- **Recommended workflow for SPAs**:
  1. **httpx**: Probe for live services and technology detection
  2. **gobuster**: Directory/file brute forcing
  3. **ffuf**: Parameter fuzzing and advanced discovery
- **Testing targets**: Use JuiceShop (OWASP vulnerable app) for safe testing
- Restart Claude Desktop after timeout errors for better performance