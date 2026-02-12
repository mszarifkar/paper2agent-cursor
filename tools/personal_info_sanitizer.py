#!/usr/bin/env python3
"""
Personal information sanitization utility for paper2agent-cursor.

Detects and removes/replaces personal information from generated code:
- User-specific file paths
- Email addresses
- Usernames
- API keys/tokens
- IP addresses
"""

import re
import sys
import ast
from pathlib import Path
from typing import List, Dict, Tuple, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class PersonalInfoSanitizer:
    """Sanitize personal information from code."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize sanitizer with optional configuration."""
        self.config = self._load_config(config_path)
        self.replacements = []
        
    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Load configuration from YAML file or use defaults."""
        defaults = {
            'sanitize': {
                'paths': {'enabled': True, 'replacement': '[PROJECT_ROOT]'},
                'emails': {'enabled': True, 'replacement': '[EMAIL_REMOVED]'},
                'usernames': {'enabled': True, 'replacement': '[USER]'},
                'api_keys': {'enabled': True, 'replacement': '[API_KEY_REMOVED]'},
                'ip_addresses': {'enabled': True, 'replacement': '[IP_ADDRESS]'},
                'custom_patterns': []
            }
        }
        
        if config_path and config_path.exists():
            if not HAS_YAML:
                print(f"Warning: PyYAML not installed, using default config. Install with: pip install pyyaml", file=sys.stderr)
            else:
                try:
                    with open(config_path, 'r') as f:
                        user_config = yaml.safe_load(f)
                        # Merge with defaults
                        defaults.update(user_config)
                except Exception as e:
                    print(f"Warning: Could not load config from {config_path}: {e}", file=sys.stderr)
        
        return defaults
    
    def sanitize_paths(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize user-specific file paths."""
        if not self.config['sanitize']['paths']['enabled']:
            return text, []
        
        replacements = []
        replacement = self.config['sanitize']['paths']['replacement']
        
        # Windows paths: C:\Users\[username]\...
        pattern_windows = r'[C-Z]:\\Users\\[^\\]+\\[^\s\'"`\)]+'
        matches = re.findall(pattern_windows, text)
        for match in matches:
            if match not in [r[0] for r in replacements]:
                text = text.replace(match, replacement)
                replacements.append((match, replacement))
        
        # Unix paths: /home/[username]/... or ~[username]/...
        pattern_unix = r'(?:/home|~)/[^/\s\'"`\)]+/[^\s\'"`\)]+'
        matches = re.findall(pattern_unix, text)
        for match in matches:
            if match not in [r[0] for r in replacements]:
                text = text.replace(match, replacement)
                replacements.append((match, replacement))
        
        # Windows user profile: C:\Users\[username]
        pattern_user = r'[C-Z]:\\Users\\[^\\\s\'"`\)]+'
        matches = re.findall(pattern_user, text)
        for match in matches:
            if match not in [r[0] for r in replacements]:
                text = text.replace(match, replacement)
                replacements.append((match, replacement))
        
        return text, [f"Path: {old} -> {new}" for old, new in replacements]
    
    def sanitize_emails(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize email addresses."""
        if not self.config['sanitize']['emails']['enabled']:
            return text, []
        
        replacements = []
        replacement = self.config['sanitize']['emails']['replacement']
        
        # Email pattern
        pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        matches = re.findall(pattern, text)
        for match in matches:
            if match not in [r[0] for r in replacements]:
                text = re.sub(re.escape(match), replacement, text)
                replacements.append((match, replacement))
        
        return text, [f"Email: {old} -> {new}" for old, new in replacements]
    
    def sanitize_usernames(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize usernames in paths and comments."""
        if not self.config['sanitize']['usernames']['enabled']:
            return text, []
        
        replacements = []
        replacement = self.config['sanitize']['usernames']['replacement']
        
        # Extract username from paths (already handled by path sanitization)
        # This focuses on standalone username mentions in comments
        # Pattern: @username, user: username, etc.
        patterns = [
            r'@([a-zA-Z0-9_-]+)',  # @username
            r'user:\s*([a-zA-Z0-9_-]+)',  # user: username
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) > 2 and match not in ['user', 'admin', 'root']:  # Skip common words
                    if match not in [r[0] for r in replacements]:
                        text = re.sub(pattern.replace(r'([a-zA-Z0-9_-]+)', re.escape(match)), replacement, text)
                        replacements.append((match, replacement))
        
        return text, [f"Username: {old} -> {new}" for old, new in replacements]
    
    def sanitize_api_keys(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize API keys and tokens."""
        if not self.config['sanitize']['api_keys']['enabled']:
            return text, []
        
        replacements = []
        replacement = self.config['sanitize']['api_keys']['replacement']
        
        # Common API key patterns
        patterns = [
            r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API keys
            r'[a-zA-Z0-9]{32,}',  # Generic long alphanumeric strings (potential API keys)
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Skip if it's a hash or UUID (common in code)
                if len(match) > 40:  # Likely an API key if very long
                    if match not in [r[0] for r in replacements]:
                        text = re.sub(re.escape(match), replacement, text)
                        replacements.append((match, replacement))
        
        return text, [f"API Key: {old[:20]}... -> {new}" for old, new in replacements]
    
    def sanitize_ip_addresses(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize IP addresses (except localhost)."""
        if not self.config['sanitize']['ip_addresses']['enabled']:
            return text, []
        
        replacements = []
        replacement = self.config['sanitize']['ip_addresses']['replacement']
        
        # IPv4 pattern
        ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        matches = re.findall(ipv4_pattern, text)
        for match in matches:
            # Skip localhost addresses
            if match not in ['127.0.0.1', 'localhost', '0.0.0.0']:
                if match not in [r[0] for r in replacements]:
                    text = re.sub(re.escape(match), replacement, text)
                    replacements.append((match, replacement))
        
        return text, [f"IP Address: {old} -> {new}" for old, new in replacements]
    
    def sanitize_custom_patterns(self, text: str) -> Tuple[str, List[str]]:
        """Sanitize custom patterns from config."""
        replacements = []
        custom_patterns = self.config['sanitize'].get('custom_patterns', [])
        
        for pattern_config in custom_patterns:
            pattern = pattern_config.get('pattern', '')
            replacement = pattern_config.get('replacement', '[CUSTOM_REMOVED]')
            
            if pattern:
                matches = re.findall(pattern, text)
                for match in matches:
                    if match not in [r[0] for r in replacements]:
                        text = re.sub(re.escape(match), replacement, text)
                        replacements.append((match, replacement))
        
        return text, [f"Custom: {old} -> {new}" for old, new in replacements]
    
    def sanitize_code(self, code: str) -> Tuple[str, List[str]]:
        """Sanitize all personal information from code."""
        all_replacements = []
        
        # Sanitize in order
        code, replacements = self.sanitize_paths(code)
        all_replacements.extend(replacements)
        
        code, replacements = self.sanitize_emails(code)
        all_replacements.extend(replacements)
        
        code, replacements = self.sanitize_usernames(code)
        all_replacements.extend(replacements)
        
        code, replacements = self.sanitize_api_keys(code)
        all_replacements.extend(replacements)
        
        code, replacements = self.sanitize_ip_addresses(code)
        all_replacements.extend(replacements)
        
        code, replacements = self.sanitize_custom_patterns(code)
        all_replacements.extend(replacements)
        
        return code, all_replacements
    
    def sanitize_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Sanitize a single file."""
        try:
            code = file_path.read_text(encoding='utf-8')
            sanitized_code, replacements = self.sanitize_code(code)
            
            # Write back if changes were made
            if sanitized_code != code:
                file_path.write_text(sanitized_code, encoding='utf-8')
                return True, replacements
            else:
                return True, []
                
        except Exception as e:
            return False, [f"Error sanitizing {file_path}: {e}"]


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sanitize personal information from generated code"
    )
    parser.add_argument(
        'target',
        help='Python file or directory to sanitize'
    )
    parser.add_argument(
        '--config', '-c',
        type=Path,
        help='Path to sanitization config file (.paper2agent-sanitize.yaml)'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Process directory recursively'
    )
    parser.add_argument(
        '--report', '-R',
        action='store_true',
        help='Generate sanitization report'
    )
    
    args = parser.parse_args()
    
    target = Path(args.target)
    config_path = args.config or Path('.paper2agent-sanitize.yaml')
    
    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)
    
    sanitizer = PersonalInfoSanitizer(config_path)
    all_replacements = []
    
    if target.is_file():
        if target.suffix != '.py':
            print(f"Error: {target} is not a Python file", file=sys.stderr)
            sys.exit(1)
        
        success, replacements = sanitizer.sanitize_file(target)
        if success:
            print(f"✓ Sanitized {target}")
            if replacements:
                all_replacements.extend(replacements)
                for replacement in replacements:
                    print(f"  - {replacement}")
        else:
            print(f"✗ Failed to sanitize {target}", file=sys.stderr)
            for replacement in replacements:
                print(f"  - {replacement}", file=sys.stderr)
            sys.exit(1)
    
    elif target.is_dir():
        py_files = list(target.rglob('*.py')) if args.recursive else list(target.glob('*.py'))
        succeeded = 0
        failed = 0
        
        for py_file in py_files:
            if py_file.name == '__init__.py':
                continue
            
            success, replacements = sanitizer.sanitize_file(py_file)
            if success:
                succeeded += 1
                all_replacements.extend(replacements)
            else:
                failed += 1
        
        print(f"\nSanitization Summary:")
        print(f"  Processed: {len(py_files)} files")
        print(f"  Succeeded: {succeeded}")
        print(f"  Failed: {failed}")
        print(f"  Replacements made: {len(all_replacements)}")
        
        if args.report and all_replacements:
            report_path = target / 'sanitization_report.txt'
            with open(report_path, 'w') as f:
                f.write("Personal Information Sanitization Report\n")
                f.write("=" * 50 + "\n\n")
                for replacement in all_replacements:
                    f.write(f"{replacement}\n")
            print(f"\nReport saved to: {report_path}")
        
        if failed > 0:
            sys.exit(1)
    
    else:
        print(f"Error: {target} is not a file or directory", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

