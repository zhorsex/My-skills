---
name: docx-to-obsidian
description: Convert Microsoft Word documents (.docx) to Obsidian knowledge base format. CRITICAL: ALWAYS ask user preference first - "Preserve ALL original content (100% unchanged)" or "Summarize and compress". Default to preserving all content unless user explicitly requests summarization. Use for: (1) Knowledge base creation, (2) Document organization in Obsidian, (3) Adding tags, properties, and internal links, (4) Extracting and preserving images from DOCX, (5) Creating indexes and navigation structures
---

# DOCX to Obsidian Knowledge Base Converter

This skill provides a complete workflow for converting Word documents (.docx) to Obsidian Flavored Markdown with full feature support.

## ⚠️ IMPORTANT: User Preference Required

**Before starting conversion, ALWAYS ask user about content preservation preference:**

> "Do you want me to:
> 1. **Preserve ALL original content** - Keep 100% of text, structure, and charts unchanged
> 2. **Summarize and compress** - Create condensed version with key points only"

**Default behavior**: If user does not specify, assume **PRESERVE ALL ORIGINAL CONTENT**.

## Conversion Modes

### Mode 1: Preserve All Content (RECOMMENDED)

**When to use**:
- User wants original content unchanged
- Technical reports requiring complete accuracy
- Legal or official documents
- Academic papers with full text
- User doesn't specify preference

**What to do**:
1. Extract DOCX and convert with pandoc
2. **DO NOT** modify, summarize, or compress content
3. **DO NOT** change original text, paragraphs, or structure
4. Only add Obsidian features that don't alter content:
   - YAML frontmatter (metadata only)
   - Tags (don't change content)
   - Image links (don't modify charts/captions)
   - Basic formatting (markdown syntax conversion only)
5. Preserve all charts, tables, and data exactly as-is

**What NOT to do**:
- ❌ Summarize sections
- ❌ Compress paragraphs
- ❌ Rewrite text
- ❌ Combine multiple points
- ❌ Change chart/table data
- ❌ Alter structure beyond Markdown conversion

### Mode 2: Summarize and Compress

**When to use**:
- User explicitly requests summarization
- Creating executive summary
- Quick reference needs
- User explicitly chooses this option

**What to do**:
1. Convert with pandoc
2. Summarize key points
3. Condense content
4. Create callouts for main conclusions
5. Convert tables to concise format

## Quick Start

Basic conversion workflow:

1. **ASK USER PREFERENCE FIRST** (Always!)
2. **Extract DOCX content**:
   ```bash
   cp input.docx temp.zip && \
   unzip -q temp.zip -d unpacked_docx && \
   rm temp.zip
   ```

3. **Convert to Markdown**:
   ```bash
   pandoc --track-changes=all unpacked_docx/word/document.xml -o temp_content.md
   ```

4. **Read and process extracted content** based on user preference:
   - **Preserve mode**: Only add Obsidian features without altering content
   - **Summarize mode**: Condense and restructure content

5. **Extract images**:
   ```bash
   mkdir -p obsidian_vault/_attachments
   cp -r unpacked_docx/word/media/* obsidian_vault/_attachments/
   ```

6. **Update image paths**:
   ```bash
   sed -i 's|media/|_attachments/|g' obsidian_vault/report.md
   ```

7. **Enhance with Obsidian features** (respecting user preference):
   - **Preserve mode**: Add frontmatter, tags, links ONLY
   - **Summarize mode**: Add frontmatter, callouts, restructure content

## Obsidian Flavored Markdown Features

### YAML Frontmatter

Add frontmatter at the start of each note:

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

Use callouts for important information:

```markdown
> [!note] Note
> Information

> [!warning] Warning
> Important notice

> [!success] Conclusion
> Final result

> [!todo] Action Item
> Things to do

> [!important] Key Point
> Critical information
```

### Tables

Format data as tables for easy comparison:

```markdown
| Parameter | Value |
|----------|--------|
| Length | 410m |
| Width | 2-20cm |
```

### Images

Embed images with proper sizing:

```markdown
![_attachments/image1.jpeg]
![_attachments/image1.jpeg|640x480]
![Caption](_attachments/image1.jpeg)
```

## Content Enhancement Guidelines

### Mode 1: Preserve All Content (DEFAULT)

**PRINCIPLE**: DO NOT ALTER original content. Only add Obsidian-specific elements.

When processing content in preserve mode:

1. **NEVER modify original text**: Keep every sentence, paragraph, and word exactly as-is
2. **NEVER summarize**: Don't create condensed versions of sections
3. **NEVER compress**: Don't combine multiple points or shorten content
4. **Only add Obsidian infrastructure**:
   - YAML frontmatter (metadata only, no content changes)
   - Tags (add to frontmatter or end, don't alter text)
   - Wikilinks (link to existing sections, don't restructure)
   - Image links (update path only, don't change captions)
   - Markdown syntax conversion (preserving meaning)
5. **Keep charts and tables exactly as-is**: Don't modify data, labels, or structure
6. **Preserve all headings**: Keep original heading hierarchy

**What you CAN do in preserve mode**:
- ✅ Add YAML frontmatter (title, date, author, tags)
- ✅ Update image paths (`media/` → `_attachments/`)
- ✅ Convert Word formatting to Markdown equivalent (same content)
- ✅ Add tags to frontmatter or end of sections
- ✅ Create internal section links (existing content only)
- ✅ Fix broken formatting from pandoc conversion
- ✅ Add comments/hidden notes for user context

**What you CANNOT do in preserve mode**:
- ❌ Summarize paragraphs or sections
- ❌ Rewrite or rephrase text
- ❌ Combine bullet points
- ❌ Create "key points" lists
- ❌ Add callout boxes that restructure content
- ❌ Modify table data or chart labels
- ❌ Add "conclusions" not in original
- ❌ Compress or shorten any content

### Mode 2: Summarize and Compress (EXPLICIT REQUEST ONLY)

**PRINCIPLE**: Only when user explicitly requests summarization.

When processing content in summarize mode:

1. **Extract key points**: Identify main ideas and conclusions
2. **Condense information**: Create concise versions
3. **Use callouts**: Highlight conclusions, warnings, recommendations
4. **Restructure for readability**: Improve flow and organization
5. **Add tables**: Convert lists of parameters to tables
6. **Add tags**: Add relevant `#tags` throughout document

**Only use this mode when**:
- User explicitly says "summarize" or "compress"
- User asks for "key points" or "main conclusions"
- User requests "executive summary" version

### Metadata Enhancement

Add frontmatter with:
- Document title and author
- Creation date
- Document type (report, memo, etc.)
- Category
- Tags (for filtering)
- Status (completed, in-progress, etc.)
- Custom properties (coordinates, IDs, etc.)

### Navigation Enhancement

- Create index notes with links to main document
- Add table of contents at top of long documents
- Use `#` tags for cross-referencing
- Link related sections within document: `[[#Section Name]]`

## Image Processing

### Extraction Workflow

1. **Unpack DOCX**: DOCX is a ZIP file containing XML and media
2. **Locate media folder**: Usually at `unpacked_docx/word/media/`
3. **Copy to attachments**: Move all images to `obsidian_vault/_attachments/`
4. **Update references**: Change `media/` to `_attachments/` in Markdown
5. **Verify paths**: Ensure all images link correctly

### Image Format Preservation

- Keep original formats (JPEG, PNG)
- Do not convert or re-encode
- Preserve original filenames (image1.jpeg, image2.png, etc.)

## File Organization

Standard Obsidian vault structure:

```
obsidian_vault/
├── README.md (index and navigation)
├── Main Document.md
├── metadata.json (optional structured metadata)
└── _attachments/
    ├── image1.jpeg
    ├── image2.png
    └── ...
```

### Optional Reference Files

Create additional notes as needed:

- `使用指南.md` - User guide in Chinese
- `索引.md` - Index for Chinese content
- `metadata.json` - Structured data for automation

## Common Conversion Patterns

### Technical Reports

**Preserve Mode** (default):
- Keep all sections, data, and conclusions unchanged
- Add YAML frontmatter (title, date, author, tags)
- Update image paths only
- Add tags for technical terms in frontmatter
- Do NOT summarize or rewrite content

**Summarize Mode** (explicit request only):
- Use callout boxes for conclusions and recommendations
- Format data and parameters in tables
- Highlight key findings
- Condense methodology sections

### Academic Papers

**Preserve Mode** (default):
- Keep abstract, methodology, results, discussion intact
- Preserve all references exactly as-is
- Add DOI/URL in frontmatter (metadata only)
- Format equations properly (preserve mathematical content)
- Add tags for key concepts

**Summarize Mode** (explicit request only):
- Format abstract as quote block
- Summarize methodology as callout
- Format results as tables
- Condense discussion to key points
- Keep references list but can highlight important ones

### Meeting Minutes

**Preserve Mode** (default):
- Keep all discussion points verbatim
- Preserve all action items exactly as stated
- Keep all decisions and outcomes
- Add YAML frontmatter (participants, date, time)
- Format action items as task lists `- [ ]` (original text only)

**Summarize Mode** (explicit request only):
- Highlight key decisions in callouts
- Summarize main discussion topics
- Condense action items
- Create summary of outcomes

## Quality Checklist

Before completing conversion, verify:

### Mode Verification
- [ ] User preference confirmed (preserve or summarize)
- [ ] Correct mode applied (preserve = full content / summarize = condensed)
- [ ] No unintended summarization in preserve mode
- [ ] No content addition in preserve mode beyond metadata

### Content Integrity
- [ ] All content preserved from original DOCX (preserve mode) OR
- [ ] Key points accurately summarized (summarize mode only)
- [ ] No broken or incomplete sections
- [ ] Tables and charts preserved intact (preserve mode)

### Obsidian Features
- [ ] All images extracted and linked correctly
- [ ] YAML frontmatter complete
- [ ] Tags added for navigation (don't alter content)
- [ ] Internal links working (pointing to existing content)
- [ ] No broken image references

### Formatting
- [ ] Tables formatted properly (preserve original data)
- [ ] Callouts used appropriately (summarize mode only or metadata only)
- [ ] Markdown syntax correct
- [ ] Image captions preserved (preserve mode)

### Final Verification (Preserve Mode Only)
- [ ] No text rewritten or paraphrased
- [ ] No paragraphs combined or shortened
- [ ] No sections compressed or condensed
- [ ] Original structure maintained
- [ ] All original headings preserved
- [ ] No "key points" or "summary" added
- [ ] No content deletion

### Final Verification (Summarize Mode Only)
- [ ] Main points captured accurately
- [ ] Conclusions highlighted
- [ ] Data preserved in tables
- [ ] Readability improved
- [ ] Key recommendations identified

## Troubleshooting

### Images Not Displaying

Ensure:
- `_attachments/` folder exists in vault
- Image paths use `_attachments/` prefix
- Image filenames match exactly (case-sensitive)

### Pandoc Not Found

Install pandoc:
```bash
# Windows
winget install pandoc

# Or download from: https://pandoc.org/installing.html
```

### Encoding Issues

Use pandoc with proper encoding:
```bash
pandoc --from docx --to markdown --output-file output.md input.docx
```

### Large Documents

For very large DOCX files:
- Process sections separately
- Consider using `--toc` to generate table of contents
- Split into multiple linked notes

## Advanced Features

### Metadata JSON Generation

Create structured metadata for automation:

```json
{
  "title": "Document Title",
  "author": "Author",
  "date": "2025-01-13",
  "tags": ["tag1", "tag2"],
  "sections": [...],
  "images": [...]
}
```

### Automated Link Generation

Use sed or similar tools to automate:
- Section links: `[[#Section Name]]`
- Image path updates: `media/` → `_attachments/`
- Tag insertion: Add `#tag` patterns

### Batch Processing

Convert multiple documents:
```bash
for file in *.docx; do
    # Run conversion pipeline
done
```

## References

For detailed Obsidian Markdown syntax, see:
- Obsidian Help: https://help.obsidian.md/syntax
- Obsidian Links: https://help.obsidian.md/links
- Callouts: https://help.obsidian.md/callouts
- Properties: https://help.obsidian.md/properties

## Summary

This skill provides a complete pipeline for DOCX to Obsidian conversion with emphasis on:

1. **User preference priority**: ALWAYS ask preserve vs. summarize before starting
2. **Content integrity**: Preserve 100% of content in preserve mode (default)
3. **Feature enhancement**: Add Obsidian-specific features without altering content
4. **Image handling**: Proper extraction and linking
5. **Navigation**: Links, tags, indexes for easy navigation
6. **Quality control**: Mode-specific checklists and verification steps

**CRITICAL RULES**:

✅ **ALWAYS** ask user: "Preserve all content or summarize?"
✅ **DEFAULT** to "preserve all content" if user doesn't specify
✅ **NEVER** summarize, compress, or rewrite in preserve mode
✅ **ONLY** add metadata, tags, image links in preserve mode
✅ **ONLY** summarize when user explicitly requests it

**PROHIBITED in preserve mode**:
❌ Summarizing sections or paragraphs
❌ Rewriting or rephrasing text
❌ Combining bullet points
❌ Creating "key points" lists
❌ Adding callouts that restructure content
❌ Modifying table or chart data
❌ Compressing any content
❌ Adding conclusions not in original

---

**Skill Version**: 1.1
**Last Updated**: 2025-01-13
**Changes in v1.1**: Added user preference prompt with two conversion modes (preserve vs. summarize)
