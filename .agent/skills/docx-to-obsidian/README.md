# DOCX to Obsidian Knowledge Base Converter - Skill Documentation

## Overview

This skill converts Microsoft Word documents (.docx) to Obsidian Flavored Markdown with comprehensive feature support including:

- **Content preservation**: Complete conversion without data loss
- **Image extraction**: Automatic extraction and proper linking of images
- **Obsidian enhancement**: Frontmatter, tags, wikilinks, callouts
- **Navigation**: Tables of contents, internal links, indexes
- **Metadata**: YAML frontmatter and optional JSON metadata

## When to Use

Use this skill when you need to:
1. Convert professional documents to Obsidian knowledge base
2. Create document collections in Obsidian
3. Add tags, properties, and internal links to documents
4. Extract and preserve images from DOCX files
5. Create indexes and navigation structures
6. Convert technical reports, academic papers, meeting notes, etc.

**IMPORTANT**: This skill now has two modes:
- **Preserve Mode (DEFAULT)**: Keep 100% of original content unchanged
- **Summarize Mode (EXPLICIT ONLY)**: Condense content when user requests it

The skill will **ALWAYS ask** you which mode you want before starting conversion.

## Quick Example

```bash
# 1. Extract DOCX
cp report.docx temp.zip && unzip temp.zip -d unpacked_docx

# 2. Convert to Markdown
pandoc --track-changes=all unpacked_docx/word/document.xml -o temp.md

# 3. Process with Obsidian features
# (Read temp.md, enhance with frontmatter, tags, links)

# 4. Extract images
mkdir obsidian_vault/_attachments
cp unpacked_docx/word/media/* obsidian_vault/_attachments/

# 5. Update paths
sed -i 's|media/|_attachments/|g' obsidian_vault/report.md
```

## Skill Structure

```
docx-to-obsidian/
├── SKILL.md                          # Main skill instructions
├── README.md                          # This file
├── references/
│   └── obsidian-syntax.md              # Obsidian syntax quick reference
└── assets/
    └── template.md                    # Example converted document
```

## Key Features

### 1. Content Enhancement

- Add YAML frontmatter with metadata
- Use callout boxes for emphasis
- Format data in tables
- Create proper heading hierarchy
- Add tags for navigation

### 2. Image Handling

- Extract all images from DOCX
- Preserve original formats
- Update path references
- Verify all links work

### 3. Navigation

- Create index notes
- Add internal links (wikilinks)
- Use tags for filtering
- Create table of contents

### 4. Quality Control

- Checklist for verification
- Troubleshooting guide
- Common patterns reference

## Reference Materials

- **SKILL.md**: Complete conversion workflow
- **references/obsidian-syntax.md**: Obsidian Markdown syntax reference
- **assets/template.md**: Example converted document

## Supported Document Types

- Technical reports
- Academic papers
- Meeting minutes
- Project documentation
- Business documents
- Research papers
- Policy documents
- User manuals

## Prerequisites

- **Pandoc**: For DOCX to Markdown conversion
  - Install: `winget install pandoc`
  - Download: https://pandoc.org/installing.html

- **Basic tools**: cp, mkdir, sed, unzip (or PowerShell equivalents)

## Common Use Cases

### Use Case 1: Single Document

Simple conversion of one DOCX file:
1. Extract and convert
2. Add Obsidian features
3. Create vault structure
4. Verify all links

### Use Case 2: Batch Processing

Convert multiple documents:
```bash
for file in *.docx; do
    # Run conversion for each file
done
```

### Use Case 3: Knowledge Base

Create complete knowledge base:
1. Convert all documents
2. Create master index
3. Add cross-references
4. Organize with tags

## Limitations

- Very large documents (>10MB) may need special handling
- Complex formatting may require manual adjustment
- Some Word features may not map to Markdown
- External links need manual verification

## Best Practices

1. **Always preserve content**: Never delete information
2. **Test images**: Verify all image links work
3. **Use tags**: Add relevant tags for navigation
4. **Create indexes**: Help users find content
5. **Keep structure**: Maintain document organization
6. **Verify quality**: Use checklist before completing

## Support

For Obsidian documentation:
- https://help.obsidian.md/syntax
- https://help.obsidian.md/links
- https://help.obsidian.md/callouts

For Pandoc documentation:
- https://pandoc.org/MANUAL.html

## Version History

- **v1.1** (2025-01-13): User preference mode added
  - CRITICAL: Always ask user preference (preserve vs. summarize)
  - Two conversion modes with clear rules
  - Default to preserving 100% of content
  - Strict prohibitions on summarization in preserve mode
  - Mode-specific quality checklists
  - Clear guidelines on what's allowed in each mode

- **v1.0** (2025-01-13): Initial release
  - Complete DOCX to Obsidian conversion workflow
  - Image extraction and linking
  - Obsidian feature enhancement
  - Reference materials and templates

## License

This skill is provided as-is for use with OhMyOpenCode.

---

**Last Updated**: 2025-01-13
**Skill Version**: 1.1
