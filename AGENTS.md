# AGENTS.md

This file provides guidelines for AI agents operating in this repository.

## Project Overview

This is an **Agent Skills Repository** containing multiple AI agent skills for document processing (Word, PDF, PowerPoint, Excel), Obsidian integration, and skill development tools. Each skill is a self-contained module with documentation, reference materials, and implementation scripts.

## Build, Lint, Test Commands

This project does not have a traditional build system. Skills are Markdown documentation files (`.md`) and scripts (`.sh`, `.js`, `.py`). There are **no npm/pip build commands** required.

- **No build process**: Skills are documentation-based, not compiled code
- **No tests**: Manual verification only
- **No linting**: Follow style guidelines below

If adding scripts to skills:
- Test scripts manually before committing
- Use shellcheck for shell scripts: `shellcheck your-script.sh`
- Use eslint/prettier for JavaScript if added

## Code Style Guidelines

### Language

- **All interactions and documentation must use Simplified Chinese** (中文)
- Comments in any code should be in Chinese
- Variable names and function names in English (standard practice)

### File Structure

Each skill should follow this structure:
```
skill-name/
├── SKILL.md          # Main skill documentation (REQUIRED)
├── LICENSE.txt       # License terms (REQUIRED)
├── reference.md      # Advanced reference material (optional)
├── forms.md          # Form handling docs (optional)
├── scripts/          # Implementation scripts (optional)
│   └── *.sh / *.js / *.py
├── ooxml/            # OOXML schema files (optional, docx skill)
└── references/       # Reference materials (optional)
```

### Documentation Style (SKILL.md)

Every skill must have a `SKILL.md` with frontmatter:
```markdown
---
name: skill-name
description: Brief description of the skill
license: License name. See LICENSE.txt for details
---

# Skill Title

## Overview
...

## Quick Start
...

## Python Libraries
...
```

### Markdown Guidelines

- Use Chinese punctuation (，。：；？！) in Chinese text
- Use English punctuation (.,:,;?!) in code blocks and technical terms
- Use ### for section headings (not ## or ####)
- Keep line width under 100 characters for readability
- Use code blocks with language tags: ```python, ```bash, ```javascript

### Script Guidelines

**Shell Scripts (.sh)**:
- Start with `#!/bin/bash` or `#!/usr/bin/env bash`
- Use `set -e` for error handling
- Add Chinese comments for complex logic
- Use `#!/bin/bash` (not sh) for compatibility

**Python Scripts (.py)**:
- Follow PEP 8 style
- Use type hints where helpful
- Add docstrings in Chinese or English

**JavaScript (.js)**:
- Use ES6+ syntax
- Prefer const over let
- Use async/await for asynchronous code

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Skill directory | kebab-case | `docx-to-obsidian` |
| Markdown files | kebab-case | `reference.md`, `交互语言.md` |
| Shell scripts | kebab-case | `extract-tables.sh` |
| Functions | snake_case (Python) / camelCase (JS) | `extract_text()`, `mergePDFs()` |
| Variables | snake_case (Python) / camelCase (JS) | `output_file`, `pdfReader` |

### Error Handling

- Scripts should handle errors gracefully
- Use `set -e` in shell scripts to exit on errors
- Print clear error messages in Chinese
- Validate file paths before processing

### Imports and Dependencies

- Document required dependencies in SKILL.md
- Use official/standard libraries where possible
- Avoid external dependencies unless necessary
- Include installation instructions for required tools (e.g., Tesseract for OCR)

## Agent Interaction Rules

See `.agent/rules/交互语言.md` for mandatory rules:
- All interactions must use Simplified Chinese
- This applies to all communication, documentation, and code comments

## Working with This Repository

1. **Do not modify** existing skills without good reason
2. **Test scripts** before adding them
3. **Use Chinese** in all documentation and comments
4. **Follow the skill structure** when adding new skills
5. **Include LICENSE.txt** with every new skill

## File Modification Workflow

When modifying existing files:
- Update frontmatter fields if changed (name, description)
- Keep Chinese punctuation consistent
- Update table of contents if adding new sections
- Test any new scripts in the `scripts/` directory

## Creating New Skills

Use `skill-creator` skill as a template:
- Copy its structure as a starting point
- Adapt SKILL.md for your specific skill
- Add relevant reference materials
- Include working scripts with Chinese comments
