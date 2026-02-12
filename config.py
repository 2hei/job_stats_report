import os
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 配置本地LLM
llm = ChatOllama(
    model="qwen2.5:r78b",
    base_url="http://localhost:11434",
    temperature=0.7
)

class ReportState(TypedDict):
    """报告状态管理"""
    messages: Sequence[BaseMessage]
    raw_data: Dict[str, Any]  # 抓取的原始数据
    analysis_data: Dict[str, Any]  # 分析后的数据
    report_content: str  # 报告内容
    review_comments: List[str]  # 审核意见
    is_approved: bool  # 是否审核通过
