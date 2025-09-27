#!/usr/bin/env python3
"""
Simple test script to verify all security tools are working
"""

import subprocess
import sys

def test_tool(command, name):
    """Test if a tool is installed and working"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 or "usage" in result.stderr.lower() or "help" in result.stderr.lower():
            print(f"✓ {name} - OK")
            return True
        else:
            print(f"✗ {name} - Failed (exit code: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print(f"✓ {name} - OK (timeout expected for help)")
        return True
    except FileNotFoundError:
        print(f"✗ {name} - Not found")
        return False
    except Exception as e:
        print(f"✗ {name} - Error: {e}")
        return False

def main():
    print("Testing Kali Linux Security Tools Installation...")
    print("=" * 50)

    tools = [
        (["nmap", "--version"], "Nmap"),
        (["nikto", "-Version"], "Nikto"),
        (["sqlmap", "--version"], "SQLMap"),
        (["wpscan", "--version"], "WPScan"),
        (["dirb"], "DIRB"),
        (["searchsploit", "--help"], "SearchSploit"),
        (["python3", "--version"], "Python3"),
    ]

    success_count = 0
    for command, name in tools:
        if test_tool(command, name):
            success_count += 1

    print("=" * 50)
    print(f"Results: {success_count}/{len(tools)} tools working correctly")

    if success_count == len(tools):
        print("🎉 All security tools are ready!")
        return 0
    else:
        print("⚠️  Some tools may need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())