---
name: docx-to-obsidian
description: "Convert Microsoft Word documents (docx) to Obsidian Flavored Markdown. ALWAYS ask user preference first: preserve all content or summarize and compress. Default to preserving all content. Use for: knowledge base creation, document organization, adding tags/properties/links, extracting images, creating indexes."
---

# DOCX to Obsidian Knowledge Base Converter

## Overview

Complete workflow for converting Word documents (.docx) to Obsidian Flavored Markdown. Preserves all content by default unless user explicitly requests summarization.

## ⚠️ CRITICAL: User Preference Required

**BEFORE starting conversion, ALWAYS ask:**

> "Do you want me to:
> 1. **Preserve ALL original content** - Keep 100% text, structure, and charts unchanged
> 2. **Summarize and compress** - Create condensed version with key points only"

**Default behavior**: If user doesn't specify, assume **PRESERVE ALL ORIGINAL CONTENT**.

## Quick Start

```bash
# 1. Extract DOCX (it's a ZIP file)
cp input.docx temp.zip && unzip -q temp.zip -d unpacked_docx && rm temp.zip

# 2. Convert to Markdown with pandoc
pandoc --track-changes=all unpacked_docx/word/document.xml -o temp_content.md

# 3. Extract images
mkdir -p obsidian_vault/_attachments
cp -r unpacked_docx/word/media/* obsidian_vault/_attachments/

# 4. Update image paths
sed -i 's|media/|_attachments/|g' obsidian_vault/report.md
```

## Conversion Modes

### Mode 1: Preserve All Content (DEFAULT)

**When**: User wants original unchanged, technical reports, legal documents, or no preference specified.

**What to do**:
- Extract and convert with pandoc
- **DO NOT** modify, summarize, or compress
- **DO NOT** change original text, paragraphs, or structure
- Only add Obsidian features that don't alter content:
  - YAML frontmatter (metadata only)
  - Tags (don't change content)
  - Image links (don't modify charts/captions)
  - Basic formatting (markdown syntax only)
- Preserve all charts, tables, and data exactly as-is

**What NOT to do**:
- ❌ Summarize sections
- ❌ Compress paragraphs
- ❌ Rewrite text
- ❌ Change chart/table data

### Mode 2: Summarize and Compress

**When**: User explicitly requests summarization, executive summary, or quick reference.

**What to do**:
- Convert with pandoc
- Summarize key points
- Condense content
- Create callouts for main conclusions
- Convert tables to concise format

## Obsidian Features

### YAML Frontmatter

```yaml
---
title: Document Title
date: 2025-01-13
author: Author Name
type: report
category: geology
tags:
  - tag1
  - tag2
status: completed
---
```

### Tags and Properties

- Use hashtags: `#tag #nested/tag`
- Add tags in frontmatter for organization
- Use tags for navigation and filtering

### Internal Links (Wikilinks)

```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]
```

### Callouts

```markdown
> [!note] Note
> Information

> [!warning] Warning
> Important notice

> [!success] Conclusion
> Final result

> [!todo] Action Item
> Things to do
```

### Tables

```markdown
| Parameter | Value |
|-----------|-------|
| Length | 410m |
| Width | 2-20cm |
```

### Images

```markdown
![_attachments/image1.jpeg]
![_attachments/image1.jpeg|640x480]
```

## Image Processing

1. **Unpack DOCX**: DOCX is a ZIP file containing XML and media
2. **Locate media folder**: `unpacked_docx/word/media/`
3. **Copy to attachments**: Move all images to `obsidian_vault/_attachments/`
4. **Update references**: Change `media/` to `_attachments/` in Markdown
5. **Verify paths**: Ensure all images link correctly

**Preserve original formats** (JPEG, PNG) - don't convert or re-encode.

## File Organization

```
obsidian_vault/
├── README.md (index and navigation)
├── Main Document.md
└── _attachments/
    ├── image1.jpeg
    ├── image2.png
    └── ...
```

## Quality Checklist

### Before Completing (Both Modes)
- [ ] User preference confirmed
- [ ] Correct mode applied
- [ ] All images extracted and linked correctly
- [ ] YAML frontmatter complete
- [ ] No broken image references

### Final Verification (Preserve Mode)
- [ ] No text rewritten or paraphrased
- [ ] No paragraphs combined or shortened
- [ ] Original structure maintained
- [ ] All original headings preserved
- [ ] No "key points" or "summary" added

## Troubleshooting

### Images Not Displaying
- Ensure `_attachments/` folder exists
- Image paths use `_attachments/` prefix
- Filenames match exactly (case-sensitive)

### Pandoc Not Found
```bash
# Windows
winget install pandoc
# Or download from: https://pandoc.org/installing.html
```

### Encoding Issues
```bash
pandoc --from docx --to markdown --output-file output.md input.docx
```

### Large Documents
- Process sections separately
- Consider using `--toc` to generate TOC
- Split into multiple linked notes

## References

- [Obsidian Help](https://help.obsidian.md/syntax)
- [Obsidian Links](https://help.obsidian.md/links)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)

---

**Skill Version**: 1.1
**Last Updated**: 2025-01-13
**Changes in v1.1**: Added user preference prompt with two conversion modes (preserve vs. summarize)
