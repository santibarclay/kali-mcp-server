# Contributing to Kali Linux Security Tools MCP Server

🎉 Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Kali Linux Security Tools MCP Server.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Adding New Tools](#adding-new-tools)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## 🤝 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- Be respectful and inclusive
- Use this project only for educational and authorized testing purposes
- Do not contribute anything that could be used for malicious purposes
- Report security vulnerabilities responsibly
- Help maintain a welcoming environment for all contributors

## 🚀 Getting Started

### Prerequisites

Before contributing, make sure you have:

- Docker and Docker Compose installed
- Basic knowledge of Python and containerization
- Understanding of cybersecurity and ethical hacking principles
- Familiarity with the Model Context Protocol (MCP)

### Initial Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/kali-mcp-server.git
   cd kali-mcp-server
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/kali-mcp-server.git
   ```
4. **Build and test** the container:
   ```bash
   docker-compose up --build -d
   docker exec kali-security-mcp python3 test_tools.py
   ```

## 💡 How to Contribute

### Types of Contributions

We welcome the following types of contributions:

- 🐛 **Bug fixes** - Fix issues with existing tools
- ✨ **New features** - Add new security tools or capabilities
- 📚 **Documentation** - Improve README, add examples, fix typos
- 🧪 **Testing** - Add or improve test coverage
- 🔒 **Security** - Report vulnerabilities (privately)
- 🛠️ **Infrastructure** - Improve Docker configuration, CI/CD

### What We Don't Accept

- Malicious code or backdoors
- Tools designed for illegal activities
- Contributions that bypass security measures
- Poorly documented or untested code

## 🔧 Development Setup

### Local Development

1. **Create a development branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes**:
   ```bash
   # Rebuild container
   docker-compose down
   docker-compose up --build -d

   # Run tests
   docker exec kali-security-mcp python3 test_tools.py

   # Test MCP server
   docker exec kali-security-mcp python3 server_native.py --test
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new security tool XYZ"
   ```

### Coding Standards

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: All functions must have docstrings
- **Security**: All inputs must be sanitized
- **Error handling**: Use proper exception handling
- **Logging**: Include appropriate logging for debugging

## 🛠️ Adding New Tools

To add a new security tool to the MCP server:

### 1. Install the Tool

Add the tool installation to `Dockerfile`:

```dockerfile
RUN apt-get install -y your-new-tool
```

### 2. Add Tool Definition

In `server_native.py`, add your tool to the `list_tools()` function:

```python
Tool(
    name="your_tool_name",
    description="Clear description of what the tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname"
            },
            "option1": {
                "type": "boolean",
                "default": False,
                "description": "Enable special feature"
            }
        },
        "required": ["target"]
    }
)
```

### 3. Implement Tool Handler

Add the tool logic in the `call_tool()` function:

```python
elif name == "your_tool_name":
    try:
        target = sanitize_target(arguments["target"])

        cmd = ["your-tool", target]

        if arguments.get("option1", False):
            cmd.append("--special-flag")

        result = await run_command(cmd, timeout=300)

        if result["success"]:
            return [TextContent(
                type="text",
                text=f"TOOL RESULTS:\n{result['stdout']}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"TOOL FAILED:\n{result.get('stderr', 'Unknown error')}"
            )]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

### 4. Add to Test Suite

Update `test_tools.py` to include your new tool:

```python
tools = [
    # ... existing tools ...
    (["your-tool", "--version"], "Your Tool"),
]
```

### 5. Update Documentation

- Add tool description to README.md
- Include usage examples
- Document all parameters

## 🧪 Testing

### Running Tests

```bash
# Test tool installation
docker exec kali-security-mcp python3 test_tools.py

# Test MCP server functionality
python3 test_mcp.py

# Manual testing
docker exec -it kali-security-mcp bash
```

### Test Requirements

All contributions should include:

- Unit tests for new functionality
- Integration tests for tool interactions
- Documentation updates
- Security validation

## 📖 Documentation

### Documentation Standards

- Use clear, concise language
- Include practical examples
- Add security warnings where appropriate
- Keep README.md updated with new features

### Required Documentation

For new tools, please provide:

- Tool purpose and use cases
- Parameter descriptions
- Usage examples
- Security considerations
- Troubleshooting tips

## 📤 Submitting Changes

### Pull Request Process

1. **Update your branch** with upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was modified
   - References to any related issues
   - Screenshots or examples if applicable

### Pull Request Requirements

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Security considerations are addressed
- [ ] Commit messages are clear and descriptive

### Review Process

1. **Automated checks** must pass
2. **Security review** for any new tools
3. **Code review** by maintainers
4. **Testing** in various environments
5. **Documentation review**

## 🔒 Security Guidelines

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities. Instead:

1. Email security concerns to: [security@yourproject.com]
2. Include detailed description and reproduction steps
3. Allow reasonable time for response before public disclosure

### Security Best Practices

- Always sanitize user inputs
- Use least-privilege principles
- Include security warnings in documentation
- Test for common vulnerabilities
- Follow secure coding practices

## 🆘 Getting Help

If you need help with your contribution:

- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Open an issue for bugs or feature requests
- 📧 **Email**: Contact maintainers for sensitive topics

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to the cybersecurity community! 🛡️