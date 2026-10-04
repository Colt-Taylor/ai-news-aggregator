# -*- coding: utf-8 -*-
"""Task definitions for the AI News Aggregator."""

from datetime import datetime
from crewai import Task, Agent
from tools.news_sources import NEWS_SOURCES, AI_CATEGORIES


def create_scraping_task(agent: Agent) -> Task:
    """Create the web scraping task.

    Args:
        agent: The scraper agent

    Returns:
        Configured scraping task
    """
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
    """Create the summarization task.

    Args:
        agent: The summarizer agent
        context: Previous tasks for context

    Returns:
        Configured summarization task
    """
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
    """Create the categorization task.

    Args:
        agent: The categorizer agent
        context: Previous tasks for context

    Returns:
        Configured categorization task
    """
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
    """Create the deep analysis task.

    Args:
        agent: The analyst agent
        context: Previous tasks for context

    Returns:
        Configured analysis task
    """
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
    """Create the reporting task.

    Args:
        agent: The reporter agent
        context: Previous tasks for context

    Returns:
        Configured reporting task
    """
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

报告要求：
- 专业、结构清晰
- 通俗易懂
- 有可操作的信息
- 格式规范，章节明确
- 全部使用中文
- 报告中不得出现韩文或英文原文，所有内容必须为中文

请特别关注以下业务方向：
- 宠物食品行业的国内零售、出口形势
- 韩国经济与市场动态
- 全球医美趋势
- 香港政策与贸易
- AI与实体产业的结合
- 中国政策变化""",
        expected_output=f"""# 每日新闻简报
日期: {current_date}

## 执行摘要
[2-3段，概述当日最重要的新闻动态，重点关注宠物食品、韩国市场、全球医美、香港政策、AI与产业结合]

## 今日头条

### 1. [最重要的新闻标题]
[详细摘要，包含背景和影响]
来源: [来源名称] | 分类: [分类]

### 2. [第二条重要新闻]
...

### 3. [第三条重要新闻]
...

## 分类新闻

### 中国政策与宏观
- [新闻1简要]
- [新闻2简要]

### 宠物食品行业
- [新闻1简要]
- [新闻2简要]

### 零售与电商
- [新闻1简要]
- [新闻2简要]

### 韩国经济与市场
- [新闻1简要]
- [新闻2简要]

### 全球医美趋势
- [新闻1简要]
- [新闻2简要]

### AI与产业结合
- [新闻1简要]
- [新闻2简要]

### 国际贸易与关税
- [新闻1简要]
- [新闻2简要]

### 香港政策与贸易
- [新闻1简要]
- [新闻2简要]

## 趋势观察
1. [趋势1]: [简要说明]
2. [趋势2]: [简要说明]
...

## 值得关注
- **公司/机构**: [提到的公司列表]
- **技术**: [讨论的关键技术]
- **人物**: [提到的重要人物]

## 数据统计
- 分析文章总数: [数量]
- 覆盖来源数: [数量]
- 覆盖类别数: [数量]

---
本报告由 AI 新闻汇总系统生成
Powered by CrewAI + DeepSeek""",
        agent=agent,
        context=context,
        output_file="outputs/daily_report.md",
    )