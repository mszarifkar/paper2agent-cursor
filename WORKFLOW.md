# Paper2Agent-Cursor: Interactive Workflow Guide

## Overview

This guide walks you through building an MCP (Model Context Protocol) toolsuit using Cursor Composer instead of Claude API. The workflow maintains the same structure as the original Paper2Agent but executes each step interactively through Cursor Composer.

## Prerequisites

- **Cursor Pro** license (active)
- **Python 3.10+** installed
- **Git** installed
- Basic familiarity with command line

## Workflow Overview

The workflow consists of 5 main steps:

1. **Environment Setup & Tutorial Discovery** - Set up Python environment and find tutorials
2. **Execute Tutorials** - Run notebooks and create validated executions
3. **Extract Tools** - Create reusable tool functions with tests
4. **Build MCP Server** - Integrate all tools into unified MCP server
5. **Coverage & Quality Reports** - Generate code coverage and quality metrics

## Quick Start

1. **Clone Repository** (if starting from scratch):
   ```bash
   git clone <your-repo-url>
   cd <your-project-dir>
   ```

2. **Set Up Project Structure**:
   ```bash
   bash scripts/03_prepare_folders.sh <project-dir>
   ```

3. **Clone Target Repository**:
   ```bash
   bash scripts/02_clone_repo.sh <project-dir> <github-repo-url>
   ```

4. **Follow Interactive Steps**:
   - Open each step guide in `interactive_steps/`
   - Copy the Cursor Composer prompt
   - Execute in Cursor Composer
   - Verify outputs before proceeding

## Step-by-Step Workflow

### Step 1: Environment Setup & Tutorial Discovery

**File**: [interactive_steps/step1_environment_and_scan.md](interactive_steps/step1_environment_and_scan.md)

**What it does**:
- Creates Python virtual environment (`[repo-name]-env`)
- Scans repository for tutorials
- Classifies tutorials for tool extraction

**Expected time**: 15-30 minutes

**Outputs**:
- `reports/environment-manager_results.md`
- `reports/tutorial-scanner.json`
- `reports/tutorial-scanner-include-in-tools.json`

**Next**: Proceed to Step 2

---

### Step 2: Execute Tutorials

**File**: [interactive_steps/step2_execute_tutorials.md](interactive_steps/step2_execute_tutorials.md)

**What it does**:
- Executes all discovered tutorials
- Creates validated notebook executions
- Extracts figures and visualizations

**Expected time**: 30 minutes - 2 hours (depends on number of tutorials)

**Outputs**:
- `notebooks/[tutorial_name]/[tutorial_name]_execution_final.ipynb`
- `notebooks/[tutorial_name]/images/`
- `reports/executed_notebooks.json`

**Next**: Proceed to Step 3

---

### Step 3: Extract Tools & Create Tests

**File**: [interactive_steps/step3_extract_tools.md](interactive_steps/step3_extract_tools.md)

**What it does**:
- Extracts reusable tools from tutorials
- Creates production-ready Python modules
- Generates comprehensive test suites

**Expected time**: 1-3 hours (depends on complexity)

**Outputs**:
- `src/tools/[tutorial_name].py`
- `tests/code/[tutorial_name]/[tool_name]_test.py`
- `tests/logs/[tutorial_name]_test.md`

**Next**: Proceed to Step 4

---

### Step 4: Build MCP Server

**File**: [interactive_steps/step4_build_mcp.md](interactive_steps/step4_build_mcp.md)

**What it does**:
- Creates unified MCP server
- Integrates all tool modules
- Provides single interface for all tools

**Expected time**: 15-30 minutes

**Outputs**:
- `src/[repo-name]_mcp.py`

**Next**: Proceed to Step 5

---

### Step 5: Coverage & Quality Reports

**File**: [interactive_steps/step5_coverage_quality.md](interactive_steps/step5_coverage_quality.md)

**What it does**:
- Generates code coverage reports
- Runs code quality analysis (pylint)
- Creates comprehensive quality assessment

**Expected time**: 15-30 minutes

**Outputs**:
- `reports/coverage/` (coverage reports)
- `reports/quality/pylint/` (style analysis)
- `reports/coverage_and_quality_report.md`

**Next**: Review reports and deploy!

---

## Progress Tracking

Use the [PROGRESS.md](PROGRESS.md) template to track your progress through each step.

## Troubleshooting

### Common Issues

**Problem**: Cursor Composer prompt doesn't work as expected
- **Solution**: Ensure you're in the correct directory
- **Solution**: Verify prerequisite files exist
- **Solution**: Check file paths in prompt match your structure

**Problem**: Step fails partway through
- **Solution**: Review error messages carefully
- **Solution**: Check troubleshooting section in step guide
- **Solution**: You can re-run steps - they're designed to be idempotent

**Problem**: Outputs don't match expected structure
- **Solution**: Review step guide for exact output requirements
- **Solution**: Check file naming conventions
- **Solution**: Verify you're following instructions exactly

### Getting Help

1. Review the troubleshooting section in each step guide
2. Check the original Paper2Agent documentation for reference
3. Review agent definitions in `agents/` directory
4. Check prompt templates in `prompts/` directory

## Differences from Original Paper2Agent

### Key Differences

1. **Interactive vs Automated**:
   - Original: Automated batch processing via Claude API
   - Cursor Version: Interactive step-by-step workflow

2. **API Usage**:
   - Original: Requires Claude API account and API key
   - Cursor Version: Uses Cursor Pro license (no separate API needed)

3. **Execution Model**:
   - Original: Single command runs entire pipeline
   - Cursor Version: Each step executed separately with user review

4. **Cost**:
   - Original: ~$15 per complex repository (one-time)
   - Cursor Version: Uses your Cursor Pro subscription

### Same Output Structure

The output structure matches the original Paper2Agent exactly:
- Same directory structure
- Same file formats
- Same MCP server format
- Compatible with existing workflows

## Best Practices

1. **Review Each Step**: Don't skip validation steps
2. **Save Progress**: Commit after each successful step
3. **Test Incrementally**: Verify outputs before proceeding
4. **Document Issues**: Note any problems in PROGRESS.md
5. **Iterate**: Steps can be re-run if needed

## Next Steps After Completion

1. **Test MCP Server**:
   ```bash
   source [repo-name]-env/bin/activate
   python src/[repo-name]_mcp.py
   ```

2. **Deploy or Share**:
   - Create GitHub repository
   - Share with colleagues
   - Use in your projects

3. **Improve Quality**:
   - Review coverage reports
   - Fix style issues
   - Add more tests if needed

## Additional Resources

- Original Paper2Agent: https://github.com/jmiao24/Paper2Agent
- FastMCP Documentation: https://github.com/jlowin/fastmcp
- MCP Protocol: https://modelcontextprotocol.io/



