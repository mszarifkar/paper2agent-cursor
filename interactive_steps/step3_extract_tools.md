# Step 3: Extract Tools & Create Tests

## Context

This step extracts reusable tools from executed tutorials and creates comprehensive test suites. Each tutorial file is processed to create production-ready Python modules with MCP tool decorators, followed by individual test files for each tool function.

## Prerequisites

- Step 2 completed successfully
- `reports/executed_notebooks.json` exists
- `notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb` files exist
- `[REPO_NAME]-env` environment is set up

## Cursor Composer Prompt

Copy and paste this prompt into Cursor Composer:

```
I'm building an MCP toolsuit for [REPO_NAME]. Please help me with Step 3: Extract Tools & Create Tests.

## Input Files

- Executed tutorials: `reports/executed_notebooks.json`
- Execution notebooks: `notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb`
- Environment: `[REPO_NAME]-env`

## Phase 1: Tool Extraction

For each tutorial file in `executed_notebooks.json`, extract tools following instructions from `agents/tutorial-tool-extractor-implementor.md`:

### For Each Tutorial File:

1. **Read Tutorial Content**:
   - Read the execution notebook: `notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb`
   - Identify all tutorial sections (by headings/markers)
   - Extract code from each section

2. **Create Tool Module**:
   - Create `src/tools/[tutorial_name].py`
   - Extract ALL tutorial sections from the same source file into this single file
   - Each section becomes one tool function
   - Follow naming convention: `library_action_target` (e.g., `scanpy_cluster_cells`)
   - Preserve exact tutorial structure - no generalized patterns
   - NEVER add parameters not in original tutorial
   - Use `@[tutorial_name]_mcp.tool` decorator for each function

3. **Tool Requirements**:
   - Runnable and self-contained
   - Accept user-provided inputs (no hardcoded values)
   - Clear input/output definition
   - Reusable functionality
   - Non-trivial capability
   - Production-quality code

4. **Create MCP Instance**:
   - At end of file, create: `[tutorial_name]_mcp = FastMCP(name="[tutorial_name]")`
   - Register all tools with this instance

5. **Code Validation**:
   - Validate generated code with `ast.parse()` before saving
   - Ensure proper Python formatting:
     - Use actual newlines in return statements (not literal `\`n` strings)
     - Exactly 2 newlines between function definitions
     - Proper indentation (4 spaces)
   - Fix any syntax errors before saving

6. **MCP Compliance**:
   - Check all tool names are ≤ 128 characters
   - Detect duplicate tool names across modules
   - Add module prefix to duplicates if needed
   - Generate compliance report

7. **Personal Information Sanitization**:
   - After code extraction, sanitize all generated files:
     ```bash
     python tools/personal_info_sanitizer.py src/tools/ --recursive --report
     ```
   - This removes/replaces:
     - User-specific file paths (C:\Users\..., /home/...)
     - Email addresses
     - Usernames
     - API keys/tokens
     - IP addresses (except localhost)
   - Review sanitization report to verify no personal info remains

### Critical Rules:
- NEVER add function parameters not in original tutorial
- PRESERVE exact tutorial structure - no generalized patterns
- Basic input file validation only
- Extract ALL tutorial sections from same source file into single output file
- Order tools same as sections in tutorial
- **Code Formatting**: Use actual newlines (not `\`n` strings), 2 newlines between functions
- **Syntax Validation**: Validate all code with `ast.parse()` before saving

## Phase 2: Test Creation

For each tutorial file that completed extraction, create tests following instructions from `agents/test-verifier-improver.md`:

### For Each Tool Function:

1. **Sequential Processing**:
   - Process tools ONE AT A TIME in tutorial order
   - Tool N+1 test creation begins only after Tool N test passes completely

2. **Create Test File**:
   - Create `tests/code/[tutorial_name]/[tool_name]_test.py` for each decorated function
   - Use exact tutorial examples verbatim
   - Copy exact parameter values, function signatures
   - Add numerical assertions (max 6 per test)

3. **Test Requirements**:
   - Use tutorial examples exactly - no simplification
   - Use real data from tutorial (never mock data)
   - Verify numerical outputs precisely
   - Test file creation when tutorial creates files
   - Verify data structures (shapes, types)

4. **Run Tests**:
   - Activate environment: `source [REPO_NAME]-env/bin/activate`
   - Run: `pytest tests/code/[tutorial_name]/[tool_name]_test.py -v`
   - Fix errors iteratively (up to 6 attempts per function)
   - If test cannot pass after 6 attempts, remove decorator from function

5. **Create Test Logs**:
   - Create `tests/logs/[tutorial_name]_[tool_name]_test.log` for each tool
   - Document test execution results
   - Create final summary: `tests/logs/[tutorial_name]_test.md`

### Test Structure:
```python
import pytest
from src.tools.[tutorial_name] import [tool_name]

def test_[tool_name]():
    # Use exact tutorial examples
    result = [tool_name](...)
    # Assertions based on tutorial outputs
    assert result == expected_value
```

## Expected Outputs

- `src/tools/[tutorial_name].py` - Tool module for each tutorial file
- `tests/code/[tutorial_name]/[tool_name]_test.py` - Individual test file for each tool
- `tests/data/[tutorial_name]/` - Test data fixtures if needed
- `tests/logs/[tutorial_name]_test.md` - Test summary for each tutorial

## Success Criteria

- [ ] All tutorial files converted to tool modules
- [ ] Each decorated function has corresponding test file
- [ ] All tests pass (or decorators removed after 6 attempts)
- [ ] Tutorial fidelity preserved (exact function calls, no added parameters)
- [ ] Test logs created with execution results
```

**Replace `[REPO_NAME]` with your actual repository name** (e.g., `panpipes`)

## Expected Outputs

After executing this step, you should have:

1. **`src/tools/[tutorial_name].py`**
   - Production-ready tool modules
   - Each tutorial file becomes one Python module
   - All tools decorated with `@[tutorial_name]_mcp.tool`
   - FastMCP instance created at end of file

2. **`tests/code/[tutorial_name]/[tool_name]_test.py`**
   - Individual test file for each tool function
   - Tests use exact tutorial examples
   - All tests pass successfully

3. **`tests/logs/[tutorial_name]_test.md`**
   - Summary of test execution
   - List of passing/failing tests
   - Any issues encountered

## Validation

To verify this step completed successfully:

1. **Check Tool Modules**:
   ```bash
   # Verify tool files exist
   ls src/tools/*.py
   
   # Count decorated functions
   grep -r "@.*_mcp.tool" src/tools/
   ```

2. **Run All Tests**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   pytest tests/code/ -v
   ```

3. **Verify Test Coverage**:
   - Each decorated function should have a test file
   - Check test logs for any failures

## Troubleshooting

### Code Generation Issues

**Problem**: Syntax errors in generated code
- **Solution**: Validate code with `ast.parse()` before saving
- **Solution**: Check for literal `\`n` strings in return statements - replace with actual newlines
- **Solution**: Ensure proper newline separation (2 newlines) between functions
- **Solution**: Run `python tools/code_postprocessor.py src/tools/` to fix formatting

**Problem**: Missing imports causing NameError
- **Solution**: Use AST to detect all used symbols
- **Solution**: Check for common patterns: `plt` → `import matplotlib.pyplot as plt`, `np` → `import numpy as np`
- **Solution**: Add missing imports at module level

**Problem**: Undefined variables in generated code
- **Solution**: Track variable dependencies across notebook cells
- **Solution**: Include required initialization code from earlier cells
- **Solution**: Verify all variables are either imported or defined in function

**Problem**: Papermill error cells in generated code
- **Solution**: Run `python tools/preprocess_notebook.py` to clean notebooks before extraction
- **Solution**: Check for HTML tags and error markers in code
- **Solution**: Remove cells containing `papermill-error-cell` markers

### Tool Extraction Issues

**Problem**: Tools don't match tutorial exactly
- **Solution**: Review tutorial code carefully
- **Solution**: Ensure no parameters are added
- **Solution**: Preserve exact data structures from tutorial

**Problem**: Multiple tutorials in one file
- **Solution**: Extract all sections into single `src/tools/[tutorial_name].py`
- **Solution**: Each section becomes one tool function
- **Solution**: Maintain order from tutorial

**Problem**: Tool names exceed 128 characters
- **Solution**: Shorten tool names while preserving meaning
- **Solution**: Check MCP compliance: `grep -r "@.*_mcp.tool" src/tools/ | grep -oP 'def \K\w+' | while read name; do [ ${#name} -gt 128 ] && echo "$name"; done`
- **Solution**: Use abbreviations for common terms

**Problem**: Duplicate tool names across modules
- **Solution**: Add module prefix to duplicate names
- **Solution**: Check for duplicates: `grep -r "@.*_mcp.tool" src/tools/ | grep -oP 'def \K\w+' | sort | uniq -d`

### Personal Information Issues

**Problem**: Personal information in generated code
- **Solution**: Run sanitization: `python tools/personal_info_sanitizer.py src/tools/ --recursive --report`
- **Solution**: Review sanitization report to verify removals
- **Solution**: Check for user paths, emails, usernames, API keys, IP addresses
- **Solution**: Configure custom patterns in `.paper2agent-sanitize.yaml` if needed

### Test Issues

**Problem**: Tests fail with tutorial data
- **Solution**: Verify data files exist and paths are correct
- **Solution**: Check data format matches tutorial expectations
- **Solution**: Review execution notebook for data processing steps

**Problem**: Sequential dependencies not working
- **Solution**: Ensure tests run in order (Tool 1 → Tool 2 → Tool N)
- **Solution**: Tool N+1 can reference Tool N outputs
- **Solution**: Use pytest ordering or run tests sequentially

**Problem**: Test cannot pass after 6 attempts
- **Solution**: Remove `@tool` decorator from function
- **Solution**: Document reason in test log
- **Solution**: Continue with other tools

## Next Steps

Once Step 3 is complete:
- Proceed to [Step 4: Build MCP Server](step4_build_mcp.md)
- Ensure all tools are properly decorated
- Verify tests pass successfully



