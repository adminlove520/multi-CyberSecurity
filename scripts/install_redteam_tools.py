#!/usr/bin/env python3
"""
multi-CyberSecurity RedTeam Tools Installer
自动安装 RedTeam 渗透测试工具

Usage:
    python install_redteam_tools.py              # 安装所有工具
    python install_redteam_tools.py --windows     # 仅 Windows
    python install_redteam_tools.py --linux       # 仅 Linux
    python install_redteam_tools.py --macos       # 仅 macOS
    python install_redteam_tools.py --tools fscan,nuclei  # 仅安装指定工具
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path
from typing import List, Dict
import urllib.request
import zipfile
import tarfile
import shutil

# 工具定义
TOOLS: Dict[str, Dict] = {
    # Network Tools
    "fscan": {
        "type": "binary",
        "os": ["windows", "linux"],
        "urls": {
            "windows": "https://github.com/shadow1ng/fscan/releases/download/fscan_1.8.2/fscan_windows_amd64.exe",
            "linux": "https://github.com/shadow1ng/fscan/releases/download/fscan_1.8.2/fscan_linux_amd64",
        },
        "dest": "tools/Network/fscan",
    },
    "gogo": {
        "type": "binary",
        "os": ["linux"],
        "urls": {
            "linux": "https://github.com/woodpeckerers/gogo/releases/download/v1.2.2/gogo_linux_amd64",
        },
        "dest": "tools/Network/gogo",
    },
    "masscan": {
        "type": "binary",
        "os": ["linux"],
        "urls": {
            "linux": "https://github.com/robertdavidgraham/masscan/releases/download/1.3.2/masscan-1.3.2-linux.tar.gz",
        },
        "dest": "tools/Network/masscan",
    },
    # Web Tools
    "httpx": {
        "type": "binary",
        "os": ["windows", "linux", "macos"],
        "urls": {
            "windows": "https://github.com/projectdiscovery/httpx/releases/download/v1.3.6/httpx_1.3.6_windows_amd64.zip",
            "linux": "https://github.com/projectdiscovery/httpx/releases/download/v1.3.6/httpx_1.3.6_linux_amd64.zip",
            "macos": "https://github.com/projectdiscovery/httpx/releases/download/v1.3.6/httpx_1.3.6_macOS_amd64.zip",
        },
        "dest": "tools/Web/httpx",
    },
    "nuclei": {
        "type": "binary",
        "os": ["windows", "linux", "macos"],
        "urls": {
            "windows": "https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_windows_amd64.zip",
            "linux": "https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_linux_amd64.zip",
            "macos": "https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_macOS_amd64.zip",
        },
        "dest": "tools/Web/nuclei",
    },
    "ffuf": {
        "type": "binary",
        "os": ["windows", "linux", "macos"],
        "urls": {
            "windows": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_windows_amd64.zip",
            "linux": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
            "macos": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_macOS_amd64.tar.gz",
        },
        "dest": "tools/Web/ffuf",
    },
    # AD Tools
    "SharpHound": {
        "type": "binary",
        "os": ["windows"],
        "urls": {
            "windows": "https://github.com/BloodHoundAD/SharpHound3/releases/download/v1.1.0/SharpHound-v1.1.0.zip",
        },
        "dest": "tools/AD/SharpHound.exe",
    },
    "bloodhound": {
        "type": "pip",
        "os": ["linux", "macos", "windows"],
        "install": "pip install bloodhound",
        "dest": "tools/AD/bloodhound-python",
    },
    "impacket": {
        "type": "pip",
        "os": ["linux", "macos", "windows"],
        "install": "pip install impacket",
        "dest": "tools/AD/impacket",
    },
    "nxc": {
        "type": "pip",
        "os": ["linux", "macos", "windows"],
        "install": "pip install netexec",
        "dest": "tools/AD/nxc",
    },
    "responder": {
        "type": "git",
        "os": ["linux"],
        "url": "https://github.com/SpiderLabs/Responder.git",
        "dest": "tools/AD/Responder",
    },
    "kerbrute": {
        "type": "binary",
        "os": ["windows", "linux", "macos"],
        "urls": {
            "windows": "https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_windows_amd64.exe",
            "linux": "https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64",
            "macos": "https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_darwin_amd64",
        },
        "dest": "tools/AD/kerbrute",
    },
    # Wordlists
    "seclists": {
        "type": "git",
        "os": ["linux", "macos", "windows"],
        "url": "https://github.com/danielmiessler/SecLists.git",
        "dest": "wordlists/SecLists",
    },
}

# Nuclei Templates
NUCLEI_TEMPLATES = {
    "nuclei-templates": {
        "type": "git",
        "os": ["linux", "macos", "windows"],
        "url": "https://github.com/projectdiscovery/nuclei-templates.git",
        "dest": "wordlists/nuclei-templates",
    }
}


def get_os() -> str:
    """获取当前操作系统"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    else:
        return "linux"


def ensure_dir(path: Path):
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path) -> bool:
    """下载文件"""
    try:
        print(f"  Downloading: {url}")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def extract_zip(src: Path, dest_dir: Path):
    """解压 ZIP 文件"""
    try:
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        return True
    except Exception as e:
        print(f"  Error extracting {src}: {e}")
        return False


def extract_tar(src: Path, dest_dir: Path):
    """解压 TAR 文件"""
    try:
        with tarfile.open(src, 'r:*') as tar_ref:
            tar_ref.extractall(dest_dir)
        return True
    except Exception as e:
        print(f"  Error extracting {src}: {e}")
        return False


def clone_repo(url: str, dest: Path) -> bool:
    """克隆 Git 仓库"""
    try:
        print(f"  Cloning: {url}")
        subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], 
                      check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"  Error cloning {url}: {e}")
        return False


def install_pip(package: str) -> bool:
    """安装 Python 包"""
    try:
        print(f"  Installing: {package}")
        subprocess.run([sys.executable, "-m", "pip", "install", package], 
                      check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"  Error installing {package}: {e}")
        return False


def install_tool(name: str, tool_info: Dict, base_path: Path, current_os: str):
    """安装单个工具"""
    if current_os not in tool_info.get("os", []):
        print(f"  [{name}] 不支持当前操作系统: {current_os}")
        return False
    
    dest = base_path / tool_info["dest"]
    ensure_dir(dest.parent if tool_info["type"] == "binary" else dest)
    
    print(f"\n[*] Installing {name}...")
    
    tool_type = tool_info["type"]
    
    if tool_type == "binary":
        urls = tool_info.get("urls", {})
        if current_os not in urls:
            print(f"  [{name}] 没有当前系统的下载链接")
            return False
        
        url = urls[current_os]
        is_archive = url.endswith(('.zip', '.tar.gz', '.tar'))
        
        if is_archive:
            temp_file = base_path / f"temp_download.{url.split('.')[-1]}"
            if download_file(url, temp_file):
                if url.endswith('.zip'):
                    extract_zip(temp_file, dest.parent)
                else:
                    extract_tar(temp_file, dest.parent)
                temp_file.unlink()
        else:
            if download_file(url, dest if not dest.suffix else dest):
                if not dest.suffix:
                    # Linux binary without extension, add execute permission
                    if current_os != "windows":
                        os.chmod(dest, 0o755)
        
        return True
    
    elif tool_type == "pip":
        return install_pip(tool_info["install"])
    
    elif tool_type == "git":
        return clone_repo(tool_info["url"], dest)
    
    return False


def main():
    parser = argparse.ArgumentParser(description="multi-CyberSecurity RedTeam Tools Installer")
    parser.add_argument("--platform", choices=["windows", "linux", "macos"], 
                       help="指定平台")
    parser.add_argument("--tools", help="指定要安装的工具（逗号分隔）")
    parser.add_argument("--all", action="store_true", help="安装所有工具包括wordlists")
    parser.add_argument("--path", default=".", help="安装路径（默认当前目录）")
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    current_os = args.platform or get_os()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║       multi-CyberSecurity RedTeam Tools Installer          ║
║                                                              ║
║  Platform: {current_os:<51}║
║  Install Path: {str(base_path):<47}║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 确定要安装的工具
    if args.tools:
        tools_to_install = {t: TOOLS[t] for t in args.tools.split(",") if t in TOOLS}
    else:
        tools_to_install = TOOLS.copy()
    
    if args.all:
        tools_to_install.update(NUCLEI_TEMPLATES)
    
    # 安装工具
    success = []
    failed = []
    
    for name, info in tools_to_install.items():
        if install_tool(name, info, base_path, current_os):
            success.append(name)
        else:
            failed.append(name)
    
    # 打印结果
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                      Installation Results                   ║
╠══════════════════════════════════════════════════════════════╣
║  ✓ Success: {len(success):<50}║
║  ✗ Failed: {len(failed):<51}║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if failed:
        print(f"Failed tools: {', '.join(failed)}")
        return 1
    
    print("\n[✓] All tools installed successfully!")
    print(f"\nTools installed at: {base_path}")
    print(f"\nQuick start:")
    print(f"  ./tools/Network/fscan -h target -np -o scan.txt")
    print(f"  ./tools/Web/httpx -l targets.txt -silent -o httpx.txt")
    print(f"  python -m impacket.examples.secretsdump user:pass@target")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
