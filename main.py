from typing import Annotated, Sequence, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama
import json
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ReportState, llm
from tools.scraper import DataScraperTool
from tools.analyzer import EmploymentDataAnalyzer
from tools.report_writer import ReportWriter
from tools.reviewer import ReportReviewer

# Agent节点定义
def data_collection_node(state: ReportState):
    """数据抓取Agent"""
    print("\n" + "="*50)
    print("【数据抓取Agent】开始工作...")
    print("="*50)
    
    scraper = DataScraperTool()
    raw_data_str = scraper.scrape_employment_data()
    raw_data = json.loads(raw_data_str)
    
    print(f"\n抓取完成！")
    print(f"- 数据源数量: {raw_data.get('total_sources', 0)}")
    print(f"- 平均就业率: {raw_data.get('avg_employment_rate', 0)*100:.1f}%")
    print(f"- 平均签约率: {raw_data.get('avg_signing_rate', 0)*100:.1f}%")
    
    # 更新状态
    new_messages = state["messages"] + [
        AIMessage(content=f"已成功抓取{raw_data.get('total_sources', 0)}个数据源的就业数据")
    ]
    
    return {
        **state,
        "raw_data": raw_data,
        "messages": new_messages
    }

def data_analysis_node(state: ReportState):
    """数据分析Agent"""
    print("\n" + "="*50)
    print("【数据分析Agent】开始工作...")
    print("="*50)
    
    analyzer = EmploymentDataAnalyzer(state["raw_data"])
    analysis_str = analyzer.analyze()
    analysis_data = json.loads(analysis_str)
    
    print(f"\n分析完成！")
    print(f"- 核心指标已提取")
    print(f"- 就业趋势已挖掘")
    print(f"- 区域、专业、学校类别分析完成")
    print(f"- 自由职业数据已分析")
    
    new_messages = state["messages"] + [
        AIMessage(content=f"数据分析完成，已生成{len(analysis_data)}个维度的分析结果")
    ]
    
    return {
        **state,
        "analysis_data": analysis_data,
        "messages": new_messages
    }

def report_writing_node(state: ReportState):
    """报告撰写Agent"""
    print("\n" + "="*50)
    print("【报告撰写Agent】开始工作...")
    print("="*50)
    
    writer = ReportWriter(state["analysis_data"])
    report_content = writer.generate_report()
    
    print(f"\n报告生成完成！")
    print(f"- 报告字数: {len(report_content)} 字")
    print(f"- 章节数: {report_content.count('##')} 个")
    
    # 使用LLM优化报告
    print("\n正在使用LLM优化报告语言...")
    prompt = f"""
    请对以下就业分析报告进行语言优化，要求：
    1. 保持原有数据和逻辑不变
    2. 优化语言表达，使其更加专业流畅
    3. 增强报告的深度和洞察力
    4. 保持Markdown格式
    
    报告内容：
    {report_content}
    """
    
    optimized_report = llm.invoke(prompt).content
    
    new_messages = state["messages"] + [
        AIMessage(content=f"报告撰写完成，已生成结构化报告并经过LLM优化")
    ]
    
    return {
        **state,
        "report_content": optimized_report,
        "messages": new_messages
    }

def report_review_node(state: ReportState):
    """审核校对Agent"""
    print("\n" + "="*50)
    print("【审核校对Agent】开始工作...")
    print("="*50)
    
    reviewer = ReportReviewer(state["report_content"])
    review_result = reviewer.review()
    
    print(f"\n审核完成！")
    print(f"- 审核分数: {review_result['score']}/100")
    print(f"- 发现问题: {len(review_result['issues'])} 个")
    print(f"- 改进建议: {len(review_result['suggestions'])} 条")
    print(f"- 审核结果: {'通过' if review_result['is_approved'] else '不通过'}")
    
    review_comments = review_result['issues'] + review_result['suggestions']
    
    new_messages = state["messages"] + [
        AIMessage(content=f"审核完成，分数：{review_result['score']}，{'通过' if review_result['is_approved'] else '需要修改'}")
    ]
    
    return {
        **state,
        "review_comments": review_comments,
        "is_approved": review_result['is_approved'],
        "messages": new_messages
    }

def check_approval(state: ReportState):
    """检查是否审核通过"""
    if state["is_approved"]:
        print("\n" + "="*50)
        print("✅ 报告审核通过！")
        print("="*50)
        return "end"
    else:
        print("\n" + "="*50)
        print("⚠️ 报告需要修改，重新生成...")
        print("="*50)
        return "rewrite"

def rewrite_report_node(state: ReportState):
    """根据审核意见重新生成报告"""
    print("\n根据审核意见修改报告...")
    
    # 构建修改提示
    review_prompt = "\n".join([f"- {comment}" for comment in state["review_comments"]])
    
    prompt = f"""
    请根据以下审核意见，修改和优化就业分析报告：
    
    审核意见：
    {review_prompt}
    
    原报告：
    {state['report_content']}
    
    要求：
    1. 修复所有指出的问题
    2. 吸收改进建议
    3. 保持数据准确性
    4. 保持结构完整性
    """
    
    revised_report = llm.invoke(prompt).content
    
    # 重新审核
    print("重新审核修改后的报告...")
    reviewer = ReportReviewer(revised_report)
    review_result = reviewer.review()
    
    print(f"\n重新审核结果：")
    print(f"- 审核分数: {review_result['score']}/100")
    print(f"- 审核结果: {'通过' if review_result['is_approved'] else '仍需修改'}")
    
    new_messages = state["messages"] + [
        AIMessage(content=f"报告已根据审核意见修改，新分数：{review_result['score']}")
    ]
    
    return {
        **state,
        "report_content": revised_report,
        "review_comments": review_result['issues'] + review_result['suggestions'],
        "is_approved": review_result['is_approved'],
        "messages": new_messages
    }

def save_report_node(state: ReportState):
    """保存报告"""
    print("\n" + "="*50)
    print("【保存报告】")
    print("="*50)
    
    import os
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    report_path = os.path.join(reports_dir, "2024-2025高校本科生就业情况分析报告.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(state["report_content"])
    
    print(f"✅ 报告已保存至: {report_path}")
    print(f"   文件大小: {len(state['report_content'])} 字符")
    
    return state

# 构建工作流图
def build_graph():
    """构建多Agent工作流"""
    workflow = StateGraph(ReportState)
    
    # 添加节点
    workflow.add_node("data_collection", data_collection_node)
    workflow.add_node("data_analysis", data_analysis_node)
    workflow.add_node("report_writing", report_writing_node)
    workflow.add_node("report_review", report_review_node)
    workflow.add_node("rewrite", rewrite_report_node)
    workflow.add_node("save_report", save_report_node)
    
    # 设置边
    workflow.set_entry_point("data_collection")
    workflow.add_edge("data_collection", "data_analysis")
    workflow.add_edge("data_analysis", "report_writing")
    workflow.add_edge("report_writing", "report_review")
    
    # 条件边：检查是否需要修改
    workflow.add_conditional_edges(
        "report_review",
        check_approval,
        {
            "end": "save_report",
            "rewrite": "rewrite"
        }
    )
    
    workflow.add_edge("rewrite", "report_review")
    workflow.add_edge("save_report", END)
    
    return workflow.compile()

if __name__ == "__main__":
    print("="*60)
    print("2024-2025年高校本科生就业情况分析报告生成系统")
    print("基于LangGraph多智能体架构")
    print("="*60)
    
    # 初始化状态
    initial_state = {
        "messages": [SystemMessage(content="你是一个专业的就业数据分析助手，负责生成高质量的高校就业分析报告。")],
        "raw_data": {},
        "analysis_data": {},
        "report_content": "",
        "review_comments": [],
        "is_approved": False
    }
    
    # 构建并执行工作流
    app = build_graph()
    
    print("\n开始执行多Agent协作流程...")
    print("-" * 60)
    
    final_state = app.invoke(initial_state)
    
    print("\n" + "="*60)
    print("🎉 报告生成完成！")
    print("="*60)
    print(f"\n最终状态：")
    print(f"- 报告已审核通过: {'是' if final_state['is_approved'] else '否'}")
    print(f"- 总执行步骤: {len(final_state['messages'])}")
    print(f"\n报告保存在: reports/2024-2025高校本科生就业情况分析报告.md")
