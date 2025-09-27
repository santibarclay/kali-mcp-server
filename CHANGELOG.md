# Changelog

All notable changes to the Kali Linux Security Tools MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-27

### Added
- ✨ **Initial Release**: Complete MCP server for Kali Linux security tools
- 🌐 **nmap_scan**: Network port scanning with configurable options
- 🔍 **nikto_scan**: Web vulnerability scanning with timeout controls
- 🔎 **searchsploit_search**: Exploit database search functionality
- 📋 **list_wordlists**: Custom wordlist management for directory brute forcing
- 🐳 **Docker Support**: Fully containerized with Kali Linux base image
- 🔒 **Security Features**: Input sanitization, non-root execution, timeout controls
- 📚 **Claude Desktop Integration**: Native MCP protocol support
- 🧪 **Testing Suite**: Comprehensive tool validation and health checks
- 📖 **Documentation**: Complete README, contributing guidelines, and security policy

### Security
- 🛡️ **Container Isolation**: All tools run in isolated Docker environment
- 👤 **Privilege Separation**: Non-root user execution with minimal capabilities
- 🧹 **Input Validation**: Comprehensive sanitization of all user inputs
- ⏱️ **Timeout Protection**: Configurable timeouts prevent hanging operations
- 📝 **Audit Logging**: All operations logged for security review

### Technical Details
- **Base Image**: kalilinux/kali-rolling:latest
- **Python Version**: 3.13
- **MCP Protocol**: Native SDK implementation with stdio transport
- **Container Runtime**: Docker with privileged network capabilities
- **Architecture**: Multi-architecture support (ARM64, x86_64)

### Tools Included
| Tool | Version | Purpose |
|------|---------|---------|
| nmap | 7.95 | Network reconnaissance and port scanning |
| nikto | 2.5.0 | Web application vulnerability assessment |
| searchsploit | Latest | Local exploit database search |
| Python | 3.13 | MCP server runtime and tool orchestration |

### Known Issues
- ⚠️ **Performance**: Network scans may timeout on slow connections
- ⚠️ **Connectivity**: Some tools require specific network configurations
- ⚠️ **Platform**: Optimized for Docker environments

### Breaking Changes
- None (Initial release)

### Deprecated
- None (Initial release)

### Removed
- None (Initial release)

### Fixed
- 🔧 **Nikto Timeouts**: Implemented proper timeout handling for web scans
- 🔧 **Container Permissions**: Fixed nmap execution with proper capabilities
- 🔧 **MCP Protocol**: Resolved session state management issues

---

## [Unreleased]

### Planned Features
- 🚀 **Additional Tools**: sqlmap, wpscan, dirb integration
- 🎯 **Custom Profiles**: Predefined scan configurations
- 📊 **Report Generation**: Structured output formats
- 🔄 **Auto-Updates**: Automatic tool and signature updates
- 🌐 **Web Interface**: Optional web-based management console

### Ideas for Future Releases
- Integration with popular security frameworks
- Support for custom tool plugins
- Advanced reporting and visualization
- Integration with CI/CD pipelines
- Multi-target batch processing
- Real-time collaboration features

---

**Legend:**
- ✨ New Feature
- 🔧 Bug Fix
- 🔒 Security
- 📚 Documentation
- 🚀 Enhancement
- ⚠️ Known Issue
- 💥 Breaking Change