from datetime import datetime, timedelta


def get_today_0am_timestamp(timestamp):
    # 将时间戳转换为日期时间对象
    current_datetime = datetime.fromtimestamp(timestamp)
    # 获取今日日期
    today_date = current_datetime.date()
    # 构造今日0时的日期时间对象
    today_0am_datetime = datetime.combine(today_date, datetime.min.time())
    # 获取今日0时的时间戳
    today_0am_timestamp = today_0am_datetime.timestamp()

    return today_0am_timestamp

def get_target_0am_timestamp(targetTimestamp):
    target_date = targetTimestamp.date()
    # 构造目标0时的日期时间对象
    target_0am_datetime = datetime.combine(target_date, datetime.min.time())
    # 获取目标0时的时间戳
    target_0am_timestamp = target_0am_datetime.timestamp()

    return target_0am_timestamp

def is_same_day(timestamp):
    # 获取当前时间戳
    current_timestamp = datetime.now().timestamp()

    # 将时间戳转换为日期时间对象
    current_datetime = datetime.fromtimestamp(current_timestamp)
    target_datetime = datetime.fromtimestamp(timestamp)

    # 获取当前日期和目标日期
    current_date = current_datetime.date()
    target_date = target_datetime.date()

    print("is_same_day {},{}".format(current_date,target_date))

    # 判断是否为同一天
    if current_date == target_date:
        return True
    else:
        return False