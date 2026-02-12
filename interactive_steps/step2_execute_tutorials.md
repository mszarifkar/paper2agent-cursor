# Step 2: Execute Tutorials

## Context

This step executes all tutorials discovered in Step 1 to create validated, reproducible notebook executions. Each tutorial is run in the prepared environment, errors are resolved iteratively, and outputs (including figures) are extracted and preserved.

## Prerequisites

- Step 1 completed successfully
- `reports/tutorial-scanner-include-in-tools.json` exists
- `[REPO_NAME]-env` environment is set up and activated
- Repository cloned to `repo/[REPO_NAME]/`

## Cursor Composer Prompt

Copy and paste this prompt into Cursor Composer:

```
I'm building an MCP toolsuit for [REPO_NAME]. Please help me with Step 2: Execute Tutorials.

## Input Files

- Tutorial list: `reports/tutorial-scanner-include-in-tools.json`
- Environment: `[REPO_NAME]-env` (already set up)
- Repository: `repo/[REPO_NAME]/`

## Task: Execute All Tutorials

Follow the instructions from `agents/tutorial-executor.md` and `prompts/step2_prompt.md`:

### For Each Tutorial:

1. **Prepare Execution Notebook**:
   - If `.ipynb`: Copy to `notebooks/[tutorial_name]/[tutorial_name]_execution.ipynb`
   - If `.py` or `.md`: Convert using jupytext to notebook format
   - Clean output cells (remove data summaries, errors, warnings, printed results)
   - Keep markdown explanation cells

2. **Add Configuration**:
   - Add matplotlib DPI configuration to first cell:
     ```python
     import matplotlib.pyplot as plt
     plt.rcParams["figure.dpi"] = 300
     plt.rcParams["savefig.dpi"] = 300
     ```
   - Update any existing DPI settings to 300
   - If API key needed: Inject API key configuration at beginning
     ```python
     api_key = "[API_KEY]"  # Replace if needed
     ```

3. **Execute Notebook**:
   - Activate environment: `source [REPO_NAME]-env/bin/activate`
   - Use papermill or nbclient to execute
   - Handle errors iteratively (up to 5 attempts per tutorial)
   - Fix dependency issues, path problems, data loading errors

4. **Extract Images**:
   - Use `tools/extract_notebook_images.py` to extract figures
   - Save to `notebooks/[tutorial_name]/images/`
   - Verify images match tutorial outputs

5. **Clean Error Cells & Sanitize**:
   - Remove papermill error cells and HTML tags:
     ```bash
     python tools/preprocess_notebook.py notebooks/[tutorial_name]/[tutorial_name]_execution.ipynb notebooks/[tutorial_name]/[tutorial_name]_execution_cleaned.ipynb
     ```
   - Sanitize personal information from notebook:
     ```bash
     python tools/personal_info_sanitizer.py notebooks/[tutorial_name]/[tutorial_name]_execution_cleaned.ipynb
     ```
   - This removes user paths, emails, usernames, API keys, and IP addresses

6. **Create Final Notebook**:
   - Save cleaned notebook as `[tutorial_name]_execution_final.ipynb`
   - Ensure all cells executed successfully
   - Preserve outputs for reference
   - Verify no personal information remains

### File Naming Convention

Convert all tutorial names to snake_case:
- `Data-Processing-Tutorial` → `data_processing_tutorial`
- `README.md` → `readme`

### Output Structure

Create this structure for each tutorial:
```
notebooks/
├── [tutorial_name]/
│   ├── [tutorial_name]_execution_final.ipynb
│   └── images/
│       ├── figure_1.png
│       └── figure_2.png
```

### Create Execution Report

Create `reports/executed_notebooks.json` with:
- List of all successfully executed tutorials
- GitHub URLs for each tutorial
- Execution paths
- Status (success/failed)
- Any errors encountered

## Expected Outputs

- `notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb` for each tutorial
- `notebooks/[tutorial_name]/images/` directory with extracted figures
- `reports/executed_notebooks.json` with execution summary

## Success Criteria

- [ ] All tutorials from scanner results executed
- [ ] Final notebooks created with successful execution
- [ ] Images extracted to proper directories
- [ ] Execution report created with GitHub URLs
- [ ] Snake_case naming convention applied consistently
```

**Replace `[REPO_NAME]` with your actual repository name** (e.g., `panpipes`)
**Replace `[API_KEY]` if tutorials require API access**

## Expected Outputs

After executing this step, you should have:

1. **`notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb`**
   - Executed notebook for each tutorial
   - All cells run successfully
   - Outputs preserved

2. **`notebooks/[tutorial_name]/images/`**
   - Extracted figures and visualizations
   - High-resolution (300 DPI) images

3. **`reports/executed_notebooks.json`**
   - List of executed tutorials
   - GitHub URLs
   - Execution status
   - Paths to final notebooks

## Validation

To verify this step completed successfully:

1. **Check Error Cell Removal**:
   - Verify no `papermill-error-cell` markers in final notebook
   - Check for HTML tags in markdown cells
   - Ensure error cells were removed during preprocessing

2. **Check Personal Information**:
   - Run: `python tools/personal_info_sanitizer.py notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb --report`
   - Review sanitization report
   - Verify no user paths, emails, usernames, or API keys remain

3. **Check Notebook Execution**:
   ```bash
   # Verify notebooks exist and executed successfully
   ls notebooks/*/*_execution_final.ipynb
   ```

2. **Check Images**:
   ```bash
   # Verify images were extracted
   ls notebooks/*/images/
   ```

3. **Review Execution Report**:
   ```bash
   # Check JSON is valid
   python -m json.tool reports/executed_notebooks.json
   ```

4. **Test Notebook Execution**:
   - Open a final notebook
   - Verify all cells executed without errors
   - Check outputs match expected results

## Troubleshooting

### Execution Failures

**Problem**: Notebook fails to execute
- **Solution**: Check error messages in notebook output
- **Solution**: Verify environment has all dependencies
- **Solution**: Check file paths are correct (relative to notebook location)
- **Solution**: Review tutorial for missing data files

**Problem**: Import errors
- **Solution**: Install missing packages in environment
- **Solution**: Check if package needs to be installed from source
- **Solution**: Verify Python version compatibility

**Problem**: Data file not found
- **Solution**: Check repository structure for data files
- **Solution**: Update paths to be relative to notebook location
- **Solution**: Download missing data files if needed

### Image Extraction Issues

**Problem**: No images extracted
- **Solution**: Verify notebook creates figures (check for plt.show(), plt.savefig())
- **Solution**: Run `tools/extract_notebook_images.py` manually
- **Solution**: Check image extraction script is working

**Problem**: Low-quality images
- **Solution**: Verify DPI settings are 300
- **Solution**: Re-run notebook with correct DPI configuration

### API Key Issues

**Problem**: API calls fail
- **Solution**: Provide API key in prompt if needed
- **Solution**: Check API key format matches tutorial requirements
- **Solution**: Verify API key is injected at beginning of notebook

## Next Steps

Once Step 2 is complete:
- Proceed to [Step 3: Extract Tools](step3_extract_tools.md)
- Ensure all tutorials executed successfully
- Review `reports/executed_notebooks.json` to confirm execution status



