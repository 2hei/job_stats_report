#!/usr/bin/env python3
"""
快速测试脚本 - 验证各个模块是否正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_dependencies():
    """测试依赖是否安装"""
    print("测试依赖包...")
    try:
        import langgraph
        import langchain
        import langchain_ollama
        import requests
        import bs4
        import pandas
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def test_ollama_connection():
    """测试Ollama连接"""
    print("\n测试Ollama连接...")
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="qwen2.5:8b", base_url="http://localhost:11434")
        response = llm.invoke("你好，请简短回复。")
        print(f"✅ Ollama连接正常，模型响应: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Ollama连接失败: {e}")
        print("请确保: 1) ollama服务运行 (ollama serve)  2) 已下载模型 (ollama pull qwen2.5:8b)")
        return False

def test_scraper():
    """测试数据抓取"""
    print("\n测试数据抓取模块...")
    try:
        from tools.scraper import WebScraper
        scraper = WebScraper()
        test_html = """
        <html>
            <body>
                <p>2024年毕业人数820万人，就业率达到85.5%，签约率78.2%</p>
            </body>
        </html>
        """
        data = scraper.extract_employment_data(test_html)
        print(f"✅ 数据抓取正常: {data}")
        return True
    except Exception as e:
        print(f"❌ 数据抓取失败: {e}")
        return False

def test_analyzer():
    """测试数据分析"""
    print("\n测试数据分析模块...")
    try:
        from tools.analyzer import EmploymentDataAnalyzer
        test_data = {
            'total_sources': 10,
            'avg_employment_rate': 0.85,
            'avg_signing_rate': 0.78,
            'employment_rates': [0.85, 0.90, 0.80]
        }
        analyzer = EmploymentDataAnalyzer(test_data)
        result = analyzer.analyze()
        print(f"✅ 数据分析正常，生成分析结果")
        return True
    except Exception as e:
        print(f"❌ 数据分析失败: {e}")
        return False

def test_report_writer():
    """测试报告撰写"""
    print("\n测试报告撰写模块...")
    try:
        from tools.report_writer import ReportWriter
        from tools.analyzer import EmploymentDataAnalyzer
        
        test_data = {
            'total_sources': 10,
            'avg_employment_rate': 0.85,
            'avg_signing_rate': 0.78,
            'employment_rates': [0.85, 0.90, 0.80],
            'signing_rates': [0.78, 0.82, 0.75]
        }
        
        analyzer = EmploymentDataAnalyzer(test_data)
        analysis = analyzer.analyze()
        
        writer = ReportWriter(eval(analysis))
        report = writer.generate_report()
        print(f"✅ 报告撰写正常，生成 {len(report)} 字的报告")
        return True
    except Exception as e:
        print(f"❌ 报告撰写失败: {e}")
        return False

def test_reviewer():
    """测试报告审核"""
    print("\n测试报告审核模块...")
    try:
        from tools.reviewer import ReportReviewer
        test_report = """
        # 测试报告
        就业率达到85%
        数据来源：测试数据
        """
        reviewer = ReportReviewer(test_report)
        result = reviewer.review()
        print(f"✅ 报告审核正常，分数: {result['score']}")
        return True
    except Exception as e:
        print(f"❌ 报告审核失败: {e}")
        return False

def main():
    print("="*60)
    print("高校就业报告生成系统 - 环境测试")
    print("="*60)
    
    tests = [
        test_dependencies,
        test_ollama_connection,
        test_scraper,
        test_analyzer,
        test_report_writer,
        test_reviewer
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print(f"测试完成: {sum(results)}/{len(results)} 通过")
    print("="*60)
    
    if all(results):
        print("\n🎉 所有测试通过，可以运行 python main.py")
    else:
        print("\n⚠️ 部分测试失败，请检查上述错误信息")

if __name__ == "__main__":
    main()
