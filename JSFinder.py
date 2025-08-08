#!/usr/bin/env python3
# coding: utf-8
# Optimized URL Extractor
# Original by Threezh1, optimized version

import requests
import argparse
import sys
import re
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Set, Optional, Dict
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class URLExtractor:
    def __init__(self, cookie: Optional[str] = None, max_workers: int = 10):
        self.cookie = cookie
        self.max_workers = max_workers
        self.session = self._create_session()
        self.url_pattern = self._compile_url_pattern()
        self.processed_urls: Set[str] = set()
        
    def _create_session(self) -> requests.Session:
        """创建带有重试机制的会话"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        if self.cookie:
            session.headers.update({"Cookie": self.cookie})
        return session
    
    def _compile_url_pattern(self) -> re.Pattern:
        """预编译正则表达式提高性能"""
        pattern_raw = r"""
        (?:"|')                               # Start delimiter
        (
          ((?:[a-zA-Z]{1,10}://|//)           # Match scheme or //
          [^"'/]{1,}\.                        # Match domain
          [a-zA-Z]{2,}[^"']{0,})              # Extension and/or path
          |
          ((?:/|\.\./|\./)                    # Start with /,../,./
          [^"'><,;| *()(%%$^/\\\[\]]          # Next char restrictions
          [^"'><,;|()]{1,})                   # Rest of chars
          |
          ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint
          [a-zA-Z0-9_\-/]{1,}                 # Resource name
          \.(?:[a-zA-Z]{1,4}|action)          # Extension
          (?:[\?|/][^"|']{0,}|))              # Parameters
          |
          ([a-zA-Z0-9_\-]{1,}                 # Filename
          \.(?:php|asp|aspx|jsp|json|
               action|html|js|txt|xml)         # Extensions
          (?:\?[^"|']{0,}|))                  # Parameters
        )
        (?:"|')                               # End delimiter
        """
        return re.compile(pattern_raw, re.VERBOSE)
    
    def extract_urls_from_content(self, content: str) -> List[str]:
        """从内容中提取URL"""
        if not content:
            return []
        
        matches = self.url_pattern.finditer(content)
        return [match.group().strip('"').strip("'") for match in matches]
    
    def fetch_content(self, url: str) -> Optional[str]:
        """获取网页内容"""
        if url in self.processed_urls:
            return None
            
        self.processed_urls.add(url)
        
        try:
            response = self.session.get(url, timeout=10, verify=False)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None
    
    def analyze_page_info(self, url: str) -> Dict[str, str]:
        """分析页面信息，包括标题、状态码、长度等"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            content_length = len(response.text)
            
            # 提取页面标题
            title = "No title"
            try:
                soup = BeautifulSoup(response.text, "html.parser")
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()
            except Exception:
                pass
            
            return {
                'url': url,
                'status_code': response.status_code,
                'title': title,
                'content_length': content_length,
                'content': response.text if response.status_code == 200 else None
            }
            
        except requests.RequestException as e:
            logger.warning(f"Failed to analyze {url}: {e}")
            return {
                'url': url,
                'status_code': 0,
                'title': 'Error',
                'content_length': 0,
                'content': None
            }
    
    def normalize_url(self, base_url: str, relative_url: str) -> str:
        """标准化URL处理"""
        # 黑名单过滤
        blacklist = ["javascript:", "mailto:", "tel:", "#"]
        if any(relative_url.startswith(item) for item in blacklist):
            return ""
        
        # 使用urljoin处理相对URL，比手动处理更可靠
        try:
            return urljoin(base_url, relative_url)
        except Exception as e:
            logger.warning(f"URL join failed for {base_url} + {relative_url}: {e}")
            return ""
    
    def extract_domain_info(self, url: str) -> Dict[str, str]:
        """提取域名信息"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 获取主域名 (example.com from sub.example.com)
        domain_parts = domain.split('.')
        main_domain = '.'.join(domain_parts[-2:]) if len(domain_parts) >= 2 else domain
        
        return {
            'full_domain': domain,
            'main_domain': main_domain,
            'scheme': parsed.scheme
        }
    
    def extract_urls_from_page(self, url: str, include_js: bool = True) -> Dict[str, any]:
        """从单个页面提取URL，返回页面信息和URL"""
        logger.info(f"Processing: {url}")
        
        # 获取页面分析信息
        page_info = self.analyze_page_info(url)
        content = page_info.get('content')
        
        if not content:
            return {'page_info': page_info, 'urls': []}
        
        all_urls = []
        base_domain_info = self.extract_domain_info(url)
        
        # 解析HTML
        try:
            soup = BeautifulSoup(content, "html.parser")
            
            # 处理内联脚本
            inline_scripts = soup.find_all("script", src=False)
            for script in inline_scripts:
                script_content = script.get_text()
                urls = self.extract_urls_from_content(script_content)
                all_urls.extend(urls)
            
            # 处理外部脚本
            if include_js:
                external_scripts = soup.find_all("script", src=True)
                for script in external_scripts:
                    script_url = self.normalize_url(url, script.get("src"))
                    if script_url:
                        script_page_info = self.analyze_page_info(script_url)
                        script_content = script_page_info.get('content')
                        if script_content:
                            urls = self.extract_urls_from_content(script_content)
                            all_urls.extend(urls)
            
        except Exception as e:
            logger.warning(f"HTML parsing failed for {url}: {e}")
        
        # 从页面内容中直接提取URL
        content_urls = self.extract_urls_from_content(content)
        all_urls.extend(content_urls)
        
        # 标准化所有URL并过滤
        normalized_urls = []
        for raw_url in all_urls:
            normalized = self.normalize_url(url, raw_url)
            if normalized and normalized not in normalized_urls:
                # 过滤掉静态资源
                if self._is_valid_endpoint(normalized):
                    # 只保留同主域名下的URL
                    url_domain_info = self.extract_domain_info(normalized)
                    if (base_domain_info['main_domain'] in url_domain_info['full_domain'] or 
                        url_domain_info['full_domain'] == ''):
                        normalized_urls.append(normalized)
        
        logger.info(f"Found {len(normalized_urls)} URLs in {url}")
        return {'page_info': page_info, 'urls': normalized_urls}
    
    def _is_valid_endpoint(self, url: str) -> bool:
        """判断是否为有效的API端点，过滤静态资源"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # 过滤静态资源文件
        static_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg', 
                           '.ico', '.woff', '.woff2', '.ttf', '.eot', '.vue', '.exe'}
        
        # 检查是否以静态资源扩展名结尾
        for ext in static_extensions:
            if path.endswith(ext):
                return False
        
        # 过滤包含某些字符的URL
        if '@' in path:
            return False
            
        return True
    
    def extract_subdomains(self, urls: List[str], base_url: str) -> List[str]:
        """提取子域名"""
        base_domain_info = self.extract_domain_info(base_url)
        main_domain = base_domain_info['main_domain']
        
        subdomains = set()
        for url in urls:
            domain_info = self.extract_domain_info(url)
            full_domain = domain_info['full_domain']
            
            if full_domain and main_domain in full_domain:
                subdomains.add(full_domain)
        
        return sorted(list(subdomains))
    
    def extract_from_multiple_urls(self, urls: List[str], include_js: bool = False) -> Dict[str, any]:
        """并发处理多个URL，返回详细信息"""
        all_urls = []
        all_page_info = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.extract_urls_from_page, url, include_js) for url in urls]
            
            for i, future in enumerate(futures):
                try:
                    result = future.result(timeout=30)
                    all_urls.extend(result['urls'])
                    all_page_info.append(result['page_info'])
                    logger.info(f"Processed {i+1}/{len(urls)} URLs")
                except Exception as e:
                    logger.error(f"Error processing URL {i+1}: {e}")
        
        return {
            'urls': list(set(all_urls)),  # 去重
            'page_info': all_page_info
        }
    
    def extract_links_from_page(self, url: str) -> List[str]:
        """提取页面中的所有链接"""
        content = self.fetch_content(url)
        if not content:
            return []
        
        try:
            soup = BeautifulSoup(content, "html.parser")
            links = []
            
            for a_tag in soup.find_all("a", href=True):
                href = a_tag.get("href")
                if href:
                    normalized = self.normalize_url(url, href)
                    if normalized:
                        links.append(normalized)
            
            return list(set(links))
        except Exception as e:
            logger.error(f"Failed to extract links from {url}: {e}")
            return []

def parse_args():
    parser = argparse.ArgumentParser(
        description="Enhanced URL and subdomain extractor",
        epilog="Example: python script.py -u https://example.com -ou urls.txt -os subdomains.txt"
    )
    parser.add_argument("-u", "--url", help="Target website URL")
    parser.add_argument("-c", "--cookie", help="Cookie string for requests")
    parser.add_argument("-f", "--file", help="File containing URLs or JS files")
    parser.add_argument("-ou", "--output-urls", help="Output file for URLs")
    parser.add_argument("-os", "--output-subdomains", help="Output file for subdomains")
    parser.add_argument("-ow", "--output-web-info", help="Output file for web page information")
    parser.add_argument("-j", "--js", action="store_true", help="Extract from JS files")
    parser.add_argument("-d", "--deep", action="store_true", help="Deep extraction (follow links)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    return parser.parse_args()

def save_results(urls: List[str], subdomains: List[str], page_info: List[Dict], 
                output_urls: Optional[str], output_subdomains: Optional[str], output_web_info: Optional[str]):
    """保存结果到文件"""
    if output_urls and urls:
        try:
            with open(output_urls, 'w', encoding='utf-8') as f:
                f.write('\n'.join(urls))
            logger.info(f"Saved {len(urls)} URLs to {output_urls}")
        except Exception as e:
            logger.error(f"Failed to save URLs: {e}")
    
    if output_subdomains and subdomains:
        try:
            with open(output_subdomains, 'w', encoding='utf-8') as f:
                f.write('\n'.join(subdomains))
            logger.info(f"Saved {len(subdomains)} subdomains to {output_subdomains}")
        except Exception as e:
            logger.error(f"Failed to save subdomains: {e}")
    
    if output_web_info and page_info:
        try:
            with open(output_web_info, 'w', encoding='utf-8') as f:
                for info in page_info:
                    line = f"URL: {info['url']} | Status: {info['status_code']} | Title: {info['title']} | Length: {info['content_length']}\n"
                    f.write(line)
            logger.info(f"Saved {len(page_info)} page info records to {output_web_info}")
        except Exception as e:
            logger.error(f"Failed to save web info: {e}")

def main():
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.url and not args.file:
        logger.error("Please specify either -u URL or -f FILE")
        sys.exit(1)
    
    extractor = URLExtractor(cookie=args.cookie, max_workers=args.threads)
    
    try:
        if args.file:
            # 从文件读取URL
            with open(args.file, 'r', encoding='utf-8') as f:
                urls_to_process = [line.strip() for line in f if line.strip()]
            
            if args.js:
                # 处理为JS文件内容
                all_urls = []
                all_page_info = []
                for file_content in urls_to_process:
                    urls = extractor.extract_urls_from_content(file_content)
                    all_urls.extend(urls)
                base_url = all_urls[0] if all_urls else ""
            else:
                # 处理为URL列表
                result = extractor.extract_from_multiple_urls(urls_to_process, include_js=True)
                all_urls = result['urls']
                all_page_info = result['page_info']
                base_url = urls_to_process[0] if urls_to_process else ""
                
        elif args.deep:
            # 深度提取
            logger.info("Starting deep extraction...")
            links = extractor.extract_links_from_page(args.url)
            logger.info(f"Found {len(links)} links to process")
            result = extractor.extract_from_multiple_urls(links, include_js=True)
            all_urls = result['urls']
            all_page_info = result['page_info']
            base_url = args.url
            
        else:
            # 单URL处理
            result = extractor.extract_urls_from_page(args.url, include_js=True)
            all_urls = result['urls']
            all_page_info = [result['page_info']]
            base_url = args.url
        
        # 提取子域名
        subdomains = extractor.extract_subdomains(all_urls, base_url) if base_url else []
        
        # 输出结果
        print(f"\n找到 {len(all_urls)} 个URL:")
        for url in sorted(set(all_urls)):
            print(url)
        
        print(f"\n找到 {len(subdomains)} 个子域名:")
        for subdomain in subdomains:
            print(subdomain)
        
        # 输出页面信息
        if all_page_info and hasattr(all_page_info[0], 'get'):
            print(f"\n页面信息:")
            for info in all_page_info:
                if info.get('status_code', 0) > 0:
                    print(f"URL: {info['url']} | Status: {info['status_code']} | Title: {info['title']} | Length: {info['content_length']}")
        
        # 保存结果
        save_results(sorted(set(all_urls)), subdomains, all_page_info if 'all_page_info' in locals() else [], 
                    args.output_urls, args.output_subdomains, args.output_web_info)
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()
