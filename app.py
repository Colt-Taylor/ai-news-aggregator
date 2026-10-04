# -*- coding: utf-8 -*-
"""Streamlit 界面 - 用于阅读 AI 新闻简报."""

import streamlit as st
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI 新闻简报",
    page_icon="📰",
    layout="wide",
)

# 标题
st.title("📰 AI 新闻简报")
st.caption(f"最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 操作面板")

    if st.button("🔄 立即生成今日简报", use_container_width=True):
        with st.spinner("正在抓取新闻、分析、生成报告，请耐心等待（约 5-15 分钟）..."):
            result = subprocess.run(
                [sys.executable, "main.py"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            if result.returncode == 0:
                st.success("✅ 报告生成成功！")
                st.rerun()
            else:
                st.error("❌ 生成失败，请查看终端日志。")
                st.code(result.stderr[-2000:])

    st.divider()
    st.markdown("### 📖 使用说明")
    st.markdown(
        """
        1. 点击「立即生成今日简报」
        2. 等待 5-15 分钟
        3. 右侧查看报告
        """
    )

# 主区域：显示报告
report_path = Path("outputs/daily_report.md")

if report_path.exists():
    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()

    # 显示报告
    st.markdown(report_content)

    # 下载按钮
    st.download_button(
        label="📥 下载报告 (Markdown)",
        data=report_content,
        file_name=f"news_report_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
    )
else:
    st.info("👈 还没有生成报告，请点击左侧的「立即生成今日简报」按钮。")	 