# -*- coding: utf-8 -*-
"""Task definitions for the AI News Aggregator."""

from datetime import datetime
from crewai import Task, Agent
from tools.news_sources import NEWS_SOURCES, AI_CATEGORIES


def create_scraping_task(agent: Agent) -> Task:
    """Create the web scraping task."""
    sources_list = "\n".join([f"- {s['name']}: {s['url']}" for s in NEWS_SOURCES])

    return Task(
        description=f"""Collect the latest news articles from the following sources:

{sources_list}

For each source:
1. Use the ai_news_scraper tool to collect up to 5 articles per source
2. Extract the title, URL, description, and date for each article
3. Focus on articles about politics, finance, AI, trade, retail, pet industry, medical aesthetics, and related topics
4. Include articles from all these categories

Compile all collected articles into a structured list.

注意：所有内容（包括韩文、英文）请保留原文，后续环节会统一翻译。""",
        expected_output="""A structured list of collected articles in the following format:

COLLECTED ARTICLES
==================

Source: [Source Name]
1. Title: [Article Title]
   URL: [Article URL]
   Description: [Brief description]
   Date: [Publication date]

2. Title: ...
   ...

(Continue for all sources and articles)

Total articles collected: [number]""",
        agent=agent,
    )


def create_summarization_task(agent: Agent, context: list) -> Task:
    """Create the summarization task."""
    return Task(
        description="""Review the collected news articles and create concise summaries.

For each article:
1. Read the title and available description
2. Create a 2-3 sentence summary capturing the key points
3. Identify the main topic and significance
4. Note any mentioned companies, technologies, or researchers

Focus on:
- What happened or was announced
- Why it matters for its field
- Key technical details if available

请将所有摘要以中文输出。如果原文是韩文或英文，请先翻译成中文再生成摘要。""",
        expected_output="""Summarized articles in the following format:

文章摘要
========

1. [原标题]
   来源: [来源名称]
   摘要: [2-3句话的核心要点]
   关键主题: [涉及的主要话题]
   意义: [为什么重要]

2. [原标题]
   ...

(为所有文章继续)""",
        agent=agent,
        context=context,
    )


def create_categorization_task(agent: Agent, context: list) -> Task:
    """Create the categorization task."""
    categories_list = "\n".join([f"- {cat}" for cat in AI_CATEGORIES])

    return Task(
        description=f"""Categorize the summarized news articles into appropriate topics.

Available categories:
{categories_list}

For each article:
1. Analyze the summary and key topics
2. Assign one primary category
3. Assign up to 2 secondary categories if applicable
4. Group articles by their primary category

Consider:
- The main focus of the article
- Technologies mentioned
- Application domain
- Research vs. industry focus""",
        expected_output="""Categorized articles organized by topic:

分类新闻
========

## 中国政策与宏观
1. [文章标题]
   摘要: [简要摘要]
   次要分类: [如果有]

2. ...

## 宠物食品行业
...

## 零售与电商
...

## 韩国经济与市场
...

## 全球医美趋势
...

## AI与产业结合
...

## 国际贸易与关税
...

## 香港政策与贸易
...

## 其他值得关注
...

分类统计:
- 中国政策与宏观: X 篇
- 宠物食品行业: Y 篇
- ...

热门话题: [所有文章中最常见的主题列表]""",
        agent=agent,
        context=context,
    )


def create_analysis_task(agent: Agent, context: list) -> Task:
    """Create the deep analysis task."""
    return Task(
        description="""对分类后的新闻进行深度分析。请从每个分类中挑选最重要的 2-3 条新闻，进行深入分析。

分析步骤：
1. 从每个分类中筛选出最重要的 2-3 条新闻（判断标准：影响范围、与宠物食品/零售贸易/医美/香港业务的相关性、事件的重要性）
2. 对每条选中的新闻，使用搜索工具查找相关背景资料
3. 分析事件的深层原因、潜在影响和未来趋势

每条新闻的分析要包含：
- 背景调查：这件事的来龙去脉，相关方是谁，有没有历史先例
- 影响评估：对行业、市场、普通人的影响
- 趋势判断：这是孤立事件还是趋势开始，未来值得关注什么
- 业务关联：如果与宠物食品、零售贸易、医美、香港政策与贸易相关，特别说明其商业影响

特别关注以下方向：
- 宠物食品行业的国内零售、出口形势、行业标准、竞品动态
- 韩国经济与市场动态，对医美推广业务的影响
- 全球医美趋势（东亚、日韩、欧美）
- 香港政策与贸易，尤其是转口贸易和宠物相关政策
- AI与实体产业的结合

要求：
- 每条新闻的分析约 200-300 字
- 分析要基于事实，观点客观
- 输出语言为中文，不得出现韩文或英文原文
- 优先分析宠物食品行业、韩国经济与市场、全球医美趋势、香港政策与贸易、中国政策与宏观类别的新闻""",
        expected_output="""深度分析报告，格式如下：

# 深度分析

## 宠物食品行业
### [新闻标题]
- **背景**：[来龙去脉，200字左右]
- **影响**：[潜在影响，100字左右]
- **趋势**：[未来判断，100字左右]

（如果有业务关联，额外加一行）
- **业务关联**：[说明]

## 韩国经济与市场
### [新闻标题]
（同上格式）

## 全球医美趋势
### [新闻标题]
（同上格式）

## 香港政策与贸易
### [新闻标题]
（同上格式）

## 中国政策与宏观
### [新闻标题]
（同上格式）

## AI与产业结合
### [新闻标题]
（同上格式）""",
        agent=agent,
        context=context,
    )


def create_reporting_task(agent: Agent, context: list) -> Task:
    """Create the reporting task."""
    current_date = datetime.now().strftime("%Y-%m-%d")

    return Task(
        description=f"""Create a comprehensive daily news report by combining all the collected, summarized, categorized, and analyzed information.

IMPORTANT: Today's date is {current_date}. Use this date in the report.

The report should include:
1. 执行摘要 - 当日重点新闻概览
2. 今日头条 - 最重要的 3-5 条新闻
3. 分类新闻 - 按类别整理的新闻
4. 趋势观察 - 观察到的模式和主题
5. 值得关注 - 提到的公司、人物、产品

执行摘要要求（非常重要）：
- 用一句话概括每条重要新闻，每条不超过 50 字
- 列出 5-8 条最重要的新闻
- 每条一行，用列表形式
- 不要写成段落
- 要让读者 5 秒内扫完

报告要求：
- 专业、结构清晰
- 通俗易懂
- 全部使用中文
- 报告中不得出现韩文或英文原文

输出格式要求（非常重要）：
- 必须输出完整的 HTML 代码，不要用 Markdown
- 使用 <h1>、<h2>、<h3> 做标题
- 使用 <ul>、<li> 做列表
- 使用 <strong> 加粗重点内容
- 使用 <span class="highlight"> 高亮关键信息
- 使用 <div class="section"> 包裹每个章节
- 在 HTML 开头包含完整的 <style> 样式

请特别关注以下业务方向：
- 宠物食品行业的国内零售、出口形势
- 韩国经济与市场动态
- 全球医美趋势
- 香港政策与贸易
- AI与实体产业的结合
- 中国政策变化""",
        expected_output=f"""完整的 HTML 代码，格式如下：

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: -apple-system, "Microsoft YaHei", sans-serif;
        color: #333;
        line-height: 1.8;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }}
    h1 {{
        color: #1a5490;
        border-bottom: 3px solid #1a5490;
        padding-bottom: 10px;
    }}
    h2 {{
        color: #2e75b6;
        border-left: 5px solid #2e75b6;
        padding-left: 12px;
        margin-top: 35px;
    }}
    h3 {{
        color: #c55a11;
        margin-top: 25px;
    }}
    .highlight {{
        background-color: #fff3cd;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: 600;
        color: #856404;
    }}
    .section {{
        margin-bottom: 30px;
    }}
    ul {{
        padding-left: 25px;
    }}
    li {{
        margin-bottom: 8px;
    }}
    .summary-list {{
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px 25px;
        border-left: 4px solid #2e75b6;
    }}
    .summary-list li {{
        font-size: 1.05em;
        line-height: 1.9;
        margin-bottom: 10px;
    }}
    .source {{
        color: #888;
        font-size: 0.9em;
    }}
    .date {{
        color: #666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }}
</style>
</head>
<body>

<h1>每日新闻简报</h1>
<div class="date">日期: {current_date}</div>

<div class="section">
<h2>执行摘要</h2>
<ul class="summary-list">
<li>[一句话新闻1，不超过50字]</li>
<li>[一句话新闻2]</li>
<li>[一句话新闻3]</li>
<li>[一句话新闻4]</li>
<li>[一句话新闻5]</li>
<li>[一句话新闻6]</li>
<li>[一句话新闻7]</li>
<li>[一句话新闻8]</li>
</ul>
</div>

<div class="section">
<h2>今日头条</h2>
<h3>1. [新闻标题]</h3>
<p>[详细摘要]</p>
<p class="source">来源: [来源] | 分类: [分类]</p>

<h3>2. [新闻标题]</h3>
<p>[详细摘要]</p>
<p class="source">来源: [来源] | 分类: [分类]</p>

<h3>3. [新闻标题]</h3>
<p>[详细摘要]</p>
<p class="source">来源: [来源] | 分类: [分类]</p>
</div>

<div class="section">
<h2>分类新闻</h2>

<h3>宠物食品行业</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>韩国经济与市场</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>全球医美趋势</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>香港政策与贸易</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>中国政策与宏观</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>AI与产业结合</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>零售与电商</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>国际贸易与关税</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>

<h3>其他值得关注</h3>
<ul>
<li>[新闻1]</li>
<li>[新闻2]</li>
</ul>
</div>

<div class="section">
<h2>趋势观察</h2>
<ol>
<li><strong>[趋势1]</strong>: [说明]</li>
<li><strong>[趋势2]</strong>: [说明]</li>
<li><strong>[趋势3]</strong>: [说明]</li>
<li><strong>[趋势4]</strong>: [说明]</li>
<li><strong>[趋势5]</strong>: [说明]</li>
<li><strong>[趋势6]</strong>: [说明]</li>
</ol>
</div>

<div class="section">
<h2>值得关注</h2>
<ul>
<li><strong>公司/机构</strong>: [...]</li>
<li><strong>技术</strong>: [...]</li>
<li><strong>人物</strong>: [...]</li>
<li><strong>关键议题</strong>: [...]</li>
</ul>
</div>

<div class="section">
<h2>数据统计</h2>
<ul>
<li>分析文章总数: [数量]</li>
<li>覆盖来源数: [数量]</li>
<li>覆盖类别数: [数量]</li>
</ul>
</div>

<hr>
<p class="source">本报告由 AI 新闻汇总系统生成</p>

</body>
</html>""",
        agent=agent,
        context=context,
        output_file="outputs/daily_report.html",
    )