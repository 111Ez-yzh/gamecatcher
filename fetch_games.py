#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Medicine Hunter (赛博采药人)

功能：一键抓取 Steam 高分与新品数据，生成 JSON 格式

使用说明：
1. 安装依赖：pip install -r requirements.txt
2. 运行脚本：python fetch_games.py

注意：本项目仅供学习，请遵守 Steam 的 Robots.txt 协议，切勿高频恶意爬取。
"""

import requests
import json
import time
import random

# 配置字典 - 可根据需要修改
CONFIG = {
    # 抓取配置
    'TOP_RATED_LIMIT': 50,  # 高分游戏抓取数量
    'TRENDING_LIMIT': 25,     # 热门新品抓取数量
    'MAX_RETRIES': 3,          # 最大重试次数
    'RETRY_DELAY': (1, 3),     # 重试延迟范围（秒）
    'REQUEST_DELAY': (1, 2),    # 请求间隔范围（秒）
    
    # API 配置
    'STEAMSPY_API': {
        'ALL_GAMES': 'https://steamspy.com/api.php?request=all&page=0',
        'TOP_100_IN_2WEEKS': 'https://steamspy.com/api.php?request=top100in2weeks'
    },
    'STEAM_API': {
        'APP_DETAIL': 'https://store.steampowered.com/api/appdetails?appids={}&l=zh-cn'
    },
    
    # 输出配置
    'OUTPUT_FILE': 'games_master.json'
}

class SteamCrawler:
    """
    Steam 游戏数据抓取器
    通过 SteamSpy API 获取游戏数据，包括高分游戏和热门新品
    """
    
    def __init__(self):
        """初始化抓取器"""
        # 随机 User-Agent，避免被封禁
        self.headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ])
        }
        self.games_data = []
    
    def _retry_request(self, url):
        """
        带重试机制的请求函数
        Args:
            url: 请求 URL
        Returns:
            响应数据（JSON 格式）
        """
        retries = 0
        while retries < CONFIG['MAX_RETRIES']:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()  # 检查 HTTP 状态码
                return response.json()
            except Exception as e:
                retries += 1
                if retries < CONFIG['MAX_RETRIES']:
                    delay = random.uniform(*CONFIG['RETRY_DELAY'])
                    print(f"[!] 请求失败，{delay:.2f}秒后重试 ({retries}/{CONFIG['MAX_RETRIES']}): {e}")
                    time.sleep(delay)
                else:
                    print(f"[!] 请求失败，已达到最大重试次数: {e}")
                    return None
    
    def fetch_top_rated(self, limit=None):
        """
        抓取高分游戏
        Args:
            limit: 抓取数量，默认为配置中的 TOP_RATED_LIMIT
        """
        if limit is None:
            limit = CONFIG['TOP_RATED_LIMIT']
        
        print(f"[*] 正在抓取前 {limit} 个高分游戏...")
        
        # 使用 SteamSpy API 抓取所有游戏数据
        data = self._retry_request(CONFIG['STEAMSPY_API']['ALL_GAMES'])
        
        if data:
            # 按好评数排序并提取
            sorted_games = sorted(data.values(), key=lambda x: x.get('positive', 0), reverse=True)
            for game in sorted_games[:limit]:
                self.games_data.append(self._format_game(game))
            
            print(f"[+] 成功抓取 {len(self.games_data)} 个高分游戏")
        else:
            print("[!] 抓取高分游戏失败")
        
        # 添加随机延迟，避免请求过于频繁
        time.sleep(random.uniform(*CONFIG['REQUEST_DELAY']))
    
    def fetch_trending(self, limit=None):
        """
        抓取热门新品
        Args:
            limit: 抓取数量，默认为配置中的 TRENDING_LIMIT
        """
        if limit is None:
            limit = CONFIG['TRENDING_LIMIT']
        
        print(f"[*] 正在抓取前 {limit} 个热门新品...")
        
        # 使用 SteamSpy 热门接口
        data = self._retry_request(CONFIG['STEAMSPY_API']['TOP_100_IN_2WEEKS'])
        
        if data:
            for game in list(data.values())[:limit]:
                self.games_data.append(self._format_game(game))
            
            print(f"[+] 成功抓取热门新品")
        else:
            print("[!] 抓取热门新品失败")
        
        # 添加随机延迟，避免请求过于频繁
        time.sleep(random.uniform(*CONFIG['REQUEST_DELAY']))
    
    def _get_game_tags(self, appid):
        """
        从 Steam 官方 API 获取游戏标签
        Args:
            appid: 游戏 ID
        Returns:
            游戏标签列表
        """
        tags = []
        try:
            url = CONFIG['STEAM_API']['APP_DETAIL'].format(appid)
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if str(appid) in data and data[str(appid)]['success']:
                game_data = data[str(appid)]['data']
                # 获取标签
                if 'genres' in game_data:
                    tags = [genre['description'] for genre in game_data['genres']]
                # 也可以添加类别信息
                if 'categories' in game_data:
                    categories = [cat['description'] for cat in game_data['categories']]
                    tags.extend(categories)
            
            # 随机延迟，避免请求过于频繁
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"[!] 获取游戏标签失败 (APP ID: {appid}): {e}")
        
        return tags
    
    def _format_game(self, game):
        """
        格式化游戏数据
        Args:
            game: 原始游戏数据
        Returns:
            格式化后的游戏数据
        """
        appid = game.get('appid')
        
        # 从 Steam 官方 API 获取标签
        tags = self._get_game_tags(appid)
        
        return {
            'id': appid,
            'name': game.get('name'),
            'tags': tags,
            'score': round(game.get('positive', 0) / (game.get('positive', 1) + game.get('negative', 0)) * 100, 2),
            'header_image': f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg",
            'description': f"Developer: {game.get('developer')}, Publisher: {game.get('publisher')}",
            'release_date': game.get('initialprice', 'N/A')  # 示例字段
        }
    
    def save_to_json(self, filename=None):
        """
        保存数据到 JSON 文件
        Args:
            filename: 输出文件名，默认为配置中的 OUTPUT_FILE
        """
        if filename is None:
            filename = CONFIG['OUTPUT_FILE']
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.games_data, f, ensure_ascii=False, indent=4)
        print(f"[+] 数据已保存至 {filename}")

if __name__ == "__main__":
    """主函数"""
    crawler = SteamCrawler()
    crawler.fetch_top_rated()
    crawler.fetch_trending()
    crawler.save_to_json()