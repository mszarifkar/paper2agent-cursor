# Security & Privacy: Personal Information Sanitization

## Overview

Paper2Agent-Cursor includes automatic sanitization of personal information to prevent privacy leaks and security risks in generated code. This document describes the sanitization process and how to configure it.

## What Gets Sanitized

The following types of personal information are automatically detected and removed/replaced:

1. **User-Specific File Paths**
   - Windows: `C:\Users\[username]\...` → `[PROJECT_ROOT]/...`
   - Unix: `/home/[username]/...` → `[PROJECT_ROOT]/...`
   - User profile paths: `C:\Users\[username]` → `[PROJECT_ROOT]`

2. **Email Addresses**
   - Pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Replacement: `[EMAIL_REMOVED]` (configurable)

3. **Usernames**
   - In paths: `/home/[username]`, `C:\Users\[username]`
   - In comments: `@username`, `user: username`
   - Replacement: `[USER]` (configurable)

4. **API Keys & Tokens**
   - Long alphanumeric strings (>40 chars)
   - OpenAI-style keys: `sk-[a-zA-Z0-9]{32,}`
   - Replacement: `[API_KEY_REMOVED]` (configurable)

5. **IP Addresses**
   - IPv4 addresses (except localhost: 127.0.0.1, 0.0.0.0)
   - Replacement: `[IP_ADDRESS]` (configurable)

## When Sanitization Runs

Sanitization is integrated at three points in the workflow:

1. **Step 2 (Notebook Preprocessing)**: Before executing notebooks
   - Run: `python tools/preprocess_notebook.py` (includes error cell removal)
   - Run: `python tools/personal_info_sanitizer.py notebooks/[tutorial_name]/[tutorial_name]_execution.ipynb`

2. **Step 3 (Code Extraction)**: During tool extraction
   - Automatic sanitization instructions in agent prompts

3. **Step 3 (Post-Processing)**: After code generation
   - Run: `python tools/personal_info_sanitizer.py src/tools/ --recursive --report`

## Configuration

### Default Behavior

By default, all sanitization is enabled with standard replacements. No configuration file is required.

### Custom Configuration

Create `.paper2agent-sanitize.yaml` in your project root to customize sanitization:

```yaml
sanitize:
  paths:
    enabled: true
    replacement: "[PROJECT_ROOT]"
  emails:
    enabled: true
    replacement: "[EMAIL_REMOVED]"
  usernames:
    enabled: true
    replacement: "[USER]"
  api_keys:
    enabled: true
    replacement: "[API_KEY_REMOVED]"
  ip_addresses:
    enabled: true
    replacement: "[IP_ADDRESS]"
  custom_patterns:
    - pattern: "your-custom-pattern"
      replacement: "[CUSTOM_REMOVED]"
```

### Disabling Sanitization

To disable specific sanitization types, set `enabled: false` in the config file:

```yaml
sanitize:
  emails:
    enabled: false  # Don't sanitize emails
```

## Usage

### Command Line

```bash
# Sanitize a single file
python tools/personal_info_sanitizer.py src/tools/example.py

# Sanitize directory recursively
python tools/personal_info_sanitizer.py src/tools/ --recursive

# Generate sanitization report
python tools/personal_info_sanitizer.py src/tools/ --recursive --report
```

### Integration in Workflow

Sanitization is automatically integrated into Step 2 and Step 3 workflows. Manual execution is only needed if you want to re-sanitize existing code.

## What Gets Preserved

The following are **NOT** sanitized (preserved as-is):

- Relative paths within project: `data/file.csv`, `../data/file.csv`
- Generic example paths: `/path/to/data`, `data/file.csv`
- Library-specific data paths: `sc.datasets.pbmc68k_reduced()`
- Localhost IP addresses: `127.0.0.1`, `localhost`, `0.0.0.0`
- Common words: `user`, `admin`, `root` (when standalone)

## Sanitization Report

When using `--report` flag, a sanitization report is generated listing all replacements made:

```
Personal Information Sanitization Report
==================================================

Path: C:\Users\username\Desktop\project -> [PROJECT_ROOT]
Email: user@example.com -> [EMAIL_REMOVED]
API Key: sk-abc123... -> [API_KEY_REMOVED]
```

## Best Practices

1. **Review Reports**: Always review sanitization reports to verify removals
2. **Test After Sanitization**: Verify code still works after sanitization
3. **Custom Patterns**: Add project-specific patterns to config if needed
4. **Version Control**: Don't commit sanitization config files with sensitive patterns
5. **Regular Checks**: Run sanitization before committing code

## Troubleshooting

**Problem**: Sanitization removes legitimate paths
- **Solution**: Use relative paths or generic placeholders in tutorials
- **Solution**: Configure custom patterns to preserve specific paths

**Problem**: Personal info still appears after sanitization
- **Solution**: Check sanitization report for what was replaced
- **Solution**: Add custom patterns for project-specific formats
- **Solution**: Verify sanitization ran on all files (`--recursive` flag)

**Problem**: Code breaks after sanitization
- **Solution**: Review replacements in sanitization report
- **Solution**: Ensure relative paths are used instead of absolute paths
- **Solution**: Test code after sanitization

## Security Considerations

- **Never commit** `.paper2agent-sanitize.yaml` if it contains sensitive patterns
- **Review** all generated code before publishing
- **Test** sanitization on sample code first
- **Report** any issues with sanitization patterns

## Related Tools

- `tools/preprocess_notebook.py` - Removes error cells and HTML tags
- `tools/code_postprocessor.py` - Validates syntax and formats code
- `tools/personal_info_sanitizer.py` - Sanitizes personal information

