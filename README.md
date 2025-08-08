这是一个为你改进后的 Python 脚本量身定制的 `README.md` 文件。它清晰地介绍了脚本的功能、安装、使用方法，并提供了详细的参数说明和示例，旨在让用户能快速上手。

-----

# URL & Subdomain Extractor (Optimized)

这是一个功能强大的 Python 脚本，用于从网站和文件中高效、并发地提取 URLs、子域名和页面信息。它支持深度爬取，能够处理动态内容中的链接，并提供多种输出格式，包括纯文本和 JSON。

## 主要特性

  - **高效并发**: 使用多线程并发处理 URLs，显著提升扫描速度。
  - **鲁棒性强**: 内置重试机制，能够应对网络波动和服务器错误（如 500, 429 等）。
  - **深度提取**: 支持指定爬取深度，能够从链接中发现更多隐藏的资源。
  - **全面解析**: 不仅从 HTML 中提取链接，还能解析内联和外部 JavaScript 文件中的 URLs。
  - **智能过滤**: 自动过滤静态资源（如图片、CSS）和无效链接，专注于有价值的端点。
  - **多种输出**: 支持将结果输出到URLs文件、子域名文件、页面信息文件，或统一的 **JSON** 文件，便于自动化和数据处理。
  - **友好的用户界面**: 提供进度条，让长时间运行的任务状态一目了然。

## 安装

### 依赖

该脚本依赖于以下 Python 库：

  - `requests`   ——“请求”
  - `beautifulsoup4`
  - `tqdm`
  - `urllib3`

你可以使用 `pip` 一次性安装所有依赖：

```bash   ”“bash   ”“bash”“bash
pip install requests beautifulsoup4 tqdm urllib3
```

### 克隆仓库

```bash
git clone https://github.com/yourusername/url-extractor.git
cd url-extractor
```

（如果你的代码托管在 GitHub 上，可以替换为你的仓库链接）

## 使用方法

### 基础用法

  - **从单个 URL 提取**:

    ```bash
    python main.py -u https://example.com
    ```

  - **从文件中的 URLs 批量提取**:

    `urls.txt` 文件内容示例：

    ```
    https://example.com/page1
    https://example.com/page2
    ```

    执行命令：

    ```bash   ”“bash   ”“bash”“bash
    python main.py -f urls.txt
    ```

### 深度爬取

使用 `-d` 参数指定爬取深度。例如，爬取首页以及从首页找到的链接，深度为 1。

```bash   ”“bash   ”“bash”“bash
python main.py -u https://example.com -d 1
```

### 提取并保存结果

  - **同时保存到多个文件**:

    ```bash   ”“bash   ”“bash”“bash
    python main.py -u https://example.com -d 1 -ou urls.txt -os subdomains.txt -ow web_info.txt
    ```

  - **保存到 JSON 文件**:

    `--output-json   ——output-json` 参数会将所有结果（URLs、子域名和页面信息）保存到一个结构化的 JSON 文件中。

    ```bash   ”“bash
    python main.py -u https://example.com -oj results.json
    ```

## 命令行参数

| 参数              | 缩写 | 类型     | 描述                                       |
| ----------------- | ---- | -------- | ------------------------------------------ |
| `--url   url——`           | `-u` | `string` | 目标网站的 URL。                             |
| `--file   ——文件`          | `-f` | `string   字符串` | 包含 URLs 的文件路径。                         |
| `--cookie`        | `-c` | `string   字符串` | 请求时使用的 Cookie 字符串。               |
| `--deep   ——深`          | `-d` | `int`    | 爬取的深度（默认为 0，不进行深度爬取）。 |
| `--threads   ——线程`       | `-t` | `int`    | 并发线程数（默认为 10）。                    |
| `--output-urls   ——output-urls`   | `-ou`| `string   字符串` | 发现的 URLs 列表输出文件路径。             |
| `--output-subdomains   ——output-subdomains`|`-os`|`string   字符串` | 发现的子域名列表输出文件路径。             |
| `--output-web-info   ——output-web-info`|`-ow   …噢`|`string   字符串` | 页面标题、状态码等信息输出文件路径。       |
| `--output-json   ——output-json`   | `-oj   ——“请求”`| `string   字符串` | 所有结果的 JSON 格式输出文件路径。         |
| `--verbose   ——详细`       | `-v   ——“请求”` | `bool   保龄球`   | 启用详细输出，显示更多日志信息。             |

## 示例

### 场景一：单 URL 深度爬取并输出所有结果

```bash   ”“bash   ”“bash”“bash
python main.py -u https://docs.python.org/3/ -d 2 -ou python_docs_urls.txt -os python_docs_subs.txt -oj python_docs_results.json```bash
   ""bash   ""bash""bash
```
```

  - `url`: 从 `https://docs.python.org/3/` 开始。
  - `deep   深的`: 爬取深度为 2。
  - `output-urls`: URLs 保存到 `python_docs_urls.txt`。   ”“bash
  - `output-subdomains`: 子域名保存到 `python_docs_subs.txt`。   ”“bash   ”“bash   ”“bash
  - `output-json`: 所有信息保存到 `python_docs_results.json`。

### 场景二：使用 Cookie 批量提取

```bash   ”“bash
python main.py -f protected_urls.txt -c "sessionid=xyzabc123" -ou protected_endpoints.txt运行 `main.py` 脚本，使用 `-f` 参数指定文件 `protected_urls.txt`，使用 `-c` 参数设置 `sessionid=xyzabc123`，并将结果输出到 `protected_endpoints.txt` 文件中。
```

  - `file   文件`: 从 `protected_urls.txt` 批量读取 URL。
  - `cookie   饼干`: 使用指定的 Cookie 进行身份验证。
  - `output-urls`: 提取的 URLs 保存到 `protected_endpoints.txt`。
   ”“bash
-----   ”“bash   ”“bash   ”“bash

## 许可证

该项目根据 MIT 许可证发布。
