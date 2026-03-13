%% IC价格三维走势分析工具
% 作者：AI助手
% 日期：2026-03-13
% 功能：使用plot3函数绘制IC价格的三维走势图
%       包含时间轴缩放、支撑阻力位、多IC颜色区分功能

clear; close all; clc;

%% ===================== 参数设置区 =====================
% 用户可以在这里修改所有参数

% 1. 基本参数设置
ic_names = {'STM32F103', 'ATmega328P', 'ESP32', 'Raspberry Pi Pico', 'NRF52840'}; % IC型号名称
ic_colors = lines(length(ic_names)); % 使用MATLAB内置颜色
% 或者自定义颜色：
% ic_colors = [0.2 0.4 0.8; 0.8 0.2 0.2; 0.2 0.8 0.4; 0.8 0.6 0.2; 0.6 0.2 0.8];

% 2. 时间轴设置
total_days = 365; % 总天数
time_scale = 'month'; % 时间尺度: 'day', 'week', 'month'
start_date = datetime(2026,1,1); % 起始日期

% 3. 价格参数设置
base_prices = [8.5, 3.2, 12.8, 6.5, 15.2]; % 基准价格(元)
price_volatility = 0.15; % 价格波动率
support_levels = [7.0, 2.5, 10.0, 5.0, 12.0]; % 支撑位价格
resistance_levels = [10.0, 4.0, 15.0, 8.0, 18.0]; % 阻力位价格

% 4. 热度参数设置
base_heat = [50000, 30000, 80000, 40000, 60000]; % 基准月搜索量
heat_volatility = 0.2; % 热度波动率

% 5. 图形参数设置
enable_grid = true; % 是否显示网格
show_support_resistance = true; % 是否显示支撑阻力位
line_width = 2.5; % 线条宽度
marker_size = 30; % 数据点标记大小
font_size = 14; % 字体大小

%% ===================== 数据生成模块 =====================
fprintf('正在生成模拟数据...\n');

% 生成时间序列
T = days(1:total_days); % 天数序列
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

fprintf('数据生成完成！共生成 %d 个IC型号，时间跨度 %d 天\n', num_ics, total_days);

%% ===================== 时间轴处理模块 =====================
fprintf('正在处理时间轴...\n');

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

fprintf('时间尺度: %s，显示点数: %d\n', time_scale, length(display_points));

%% ===================== 图形绘制模块 =====================
fprintf('正在创建三维图形...\n');

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
    X = display_points / time_factor; % 时间轴
    Y = heat_data(i, display_points) / 1000; % 热度（千次搜索）
    Z = price_data(i, display_points); % 价格
    
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
    fprintf('正在绘制支撑阻力位...\n');
    
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
            'DisplayName', sprintf('%s-支撑位', ic_names{i}));
        
        % 阻力位（半透明红色）
        zs_resistance = ones(size(xs)) * resistance_levels(i);
        surf(xs, ys, zs_resistance, ...
            'FaceColor', [0.8 0 0], ...
            'FaceAlpha', 0.1, ...
            'EdgeColor', 'none', ...
            'DisplayName', sprintf('%s-阻力位', ic_names{i}));
    end
end

%% ===================== 图形美化模块 =====================
fprintf('正在美化图形...\n');

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
view(ax, 45, 30); % 默认视角

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

% 添加颜色栏说明（如果需要）
colormap(ax, ic_colors);

% 添加文字说明
text_str = sprintf('数据时间: %s 至 %s\nIC数量: %d', ...
    datestr(start_date, 'yyyy-mm-dd'), ...
    datestr(start_date + total_days, 'yyyy-mm-dd'), ...
    num_ics);
annotation('textbox', [0.02, 0.02, 0.2, 0.05], ...
    'String', text_str, ...
    'FitBoxToText', 'on', ...
    'BackgroundColor', [1 1 1 0.8], ...
    'FontSize', font_size-4);

hold(ax, 'off');

%% ===================== 交互功能模块 =====================
fprintf('正在添加交互功能...\n');

% 创建交互式按钮面板
uipanel('Position', [0.7, 0.02, 0.28, 0.15], ...
    'Title', '交互控制', ...
    'BackgroundColor', [0.95 0.95 0.95], ...
    'FontSize', font_size-2);

% 添加时间尺度切换按钮
time_buttons = {'按日显示', '按周显示', '按月显示'};
for b = 1:3
    uicontrol('Style', 'pushbutton', ...
        'Position', [0.71+0.09*(b-1), 0.03, 0.08, 0.05], ...
        'String', time_buttons{b}, ...
        'FontSize', font_size-4, ...
        'Callback', @(src,event) switchTimeScale(time_buttons{b}));
end

% 添加显示/隐藏支撑阻力位按钮
uicontrol('Style', 'pushbutton', ...
    'Position', [0.71, 0.09, 0.25, 0.04], ...
    'String', '切换支撑/阻力位显示', ...
    'FontSize', font_size-4, ...
    'Callback', @toggleSupportResistance);

% 添加视角重置按钮
uicontrol('Style', 'pushbutton', ...
    'Position', [0.71, 0.14, 0.25, 0.04], ...
    'String', '重置视角 (45°, 30°)', ...
    'FontSize', font_size-4, ...
    'Callback', @resetView);

%% ===================== 信息输出模块 =====================
fprintf('\n========== 分析完成 ==========\n');
fprintf('图形已成功生成！\n\n');

% 显示当前设置
fprintf('当前设置:\n');
fprintf('  - IC型号: %s\n', strjoin(ic_names, ', '));
fprintf('  - 时间尺度: %s\n', time_scale);
fprintf('  - 总天数: %d\n', total_days);
fprintf('  - 起始日期: %s\n', datestr(start_date, 'yyyy-mm-dd'));

% 显示最新价格和热度
fprintf('\n最新数据 (最后一天):\n');
fprintf('型号               价格(元)   月搜索量(千次)\n');
fprintf('---------------------------------------------\n');
for i = 1:num_ics
    fprintf('%-15s   %6.2f        %8.1f\n', ...
        ic_names{i}, ...
        price_data(i, end), ...
        heat_data(i, end)/1000);
end

fprintf('\n支撑位/阻力位:\n');
fprintf('型号               支撑位     阻力位\n');
fprintf('-------------------------------------\n');
for i = 1:num_ics
    fprintf('%-15s   %6.2f     %6.2f\n', ...
        ic_names{i}, ...
        support_levels(i), ...
        resistance_levels(i));
end

fprintf('\n提示:\n');
fprintf('1. 您可以在"参数设置区"修改所有参数\n');
fprintf('2. 使用图形窗口上的交互按钮可以切换显示模式\n');
fprintf('3. 可以直接拖动图形旋转视角\n');
fprintf('4. 将脚本中的模拟数据替换为您的真实数据即可使用\n');

%% ===================== 回调函数定义 =====================
% 这里定义了交互按钮的回调函数

function switchTimeScale(scale_name)
    % 切换时间尺度
    global time_scale;
    
    switch scale_name
        case '按日显示'
            time_scale = 'day';
        case '按周显示'
            time_scale = 'week';
        case '按月显示'
            time_scale = 'month';
    end
    
    fprintf('切换到时间尺度: %s\n', time_scale);
    
    % 重新运行绘图（简化示例）
    % 实际应用中可能需要重构代码以动态更新
    fprintf('请重新运行脚本以应用新的时间尺度\n');
end

function toggleSupportResistance()
    % 切换支撑/阻力位显示
    global show_support_resistance;
    show_support_resistance = ~show_support_resistance;
    
    if show_support_resistance
        fprintf('已启用支撑/阻力位显示\n');
    else
        fprintf('已禁用支撑/阻力位显示\n');
    end
    
    fprintf('请重新运行脚本以应用显示设置\n');
end

function resetView()
    % 重置视角
    view(45, 30);
    fprintf('视角已重置为 (45°, 30°)\n');
end