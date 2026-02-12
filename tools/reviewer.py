from typing import List, Dict, Any
import re

class ReportReviewer:
    """报告审核器"""
    
    def __init__(self, report_content: str):
        self.report = report_content
        self.review_result = {
            'is_approved': False,
            'issues': [],
            'suggestions': [],
            'score': 0
        }
    
    def review(self) -> Dict[str, Any]:
        """执行审核"""
        self._check_logic_consistency()
        self._check_data_integrity()
        self._check_format_standardization()
        self._check_language_quality()
        self._check_depth_attitude()
        
        # 计算审核分数
        self._calculate_score()
        
        # 判断是否通过
        self.review_result['is_approved'] = self.review_result['score'] >= 80
        
        return self.review_result
    
    def _check_logic_consistency(self):
        """检查逻辑一致性"""
        # 检查数据是否合理
        employment_rates = re.findall(r'就业率：(\d+\.?\d*)%', self.report)
        for rate in employment_rates:
            rate_val = float(rate)
            if rate_val < 50 or rate_val > 100:
                self.review_result['issues'].append(f"异常就业率数据：{rate_val}%，超出合理范围")
        
        # 检查趋势描述是否与数据一致
        if "就业率有所下降" in self.report:
            # 检查是否有下降的证据
            if "较往年有所下滑" not in self.report:
                self.review_result['suggestions'].append("建议补充就业率下降的具体数据支撑")
    
    def _check_data_integrity(self):
        """检查数据完整性"""
        required_sections = [
            '执行摘要',
            '核心指标分析',
            '就业趋势',
            '区域分析',
            '专业类别分析',
            '结论与建议'
        ]
        
        for section in required_sections:
            if section not in self.report:
                self.review_result['issues'].append(f"缺少必要章节：{section}")
        
        # 检查是否有具体数据
        if not re.search(r'\d+\.?\d*%', self.report):
            self.review_result['issues'].append("报告缺乏具体百分比数据")
        
        # 检查是否有数据来源
        if "数据来源" not in self.report:
            self.review_result['issues'].append("缺少数据来源说明")
    
    def _check_format_standardization(self):
        """检查格式规范性"""
        # 检查标题层级
        if not re.search(r'#+\s+', self.report):
            self.review_result['issues'].append("缺少Markdown标题格式")
        
        # 检查列表格式
        if re.search(r'^\s*-\s+', self.report, re.MULTILINE):
            if not self.report.count('- ') >= 5:
                self.review_result['suggestions'].append("建议增加更多列表形式呈现数据")
        
        # 检查是否有图表占位
        if not re.search(r'(图表|图\d+|表\d+)', self.report):
            self.review_result['suggestions'].append("建议添加图表以增强数据可视化")
    
    def _check_language_quality(self):
        """检查语言表达质量"""
        # 检查错别字（简单示例）
        common_typos = {
            '就业形势': '就业形势',
            '签约率': '签约率',
            '高校': '高校'
        }
        
        # 检查句子长度
        sentences = re.split(r'[。！？]', self.report)
        long_sentences = [s for s in sentences if len(s) > 100]
        if long_sentences:
            self.review_result['suggestions'].append(f"发现{len(long_sentences)}个超长句子，建议拆分")
        
        # 检查是否有重复表述
        duplicate_check = self.report.split()
        if len(duplicate_check) != len(set(duplicate_check)):
            self.review_result['suggestions'].append("检测到部分重复表述，建议精简")
    
    def _check_depth_attitude(self):
        """检查深度和态度"""
        depth_keywords = [
            '深度分析', '根本原因', '关键因素', '重要发现',
            '深度观点', '启示', '展望', '建议'
        ]
        
        found_depth = sum(1 for keyword in depth_keywords if keyword in self.report)
        if found_depth < 4:
            self.review_result['suggestions'].append("报告深度不足，建议增加分析和见解")
        
        # 检查是否有数据支撑的观点
        if "根据" not in self.report and "数据显示" not in self.report:
            self.review_result['suggestions'].append("观点缺乏数据支撑，建议增加")
        
        # 检查是否有建设性建议
        if "建议" not in self.report or self.report.count('建议') < 5:
            self.review_result['suggestions'].append("建议部分不够充分，需要补充具体可操作的建议")
    
    def _calculate_score(self):
        """计算审核分数"""
        base_score = 100
        
        # 扣分项
        issues_count = len(self.review_result['issues'])
        suggestions_count = len(self.review_result['suggestions'])
        
        score_deduction = issues_count * 10 + suggestions_count * 5
        self.review_result['score'] = max(0, base_score - score_deduction)
    
    def generate_review_report(self) -> str:
        """生成审核报告"""
        status = "通过" if self.review_result['is_approved'] else "不通过"
        
        report = f"""
# 报告审核报告

## 审核结果：{status}

## 审核分数：{self.review_result['score']}/100

## 发现的问题
"""
        if self.review_result['issues']:
            for i, issue in enumerate(self.review_result['issues'], 1):
                report += f"{i}. {issue}\n"
        else:
            report += "✓ 未发现严重问题\n"
        
        report += "\n## 改进建议\n"
        if self.review_result['suggestions']:
            for i, suggestion in enumerate(self.review_result['suggestions'], 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "✓ 报告质量优秀\n"
        
        report += f"\n## 总体评价\n"
        if self.review_result['score'] >= 90:
            report += "报告质量优秀，数据详实，分析深入，可直接发布。\n"
        elif self.review_result['score'] >= 80:
            report += "报告质量良好，建议根据建议进行适当优化。\n"
        elif self.review_result['score'] >= 60:
            report += "报告基本符合要求，但需要修改和完善。\n"
        else:
            report += "报告存在较多问题，需要重大修改。\n"
        
        return report
