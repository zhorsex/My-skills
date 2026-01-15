# 输出模式 (Output Patterns)

当技能需要产生一致且高质量的输出时，请使用这些模式。

## 模板模式 (Template Pattern)

提供输出格式的模板。根据你的需求匹配严格程度。

**针对严格要求（如 API 响应或数据格式）：**

```markdown
## 报告结构

始终使用此确切的模板结构：

# [分析标题]

## 执行摘要
[关键发现的一段话概览]

## 关键发现
- 发现 1 及其支撑数据
- 发现 2 及其支撑数据
- 发现 3 及其支撑数据

## 建议
1. 具体的、可操作的建议
2. 具体的、可操作的建议
```

**针对灵活指导（当适应性有用时）：**

```markdown
## 报告结构

这是一个合理的默认格式，但请运用你的最佳判断：

# [分析标题]

## 执行摘要
[概览]

## 关键发现
[基于你的发现调整章节]

## 建议
[根据具体的上下文量身定制]

根据特定的分析类型，按需调整章节。
```

## 示例模式 (Examples Pattern)

对于输出质量取决于查看示例的技能，请提供输入/输出对：

```markdown
## Commit 消息格式

遵循以下示例生成 commit 消息：

**示例 1：**
输入：使用 JWT 令牌添加了用户身份验证
输出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**示例 2：**
输入：修复了报告中日期显示不正确的 bug
输出：
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

遵循此风格：type(scope): 简短描述，然后是详细说明。
```

示例能比单纯的描述更清晰地帮助 Claude 理解所需的风格和详细程度。
