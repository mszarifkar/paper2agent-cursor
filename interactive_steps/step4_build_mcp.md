# Step 4: Build MCP Server

## Context

This step creates a unified MCP server that integrates all extracted tools into a single, well-structured interface. The server imports all tool modules and mounts them to provide unified access to all tutorial functionalities.

## Prerequisites

- Step 3 completed successfully
- `src/tools/[tutorial_name].py` files exist for all tutorials
- All tool modules have FastMCP instances
- `[REPO_NAME]-env` environment has fastmcp installed

## Cursor Composer Prompt

Copy and paste this prompt into Cursor Composer:

```
I'm building an MCP toolsuit for [REPO_NAME]. Please help me with Step 4: Build MCP Server.

## Input Files

- Tool modules: `src/tools/*.py`
- Repository name: `[REPO_NAME]`

## Task: Create Unified MCP Server

Follow the instructions from `prompts/step4_prompt.md`:

### Step 1: Discover Tool Modules

1. **Scan Tools Directory**:
   - List all `.py` files in `src/tools/`
   - Extract module names (without .py extension)
   - Verify each module can be imported

2. **Analyze Tool Modules**:
   - For each module, identify:
     - Tool names and descriptions
     - FastMCP instance name (usually `[tutorial_name]_mcp`)
   - Extract tool descriptions for documentation

### Step 2: Generate MCP Server

Create `src/[REPO_NAME]_mcp.py` following this exact template:

```python
"""
Model Context Protocol (MCP) for [REPO_NAME]

[Three-sentence description of codebase functionality]

This MCP Server contains tools extracted from the following tutorial files:
1. [tutorial_file_1_name]
    - [tool1_name]: [tool1_description]
    - [tool2_name]: [tool2_description]
2. [tutorial_file_2_name]
    - [tool1_name]: [tool1_description]
    ...
"""

from fastmcp import FastMCP

# Import statements (alphabetical order)
from tools.tutorial_file_1_name import tutorial_file_1_name_mcp
from tools.tutorial_file_2_name import tutorial_file_2_name_mcp
# ... add all tool modules

# Server definition and mounting
mcp = FastMCP(name="[REPO_NAME]")
mcp.mount(tutorial_file_1_name_mcp)
mcp.mount(tutorial_file_2_name_mcp)
# ... mount all tool modules

if __name__ == "__main__":
    mcp.run()
```

### Step 3: Validation

1. **Import Verification**:
   - Test imports: `python -c "import sys; sys.path.insert(0, 'src'); from tools.[tutorial_name] import [tutorial_name]_mcp"`
   - Verify all modules import successfully
   - Fix any import errors
   - Note: Imports use `from tools.` not `from src.tools.` because the server file is in `src/` directory

2. **Server Execution Test**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   python src/[REPO_NAME]_mcp.py
   ```
   - Server should start without errors
   - Verify all tools are mounted

3. **Documentation**:
   - Ensure docstring lists all tutorials and tools
   - Verify tool descriptions are accurate

## Expected Outputs

- `src/[REPO_NAME]_mcp.py` - Unified MCP server file

## Success Criteria

- [ ] All tool modules discovered and analyzed
- [ ] MCP server file created following exact template
- [ ] All tool modules imported successfully
- [ ] All tools mounted to server
- [ ] Server executes without errors
- [ ] Documentation accurately reflects available tools
```

**Replace `[REPO_NAME]` with your actual repository name** (e.g., `panpipes`)

## Expected Outputs

After executing this step, you should have:

1. **`src/[REPO_NAME]_mcp.py`**
   - Unified MCP server file
   - Imports all tool modules
   - Mounts all FastMCP instances
   - Comprehensive docstring listing all tools

## Validation

To verify this step completed successfully:

1. **Check Server File**:
   ```bash
   # Verify file exists
   ls src/[REPO_NAME]_mcp.py
   
   # Check imports
   python -c "import sys; sys.path.insert(0, 'src'); from [REPO_NAME]_mcp import mcp"
   ```

2. **Test Server Execution**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   python src/[REPO_NAME]_mcp.py
   ```
   - Server should start and wait for connections
   - No import or execution errors

3. **Verify Tool Mounting**:
   - Check that all tool modules are imported
   - Verify all FastMCP instances are mounted
   - Review docstring for completeness

## Troubleshooting

### Import Errors

**Problem**: Module import fails
- **Solution**: Check module name matches file name
- **Solution**: Verify FastMCP instance name in tool module
- **Solution**: Ensure `src/tools/` is in Python path
- **Solution**: Check for circular imports

**Problem**: FastMCP instance not found
- **Solution**: Verify instance is created at end of tool module
- **Solution**: Check instance name matches import statement
- **Solution**: Ensure instance is exported (not inside function)

### Server Execution Issues

**Problem**: Server fails to start
- **Solution**: Check all imports are correct
- **Solution**: Verify fastmcp is installed in environment
- **Solution**: Review error messages for specific issues

**Problem**: Tools not accessible
- **Solution**: Verify all modules are mounted
- **Solution**: Check tool decorators are correct
- **Solution**: Test individual tool modules first

### Template Compliance

**Problem**: Server doesn't follow template
- **Solution**: Use exact template structure provided
- **Solution**: No additions beyond specified template
- **Solution**: Import order should be alphabetical

## Next Steps

Once Step 4 is complete:
- Proceed to [Step 5: Coverage & Quality Reports](step5_coverage_quality.md)
- Test MCP server with a client if desired
- Prepare for deployment or sharing

