#!/usr/bin/env python3
"""
Code post-processing utility for paper2agent-cursor.

Validates syntax, normalizes formatting, sorts imports, and ensures code quality.
"""

import ast
import sys
import re
from pathlib import Path
from typing import List, Tuple


def validate_syntax(code: str, file_path: str) -> Tuple[bool, str]:
    """
    Validate Python syntax using AST parsing.
    
    Returns:
        (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error in {file_path}: {e.msg} at line {e.lineno}"


def fix_return_statements(code: str) -> str:
    """
    Fix malformed return statements with literal `\`n` strings.
    """
    # Replace literal `\`n` with actual newlines
    code = re.sub(r'`n', '\n', code)
    # Replace `\\n` with actual newlines
    code = re.sub(r'\\n', '\n', code)
    return code


def normalize_newlines(code: str) -> str:
    """
    Normalize newlines and ensure proper spacing between functions.
    """
    # Normalize line endings
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    
    # Ensure exactly 2 newlines between function definitions
    # Pattern: closing brace/bracket followed by decorator or def
    code = re.sub(r'}\n+@', r'}\n\n@', code)
    code = re.sub(r'}\n+def ', r'}\n\ndef ', code)
    
    # Remove excessive newlines (more than 2)
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    return code


def sort_imports(code: str) -> str:
    """
    Sort imports alphabetically within import groups.
    """
    lines = code.split('\n')
    import_lines = []
    other_lines = []
    in_imports = False
    import_group = []
    
    for line in lines:
        stripped = line.strip()
        # Check if this is an import line
        if stripped.startswith('import ') or stripped.startswith('from '):
            if not in_imports:
                in_imports = True
            import_group.append(line)
        else:
            if in_imports and import_group:
                # Sort the import group
                import_group.sort()
                import_lines.extend(import_group)
                import_lines.append('')  # Add blank line after imports
                import_group = []
                in_imports = False
            other_lines.append(line)
    
    # Handle remaining imports at end
    if import_group:
        import_group.sort()
        import_lines.extend(import_group)
    
    # Combine: imports first, then other code
    result = '\n'.join(import_lines + other_lines)
    return result


def format_code(code: str) -> str:
    """
    Apply consistent code formatting.
    """
    # Fix return statements
    code = fix_return_statements(code)
    
    # Normalize newlines
    code = normalize_newlines(code)
    
    # Sort imports
    code = sort_imports(code)
    
    return code


def process_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Process a single Python file.
    
    Returns:
        (success, list_of_issues)
    """
    issues = []
    
    try:
        # Read file
        code = file_path.read_text(encoding='utf-8')
        
        # Validate syntax
        is_valid, error_msg = validate_syntax(code, str(file_path))
        if not is_valid:
            issues.append(error_msg)
            return False, issues
        
        # Format code
        formatted_code = format_code(code)
        
        # Validate formatted code
        is_valid, error_msg = validate_syntax(formatted_code, str(file_path))
        if not is_valid:
            issues.append(f"Formatted code has syntax errors: {error_msg}")
            return False, issues
        
        # Write back if changed
        if formatted_code != code:
            file_path.write_text(formatted_code, encoding='utf-8')
            issues.append("Code formatted and updated")
        
        return True, issues
        
    except Exception as e:
        issues.append(f"Error processing {file_path}: {e}")
        return False, issues


def process_directory(directory: Path) -> dict:
    """
    Process all Python files in a directory recursively.
    
    Returns:
        Dictionary with processing results
    """
    results = {
        'processed': 0,
        'succeeded': 0,
        'failed': 0,
        'issues': []
    }
    
    for py_file in directory.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue  # Skip __init__.py files
        
        results['processed'] += 1
        success, issues = process_file(py_file)
        
        if success:
            results['succeeded'] += 1
        else:
            results['failed'] += 1
        
        if issues:
            results['issues'].extend([f"{py_file}: {issue}" for issue in issues])
    
    return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Post-process generated Python code: validate syntax, format, sort imports"
    )
    parser.add_argument(
        'target',
        help='Python file or directory to process'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Process directory recursively'
    )
    
    args = parser.parse_args()
    
    target = Path(args.target)
    
    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)
    
    if target.is_file():
        if target.suffix != '.py':
            print(f"Error: {target} is not a Python file", file=sys.stderr)
            sys.exit(1)
        
        success, issues = process_file(target)
        if success:
            print(f"✓ Processed {target}")
            if issues:
                for issue in issues:
                    print(f"  - {issue}")
        else:
            print(f"✗ Failed to process {target}", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            sys.exit(1)
    
    elif target.is_dir():
        results = process_directory(target)
        print(f"\nProcessing Summary:")
        print(f"  Processed: {results['processed']} files")
        print(f"  Succeeded: {results['succeeded']}")
        print(f"  Failed: {results['failed']}")
        
        if results['issues']:
            print(f"\nIssues found:")
            for issue in results['issues']:
                print(f"  - {issue}")
        
        if results['failed'] > 0:
            sys.exit(1)
    
    else:
        print(f"Error: {target} is not a file or directory", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

