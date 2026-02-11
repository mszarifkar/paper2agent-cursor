# Step 5: Coverage & Quality Reports

## Context

This step generates comprehensive code coverage and quality reports for all extracted tools. It runs pytest with coverage analysis and pylint for code style analysis, then creates detailed reports summarizing the results.

## Prerequisites

- Step 3 completed successfully (tools and tests exist)
- `src/tools/*.py` files exist
- `tests/code/` directory with test files
- `[REPO_NAME]-env` environment has pytest, pytest-cov, and pylint installed

## Cursor Composer Prompt

Copy and paste this prompt into Cursor Composer:

```
I'm building an MCP toolsuit for [REPO_NAME]. Please help me with Step 5: Coverage & Quality Reports.

## Input Files

- Tool modules: `src/tools/*.py`
- Test files: `tests/code/**/*_test.py`
- Executed tutorials: `reports/executed_notebooks.json`

## Task 1: Code Formatting

Before running analysis, format code:

1. **Format Tool Modules**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   black src/tools/*.py
   isort src/tools/*.py
   ```

2. **Format Test Files**:
   ```bash
   black tests/code/**/*.py
   isort tests/code/**/*.py
   ```

## Task 2: Code Coverage Analysis

Run pytest with coverage:

1. **Run Coverage Analysis**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   pytest tests/code/ --cov=src/tools --cov-report=xml --cov-report=json --cov-report=html --cov-report=term -v > reports/coverage/pytest_output.txt 2>&1
   ```

2. **Generate Coverage Reports**:
   - XML report: `reports/coverage/coverage.xml` (for CI/CD)
   - JSON report: `reports/coverage/coverage.json` (machine-readable)
   - HTML report: `reports/coverage/htmlcov/` (human-readable)
   - Text summary: Extract to `reports/coverage/coverage_summary.txt`

3. **Create Coverage Analysis Report**:
   - Read coverage JSON/XML to extract metrics
   - Create `reports/coverage/coverage_report.md` with:
     - Overall coverage percentages (lines, branches, functions, statements)
     - Per-file coverage breakdown
     - Per-tutorial coverage analysis
     - Coverage gaps identification
     - Quality recommendations

## Task 3: Code Quality Analysis (Pylint)

Run pylint for style analysis:

1. **Run Pylint**:
   ```bash
   source [REPO_NAME]-env/bin/activate
   pylint src/tools/*.py --output-format=text > reports/quality/pylint/pylint_report.txt 2>&1
   ```

2. **Extract Scores**:
   - Parse pylint output for per-file scores
   - Create `reports/quality/pylint/pylint_scores.txt` with scores summary

3. **Create Pylint Issues Report**:
   - Create `reports/quality/pylint/pylint_issues.md` with:
     - Per-file score breakdown
     - Top issues by category
     - Most problematic files
     - Style recommendations

## Task 4: Combined Quality Report

Create comprehensive quality report:

1. **Calculate Quality Metrics**:
   - Overall coverage percentages from coverage JSON
   - Average pylint score from parsed scores
   - Test-to-code ratio
   - Coverage distribution (<50%, 50-80%, >80%)
   - Quality distribution (excellent >9, good 7-9, fair 5-7, poor <5)

2. **Generate Combined Report**:
   - Create `reports/coverage_and_quality_report.md` with:
     - Overall quality metrics
     - Per-tutorial quality breakdown
     - Combined quality score (weighted: coverage 40%, style 30%, completeness 20%, structure 10%)
     - Actionable recommendations

## Expected Outputs

- `reports/coverage/coverage.xml` - XML coverage report
- `reports/coverage/coverage.json` - JSON coverage report
- `reports/coverage/htmlcov/` - HTML coverage dashboard
- `reports/coverage/coverage_summary.txt` - Text summary
- `reports/coverage/coverage_report.md` - Detailed coverage analysis
- `reports/coverage/pytest_output.txt` - Full pytest output
- `reports/quality/pylint/pylint_report.txt` - Full pylint output
- `reports/quality/pylint/pylint_scores.txt` - Scores summary
- `reports/quality/pylint/pylint_issues.md` - Issues breakdown
- `reports/coverage_and_quality_report.md` - Combined quality report

## Success Criteria

- [ ] Code formatted with black and isort
- [ ] Coverage reports generated (XML, JSON, HTML, text)
- [ ] Coverage analysis report created
- [ ] Pylint analysis completed
- [ ] Pylint issues report created
- [ ] Combined quality report generated
- [ ] Quality metrics calculated
```

**Replace `[REPO_NAME]` with your actual repository name** (e.g., `panpipes`)

## Expected Outputs

After executing this step, you should have:

1. **Coverage Reports** (`reports/coverage/`):
   - `coverage.xml` - For CI/CD integration
   - `coverage.json` - Machine-readable format
   - `htmlcov/` - Interactive HTML dashboard
   - `coverage_summary.txt` - Quick reference
   - `coverage_report.md` - Detailed analysis
   - `pytest_output.txt` - Full test execution log

2. **Quality Reports** (`reports/quality/pylint/`):
   - `pylint_report.txt` - Full analysis output
   - `pylint_scores.txt` - Per-file scores
   - `pylint_issues.md` - Detailed issues breakdown

3. **Combined Report**:
   - `reports/coverage_and_quality_report.md` - Comprehensive quality assessment

## Validation

To verify this step completed successfully:

1. **Check Coverage Reports**:
   ```bash
   # Verify files exist
   ls reports/coverage/
   
   # View HTML report
   open reports/coverage/htmlcov/index.html  # macOS
   # or
   start reports/coverage/htmlcov/index.html  # Windows
   ```

2. **Check Quality Reports**:
   ```bash
   # Verify pylint reports exist
   ls reports/quality/pylint/
   
   # Review scores
   cat reports/quality/pylint/pylint_scores.txt
   ```

3. **Review Combined Report**:
   ```bash
   # Check combined report
   cat reports/coverage_and_quality_report.md
   ```

## Troubleshooting

### Coverage Issues

**Problem**: Coverage reports not generated
- **Solution**: Verify pytest-cov is installed: `pip install pytest-cov`
- **Solution**: Check pytest command syntax
- **Solution**: Ensure test files are discovered by pytest

**Problem**: Low coverage percentages
- **Solution**: Review coverage report to identify uncovered lines
- **Solution**: Add tests for uncovered functions
- **Solution**: Check if some code is intentionally excluded

### Pylint Issues

**Problem**: Pylint fails to run
- **Solution**: Verify pylint is installed: `pip install pylint`
- **Solution**: Check Python version compatibility
- **Solution**: Review pylint configuration if needed

**Problem**: Many style issues
- **Solution**: Review `pylint_issues.md` for common problems
- **Solution**: Fix high-priority issues first
- **Solution**: Some issues may be acceptable (document if so)

### Report Generation Issues

**Problem**: Reports not created
- **Solution**: Verify directory structure exists
- **Solution**: Check file permissions
- **Solution**: Review error messages in output

## Next Steps

Once Step 5 is complete:
- Review quality reports to identify improvements
- Address high-priority coverage gaps if needed
- Consider fixing critical style issues
- Your MCP toolsuit is now complete!



