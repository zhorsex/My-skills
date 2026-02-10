// Mock helper functions for testing

/**
 * Mock skill content for testing
 */
export function mockSkillContent() {
  return {
    hasTerminology: true,
    hasCharts: false,
    chapterCount: 10,
    targetWordCount: 3000,
  };
}

/**
 * Mock chapter data for testing
 */
export function mockChapterData() {
  return {
    title: "第1章 项目背景与目标",
    content: "这是第一章的内容...",
    wordCount: 2000,
    modificationCount: 2,
    satisfaction: 4,
  };
}

/**
 * Mock user feedback for testing
 */
export function mockFeedback() {
  return {
    feedbackId: "FB001",
    reportId: "RPT001",
    chapter: "第1章",
    userEvaluation: "⭐⭐⭐⭐ 5星",
    modificationCount: 0,
    modificationType: "-",
    userComments: "完全符合，继续下一章",
    processingResult: "已确认",
  };
}

/**
 * Mock usage data for testing
 */
export function mockUsageData() {
  return {
    reportId: "RPT001",
    reportTitle: "河南省沿黄流域风电场地质调查报告",
    reportType: "工程技术报告",
    targetAudience: "项目评审专家",
    totalChapters: 10,
    totalWords: 15000,
    totalTime: 300, // minutes
    status: "完成",
  };
}

/**
 * Mock chart configuration for testing
 */
export function mockChartConfig() {
  return {
    chartId: "CH001",
    chartType: "柱状图",
    applicationScenario: "不同型号风机参数对比",
    usageCount: 12,
    userRating: 5,
    colorScheme: "steelblue, coral",
  };
}

/**
 * Mock terminology entry for testing
 */
export function mockTerminologyEntry() {
  return {
    term: "风力发电机组",
    unifiedDefinition: "将风能转换为电能的整套设备系统，包括风轮、发电机、控制系统等",
    usageFrequency: "高",
    usageScenario: "风电场设计、设备选型",
    userRating: 5,
  };
}

/**
 * Mock search strategy for testing
 */
export function mockSearchStrategy() {
  return {
    level: "Level 2: 标准搜索",
    materialCount: "3-5个",
    timeBudget: "8-10分钟",
    sourcePriority: "国家标准/行业标准 → 官方技术白皮书 → 行业报告 → 学术论文摘要",
    validationStandard: "至少2个来源一致、数据有时间标注",
  };
}

/**
 * Assert that a file exists
 */
export async function assertFileExists(filePath: string): Promise<boolean> {
  try {
    await Bun.file(filePath).text();
    return true;
  } catch {
    return false;
  }
}

/**
 * Assert that a file contains specific content
 */
export async function assertFileContains(filePath: string, content: string): Promise<boolean> {
  try {
    const fileContent = await Bun.file(filePath).text();
    return fileContent.includes(content);
  } catch {
    return false;
  }
}

/**
 * Clean up test artifacts
 */
export function cleanupTestFiles() {
  // This would be called after tests to clean up any test-generated files
  console.log("Cleanup: Removing test artifacts");
}
