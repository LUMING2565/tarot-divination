"""
塔罗牌占卜 API 服务
FastAPI 后端，提供牌阵抽取、牌义解读等接口
支持 DeepSeek-V3 联合推理，生成更具体全面的 AI 解读
"""
import random
import uuid
import os
import json
import asyncio
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tarot_data import (
    MAJOR_ARCANA, MINOR_ARCANA_SUITS, MINOR_ARCANA_RANKS,
    MINOR_ARCANA_MEANINGS, SPREADS
)

# ============ DeepSeek API 配置 ============
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"  # DeepSeek-V3
AI_ENABLED = bool(DEEPSEEK_API_KEY)

app = FastAPI(title="塔罗牌占卜 API", version="1.0.0")

# CORS — 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 前端静态文件路径
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "tarot-frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/app")
    @app.get("/app/")
    async def serve_frontend():
        """提供前端页面"""
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# ============ 构建完整牌库 ============

def build_full_deck():
    """构建完整的78张塔罗牌"""
    deck = []
    card_id = 0

    # 大阿卡纳
    for card in MAJOR_ARCANA:
        deck.append({
            "card_id": card_id,
            "type": "major",
            "name_zh": card["name_zh"],
            "name_en": card["name_en"],
            "suit": None,
            "suit_zh": None,
            "rank": None,
            "element": card["element"],
            "planet": card["planet"],
            "keywords": card["keywords"],
            "upright": card["upright"],
            "reversed": card["reversed"],
        })
        card_id += 1

    # 小阿卡纳
    for suit_key, suit_info in MINOR_ARCANA_SUITS.items():
        for rank_info in MINOR_ARCANA_RANKS:
            rank_key = rank_info["rank"]
            meaning = MINOR_ARCANA_MEANINGS.get(suit_key, {}).get(rank_key, {})
            deck.append({
                "card_id": card_id,
                "type": "minor",
                "name_zh": f"{suit_info['name_zh']}{rank_info['name_zh']}",
                "name_en": f"{rank_key.title()} of {suit_key.title()}",
                "suit": suit_key,
                "suit_zh": suit_info["name_zh"],
                "rank": rank_key,
                "rank_zh": rank_info["name_zh"],
                "element": suit_info["element"],
                "domain": suit_info["domain"],
                "keywords": [],
                "upright": {
                    "summary": meaning.get("upright", f"{rank_info['meaning_prefix']}的{suit_info['name_zh']}能量"),
                    "love": meaning.get("upright", ""),
                    "career": meaning.get("upright", ""),
                    "fortune": meaning.get("upright", ""),
                },
                "reversed": {
                    "summary": meaning.get("reversed", f"{rank_info['meaning_prefix']}的{suit_info['name_zh']}能量被阻碍"),
                    "love": meaning.get("reversed", ""),
                    "career": meaning.get("reversed", ""),
                    "fortune": meaning.get("reversed", ""),
                },
            })
            card_id += 1

    return deck

FULL_DECK = build_full_deck()

# ============ 内存存储 ============
readings_store = {}  # reading_id -> reading data

# ============ 模型 ============

class ReadingRequest(BaseModel):
    spread_type: str = "three"  # single, three, celtic_cross, relationship, horseshoe
    question: str = ""  # 用户的问题（可选）

class CardInterpretation(BaseModel):
    position: str         # 牌位名称
    position_index: int   # 牌位序号
    card_id: int
    name_zh: str
    name_en: str
    type: str             # major / minor
    suit_zh: str | None
    element: str | None
    keywords: list[str]
    is_reversed: bool     # 是否逆位
    interpretation: dict  # 正位或逆位的释义

class ReadingResponse(BaseModel):
    reading_id: str
    spread_name: str
    spread_description: str
    question: str
    cards: list[CardInterpretation]
    overall_reading: str   # 综合解读
    ai_powered: bool       # 是否使用了 AI 增强解读
    created_at: str

# ============ API 路由 ============

@app.get("/")
async def root():
    """访问根路径直接展示塔罗牌占卜页面"""
    if os.path.isdir(FRONTEND_DIR):
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
    return {"name": "塔罗牌占卜 API", "version": "1.0.0", "cards_total": len(FULL_DECK)}

@app.get("/api/deck")
def get_deck():
    """获取完整牌库（不含释义详情，用于前端展示牌背）"""
    return {
        "total": len(FULL_DECK),
        "cards": [
            {
                "card_id": c["card_id"],
                "name_zh": c["name_zh"],
                "name_en": c["name_en"],
                "type": c["type"],
                "suit_zh": c["suit_zh"],
                "element": c["element"],
            }
            for c in FULL_DECK
        ]
    }

@app.get("/api/spreads")
def get_spreads():
    """获取所有可用牌阵"""
    return SPREADS

@app.post("/api/reading")
async def create_reading(req: ReadingRequest, x_api_key: str = Header(default="")):
    """抽牌并进行占卜解读（AI 增强）"""
    if req.spread_type not in SPREADS:
        raise HTTPException(status_code=400, detail=f"不支持的牌阵类型: {req.spread_type}")

    spread = SPREADS[req.spread_type]
    count = spread["cards_count"]

    # 随机抽牌
    selected = random.sample(FULL_DECK, count)

    # 构建解读
    cards = []
    for i, card in enumerate(selected):
        is_reversed = random.random() < 0.3
        cards.append(CardInterpretation(
            position=spread["positions"][i],
            position_index=i,
            card_id=card["card_id"],
            name_zh=card["name_zh"],
            name_en=card["name_en"],
            type=card["type"],
            suit_zh=card["suit_zh"],
            element=card["element"],
            keywords=card["keywords"],
            is_reversed=is_reversed,
            interpretation=card["reversed"] if is_reversed else card["upright"],
        ))

    # 优先使用请求中的 API key，其次环境变量
    api_key = x_api_key or DEEPSEEK_API_KEY
    ai_powered = False
    overall = generate_overall_reading(cards, req.spread_type, req.question)

    if api_key:
        try:
            ai_overall = await call_deepseek_reading(cards, spread, req.question, api_key)
            if ai_overall:
                overall = ai_overall
                ai_powered = True
        except Exception as e:
            print(f"[AI] DeepSeek 调用失败，使用本地解读: {e}")

    reading_id = str(uuid.uuid4())[:8]
    reading = {
        "reading_id": reading_id,
        "spread_name": spread["name"],
        "spread_description": spread["description"],
        "question": req.question,
        "cards": [c.model_dump() for c in cards],
        "overall_reading": overall,
        "ai_powered": ai_powered,
        "created_at": datetime.now().isoformat(),
    }
    readings_store[reading_id] = reading
    return reading


@app.get("/api/ai/check")
async def check_ai_key(x_api_key: str = Header(default="")):
    """检查 AI API Key 是否有效"""
    api_key = x_api_key or DEEPSEEK_API_KEY
    if not api_key:
        return {"status": "no_key", "message": "未配置 API Key"}

    try:
        import httpx
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "max_tokens": 5,
                },
            )
            if resp.status_code == 200:
                return {"status": "ok", "message": "DeepSeek-V3 API Key 有效"}
            else:
                return {"status": "invalid", "message": f"API 返回错误: {resp.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/reading/{reading_id}")
def get_reading(reading_id: str):
    """获取历史占卜记录"""
    if reading_id not in readings_store:
        raise HTTPException(status_code=404, detail="占卜记录不存在")
    return readings_store[reading_id]


@app.get("/api/card/{card_id}")
def get_card_detail(card_id: int):
    """获取单张牌的详细信息"""
    if card_id < 0 or card_id >= len(FULL_DECK):
        raise HTTPException(status_code=404, detail="牌不存在")
    return FULL_DECK[card_id]

# ============ DeepSeek AI 联合推理 ============

async def call_deepseek_reading(
    cards: list[CardInterpretation],
    spread: dict,
    question: str,
    api_key: str = "",
) -> str | None:
    """调用 DeepSeek-V3 进行深度塔罗解读"""
    key = api_key or DEEPSEEK_API_KEY
    if not key:
        return None

    # 构建牌阵信息
    cards_info = []
    for c in cards:
        direction = "逆位" if c.is_reversed else "正位"
        cards_info.append({
            "position": c.position,
            "card": f"{c.name_zh}（{c.name_en}）",
            "direction": direction,
            "type": "大阿卡纳" if c.type == "major" else f"小阿卡纳·{c.suit_zh or ''}",
            "element": c.element or "",
            "base_meaning": c.interpretation["summary"],
        })

    # 构建给 AI 的系统提示
    system_prompt = """你是一位资深塔罗牌占卜师，拥有30年解读经验。你精通：
- 78张塔罗牌的深层含义与象征
- 各种牌阵的结构与解读方法
- 正位与逆位的能量解读
- 卡牌之间的组合与联动含义
- 心理学与荣格原型理论
- 占星学与元素对应关系

请根据用户抽到的牌阵，给出专业、深入、温暖的解读。要求：
1. 逐张分析每张牌在当前牌位中的具体含义
2. 结合用户的具体问题（如果有）给出针对性指导
3. 分析牌与牌之间的能量流动和关联
4. 从感情、事业、财运、心灵成长等多个维度展开
5. 给出务实可行的建议，而非空洞的安慰
6. 使用温馨而有智慧的语气，适当引用塔罗的象征意义
7. 提示正逆位组合传递的整体信息
8. 结尾给出一个简短的能量总结（一句话）"""

    user_prompt = f"""请为我解读以下塔罗牌阵：

【牌阵类型】{spread['name']}
【牌阵说明】{spread['description']}
【用户问题】{question or '无具体问题，请给予综合指引'}

【抽到的牌】
{json.dumps(cards_info, ensure_ascii=False, indent=2)}

请按以下结构输出解读：
## 🔮 整体能量概览
（2-3句话概括牌阵整体能量）

## 📜 各牌位详细解读
（逐一分析每张牌在对应牌位中的含义）

## 🔗 牌阵联动分析
（分析牌与牌之间的关联、冲突、加强关系）

## 💫 多维指引
（分感情、事业、财运、心灵成长等方面给出建议）

## ✨ 能量总结
（一句话总结）"""

    try:
        # 使用 httpx 异步调用
        import httpx
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2048,
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                # 标记 AI 生成
                return f"> 🤖 本解读由 **DeepSeek-V3** 联合推理模型生成，结合传统塔罗智慧与 AI 深度分析。\n\n{content}"
            else:
                print(f"[AI] API 返回错误 {resp.status_code}: {resp.text}")
                return None
    except Exception as e:
        print(f"[AI] 调用异常: {e}")
        return None


# ============ 本地规则解读（备选） ============

def generate_overall_reading(cards: list[CardInterpretation], spread_type: str, question: str) -> str:
    """根据抽到的牌生成综合解读"""
    major_count = sum(1 for c in cards if c.type == "major")
    reversed_count = sum(1 for c in cards if c.is_reversed)

    parts = []

    # 开场
    if question:
        parts.append(f"🎴 你提出的问题是：「{question}」\n")
    parts.append(f"📜 本次使用 **{SPREADS[spread_type]['name']}** 为你解读。\n")

    # 逐牌解读
    for c in cards:
        direction = "逆位 ⚠️" if c.is_reversed else "正位 ✨"
        parts.append(
            f"\n### [{c.position}] {c.name_zh} ({c.name_en}) — {direction}\n"
            f"**{c.interpretation['summary']}**\n"
        )
        if c.interpretation.get("love"):
            parts.append(f"- 💕 感情：{c.interpretation['love']}")
        if c.interpretation.get("career"):
            parts.append(f"- 💼 事业：{c.interpretation['career']}")
        if c.interpretation.get("fortune"):
            parts.append(f"- 💰 财运：{c.interpretation['fortune']}")

    # 综合分析
    parts.append("\n---\n## 🔮 综合分析\n")

    if major_count >= 2:
        parts.append("牌阵中出现多张大阿卡纳，说明命运之力正在强力作用。这些重大的能量将对你的人生产生深远影响。")
    elif major_count == 0:
        parts.append("牌阵中全部为小阿卡纳，说明当前的问题主要体现在日常生活的具体事务上，需要从细节入手。")

    if reversed_count >= 2:
        parts.append("部分牌以逆位出现，提示当前可能存在一些阻塞或需要内省的地方。注意调整心态，不要抗拒改变的到来。")
    elif reversed_count == 0:
        parts.append("所有牌均为正位，能量流动顺畅。这是一个万事俱备的好时机，大胆前行。")

    # 结尾
    parts.append("\n> 🌙 塔罗牌是你潜意识的镜子，以上解读仅供参考。最终的选择权永远在你手中。")

    return "\n".join(parts)

# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
