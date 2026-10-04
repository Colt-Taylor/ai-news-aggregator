# -*- coding: utf-8 -*-
"""AI News Sources Configuration."""

NEWS_SOURCES = [
    # ===== 时政锚点 =====
    {
        "name": "新华社",
        "url": "http://www.news.cn/politics/",
        "type": "politics",
    },
    {
        "name": "参考消息",
        "url": "https://www.cankaoxiaoxi.com/",
        "type": "world_news",
    },
    # ===== 财经与贸易 =====
    {
        "name": "财联社",
        "url": "https://www.cls.cn/telegraph",
        "type": "finance",
    },
    {
        "name": "华尔街见闻",
        "url": "https://wallstreetcn.com/",
        "type": "finance",
    },
    # ===== 宠物行业 =====
    {
        "name": "宠业家",
        "url": "https://www.petdhw.com/",
        "type": "pet_industry",
    },
    {
        "name": "Petfood Industry",
        "url": "https://www.petfoodindustry.com/",
        "type": "pet_industry",
    },
    # ===== 零售与电商 =====
    {
        "name": "36氪",
        "url": "https://36kr.com/",
        "type": "business",
    },
    {
        "name": "亿邦动力",
        "url": "https://www.ebrun.com/",
        "type": "retail",
    },
    {
        "name": "Retail Dive",
        "url": "https://www.retaildive.com/",
        "type": "retail",
    },
    # ===== 韩国经济 =====
    {
        "name": "韩国贸易协会",
        "url": "https://www.kita.net/",
        "type": "korea_economy",
    },
    {
        "name": "韩国统计厅",
        "url": "https://kostat.go.kr/",
        "type": "korea_economy",
    },
    # ===== 全球医美 =====
    {
        "name": "GlobalPETS",
        "url": "https://globalpets.community/",
        "type": "global_pets",
    },
    # ===== AI 前沿 =====
    {
        "name": "量子位",
        "url": "https://www.qbitai.com/",
        "type": "ai_news",
    },
    {
        "name": "机器之心",
        "url": "https://www.jiqizhixin.com/",
        "type": "ai_news",
    },
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/",
        "type": "tech_news",
    },
    # ===== 韩国医疗观光 =====
    {
        "name": "韩国保健产业振兴院",
        "url": "https://www.khidi.or.kr/",
        "type": "korea_medical",
    },
    # ===== 香港政策与贸易 =====
    {
        "name": "香港特区政府新闻网",
        "url": "https://www.news.gov.hk/",
        "type": "hongkong_policy",
    },
    {
        "name": "香港贸易发展局",
        "url": "https://www.hktdc.com/",
        "type": "hongkong_trade",
    },
    {
        "name": "USDA香港宠物食品报告",
        "url": "https://www.fas.usda.gov/regions/hong-kong",
        "type": "hongkong_pet",
    },
]

AI_CATEGORIES = [
    "中国政策与宏观",
    "宠物食品行业",
    "零售与电商",
    "韩国经济与市场",
    "全球医美趋势",
    "AI与产业结合",
    "国际贸易与关税",
    "香港政策与贸易",
    "其他值得关注",
]