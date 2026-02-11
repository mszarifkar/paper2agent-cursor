# Paper2Agent-Cursor

A Cursor Composer-based version of [Paper2Agent](https://github.com/jmiao24/Paper2Agent) that transforms research papers into interactive AI agents using Cursor Composer instead of Claude API.

## Overview

Paper2Agent-Cursor provides an interactive workflow for building MCP (Model Context Protocol) toolsuits from research paper codebases. Unlike the original Paper2Agent which uses Claude API for automated batch processing, this version uses Cursor Composer for step-by-step interactive execution.

## Key Features

- **No External API Required**: Uses your Cursor Pro license instead of Claude API
- **Interactive Workflow**: Step-by-step execution with full control
- **Same Output Structure**: Compatible with original Paper2Agent outputs
- **Cost Effective**: No per-repository API costs
- **Full Control**: Review and approve each step before proceeding

## Prerequisites

- **Cursor Pro** license (active)
- **Python 3.10+** installed
- **Git** installed
- Basic command line familiarity

## Quick Start

1. **Clone this repository**:
   ```bash
   git clone <this-repo-url>
   cd paper2agent-cursor
   ```

2. **Set up your project**:
   ```bash
   bash scripts/01_setup_project.sh . <project-name>
   bash scripts/02_clone_repo.sh <project-dir> <github-repo-url>
   bash scripts/03_prepare_folders.sh <project-dir>
   ```

3. **Follow the interactive workflow**:
   - Start with [WORKFLOW.md](WORKFLOW.md) for overview
   - Follow each step in `interactive_steps/` directory
   - Copy prompts into Cursor Composer and execute

## Workflow Steps

1. **[Step 1: Environment Setup & Tutorial Discovery](interactive_steps/step1_environment_and_scan.md)**
   - Set up Python environment
   - Discover and classify tutorials

2. **[Step 2: Execute Tutorials](interactive_steps/step2_execute_tutorials.md)**
   - Run tutorials to create validated executions
   - Extract figures and outputs

3. **[Step 3: Extract Tools & Create Tests](interactive_steps/step3_extract_tools.md)**
   - Extract reusable tools from tutorials
   - Create comprehensive test suites

4. **[Step 4: Build MCP Server](interactive_steps/step4_build_mcp.md)**
   - Create unified MCP server
   - Integrate all tools

5. **[Step 5: Coverage & Quality Reports](interactive_steps/step5_coverage_quality.md)**
   - Generate code coverage reports
   - Run code quality analysis

See [WORKFLOW.md](WORKFLOW.md) for detailed instructions.

## How It Works

### Original Paper2Agent
```
Paper2Agent.sh → Scripts → Claude API → JSON outputs → Next step
```

### Paper2Agent-Cursor
```
WORKFLOW.md → User reads step guide → Cursor Composer prompt → Direct file creation → Next step
```

### Key Differences

| Feature | Original Paper2Agent | Paper2Agent-Cursor |
|---------|---------------------|-------------------|
| Execution | Automated batch | Interactive step-by-step |
| API | Claude API required | Cursor Pro license |
| Cost | ~$15 per repository | Included in subscription |
| Control | Limited (batch) | Full (interactive) |
| Output | Same structure | Same structure |

## Project Structure

```
paper2agent-cursor/
├── README.md                    # This file
├── WORKFLOW.md                  # Main workflow guide
├── PROGRESS.md                  # Progress tracking template
├── LICENSE                      # MIT License
├── interactive_steps/           # Step-by-step guides
│   ├── step1_environment_and_scan.md
│   ├── step2_execute_tutorials.md
│   ├── step3_extract_tools.md
│   ├── step4_build_mcp.md
│   └── step5_coverage_quality.md
├── prompts/                     # Original prompts (reference)
│   ├── step1_prompt.md
│   ├── step2_prompt.md
│   ├── step3_prompt.md
│   ├── step4_prompt.md
│   └── step5_prompt.md
├── agents/                      # Agent definitions (reference)
│   ├── tutorial-scanner.md
│   ├── tutorial-executor.md
│   ├── tutorial-tool-extractor-implementor.md
│   └── ...
├── scripts/                     # Helper scripts
│   ├── 01_setup_project.sh
│   ├── 02_clone_repo.sh
│   ├── 03_prepare_folders.sh
│   └── 06_launch_mcp.sh
└── tools/                       # Utility scripts
    ├── extract_notebook_images.py
    └── preprocess_notebook.py
```

## Usage Example

Building an MCP toolsuit for panpipes:

1. **Set up project**:
   ```bash
   bash scripts/01_setup_project.sh . panpipes-mpc
   bash scripts/02_clone_repo.sh panpipes-mpc https://github.com/DendrouLab/panpipes
   bash scripts/03_prepare_folders.sh panpipes-mpc
   ```

2. **Execute Step 1**:
   - Open `interactive_steps/step1_environment_and_scan.md`
   - Copy the Cursor Composer prompt
   - Replace `[REPO_NAME]` with `panpipes`
   - Execute in Cursor Composer

3. **Continue with remaining steps**:
   - Follow each step guide in order
   - Verify outputs before proceeding
   - Track progress in PROGRESS.md

## Output Structure

After completion, your project will have:

```
<project-dir>/
├── src/
│   ├── <repo-name>_mcp.py      # Generated MCP server
│   └── tools/
│       └── <tutorial-name>.py   # Extracted tools
├── <repo-name>-env/             # Python environment
├── repo/
│   └── <repo-name>/             # Cloned repository
├── notebooks/                    # Executed tutorials
├── tests/                        # Test files
└── reports/                      # Analysis reports
```

## Troubleshooting

See [WORKFLOW.md](WORKFLOW.md) for detailed troubleshooting guide.

Common issues:
- **Cursor Composer prompt issues**: Check file paths and directory structure
- **Step failures**: Review troubleshooting section in step guide
- **Output mismatches**: Verify you're following instructions exactly

## Comparison with Original Paper2Agent

### Advantages

- ✅ No external API costs
- ✅ Full interactive control
- ✅ Review and approve each step
- ✅ Easy to customize and iterate
- ✅ Uses familiar Cursor interface

### Considerations

- ⚠️ Requires manual execution of each step
- ⚠️ Takes longer than automated version
- ⚠️ Requires Cursor Pro license

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original Paper2Agent by [Jiacheng Miao](https://github.com/jmiao24)
- Based on the Paper2Agent architecture and methodology
- Uses FastMCP for MCP server implementation

## Related Projects

- [Paper2Agent](https://github.com/jmiao24/Paper2Agent) - Original automated version
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [MCP Protocol](https://modelcontextprotocol.io/) - Model Context Protocol specification

## Support

For issues or questions:
1. Check [WORKFLOW.md](WORKFLOW.md) troubleshooting section
2. Review step guides in `interactive_steps/`
3. Check original Paper2Agent documentation
4. Open an issue on GitHub



