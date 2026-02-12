import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import re
from typing import List, Dict, Any, Optional
import json

class WebScraper:
    """网页抓取工具"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
    def fetch_page(self, url: str, timeout: int = 30, params: Optional[Dict] = None) -> str:
        """抓取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout, params=params)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            print(f"抓取失败 {url}: {e}")
            return ""
    
    def extract_employment_data(self, html: str) -> Dict[str, Any]:
        """从HTML中提取就业数据"""
        soup = BeautifulSoup(html, 'lxml')
        data = {
            'total_graduates': 0,
            'employment_rate': 0,
            'signing_rate': 0,
            'province': '',
            'school_type': '',
            'major_categories': {},
            'freelance_data': {},
            'trends': []
        }
        
        # 提取文本内容
        text = soup.get_text(separator=' ', strip=True)
        
        # 匹配毕业人数
        graduate_patterns = [
            r'毕业[生人数]+[:：]?(\d+[万千万]?)人',
            r'(\d+[万千万]?)毕业生',
            r'共(\d+[万千万]?)名毕业生'
        ]
        for pattern in graduate_patterns:
            match = re.search(pattern, text)
            if match:
                data['total_graduates'] = match.group(1)
                break
        
        # 匹配就业率
        rate_patterns = [
            r'就业率[:：]?(\d+\.?\d*)%',
            r'就业.*?(\d+\.?\d*)%'
        ]
        for pattern in rate_patterns:
            match = re.search(pattern, text)
            if match:
                data['employment_rate'] = float(match.group(1))
                break
        
        # 匹配签约率
        signing_patterns = [
            r'签约率[:：]?(\d+\.?\d*)%',
            r'签(?:约|三方)[^%]*(\d+\.?\d*)%'
        ]
        for pattern in signing_patterns:
            match = re.search(pattern, text)
            if match:
                data['signing_rate'] = float(match.group(1))
                break
        
        return data
    
    def extract_search_results(self, html: str, engine: str) -> List[str]:
        """从搜索结果页面提取URL链接"""
        urls = []
        
        try:
            if engine == 'bing':
                soup = BeautifulSoup(html, 'lxml')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if (href and href.startswith('http') 
                        and 'bing.com' not in href 
                        and 'microsoft.com' not in href
                        and 'live.com' not in href
                        and 'msn.com' not in href):
                        urls.append(href)
            elif engine == 'sogou':
                # 搜狗使用动态渲染，需要从 HTML 源码的 JSON 数据中提取 URL
                # 搜索结果链接通常在 sup_url 字段中
                patterns = [
                    r'\"sup_url\":\"(https?:\\\\/\\\\/[^\"]+)\"',
                    r'\"url\":\"(https?:\\\\/\\\\/[^\"]+)\"',
                    r'\"link\":\"(https?:\\\\/\\\\/[^\"]+)\"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html)
                    for url in matches:
                        clean_url = url.replace('\\\\/', '/')
                        url_lower = clean_url.lower()
                        
                        # 过滤条件
                        if (len(clean_url) > 40 and 
                            'sogou.com' not in url_lower and 
                            'sogoucdn.com' not in url_lower and
                            'sogouws.com' not in url_lower and
                            'openapi' not in url_lower and  # 排除 API 链接
                            'qpic.cn' not in url_lower):  # 排除 QQ 图片
                            urls.append(clean_url)
                
                # 如果没有从 JSON 中提取到，尝试从 href 属性中提取（PC 版）
                if not urls:
                    soup = BeautifulSoup(html, 'lxml')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if (href and href.startswith('http') 
                            and 'sogou.com' not in href 
                            and 'sogoucdn.com' not in href
                            and 'sogouws.com' not in href):
                            urls.append(href)
            elif engine == 'sogou':
                # 搜狗使用动态渲染，需要从 HTML 源码的 JSON 数据中提取 URL
                # 搜索结果链接通常在 sup_url 字段中
                patterns = [
                    r'\"sup_url\":\"(https?:\\\\/\\\\/[^\"]+)\"',
                    r'\"url\":\"(https?:\\\\/\\\\/[^\"]+)\"',
                    r'\"link\":\"(https?:\\\\/\\\\/[^\"]+)\"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html)
                    for url in matches:
                        clean_url = url.replace('\\\\/', '/')
                        url_lower = clean_url.lower()
                        
                        # 过滤条件
                        if (len(clean_url) > 40 and 
                            'sogou.com' not in url_lower and 
                            'sogoucdn.com' not in url_lower and
                            'sogouws.com' not in url_lower and
                            'openapi' not in url_lower and  # 排除 API 链接
                            'qpic.cn' not in url_lower):  # 排除 QQ 图片
                            urls.append(clean_url)
                
                # 如果没有从 JSON 中提取到，尝试从 href 属性中提取（PC 版）
                if not urls:
                    soup = BeautifulSoup(html, 'lxml')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if (href and href.startswith('http') 
                            and 'sogou.com' not in href 
                            and 'sogoucdn.com' not in href
                            and 'sogouws.com' not in href):
                            urls.append(href)
        except Exception as e:
            print(f"   ⚠️ 提取搜索结果时出错: {e}")
        
        return urls
    
    def filter_urls(self, urls: List[str]) -> List[str]:
        """过滤URL，去除广告和不相关链接"""
        filtered = []
        
        # 定义需要过滤的域名
        blocked_domains = [
            'ads.', 'advertisement', 'ad.', 'tracking.',
            'youdao', 'hao123', 'sohu.com', '163.com',
            '360.cn', 'tongji.baidu.com',
            'sogoucdn.com', 'sogouws.com',
            'baiducontent.com', 'm.baidu.com', 'baidubce.com',
            'play.google.com', 'apps.apple.com',
            'facebook.com', 'twitter.com', 'instagram.com',
            'linkedin.com', 'youtube.com', 'tiktok.com',
            'ifsc', 'swiftcode', 'ifsccode', 'ifsccodebank',
            'cleartax', 'getswipe'
        ]
        
        # 定义需要保留的关键词（更广泛）
        keep_keywords = [
            'edu.cn', 'gov.cn', 'org.cn', 'ac.cn',
            'news', 'xinwen', 'zaixian', 'article',
            'employment', 'job', 'zhipin', 'jobui',
            'career', 'graduate', 'bysh',
            'wangjiao', 'juye', 'qiuzhi',
            'rencai', 'zhaopin', '51job',
            'chsi', 'moe', 'people.com.cn',
            'chinanews', 'xinhuanet', 'thepaper',
            'cctv', 'cnbeta', '36kr',
            'gaoxiaojob', 'yjbys',
            'paper', 'report', 'analysis',
            'data', 'statistics', 'trend'
        ]
        
        for url in urls:
            url_lower = url.lower()
            
            # 过滤广告域名
            if any(blocked in url_lower for blocked in blocked_domains):
                continue
            
            # 过滤短URL（可能是重定向或广告）
            if len(url) < 30:
                continue
            
            # 过滤重复的主页
            if url.endswith('/') and len(url) < 35:
                continue
            
            # 过滤明显不相关的URL（IFSC代码、银行等）
            if 'ifsc' in url_lower or 'swiftcode' in url_lower:
                continue
            
            # 保留包含关键词的URL
            if any(keyword in url_lower for keyword in keep_keywords):
                filtered.append(url)
            else:
                # 如果URL看起来是内容页面，也保留
                if (len(url) > 50 and 
                    any(char in url for char in ['?', '=', '-', '_', '.', '/']) and
                    len(url.split('/')) > 3):
                    filtered.append(url)
        
        return filtered
    
    def search_bing(self, query: str, max_pages: int = 3, results_per_page: int = 10) -> List[str]:
        """使用 Bing 搜索引擎搜索（支持翻页）"""
        print(f"\n🔍 Bing 搜索: {query}")
        search_url = "https://www.bing.com/search"
        all_urls = []
        
        for page in range(1, max_pages + 1):
            offset = (page - 1) * results_per_page
            params = {
                'q': query,
                'count': results_per_page,
                'first': offset,
                'setlang': 'zh-CN'
            }
            
            print(f"   第 {page} 页 (offset: {offset})")
            html = self.fetch_page(search_url, params=params)
            if html:
                urls = self.extract_search_results(html, 'bing')
                print(f"   找到 {len(urls)} 个结果")
                all_urls.extend(urls)
            else:
                print(f"   第 {page} 页抓取失败")
                break
            
            time.sleep(1)
        
        return all_urls
    
    def search_sogou(self, query: str, max_pages: int = 3, results_per_page: int = 10) -> List[str]:
        """使用搜狗搜索引擎搜索（支持翻页）"""
        print(f"\n🔍 搜狗搜索: {query}")
        search_url = "https://sogou.com/web"
        all_urls = []
        
        for page in range(max_pages):
            page_num = page + 1
            params = {
                'query': query,
                'page': page_num,
                'ie': 'utf8'
            }
            
            print(f"   第 {page_num} 页")
            html = self.fetch_page(search_url, params=params)
            
            if html:
                urls = self.extract_search_results(html, 'sogou')
                print(f"   找到 {len(urls)} 个结果")
                all_urls.extend(urls)
            else:
                print(f"   第 {page_num} 页抓取失败")
                break
            
            time.sleep(1)
        
        return all_urls
    
    def search_and_scrape(self, query: str, max_pages: int = 3, num_to_scrape: int = 30) -> List[Dict[str, Any]]:
        """搜索并抓取相关页面数据（支持翻页）"""
        all_results = []
        
        print(f"\n{'='*60}")
        print(f"开始搜索并抓取数据: {query}")
        print(f"翻页: 最多 {max_pages} 页/搜索引擎")
        print(f"抓取: 最多 {num_to_scrape} 个页面")
        print(f"{'='*60}")
        
        # 同时使用 Bing 和搜狗搜索（支持翻页）
        bing_urls = self.search_bing(query, max_pages=max_pages, results_per_page=10)
        sogou_urls = self.search_sogou(query, max_pages=max_pages, results_per_page=10)
        
        print(f"\n📊 搜索统计:")
        print(f"   Bing 找到: {len(bing_urls)} 个结果")
        print(f"   搜狗找到: {len(sogou_urls)} 个结果")
        
        # 合并去重
        all_urls = list(set(bing_urls + sogou_urls))
        
        # 过滤广告和不相关链接
        all_urls = self.filter_urls(all_urls)
        
        print(f"   过滤后: {len(all_urls)} 个唯一链接")
        
        if not all_urls:
            print("⚠️ 未找到有效搜索结果")
            return all_results
        
        # 限制抓取数量
        urls_to_scrape = all_urls[:num_to_scrape]
        print(f"\n开始抓取 {len(urls_to_scrape)} 个页面...")
        
        # 抓取搜索结果页面
        success_count = 0
        for idx, url in enumerate(urls_to_scrape, 1):
            print(f"\n[{idx}/{len(urls_to_scrape)}] 抓取: {url}")
            html = self.fetch_page(url)
            if html:
                data = self.extract_employment_data(html)
                data['source_url'] = url
                data['search_query'] = query
                
                # 检查是否有有效数据
                has_data = (data.get('employment_rate', 0) > 0 or 
                          data.get('signing_rate', 0) > 0 or 
                          data.get('total_graduates'))
                
                if has_data or len(html) > 1000:  # 有数据或页面内容充足
                    all_results.append(data)
                    success_count += 1
                    print(f"   ✅ 成功 (就业率: {data.get('employment_rate', 0)}%)")
                else:
                    print(f"   ⚠️ 页面数据不足")
            else:
                print(f"   ❌ 抓取失败")
            
            time.sleep(2)
        
        print(f"\n✅ 成功抓取 {success_count} 个有效页面")
        return all_results
    
    def scrape_multiple_sources(self, urls: List[str]) -> List[Dict[str, Any]]:
        """批量抓取多个数据源"""
        results = []
        for url in urls:
            print(f"正在抓取: {url}")
            html = self.fetch_page(url)
            if html:
                data = self.extract_employment_data(html)
                data['source_url'] = url
                results.append(data)
            time.sleep(2)  # 避免请求过快
        return results


class DataScraperTool:
    """数据抓取工具类"""
    
    def __init__(self):
        self.scraper = WebScraper()
        
        self.search_queries = [
            '2024年 高校本科毕业生 就业率',
            '2024-2025 大学生 就业数据 统计',
            '2024届 本科生 就业情况 报告',
            '高校 毕业生 签约率 2024',
            '大学生 就业趋势 2024 2025',
            '高校毕业生就业质量报告 2024',
            '本科生就业数据 2024年'
        ]
    
    def scrape_employment_data(self) -> str:
        """抓取就业数据主函数 - 使用搜索引擎搜索（支持翻页）"""
        all_data = []
        
        print("\n" + "="*70)
        print("【数据抓取策略】使用搜索引擎搜索，支持翻页（最多5页/搜索引擎）")
        print("="*70)
        
        # 使用搜索引擎搜索并翻页
        for query in self.search_queries[:5]:  # 使用前5个查询
            results = self.scraper.search_and_scrape(
                query, 
                max_pages=5,  # 每个搜索引擎最多翻5页
                num_to_scrape=30  # 取30个页面进行抓取
            )
            all_data.extend(results)
            time.sleep(3)  # 查询间延迟
        
        # 统计汇总
        summary = self._summarize_data(all_data)
        return json.dumps(summary, ensure_ascii=False, indent=2)
    
    def _summarize_data(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """汇总数据"""
        summary = {
            'total_sources': len(data_list),
            'employment_rates': [],
            'signing_rates': [],
            'graduate_counts': [],
            'sources': []
        }
        
        for data in data_list:
            if data.get('employment_rate'):
                summary['employment_rates'].append(data['employment_rate'])
            if data.get('signing_rate'):
                summary['signing_rates'].append(data['signing_rate'])
            if data.get('total_graduates'):
                summary['graduate_counts'].append(data['total_graduates'])
            summary['sources'].append(data.get('source_url', ''))
        
        # 计算平均值
        if summary['employment_rates']:
            summary['avg_employment_rate'] = sum(summary['employment_rates']) / len(summary['employment_rates'])
        if summary['signing_rates']:
            summary['avg_signing_rate'] = sum(summary['signing_rates']) / len(summary['signing_rates'])
        
        return summary
