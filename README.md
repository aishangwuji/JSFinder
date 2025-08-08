# JSFind - 高级URL和子域名提取工具

一个功能强大的Python工具，专门用于从网页和JavaScript文件中提取URL、API端点和子域名。适用于渗透测试、安全研究和Web资产发现。

## ✨ 特性

- 🚀 **高性能并发处理** - 支持多线程并发访问，大幅提升扫描速度
- 🎯 **智能URL提取** - 从HTML和JavaScript代码中精确提取各类URL
- 🌐 **子域名发现** - 自动识别和收集目标域名下的所有子域名
- 📊 **页面信息分析** - 获取HTTP状态码、页面标题、响应长度等详细信息
- 🔍 **深度链接爬取** - 支持递归爬取页面中的所有链接
- 🛡️ **智能过滤** - 自动过滤静态资源，专注于API端点和动态内容
- 📁 **灵活输出** - 支持多种格式的结果输出和保存
- 🔄 **会话复用** - 内置连接池和重试机制，提高稳定性

## 🚀 快速开始

### 安装依赖

```bash
pip install requests beautifulsoup4 urllib3
```

### 基本使用

```bash
# 扫描单个URL
python jsfind.py -u https://example.com

# 从文件批量扫描
python jsfind.py -f urls.txt

# 深度扫描（跟随链接）
python jsfind.py -u https://example.com -d

# 带cookie扫描
python jsfind.py -u https://example.com -c "session_id=xxx; token=yyy"
```

### 输出结果到文件

```bash
python jsfind.py -u https://example.com \
  -ou urls.txt \
  -os subdomains.txt \
  -ow page_info.txt
```

## 📖 详细用法

### 命令行参数

| 参数 | 长参数 | 描述 | 示例 |
|------|--------|------|------|
| `-u` | `--url` | 指定目标URL | `-u https://example.com` |
| `-f` | `--file` | 从文件读取URL列表 | `-f target_urls.txt` |
| `-c` | `--cookie` | 设置请求Cookie | `-c "session=abc123"` |
| `-ou` | `--output-urls` | URL结果输出文件 | `-ou discovered_urls.txt` |
| `-os` | `--output-subdomains` | 子域名输出文件 | `-os subdomains.txt` |
| `-ow` | `--output-web-info` | 页面信息输出文件 | `-ow page_details.txt` |
| `-j` | `--js` | 从JS文件中提取URL | `-j` |
| `-d` | `--deep` | 深度扫描模式 | `-d` |
| `-t` | `--threads` | 线程数量 | `-t 20` |
| `-v` | `--verbose` | 详细输出模式 | `-v` |

### 使用场景

#### 1. 单目标扫描
```bash
# 基本扫描
python jsfind.py -u https://target.com

# 带认证扫描
python jsfind.py -u https://target.com -c "auth_token=xxx"
```

#### 2. 批量扫描
```bash
# 准备URL列表文件
echo "https://site1.com" > targets.txt
echo "https://site2.com" >> targets.txt

# 批量扫描
python jsfind.py -f targets.txt -t 15
```

#### 3. 深度发现
```bash
# 深度扫描，跟随页面链接
python jsfind.py -u https://target.com -d -ou all_urls.txt
```

#### 4. JavaScript文件分析
```bash
# 专门分析JS文件中的URL
python jsfind.py -f js_files.txt -j
```

## 📊 输出格式

### 控制台输出
```
找到 156 个URL:
https://api.example.com/v1/users
https://api.example.com/v1/posts  
https://cdn.example.com/assets/app.js
...

找到 8 个子域名:
api.example.com
cdn.example.com
admin.example.com
...

页面信息:
URL: https://example.com | Status: 200 | Title: Example Site | Length: 2048
```

### 文件输出

**URLs文件 (urls.txt):**
```
https://api.example.com/v1/users
https://api.example.com/v1/posts
https://api.example.com/v2/auth/login
```

**子域名文件 (subdomains.txt):**
```
api.example.com
cdn.example.com
admin.example.com
```

**页面信息文件 (page_info.txt):**
```
URL: https://example.com | Status: 200 | Title: Homepage | Length: 15670网址：https://example.com | 状态：200 | 标题：主页 | 长度：15670
URL: https://api.example.com | Status: 403 | Title: API Gateway | Length: 1024
```

## 🔧 高级配置

### 自定义线程数
```bash
# 提高并发数以加快扫描速度（注意目标服务器承受能力）
python jsfind.py -u https://example.com -t 30
```

### 详细日志输出
```bash
# 启用详细日志以便调试
python jsfind.py -u https://example.com -v
```

### 组合使用
```bash   ”“bash   ”“bash”“bashbash   bash   bash   bash```bash
   ""bash   ""bash""bash   “bash” “bash” “bash”
```
# 完整的扫描配置
python jsfind.py \   Python jsfind.py \
  -u https://target.com \
  -c "session_id=xxx; csrf_token=yyy" \会话 ID 为 xxx；CSRF 令牌为 yyy
  -d \
  -t 20 \
  -ou discovered_urls.txt \
  -os found_subdomains.txt \
  -ow page_analysis.txt \   -ow page_analysis.txt \ （此句为命令行输入，无实际中文翻译内容）
  -v
```

## 🎯 实际应用案例

### 渗透测试中的资产发现
```bash   ”“bash   ”“bash”“bashbash   bash   bash   bash```bash
   ""bash   ""bash""bash   “bash” “bash” “bash”“bash” “bash” “bash” “bash” “bash” “bash”
```
# 1. 首先进行基础扫描
python jsfind.py -u https://target.com -ou initial_urls.txt运行 `jsfind.py` 脚本，使用 `-u` 参数指定目标网址为 `https://target.com`，并将初始网址输出到 `initial_urls.txt` 文件中。

# 2. 深度扫描发现更多端点  
python jsfind.py -u https://target.com -d -ou deep_urls.txt运行 `jsfind.py` 脚本，使用参数 `-u https://target.com` 指定目标网址，使用 `-d` 参数进行深度查找，最后将结果输出到 `deep_urls

# 3. 分析JS文件获取API端点
python jsfind.py -f js_urls.txt -j -ou api_endpoints.txt运行 `jsfind.py` 脚本，使用 `-f js_urls.txt` 参数指定文件，使用 `-j` 参数启用 JavaScript 分析，使用 `-ou api_endpoints.txt` 参数指定输出文件
```

### Bug Bounty中的域名枚举
```bash   ”“bash
# 收集子域名进行进一步测试
python jsfind.py -u https://program.com -d -os subdomains.txtpython jsfind.py -u https://program.com -d -os 子域名.txt
```

## ⚠️ 注意事项

1. **请求频率控制** - 使用`-t`参数合理设置线程数，避免对目标服务器造成过大压力
2. **法律合规** - 仅在授权的测试环境或漏洞奖励项目中使用
3. **网络环境** - 某些网络环境下可能需要配置代理
4. **目标限制** - 部分网站可能有反爬虫机制，适当降低并发数

## 🐛 故障排除

### 常见问题

**Q: 扫描速度很慢怎么办？**  
A: 尝试增加线程数：`-t 20`，但注意不要过高避免被封IP

**Q: 某些页面无法访问？**  
A: 检查是否需要认证，使用`-c`参数添加cookie

**Q: 输出结果为空？**  
A: 使用`-v`参数查看详细日志，检查目标URL是否可访问

**Q: 内存占用过高？**  
A: 降低线程数或分批处理大量URL

## 🔮 更新日志

### v2.0.0
- ✨ 重构为面向对象设计
- 🚀 新增多线程并发处理
- 📊 添加页面信息分析功能
- 🛡️ 智能静态资源过滤
- 🔄 会话复用和重试机制
- 📝 完善的错误处理和日志

### v1.x
- 基础URL提取功能
- 简单的子域名发现

## 📄 许可证

本项目仅供学习和授权测试使用。请在合法合规的前提下使用此工具。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！

---

**⭐ 如果这个工具对你有帮助，请给个Star支持一下！**
