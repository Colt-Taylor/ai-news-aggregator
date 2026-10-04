# -*- coding: utf-8 -*-
"""Deep Analyst Agent - 新闻深度分析员."""

from crewai import Agent, LLM
from typing import List, Any


def create_analyst_agent(llm: LLM, tools: List[Any] = None) -> Agent:
    """Create and configure the deep news analyst agent.

    Args:
        llm: The language model to use
        tools: Optional list of extra tools (default: None)

    Returns:
        Agent configured for deep news analysis
    """
    # 尝试加载 Serper 搜索工具
    all_tools = []
    if tools:
        all_tools.extend(tools)

    try:
        from crewai_tools import SerperDevTool
        import os
        if os.getenv("SERPER_API_KEY"):
            search_tool = SerperDevTool()
            all_tools.append(search_tool)
            print("[+] 深度分析员已加载 Serper 搜索工具")
        else:
            print("[!] 未设置 SERPER_API_KEY，分析员将无法联网搜索")
    except ImportError:
        print("[!] 未安装 crewai-tools，分析员将无法联网搜索")

    return Agent(
        role="新闻深度分析员",
        goal="""对每个分类中最重要的 2-3 条新闻进行深度分析和背景调查。
        挖掘事件背后的深层原因，评估其潜在影响，判断未来趋势。
        特别关注对零售业、贸易行业的影响。""",
        backstory="""你是一名资深调查记者，拥有 20 年深度报道经验。
        你擅长快速搜索并核实背景信息，从多个角度分析事件的深层原因，
        评估事件对行业和市场的潜在影响，判断事件是孤立现象还是趋势的开始。

        你的分析基于事实，逻辑清晰，观点客观。
        你总是会搜索最新的相关信息，确保分析的准确性。""",
        tools=all_tools,
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=10,
    )