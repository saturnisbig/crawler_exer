#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import re

# example1

# 编译成Pattern对象
pat = re.compile(r'hello')
# 匹配成功
result1 = re.match(pat, 'hello')
result2 = re.match(pat, 'hello0 CQC!')
result4 = re.match(pat, 'hello CQC!')
# 匹配失败
result3 = re.match(pat, 'helo CQC!')

# 输出pat匹配的字符串，可能为多个分组
print result1.group()

# example2

# 匹配：单词+空格+单词+任意字符
m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')

# 匹配时使用的文本
print 'm.string:', m.string
# 匹配时使用的Pattern对象
print 'm.re:', m.re
# 文本中正则表达式开始搜索的索引
print 'm.pos:', m.pos
# 文本中正则表达式结束搜索的索引
print 'm.endpos:', m.endpos
# 最后一个捕获的分组在文本中的索引，如果无捕获则为None
print 'm.lastindex:', m.lastindex
# 最后一个捕获的分组的别名，如果无则为None
print 'm.lastgroup:', m.lastgroup
# 一个或多个分组捕获的字符串，多个参数时将以元组形式返回；
# 可以使用编号也可以使用别名，编号0代表整个匹配字符串，不填写参数返回goup(0)
print 'm.goup()', m.group()
# 以元组形式返回全部捕获的字符串
print 'm.groups():', m.groups()
# 返回有以别名的组，别名为健、捕获字符串为值的字典
print 'm.groupdict():', m.groupdict()
# 返回指定的组捕获的子串在string中的索引(子串第一个字符的索引)
print 'm.start(2):', m.start(2)
# end([group])，返回指定的组在捕获的子串中的结束索引
print 'm.end(2):', m.end(2)
# span([goup])，返回指定的组捕获的字符串的开始和结束索引
print 'm.span(2):', m.span(2)
# expan(template)，将匹配的分组代入template中，可以使用\id或
# \g引用分组，但不能使用编号0
print 'm.expand(r"\g \g\g"):', m.expand(r'\2 \1\3')

#
