"""shareBike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path
from bike import views
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^$', views.index),
    path('index', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('login_form', views.post_Login),
    path('register', views.register),
    path('register_form', views.post_Register),
    path('dataset', views.dataset),
    path('upload', views.upload),
    path('visualisation', views.visualisation),
    path('history_data_analyse', views.history_data_analyse),
    # 骑行路线
    path('if_bike_route', views.bike_route),
    path('route_0510', views.route_0510),
    path('route_0511', views.route_0511),
    path('route_0512', views.route_0512),
    path('route_0513', views.route_0513),
    path('route_0514', views.route_0514),

    # 热点区域
    path('if_heat_area', views.heat_area),
    path('heat_0510', views.heat_0510),
    path('heat_0511', views.heat_0511),
    path('heat_0512', views.heat_0512),
    path('heat_0512', views.heat_0512),
    path('heat_0513', views.heat_0513),
    path('heat_0514', views.heat_0514),
    # 影响因素
    path('if_weather', views.weather),
    path('if_holiday', views.holiday),
    path('if_month', views.month),
    path('if_season', views.season),
    path('if_temperature', views.temperature),
    # path('dew_point', views.v_dew_point),
    # path('if_dew_point', views.dew_point),
    path('if_humidity', views.humidity),
    # path('pressure', views.v_pressure),
    # path('if_pressure', views.pressure),
    path('if_visibility_miles', views.visibility_miles),
    path('if_wind_speed', views.wind_speed),
    path('if_precipitation', views.precipitation),
    path('if_temp_speed', views.temp_speed),
    # 用户画像
    path('if_gender', views.gender),
    path('if_age', views.age),
    path('if_is_register', views.is_register),
    path('self_visualisation', views.self_visualisation),
    path('if_self_visualisation', views.self_visualisation),
    #可视化
    # path('line', views.self_lineChart),
    # path('boxplot', views.self_boxPlot),


    path('influence', views.influence),
    path('user', views.user),


    path('table', views.table),
    #influence
    path('route', views.self_route),
    path('heat', views.self_heat),
    path('season', views.self_rose_season),
    path('month', views.self_month),
    path('holiday', views.self_holiday),
    path('visibility', views.self_visibility),
    path('temp_speed', views.self_temp_speed),

    #user
    path('gender', views.self_gender),
    path('age', views.self_age),
    path('is_register', views.self_is_register),

    path('predict_bike', views.predict_bike),

    #my
    path('my', views.my),
    path('set_up', views.set_up),

    path('result', views.result),
    path('pred', views.pred_count),

]
