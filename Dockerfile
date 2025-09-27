FROM kalilinux/kali-rolling:latest

# Update and install required packages
RUN apt-get update && apt-get install -y \
    nmap \
    nikto \
    sqlmap \
    wpscan \
    dirb \
    exploitdb \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    libcap2-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with sudo privileges
RUN useradd -m -s /bin/bash pentest && \
    echo "pentest ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set up Python virtual environment
USER pentest
WORKDIR /home/pentest

RUN python3 -m venv venv
ENV PATH="/home/pentest/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy MCP server files
COPY server.py .
COPY test_tools.py .
COPY wordlists/ ./wordlists/

# Set capabilities for network tools (run as root temporarily)
USER root
RUN setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap
USER pentest

# Expose MCP server port
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/home/pentest
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8000

# Keep container running and provide shell access
CMD ["/bin/bash", "-c", "echo 'Kali Security MCP Server Ready!' && echo 'Use: python server.py to start MCP server' && echo 'Or exec into container: docker exec -it kali-security-mcp bash' && tail -f /dev/null"]