"""
Vercel Serverless 入口 — 塔罗牌占卜
所有请求通过此 FastAPI 应用处理
"""
import os, sys, random, uuid, json
from datetime import datetime

# 确保能找到 tarot-backend 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tarot-backend"))
from tarot_data import *

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "tarot-frontend")
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

app = FastAPI(title="塔罗牌占卜")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ============ 牌库 ============
def build_deck():
    deck, cid = [], 0
    for c in MAJOR_ARCANA:
        deck.append(dict(card_id=cid, type="major", name_zh=c["name_zh"], name_en=c["name_en"],
            suit=None, suit_zh=None, element=c["element"], keywords=c["keywords"],
            upright=c["upright"], reversed=c["reversed"])); cid += 1
    for sk, si in MINOR_ARCANA_SUITS.items():
        for ri in MINOR_ARCANA_RANKS:
            rk = ri["rank"]; m = MINOR_ARCANA_MEANINGS.get(sk, {}).get(rk, {})
            deck.append(dict(card_id=cid, type="minor", name_zh=f"{si['name_zh']}{ri['name_zh']}",
                name_en=f"{rk.title()} of {sk.title()}", suit=sk, suit_zh=si["name_zh"], element=si["element"],
                keywords=[], upright=dict(summary=m.get("upright",""), love=m.get("upright",""),
                career=m.get("upright",""), fortune=m.get("upright","")),
                reversed=dict(summary=m.get("reversed",""), love=m.get("reversed",""),
                career=m.get("reversed",""), fortune=m.get("reversed","")))); cid += 1
    return deck

DECK = build_deck()
STORE = {}

class ReadingReq(BaseModel):
    spread_type: str = "three"; question: str = ""

# ============ 前端 ============
@app.get("/")
@app.get("/app")
@app.get("/app/")
async def serve_frontend():
    path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(path): return FileResponse(path)
    return {"name": "塔罗牌占卜 API", "cards": len(DECK)}

# ============ API ============
@app.get("/api/spreads")
def get_spreads(): return SPREADS

@app.get("/api/deck")
def get_deck():
    return {"total": len(DECK), "cards": [{"card_id": c["card_id"], "name_zh": c["name_zh"],
        "name_en": c["name_en"], "type": c["type"], "suit_zh": c["suit_zh"], "element": c["element"]} for c in DECK]}

@app.post("/api/reading")
async def create_reading(req: ReadingReq, x_api_key: str = Header(default="")):
    if req.spread_type not in SPREADS: raise HTTPException(400, "不支持的牌阵")
    spread = SPREADS[req.spread_type]; selected = random.sample(DECK, spread["cards_count"])
    cards = []
    for i, c in enumerate(selected):
        is_rev = random.random() < 0.3
        cards.append(dict(position=spread["positions"][i], position_index=i, card_id=c["card_id"],
            name_zh=c["name_zh"], name_en=c["name_en"], type=c["type"], suit_zh=c["suit_zh"],
            element=c["element"], keywords=c["keywords"], is_reversed=is_rev,
            interpretation=c["reversed"] if is_rev else c["upright"]))
    ai_powered = False
    overall = local_reading(cards, req.spread_type, req.question)
    key = x_api_key or DEEPSEEK_KEY
    if key:
        try:
            ao = await ai_reading(cards, spread, req.question, key)
            if ao: overall, ai_powered = ao, True
        except: pass
    rid = str(uuid.uuid4())[:8]
    r = {"reading_id": rid, "spread_name": spread["name"], "spread_description": spread["description"],
        "question": req.question, "cards": cards, "overall_reading": overall,
        "ai_powered": ai_powered, "created_at": datetime.now().isoformat()}
    STORE[rid] = r; return r

@app.get("/api/ai/check")
async def check_ai(x_api_key: str = Header(default="")):
    key = x_api_key or DEEPSEEK_KEY
    if not key: return {"status": "no_key"}
    try:
        import httpx
        async with httpx.AsyncClient(timeout=15) as cl:
            r = await cl.post("https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5})
            return {"status": "ok" if r.status_code == 200 else "invalid"}
    except: return {"status": "error"}

# ============ 本地解读 ============
def local_reading(cards, stype, question):
    p = []
    if question: p.append(f"🎴 问题：「{question}」\n")
    p.append(f"📜 **{SPREADS[stype]['name']}**\n")
    for c in cards:
        d = "逆位 ⚠️" if c["is_reversed"] else "正位 ✨"
        p.append(f"\n### [{c['position']}] {c['name_zh']} — {d}\n**{c['interpretation']['summary']}**\n")
        for k, em in [("love","💕 感情"), ("career","💼 事业"), ("fortune","💰 财运")]:
            if c["interpretation"].get(k): p.append(f"- {em}：{c['interpretation'][k]}")
    mc = sum(1 for c in cards if c["type"] == "major")
    rc = sum(1 for c in cards if c["is_reversed"])
    p.append("\n---\n## 🔮 综合分析\n")
    if mc >= 2: p.append("多张大阿卡纳，命运之力强力作用。")
    elif mc == 0: p.append("全小阿卡纳，关注日常细节。")
    if rc >= 2: p.append("多张逆位提示存在阻塞。")
    p.append("\n> 🌙 塔罗是你潜意识的镜子。")
    return "\n".join(p)

# ============ AI 解读 ============
async def ai_reading(cards, spread, question, key):
    ci = [{"position": c["position"], "card": c["name_zh"],
           "direction": "逆位" if c["is_reversed"] else "正位",
           "meaning": c["interpretation"]["summary"]} for c in cards]
    prompt = f"""你是资深塔罗师。牌阵:{spread['name']}。问题:{question or '无'}。
牌:{json.dumps(ci, ensure_ascii=False)}
输出：## 🔮整体能量 ## 📜各牌解读 ## 🔗联动分析 ## 💫多维指引 ## ✨总结"""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=50) as cl:
            r = await cl.post("https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [
                    {"role": "system", "content": "你是资深塔罗占卜师，30年经验。解读具体深入，温暖有智慧。"},
                    {"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 2048})
            if r.status_code == 200:
                return "> 🤖 **DeepSeek-V3 AI 深度解读**\n\n" + r.json()["choices"][0]["message"]["content"]
    except: pass
    return None
