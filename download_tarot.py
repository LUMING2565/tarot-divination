import requests
import os
import json
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========== 配置 ==========
CATEGORY = "Rider-Waite-Smith_tarot_deck_(Geldard)"
OUTPUT_DIR = "./public/cards/rws"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Wikimedia API
API_URL = "https://commons.wikimedia.org/w/api.php"
# API 用这个 UA 即可，图片下载需要用浏览器 UA 避免 403
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json",
}

# 大阿卡纳——英文名 → 编号+规范名
MAJOR_EN = {
    "fool": "00-the-fool",
    "magician": "01-the-magician",
    "high priestess": "02-the-high-priestess",
    "empress": "03-the-empress",
    "emperor": "04-the-emperor",
    "hierophant": "05-the-hierophant",
    "lovers": "06-the-lovers",
    "chariot": "07-the-chariot",
    "strength": "08-strength",
    "hermit": "09-the-hermit",
    "wheel of fortune": "10-wheel-of-fortune",
    "justice": "11-justice",
    "hanged man": "12-the-hanged-man",
    "death": "13-death",
    "temperance": "14-temperance",
    "devil": "15-the-devil",
    "tower": "16-the-tower",
    "star": "17-the-star",
    "moon": "18-the-moon",
    "sun": "19-the-sun",
    "judgement": "20-judgement",
    "world": "21-the-world",
}

# 英文花色
SUIT_EN = {"wands": "wands", "cups": "cups", "swords": "swords", "pentacles": "pentacles"}

# 英文 rank → 规范名
RANK_EN = {
    "ace": "ace", "one": "ace",
    "two": "two", "three": "three", "four": "four", "five": "five",
    "six": "six", "seven": "seven", "eight": "eight", "nine": "nine", "ten": "ten",
    "page": "page", "knight": "knight", "queen": "queen", "king": "king",
}

# 小阿卡纳编号
SUIT_BASE = {"wands": 22, "cups": 36, "swords": 50, "pentacles": 64}
RANK_ORDER = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
              "page", "knight", "queen", "king"]


def create_session():
    """创建带重试机制的 requests Session"""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def get_card_number(rank, suit):
    base = SUIT_BASE.get(suit, 0)
    idx = RANK_ORDER.index(rank) if rank in RANK_ORDER else 0
    return base + idx


def get_files_from_category(session, category):
    """获取分类下所有文件（带缓存和重试）"""
    cache_file = os.path.join(OUTPUT_DIR, ".filelist_cache.json")

    # 尝试读缓存
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            cached = json.load(f)
        print(f"  (使用缓存文件列表: {len(cached)} 个文件)")
        return cached

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "max",
        "format": "json"
    }

    for attempt in range(10):
        try:
            resp = session.get(API_URL, params=params, timeout=60)
            if resp.status_code == 429 or resp.status_code == 403:
                wait = min((attempt + 1) * 15, 120)
                print(f"  ⏳ 被限流(HTTP {resp.status_code})，等待 {wait}s 后重试(第{attempt+1}次)...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            members = data.get("query", {}).get("categorymembers", [])
            files = [m for m in members if m["title"].startswith("File:")]
            # 缓存到磁盘
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(files, f, ensure_ascii=False)
            return files
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            wait = min((attempt + 1) * 10, 60)
            print(f"  ⚠️ 请求失败: {e}，等待 {wait}s 重试...")
            time.sleep(wait)
    raise RuntimeError("重试 10 次后仍无法获取文件列表，请稍后再运行脚本。")


def get_image_url(session, filename):
    """获取图片直接下载链接"""
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    resp = session.get(API_URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if "imageinfo" in page:
            return page["imageinfo"][0]["url"]
    return None


def guess_standard_name(filename):
    """根据文件名猜测规范命名"""
    name_lower = filename.replace("File:", "", 1).lower().strip()

    # 1. 大阿卡纳
    for key, en_name in MAJOR_EN.items():
        if key in name_lower:
            return en_name + ".jpg"

    # 2. 小阿卡纳: "Rank of Suit"
    match = re.match(
        r"(one|ace|two|three|four|five|six|seven|eight|nine|ten|page|knight|queen|king)"
        r"\s+of\s+(wands|cups|swords|pentacles)",
        name_lower
    )
    if match:
        rank = RANK_EN.get(match.group(1), match.group(1))
        suit = SUIT_EN.get(match.group(2), match.group(2))
        card_num = get_card_number(rank, suit)
        return f"{card_num:02d}-{rank}-of-{suit}.jpg"

    return None


def main():
    session = create_session()

    print("\U0001F52E 正在获取 Wikimedia Commons 文件列表...")
    files = get_files_from_category(session, CATEGORY)
    print(f"找到 {len(files)} 个文件")

    success = []
    failed = []
    manual = []

    for idx, f in enumerate(files, 1):
        title = f["title"].replace("File:", "")
        print(f"\n[{idx}/{len(files)}] 处理: {title}")

        # API 调用间隔，避免被封
        time.sleep(0.3)

        # 获取下载链接
        url = get_image_url(session, title)
        if not url:
            print("  ❌ 无法获取下载链接")
            failed.append(title)
            continue

        # 猜测规范名
        std_name = guess_standard_name(title)
        if not std_name:
            print(f"  ⚠️ 无法自动识别，将保留原名")
            std_name = title.replace(" ", "_")
            manual.append((title, std_name))

        output_path = os.path.join(OUTPUT_DIR, std_name)

        # 下载图片（单独请求，避免 session 连接复用问题）
        try:
            dl_headers = {
                "User-Agent": UA,
                "Referer": "https://commons.wikimedia.org/",
            }
            img_resp = requests.get(url, headers=dl_headers, timeout=120)
            img_resp.raise_for_status()
            with open(output_path, "wb") as out:
                out.write(img_resp.content)
            print(f"  ✅ 已保存: {std_name} ({len(img_resp.content)//1024}KB)")
            success.append((title, std_name))
            time.sleep(0.5)
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
            failed.append(title)

    # 输出报告
    print("\n" + "=" * 50)
    print(f"\U0001F4CA 下载完成: 成功 {len(success)}, 需手动 {len(manual)}, 失败 {len(failed)}")

    if manual:
        print("\n⚠️ 以下文件无法自动识别，请手动重命名:")
        for orig, saved in manual:
            print(f"  {saved} <- {orig}")

    if failed:
        print("\n❌ 下载失败的文件:")
        for f in failed:
            print(f"  {f}")


if __name__ == "__main__":
    main()
