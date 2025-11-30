"""Premium features installation for Claude CodePro."""

from __future__ import annotations

import json
import os
import platform
import stat
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GUMROAD_VERIFY_URL = "https://api.gumroad.com/v2/licenses/verify"
PRODUCT_ID = "c3Sr8oRvWIimCH1zf5I02w=="

GITHUB_REPO = "maxritter/claude-codepro"


def get_platform_binary_name() -> str:
    """Get the correct binary name for the current platform."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        arch = "x86_64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine

    if system == "darwin":
        return f"ccp-premium-darwin-{arch}"
    elif system == "linux":
        return f"ccp-premium-linux-{arch}"
    elif system == "windows":
        return f"ccp-premium-windows-{arch}.exe"
    else:
        return f"ccp-premium-{system}-{arch}"


def validate_license_key(license_key: str) -> tuple[bool, str]:
    """Validate license key with Gumroad API."""
    try:
        data = urllib.parse.urlencode(
            {
                "product_id": PRODUCT_ID,
                "license_key": license_key,
                "increment_uses_count": "false",
            }
        ).encode()

        request = urllib.request.Request(
            GUMROAD_VERIFY_URL,
            data=data,
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.loads(response.read().decode())

            if result.get("success"):
                purchase = result.get("purchase", {})
                if purchase.get("refunded"):
                    return False, "License has been refunded"
                if purchase.get("disputed"):
                    return False, "License is disputed"

                uses = result.get("uses", 0)
                return True, f"License valid (activation #{uses})"

            return False, result.get("message", "Invalid license key")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "Invalid license key"
        return False, f"License server error: HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Network error: {e.reason}"
    except json.JSONDecodeError:
        return False, "Invalid response from license server"
    except Exception as e:
        return False, f"Validation error: {e}"


def download_premium_binary(
    dest_dir: Path,
    version: str,
    local_mode: bool = False,
    local_repo_dir: Path | None = None,
) -> tuple[bool, str]:
    """Download premium binary from GitHub releases or copy from local dist."""
    import shutil

    binary_name = get_platform_binary_name()
    dest_path = dest_dir / "ccp-premium"

    if local_mode and local_repo_dir:
        source_path = local_repo_dir / "premium" / "dist" / binary_name
        if not source_path.exists():
            return False, f"Premium binary not found at {source_path}"

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)

            dest_path.chmod(dest_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            return True, str(dest_path)
        except Exception as e:
            return False, f"Copy error: {e}"

    url = f"https://github.com/{GITHUB_REPO}/releases/download/{version}/{binary_name}"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "claude-codepro-installer/1.0"},
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(response.read())

            dest_path.chmod(dest_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            return True, str(dest_path)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "Premium binary not found (release may not exist yet)"
        return False, f"Download failed: HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Network error: {e}"
    except Exception as e:
        return False, f"Download error: {e}"


def save_license_to_env(project_dir: Path, license_key: str) -> None:
    """Save license key to .env file."""
    _save_env_var(project_dir, "CCP_LICENSE_KEY", license_key)


def save_gemini_key_to_env(project_dir: Path, gemini_key: str) -> None:
    """Save Gemini API key to .env file."""
    _save_env_var(project_dir, "GEMINI_API_KEY", gemini_key)


def _save_env_var(project_dir: Path, var_name: str, value: str) -> None:
    """Save an environment variable to .env file."""
    env_file = project_dir / ".env"

    existing_lines: list[str] = []
    if env_file.exists():
        existing_lines = env_file.read_text().splitlines()

    filtered_lines = [line for line in existing_lines if not line.startswith(f"{var_name}=")]

    filtered_lines.append(f"{var_name}={value}")

    env_file.write_text("\n".join(filtered_lines) + "\n")


def remove_premium_hooks_from_settings(settings_file: Path) -> bool:
    """Remove all premium hooks from settings.local.json for non-premium users.

    Removes ccp-premium hooks from:
    - PreToolUse (tdd-enforcer)
    - PostToolUse (context-monitor)
    - Stop (rules-hook)
    """
    if not settings_file.exists():
        return False

    try:
        settings = json.loads(settings_file.read_text())

        if "hooks" not in settings:
            return True

        # Remove premium hooks from all hook types
        for hook_type in ["PreToolUse", "PostToolUse", "Stop"]:
            if hook_type in settings["hooks"]:
                settings["hooks"][hook_type] = [
                    hook_group
                    for hook_group in settings["hooks"][hook_type]
                    if not any("ccp-premium" in h.get("command", "") for h in hook_group.get("hooks", []))
                ]
                # Remove empty hook arrays
                if not settings["hooks"][hook_type]:
                    del settings["hooks"][hook_type]

        # Remove hooks key if empty
        if not settings["hooks"]:
            del settings["hooks"]

        settings_file.write_text(json.dumps(settings, indent=2) + "\n")
        return True
    except (json.JSONDecodeError, OSError):
        return False


def prompt_for_premium(non_interactive: bool, project_dir: Path | None = None) -> str | None:
    """Prompt user for premium license key."""
    from lib import ui

    license_key = os.getenv("CCP_LICENSE_KEY")
    if license_key:
        ui.print_status("Found license key in CCP_LICENSE_KEY environment variable")
        return license_key

    if project_dir:
        env_file = project_dir / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("CCP_LICENSE_KEY="):
                    license_key = line.split("=", 1)[1].strip()
                    if license_key:
                        ui.print_status("Found license key in .env file")
                        return license_key

    if non_interactive:
        return None

    print("")
    print(f"{ui.BLUE}━━━ Premium Features ━━━{ui.NC}")
    print("")
    print("Claude CodePro Premium includes:")
    print("  • Advanced context monitoring (warns before hitting limits)")
    print("  • Priority support")
    print("  • Future premium features")
    print("")
    print(f"Get a license at: {ui.BLUE}https://premium.claude-code.pro{ui.NC}")
    print("")

    has_license = input("Do you have a premium license key? (y/N): ").strip()
    if has_license.lower() not in ["y", "yes"]:
        return None

    for attempt in range(3):
        license_key = input("Enter your license key: ").strip()
        if not license_key:
            return None

        ui.print_status("Validating license key...")
        valid, message = validate_license_key(license_key)

        if valid:
            ui.print_success(message)
            return license_key

        ui.print_error(f"License validation failed: {message}")
        if attempt < 2:
            retry = input("Try again? (y/N): ").strip()
            if retry.lower() not in ["y", "yes"]:
                return None

    return None


def prompt_for_gemini_key(non_interactive: bool, project_dir: Path | None = None) -> str | None:
    """Prompt user for Gemini API key for Rules Supervisor feature."""
    from lib import ui

    # Check environment variable first
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        ui.print_status("Found Gemini API key in GEMINI_API_KEY environment variable")
        return gemini_key

    # Check .env file
    if project_dir:
        env_file = project_dir / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    gemini_key = line.split("=", 1)[1].strip()
                    if gemini_key:
                        ui.print_status("Found Gemini API key in .env file")
                        return gemini_key

    if non_interactive:
        return None

    print("")
    print(f"{ui.BLUE}━━━ Rules Supervisor (Gemini API) ━━━{ui.NC}")
    print("")
    print("The Rules Supervisor uses Gemini 3.0 Pro to analyze your coding sessions")
    print("against project rules. This feature requires a Gemini API key.")
    print("")
    print("  • Cost: Very low (~$0.01 per session analysis)")
    print("  • Model: Gemini 3.0 Pro (fast, accurate)")
    print("")
    print(f"Get your API key at: {ui.BLUE}https://aistudio.google.com/apikey{ui.NC}")
    print("")

    setup_gemini = input("Do you want to configure the Gemini API key? (y/N): ").strip()
    if setup_gemini.lower() not in ["y", "yes"]:
        ui.print_warning("Rules Supervisor will be disabled without Gemini API key")
        return None

    gemini_key = input("Enter your Gemini API key: ").strip()
    if not gemini_key:
        ui.print_warning("No key entered. Rules Supervisor will be disabled.")
        return None

    return gemini_key


def install_premium_with_key(
    project_dir: Path,
    license_key: str,
    version: str,
    local_mode: bool = False,
    local_repo_dir: Path | None = None,
    skip_validation: bool = False,
    non_interactive: bool = False,
) -> bool:
    """Install premium features with a pre-validated license key."""
    from lib import ui

    if not skip_validation:
        ui.print_status("Validating license key...")
        valid, message = validate_license_key(license_key)

        if not valid:
            ui.print_error(f"License validation failed: {message}")
            return False

        ui.print_success(message)

    save_license_to_env(project_dir, license_key)
    ui.print_success("Saved license key to .env")

    if local_mode:
        ui.print_status("Copying premium binary from local dist...")
    else:
        ui.print_status(f"Downloading premium binary ({version})...")

    bin_dir = project_dir / ".claude" / "bin"
    success, result = download_premium_binary(bin_dir, version, local_mode, local_repo_dir)

    if not success:
        ui.print_error(f"{'Copy' if local_mode else 'Download'} failed: {result}")
        ui.print_warning("Premium features will not be available")
        return False

    binary_path = Path(result)
    ui.print_success(f"Installed premium binary to {binary_path}")

    # Prompt for Gemini API key for Rules Supervisor
    gemini_key = prompt_for_gemini_key(non_interactive, project_dir)
    if gemini_key:
        save_gemini_key_to_env(project_dir, gemini_key)
        ui.print_success("Saved Gemini API key to .env")

    ui.print_success("Premium hooks enabled (from template)")

    return True
