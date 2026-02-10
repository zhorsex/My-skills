import { test, expect, describe } from "bun:test";
import { execSync } from "child_process";

describe("Outline Integration Tests", () => {
  
  test("end-to-end outline generation workflow", () => {
    // 1. Generate an outline
    const generateResult = execSync('python scripts/generate_outline.py --input "风电场地质调查报告" --mode quick --template OT101 --output e2e-integration-test.md', {
      encoding: "utf-8"
    });
    
    expect(generateResult.status).toBe(0);
    expect(Bun.file("e2e-integration-test.md").exists()).toBeTruthy();
    
    // 2. Edit the outline (add a chapter)
    const editResult = execSync('python scripts/outline_editor.py --add-chapter "现场采样与测试" --after 5 --input e2e-integration-test.md --output e2e-integration-edited.md', {
      encoding: "utf-8"
    });
    
    expect(editResult.status).toBe(0);
    expect(Bun.file("e2e-integration-edited.md").exists()).toBeTruthy();
    
    // Verify new chapter exists
    const editedContent = Bun.file("e2e-integration-edited.md").text();
    expect(editedContent).toContain("现场采样与测试");
    
    // 3. List outlines
    const listResult = execSync("python scripts/outline_manager.py --list", {
      encoding: "utf-8"
    });
    
    expect(listResult.status).toBe(0);
    expect(listResult.stdout).toContain("大纲文件列表");
    
    // 4. Search outlines
    const searchResult = execSync('python scripts/outline_manager.py --search "地质调查"', {
      encoding: " "utf-8"
    });
    
    expect(searchResult.status).toBe(0);
    expect(searchResult.stdout).toContain("搜索结果");
    
    // 5. Check outline metadata
    const showResult = execSync("python scripts/outline_manager.py --show e2e-integration-edited.md", {
      encoding: "utf-8"
    });
    
    expect(showResult.status).toBe(0);
    expect(showResult.stdout).toContain("元数据");
    expect(showResult.stdout).toContain("章节数量");
    
    // Cleanup
    execSync("rm e2e-integration-test.md");
    execSync("rm e2e-integration-edited.md");
  });
  
  test("outline format compatibility with report-generator", () => {
    // Generate a test outline
    const result = execSync('python scripts/generate_outline.py --input "兼容性测试" --mode quick --output compatibility-test.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    
    const content = Bun.file("compatibility-test.md").text();
    
    // Verify Markdown format
    expect(content).toMatch(/^#\s+/);  // Has title
    expect(content).toMatch(/## 元数据/);  // Has metadata section
    expect(content).toMatch(/### 第\d+章/);  // Has chapters
    expect(content).toMatch(/#### \d+(\.\d*?)?\s+/);  // Has sections
    
    // Verify structure hierarchy
    const chapterMatches = content.match(/### 第\d+章/g) || [];
    expect(chapterMatches.length).toBeGreaterThan(0);
    
    // Verify metadata completeness
    expect(content).toContain("生成时间");
    expect(content).toContain("生成模式");
    expect(content).toContain("使用模板");
    
    // Cleanup
    execSync("rm compatibility-test.md");
  });
  
  test("outline supports Chinese content", () => {
    const result = execSync('python scripts/generate_outline.py --input "中文测试报告" --mode quick --output chinese-test.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    const content = Bun.file("chinese-test.md").text();
    
    expect(content).toContain("中文测试报告");
    expect(content).toContain("项目背景");
    expect(content).toContain("技术方案");
    
    // Cleanup
    execSync("rm chinese-test.md");
  });
  
  test("outline handles special characters in titles", () => {
    const result = execSync('python scripts/generate_outline.py --input "技术方案（含特殊字符：#、@、&）" --mode quick --output special-chars-test.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    const content = Bun.file("special-chars-test.md").text();
    
    expect(content).toContain("技术方案（含特殊字符：#、@、&）");
    
    // Cleanup
    execSync("rm special-chars-test.md");
  });
  
  test("outline_editor preserves metadata", () => {
    // First generate an outline
    execSync('python scripts/generate_outline.py --input "元数据测试" --mode quick --output metadata-test.md', {
      encoding: "utf-8"
    });
    
    // Add a chapter
    const editResult = execSync('python scripts/outline_editor.py --add-chapter "新增章节" --after 2 --input metadata-test.md --output metadata-edited.md', {
      encoding: "utf-8"
    });
    
    expect(editResult.status).toBe(0);
    
    // Verify metadata is preserved
    const originalContent = Bun.file("metadata-test.md").text();
    const editedContent = Bun.file("metadata-edited.md").text();
    
    expect(originalContent).toContain("元数据");
    expect(editedContent).toContain("元数据");
    
    expect(editedContent).toContain("新增章节");
    
    // Cleanup
    execSync("rm metadata-test.md");
    execSync("rm metadata-edited.md");
  });
  
  test("outline_manager handles non-existent files gracefully", () => {
    // Try to show a non-existent outline
    const result = execSync("python scripts/outline_manager.py --show non-existent.md", {
      encoding: "utf-8"
    });
    
    // Should not crash, but return error code
    expect(result.status).not.toBe(0);
    expect(result.stderr).toContain("文件不存在");
  });
  
  test("template fallback provides valid outline", () => {
    // Use a template ID that doesn't exist to trigger fallback
    const result = execSync('python scripts/generate_outline.py --input "回退测试" --mode quick --template INVALID_ID --output fallback-test.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(Bun.file("fallback-test.md").exists()).toBeTruthy();
    
    const content = Bun.file("fallback-test.md").text();
    
    // Verify fallback generated valid structure
    expect(content).toMatch(/### 第\d+章/);
    expect(content).toContain("元数据");
    expect(content).toContain("建议章节数量"); // Enhanced recommendations should still be generated
    
    // Cleanup
    execSync("rm fallback-test.md");
  });
  
  test("outline templates are accessible", () => {
    // Check standard templates
    expect(() => Bun.file("iteration/outline-templates/standard-outline-templates.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/index.md").exists()).toBeTruthy();
    
    // Check industry templates
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/geological-survey.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/engineering-design.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/environmental-assessment.md").exists()).toBeTruthy();
    
    // Verify template content
    const geoTemplate = Bun.file("iteration/outline-templates/industry-outlines/geological-survey.md").text();
    expect(geoTemplate).toContain("OT101");
    expect(geoTemplate).toContain("地质调查报告");
    expect(geoTemplate).toContain("章节结构");
    
    const engTemplate = Bun.file("iteration/outline-templates/industry-outlines/engineering-design.md").text();
    expect(engTemplate).toContain("OT102");
    expect(engTemplate).toContain("工程设计方案");
  });
  
  test("all scripts have help documentation", () => {
    // Check that all scripts support --help
    const scripts = [
      "generate_outline.py",
      "outline_editor.py",
      "outline_manager.py"
    ];
    
    scripts.forEach(script => {
      const result = execSync(`python scripts/${script} --help`, {
        encoding: "utf-8"
      });
      
      expect(result.status).toBe(0);
      expect(result.stdout.length).toBeGreaterThan(0);
    });
  });
  
  test("outline history management", () => {
    // Generate an outline
    execSync('python scripts/generate_outline.py --input "历史测试" --mode quick --output history-test.md', {
      encoding: "utf-8"
    });
    
    // Check history
    const historyResult = execSync('python scripts/outline_manager.py --history history-test.md', {
      encoding: "utf-8"
    });
    
    expect(historyResult.status).toBe(0);
    // Should have history entry or message about no history
    
    // Cleanup
    execSync("rm history-test.md");
  });
  
});
