# Employment Analysis Report Generation System for University Graduates

An automated report generation system based on LangGraph multi-agent architecture.

## Features

- **Data Collection Agent**: Scrapes employment data from multiple sources including university websites, news media, and recruitment platforms
- **Data Analysis Agent**: Extracts core metrics, discovers employment trends, and performs multi-dimensional analysis
- **Report Writing Agent**: Integrates data to generate structured and in-depth analysis reports
- **Report Review Agent**: Checks for logical errors, corrects formatting issues, and optimizes language expression

## Tech Stack

- Python 3.12
- LangGraph (Multi-Agent Orchestration)
- LangChain + Ollama (Local LLM)
- BeautifulSoup4 (Web Parsing)
- Pandas (Data Processing)

## Installation

```bash
cd job_stats_report
pip install -r requirements.txt
```

## Start Ollama Service

Ensure Ollama service is running on `localhost:11434`

```bash
# Install qwen2.5 model
ollama pull qwen2.5:7b

# Start service
ollama serve
```

## Run the System

```bash
python main.py
```

## Project Structure

```
job_stats_report/
├── main.py              # Main program entry point, workflow definition
├── config.py            # Configuration and state definitions
├── requirements.txt     # Dependency package list
├── agents/              # Agent node definitions (implemented in main.py)
├── tools/               # Tool modules
│   ├── scraper.py       # Data scraping tools
│   ├── analyzer.py      # Data analysis tools
│   ├── report_writer.py # Report writing tools
│   └── reviewer.py      # Report review tools
├── utils/               # Utility functions
└── reports/             # Generated reports
    └── 2024-2025高校本科生就业情况分析报告.md
```

## Workflow

1. **Data Collection** → Scrape employment data from multiple sources
2. **Data Analysis** → Multi-dimensional analysis (metrics, trends, regions, majors, etc.)
3. **Report Writing** → Generate structured reports with LLM-optimized language
4. **Report Review** → Automatically check logic, data, formatting, and language quality
5. **Iteration & Optimization** → Automatically revise and re-review if not approved
6. **Save Report** → Save the final report after approval

## Custom Configuration

Modify the model configuration in `config.py`:

```python
llm = ChatOllama(
    model="qwen2.5:7b",  # Can be replaced with other models
    base_url="http://localhost:11434",
    temperature=0.7
)
```

Modify data sources in `tools/scraper.py` in the `target_sources` dictionary.

## Notes

- First run requires downloading Ollama model
- Web scraping may be subject to anti-crawling restrictions
- It is recommended to adjust scraping strategies according to actual data sources
