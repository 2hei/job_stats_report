# 快速开始指南

## 1. 安装依赖

```bash
cd job_stats_report
pip install -r requirements.txt
```

## 2. 配置Ollama

### 2.1 安装Ollama
访问 https://ollama.ai 下载并安装

### 2.2 下载模型
```bash
ollama pull qwen2.5:8b
```

### 2.3 启动服务
```bash
ollama serve
```

## 3. 测试环境

```bash
python test_setup.py
```

如果所有测试通过，即可运行主程序。

## 4. 运行系统

```bash
python main.py
```

## 5. 查看报告

生成的报告保存在 `reports/2024-2025高校本科生就业情况分析报告.md`

## 自定义数据源

编辑 `tools/scraper.py` 中的 `target_sources` 字典，添加或修改数据源URL。

## 常见问题

**Q: Ollama连接失败？**
- 确保Ollama服务正在运行 (ollama serve)
- 检查端口号是否为11434
- 确保模型已下载 (ollama list)

**Q: 爬虫抓取失败？**
- 部分网站有反爬机制，可尝试修改请求头或延迟时间
- 使用VPN访问被墙的网站
- 考虑使用API接口代替网页抓取

**Q: 报告质量不满意？**
- 调整 `config.py` 中的 temperature 参数（0-1，越低越保守）
- 尝试使用更大的模型（如 qwen2.5:14b）
- 优化 Prompt 提示词

**Q: 如何添加新的Agent？**
1. 在 `tools/` 中创建新工具模块
2. 在 `main.py` 中定义Agent节点函数
3. 在工作流中添加节点和边
