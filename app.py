import random
from datetime import datetime

import pandas as pd
import streamlit as st


DATA_FILE = "readings.csv"


st.set_page_config(
    page_title="Yuki Cards",
    page_icon="❄️",
    layout="centered",
)


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7fbff 0%, #eef5ff 100%);
        color: #2c3e55;
    }

    .main .block-container {
        max-width: 520px;
        padding-top: 24px;
        padding-bottom: 28px;
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        color: #23374f;
        margin-bottom: 4px;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #5d7594;
        margin-bottom: 18px;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #d9e6f5;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.96) !important;
        color: #243950 !important;
        border: 1px solid #c7d9ee !important;
        border-radius: 10px !important;
    }

    .stTextArea textarea::placeholder {
        color: #6b84a4 !important;
        opacity: 1 !important;
    }

    .result-card {
        background: #ffffff;
        border: 1px solid #d7e5f3;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    }

    .result-position {
        font-size: 14px;
        color: #5f7899;
        margin-bottom: 6px;
    }

    .result-name {
        font-size: 26px;
        font-weight: 800;
        color: #223a55;
        margin-bottom: 6px;
    }

    .result-keyword {
        font-size: 14px;
        color: #607a9c;
        margin-bottom: 8px;
    }

    .result-text {
        font-size: 15px;
        line-height: 1.8;
        color: #2f4a69;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


cards = [
    {
        "name": "雪夜",
        "keyword": "直觉、静默、内在感知",
        "love": "你现在可能被情绪和想象牵着走。先不要急着判断对方怎么想，真正需要看清的是：你自己到底在害怕失去什么。",
        "career": "事情还没有完全明朗，不适合马上做重大决定。先收集信息，给自己一点安静的观察时间。",
        "daily": "今天适合慢一点。不要逼自己立刻清醒，答案常在最安静的时候落下。",
    },
    {
        "name": "星星",
        "keyword": "修复、希望、温柔的未来",
        "love": "这张牌像是在说，你正在慢慢恢复。不是所有关系都能回到原点，但你会重新找回自己的光。",
        "career": "你可以开始相信长期积累的力量。眼前的小努力，会在之后连成线。",
        "daily": "今天适合做一点让自己重新有希望的小事，不用很大。",
    },
    {
        "name": "恋人",
        "keyword": "选择、关系、真实心意",
        "love": "你正在面对一个和关系有关的选择。重点不是对方选不选你，而是你有没有真正选择自己。",
        "career": "你可能需要在两个方向之间做取舍。不要只看哪个更安全，也要看哪个更接近你真实想要的生活。",
        "daily": "今天留意你真正想靠近的人和事。你的心会给你信号。",
    },
    {
        "name": "隐士",
        "keyword": "独处、内省、慢慢看清",
        "love": "这段时间你可能不适合追问答案。先把注意力收回来，独处不是失败，是恢复判断力。",
        "career": "适合深度学习、整理计划、独立完成任务。不要太被外界声音打乱。",
        "daily": "今天适合少说一点，多听听自己。",
    },
    {
        "name": "力量",
        "keyword": "温柔的勇气、自控、内在力量",
        "love": "你其实比自己以为的更能撑住。真正的力量不是不想念，而是想念的时候也不立刻伤害自己。",
        "career": "你有能力处理眼前的问题，但方式不一定要强硬。稳定比爆发更重要。",
        "daily": "今天的关键词是：温柔地坚持。",
    },
    {
        "name": "高塔",
        "keyword": "崩塌、真相、重新开始",
        "love": "有些东西已经不是靠忍耐就能维持的。痛苦可能来自崩塌，但崩塌也会让你看见真实。",
        "career": "原有计划可能被打断，但这不一定是坏事。它逼你重新检查根基。",
        "daily": "今天如果有什么不舒服的真相出现，先别逃。它可能是在帮你醒来。",
    },
    {
        "name": "节制",
        "keyword": "平衡、慢慢融合、恢复节奏",
        "love": "你不需要一下子放下，也不需要一下子回头。现在最重要的是恢复自己的节奏。",
        "career": "适合调整方法，而不是推翻全部。慢慢磨合会比强行推进更有效。",
        "daily": "今天适合把生活调回温和一点的频率。",
    },
    {
        "name": "女祭司",
        "keyword": "秘密、直觉、未说出口的答案",
        "love": "你其实已经感觉到一些答案了，只是还没准备好承认。不要急着从别人那里要确认。",
        "career": "适合观察、学习和等待时机。现在不是所有东西都要说出来。",
        "daily": "今天相信你心里很安静的那个声音。",
    },
    {
        "name": "太阳",
        "keyword": "明朗、能量、被照亮",
        "love": "你会慢慢从那段阴影里走出来。真正适合你的关系，不会一直让你猜。",
        "career": "事情有变清楚的趋势。适合展示自己、表达想法、争取机会。",
        "daily": "今天适合出门晒晒太阳，做一点让身体醒过来的事。",
    },
    {
        "name": "审判",
        "keyword": "觉醒、复盘、重新定义自己",
        "love": "你正在从过去关系里学到一些重要的东西。重点不是回到过去，而是带着新的自己往前走。",
        "career": "适合总结经验，重新规划方向。过去的经历不是浪费。",
        "daily": "今天可以问自己：我已经不想再重复什么？",
    },
    {
        "name": "命运之轮",
        "keyword": "变化、转折、流动",
        "love": "你现在可能很想抓住一个确定答案，但关系有时就是在变化里露出真相。别急着把一刻的情绪当成全部结局。",
        "career": "事情可能会出现转机。你需要保持开放，但也不要把所有希望都押在外部变化上。",
        "daily": "今天提醒你：变化不一定是坏事，它也可能是在把你带到新的位置。",
    },
    {
        "name": "愚者",
        "keyword": "新的开始、轻盈、未知",
        "love": "你不需要马上知道下一段路会去哪里。能重新开始，本身就是一种勇气。",
        "career": "适合尝试新方向，但不要完全没有准备。带着好奇心，也带着一点现实感。",
        "daily": "今天允许自己轻一点，不用把所有问题都想完。",
    },
    {
        "name": "世界",
        "keyword": "完成、闭环、走向下一章",
        "love": "有些故事未必有你想要的结尾，但它依然可以成为一个完整的章节。你正在慢慢走出那一页。",
        "career": "一个阶段可能快要完成。适合总结、整理成果，准备进入新的循环。",
        "daily": "今天适合给自己一点肯定：你已经走了很远。",
    },
    {
        "name": "倒吊人",
        "keyword": "暂停、换角度、等待",
        "love": "现在越急着要答案，越容易让自己更乱。暂停不是无能为力，而是在给自己换一个角度。",
        "career": "暂时卡住不代表失败。也许你需要换一种方法，而不是继续硬推。",
        "daily": "今天适合停一下。不是所有问题都要立刻解决。",
    },
    {
        "name": "魔术师",
        "keyword": "行动、创造、把想法变成现实",
        "love": "别把所有能量都放在猜对方身上。你还有很多可以重新创造自己生活的能力。",
        "career": "适合开始行动。你已经有一些资源了，关键是把它们组织起来。",
        "daily": "今天做一件具体的小事，把想法落到现实里。",
    },
]


def interpret_card(card, topic):
    if topic == "感情":
        return card["love"]
    if topic == "学业 / 事业":
        return card["career"]
    if topic == "今日指引":
        return card["daily"]
    return random.choice([card["love"], card["career"], card["daily"]])


def save_reading(question, topic, spread, result_text):
    new_row = {
        "日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "问题": question,
        "主题": topic,
        "牌阵": spread,
        "结果": result_text,
    }

    try:
        old_data = pd.read_csv(DATA_FILE)
        data = pd.concat([old_data, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        data = pd.DataFrame([new_row])

    data.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def render_result_card(position, name, keyword, text):
    html = f"""
    <div class="result-card">
        <div class="result-position">{position}</div>
        <div class="result-name">「{name}」</div>
        <div class="result-keyword">{keyword}</div>
        <div class="result-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


st.markdown('<div class="title">❄️ Yuki Cards</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">当心里没有答案时，等一片雪花落下</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="panel">', unsafe_allow_html=True)

question = st.text_area(
    "先把你想问的问题写下来",
    placeholder="例如：我和他还有可能吗？/ 我最近的实习方向怎么样？/ 今天我需要注意什么？",
    height=120,
    key="question_input_primary",
)

topic = st.radio(
    "你想问哪一类？",
    ["感情", "学业 / 事业", "今日指引", "随机"],
    horizontal=True,
    key="topic_radio_primary",
)

spread = st.radio(
    "选择牌阵",
    ["一张牌", "三张牌"],
    horizontal=True,
    key="spread_radio_primary",
)

st.markdown('</div>', unsafe_allow_html=True)

draw_clicked = st.button("❄️ 等一片雪花落下", use_container_width=True, key="draw_button_primary")

if draw_clicked:
    if not question.strip():
        st.warning("先写一个你想问的问题。")
    else:
        if spread == "一张牌":
            selected_cards = random.sample(cards, 1)
        else:
            selected_cards = random.sample(cards, 3)

        result_parts = []
        st.markdown("### 给你的牌")

        if spread == "一张牌":
            card = selected_cards[0]
            text = interpret_card(card, topic)
            render_result_card("给你的雪牌", card["name"], card["keyword"], text)
            result_parts.append(f"你抽到了「{card['name']}」｜{card['keyword']}。\n{text}")
        else:
            positions = ["过去的雪痕", "此刻的雪面", "即将落下的雪"]
            for position, card in zip(positions, selected_cards):
                text = interpret_card(card, topic)
                render_result_card(position, card["name"], card["keyword"], text)
                result_parts.append(f"{position}：{card['name']}｜{card['keyword']}。{text}")

        closing_messages = [
            "答案不一定在别人那里，也可能正在你慢慢安静下来的心里。",
            "这次抽牌不替你决定，只提醒你：别在情绪最重的时候伤害自己。",
            "你可以慢一点。很多事情不是今天必须想明白。",
            "如果你现在很乱，先不要做决定。先喝水，洗脸，把自己带回现实。",
            "你不是没有方向，你只是还在从一段消耗里恢复。",
            "今天先不要追着答案跑。先把自己照顾好。",
            "有些事还没有答案，但你可以先站回自己这一边。",
        ]
        closing = random.choice(closing_messages)
        st.info(f"最后一句提醒：{closing}")

        full_result = "\n".join(result_parts) + "\n最后一句话：" + closing
        save_reading(question, topic, spread, full_result)
        st.caption("已保存到本地占卜记录。")


with st.expander("查看占卜记录", expanded=False):
    try:
        data = pd.read_csv(DATA_FILE)
        st.dataframe(data[["日期", "主题", "牌阵", "问题"]], use_container_width=True)
    except FileNotFoundError:
        st.info("还没有占卜记录。")
import random
from datetime import datetime

import pandas as pd
import streamlit as st


DATA_FILE = "readings.csv"

st.set_page_config(
    page_title="Yuki Cards",
    page_icon="❄️",
    layout="centered"
)

# ---------- CSS ----------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(255, 255, 255, 0.86) 0%, rgba(255, 255, 255, 0) 38%),
            linear-gradient(180deg, #fcfeff 0%, #eef5ff 55%, #ecebff 100%);
        color: #2d4360;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 520px;
        padding-top: 26px;
        padding-bottom: 34px;
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 4px;
        color: #22354d;
    }

    .subtitle {
        text-align: center;
        color: #5c7392;
        font-size: 16px;
        margin-bottom: 18px;
    }

    .soft-note {
        padding: 14px 16px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.74);
        border: 1px solid rgba(177, 203, 232, 0.52);
        box-shadow: 0 8px 22px rgba(76, 105, 148, 0.10);
        color: #34506d;
        line-height: 1.75;
        margin-bottom: 16px;
        font-size: 14px;
    }

    .input-shell {
        padding: 18px 16px 14px 16px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.68);
        border: 1px solid rgba(171, 198, 228, 0.55);
        box-shadow: 0 12px 30px rgba(67, 96, 138, 0.12);
        margin-bottom: 12px;
    }

    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stTextArea label,
    .stRadio label,
    .stCaption,
    p,
    span,
    div {
        color: #2d4360;
    }

    .stTextArea textarea {
        min-height: 128px;
        color: #243a54 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(153, 184, 218, 0.56) !important;
        border-radius: 12px !important;
        line-height: 1.65 !important;
    }

    .stTextArea textarea:focus {
        border: 1px solid rgba(120, 160, 205, 0.78) !important;
        box-shadow: 0 0 0 0.12rem rgba(146, 184, 225, 0.28) !important;
    }

    .stTextArea textarea::placeholder {
        color: #647f9f !important;
        opacity: 1 !important;
    }

    div[role="radiogroup"] {
        color: #2d4360 !important;
    }

    .oracle-card {
        padding: 18px 16px 16px 16px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(173, 200, 229, 0.55);
        box-shadow: 0 10px 24px rgba(71, 102, 140, 0.12);
        margin-bottom: 16px;
    }

    .card-snow {
        text-align: center;
        color: #7b95b4;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .card-title {
        text-align: center;
        font-size: 15px;
        font-weight: 700;
        color: #5b7392;
        margin-bottom: 8px;
    }

    .card-name {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #223a56;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .card-keyword {
        text-align: center;
        font-size: 14px;
        color: #5d789b;
        margin-bottom: 14px;
    }

    .reading-text {
        font-size: 15px;
        line-height: 1.85;
        color: #2f4a69;
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(184, 210, 237, 0.58);
        border-radius: 12px;
        padding: 11px 12px;
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 8px;
        margin-bottom: 4px;
    }

    .stButton > button {
        min-width: 260px;
        border-radius: 999px;
        border: none;
        background: linear-gradient(135deg, #3f6186 0%, #6e8fb6 100%);
        color: #f7fbff;
        font-size: 17px;
        font-weight: 700;
        padding: 12px 20px;
        box-shadow: 0 10px 24px rgba(58, 92, 132, 0.24);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(58, 92, 132, 0.30);
    }

    .stButton > button:focus,
    .stButton > button:focus-visible {
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(145, 181, 220, 0.35);
    }

    .stAlert {
        border-radius: 14px;
    }

    .record-caption {
        text-align: center;
        color: #6f85a2;
        font-size: 13px;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- 标题 ----------
st.markdown('<div class="title">❄️ Yuki Cards</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">当心里没有答案时，等一片雪花落下</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="soft-note">
    这里不是用来预测命运的地方。<br>
    它只是一个轻量的小卡片工具：当你犹豫、想念、焦虑，或者只是需要一点安静的时候，抽一张牌给自己，
    像在冬夜里等一片雪花落下。
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- 卡牌数据 ----------
cards = [
    {
        "name": "雪夜",
        "keyword": "直觉、静默、内在感知",
        "love": "你现在可能被情绪和想象牵着走。先不要急着判断对方怎么想，真正需要看清的是：你自己到底在害怕失去什么。",
        "career": "事情还没有完全明朗，不适合马上做重大决定。先收集信息，给自己一点安静的观察时间。",
        "daily": "今天适合慢一点。不要逼自己立刻清醒，答案常在最安静的时候落下。"
    },
    {
        "name": "星星",
        "keyword": "修复、希望、温柔的未来",
        "love": "这张牌像是在说，你正在慢慢恢复。不是所有关系都能回到原点，但你会重新找回自己的光。",
        "career": "你可以开始相信长期积累的力量。眼前的小努力，会在之后连成线。",
        "daily": "今天适合做一点让自己重新有希望的小事，不用很大。"
    },
    {
        "name": "恋人",
        "keyword": "选择、关系、真实心意",
        "love": "你正在面对一个和关系有关的选择。重点不是对方选不选你，而是你有没有真正选择自己。",
        "career": "你可能需要在两个方向之间做取舍。不要只看哪个更安全，也要看哪个更接近你真实想要的生活。",
        "daily": "今天留意你真正想靠近的人和事。你的心会给你信号。"
    },
    {
        "name": "隐士",
        "keyword": "独处、内省、慢慢看清",
        "love": "这段时间你可能不适合追问答案。先把注意力收回来，独处不是失败，是恢复判断力。",
        "career": "适合深度学习、整理计划、独立完成任务。不要太被外界声音打乱。",
        "daily": "今天适合少说一点，多听听自己。"
    },
    {
        "name": "力量",
        "keyword": "温柔的勇气、自控、内在力量",
        "love": "你其实比自己以为的更能撑住。真正的力量不是不想念，而是想念的时候也不立刻伤害自己。",
        "career": "你有能力处理眼前的问题，但方式不一定要强硬。稳定比爆发更重要。",
        "daily": "今天的关键词是：温柔地坚持。"
    },
    {
        "name": "高塔",
        "keyword": "崩塌、真相、重新开始",
        "love": "有些东西已经不是靠忍耐就能维持的。痛苦可能来自崩塌，但崩塌也会让你看见真实。",
        "career": "原有计划可能被打断，但这不一定是坏事。它逼你重新检查根基。",
        "daily": "今天如果有什么不舒服的真相出现，先别逃。它可能是在帮你醒来。"
    },
    {
        "name": "节制",
        "keyword": "平衡、慢慢融合、恢复节奏",
        "love": "你不需要一下子放下，也不需要一下子回头。现在最重要的是恢复自己的节奏。",
        "career": "适合调整方法，而不是推翻全部。慢慢磨合会比强行推进更有效。",
        "daily": "今天适合把生活调回温和一点的频率。"
    },
    {
        "name": "女祭司",
        "keyword": "秘密、直觉、未说出口的答案",
        "love": "你其实已经感觉到一些答案了，只是还没准备好承认。不要急着从别人那里要确认。",
        "career": "适合观察、学习和等待时机。现在不是所有东西都要说出来。",
        "daily": "今天相信你心里很安静的那个声音。"
    },
    {
        "name": "太阳",
        "keyword": "明朗、能量、被照亮",
        "love": "你会慢慢从那段阴影里走出来。真正适合你的关系，不会一直让你猜。",
        "career": "事情有变清楚的趋势。适合展示自己、表达想法、争取机会。",
        "daily": "今天适合出门晒晒太阳，做一点让身体醒过来的事。"
    },
    {
        "name": "审判",
        "keyword": "觉醒、复盘、重新定义自己",
        "love": "你正在从过去关系里学到一些重要的东西。重点不是回到过去，而是带着新的自己往前走。",
        "career": "适合总结经验，重新规划方向。过去的经历不是浪费。",
        "daily": "今天可以问自己：我已经不想再重复什么？"
    },
    {
        "name": "命运之轮",
        "keyword": "变化、转折、流动",
        "love": "你现在可能很想抓住一个确定答案，但关系有时就是在变化里露出真相。别急着把一刻的情绪当成全部结局。",
        "career": "事情可能会出现转机。你需要保持开放，但也不要把所有希望都押在外部变化上。",
        "daily": "今天提醒你：变化不一定是坏事，它也可能是在把你带到新的位置。"
    },
    {
        "name": "愚者",
        "keyword": "新的开始、轻盈、未知",
        "love": "你不需要马上知道下一段路会去哪里。能重新开始，本身就是一种勇气。",
        "career": "适合尝试新方向，但不要完全没有准备。带着好奇心，也带着一点现实感。",
        "daily": "今天允许自己轻一点，不用把所有问题都想完。"
    },
    {
        "name": "世界",
        "keyword": "完成、闭环、走向下一章",
        "love": "有些故事未必有你想要的结尾，但它依然可以成为一个完整的章节。你正在慢慢走出那一页。",
        "career": "一个阶段可能快要完成。适合总结、整理成果，准备进入新的循环。",
        "daily": "今天适合给自己一点肯定：你已经走了很远。"
    },
    {
        "name": "倒吊人",
        "keyword": "暂停、换角度、等待",
        "love": "现在越急着要答案，越容易让自己更乱。暂停不是无能为力，而是在给自己换一个角度。",
        "career": "暂时卡住不代表失败。也许你需要换一种方法，而不是继续硬推。",
        "daily": "今天适合停一下。不是所有问题都要立刻解决。"
    },
    {
        "name": "魔术师",
        "keyword": "行动、创造、把想法变成现实",
        "love": "别把所有能量都放在猜对方身上。你还有很多可以重新创造自己生活的能力。",
        "career": "适合开始行动。你已经有一些资源了，关键是把它们组织起来。",
        "daily": "今天做一件具体的小事，把想法落到现实里。"
    },
]


# ---------- 工具函数 ----------
def interpret_card(card, topic):
    if topic == "感情":
        return card["love"]
    if topic == "学业 / 事业":
        return card["career"]
    if topic == "今日指引":
        return card["daily"]
    return random.choice([card["love"], card["career"], card["daily"]])


def save_reading(question, topic, spread, result_text):
    new_row = {
        "日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "问题": question,
        "主题": topic,
        "牌阵": spread,
        "结果": result_text
    }

    try:
        old_data = pd.read_csv(DATA_FILE)
        data = pd.concat([old_data, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        data = pd.DataFrame([new_row])

    data.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def render_card(position, card_name, keyword, text):
    html = f"""
    <div class="oracle-card">
        <div class="card-snow">✦ ❄ ✦</div>
        <div class="card-title">{position}</div>
        <div class="card-name">「{card_name}」</div>
        <div class="card-keyword">{keyword}</div>
        <div class="reading-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ---------- 输入区 ----------
st.markdown('<div class="input-shell">', unsafe_allow_html=True)

question = st.text_area(
    "先把你想问的问题写下来",
    placeholder="例如：我和他还有可能吗？/ 我最近的实习方向怎么样？/ 今天我需要注意什么？",
    height=128,
    key="question_input"
)

topic = st.radio(
    "你想问哪一类？",
    ["感情", "学业 / 事业", "今日指引", "随机"],
    horizontal=True,
    key="topic_radio"
)

spread = st.radio(
    "选择牌阵",
    ["一张牌", "三张牌"],
    horizontal=True,
    key="spread_radio"
)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- 抽牌 ----------
button_col_left, button_col_mid, button_col_right = st.columns([1, 4, 1])
with button_col_mid:
    draw_clicked = st.button("❄️ 等一片雪花落下", use_container_width=True, key="draw_button")

if draw_clicked:
    if not question.strip():
        st.warning("先写一个你想问的问题。")
    else:
        if spread == "一张牌":
            selected_cards = random.sample(cards, 1)
        else:
            selected_cards = random.sample(cards, 3)

        result_parts = []

        st.markdown("## 给你的牌")

        if spread == "一张牌":
            card = selected_cards[0]
            text = interpret_card(card, topic)

            render_card(
                position="给你的雪牌",
                card_name=card["name"],
                keyword=card["keyword"],
                text=text
            )

            final_text = f"你抽到了「{card['name']}」｜{card['keyword']}。\n{text}"
            result_parts.append(final_text)

        else:
            positions = ["过去的雪痕", "此刻的雪面", "即将落下的雪"]

            for position, card in zip(positions, selected_cards):
                text = interpret_card(card, topic)

                render_card(
                    position=position,
                    card_name=card["name"],
                    keyword=card["keyword"],
                    text=text
                )

                result_parts.append(
                    f"{position}：{card['name']}｜{card['keyword']}。{text}"
                )

        # 总结
        st.markdown("### Yuki 给你的最后一句话")

        closing_messages = [
            "答案不一定在别人那里，也可能正在你慢慢安静下来的心里。",
            "这次抽牌不替你决定，只提醒你：别在情绪最重的时候伤害自己。",
            "你可以慢一点。很多事情不是今天必须想明白。",
            "如果你现在很乱，先不要做决定。先喝水，洗脸，把自己带回现实。",
            "你不是没有方向，你只是还在从一段消耗里恢复。",
            "今天先不要追着答案跑。先把自己照顾好。",
            "有些事还没有答案，但你可以先站回自己这一边。"
        ]

        closing = random.choice(closing_messages)
        st.success(closing)

        full_result = "\n".join(result_parts) + "\n最后一句话：" + closing
        save_reading(question, topic, spread, full_result)

        st.markdown('<div class="record-caption">已保存到本地占卜记录。</div>', unsafe_allow_html=True)

st.divider()

# ---------- 历史记录 ----------
with st.expander("查看占卜记录", expanded=False):
    try:
        data = pd.read_csv(DATA_FILE)
        st.dataframe(data[["日期", "主题", "牌阵", "问题"]], use_container_width=True)
    except FileNotFoundError:
        st.info("还没有占卜记录。")