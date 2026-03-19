import requests
import json
import time
import random

class SteamCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ])
        }
        self.games_data = []

    def fetch_top_rated(self, limit=1000):
        print(f"[*] 正在抓取前 {limit} 个高分游戏...")
        # 示例：使用 SteamSpy API 抓取
        try:
            url = "https://steamspy.com/api.php?request=all&page=0"
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            # 排序并提取
            sorted_games = sorted(data.values(), key=lambda x: x.get('positive', 0), reverse=True)
            for game in sorted_games[:limit]:
                self.games_data.append(self._format_game(game))
            
            print(f"[+] 成功抓取 {len(self.games_data)} 个高分游戏")
        except Exception as e:
            print(f"[!] 抓取失败: {e}")

    def fetch_trending(self, limit=500):
        print(f"[*] 正在抓取前 {limit} 个热门新品...")
        # 示例：使用 SteamSpy 热门接口
        try:
            url = "https://steamspy.com/api.php?request=top100in2weeks"
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            for game in list(data.values())[:limit]:
                self.games_data.append(self._format_game(game))
                
            print(f"[+] 成功抓取热门新品")
        except Exception as e:
            print(f"[!] 抓取失败: {e}")

    def _format_game(self, game):
        appid = game.get('appid')
        return {
            'id': appid,
            'name': game.get('name'),
            'tags': game.get('tags', []),
            'score': round(game.get('positive', 0) / (game.get('positive', 1) + game.get('negative', 0)) * 100, 2),
            'header_image': f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg",
            'description': f"Developer: {game.get('developer')}, Publisher: {game.get('publisher')}",
            'release_date': game.get('initialprice', 'N/A') # 示例字段
        }

    def save_to_json(self, filename="games_master.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.games_data, f, ensure_ascii=False, indent=4)
        print(f"[+] 数据已保存至 {filename}")

if __name__ == "__main__":
    crawler = SteamCrawler()
    crawler.fetch_top_rated(1000)
    time.sleep(random.uniform(1, 3))
    crawler.fetch_trending(500)
    crawler.save_to_json()
