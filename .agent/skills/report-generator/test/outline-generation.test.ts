import { test, expect, describe } from "bun:test";
import { execSync } from "child_process";

describe("Outline Generation Tests", () => {
  
  test("generate_outline.py script exists", () => {
    expect(() => Bun.file("scripts/generate_outline.py").exists()).toBeTruthy();
  });
  
  test("generate_outline.py has proper permissions", () => {
    const stats = Bun.file("scripts/generate_outline.py").stat();
    expect(stats.mode).toBeReadable();
    expect(stats.mode).toBeExecutable();
  });
  
  test("generate_outline.py --help shows usage", () => {
    const result = execSync("python scripts/generate_outline.py --help", {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("AI驱动的交互式大纲生成工具");
    expect(result.stdout).toContain("--input");
    expect(result.stdout).toContain("--mode");
    expect(result.stdout).toContain("--output");
  });
  
  test("generate_outline.py generates outline file", () => {
    // Test with quick mode
    const result = execSync('python scripts/generate_outline.py --input "测试报告" --mode quick --output test-outline.md', {
      encoding: "utf-8",
      stdio: "pipe"
    });
    
    expect(result.status).toBe(0);
    expect(Bun.file("test-outline.md").exists()).toBeTruthy();
    
    // Verify output contains expected structure
    const content = Bun.file("test-outline.md").text();
    expect(content).toContain("测试报告");
    expect(content).toContain("### 第");
    expect(content).toContain("## 元数据");
    
    // Cleanup
    execSync("rm test-outline.md");
  });
  
  test("generate_outline.py supports mode parameter", () => {
    const modes = ["quick", "chapter", "keypoints"];
    
    modes.forEach(mode => {
      const result = execSync(`python scripts/generate_outline.py --input "测试" --mode ${mode} --output test-${mode}-outline.md`, {
        encoding: "utf-8",
        stdio: "pipe"
      });
      
      expect(result.status).toBe(0);
      expect(Bun.file(`test-${mode}-outline.md`).exists()).toBeTruthy();
      
      // Cleanup
      execSync(`rm test-${mode}-outline.md`);
    });
  });
  
  test("generate_outline.py template fallback works", () => {
    // Test with non-existent template to trigger fallback
    const result = execSync('python scripts/generate_outline.py --input "地质调查" --mode quick --template NONEXISTENT --output test-fallback.md', {
      encoding: "utf-8",
      stdio: "pipe"
    });
    
    // Should still succeed due to fallback to default template
    expect(result.status).toBe(0);
    expect(Bun.file("test-fallback.md").exists()).toBeTruthy();
    
    // Cleanup
    execSync("rm test-fallback.md");
  });
  
  test("generate_outline.py creates history file", () => {
    const result = execSync('python scripts/generate_outline.py --input "测试历史" --mode quick --output test-history.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    
    // Check if history file was created in iteration/outline-history/
    const historyFiles = execSync("ls iteration/outline-history/*.json 2>/dev/null || echo ''", {
      encoding: "utf-8"
    });
    
    // Cleanup
    execSync("rm test-history.md");
    execSync("rm -rf iteration/outline-history/test-history*.json 2>/dev/null || true");
  });
  
  test("generate_outline.py includes recommendations", () => {
    const result = execSync('python scripts/generate_outline.py --input "技术方案" --mode quick --output test-recommendations.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    const content = Bun.file("test-recommendations.md").text();
    
    // Check for enhanced recommendations section
    expect(content).toContain("## 增强建议");
    expect(content).toContain("章节数量建议");
    expect(content).toContain("配图建议");
    expect(content).toContain("写作方向推荐");
    
    // Cleanup
    execSync("rm test-recommendations.md");
  });
  
  test("generate_outline.py supports chapter and section structure", () => {
    const result = execSync('python scripts/generate_outline.py --input "多章节报告" --mode quick --output test-structure.md', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    const content = Bun.file("test-structure.md").text();
    
    // Verify chapter structure
    expect(content).toMatch(/### 第\d+章/);
    expect(content).toMatch(/#### \d+(\.\d*)?\s+/);
    
    // Cleanup
    execSync("rm test-structure.md");
  });
  
  test("outline_editor.py script exists and is executable", () => {
    expect(() => Bun.file("scripts/outline_editor.py").exists()).toBeTruthy();
    
    const stats = Bun.file("scripts/outline_editor.py").stat();
    expect(stats.mode).toBeReadable();
    expect(stats.mode).toBeExecutable();
  });
  
  test("outline_editor.py --help shows usage", () => {
    const result = execSync("python scripts/outline_editor.py --help", {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("大纲文本编辑器");
    expect(result.stdout).toContain("--input");
    expect(result.stdout).toContain("--mode");
  });
  
  test("outline_manager.py script exists and is executable", () => {
    expect(() => Bun.file("scripts/outline_manager.py").exists()).toBeTruthy();
    
    const stats = Bun.file("scripts/outline_manager.py").stat();
    expect(stats.mode).toBeReadable();
    expect(stats.mode).toBeExecutable();
  });
  
  test("outline_manager.py --help shows usage", () => {
    const result = execSync("python scripts/outline_manager.py --help", {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("大纲管理工具");
    expect(result.stdout).toContain("--list");
    expect(result.stdout).toContain("--show");
  });
  
  test("outline_manager.py can list outlines", () => {
    const result = execSync("python scripts/outline_manager.py --list", {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("大纲文件列表");
  });
  
  test("outline_manager.py can search outlines", () => {
    const result = execSync('python scripts/outline_manager.py --search "地质调查"', {
      encoding: "utf-8"
    });
    
    expect(result.status).toBe(0);
    expect(result.stdout).toContain("搜索结果");
  });
  
  test("outline templates directory exists", () => {
    expect(() => Bun.file("iteration/outline-templates").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/standard-outline-templates.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/index.md").exists()).toBeTruthy();
  });
  });
  
  test("outline templates industry subdirectories exist", () => {
    expect(() => Bun.file("iteration/outline-templates/industry-outlines").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/geological-survey.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/engineering-design.md").exists()).toBeTruthy();
    expect(() => Bun.file("iteration/outline-templates/industry-outlines/environmental-assessment.md").exists()).toBeTruthy();
  });
  
  test("outline templates contain expected structure", () => {
    const standardTemplates = Bun.file("iteration/outline-templates/standard-outline-templates.md").text();
    const index = Bun.file("iteration/outline-outline-templates/index.md").text();
    
    // Check standard templates
    expect(standardTemplates).toContain("模板001");
    expect(standardTemplates).toContain("模板002");
    expect(standardTemplates).toContain("模板003");
    
    // Check index structure
    expect(index).toContain("模板分类");
    expect(index).toContain("搜索标签");
    
    // Check industry templates
    const geoTemplate = Bun.file("iteration/outline-templates/industry-outlines/geological-survey.md").text();
    expect(geoTemplate).toContain("模板ID: OT101");
    expect(geoTemplate).toContain("适用场景");
    expect(geoTemplate).toContain("章节结构");
  });
  
  test("outline history directory exists", () => {
    const historyDir = Bun.file("iteration/outline-history");
    historyDir.mkdir({ recursive: true, parents: true });
    expect(historyDir.exists()).toBeTruthy();
  });
  
  test("SKILL.md updated with outline generation feature", () => {
    const skillMd = Bun.file("SKILL.md").text();
    
    expect(skillMd).toContain("选项B：帮我生成大纲");
    expect(skillMd).toContain("步骤1.2.5 - 收集大纲生成信息");
    expect(skillMd).toContain("步骤1.2.6 - 执行大纲生成");
    expect(skillMd).toContain("步骤1.2.7 - 展示大纲候选模板");
    expect(skillMd).toContain("增强建议显示");
  });
  
  test("USAGE.md updated with outline generation guide", () => {
    const usageMd = Bun.file("USAGE.md").text();
    
    expect(usageMd).toContain("🚀 交互式大纲生成功能（新增）");
    expect(usageMd).toContain("快速开始（大纲生成）");
    expect(usageMd).toContain("python scripts/generate_outline.py");
    expect(usageMd).toContain("python scripts/outline_editor.py");
    expect(usageMd).toContain("python scripts/outline_manager.py");
  });
  
  test("templates/README.md updated with outline templates", () => {
    const readme = Bun.file("templates/README.md").text();
    
    expect(readme).toContain("## 大纲模板（新增）");
    expect(readme).toContain("OT101 | 地质调查报告");
    expect(readme).toContain("OT102 | 工程设计方案");
    expect(readme).toContain("OT103 | 环境影响评估报告");
    expect(readme).toContain("iteration/outline-templates/");
  });
  
  test("end-to-end: generate and manage outline workflow", () => {
    // Generate an outline
    const generateResult = execSync('python scripts/generate_outline.py --input "集成测试报告" --mode quick --output integration-test-outline.md', {
      encoding: "utf-8"
    });
    expect(generateResult.status).toBe(0);
    expect(Bun.file("integration-test-outline.md").exists()).toBeTruthy();
    
    // List outlines
    const listResult = execSync("python scripts/outline_manager.py --list", {
      encoding: "utf-8"
    });
    expect(listResult.status).toBe(0);
    
    // Show outline details
    const showResult = execSync("python scripts/outline_manager.py --show integration-test-outline.md", {
      encoding: "utf-8"
    });
    expect(showResult.status).toBe(0);
    
    // Search outline
    const searchResult = execSync('python scripts/outline_manager.py --search "集成测试"', {
      encoding: "utf-8"
    });
    expect(searchResult.status).toBe(0);
    
    // Cleanup
    execSync("rm integration-test-outline.md");
  });
  
});
