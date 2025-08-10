import json
import os
from datetime import datetime  
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(script_dir, 'usernamecache.json')
with open(cache_path, 'r', encoding='utf-8') as f:
    username_cache = json.load(f)
player_list = [(uuid, name) for uuid, name in username_cache.items()]
update_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十八方块研究所玩家数据统计</title>
    <link rel="stylesheet" href="style.css">
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        document.querySelectorAll('.index-item').forEach(item => {{
                            item.classList.remove('active');
                        }});
                        const uuid = entry.target.id.split('-')[1];
                        const activeItem = document.querySelector(`.index-item[href="#player-${{uuid}}"]`);
                        if (activeItem) activeItem.classList.add('active');
                    }});
                }});
            }}, {{ threshold: 0.5 }});

            document.querySelectorAll('.player-card').forEach(card => {{
                observer.observe(card);
            }});
        }});
    </script>
</head>
<body>
    <header>
        <h1>十八方块研究所玩家数据统计</h1>
        <p class="subtitle">数据更新时间：{update_time}</p> 
    </header>
    
    <div class="page-container">
        <div class="index-container">
            <div class="index-title">玩家索引</div>
            <div class="index-list">
"""
for uuid, name in player_list:
    html_content += f"""
                <a href="#player-{uuid}" class="index-item">{name}</a>
    """
html_content += """
            </div>
        </div>

        <div class="main-container">
            <h2 style="text-align: center; margin-bottom: 20px; color: #4facfe; font-size: 1.8rem;">
                玩家数据统计
            </h2>
            
            <div class="player-container">
"""
for uuid, name in player_list:
    player_card = f"""
            <div class="player-card" id="player-{uuid}">
                <div class="player-header">
                    <div class="player-avatar">
                    </div>
                    <div class="player-info">
                        <div class="player-name">{name}</div>
                        <div class="player-uuid">UUID: {uuid}</div>
                    </div>
                </div>
                <div class="dimensions-container stacked">
    """
    # ---------------------- 一周目数据处理 ----------------------
    week1_data = {}
    week1_file_path = os.path.join(script_dir, '一周目', f'{uuid}.json')
    if os.path.exists(week1_file_path):
        with open(week1_file_path, 'r', encoding='utf-8') as f:
            week1_data = json.load(f)

    custom_stats_1 = week1_data.get('stats', {}).get('minecraft:custom', {})
    killed_stats_1 = week1_data.get('stats', {}).get('minecraft:killed', {})
    kill_count_1 = sum(killed_stats_1.values()) if killed_stats_1 else '----'
    play_time_1 = custom_stats_1.get('minecraft:play_time')
    play_time_1 = f"{int(play_time_1 / 72000)}h" if play_time_1 else '----'
    death_count_1 = custom_stats_1.get('minecraft:deaths', '----')
    damage_dealt_1 = custom_stats_1.get('minecraft:damage_dealt', '----')
    damage_taken_1 = custom_stats_1.get('minecraft:damage_taken', '----')
    move_stats = [
        'minecraft:aviate_one_cm', 'minecraft:boat_one_cm', 'minecraft:climb_one_cm',
        'minecraft:crouch_one_cm', 'minecraft:fall_one_cm', 'minecraft:fly_one_cm'
    ]
    total_cm_1 = 0
    has_move_data = False
    for stat in move_stats:
        if stat in custom_stats_1 and isinstance(custom_stats_1[stat], int):
            total_cm_1 += custom_stats_1[stat]
            has_move_data = True
    move_distance_1 = f"{total_cm_1 / 100:.1f}m" if has_move_data else '----'
    player_card += f"""
                    <div class="dimension dimension-1 stacked-dimension">
                        <div class="dimension-title">一周目数据</div>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value-sm">{play_time_1}</div>
                                <div class="stat-label-sm">游戏时间</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{death_count_1}</div>
                                <div class="stat-label-sm">死亡次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{kill_count_1}</div>
                                <div class="stat-label-sm">击杀次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{move_distance_1}</div>
                                <div class="stat-label-sm">移动距离</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_dealt_1}</div>
                                <div class="stat-label-sm">造成伤害</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_taken_1}</div>
                                <div class="stat-label-sm">收到伤害</div>
                            </div>
                        </div>
                    </div>
    """
    week2_data = {}
    week2_file_path = os.path.join(script_dir, '二周目', f'{uuid}.json')
    if os.path.exists(week2_file_path):
        with open(week2_file_path, 'r', encoding='utf-8') as f:
            week2_data = json.load(f)
    custom_stats_2 = week2_data.get('stats', {}).get('minecraft:custom', {})
    killed_stats_2 = week2_data.get('stats', {}).get('minecraft:killed', {})
    kill_count_2 = sum(killed_stats_2.values()) if killed_stats_2 else '----'
    play_time_2 = custom_stats_2.get('minecraft:play_time')
    play_time_2 = f"{int(play_time_2 / 72000)}h" if play_time_2 else '----'
    death_count_2 = custom_stats_2.get('minecraft:deaths', '----')
    damage_dealt_2 = custom_stats_2.get('minecraft:damage_dealt', '----')
    damage_taken_2 = custom_stats_2.get('minecraft:damage_taken', '----')
    total_cm_2 = 0
    has_move_data_2 = False
    for stat in move_stats:
        if stat in custom_stats_2 and isinstance(custom_stats_2[stat], int):
            total_cm_2 += custom_stats_2[stat]
            has_move_data_2 = True
    move_distance_2 = f"{total_cm_2 / 100:.1f}m" if has_move_data_2 else '----'
    player_card += f"""
                    <div class="dimension dimension-2 stacked-dimension">
                        <div class="dimension-title">二周目数据</div>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value-sm">{play_time_2}</div>
                                <div class="stat-label-sm">游戏时间</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{death_count_2}</div>
                                <div class="stat-label-sm">死亡次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{kill_count_2}</div>
                                <div class="stat-label-sm">击杀次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{move_distance_2}</div>
                                <div class="stat-label-sm">移动距离</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_dealt_2}</div>
                                <div class="stat-label-sm">造成伤害</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_taken_2}</div>
                                <div class="stat-label-sm">收到伤害</div>
                            </div>
                        </div>
                    </div>
    """
    week3_data = {}
    week3_file_path = os.path.join(script_dir, '三周目', f'{uuid}.json') 
    if os.path.exists(week3_file_path):
        with open(week3_file_path, 'r', encoding='utf-8') as f:
            week3_data = json.load(f)
    custom_stats_3 = week3_data.get('stats', {}).get('minecraft:custom', {})
    killed_stats_3 = week3_data.get('stats', {}).get('minecraft:killed', {})
    kill_count_3 = sum(killed_stats_3.values()) if killed_stats_3 else '----'
    play_time_3 = custom_stats_3.get('minecraft:play_time')
    play_time_3 = f"{int(play_time_3 / 72000)}h" if play_time_3 else '----'
    death_count_3 = custom_stats_3.get('minecraft:deaths', '----')
    damage_dealt_3 = custom_stats_3.get('minecraft:damage_dealt', '----')
    damage_taken_3 = custom_stats_3.get('minecraft:damage_taken', '----')
    total_cm_3 = 0
    has_move_data_3 = False
    for stat in move_stats:
        if stat in custom_stats_3 and isinstance(custom_stats_3[stat], int):
            total_cm_3 += custom_stats_3[stat]
            has_move_data_3 = True
    move_distance_3 = f"{total_cm_3 / 100:.1f}m" if has_move_data_3 else '----'
    player_card += f"""
                    <div class="dimension dimension-3 stacked-dimension">
                        <div class="dimension-title">三周目数据</div>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value-sm">{play_time_3}</div>
                                <div class="stat-label-sm">游戏时间</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{death_count_3}</div>
                                <div class="stat-label-sm">死亡次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{kill_count_3}</div>
                                <div class="stat-label-sm">击杀次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{move_distance_3}</div>
                                <div class="stat-label-sm">移动距离</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_dealt_3}</div>
                                <div class="stat-label-sm">造成伤害</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value-sm">{damage_taken_3}</div>
                                <div class="stat-label-sm">收到伤害</div>
                            </div>
                        </div>
                    </div>
    """
    player_card += """
                </div>
            </div>
    """
    html_content += player_card
html_content += f"""
            </div>
        </div>
    </div>
    <footer>
        <p style="margin-top: 8px;">&copy; 2025 十八方块研究所玩家数据统计面板</p>
    </footer>
</body>
</html>
"""
output_path = os.path.join(script_dir, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"静态页面生成成功！已在tongji目录下生成index.html（更新时间：{update_time}）")