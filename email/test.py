# -*- encoding: utf8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import os
import openpyxl

def del_null_row(filepath):
    print(filepath)
    f=open(filepath,'r')
    fnew=open(filepath+'_new.txt','w+')            # 将结果存入新的文本中
    for line in f.readlines():
        data= str(line.strip())
        if len(data)!=0:
            fnew.write(data)
            fnew.write('\n')
    f.close()
    fnew.close()


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset( msgs ):
    charset = msgs.get_charset()
    if charset is None:
        content_type = msgs.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):        #is_multipart()就是用来判断是否是垃圾邮件，如果是垃圾邮件就返回True，否则返回False
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' :                 #or content_type=='text/html'      ##HTML格式输出
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
            if 'CNY' in str(content) and '手续费' in str(content) and '支付成功' in str(content):
                with open(filename,'w') as f:
                    f.write(content + '\n')
                    f.close()

        else:
            pass
            # print('%sAttachment: %s' % ('  ' * indent, content_type))

if __name__ == "__main__":

    filename = 'D:\pycharm\email\get_email_content.txt'

    # 输入邮件地址, 口令和POP3服务器地址:
    # email = input('Email: ')
    # password = input('Password: ')
    # pop3_server = input('POP3 server: ')

    email = 'jacob_dayby@outlook.com'
    password = 'huawei123..'
    pop3_server = 'pop-mail.outlook.com'

    # 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server,'995')
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    # 身份认证:
    server.user(email)
    server.pass_(password)

    # stat()返回所有邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())

    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # print(resp)             #总邮件数量和大小， # 可以查看b'+OK 6 311323'
    # print(mails)            #每个邮件的大小，# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    print(index)
    for i in range(index):
        print(i + 1)
        resp, lines, octets = server.retr(i + 1)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # print(msg_content)
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)

        print_info(msg)
        # 可以根据邮件索引号直接从服务器删除邮件:
        # server.dele(index)

        # del_null_row(filename)

    # 关闭连接:
    server.quit()