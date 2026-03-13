#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IC价格三维走势分析工具 - MATLAB代码生成器
功能：生成可直接运行的MATLAB脚本，绘制IC价格的三维走势图
"""

import os
import json
from datetime import datetime

def generate_matlab_code(config):
    """
    根据配置生成MATLAB代码
    
    Args:
        config (dict): 配置参数
        
    Returns:
        str: MATLAB代码
    """
    
    # 解包配置参数
    time_scale = config.get('time_scale', 'week')
    total_days = config.get('total_days', 365)
    start_date = config.get('start_date', '2026-01-01')
    enable_grid = config.get('enable_grid', True)
    show_support_resistance = config.get('show_support_resistance', True)
    line_width = config.get('line_width', 2.5)
    
    # IC配置
    ics = config.get('ics', [])
    num_ics = len(ics)
    
    # 生成颜色矩阵代码
    color_lines = []
    for ic in ics:
        # 将HEX颜色转换为MATLAB格式
        hex_color = ic['color'].replace('#', '')
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        color_lines.append(f'[{r:.2f} {g:.2f} {b:.2f}]')
    color_code = '; '.join(color_lines)
    
    # 生成名称数组
    name_code = ', '.join([f"'{ic['name']}'" for ic in ics])
    
    # 生成价格和热度数组
    price_code = ', '.join([f"{ic['base_price']:.1f}" for ic in ics])
    support_code = ', '.join([f"{ic['support']:.1f}" for ic in ics])
    resistance_code = ', '.join([f"{ic['resistance']:.1f}" for ic in ics])
    heat_code = ', '.join([str(round(ic['base_heat'])) for ic in ics])
    
    # 获取当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成MATLAB代码
    matlab_code = f"""%% IC价格三维走势分析工具
% 作者：代码生成器
% 生成时间：{current_time}
% 功能：使用plot3函数绘制IC价格的三维走势图
%       包含时间轴缩放、支撑阻力位、多IC颜色区分功能

clear; close all; clc;

%% ===================== 参数设置区 =====================
% 用户可以在这里修改所有参数

% 1. IC型号配置
ic_names = {{{name_code}}};  % IC型号名称
ic_colors = [{color_code}];  % 自定义颜色矩阵

% 2. 时间轴设置
total_days = {total_days};  % 总天数
time_scale = '{time_scale}';  % 时间尺度: 'day', 'week', 'month'
start_date = datetime('{start_date}');  % 起始日期

% 3. 价格参数设置
base_prices = [{price_code}];  % 基准价格(元)
price_volatility = 0.15;  % 价格波动率
support_levels = [{support_code}];  % 支撑位价格
resistance_levels = [{resistance_code}];  % 阻力位价格

% 4. 热度参数设置
base_heat = [{heat_code}];  % 基准月搜索量
heat_volatility = 0.2;  % 热度波动率

% 5. 图形参数设置
enable_grid = {str(enable_grid).lower()};  % 是否显示网格
show_support_resistance = {str(show_support_resistance).lower()};  % 是否显示支撑阻力位
line_width = {line_width};  % 线条宽度
marker_size = 30;  % 数据点标记大小
font_size = 14;  % 字体大小

%% ===================== 数据生成模块 =====================
fprintf('正在生成模拟数据...\\n');

% 生成时间序列
T = days(1:total_days);  % 天数序列
date_sequence = start_date + T;

% 初始化数据存储
num_ics = length(ic_names);
price_data = zeros(num_ics, total_days);
heat_data = zeros(num_ics, total_days);

% 为每个IC生成价格和热度数据
for i = 1:num_ics
    % 生成基础价格趋势（随机游走）
    price_walk = cumsum(randn(1, total_days) * price_volatility);
    price_data(i, :) = base_prices(i) * exp(price_walk);
    
    % 生成季节性热度波动
    seasonal_factor = 0.3 * sin(2*pi*(1:total_days)/365) + ...
                      0.2 * sin(4*pi*(1:total_days)/365) + ...
                      0.1 * sin(6*pi*(1:total_days)/365);
    
    % 生成随机热度波动
    heat_walk = cumsum(randn(1, total_days) * heat_volatility);
    heat_data(i, :) = base_heat(i) * exp(0.1 * seasonal_factor + 0.05 * heat_walk);
end

fprintf('数据生成完成！共生成 %d 个IC型号，时间跨度 %d 天\\n', num_ics, total_days);

%% ===================== 时间轴处理模块 =====================
fprintf('正在处理时间轴...\\n');

% 根据选择的时间尺度调整数据点
switch time_scale
    case 'day'
        % 按天显示，使用全部数据点
        display_points = 1:total_days;
        x_label_text = '天数';
        time_factor = 1;
        
    case 'week'
        % 按周显示，每周取一个数据点（最后一天）
        weeks = ceil(total_days/7);
        display_points = zeros(1, weeks);
        for w = 1:weeks
            start_day = (w-1)*7 + 1;
            end_day = min(w*7, total_days);
            display_points(w) = end_day;
        end
        x_label_text = '周数';
        time_factor = 7;
        
    case 'month'
        % 按月显示，每月取一个数据点（最后一天）
        months = ceil(total_days/30);
        display_points = zeros(1, months);
        for m = 1:months
            start_day = (m-1)*30 + 1;
            end_day = min(m*30, total_days);
            display_points(m) = end_day;
        end
        x_label_text = '月数';
        time_factor = 30;
        
    otherwise
        error('不支持的时间尺度，请选择: day, week, month');
end

fprintf('时间尺度: %s，显示点数: %d\\n', time_scale, length(display_points));

%% ===================== 图形绘制模块 =====================
fprintf('正在创建三维图形...\\n');

% 创建图形窗口
figure('Name', 'IC价格三维走势分析', 'Position', [100, 100, 1400, 800], ...
       'Color', [0.96 0.96 0.96], 'NumberTitle', 'off');

% 创建三维坐标系
ax = axes('Parent', gcf);
hold(ax, 'on');
grid(ax, 'on');

% 绘制每个IC的三维走势线
legend_handles = [];
for i = 1:num_ics
    % 提取显示点的数据
    X = display_points / time_factor;  % 时间轴
    Y = heat_data(i, display_points) / 1000;  % 热度（千次搜索）
    Z = price_data(i, display_points);  % 价格
    
    % 绘制三维曲线
    h = plot3(X, Y, Z, ...
        'LineWidth', line_width, ...
        'Color', ic_colors(i, :), ...
        'Marker', 'o', ...
        'MarkerSize', 6, ...
        'MarkerFaceColor', ic_colors(i, :));
    
    % 添加数据点标记
    scatter3(X, Y, Z, marker_size, ic_colors(i, :), 'filled', ...
        'MarkerEdgeColor', 'k', 'LineWidth', 1);
    
    legend_handles = [legend_handles, h];
end

%% ===================== 支撑阻力位绘制模块 =====================
if show_support_resistance
    fprintf('正在绘制支撑阻力位...\\n');
    
    % 获取当前坐标轴范围
    x_lim = xlim;
    y_lim = ylim;
    
    % 为每个IC绘制支撑位和阻力位
    for i = 1:num_ics
        % 支撑位（半透明绿色）
        [xs, ys] = meshgrid(x_lim, y_lim);
        zs_support = ones(size(xs)) * support_levels(i);
        surf(xs, ys, zs_support, ...
            'FaceColor', [0 0.8 0], ...
            'FaceAlpha', 0.1, ...
            'EdgeColor', 'none', ...
            'DisplayName', sprintf('%s-支撑位', ic_names{{i}}));
        
        % 阻力位（半透明红色）
        zs_resistance = ones(size(xs)) * resistance_levels(i);
        surf(xs, ys, zs_resistance, ...
            'FaceColor', [0.8 0 0], ...
            'FaceAlpha', 0.1, ...
            'EdgeColor', 'none', ...
            'DisplayName', sprintf('%s-阻力位', ic_names{{i}}));
    end
end

%% ===================== 图形美化模块 =====================
fprintf('正在美化图形...\\n');

% 设置坐标轴标签和标题
xlabel(ax, x_label_text, 'FontSize', font_size, 'FontWeight', 'bold');
ylabel(ax, '月搜索量 (千次)', 'FontSize', font_size, 'FontWeight', 'bold');
zlabel(ax, '价格 (元)', 'FontSize', font_size, 'FontWeight', 'bold');
title(ax, sprintf('IC价格三维走势分析 - 时间尺度: %s', upper(time_scale)), ...
    'FontSize', font_size+2, 'FontWeight', 'bold');

% 设置图例
legend(ax, legend_handles, ic_names, ...
    'Location', 'best', ...
    'FontSize', font_size-2, ...
    'Box', 'off');

% 设置视角
view(ax, 45, 30);  % 默认视角

% 添加网格
if enable_grid
    grid(ax, 'on');
    grid(ax, 'minor');
else
    grid(ax, 'off');
end

% 设置图形颜色和透明度
ax.GridColor = [0.3 0.3 0.3];
ax.GridAlpha = 0.3;
ax.Box = 'on';

% 添加颜色栏说明
colormap(ax, ic_colors);

% 添加文字说明
text_str = sprintf('数据时间: %s 至 %s\\nIC数量: %d', ...
    datestr(start_date, 'yyyy-mm-dd'), ...
    datestr(start_date + total_days, 'yyyy-mm-dd'), ...
    num_ics);
annotation('textbox', [0.02, 0.02, 0.2, 0.05], ...
    'String', text_str, ...
    'FitBoxToText', 'on', ...
    'BackgroundColor', [1 1 1 0.8], ...
    'FontSize', font_size-4);

hold(ax, 'off');

%% ===================== 信息输出模块 =====================
fprintf('\\n========== 分析完成 ==========\\n');
fprintf('图形已成功生成！\\n\\n');

% 显示当前设置
fprintf('当前设置:\\n');
fprintf('  - IC型号: %s\\n', strjoin(ic_names, ', '));
fprintf('  - 时间尺度: %s\\n', time_scale);
fprintf('  - 总天数: %d\\n', total_days);
fprintf('  - 起始日期: %s\\n', datestr(start_date, 'yyyy-mm-dd'));

% 显示最新价格和热度
fprintf('\\n最新数据 (最后一天):\\n');
fprintf('型号               价格(元)   月搜索量(千次)\\n');
fprintf('---------------------------------------------\\n');
for i = 1:num_ics
    fprintf('%-15s   %6.2f        %8.1f\\n', ...
        ic_names{{i}}, ...
        price_data(i, end), ...
        heat_data(i, end)/1000);
end

% 显示支撑位/阻力位
fprintf('\\n支撑位/阻力位:\\n');
fprintf('型号               支撑位     阻力位\\n');
fprintf('-------------------------------------\\n');
for i = 1:num_ics
    fprintf('%-15s   %6.2f     %6.2f\\n', ...
        ic_names{{i}}, ...
        support_levels(i), ...
        resistance_levels(i));
end

fprintf('\\n提示:\\n');
fprintf('1. 您可以在"参数设置区"修改所有参数\\n');
fprintf('2. 将脚本中的模拟数据替换为您的真实数据即可使用\\n');
fprintf('3. 直接拖动图形可以旋转视角\\n');
fprintf('4. 使用图形工具栏可以保存图像或调整视图\\n');
"""
    
    return matlab_code

def main():
    """主函数"""
    
    print("=" * 60)
    print("IC价格三维走势分析工具 - MATLAB代码生成器")
    print("=" * 60)
    print()
    
    # 默认配置
    default_config = {
        "time_scale": "week",
        "total_days": 365,
        "start_date": "2026-01-01",
        "enable_grid": True,
        "show_support_resistance": True,
        "line_width": 2.5,
        "ics": [
            {
                "name": "STM32F103",
                "color": "#3366CC",
                "base_price": 8.5,
                "support": 7.0,
                "resistance": 10.0,
                "base_heat": 50000
            },
            {
                "name": "ATmega328P",
                "color": "#DC3912",
                "base_price": 3.2,
                "support": 2.5,
                "resistance": 4.0,
                "base_heat": 30000
            },
            {
                "name": "ESP32",
                "color": "#FF9900",
                "base_price": 12.8,
                "support": 10.0,
                "resistance": 15.0,
                "base_heat": 80000
            }
        ]
    }
    
    print("当前默认配置:")
    print(f"  时间尺度: {default_config['time_scale']}")
    print(f"  总天数: {default_config['total_days']}")
    print(f"  起始日期: {default_config['start_date']}")
    print(f"  IC数量: {len(default_config['ics'])}")
    for i, ic in enumerate(default_config['ics'], 1):
        print(f"  IC{i}: {ic['name']} (基准价格: {ic['base_price']}元)")
    
    print()
    choice = input("是否使用默认配置? (y/n): ").strip().lower()
    
    if choice == 'n':
        print("\n请输入自定义配置:")
        
        # 获取基本配置
        default_config['time_scale'] = input("时间尺度 (day/week/month, 默认week): ").strip() or "week"
        default_config['total_days'] = int(input("总天数 (默认365): ") or 365
        default_config['start_date'] = input("起始日期 (默认2026-01-01): ").strip() or "2026-01-01"
        default_config['enable_grid'] = input("显示网格? (y/n, 默认y): ").strip().lower() != 'n'
        default_config['show_support_resistance'] = input("显示支撑阻力位? (y/n, 默认y): ").strip().lower() != 'n'
        default_config['line_width'] = float(input("线条宽度 (默认2.5): ") or 2.5)
        
        # 获取IC配置
        default_config['ics'] = []
        ic_count = int(input("IC数量 (默认3): ") or 3)
        
        for i in range(1, ic_count + 1):
            print(f"\n配置IC{i}:")
            ic = {
                "name": input(f"  型号名称 (默认IC_{i}): ").strip() or f"IC_{i}",
                "color": input(f"  颜色代码 (默认#{i:06x}): ").strip() or f"#{i:06x}",
                "base_price": float(input(f"  基准价格(元) (默认{10.0 * i:.1f}): ") or 10.0 * i),
                "support": float(input(f"  支撑位 (默认{8.0 * i:.1f}): ") or 8.0 * i),
                "resistance": float(input(f"  阻力位 (默认{12.0 * i:.1f}): ") or 12.0 * i),
                "base_heat": float(input(f"  基准月搜索量 (默认{50000 * i}): ") or 50000 * i)
            }
            default_config['ics'].append(ic)
    
    # 生成MATLAB代码
    print("\n正在生成MATLAB代码...")
    matlab_code = generate_matlab_code(default_config)
    
    # 保存到文件
    filename = "ic_3d_price_trend_generated.m"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(matlab_code)
    
    print(f"代码已保存到: {filename}")
    print(f"文件大小: {len(matlab_code)} 字符")
    
    # 显示统计信息
    print("\n统计信息:")
    print(f"  IC数量: {len(default_config['ics'])}")
    print(f"  时间跨度: {default_config['total_days']} 天")
    print(f"  时间尺度: {default_config['time_scale']}")
    print(f"  起始日期: {default_config['start_date']}")
    
    # 简要预览代码
    print("\n代码预览 (前10行):")
    lines = matlab_code.split('\n')[:10]
    for line in lines:
        print(f"  {line}")
    
    print("\n使用说明:")
    print("1. 将生成的 .m 文件复制到MATLAB工作目录")
    print("2. 在MATLAB命令窗口输入: ic_3d_price_trend_generated")
    print("3. 脚本将自动生成三维走势图")
    print("4. 您可以直接修改 .m 文件中的参数")
    
    # 提示其他选项
    print("\n其他选项:")
    print("1. 在线预览: 打开 ic_3d_preview.html 在浏览器中配置参数")
    print("2. 完整脚本: 查看 ic_3d_price_trend.m 获得更完整的功能")
    print("3. 测试运行: 如果您有MATLAB环境，可以直接运行生成的文件")

if __name__ == "__main__":
    main()