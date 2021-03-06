import baostock as bs
import pandas as pd
import datetime


'''
参考文章： http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5
'''

'''
在调用方法get_k_line 前需要至少调用一次登录
'''
def login_in():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    if(lg.error_code !='0'):
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)

'''
在调用方法get_k_line 不在使用后需要调用该方法登出
'''
def login_out():
    #### 登出系统 ####
    bs.logout()


def get_k_line(code,start_date,end_date):


    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg


    rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date=start_date, end_date=end_date,
        frequency="d", adjustflag="3")

    # print('query_history_k_data_plus respond error_code:'+rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    pd.set_option('display.max_columns', 20)

    result = pd.DataFrame(data_list, columns=rs.fields)

    return result



if __name__ == '__main__':
    login_in()

    today = str(datetime.date.today())
    thirty_ago =str(datetime.date.today() - datetime.timedelta(30))
    one_half_year =str(datetime.date.today() - datetime.timedelta(500))
    print(one_half_year)

    print(get_k_line('sz.000832', one_half_year, today))

    login_out()
