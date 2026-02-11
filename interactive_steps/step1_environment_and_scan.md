# Step 1: Environment Setup & Tutorial Discovery

## Context

This step sets up the Python environment and discovers all tutorials in the repository. It runs two tasks in parallel:
1. **Environment Setup**: Creates a Python virtual environment with all required dependencies
2. **Tutorial Scanning**: Identifies and classifies all tutorial files in the repository

## Prerequisites

- Repository cloned to `repo/[repo_name]/`
- Project directory structure created (use `scripts/03_prepare_folders.sh` if needed)
- Python 3.10+ available on your system

## Cursor Composer Prompt

Copy and paste this prompt into Cursor Composer:

```
I'm building an MCP toolsuit for [REPO_NAME]. Please help me with Step 1: Environment Setup & Tutorial Discovery.

## Task 1: Environment Setup

Set up a Python environment named "[REPO_NAME]-env" with Python ≥3.10 in the current working directory.

Follow the instructions from `agents/environment-python-manager.md`:
- Use uv or venv to create the environment
- Search the repository for installation instructions (prioritize PyPI installations)
- Install all dependencies from pyproject.toml, requirements.txt, or setup.py
- Install pytest and testing infrastructure
- Create `reports/environment-manager_results.md` with:
  - Environment name and Python version
  - Installation method used
  - List of installed packages
  - Activation command: `source [REPO_NAME]-env/bin/activate`
  - Any issues encountered and resolutions

## Task 2: Tutorial Scanning

Scan the repository at `repo/[REPO_NAME]/` for tutorials.

Follow the instructions from `agents/tutorial-scanner.md`:
- Start with `docs/**` directory if it exists (authoritative content)
- Look for `.ipynb`, `.md` files (prioritize docs/ directory)
- Exclude `templates/`, legacy, deprecated files
- Only include Python scripts (.py) if no .ipynb or .md tutorials exist
- Apply strict filtering criteria:
  - Runnable and self-contained
  - Clear input/output definition
  - Reusable functionality
  - Non-trivial capability
  - Documentation and narrative context
- Create `reports/tutorial-scanner.json` with ALL tutorials found
- Create `reports/tutorial-scanner-include-in-tools.json` with ONLY tutorials marked "include-in-tools": true

For each tutorial, include:
- path: relative path from repository root
- title: title of the tutorial
- description: 3-sentence summary
- type: notebook|script|markdown|documentation
- include_in_tools: boolean
- reason_for_include_or_exclude: 1-2 line explanation

## Expected Outputs

After completion, verify these files exist:
- `reports/environment-manager_results.md`
- `reports/tutorial-scanner.json`
- `reports/tutorial-scanner-include-in-tools.json`

## Success Criteria

- [ ] Environment created successfully with Python ≥3.10
- [ ] All dependencies installed
- [ ] Tutorial scanning completed
- [ ] JSON files created with valid structure
- [ ] No legacy/deprecated content marked as "include-in-tools"
```

**Replace `[REPO_NAME]` with your actual repository name** (e.g., `panpipes`)

## Expected Outputs

After executing this step, you should have:

1. **`reports/environment-manager_results.md`**
   - Environment name and Python version
   - Installation method
   - Package list
   - Activation instructions

2. **`reports/tutorial-scanner.json`**
   - Complete list of all tutorials found
   - Includes both included and excluded tutorials
   - Metadata for each tutorial

3. **`reports/tutorial-scanner-include-in-tools.json`**
   - Filtered list of tutorials to include in tools
   - Only tutorials marked `"include_in_tools": true`

## Validation

To verify this step completed successfully:

1. **Check Environment**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   python --version  # Should be ≥3.10
   ```

2. **Check JSON Files**:
   ```bash
   # Verify files exist and are valid JSON
   python -m json.tool reports/tutorial-scanner.json > /dev/null
   python -m json.tool reports/tutorial-scanner-include-in-tools.json > /dev/null
   ```

3. **Review Tutorial List**:
   - Open `reports/tutorial-scanner-include-in-tools.json`
   - Verify tutorials are appropriate for tool extraction
   - Check that no deprecated/legacy files are included

## Troubleshooting

### Environment Setup Issues

**Problem**: Environment creation fails
- **Solution**: Try different Python versions (3.10, 3.11, 3.12)
- **Solution**: Check if `uv` is installed: `pip install uv`
- **Solution**: Use `venv` as fallback: `python3 -m venv [REPO_NAME]-env`

**Problem**: Dependencies fail to install
- **Solution**: Check repository README for specific installation instructions
- **Solution**: Try installing from PyPI first, then git URLs
- **Solution**: Install dependencies incrementally to identify problematic packages

### Tutorial Scanning Issues

**Problem**: No tutorials found
- **Solution**: Check if repository uses different directory structure
- **Solution**: Verify you're scanning `repo/[REPO_NAME]/` not the project root
- **Solution**: Look for tutorials in alternative locations (examples/, notebooks/, docs/)

**Problem**: Too many/few tutorials included
- **Solution**: Review `reports/tutorial-scanner.json` to see all tutorials
- **Solution**: Manually edit `reports/tutorial-scanner-include-in-tools.json` if needed
- **Solution**: Check tutorial quality criteria in `agents/tutorial-scanner.md`

## Next Steps

Once Step 1 is complete:
- Proceed to [Step 2: Execute Tutorials](step2_execute_tutorials.md)
- Ensure `reports/tutorial-scanner-include-in-tools.json` contains the tutorials you want to process



