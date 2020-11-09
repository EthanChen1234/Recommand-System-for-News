import re
import requests
import hashlib
import datetime
import uuid
import time
import json
import sys
from datetime import timedelta, timezone
from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "Host": "bond.aigushou.com",
    "Connection": "keep-alive",
    "appVersion": "3.6.5",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://bond.aigushou.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://bond.aigushou.com/bondH5/quotationBoard?code=001S0ad520DyyR0Hpwc52MA5d52S0ad1&state=",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4"
}

PAGE_SIZE = 100  # 每页最多消息量（每5分钟的最大消息量）
TIME_INTERVAL = 60  # 5min x 60
BATCH_NUM = 50  # 每次最多发送的消息数量

PATTERN_SPLIT_FLAG = r'(出|收|承接|买断|卖断)'
PATTERN_SPLIT_NUM = r'[1-9][-.，、](?!\d)'

RELEASE_FLAG = 'dev'


def spider_pipeline():
    try:
        msgs, curr_time = spider_msgs()  # 爬取所有消息
        msgs = remove_repeating_msgs(msgs)  # 消息去重
        msgs = get_interval_msgs(msgs, curr_time)  # 取最近时间间隔
        msgs = split_msgs(msgs)  # 消息分行
        msgs = convert_msgs(msgs)
        send_msgs(msgs, release_flag=RELEASE_FLAG)
        print(datetime.datetime.now())
    except Exception as e:
        pass


def spider_msgs():
    page_balance = [1, 2]  # QUOTE 1, STOCK 2
    url = 'https://bond.aigushou.com/acceptance-api/wechat/messageList'
    msgs = []
    cur_time = datetime.datetime.now(tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    for balance in page_balance:
        msgs = spider_single_balance_msg(msgs, balance, url)
    msgs.sort(key=lambda x: x['time'])  # 早上 -> 晚上
    return msgs, cur_time


def spider_single_balance_msg(msgs, balance, url, page_size=PAGE_SIZE):
    page_num = 1
    while True:
        params = {
            'pageNum': page_num,
            'pageSize': page_size,
            'balance': balance,
            'token': '',
            'type': 1
        }
        response = requests.post(url=url, data=params, headers=HEADERS, verify=False)
        data = response.json().get('data').get('list')  # 晚上 -> 早上
        if data:
            page_num += 1
            msgs.extend(data)
            break  # 只取最新的一页消息
        # else:
        #     break  # 取所有页的消息
    return msgs


def remove_repeating_msgs(msgs):
    md5_set = set()
    msgs_out = []
    for msg in msgs:
        msg_content = msg['wechat_content']
        msg_md5 = hashlib.md5(msg_content.encode(encoding='UTF-8')).hexdigest()
        if msg_md5 not in md5_set:
            msgs_out.append(msg)
            md5_set.add(msg_md5)
    return msgs_out


def get_interval_msgs(msgs, curr_time, time_interval=TIME_INTERVAL):
    # 取最近时间间隔内的消息
    curr_datetime = datetime.datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')
    msgs_out = []
    for msg in msgs:
        msg_time = msg['time']
        msg_datetime = datetime.datetime.strptime(msg_time, '%Y-%m-%d %H:%M:%S')
        if (curr_datetime-msg_datetime).seconds <= time_interval:
            msgs_out.append(msg)
    return msgs_out


# def split_msgs(msgs, pattern_flag=PATTERN_SPLIT_FLAG, pattern_num=PATTERN_SPLIT_NUM):
#     for i, msg in enumerate(msgs):
#         content_line = msg['wechat_content']
#         index_nums = get_index(content_line, pattern_num)
#         index_flags = get_index(content_line, pattern_flag)
#         if len(index_nums) >= 2:
#             content_line = split_line(content_line, index_nums)
#         elif len(index_flags) >= 2:
#             content_line = split_line(content_line, index_flags)
#         else:
#             content_line = split_line(content_line, [])
#         msgs[i]['wechat_content'] = content_line
#     return msgs
#
#
# def get_index(line, pattern):
#     indexes = []
#     obj_patterns = re.finditer(pattern, line)
#     for obj_pattern in obj_patterns:
#         index_start = obj_pattern.start()
#         indexes.append(index_start)
#     return indexes
#
#
# def split_line(line, indexes):
#     line_out = ''
#     if 0 not in indexes:
#         indexes.insert(0, 0)
#     indexes.append(len(line))
#     for i in range(len(indexes)-1):
#         line_out += (line[indexes[i]: indexes[i+1]] + '\n')
#     return line_out


def convert_msgs(msgs):
    msgs_convert = []
    keys_map = {'msg_content': 'wechat_content', 'wechat_nickname': 'wechat_nickname', 'msg_publish_time': 'time',
                'user_in_group_nickname': 'group_nickname', 'wechat_group_name': 'wechat_group_name'}
    for i, msg in enumerate(msgs):
        msg_temp = {}
        for key1, key2 in keys_map.items():
            msg_temp[key1] = msg.get(key2, '')
        msg_temp['msg_id'] = uuid.uuid1().hex
        msg_temp['platform_type'] = 'AI固收'
        msgs_convert.append(msg_temp)
    return msgs_convert


def send_msgs(msgs, release_flag, batch_num=BATCH_NUM):
    epoch_num = len(msgs) // batch_num if len(msgs) % batch_num == 0 else len(msgs) // batch_num + 1
    url_request = get_host(release_flag)
    for j in range(epoch_num):
        try:
            msgs_batch = msgs[j * batch_num: (j + 1) * batch_num]
            data = {'msg_list': msgs_batch}
            params = json.dumps(data).encode(encoding='UTF8')
            req = Request(url_request, params)
            r = urlopen(req)
            r.close()
            time.sleep(30)  # 有必要的吧
        except Exception as e:
            pass


def get_host(release_flag):
    if release_flag == 'test':
        HOST = "http://118.25.61.166:9100"
    elif release_flag == 'dev':
        HOST = "http://118.25.144.31:9100"
    elif release_flag == 'product':
        HOST = "http://47.100.42.249:9100"
    elif release_flag == 'official':
        HOST = "http://118.25.46.44:9100"
    else:  # local
        HOST = "http://127.0.0.1"
    return HOST + '/ai/nlp/repost/robot'


def get_release_flag():
    if len(sys.argv) == 1:
        return None
    return int(sys.argv[1])


if __name__ == '__main__':
    scheduler = BlockingScheduler()  # 实例化
    scheduler.add_job(spider_pipeline, 'interval', seconds=TIME_INTERVAL)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


# def split_line(line, pattern=r'(出|收|承接|买断|卖断)'):
#     # 收国股5000 出大商3000\n  -> 收国股5000\n  出大商3000\n
#     lines_raw = line.split('\n')
#     line_out = ''
#     for line_raw in lines_raw:
#         # 空行
#         if not line_raw:
#             continue  # ''
#         indexes = []
#         obj_patterns = re.finditer(pattern, line_raw)
#         for obj_pattern in obj_patterns:
#             index_start = obj_pattern.start()
#             indexes.append(index_start)
#         # 不需要分行
#         if len(indexes) < 2:
#             line_out += line_raw + '\n'
#             continue
#         # 分行
#         if 0 not in indexes:
#             indexes.insert(0, 0)
#         indexes.append(len(line_raw))
#         for i in range(len(indexes)-1):
#             line_out += (line_raw[indexes[i]: indexes[i+1]] + '\n')
#     return line_out
#
#
# line = '收国股5000 出大商3000\n'
# out = split_line(line)
# print(out)
