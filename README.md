# 国家自然科学基金申请书正文模板（主要面上项目）

[![compile](https://github.com/wenh06/NSFC-Template/actions/workflows/compile.yml/badge.svg)](https://github.com/wenh06/NSFC-Template/actions/workflows/compile.yml)
[![license](https://img.shields.io/github/license/wenh06/NSFC-Template?style=flat-square)](LICENSE)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wenh06/NSFC-Template)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/wenh06/NSFC-Template/latest)

主要基于 [NSFC-LaTeX-Template](https://github.com/Ruzim/NSFC-application-template-latex) 修改而来，感谢原作者。

主要修改如下：

1. 将各个部分拆分成单独的文件，尤其是第一部分“立项依据与研究内容”，方便协作，以及分别统计字数。因为包含标题，所以字数统计会稍微多一些。

2. 利用 `biblatex` 和 `biber` 处理参考文献 (`\usepackage[backend=biber, style=gb7714-2015, maxbibnames=5]{biblatex}`)，可以用 `\parencite` 等命令引用文献。

3. 利用 [`texcount`](https://ctan.org/pkg/texcount) 工具以及 [`currfile`](https://ctan.org/pkg/currfile) 宏包统计各部分字数。 `currfile` 宏包也被用于动态路径拼接。

目前来看，面上项目、青年项目、重点项目的申请书格式基本都是一样的，只是字数要求不同，此外青年项目没有 `主要参与者`，面上项目页边距稍小。

## 更新状态

| 项目类型           | 已更新2026版       |
|-------------------|--------------------|
| 面上项目           | :heavy_check_mark: |
| 青年C             | :xheavy_check_mark: |
| 重点项目           | :x:                |
| 专项项目           | :x:                |

## 一些有用的命令

### 1. 编译

```bash
python compile.py [filename]
```

[filename] 是文件名，可以不写，默认为 `main.tex`。报错停止编译了按 `ctrl+c` 退出。以上文件包含了用 `latexmk` 编译

```bash
latexmk -xelatex --shell-escape -f -outdir=build [filename]
```

以及清理中间文件的命令

```bash
latexmk -C [filename]
```

以及一些文件名的替换等操作。

### 2. 创建新项目申请书

使用如下命令可以快速创建一个新的项目申请书：

```bash
python create.py [project-type] [project-name]
```

其中 `program-type` 是项目类型，包括

- `youth`: 青年基金，同义词 `y`
- `general`: 面上项目，同义词 `g`
- ~~`key`: 重点项目，同义词 `k`~~
- ~~`dedicated`: 专项项目，同义词 `d`~~

查看帮助：

```bash
python create.py help
```

### 3. 数字数

```bash
texcount -inc -sum -0 -utf8 -ch -template={SUM} [filename]
```

[filename] 是文件名。因为本项目将申请书的各部分分开了，所以可以分别统计。例如，统计 `项依据与研究内容` 的字数：

```bash
texcount -inc -sum -0 -utf8 -ch -template={SUM} general-program/template/1-立项依据与研究内容/aggregate.tex
```

### 3. DEBUG

biblatex 会报一些警告，但是不影响编译。可以忽略。

```text
BibTeX subsystem: warning: comma(s) at end of name (removing)
```

以上错误是因为 bib 文件中的作者 (author)、编辑 (editor) 字段的名字后面有逗号 (例如 arXiv 上的 GPT-4 技术报告)，可以用下面的命令查找：

```bash
grep -nP '(?:author|editor)\s*=.*,\s*(?:and|})' *.bib
```

## 已知问题

1. 计字数工具 `texcount` 无法处理带变量的路径，它不会把 `\currfiledir` 替换成实际路径，所以在 `1-立项依据与研究内容/aggregate.tex` 中需要手动修改路径：

```latex
% \input{\currfiledir 1-项目的立项依据}
\input{general-program/template/1-立项依据与研究内容/1-项目的立项依据}
```

如果要修改 `template` 文件夹的名字，需要进到其中的 `1-立项依据与研究内容/aggregate.tex` 中修改路径。
用 `\input{\currfiledir 1-项目的立项依据}` 能正确编译，但是无法正确统计字数。
