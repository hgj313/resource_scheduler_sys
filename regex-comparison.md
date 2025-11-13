# JavaScript与Python正则表达式语法对比文档

## 1. 简介

正则表达式（Regular Expression，简称Regex）是一种用于描述字符串模式的强大工具，可以用来匹配、查找、替换符合特定模式的字符串。JavaScript和Python都提供了对正则表达式的支持，虽然基本语法相似，但在具体实现和使用上有一些差异。

## 2. 创建正则表达式

### JavaScript

在JavaScript中，可以通过两种方式创建正则表达式：

1. 字面量形式：`/pattern/flags`
2. 构造函数形式：`new RegExp('pattern', 'flags')`

```javascript
// 字面量形式
const regex1 = /abc/g;

// 构造函数形式
const regex2 = new RegExp('abc', 'g');
```

### Python

在Python中，通过`re`模块来使用正则表达式：

```python
import re

# 使用compile方法创建正则表达式对象
pattern = re.compile(r'abc')

# 直接使用re模块的函数
result = re.search(r'abc', text)
```

## 3. 常用元字符对比

| 元字符 | JavaScript | Python | 描述 |
|--------|------------|--------|------|
| `.` | ✓ | ✓ | 匹配除换行符以外的任意字符 |
| `^` | ✓ | ✓ | 匹配字符串的开始 |
| `$` | ✓ | ✓ | 匹配字符串的结束 |
| `*` | ✓ | ✓ | 匹配前面的子表达式零次或多次 |
| `+` | ✓ | ✓ | 匹配前面的子表达式一次或多次 |
| `?` | ✓ | ✓ | 匹配前面的子表达式零次或一次 |
| `{n}` | ✓ | ✓ | 匹配确定的n次 |
| `{n,}` | ✓ | ✓ | 至少匹配n次 |
| `{n,m}` | ✓ | ✓ | 匹配n到m次 |
| `[]` | ✓ | ✓ | 字符集合 |
| `[^]` | ✓ | ✓ | 负值字符集合 |
| `|` | ✓ | ✓ | 或 |
| `()` | ✓ | ✓ | 分组 |
| `\d` | ✓ | ✓ | 匹配数字字符 |
| `\D` | ✓ | ✓ | 匹配非数字字符 |
| `\w` | ✓ | ✓ | 匹配字母、数字、下划线 |
| `\W` | ✓ | ✓ | 匹配非字母、数字、下划线 |
| `\s` | ✓ | ✓ | 匹配空白字符 |
| `\S` | ✓ | ✓ | 匹配非空白字符 |

## 4. 标志位(flags)对比

| 标志 | JavaScript | Python | 描述 |
|------|------------|--------|------|
| `g` | ✓ | N/A | 全局匹配 |
| `i` | ✓ | `re.IGNORECASE` | 忽略大小写 |
| `m` | ✓ | `re.MULTILINE` | 多行模式 |
| `s` | ✓ | `re.DOTALL` | 使`.`匹配包括换行符在内的所有字符 |
| `u` | ✓ | N/A | Unicode模式 |
| `y` | ✓ | N/A | 粘性匹配 |
| `x` | N/A | `re.VERBOSE` | 扩展模式，允许添加注释 |

## 5. 主要差异

### 5.1 标志位表示方式

JavaScript使用单个字母作为标志位，可以直接在字面量中指定或在构造函数中传递。
Python使用`re`模块中的常量来表示标志位，可以在编译时或使用函数时传递。

### 5.2 命名分组

JavaScript使用`(?<name>...)`语法创建命名分组。
Python同样使用`(?P<name>...)`语法创建命名分组。

### 5.3 反向引用

JavaScript中可以使用`\n`或`\k<name>`进行反向引用。
Python中可以使用`\n`或`(?P=name)`进行反向引用。

## 6. 使用示例

### JavaScript

```javascript
const text = "Hello, my email is example@example.com";
const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
const emails = text.match(emailRegex);
console.log(emails); // ["example@example.com"]
```

### Python

```python
import re

text = "Hello, my email is example@example.com"
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = re.findall(email_pattern, text)
print(emails)  # ['example@example.com']
```

## 7. 总结

JavaScript和Python的正则表达式在基本语法上非常相似，但在标志位表示、命名分组语法和反向引用等方面有一些细微差异。了解这些差异有助于在不同语言环境中正确使用正则表达式。