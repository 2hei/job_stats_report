from typing import Dict, Any
import json

class ReportWriter:
    """报告撰写器"""
    
    def __init__(self, analysis_data: Dict[str, Any]):
        self.analysis = analysis_data
    
    def generate_report(self) -> str:
        """生成结构化报告"""
        report = f"""
# 2024-2025年高校本科生就业情况分析报告

## 一、执行摘要

本报告基于2024-2025年高校毕业生就业数据的综合分析，涵盖{self.analysis['core_indicators']['total_sources']}个权威数据源。报告显示，在宏观经济环境变化和就业市场结构调整的双重影响下，高校毕业生就业形势呈现新特征。

### 核心数据速览
- 平均就业率：{self.analysis['core_indicators']['avg_employment_rate']*100:.1f}%
- 平均签约率：{self.analysis['core_indicators']['avg_signing_rate']*100:.1f}%
- 就业率波动范围：{self.analysis['core_indicators']['employment_rate_range']['min']*100:.1f}% - {self.analysis['core_indicators']['employment_rate_range']['max']*100:.1f}%

## 二、核心指标分析

### 2.1 整体就业形势
2024-2025年，高校毕业生就业市场面临较大压力。整体就业率较往年有所下滑，签约率相对稳定但签约周期明显延长。这一现象反映出：
1. 企业招聘更为谨慎，更倾向于"优中选优"
2. 毕业生就业期望与市场需求存在结构性错配
3. 部分毕业生选择"慢就业"或继续深造

### 2.2 关键数据解读
- **就业率分布**：不同类型院校、不同专业间就业率差异显著，极差达到{(self.analysis['core_indicators']['employment_rate_range']['max'] - self.analysis['core_indicators']['employment_rate_range']['min'])*100:.1f}个百分点
- **签约趋势**：签约率保持相对稳定，但"先就业后择业"心态普遍

## 三、就业趋势深度剖析

### 3.1 时代特征
{self._format_trends()}

### 3.2 行业变革
新兴产业的崛起正在重塑就业格局。人工智能、新能源、生物医药等前沿领域展现出强劲的吸纳能力，而传统行业则在数字化转型中探索新的用人模式。这种结构性变化既是挑战，也是机遇。

### 3.3 就业观念转变
当代大学生就业观念正在发生深刻变化：
- "铁饭碗"思维逐渐淡化，更注重个人成长和发展空间
- 自由职业、灵活就业被更多接受
- 创业意愿有所提升，特别是在数字创意领域

## 四、区域分析

### 4.1 东部沿海地区
- 平均就业率：{self.analysis['regional_analysis']['east_coast']['avg_employment_rate']*100:.1f}%
- 特征：经济发达，就业机会集中，但生活成本高企，竞争最为激烈
- 热门省份：{', '.join(self.analysis['regional_analysis']['east_coast']['hot_provinces'])}

### 4.2 中部地区
- 平均就业率：{self.analysis['regional_analysis']['central_region']['avg_employment_rate']*100:.1f}%
- 特征：发展潜力大，就业机会稳定，生活成本相对适中
- 热门省份：{', '.join(self.analysis['regional_analysis']['central_region']['hot_provinces'])}

### 4.3 西部地区
- 平均就业率：{self.analysis['regional_analysis']['west_region']['avg_employment_rate']*100:.1f}%
- 特征：政策支持力度大，新兴产业加速发展，人才引进政策积极
- 热门省份：{', '.join(self.analysis['regional_analysis']['west_region']['hot_provinces'])}

## 五、专业类别分析

### 5.1 理工科专业（STEM）
- 就业率：{self.analysis['major_analysis']['stem_majors']['employment_rate']*100:.1f}%
- 优势专业：{', '.join(self.analysis['major_analysis']['stem_majors']['top_majors'])}
- 发展态势：{self.analysis['major_analysis']['stem_majors']['trend']}

**深度观点**：理工科专业依然是就业市场的"硬通货"。随着数字化转型加速和科技自立自强战略推进，计算机、电子信息等领域人才需求持续旺盛。但需警惕"扎堆"现象，部分细分领域出现供给过剩。

### 5.2 人文社科专业
- 就业率：{self.analysis['major_analysis']['humanities_majors']['employment_rate']*100:.1f}%
- 优势专业：{', '.join(self.analysis['major_analysis']['humanities_majors']['top_majors'])}
- 发展态势：{self.analysis['major_analysis']['humanities_majors']['trend']}

**深度观点**：人文社科专业就业形势更为复杂。传统就业渠道（如教育、公务员）竞争激烈，但新媒体、内容创作、品牌营销等领域为人文社科学生提供了新的可能。关键是培养"人文素养+数字技能"的复合能力。

### 5.3 社会科学专业
- 就业率：{self.analysis['major_analysis']['social_science_majors']['employment_rate']*100:.1f}%
- 优势专业：{', '.join(self.analysis['major_analysis']['social_science_majors']['top_majors'])}
- 发展态势：{self.analysis['major_analysis']['social_science_majors']['trend']}

**深度观点**：社会科学专业展现出较强适应性。经济管理类人才在金融科技、企业咨询等领域需求增长，法学专业则在企业合规、知识产权等新兴领域找到新空间。

### 5.4 艺术类专业
- 就业率：{self.analysis['major_analysis']['arts_majors']['employment_rate']*100:.1f}%
- 优势专业：{', '.join(self.analysis['major_analysis']['arts_majors']['top_majors'])}
- 发展态势：{self.analysis['major_analysis']['arts_majors']['trend']}

**深度观点**：艺术类专业就业呈现"两极分化"。顶尖院校毕业生在创意设计领域竞争力强，但普通院校毕业生面临较大就业压力。数字艺术的兴起为艺术生提供了新出路。

## 六、学校类别分析

### 6.1 985/211高校
- 就业率：{self.analysis['school_type_analysis']['985_211_universities']['employment_rate']*100:.1f}%
- 平均薪资：{self.analysis['school_type_analysis']['985_211_universities']['avg_salary']}
- 特征：{self.analysis['school_type_analysis']['985_211_universities']['characteristics']}

### 6.2 普通高校
- 就业率：{self.analysis['school_type_analysis']['general_universities']['employment_rate']*100:.1f}%
- 平均薪资：{self.analysis['school_type_analysis']['general_universities']['avg_salary']}
- 特征：{self.analysis['school_type_analysis']['general_universities']['characteristics']}

### 6.3 高职院校
- 就业率：{self.analysis['school_type_analysis']['vocational_colleges']['employment_rate']*100:.1f}%
- 平均薪资：{self.analysis['school_type_analysis']['vocational_colleges']['avg_salary']}
- 特征：{self.analysis['school_type_analysis']['vocational_colleges']['characteristics']}

**重要发现**：高职院校就业率表现亮眼，反映出技能型人才的市场需求。这启示高等教育需要更加注重实践能力和职业技能的培养。

## 七、自由职业深度分析

### 7.1 自由职业概况
- 自由就业比例：{self.analysis['freelance_analysis']['freelance_rate']*100:.1f}%
- 年增长率：{self.analysis['freelance_analysis']['growth_trend']}

### 7.2 热门自由职业领域
{self._format_freelance_categories()}

### 7.3 挑战与机遇
**挑战：**
{self._format_challenges()}

**机遇：**
{self._format_opportunities()}

**深度观点**：自由职业不再是"退而求其次"的选择，而是许多年轻人的主动追求。这一趋势背后是互联网平台、数字工具的普及，以及年轻一代对工作方式的新理解。但需要建立更完善的社会保障体系支持。

## 八、结论与建议

### 8.1 主要结论
1. **就业形势稳中有变**：整体就业率略有下滑，但结构性机会依然存在
2. **专业分化加剧**：理工科优势明显，人文社科需转型突破
3. **区域差异显著**：东部机会多但竞争激烈，中西部潜力待挖掘
4. **就业形态多元化**：自由职业比例上升，就业观念更加开放

### 8.2 对学生的建议
- **能力建设**：强化专业技能，培养跨学科复合能力
- **心态调整**：降低不切实际的期望，重视第一份工作的积累
- **路径规划**：不拘泥于传统就业渠道，积极探索新兴领域
- **持续学习**：保持终身学习意识，适应快速变化的市场

### 8.3 对高校的建议
- **专业设置**：优化专业结构，增加新兴交叉学科
- **教学改革**：强化实践教学，提升学生就业竞争力
- **就业指导**：加强职业规划教育，提供个性化就业服务
- **校企合作**：深化产学研合作，拓宽就业渠道

### 8.4 对政策制定者的建议
- **宏观调控**：实施积极的就业政策，稳定就业预期
- **区域协调**：推动区域协调发展，平衡就业机会
- **保障体系**：完善灵活就业社会保障，解除后顾之忧
- **创业支持**：加大创业扶持力度，激发创新活力

## 九、展望

展望未来，高校毕业生就业将面临更多不确定性，但也蕴含新的机遇。人工智能、数字经济、绿色经济等新兴领域将持续创造高质量就业岗位。关键在于：
- 学生要主动适应变化，提升核心竞争力
- 高校要与时俱进，培养社会需要的人才
- 社会要营造包容多元的就业环境
- 政策要精准有力，为青年就业保驾护航

---
**报告编制时间**：2025年1月  
**数据来源**：教育部、各高校就业质量报告、主流媒体、招聘平台数据  
**声明**：本报告基于公开数据进行分析，仅供参考
"""
        return report
    
    def _format_trends(self) -> str:
        """格式化趋势"""
        trends_text = []
        for i, trend in enumerate(self.analysis['trends'], 1):
            trends_text.append(f"{i}. {trend}")
        return '\n'.join(trends_text)
    
    def _format_freelance_categories(self) -> str:
        """格式化自由职业类别"""
        return '\n'.join(f"- {cat}" for cat in self.analysis['freelance_analysis']['popular_categories'])
    
    def _format_challenges(self) -> str:
        """格式化挑战"""
        return '\n'.join(f"- {ch}" for ch in self.analysis['freelance_analysis']['challenges'])
    
    def _format_opportunities(self) -> str:
        """格式化机遇"""
        return '\n'.join(f"- {opp}" for opp in self.analysis['freelance_analysis']['opportunities'])
