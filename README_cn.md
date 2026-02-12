# 高校本科生就业情况分析报告生成系统

基于LangGraph多智能体架构的自动化报告生成系统。

## 功能特性

- **数据抓取Agent**：从高校站点、新闻媒体、招聘平台等多源抓取就业数据
- **数据分析Agent**：提炼核心指标，挖掘就业趋势，进行多维度分析
- **报告撰写Agent**：整合数据，生成结构化、有深度的分析报告
- **审核校对Agent**：检查逻辑漏洞，修正格式错误，优化语言表达

## 技术栈

- Python 3.12
- LangGraph（多智能体编排）
- LangChain + Ollama（本地LLM）
- BeautifulSoup4（网页解析）
- Pandas（数据处理）

## 安装依赖

```bash
cd job_stats_report
pip install -r requirements.txt
```

## 启动Ollama服务

确保Ollama服务运行在 `localhost:11434`

```bash
# 安装qwen2.5模型
ollama pull qwen2.5:7b

# 启动服务
ollama serve
```

## 运行系统

```bash
python main.py
```

## 项目结构

```
job_stats_report/
├── main.py              # 主程序入口，定义工作流
├── config.py            # 配置和状态定义
├── requirements.txt     # 依赖包列表
├── agents/              # Agent节点定义（在main.py中实现）
├── tools/               # 工具模块
│   ├── scraper.py       # 数据抓取工具
│   ├── analyzer.py      # 数据分析工具
│   ├── report_writer.py # 报告撰写工具
│   └── reviewer.py      # 报告审核工具
├── utils/               # 工具函数
└── reports/             # 生成的报告
    └── 2024-2025高校本科生就业情况分析报告.md
```

## 工作流程

1. **数据抓取** → 从多源抓取就业数据
2. **数据分析** → 多维度分析（指标、趋势、区域、专业等）
3. **报告撰写** → 生成结构化报告，使用LLM优化语言
4. **审核校对** → 自动检查逻辑、数据、格式、语言质量
5. **迭代优化** → 如审核不通过，自动修改后重新审核
6. **保存报告** → 审核通过后保存最终报告

## 自定义配置

修改 `config.py` 中的模型配置：

```python
llm = ChatOllama(
    model="qwen2.5:8b",  # 可替换为其他模型
    base_url="http://localhost:11434",
    temperature=0.7
)
```

修改数据源在 `tools/scraper.py` 中的 `target_sources`。

## 注意事项

- 首次运行需要下载Ollama模型
- 网页抓取可能受网站反爬限制
- 建议根据实际数据源调整抓取策略
