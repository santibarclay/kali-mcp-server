#!/bin/bash
# Wrapper script to run Kali Security MCP Server for Claude Desktop
# Ensures the container is running and starts the MCP server

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "kali-security-mcp"; then
    echo "Container not running. Starting..." >&2
    docker-compose up -d
    sleep 2
fi

# Execute the MCP server
docker exec -i kali-security-mcp python3 server.py