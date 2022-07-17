import os
from io import BytesIO
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import base64
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from pyecharts.charts import Boxplot
from bike import db
import os

@csrf_exempt
def index(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'index.html', {"userName": userName})
    # render打开html文件


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def post_Login(request):
    userName = request.POST['userName']
    password = request.POST['password']
    userName_msg = ''
    password_msg = ''
    if userName == '':
        userName_msg = '请输入用户名'
        return render(request, 'login.html')
    else:
        data = db.is_password_correct(userName)
        if not data:
            userName_msg = '用户名不存在'
            return render(request, 'login.html', {"userName_msg": userName_msg})
        else:
            if password == str(data[0][0]):
                request.session["is_login"] = "1"
                request.session["userName"] = userName
                response = HttpResponseRedirect('/index')
                response.set_cookie('userName', userName)
                return response
            else:
                password_msg = '密码错误'
                return render(request, 'login.html', {"userName_msg": userName_msg, "password_msg": password_msg})


def logout(request):
    response = HttpResponseRedirect('/index')
    response.delete_cookie('userName')
    return response


def post_Register(request):
    userName = request.POST['userName']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    email = request.POST['email']
    company = request.POST['company']
    db_data = db.select_All()
    username_msg = ''
    password_msg = ''
    email_msg = ''
    company_msg = ''
    if userName == '':
        username_msg = '请输入用户名'
    for i in db_data:
        if userName == i[0]:
            username_msg = username_msg + ' ' + '用户名已存在，请重新输入'
            break
    if password == '' or confirm_password == '':
        password_msg = '请输入密码'
    if password != confirm_password:
        password_msg = password_msg + ' ' + '两次密码输入不一致，请重新输入'
    if email == '':
        email_msg = '邮箱不能为空，请输入邮箱'
    if company == '':
        company_msg = '公司或学校不能为空'
    if username_msg == '' and password_msg == '' and email_msg == '' and company_msg == '':
        db.mysql_connect(userName, password, email, company)
        request.session["is_login"] = "1"
        request.session["userName"] = userName
        response = HttpResponseRedirect('/index')
        response.set_cookie('userName', userName, 3600)
        return response
    else:
        return render(request, 'register.html',
                      {"username_msg": username_msg, "password_msg": password_msg, "email_msg": email_msg,
                       "company_msg": company_msg,
                       "userName": userName, "password": password, "confirm_password": confirm_password, "email": email,
                       "company": company})


def dataset(request):
    userName = request.COOKIES.get('userName', '')
    # print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    return render(request, 'dataset.html', {'userName': userName})


def upload(request):
    userName = request.COOKIES.get('userName')
    msg = ''
    if request.method == "POST":
        userName = request.COOKIES.get('userName')
        name = request.POST['name']
        description = request.POST['description']
        myFile = request.FILES.get("file", None)
        select_all = db.select_file_all(userName)
        position = os.path.join('C:\\Users\\wanghui\\Desktop\\test', userName, myFile.name)
        name_num = 0
        path_num = 0
        for i in select_all:
            if name == i[1]:
                name_num = name_num + 1
            if position == i[3]:
                path_num = path_num + 1
        if name_num != 0:
            msg = '请重新命名数据名称  '
        if path_num != 0:
            msg = msg + '您已经上传过此名称的数据，请重新选择'
        if name_num != 0 or path_num != 0:
            return render(request, 'dataset.html', {"msg": msg, "userName": userName, "name": name, "description": description, "file":myFile})
        else:
            myFile = request.FILES.get("file", None)
            print(myFile)
            if not myFile:
                return render(request, 'dataset.html', {"msg": "no files for upload!", "userName": userName})
            else:
                path = "C:\\Users\\wanghui\\Desktop\\test\\" + userName
                a = os.path.isdir(path)
                print(a)
                if a == True:
                    position = os.path.join('C:\\Users\\wanghui\\Desktop\\test', userName, myFile.name)
                    filePath = position
                    destination = open(position, 'wb+')
                    for chunk in myFile.chunks():
                        destination.write(chunk)
                    db.save_file(userName, name, description, filePath)
                    destination.close()
                    return render(request, 'dataset.html', {"msg": "upload over!", "userName": userName, "name": name, "description": description, "file":myFile})
                else:
                    os.mkdir(path)
                    position = os.path.join('C:\\Users\\wanghui\\Desktop\\test', userName, myFile.name)
                    filePath = position
                    destination = open(position, 'wb+')
                    for chunk in myFile.chunks():
                        destination.write(chunk)
                    db.save_file(userName, name, description, filePath)
                    destination.close()
                    return render(request, 'dataset.html', {"msg": "upload over!", "userName": userName})


def history_data_analyse(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'history_data_analyse.html', {"userName": userName})


def visualisation(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'visualisation.html', {"userName": userName})


# 骑行路线
# 北京
def v_bike_route(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'history_data_analyse.html',
                  {"src": 'http://127.0.0.1:8000/if_bike_route', "userName": userName})


def bike_route(request):
    return render(request, './chart/map_route_beijing_10.html')


# 0510
def route_0510(request):
    return render(request, './chart/map_route_beijing_10.html')


def route_0511(request):
    return render(request, './chart/map_route_beijing_11.html')


def route_0512(request):
    return render(request, './chart/map_route_beijing_12.html')


def route_0513(request):
    return render(request, './chart/map_route_beijing_13.html')


def route_0514(request):
    return render(request, './chart/map_route_beijing_14.html')


# # 上海
# def v_route_shanghai(request):
#     return render(request, 'visualisation.html', {"src": 'http://127.0.0.1:8000/if_route_shanghai'})
# def route_shanghai(request):
#     return render(request, '迁移图0510.html')

# 热点区域
# 北京
def v_heat_area(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'history_data_analyse.html',
                  {"src": 'http://127.0.0.1:8000/if_heat_area', "userName": userName})


def heat_area(request):
    return render(request, './chart/map_heat_beijing_10.html')


def heat_0510(request):
    return render(request, './chart/map_heat_beijing_10.html')


def heat_0511(request):
    return render(request, './chart/map_heat_beijing_11.html')


def heat_0512(request):
    return render(request, './chart/map_heat_beijing_12.html')


def heat_0513(request):
    return render(request, './chart/map_heat_beijing_13.html')


def heat_0514(request):
    return render(request, './chart/map_heat_beijing_14.html')


# # 上海
# def v_heat_shanghai(request):
#     return render(request, 'visualisation.html', {"src": 'http://127.0.0.1:8000/if_heat_shanghai'})
# def heat_shanghai(request):
#     return render(request, '迁移图0510.html')

# 影响因素
# 天气
def weather(request):
    return render(request, './chart/chart_pie_weather.html')


# 节假日
def holiday(request):
    return render(request, './chart/chart_line_holiday.html')


# 月份
def month(request):
    return render(request, './chart/chart_boxplot_month.html')


# 季节
def season(request):
    return render(request, './chart/chart_pie_season.html')


# 温度
def temperature(request):
    return render(request, './chart/chart_line_temperature.html')


# # 露点
# def v_dew_point(request):
#     userName = request.COOKIES.get('userName', '')
#     return render(request, 'visualisation.html', {"src": 'http://127.0.0.1:8000/if_dew_point', "userName": userName})
# def dew_point(request):
#     return render(request, '迁移图0510.html')
# 湿度
def humidity(request):
    return render(request, './chart/chart_line_humidity.html')


# # 气压
# def v_pressure(request):
#     userName = request.COOKIES.get('userName', '')
#     return render(request, 'visualisation.html', {"src": 'http://127.0.0.1:8000/if_pressure', "userName": userName})
# def pressure(request):
#     return render(request, '迁移图0510.html')
# 能见度

def visibility_miles(request):
    return render(request, './chart/chart_line_visibility.html')


# 风速

def wind_speed(request):
    return render(request, './chart/chart_line_wind_speed.html')


# 降水量

def precipitation(request):
    return render(request, './chart/chart_line_Precipitation.html')


def temp_speed(request):
    return render(request, './chart/temp_speed.html')


# 用户画像
# 性别

def gender(request):
    return render(request, './chart/chart_pictorial_bar_gender.html')


# 年龄

def age(request):
    return render(request, './chart/chart_line_age.html')


# 是否为注册用户

def is_register(request):
    return render(request, './chart/chart_pie_user_type.html')


# 可视化
def self_visualisation(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, 'self_visualisation.html', {"userName": userName})


def influence(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, '../templates/self_chart/self_influence.html', {"userName": userName})


def user(request):
    userName = request.COOKIES.get('userName', '')
    return render(request, '../templates/self_chart/self_user.html', {"userName": userName})


def self_rose_season(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                print(name)
                print(db.selece_file(name)[0])
                file_path = db.selece_file(name)[0][0]

                data = pd.read_csv(file_path)
                data_columns = data.columns.values.tolist()
                print(data_columns)
                data_x = []
                count = []
                for i in range(0, len(data[data_columns[0]])):
                    data_x.append(data[data_columns[0]][i])
                    count.append(int(data[data_columns[1]][i]))
                print(data_x)
                print(count)
                # count = [15, 25, 50, 37, 8]
                import pyecharts.options as opts
                from pyecharts.charts import Pie
                pie = (
                    Pie(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add(
                        series_name="",
                        data_pair=[list(z) for z in zip(data_x, count)],
                        radius=["30%", "75%"],
                        center=["50%", "50%"],
                        rosetype="radius",
                        label_opts=opts.LabelOpts(is_show=False, position="center"),
                    )
                        .set_global_opts(
                        legend_opts=opts.LegendOpts(pos_left="right", orient="vertical"),
                        title_opts=opts.TitleOpts(title="玫瑰图"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    )
                        .set_series_opts(
                        tooltip_opts=opts.TooltipOpts(
                            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                        ),
                        label_opts=opts.LabelOpts(
                            formatter="{b}: {c} ({d}%)",
                            font_size=15
                        )
                    )
                )
                pie.render("templates/self_chart/season_rose.html")
                userName = request.COOKIES.get('userName', '')
                return render(request, './self_chart/season_rose.html', {"userName": userName})

            else:
                userName = request.COOKIES.get('userName', '')
                print(db.select_file_all(userName))
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_season_rose.html', {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            print(db.select_file_all(userName))
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_season_rose.html',
                          {"userName": userName, "data": data, "msg": "没有找到文件，或文件读取异常，请重新选择"})


def self_month(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                import pyecharts.options as opts
                from pyecharts.charts import Pie
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                data_columns = data.columns.values.tolist()
                data_xaxis = data.groupby(data_columns[0])
                print("----------------------")
                xaxis = []
                yaxis = []
                for key, value in data_xaxis:
                    xaxis.append(key)
                    yaxis.append(value[data_columns[1]].tolist())
                # return render(request, 'index.html')
                print(xaxis)
                print(yaxis)
                c = Boxplot(init_opts=opts.InitOpts(width="100%", height="600px"))
                c.add_xaxis(xaxis)
                c.add_yaxis("", c.prepare_data(yaxis))
                c.set_global_opts(
                    title_opts=opts.TitleOpts(title='箱线图'),
                    xaxis_opts=opts.AxisOpts(name=data_columns[0]),
                    yaxis_opts=opts.AxisOpts(name=data_columns[1]),
                    tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    toolbox_opts=opts.ToolboxOpts(is_show=True),
                )
                c.render("templates/self_chart/month_boxplot.html")
                return render(request, './self_chart/month_boxplot.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_month.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_month.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_holiday(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                import pyecharts.options as opts
                from pyecharts.charts import Line
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                print(file_path)
                data_columns = data.columns.values.tolist()
                print("----------------------")
                xaxis = []
                y1axis = []
                y2axis = []
                for i in range(0, len(data[data_columns[0]])):
                    xaxis.append(data[data_columns[0]][i])
                    y1axis.append(int(data[data_columns[1]][i]))
                    y2axis.append(int(data[data_columns[2]][i]))
                # return render(request, 'index.html')
                print(xaxis)
                line = (
                    Line(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add_xaxis(xaxis_data=xaxis)
                        .add_yaxis(
                        series_name=data_columns[1][0],
                        y_axis=y1axis,
                        markpoint_opts=opts.MarkPointOpts(
                            data=[
                                opts.MarkPointItem(type_="max", name="最大值"),
                                opts.MarkPointItem(type_="min", name="最小值"),
                                opts.MarkPointOpts()
                            ]
                        ),
                        markline_opts=opts.MarkLineOpts(
                            data=[opts.MarkLineItem(type_="average", name="平均值")]
                        ),
                    )
                        .add_yaxis(
                        series_name=data_columns[2][0],
                        y_axis=y2axis,
                        markpoint_opts=opts.MarkPointOpts(
                            data=[
                                opts.MarkPointItem(type_="max", name="最大值"),
                                opts.MarkPointItem(type_="min", name="最小值"),
                                opts.MarkPointOpts()
                            ]
                        ),
                        markline_opts=opts.MarkLineOpts(
                            data=[opts.MarkLineItem(type_="average", name="平均值")]
                        ),
                    )
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="折线图"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                        toolbox_opts=opts.ToolboxOpts(is_show=True),
                        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, name=data_columns[0]),
                        yaxis_opts=opts.AxisOpts(name=data_columns[1])
                    )
                )
                line.render("templates/self_chart/holiday_line.html")
                return render(request, './self_chart/holiday_line.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_line_holiday.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_line_holiday.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_visibility(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                import pyecharts.options as opts
                from pyecharts.charts import Bar
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                print(file_path)
                data_columns = data.columns.values.tolist()
                print("----------------------")
                xaxis = []
                y1axis = []
                y2axis = []
                print(data_columns)
                for i in range(0, len(data[data_columns[0]])):
                    xaxis.append(data[data_columns[0]][i])
                    y1axis.append(int(data[data_columns[1]][i]))
                # return render(request, 'index.html')
                print("y1")
                print(y1axis)
                bar = (
                    Bar(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add_xaxis(xaxis_data=xaxis)
                        .add_yaxis(
                        series_name=data_columns[1][0],
                        y_axis=y1axis,
                        markpoint_opts=opts.MarkPointOpts(
                            data=[
                                opts.MarkPointItem(type_="max", name="最大值"),
                                opts.MarkPointItem(type_="min", name="最小值"),
                                opts.MarkPointOpts()
                            ]
                        ),
                    )
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="柱状图"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                        toolbox_opts=opts.ToolboxOpts(is_show=True),
                        xaxis_opts=opts.AxisOpts(name=data_columns[0]),
                        yaxis_opts=opts.AxisOpts(name=data_columns[1])
                    )
                )
                bar.render("templates/self_chart/visibility_bar.html")
                return render(request, './self_chart/visibility_bar.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_bar_visliality.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_bar_visliality.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def table(request):
    return render(request, './self_chart/table.html')


def self_temp_speed(request):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":

                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                print(file_path)
                data_columns = data.columns.values.tolist()
                print("----------------------")
                xaxis = []
                y1axis = []
                print(data_columns)
                for i in range(0, len(data[data_columns[0]])):
                    xaxis.append(data[data_columns[0]][i])
                    y1axis.append(int(data[data_columns[1]][i]))
                # return render(request, 'index.html')
                print("y1")
                print(xaxis)
                print(y1axis)
                matplotlib.rc("font", family='YouYuan')
                plt.figure(figsize=(10, 8))
                sns.kdeplot(x=xaxis, y=y1axis, shade=True, cmap='YlGnBu', cbar=False)
                sns.despine(top=True, right=True)
                # plt.grid(linestyle='--',alpha=0.4)

                plt.xlabel(data_columns[0], fontsize=13)
                plt.ylabel(data_columns[1], fontsize=13)
                plt.title('核密度曲线图', fontsize=20)
                figfile = BytesIO()
                plt.savefig(figfile, format='png')
                figfile.seek(0)
                figdata_png = base64.b64encode(figfile.getvalue())  # 将图片转为base64
                figdata_str = str(figdata_png, "utf-8")  # 提取base64的字符串，不然是b'xxx'

                # 保存为.html
                html = '<img width="750px" src=\"data:image/png;base64,{}\"/>'.format(figdata_str)
                filename = 'templates/self_chart/kdeplot.html'
                with open(filename, 'w') as f:
                    f.write(html)
                plt.close()
                return render(request, './self_chart/kdeplot.html', {"userName": userName, })
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_kdeplot_temp.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_kdeplot_temp.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_route(request):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Geo, Timeline, BMap
    from pyecharts.globals import ChartType, SymbolType
    userName = request.COOKIES.get('userName', '')
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                data_columns = data.columns.values.tolist()
                print(data_columns)
                location = []
                for i in range(0, len(data[data_columns[0]])):
                    location.append([[data[data_columns[0]][i], data[data_columns[1]][i]],
                                     [data[data_columns[2]][i], data[data_columns[3]][i]]])
                print(location)
                bmap = (
                    BMap(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add_schema(
                        baidu_ak="gyPK3aqp49SVNuM0GIo3EeTrjpwG5UIn",
                        center=[116.40, 40.04],
                        is_roam=True,
                        zoom=7
                    )
                        .add(
                        series_name="",
                        type_=ChartType.LINES,
                        data_pair=location,
                        is_polyline=True,
                        is_large=True,
                        effect_opts=opts.EffectOpts(
                            symbol='arrow', symbol_size=1, color="white"
                        ),
                        linestyle_opts=opts.LineStyleOpts(opacity=0.6, width=1, color="purple"),
                    )
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="BMap-Route"),
                    )
                )
                bmap.render("templates/self_chart/route.html")
                userName = request.COOKIES.get('userName', '')
                return render(request, './self_chart/route.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                print(db.select_file_all(userName))
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                print("------------")
                print(data)
                return render(request, './self_chart/self_route.html', {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            print(db.select_file_all(userName))
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            print("------------")
            print(data)
            return render(request, './self_chart/self_route.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_heat(request):
    import pandas as pd
    userName = request.COOKIES.get('userName', '')
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                name = request.POST['file']
                map_type = request.POST['map_type']
                file_path = db.selece_file(name)[0][0]

                data = pd.read_csv(file_path)
                data_columns = data.columns.values.tolist()
                location = []
                count = []
                for i in range(0, len(data[data_columns[0]])):
                    location.append(data[data_columns[0]][i])
                    count.append(int(data[data_columns[1]][i]))
                print(location)
                print(count)
                from pyecharts import options as opts
                from pyecharts.charts import Map

                c = (
                    Map(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add(
                        data_columns[1],
                        data_pair=[list(z) for z in zip(location, count)],
                        maptype=map_type,
                        is_map_symbol_show=False
                    )
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="Map-heatMap"),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=max(count),
                            range_text=["High", "Low"],
                            is_calculable=True,
                            range_color=["lightskyblue", "yellow", "orangered"],
                        ),
                    )
                        .render("templates/self_chart/heat.html")
                )

                # c.render("templates/self_chart/heat.html")
                userName = request.COOKIES.get('userName', '')
                return render(request, './self_chart/heat.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_heat.html', {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_heat.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_gender(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                import pyecharts.options as opts
                from pyecharts.charts import Bar
                name = request.POST['file']
                graphical = request.POST['graphical']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                print(file_path)
                data_columns = data.columns.values.tolist()
                print("----------------------")
                xaxis = []
                y1axis = []
                print(data_columns)
                print(graphical)
                for i in range(0, len(data[data_columns[0]])):
                    xaxis.append(str(data[data_columns[0]][i]))
                    y1axis.append(int(data[data_columns[1]][i]))
                from pyecharts import options as opts
                from pyecharts.charts import PictorialBar, Pie, Grid
                image = 'image://static/images/' + graphical + '.png'
                pictorial_bar = (
                    PictorialBar(init_opts=opts.InitOpts(width='90%', height='600px'))
                        .add_xaxis(xaxis)
                        .add_yaxis(
                        "",
                        y1axis,
                        label_opts=opts.LabelOpts(is_show=False),
                        symbol_size=[30, 30],
                        symbol_repeat="fixed",
                        symbol_offset=[0, 5],
                        is_symbol_clip=True,
                        symbol=image
                        # symbol=SymbolType.ARROW
                    )
                        .reversal_axis()
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="象形柱图"),
                        xaxis_opts=opts.AxisOpts(name=data_columns[1]),
                        yaxis_opts=opts.AxisOpts(
                            name=data_columns[0],
                            axistick_opts=opts.AxisTickOpts(is_show=False),
                            axisline_opts=opts.AxisLineOpts(
                                linestyle_opts=opts.LineStyleOpts(opacity=1)
                            ),
                        ),
                    )
                        .set_series_opts(
                        tooltip_opts=opts.TooltipOpts(
                            trigger="item", formatter="{b}: {c}"
                        ),
                        label_opts=opts.LabelOpts(
                            formatter="{b}: {c}",
                            font_size=15
                        )
                    )
                )
                pictorial_bar.render("templates/self_chart/gender_pictorial.html")
                return render(request, './self_chart/gender_pictorial.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_gender_pi.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_gender_pi.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_age(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                import pyecharts.options as opts
                from pyecharts.charts import Line
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                file_path = db.selece_file(name)[0][0]
                data = pd.read_csv(file_path)
                print(file_path)
                data_columns = data.columns.values.tolist()
                print("----------------------")
                xaxis = []
                y1axis = []
                y2axis = []
                print(data_columns)
                for i in range(0, len(data[data_columns[0]])):
                    xaxis.append(str(data[data_columns[0]][i]))
                    y1axis.append(int(data[data_columns[1]][i]))
                # return render(request, 'index.html')
                print("y1")
                print(xaxis)
                line = (
                    Line(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add_xaxis(xaxis_data=xaxis)
                        .add_yaxis(
                        series_name=data_columns[1][0],
                        y_axis=y1axis,
                        markpoint_opts=opts.MarkPointOpts(
                            data=[
                                opts.MarkPointItem(type_="max", name="最大值"),
                                opts.MarkPointItem(type_="min", name="最小值"),
                                opts.MarkPointOpts()
                            ]
                        ),
                        markline_opts=opts.MarkLineOpts(
                            data=[opts.MarkLineItem(type_="average", name="平均值")]
                        ),
                    )
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                        .set_global_opts(
                        title_opts=opts.TitleOpts(title="折线图"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                        toolbox_opts=opts.ToolboxOpts(is_show=True),
                        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, name=data_columns[0]),
                        yaxis_opts=opts.AxisOpts(name=data_columns[1])
                    )
                )
                line.render("templates/self_chart/age_line.html")
                return render(request, './self_chart/age_line.html', {"userName": userName})
            else:
                userName = request.COOKIES.get('userName', '')
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_age_line.html',
                              {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_age_line.html',
                          {"userName": userName, "data": data, "msg": "没有获取文件，或文件读取异常，请重新选择"})


def self_is_register(request):
    userName = request.COOKIES.get('userName', '')
    print(userName)
    if not userName:
        return HttpResponseRedirect('/login')
    else:
        try:
            if request.method == "POST":
                name = request.POST['file']
                chart_name = request.POST['chart_name']
                print(name)
                print(db.selece_file(name)[0])
                file_path = db.selece_file(name)[0][0]

                data = pd.read_csv(file_path)
                data_columns = data.columns.values.tolist()
                print(data_columns)
                data_x = []
                count = []
                for i in range(0, len(data[data_columns[0]])):
                    data_x.append(data[data_columns[0]][i])
                    count.append(int(data[data_columns[1]][i]))
                print(data_x)
                print(count)
                # count = [15, 25, 50, 37, 8]
                import pyecharts.options as opts
                from pyecharts.charts import Pie
                pie = (
                    Pie(init_opts=opts.InitOpts(width="100%", height="600px"))
                        .add(
                        series_name="",
                        data_pair=[list(z) for z in zip(data_x, count)],
                        center=["50%", "50%"],
                        label_opts=opts.LabelOpts(is_show=False, position="center"),
                    )
                        .set_global_opts(
                        legend_opts=opts.LegendOpts(pos_left="right", orient="vertical"),
                        title_opts=opts.TitleOpts(title="饼图"),
                        tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    )
                        .set_series_opts(
                        tooltip_opts=opts.TooltipOpts(
                            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                        ),
                        label_opts=opts.LabelOpts(
                            formatter="{b}: {c} ({d}%)",
                            font_size=15
                        )
                    )
                )
                pie.render("templates/self_chart/register_pie.html")
                userName = request.COOKIES.get('userName', '')
                return render(request, './self_chart/register_pie.html', {"userName": userName})

            else:
                userName = request.COOKIES.get('userName', '')
                print(db.select_file_all(userName))
                data = {}
                for i in range(0, len(db.select_file_all(userName))):
                    data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
                return render(request, './self_chart/self_pie_regis.html', {"userName": userName, "data": data})
        except:
            userName = request.COOKIES.get('userName', '')
            print(db.select_file_all(userName))
            data = {}
            for i in range(0, len(db.select_file_all(userName))):
                data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][2]
            return render(request, './self_chart/self_pie_regis.html',
                          {"userName": userName, "data": data, "msg": "没有找到文件，或文件读取异常，请重新选择"})


def tagString(str):
    return str.get_text().strip().split("<")[0]


def get_tag(year, month, day):
    import requests
    import xlwt
    from bs4 import BeautifulSoup as bs
    response = requests.get(
        "https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D=351409&areaInfo%5BareaType%5D=1&date%5Byear%5D=" + year + "&date%5Bmonth%5D=" + month)
    soup = bs(response.content.decode("unicode_escape"), "html.parser")
    tr = soup.find("table").find_all("tr")  # 获得table中的所有记录行，th是字段行，tr是记录行
    trlist = []
    for j in tr[1:]:
        td = j.find_all("td")  # 获得一个tr中的所有td，学过前端的应该很好理解
        date = tagString(td[0])[:10]
        date = pd.to_datetime(date)
        temp_max = tagString(td[1])[:1]
        temp_min = tagString(td[2])[:1]
        weather = tagString(td[3])
        if str(day) == str(date.day):
            temp_avg = int((int(temp_max) + int(temp_min)) / 2 + 0.5)
            weekday = date.strftime("%w")
            month_day = '2000' + '-' + str(date.month) + '-' + str(date.day)
            month_day = pd.to_datetime(month_day)
            if month_day >= pd.to_datetime('2000-3-21') and month_day <= pd.to_datetime('2000-6-21'):
                season = 1
            if month_day >= pd.to_datetime('2000-6-22') and month_day <= pd.to_datetime('2000-9-22'):
                season = 2
            if month_day >= pd.to_datetime('2000-9-23') and month_day <= pd.to_datetime('2000-12-21'):
                season = 3
            if month_day >= pd.to_datetime('2000-12-22') and month_day <= pd.to_datetime('2000-12-31'):
                season = 4
            if month_day >= pd.to_datetime('2000-1-1') and month_day <= pd.to_datetime('2000-3-20'):
                season = 4
            df_value = pd.read_csv('E:\\shareBike\\static\\value.csv')
            for i in range(0, len(df_value['weather'])):
                if weather == df_value['weather'][i]:
                    weather = df_value['value'][i]
            trlist.append(date)
            trlist.append(season)
            trlist.append(weekday)
            trlist.append(temp_avg)
            trlist.append(weather)

    return trlist


def randomForestRegressor_have(influence):
    year = influence[0]
    month = influence[1]
    day = influence[2]
    weekday = influence[3]
    season = influence[4]
    temp = influence[5]
    weather = influence[6]
    dew_point = influence[7]
    humidity = influence[8]
    sea_level_pressure_in = influence[9]
    visibility_miles = influence[10]
    wind_speed = influence[11]
    precipitation_in = influence[12]
    influence_value = [year, month, day, weekday, season, temp, weather,
                       dew_point, humidity, sea_level_pressure_in,
                       visibility_miles, wind_speed, precipitation_in]
    influence_name = ['year', 'month', 'day', 'weekday', 'season', 'temp', 'weather',
                      'dew_point', 'humidity', 'sea_level_pressure_in',
                      'visibility_miles', 'wind_speed', 'precipitation_in']
    test_data = pd.DataFrame(columns=('Date', 'year', 'month', 'day', 'weekday', 'season', 'temp', 'weather'))
    test_data['Date'] = [str(year) + '/' + str(month) + '/' + str(day)]
    for i in range(0, len(influence_name)):
        test_data[influence_name[i]] = [influence_value[i]]
    data_train = pd.read_csv('E:\\shareBike\\static\\data_train.csv')
    df_value = pd.read_csv('E:\\shareBike\\static\\value.csv')
    for i in range(0, len(df_value['weather'])):
        for j in range(0, len(data_train['Date'])):
            if data_train['weather'][j] == '晴':
                data_train['weather'][j] == 1
            if data_train['weather'][j] == df_value['weather'][i]:
                data_train['weather'][j] = df_value['value'][i]
    bike_count = data_train['count']
    yLabels_log = np.log(bike_count)
    data_train['Date'] = pd.to_datetime(data_train['Date'])
    data_train['year'] = data_train['Date'].dt.year
    data_train['month'] = data_train['Date'].dt.month
    data_train['day'] = data_train['Date'].dt.day
    data_train['weekday'] = data_train['Date'].dt.dayofweek
    Bike_data = pd.concat([data_train, test_data], ignore_index=True)
    dummies_year = pd.get_dummies(Bike_data['year'], prefix='year')
    dummies_month = pd.get_dummies(Bike_data['month'], prefix='month')
    dummies_day = pd.get_dummies(Bike_data['day'], prefix='day')
    dummies_weather = pd.get_dummies(Bike_data['weather'], prefix='weather')
    dummies_weekday = pd.get_dummies(Bike_data['weekday'], prefix='weekday')
    dummies_season = pd.get_dummies(Bike_data['season'], prefix='season')
    Bike_data = pd.concat(
        [Bike_data, dummies_year, dummies_month, dummies_day, dummies_weather, dummies_weekday, dummies_season],
        axis=1)
    dataTrain = Bike_data[pd.notnull(Bike_data['count'])]
    dataTest = Bike_data[~pd.notnull(Bike_data['count'])].sort_values(by=['Date'])
    drop_feature = ['year', 'month', 'day', 'weather', 'weekday', 'season',
                    'count', 'Date']
    dataTrain = dataTrain.drop(drop_feature, axis=1)
    dataTest = dataTest.drop(drop_feature, axis=1)
    rfModel = RandomForestRegressor(n_estimators=1000, random_state=42)
    rfModel.fit(dataTrain, yLabels_log)
    # preds = rfModel.predict(X=dataTrain)
    predsTest = rfModel.predict(X=dataTest)
    count = [max(0, x) for x in np.exp(predsTest)][0]
    int_count = int(count + 0.5)
    return int_count


def randomForestRegressor_nohave(influence):
    year = influence[0]
    month = influence[1]
    day = influence[2]
    weekday = influence[3]
    season = influence[4]
    temp = influence[5]
    weather = influence[6]
    influence_value = [year, month, day, weekday, season, temp, weather]
    influence_name = ['year', 'month', 'day', 'weekday', 'season', 'temp', 'weather']
    test_data = pd.DataFrame(columns=('Date', 'year', 'month', 'day', 'weekday', 'season', 'temp', 'weather'))
    test_data['Date'] = [str(year) + '/' + str(month) + '/' + str(day)]
    for i in range(0, len(influence_name)):
        test_data[influence_name[i]] = [influence_value[i]]
    data_train = pd.read_csv('E:\\shareBike\\static\\data_train.csv')
    df_value = pd.read_csv('E:\\shareBike\\static\\value.csv')
    for i in range(0, len(df_value['weather'])):
        for j in range(0, len(data_train['Date'])):
            if data_train['weather'][j] == '晴':
                data_train['weather'][j] == 1
            if data_train['weather'][j] == df_value['weather'][i]:
                data_train['weather'][j] = df_value['value'][i]
    bike_count = data_train['count']
    yLabels_log = np.log(bike_count)
    data_train['Date'] = pd.to_datetime(data_train['Date'])
    data_train['year'] = data_train['Date'].dt.year
    data_train['month'] = data_train['Date'].dt.month
    data_train['day'] = data_train['Date'].dt.day
    data_train['weekday'] = data_train['Date'].dt.dayofweek
    Bike_data = pd.concat([data_train, test_data], ignore_index=True)
    dummies_year = pd.get_dummies(Bike_data['year'], prefix='year')
    dummies_month = pd.get_dummies(Bike_data['month'], prefix='month')
    dummies_day = pd.get_dummies(Bike_data['day'], prefix='day')
    dummies_weather = pd.get_dummies(Bike_data['weather'], prefix='weather')
    dummies_weekday = pd.get_dummies(Bike_data['weekday'], prefix='weekday')
    dummies_season = pd.get_dummies(Bike_data['season'], prefix='season')
    Bike_data = pd.concat(
        [Bike_data, dummies_year, dummies_month, dummies_day, dummies_weather, dummies_weekday, dummies_season],
        axis=1)
    dataTrain = Bike_data[pd.notnull(Bike_data['count'])]
    dataTest = Bike_data[~pd.notnull(Bike_data['count'])].sort_values(by=['Date'])
    drop_feature = ['year', 'month', 'day', 'weather', 'weekday', 'season',
                    'count', 'Date', 'dew_point', 'humidity', 'sea_level_pressure_in',
                    'visibility_miles', 'wind_speed', 'precipitation_in']
    dataTrain = dataTrain.drop(drop_feature, axis=1)
    dataTest = dataTest.drop(drop_feature, axis=1)
    rfModel = RandomForestRegressor(n_estimators=1000, random_state=42)
    rfModel.fit(dataTrain, yLabels_log)
    # preds = rfModel.predict(X=dataTrain)
    predsTest = rfModel.predict(X=dataTest)
    count = [max(0, x) for x in np.exp(predsTest)][0]
    int_count = int(count + 0.5)
    return int_count

def time_line_predict():
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdate
    import pylab as mpl  # 导入中文字体，避免显示乱码
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设置为黑体字
    # 需要用到read_csv方法中的parse_dates参数和date_parser参数
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d')
    data = pd.read_csv('E:\\shareBike\\static\\predictions.csv', encoding='utf-8', parse_dates=['datetime'], date_parser=dateparse)
    # 数据透视表，需要对受理日期进行聚合，并对‘区局’列计数，计数使用的函数是aggfunc='count'
    table = pd.pivot_table(data, index=['datetime'], values=['count'], aggfunc='count')
    table.head(20)  # 看一下table的前20行数据是否正常

    # 生成figure对象
    fig = plt.figure(figsize=(15, 9))
    # 生成axis对象
    ax = fig.add_subplot(111)  # 本案例的figure中只包含一个图表
    # 设置x轴为时间格式，这句非常重要，否则x轴显示的将是类似于‘736268’这样的转码后的数字格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    # 设置x轴坐标值和标签旋转45°的显示方式
    plt.xticks(pd.date_range(table.index[0], table.index[-1], freq='M'), rotation=45)
    # x轴为table.index，也就是‘受理日期’，y轴为数量，颜色设置为红色
    ax.plot(table.index, data['count'], color='r', label='实际人数')
    ax.plot(table.index, data['pred_count'], color='b', label='预测人数')
    plt.xlabel("时间")
    plt.ylabel("人数", fontproperties="SimSun")  # 步骤一    （宋体）
    plt.title("预测量与实际量")
    plt.legend()
    plt.savefig('E:\\shareBike\\static\\time_predict.png')

def predict_bike(request):
    userName = request.COOKIES.get('userName', '')
    if request.method == "POST":
        try:
            year = request.POST['year']
            month = request.POST['month']
            day = request.POST['day']
            date = str(year) + '-' + str(month) + '-' + str(day)
            date_print = str(year) + '-' + str(month) + '-' + str(day)
            date = pd.to_datetime(date)
            weekday = date.strftime("%w")
            if (date >= pd.to_datetime('2014/11/11') and date <= pd.to_datetime('2015/10/12')):
                df = pd.read_csv('E:\\shareBike\\static\\data_train.csv')
                df['Date'] = pd.to_datetime(df['Date'])
                for i in range(0, len(df['Date'])):
                    if date == df['Date'][i]:
                        temp = df['temp'][i]
                        weather = df['weather'][i]
                        season = df['season'][i]
                        dew_point = df['dew_point'][i]
                        humidity = df['humidity'][i]
                        sea_level_pressure_in = df['sea_level_pressure_in'][i]
                        visibility_miles = df['visibility_miles'][i]
                        wind_speed = df['wind_speed'][i]
                        precipitation_in = df['precipitation_in'][i]
                        influence = [year, month, day, weekday, season, temp, weather,
                                     dew_point, humidity, sea_level_pressure_in,
                                     visibility_miles, wind_speed, precipitation_in]
                        count_true = df['count'][i]
                count = randomForestRegressor_have(influence)
                season_list = ['春天(Spring)', '夏天(Summer)', '秋天(autumn)', '冬天(winner)']
                season_value = [1, 2, 3, 4]
                season_print = ''
                for i in range(0, 4):
                    if season == season_value[i]:
                        season_print = season_list[i]
                weekday_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期鈤']
                weekday_value = [1, 2, 3, 4, 5, 6, 7]
                weekday_print = ''
                for i in range(0, 7):
                    if str(weekday) == str(weekday_value[i]):
                        weekday_print = weekday_list[i]
                temp_print = int((int(temp) - 32) / 1.8 + 0.5)
                request.session["date"] = date_print
                request.session["season"] = season_print
                request.session["weekday"] = weekday_print
                request.session["weather"] = weather
                request.session["temp"] = str(temp_print)
                request.session["count"] = str(count)
                request.session["count_true"] = str(count_true)
                year = range(2015, 2100)
                month = range(1, 13)
                day = range(1, 32)
                return render(request, 'predict_bike.html',
                              {"userName": userName, "year": year, "month": month, "day": day, "method":"post"})

            else:
                weather_list = get_tag(year, month, day)
                print(weather_list)
                season = weather_list[1]
                weekday = weather_list[2]
                temp_print = weather_list[3]
                weather = weather_list[4]
                temp = int(int(temp_print) * 1.8 + 32 + 0.5)
                influence = [year, month, day, weekday, season, temp, weather]
                count = randomForestRegressor_nohave(influence)
                date = str(year) + '-' + str(month) + '-' + str(day)
                df_value = pd.read_csv('E:\\shareBike\\static\\value.csv')
                for i in range(0, len(df_value['weather'])):
                    if weather == df_value['value'][i]:
                        weather_name = df_value['weather'][i]
                season_list = ['春天(Spring)', '夏天(Summer)', '秋天(autumn)', '冬天(winner)']
                season_value = [1, 2, 3, 4]
                season_print = ''
                for i in range(0, 4):
                    if season == season_value[i]:
                        season_print = season_list[i]
                weekday_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期鈤']
                weekday_value = [1, 2, 3, 4, 5, 6, 7]
                weeday_print = ''
                for i in range(0, 7):
                    if str(weekday) == str(weekday_value[i]):
                        weekday_print = weekday_list[i]
                temp_print = int((int(temp) - 32) / 1.8 + 0.5)
                request.session["date"] = date
                request.session["season"] = season_print
                request.session["weekday"] = weekday_print
                request.session["weather"] = weather_name
                request.session["temp"] = str(temp_print)
                request.session["count"] = str(count)
                request.session["count_true"] = ''

                year = range(2015, 2100)
                month = range(1, 13)
                day = range(1, 32)
                return render(request, 'predict_bike.html',
                              {"userName": userName, "year": year, "month": month, "day": day, "method": "post"})
        except:
            year = range(2015, 2100)
            month = range(1, 13)
            day = range(1, 32)
            return render(request, 'predict_bike.html', {"userName": userName, "year": year, "month": month, "day": day, "method":"get"})
    else:
        year = range(2015, 2100)
        month = range(1, 13)
        day = range(1, 32)
        time_line_predict()
        return render(request, 'predict_bike.html', {"userName": userName, "year": year, "month": month, "day": day, "method":"get"})

def result(request):
    userName = request.COOKIES.get('userName', '')
    date = request.session.get('date', '')
    season = request.session.get('season', '')
    weekday = request.session.get('weekday', '')
    weather = request.session.get('weather', '')
    temp = request.session.get('temp', '')
    count = request.session.get('count', '')
    count_true = request.session.get('count_true', '')
    print("date")
    return render(request, 'result.html',
                  {"userName": userName, "date": date, "season": season, "weekday": weekday,
                   "weather": weather, "temp": temp, "count": count, "count_true": count_true})

def pred_count(request):
    return render(request, 'self_chart/pred_count.html')

def my(request):
    userName = request.COOKIES.get('userName', '')
    if request.method == "POST":
        name = request.POST['name']
        print(name)
        file_path = db.selece_file(name)[0][0]
        print(db.selece_file(name))
        print(file_path)
        data_set = pd.read_csv(file_path)
        data_columns = data_set.columns.tolist()
        data = data_set.values[:, :]
        print(data_set)
        test_data = [data_columns]
        for line in data:
            ls = []
            for j in line:
                ls.append(j)
            test_data.append(ls)
        print(test_data)
        return render(request, 'open_file.html', {"test_data": test_data})
    else:
        userName = request.COOKIES.get('userName', '')
        user_data = db.select_userName(userName)
        password = user_data[0][1]
        email = user_data[0][2]
        company = user_data[0][3]
        data = {}
        for i in range(0, len(db.select_file_all(userName))):
            data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][3]
        return render(request, 'my_information.html',
                      {"data": data, "userName": userName, "password": password, "email": email, "company": company})


def set_up(request):
    userName = request.COOKIES.get('userName', '')
    password = request.POST['password']
    email = request.POST['email']
    company = request.POST['company']
    db.mysql_change(userName, password, email, company)
    user_data = db.select_userName(userName)
    password = user_data[0][1]
    email = user_data[0][2]
    company = user_data[0][3]
    data = {}
    for i in range(0, len(db.select_file_all(userName))):
        data[db.select_file_all(userName)[i][1]] = db.select_file_all(userName)[i][3]
    return render(request, 'my_information.html',
                  {"data": data, "userName": userName, "password": password, "email": email, "company": company})
