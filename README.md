# Kali Linux Security Tools MCP Server

A Model Context Protocol (MCP) server that provides access to Kali Linux penetration testing tools through Claude Desktop.

⚠️ **For educational purposes and authorized testing only**

## Tools

| Tool | Description |
|------|-------------|
| `nmap_scan` | Network port scanning and service detection |
| `nikto_scan` | Web vulnerability scanning |
| `searchsploit_search` | Search exploit database |
| `list_wordlists` | List available wordlists |

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
- "Run nikto scan on http://httpbin.org"
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

- **Nikto limitations**: Works best on traditional web apps. Modern SPAs (like Angular/React) may timeout or show limited results
- **Best targets for Nikto**: Traditional PHP/Apache/Nginx sites like httpbin.org
- **For SPAs**: Use nmap for port discovery, searchsploit for specific vulnerabilities
- Restart Claude Desktop after timeout errors for better performance