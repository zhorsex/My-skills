import { test, expect } from "bun:test";

test("skill directory structure exists", () => {
  // Check that main directories exist
  expect(() => import.meta.resolve("./SKILL.md")).toExist();
  expect(() => import.meta.resolve("./references")).toExist();
  expect(() => import.meta.resolve("./scripts")).toExist();
  expect(() => import.meta.resolve("./iteration")).toExist();
});

test("iteration subdirectories exist", () => {
  // Check that iteration subdirectories exist
  expect(() => import.meta.resolve("./iteration/patterns")).toExist();
  expect(() => import.meta.resolve("./iteration/cache")).toExist();
  expect(() => import.meta.resolve("./iteration/evaluations")).toExist();
  expect(() => import.meta.resolve("./iteration/suggestions")).toExist();
  expect(() => import.meta.resolve("./iteration/shared")).toExist();
  expect(() => import.meta.resolve("./iteration/local")).toExist();
});

test("reference files exist", () => {
  // Check that reference files exist
  expect(() => import.meta.resolve("./references/engineering-terms.md")).toExist();
  expect(() => import.meta.resolve("./references/citation-sources.md")).toExist();
  expect(() => import.meta.resolve("./references/chart-patterns.md")).toExist();
});

test("SKILL.md has proper structure", async () => {
  const skillMd = await Bun.file("SKILL.md").text();
  
  // Check YAML frontmatter
  expect(skillMd).toContain("name: report-generator");
  expect(skillMd).toContain("description:");
  
  // Check for main sections
  expect(skillMd).toMatch(/## /);
  
  // Check for workflow phases
  expect(skillMd).toContain("阶段1");
  expect(skillMd).toContain("阶段2");
  expect(skillMd).toContain("阶段3");
  expect(skillMd).toContain("阶段4");
});

test("iteration template files exist", () => {
  // Check that iteration template files exist
  expect(() => import.meta.resolve("./iteration/feedback-log.md")).toExist();
  expect(() => import.meta.resolve("./iteration/usage-log.md")).toExist();
  expect(() => import.meta.resolve("./iteration/search-strategies.md")).toExist();
  expect(() => import.meta.resolve("./iteration/patterns/chapter-templates.md")).toExist();
  expect(() => import.meta.resolve("./iteration/patterns/common-terms.md")).toExist();
  expect(() => import.meta.resolve("./iteration/patterns/chart-configs.md")).toExist();
  expect(() => import.meta.resolve("./iteration/patterns/writing-styles.md")).toExist();
  expect(() => import.meta.resolve("./iteration/suggestions/update-proposals.md")).toExist();
});

test("scripts exist and are valid", () => {
  // Check that script files exist
  expect(() => import.meta.resolve("./scripts/generate_chart.py")).toExist();
  expect(() => import.meta.resolve("./scripts/cache_manager.py")).toExist();
  expect(() => import.meta.resolve("./scripts/analyze_usage.py")).toExist();
  expect(() => import.meta.resolve("./scripts/README.md")).toExist();
});
