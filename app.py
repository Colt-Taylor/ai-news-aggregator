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
st.caption(f"页面打开时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
                st.error("❌ 生成失败，请查看下方错误信息。")
                st.code(result.stderr[-2000:])

    st.divider()
    st.markdown("### 📖 使用说明")
    st.markdown(
        """
        1. 点击「立即生成今日简报」
        2. 等待 5-15 分钟（分析员需要联网搜索）
        3. 右侧查看报告
        4. 可点击下方按钮下载报告
        """
    )

# 主区域：显示报告
html_path = Path("outputs/daily_report.html")

if html_path.exists():
    with open(html_path, "r", encoding="utf-8") as f:
        report_html = f.read()

    # 用 st.html 渲染 HTML（支持样式、颜色、高亮）
    st.html(report_html)

    # 下载按钮
    st.divider()
    st.download_button(
        label="📥 下载报告 (HTML)",
        data=report_html,
        file_name=f"news_report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
    )
else:
    st.info("👈 还没有生成报告，请点击左侧的「立即生成今日简报」按钮。")