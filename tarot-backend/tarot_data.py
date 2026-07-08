"""
78张塔罗牌完整数据
22张大阿卡纳 (Major Arcana) + 56张小阿卡纳 (Minor Arcana)
每张牌包含：名称、关键词、正位释义、逆位释义、元素、占星对应
"""

MAJOR_ARCANA = [
    {
        "id": 0, "name_en": "The Fool", "name_zh": "愚者",
        "element": "风", "planet": "天王星",
        "keywords": ["开始", "冒险", "天真", "自由", " spontaneity"],
        "upright": {
            "summary": "新的开始，一段未知的旅程即将展开",
            "love": "轻松愉快的恋情，保持开放的心态",
            "career": "新的工作机会，勇于尝试",
            "fortune": "意外之喜，把握当下的机会"
        },
        "reversed": {
            "summary": "鲁莽行事，缺乏考虑，可能错过良机",
            "love": "冲动的情感决定，需冷静思考",
            "career": "贸然跳槽有风险，需谨慎评估",
            "fortune": "冒险投资需三思，避免不必要的损失"
        }
    },
    {
        "id": 1, "name_en": "The Magician", "name_zh": "魔术师",
        "element": "风", "planet": "水星",
        "keywords": ["创造", "能力", "意志力", "自信", "技巧"],
        "upright": {
            "summary": "你拥有创造奇迹的能力，万事俱备",
            "love": "主动出击的好时机，展现你的魅力",
            "career": "专注与技能的展现，将获得认可",
            "fortune": "财运亨通，善用你的资源和能力"
        },
        "reversed": {
            "summary": "能力被滥用或未被善用，缺乏行动力",
            "love": "花言巧语需警惕，看清对方的真实意图",
            "career": "才华被埋没，需要重新找到方向",
            "fortune": "投资需谨慎，不要被表象迷惑"
        }
    },
    {
        "id": 2, "name_en": "The High Priestess", "name_zh": "女祭司",
        "element": "水", "planet": "月亮",
        "keywords": ["直觉", "潜意识", "神秘", "智慧", "内省"],
        "upright": {
            "summary": "倾听内心的声音，直觉会指引你方向",
            "love": "心灵相通的缘分，等待比追求更有意义",
            "career": "需要更多的知识和内在的沉淀",
            "fortune": "暗中酝酿的机会，保持耐心"
        },
        "reversed": {
            "summary": "忽略了内心的声音，被表面的信息迷惑",
            "love": "隐藏的情感或秘密可能浮现",
            "career": "信息不透明，不要贸然做决定",
            "fortune": "潜在的财务问题需要关注"
        }
    },
    {
        "id": 3, "name_en": "The Empress", "name_zh": "皇后",
        "element": "土", "planet": "金星",
        "keywords": ["丰收", "母性", "美", "自然", "丰饶"],
        "upright": {
            "summary": "收获的季节，万物生长，幸福美满",
            "love": "感情甜蜜稳定，适合成家立业",
            "career": "创意与成果将得到丰厚的回报",
            "fortune": "财运旺盛，适合投资和理财"
        },
        "reversed": {
            "summary": "收获延迟，创造力被压抑，过度依赖",
            "love": "感情中的不平等让你疲惫",
            "career": "付出多却回报少，需要调整心态",
            "fortune": "冲动消费，需控制开支"
        }
    },
    {
        "id": 4, "name_en": "The Emperor", "name_zh": "皇帝",
        "element": "火", "planet": "白羊座",
        "keywords": ["权威", "秩序", "领导", "稳定", "权力"],
        "upright": {
            "summary": "凭借纪律与权威获得成功，掌控全局",
            "love": "稳重成熟的伴侣，或者需要更多责任心",
            "career": "升职加薪，领导能力获得认可",
            "fortune": "财务稳定，有规划的收入增长"
        },
        "reversed": {
            "summary": "滥用权力，缺乏自律，或被人控制",
            "love": "控制欲太强，让对方感到窒息",
            "career": "与上级发生冲突，或缺乏执行力",
            "fortune": "财务混乱，需要重新规划"
        }
    },
    {
        "id": 5, "name_en": "The Hierophant", "name_zh": "教皇",
        "element": "土", "planet": "金牛座",
        "keywords": ["传统", "信仰", "教育", "精神引导", "仪式"],
        "upright": {
            "summary": "遵循传统，寻求智慧的指引和精神成长",
            "love": "适合步入婚姻，传统的恋爱方式",
            "career": "按部就班，适合进修和学习",
            "fortune": "稳健保守的理财方式更合适"
        },
        "reversed": {
            "summary": "挑战传统，被陈旧观念束缚，缺乏独立思考",
            "love": "不按常理出牌的关系，需要打破常规",
            "career": "创新受阻于旧制度，需要灵活变通",
            "fortune": "打破常规可能会带来新的机会"
        }
    },
    {
        "id": 6, "name_en": "The Lovers", "name_zh": "恋人",
        "element": "风", "planet": "双子座",
        "keywords": ["爱情", "选择", "和谐", "结合", "价值观"],
        "upright": {
            "summary": "命中注定的缘分，重要的选择摆在面前",
            "love": "美满的爱情，灵魂的契合",
            "career": "适合合伙创业，合作关系良好",
            "fortune": "合作带来财富，但需做明智选择"
        },
        "reversed": {
            "summary": "感情破裂，错误的选择，价值观冲突",
            "love": "三角关系，或感情出现裂痕",
            "career": "合伙关系破裂，需重新考虑合作",
            "fortune": "因情感因素做出不理智的财务决策"
        }
    },
    {
        "id": 7, "name_en": "The Chariot", "name_zh": "战车",
        "element": "水", "planet": "巨蟹座",
        "keywords": ["胜利", "动力", "决心", "控制", "前进"],
        "upright": {
            "summary": "克服困难，凭借坚强的意志力达成目标",
            "love": "主动追求，努力经营感情会成功",
            "career": "事业突飞猛进，竞争中胜出",
            "fortune": "积极主动出击，财务目标可实现"
        },
        "reversed": {
            "summary": "失控，失败，方向错误，被情绪主导",
            "love": "争吵激烈，无法控制局面",
            "career": "竞争失利，需要调整策略",
            "fortune": "财务失控，投资失利"
        }
    },
    {
        "id": 8, "name_en": "Strength", "name_zh": "力量",
        "element": "火", "planet": "狮子座",
        "keywords": ["勇气", "耐心", "内在力量", "信心", "温柔"],
        "upright": {
            "summary": "以柔克刚，用爱和耐心驯服内心的野兽",
            "love": "温柔的力量让感情更深厚",
            "career": "面对挑战从容不迫，内在实力支撑",
            "fortune": "稳健理财，不被短期波动影响"
        },
        "reversed": {
            "summary": "自我怀疑，脆弱，失去内在的平衡",
            "love": "缺乏自信让感情出现危机",
            "career": "压力过大，需要找回信心",
            "fortune": "因恐惧做出保守决策"
        }
    },
    {
        "id": 9, "name_en": "The Hermit", "name_zh": "隐士",
        "element": "土", "planet": "处女座",
        "keywords": ["内省", "孤独", "智慧", "引导", "沉思"],
        "upright": {
            "summary": "向内探索的时期，独处带来深刻的领悟",
            "love": "需要时间和空间思考真正想要什么",
            "career": "适合独自深耕、学习和研究",
            "fortune": "需要更谨慎的财务规划"
        },
        "reversed": {
            "summary": "过度孤立，逃避现实，拒绝帮助",
            "love": "过于封闭自己，错过缘分",
            "career": "与团队脱节，需要与人交流",
            "fortune": "拒绝理财建议，一意孤行"
        }
    },
    {
        "id": 10, "name_en": "Wheel of Fortune", "name_zh": "命运之轮",
        "element": "火", "planet": "木星",
        "keywords": ["命运", "转折", "机遇", "循环", "因果"],
        "upright": {
            "summary": "命运之轮转动，好运将至，顺势而为",
            "love": "命运的安排，良缘将至",
            "career": "转运的机会来了，把握转折点",
            "fortune": "财运上升期，好运连连"
        },
        "reversed": {
            "summary": "厄运降临，抵抗变化，被命运捉弄",
            "love": "感情起伏不定，遭遇挫折",
            "career": "意想不到的变故，需要随机应变",
            "fortune": "财运低迷，做好风险防范"
        }
    },
    {
        "id": 11, "name_en": "Justice", "name_zh": "正义",
        "element": "风", "planet": "天秤座",
        "keywords": ["公平", "真相", "因果", "平衡", "法律"],
        "upright": {
            "summary": "公平公正的结果，为自己的行为负责",
            "love": "平等的关系，诚实相待",
            "career": "公正的评判，付出得到应有回报",
            "fortune": "财务平衡，合理分配资源"
        },
        "reversed": {
            "summary": "不公的待遇，逃避责任，偏见影响判断",
            "love": "不平等的关系需要重新审视",
            "career": "遭遇不公平对待，需要据理力争",
            "fortune": "财务纠纷，合同需要仔细检查"
        }
    },
    {
        "id": 12, "name_en": "The Hanged Man", "name_zh": "倒吊人",
        "element": "水", "planet": "海王星",
        "keywords": ["牺牲", "等待", "换位思考", "放下", "顿悟"],
        "upright": {
            "summary": "换个角度看世界，暂时的停顿是为了更好的出发",
            "love": "为爱付出和等待，但不要失去自我",
            "career": "暂时停滞，适合反思和调整方向",
            "fortune": "需要暂时牺牲短期利益换取长远发展"
        },
        "reversed": {
            "summary": "不愿做出必要的牺牲，无谓的挣扎",
            "love": "不愿妥协导致关系僵持",
            "career": "固执己见，拒绝改变会错失机会",
            "fortune": "不愿止损导致更大损失"
        }
    },
    {
        "id": 13, "name_en": "Death", "name_zh": "死神",
        "element": "水", "planet": "天蝎座",
        "keywords": ["结束", "转变", "重生", "放下", "新生"],
        "upright": {
            "summary": "旧的篇章结束，全新的开始即将来临",
            "love": "旧感情的彻底结束，或关系进入新阶段",
            "career": "职业生涯的重大转变，置之死地而后生",
            "fortune": "旧的财务模式终结，新的机会出现"
        },
        "reversed": {
            "summary": "抗拒改变，停滞不前，拖着不放",
            "love": "不愿放手已经结束的感情",
            "career": "死守已经没有前途的工作",
            "fortune": "坚持错误的投资，不肯放手"
        }
    },
    {
        "id": 14, "name_en": "Temperance", "name_zh": "节制",
        "element": "火", "planet": "射手座",
        "keywords": ["平衡", "中庸", "调和", "耐心", "适应"],
        "upright": {
            "summary": "调和矛盾，找到生活的平衡点，从容应对",
            "love": "感情细水长流，互相理解和包容",
            "career": "工作与生活的平衡，稳中求进",
            "fortune": "合理的财务管理，收支平衡"
        },
        "reversed": {
            "summary": "失衡，过度或不足，缺乏节制",
            "love": "关系失衡，一方付出过多",
            "career": "工作过度劳累，需要调整节奏",
            "fortune": "消费失控或过度节俭"
        }
    },
    {
        "id": 15, "name_en": "The Devil", "name_zh": "恶魔",
        "element": "土", "planet": "摩羯座",
        "keywords": ["欲望", "束缚", "诱惑", "物质主义", "阴影"],
        "upright": {
            "summary": "被欲望和执念束缚，但钥匙就在自己手中",
            "love": "激情却危险的恋情，需警惕控制与依赖",
            "career": "对权力和金钱的迷恋可能走上歧途",
            "fortune": "贪婪导致损失，需审视消费习惯"
        },
        "reversed": {
            "summary": "挣脱束缚，觉醒，认清内心的欲望",
            "love": "从一段不健康的关系中解脱",
            "career": "摆脱不良工作环境，重获自由",
            "fortune": "停止沉迷于物质追求"
        }
    },
    {
        "id": 16, "name_en": "The Tower", "name_zh": "高塔",
        "element": "火", "planet": "火星",
        "keywords": ["剧变", "崩塌", "启示", "觉醒", "颠覆"],
        "upright": {
            "summary": "突然的变故打破了原有的秩序，但也带来了觉醒",
            "love": "突如其来的分手或关系危机",
            "career": "失业或公司变动，但可能是转机",
            "fortune": "意外的财务损失，需重建"
        },
        "reversed": {
            "summary": "阻止不可避免的改变，恐惧改变",
            "love": "努力修补已经破碎的关系",
            "career": "勉强维持现状，但压力日增",
            "fortune": "财务危机的预警"
        }
    },
    {
        "id": 17, "name_en": "The Star", "name_zh": "星星",
        "element": "风", "planet": "水瓶座",
        "keywords": ["希望", "灵感", "平静", "疗愈", "信心"],
        "upright": {
            "summary": "希望的曙光出现，心中充满平静与信心",
            "love": "美好的缘分正在靠近，保持期待",
            "career": "充满灵感和创意，前途光明",
            "fortune": "财务状况好转，新希望出现"
        },
        "reversed": {
            "summary": "失望，失去希望，自我怀疑",
            "love": "对感情失去期待，需要重拾信心",
            "career": "创意枯竭，对未来感到迷茫",
            "fortune": "财务信心不足，需重新建立"
        }
    },
    {
        "id": 18, "name_en": "The Moon", "name_zh": "月亮",
        "element": "水", "planet": "双鱼座",
        "keywords": ["幻觉", "恐惧", "潜意识", "迷茫", "直觉"],
        "upright": {
            "summary": "迷雾重重，需要依靠直觉穿越黑暗",
            "love": "暧昧不清的关系，需要时间和耐心",
            "career": "前路不明朗，谨慎行事",
            "fortune": "财务信息不清晰，不要做重大决策"
        },
        "reversed": {
            "summary": "迷雾散去，真相大白，恐惧被释放",
            "love": "误会澄清，真相浮出水面",
            "career": "逐渐看清方向，走出迷茫",
            "fortune": "财务隐患被发现并解决"
        }
    },
    {
        "id": 19, "name_en": "The Sun", "name_zh": "太阳",
        "element": "火", "planet": "太阳",
        "keywords": ["快乐", "成功", "活力", "生命", "光明"],
        "upright": {
            "summary": "阳光普照，一切美好都在发生，尽情享受吧",
            "love": "幸福的恋情，充满热情和快乐",
            "career": "事业如日中天，获得巨大成功",
            "fortune": "财运最佳时期，收入丰厚"
        },
        "reversed": {
            "summary": "快乐被遮挡，暂时看不到光明",
            "love": "热情减退，需要重新点燃激情",
            "career": "成功来迟，但仍可期待",
            "fortune": "短暂的财务阴影，但很快会过去"
        }
    },
    {
        "id": 20, "name_en": "Judgement", "name_zh": "审判",
        "element": "火", "planet": "冥王星",
        "keywords": ["觉醒", "重生", "召唤", "清算", "升华"],
        "upright": {
            "summary": "接受内心的召唤，迎接灵魂的觉醒与重生",
            "love": "旧情复燃，或感情得到升华",
            "career": "职业生涯的重要转折，追随内心的召唤",
            "fortune": "投资获得回报，财务进入新阶段"
        },
        "reversed": {
            "summary": "拒绝内心的召唤，逃避审判",
            "love": "无法放下过去，难以向前",
            "career": "逃避责任，错过改变的机会",
            "fortune": "不愿面对财务现实"
        }
    },
    {
        "id": 21, "name_en": "The World", "name_zh": "世界",
        "element": "土", "planet": "土星",
        "keywords": ["完成", "圆满", "达成", "旅程", "整合"],
        "upright": {
            "summary": "一个完整的循环画上句号，获得了圆满的成功",
            "love": "完美的恋爱关系，或修成正果",
            "career": "项目成功完成，达到事业的巅峰",
            "fortune": "财务目标达成，收获满满"
        },
        "reversed": {
            "summary": "接近完成但还有一步之遥，不要放弃",
            "love": "差一点就能圆满，需要最后的努力",
            "career": "事业接近成功但尚有欠缺",
            "fortune": "财务目标即将实现，坚持住"
        }
    }
]

MINOR_ARCANA_SUITS = {
    "wands": {"name_zh": "权杖", "element": "火", "domain": "行动、创造、事业"},
    "cups": {"name_zh": "圣杯", "element": "水", "domain": "情感、直觉、关系"},
    "swords": {"name_zh": "宝剑", "element": "风", "domain": "思想、冲突、真理"},
    "pentacles": {"name_zh": "星币", "element": "土", "domain": "物质、财富、健康"},
}

MINOR_ARCANA_RANKS = [
    {"rank": "ace", "name_zh": "王牌（ACE）", "meaning_prefix": "新的开始，纯粹的"},
    {"rank": "two", "name_zh": "二", "meaning_prefix": "二元对立与选择"},
    {"rank": "three", "name_zh": "三", "meaning_prefix": "初步的成果与成长"},
    {"rank": "four", "name_zh": "四", "meaning_prefix": "稳定与基础"},
    {"rank": "five", "name_zh": "五", "meaning_prefix": "冲突与挑战"},
    {"rank": "six", "name_zh": "六", "meaning_prefix": "恢复与和谐"},
    {"rank": "seven", "name_zh": "七", "meaning_prefix": "反思与评估"},
    {"rank": "eight", "name_zh": "八", "meaning_prefix": "行动与进展"},
    {"rank": "nine", "name_zh": "九", "meaning_prefix": "接近完成与满足"},
    {"rank": "ten", "name_zh": "十", "meaning_prefix": "完成与结果"},
    {"rank": "page", "name_zh": "侍从", "meaning_prefix": "学习与探索"},
    {"rank": "knight", "name_zh": "骑士", "meaning_prefix": "行动与追求"},
    {"rank": "queen", "name_zh": "皇后", "meaning_prefix": "内在掌控与滋养"},
    {"rank": "king", "name_zh": "国王", "meaning_prefix": "外在权威与掌握"},
]

# 小阿卡纳每张牌的详细释义
MINOR_ARCANA_MEANINGS = {
    "wands": {
        "ace": {"upright": "新的创意和行动力，激情点燃，事业新起点", "reversed": "计划受阻，缺乏动力，错失机会"},
        "two": {"upright": "规划未来，展望新方向，做出选择", "reversed": "犹豫不决，计划脱离实际"},
        "three": {"upright": "事业初显成效，团队合作顺利", "reversed": "成果不如预期，团队沟通不畅"},
        "four": {"upright": "庆祝成果，稳定和谐的环境", "reversed": "过度放松，忽视了持续的挑战"},
        "five": {"upright": "激烈的竞争和冲突，需要坚持立场", "reversed": "避免冲突，妥协求和"},
        "six": {"upright": "胜利与认可，好消息传来", "reversed": "失败或认可被推迟"},
        "seven": {"upright": "坚守立场，面对挑战保持勇气", "reversed": "退缩放弃，不敌压力"},
        "eight": {"upright": "消息快速传来，事情进展加快", "reversed": "计划受阻，进展缓慢"},
        "nine": {"upright": "接近完成时的坚持，积累经验", "reversed": "疲惫不堪，想要放弃"},
        "ten": {"upright": "负担沉重，但收获在望", "reversed": "压力过大无法承受"},
        "page": {"upright": "充满热情的学习者，好消息传来", "reversed": "缺乏方向感，热情消退"},
        "knight": {"upright": "充满激情和行动力，追求目标", "reversed": "冲动鲁莽，三分钟热度"},
        "queen": {"upright": "自信、热情、有魅力的领导者", "reversed": "过于强势，嫉妒心重"},
        "king": {"upright": "远见卓识的领导者，事业有成", "reversed": "独断专行，期望过高"}
    },
    "cups": {
        "ace": {"upright": "新的感情或情感开始，爱意涌现", "reversed": "情感空虚，爱意枯竭"},
        "two": {"upright": "两情相悦，灵魂伴侣的联结", "reversed": "感情破裂，信任危机"},
        "three": {"upright": "友情欢乐，庆祝与分享", "reversed": "过度放纵，友谊变味"},
        "four": {"upright": "对现状不满，寻找更深的意义", "reversed": "重新找到满足感"},
        "five": {"upright": "失去与悲伤，但仍有希望", "reversed": "走出悲伤，重拾希望"},
        "six": {"upright": "美好的回忆，纯真的快乐", "reversed": "活在过去，不愿面对现实"},
        "seven": {"upright": "幻想与选择，需要做出抉择", "reversed": "做出决定，不再迷茫"},
        "eight": {"upright": "放下过去，走出舒适圈", "reversed": "犹豫不决，害怕改变"},
        "nine": {"upright": "愿望成真，情感满足", "reversed": "愿望落空，内心空虚"},
        "ten": {"upright": "家庭幸福，情感圆满", "reversed": "家庭不睦，情感破裂"},
        "page": {"upright": "温柔敏感，创意灵感涌现", "reversed": "情感不成熟，过于敏感"},
        "knight": {"upright": "浪漫的追求者，为爱付出", "reversed": "情绪化，不够真诚"},
        "queen": {"upright": "情感丰富、富有同理心的女性形象", "reversed": "过度依赖情感，缺乏理性"},
        "king": {"upright": "情感成熟稳重，值得信赖", "reversed": "情感压抑，无法表达真实感受"}
    },
    "swords": {
        "ace": {"upright": "清晰的思维，真理在握，新的洞见", "reversed": "思维混乱，错误的判断"},
        "two": {"upright": "两难的选择，需要权衡利弊", "reversed": "做出选择，但可能后悔"},
        "three": {"upright": "心碎与悲伤，情感上的伤痛", "reversed": "走出伤痛，开始疗愈"},
        "four": {"upright": "休息与恢复，暂时退避", "reversed": "恢复完毕，准备重新出发"},
        "five": {"upright": "冲突与争斗，胜利但代价高昂", "reversed": "和解妥协，但心存不甘"},
        "six": {"upright": "渡过难关，向前迈进", "reversed": "停滞不前，无法放下"},
        "seven": {"upright": "暗中行动，投机取巧", "reversed": "阴谋败露，回心转意"},
        "eight": {"upright": "困在思维的牢笼中，自我设限", "reversed": "释放自己，冲破思维的束缚"},
        "nine": {"upright": "焦虑与噩梦，过度的担忧", "reversed": "从焦虑中解脱，重获平静"},
        "ten": {"upright": "结局已定，彻底的结束", "reversed": "重生在即，黑暗即将过去"},
        "page": {"upright": "思维敏捷，好奇探索", "reversed": "言语冲动，缺乏深度思考"},
        "knight": {"upright": "果敢决断，为真理而战", "reversed": "鲁莽好斗，不计后果"},
        "queen": {"upright": "智慧理性，独立自主", "reversed": "冷漠刻薄，过于理性"},
        "king": {"upright": "公正严厉，思维清晰果断", "reversed": "独断专行，滥用权力"}
    },
    "pentacles": {
        "ace": {"upright": "新的财富机会，物质丰收的开端", "reversed": "错失财务良机，浪费资源"},
        "two": {"upright": "平衡财务，多任务处理", "reversed": "财务失衡，难以兼顾"},
        "three": {"upright": "团队合作，技艺精进", "reversed": "合作不顺，技能不足"},
        "four": {"upright": "牢牢掌握财富，但过于保守", "reversed": "消费过度，或放手投资"},
        "five": {"upright": "物质上的困难和缺乏", "reversed": "走出贫困，找到工作"},
        "six": {"upright": "慷慨分享，接受帮助", "reversed": "贪婪或拒绝接受帮助"},
        "seven": {"upright": "耐心等待成长，评估进展", "reversed": "缺乏耐心，投资失败"},
        "eight": {"upright": "辛勤工作，专注于技艺", "reversed": "枯燥重复，缺乏创意"},
        "nine": {"upright": "物质富足，独立自足", "reversed": "财务安全问题，过度依赖"},
        "ten": {"upright": "家族财富，长期的物质保障", "reversed": "家族纠纷，财产损失"},
        "page": {"upright": "务实好学，新的学习机会", "reversed": "拖延懒惰，缺乏上进心"},
        "knight": {"upright": "踏实的建设者，值得信赖", "reversed": "停滞不前，缺乏野心"},
        "queen": {"upright": "务实温柔，生活富足安稳", "reversed": "过度追求物质，忽视精神"},
        "king": {"upright": "财务成功，稳定可靠的领导者", "reversed": "贪婪固执，过于物质主义"}
    }
}

SPREADS = {
    "single": {
        "name": "单张牌占卜",
        "description": "抽出1张牌，快速获得今日指引",
        "cards_count": 1,
        "positions": ["今日指引"]
    },
    "three": {
        "name": "三张牌牌阵（过去·现在·未来）",
        "description": "经典的占卜阵法，揭示事情的来龙去脉",
        "cards_count": 3,
        "positions": ["过去", "现在", "未来"]
    },
    "celtic_cross": {
        "name": "凯尔特十字牌阵",
        "description": "最完整的占卜阵法，全面剖析问题的各个方面",
        "cards_count": 10,
        "positions": [
            "核心问题（现状）",
            "阻碍或助力（交叉）",
            "基础（过往根源）",
            "过去的影响",
            "可能的结果（目标）",
            "近未来",
            "你的态度",
            "外界环境",
            "希望与恐惧",
            "最终结果"
        ]
    },
    "relationship": {
        "name": "关系牌阵",
        "description": "深入了解人与人之间的关系动态",
        "cards_count": 5,
        "positions": [
            "你的状态",
            "对方的状态",
            "关系的现状",
            "关系的挑战",
            "关系的未来"
        ]
    },
    "horseshoe": {
        "name": "马蹄铁牌阵",
        "description": "揭示一件事从过去到未来的发展轨迹",
        "cards_count": 7,
        "positions": [
            "过去的根源",
            "当前的状况",
            "隐藏的影响",
            "面临的障碍",
            "外界的态度",
            "你的建议",
            "最终结果"
        ]
    }
}
