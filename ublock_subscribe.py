import sys
import re

# 检查命令行参数数量，要求两个：输入文件和输出文件
if len(sys.argv) != 3:
    print("Usage: python convert_to_ublock_subscribe.py <input_rules.txt> <output_rules.txt>")
    sys.exit(1)

input_file = sys.argv[1]    # 第一个参数，输入规则文件路径
output_file = sys.argv[2]   # 第二个参数，输出规则文件路径

# 正则匹配形如 '||domain.com^' 的规则，捕获 domain.com 部分
pattern = re.compile(r'^\|\|([^\^]+)\^$')

# 读取输入文件所有行
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

converted = []   # 用来存放转换后的规则列表

converted.append("! Title: 我的规则")
for line in lines:
    line = line.strip()  # 去除行首尾空白
    # 跳过空行，注释行（以!开头），以及含有 $ 符号的规则（防止误杀复杂规则）
    if not line or line.startswith('!') or '$' in line:
        continue
    # 匹配简单的 ||domain.com^ 规则
    m = pattern.match(line)
    if m:
        domain = m.group(1)  # 获取域名部分
        # 转换为 uBlock 格式，添加 $all 和 redirect=nooptext 标记
        converted.append(f'||{domain}^$all,redirect=nooptext')

# 把所有转换后的规则写入输出文件，每条一行
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(converted))

# 打印转换结果统计
print(f'转换完成，规则数：{len(converted)}，输出文件：{output_file}')
