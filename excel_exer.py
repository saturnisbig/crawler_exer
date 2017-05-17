#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import xlrd, xlwt, xlutils


def new_excel(file_name):
    print(u'存储文件不存在，正在创建文件' + file_name)
    book = xlwt.Workbook(encoding='utf-8')
    book.add_sheet('sheet1', cell_overwrite_ok=True)
    book.save(file_name)
    print(u'成功创建文件！' + file_name)


def repeat_name(file_name, name):
    print u'正在检测', name, u'是否存在excel中'
    try:
        book = xlrd.open_workbook(file_name)
        sheet = book.sheet_by_index(0)
        usernames = sheet.col_values(0)
        for user in usernames:
            if user.strip() == name.strip():
                print u'用户名已经存在', name, u'跳过'
                return True
        print u'用户名不存在excel中'
        return False
    except IOError, e:
        if 'No such file' in e.strerror:
            print u'匹配重复时未找到文件', file_name
            new_excel(file_name)
            return False
    return False


def write_to_excel(contents, file_name):
    print u'正在将内容写入excel文件', file_name
    rbook = xlrd.open_workbook(file_name)
    sheet = rbook.sheet_by_index(0)
    row = sheet.nrows
    wbook = xlutils.copy(rbook)
    wsheet = wbook.sheet_by_index(0)
    col = 0
    user = contents[0]
    if not repeat_name(user, file_name):
        for content in contents:
            wsheet.write(row, count, content)
            count += 1
        wb.save(file_name)
        print u'成功写入到文件', file_name, u'第', row+1, u'行'
    else:
        print u'内容已存在，跳过写入文件', file_name


def write_comments(comments, file_name):
    for comment in comments:
        url = comment.get('url', '')
        contents = comment.get('comments', [])
        for content in contents:
            user = content[0]
            text = content[1]
            write_to_excel((user, text, url), file_name)


def write_count(file_name):
    pass
