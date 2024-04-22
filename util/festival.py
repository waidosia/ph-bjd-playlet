from datetime import date

from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()

# 祝福语map
blessing_map = {
    '元旦': '新年快乐！新的一年，新的开始！',
    '腊八': '腊八节快乐！记得喝腊八粥哦！',
    '除夕': '除夕快乐！祝大家新年快乐！',
    '春节': '新年快乐！恭喜发财！',
    '情人节': '情人节快乐！珍惜身边的人！',
    '元宵节': '元宵节快乐！今天吃元宵了吗？',
    '妇女节': '女神节快乐！',
    '清明': '今天你去踏青了嘛！',
    '劳动节': '劳动节快乐！劳动最光荣！',
    '青年节': '青年节快乐！青春永驻！',
    '母亲节': '祝所有的妈妈节日快乐！',
    '儿童节': '儿童节快乐！童心永驻！',
    '端午节': '端午节快乐！粽子好吃！',
    '父亲节': '祝所有的爸爸节日快乐！',
    '建军节': '向所有的军人致敬！',
    '七夕': '七夕节快乐！今天有约会吗？',
    '教师节': '老师，您辛苦了！',
    '中秋节': '中秋节快乐！月圆人团圆！',
    '国庆节': '国庆节快乐！祝祖国繁荣昌盛！',
    '重阳节': '重阳节快乐！登高赏菊！',
    '圣诞节': '圣诞节快乐！圣诞老人来了！',
}


def get_festival_blessing():
    # 获取今天的日期
    d = date.today()
    names = library.get_festival_names(d)
    result = '| '
    for n in names:
        if n in blessing_map:
            result += blessing_map[n] + '| '
    result = result[:-2]
    return result
