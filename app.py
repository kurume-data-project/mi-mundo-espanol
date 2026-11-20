
import random
import html
import streamlit as st

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="centered"
)

# =====================================
# 問題・マインドマップデータ
# =====================================

QUESTIONS = [
    {
        "title": "En una cafetería",
        "level": "A1",
        "icon": "☕",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
        "words": [
            {"es": "la mesa", "ja": "テーブル", "correct": True},
            {"es": "la silla", "ja": "椅子", "correct": True},
            {"es": "el café", "ja": "コーヒー", "correct": True},
            {"es": "el avión", "ja": "飛行機", "correct": False},
            {"es": "el hospital", "ja": "病院", "correct": False},
        ],
        "mindmap": [
            {
                "category": "Comida y bebida",
                "ja": "食べ物・飲み物",
                "icon": "🥐",
                "color": "#F6C66B",
                "words": [
                    ("el té", "お茶"),
                    ("la leche", "牛乳"),
                    ("el azúcar", "砂糖"),
                    ("el agua", "水"),
                    ("el zumo", "ジュース"),
                ]
            },
            {
                "category": "Personas y lugares",
                "ja": "人・お店",
                "icon": "🧑‍🍳",
                "color": "#80C6A5",
                "words": [
                    ("el camarero", "ウェイター"),
                    ("la camarera", "ウェイトレス"),
                    ("el cliente", "お客さん"),
                    ("la cafetería", "カフェ"),
                    ("el menú", "メニュー"),
                ]
            },
            {
                "category": "Utensilios",
                "ja": "食器・道具",
                "icon": "🍽️",
                "color": "#85B8E8",
                "words": [
                    ("la taza", "カップ"),
                    ("el vaso", "グラス"),
                    ("la cuchara", "スプーン"),
                    ("el tenedor", "フォーク"),
                    ("el plato", "皿"),
                ]
            },
            {
                "category": "Acciones",
                "ja": "行動・その他",
                "icon": "💬",
                "color": "#D6A0D8",
                "words": [
                    ("pedir", "注文する"),
                    ("pagar", "支払う"),
                    ("la cuenta", "お会計"),
                    ("desayunar", "朝食をとる"),
                    ("la propina", "チップ"),
                ]
            }
        ]
    },
    {
        "title": "En la playa",
        "level": "A1",
        "icon": "🏖️",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
        "words": [
            {"es": "el mar", "ja": "海", "correct": True},
            {"es": "la playa", "ja": "ビーチ", "correct": True},
            {"es": "el sol", "ja": "太陽", "correct": True},
            {"es": "el tren", "ja": "電車", "correct": False},
            {"es": "la oficina", "ja": "オフィス", "correct": False},
        ],
        "mindmap": [
            {
                "category": "Animales marinos",
                "ja": "海の生き物",
                "icon": "🐬",
                "color": "#85B8E8",
                "words": [
                    ("el pez", "魚"),
                    ("el delfín", "イルカ"),
                    ("la tortuga", "カメ"),
                    ("el tiburón", "サメ"),
                    ("la medusa", "クラゲ"),
                ]
            },
            {
                "category": "Objetos",
                "ja": "持ち物",
                "icon": "🕶️",
                "color": "#F6C66B",
                "words": [
                    ("la toalla", "タオル"),
                    ("el bañador", "水着"),
                    ("las gafas de sol", "サングラス"),
                    ("la sombrilla", "パラソル"),
                    ("la crema solar", "日焼け止め"),
                ]
            },
            {
                "category": "Naturaleza",
                "ja": "自然・天気",
                "icon": "🌤️",
                "color": "#80C6A5",
                "words": [
                    ("la arena", "砂"),
                    ("la ola", "波"),
                    ("el viento", "風"),
                    ("la nube", "雲"),
                    ("la lluvia", "雨"),
                ]
            },
            {
                "category": "Acciones",
                "ja": "行動",
                "icon": "🏊",
                "color": "#D6A0D8",
                "words": [
                    ("nadar", "泳ぐ"),
                    ("bucear", "潜る"),
                    ("tomar el sol", "日光浴する"),
                    ("jugar", "遊ぶ"),
                    ("descansar", "休む"),
                ]
            }
        ]
    },
    {
        "title": "En el mercado",
        "level": "A2",
        "icon": "🛒",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            {"es": "la fruta", "ja": "果物", "correct": True},
            {"es": "la verdura", "ja": "野菜", "correct": True},
            {"es": "el vendedor", "ja": "販売員", "correct": True},
            {"es": "el ordenador", "ja": "パソコン", "correct": False},
            {"es": "el aeropuerto", "ja": "空港", "correct": False},
        ],
        "mindmap": [
            {
                "category": "Frutas",
                "ja": "果物",
                "icon": "🍎",
                "color": "#F6C66B",
                "words": [
                    ("la manzana", "りんご"),
                    ("el plátano", "バナナ"),
                    ("la naranja", "オレンジ"),
                    ("la fresa", "いちご"),
                    ("la uva", "ぶどう"),
                ]
            },
            {
                "category": "Verduras",
                "ja": "野菜",
                "icon": "🥕",
                "color": "#80C6A5",
                "words": [
                    ("la cebolla", "たまねぎ"),
                    ("la zanahoria", "にんじん"),
                    ("el tomate", "トマト"),
                    ("la patata", "じゃがいも"),
                    ("el pepino", "きゅうり"),
                ]
            },
            {
                "category": "Compras",
                "ja": "買い物",
                "icon": "🛍️",
                "color": "#85B8E8",
                "words": [
                    ("el precio", "価格"),
                    ("el dinero", "お金"),
                    ("la bolsa", "袋"),
                    ("el kilo", "キログラム"),
                    ("el descuento", "割引"),
                ]
            },
            {
                "category": "Acciones",
                "ja": "行動・その他",
                "icon": "🤝",
                "color": "#D6A0D8",
                "words": [
                    ("comprar", "買う"),
                    ("vender", "売る"),
                    ("elegir", "選ぶ"),
                    ("pesar", "重さを量る"),
                    ("fresco", "新鮮な"),
                ]
            }
        ]
    }
]


# =====================================
# マインドマップ表示
# =====================================

def show_mindmap(question):

    st.markdown("""
    <style>
    .mindmap {
        background: #FFFDF7;
        padding: 18px;
        border-radius: 20px;
        border: 1px solid #E8DFC9;
        color: #344054;
    }

    .mind-center {
        background: #245C83;
        color: white;
        border-radius: 18px;
        padding: 20px 10px;
        text-align: center;
        margin: 0 auto;
        max-width: 270px;
        box-shadow: 0 4px 10px #00000018;
    }

    .mind-center .emoji {
        font-size: 48px;
    }

    .mind-center .title {
        font-size: 21px;
        font-weight: bold;
    }

    .mind-connector {
        width: 3px;
        height: 28px;
        background: #B9B4A7;
        margin: auto;
    }

    .mind-branches {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        position: relative;
    }

    .mind-card {
        background: white;
        border-radius: 14px;
        padding: 12px;
        border: 1px solid #E6E2D8;
        border-top: 5px solid var(--branch-color);
        box-shadow: 0 2px 7px #0000000D;
        min-width: 0;
    }

    .mind-category {
        font-size: 13px;
        font-weight: bold;
        color: #344054;
        margin-bottom: 3px;
    }

    .mind-category-icon {
        font-size: 27px;
    }

    .mind-category-ja {
        font-size: 11px;
        color: #777777;
        margin-bottom: 10px;
    }

    .mind-word {
        border-left: 2px solid var(--branch-color);
        padding: 4px 5px;
        margin: 5px 0;
        background: #FAFAF8;
        border-radius: 4px;
    }

    .mind-es {
        font-size: 13px;
        font-weight: bold;
        color: #245C83;
        overflow-wrap: anywhere;
    }

    .mind-ja {
        font-size: 11px;
        color: #777777;
    }

    .mind-footer {
        text-align: center;
        color: #777777;
        font-size: 12px;
        padding-top: 15px;
    }

    @media (max-width: 480px) {
        .mindmap {
            padding: 10px;
        }
        .mind-branches {
            gap: 8px;
        }
        .mind-card {
            padding: 8px;
        }
        .mind-es {
            font-size: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    title = html.escape(question["title"])
    icon = html.escape(question["icon"])

    content = f"""
    <div class="mindmap">
      <div class="mind-center">
        <div class="emoji">{icon}</div>
        <div class="title">{title}</div>
        <div>Mi vocabulario</div>
      </div>
      <div class="mind-connector"></div>
      <div class="mind-branches">
    """

    for category in question["mindmap"]:
        color = html.escape(category["color"])
        cat_icon = html.escape(category["icon"])
        cat_name = html.escape(category["category"])
        cat_ja = html.escape(category["ja"])

        content += f"""
        <div class="mind-card" style="--branch-color:{color}">
          <div class="mind-category-icon">{cat_icon}</div>
          <div class="mind-category">{cat_name}</div>
          <div class="mind-category-ja">{cat_ja}</div>
        """

        for es, ja in category["words"]:
            es = html.escape(es)
            ja = html.escape(ja)

            content += f"""
            <div class="mind-word">
              <div class="mind-es">{es}</div>
              <div class="mind-ja">{ja}</div>
            </div>
            """

        content += "</div>"

    content += """
      </div>
      <div class="mind-footer">
        Aprende nuevas palabras cada día 🇪🇸
      </div>
    </div>
    """

    st.markdown(content, unsafe_allow_html=True)


# =====================================
# セッション状態
# =====================================

if "q_index" not in st.session_state:
    st.session_state.q_index = random.randrange(len(QUESTIONS))
    st.session_state.round_id = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.order = random.sample(range(5), 5)
    st.session_state.is_correct = False


def next_question():
    previous = st.session_state.q_index
    candidates = [
        i for i in range(len(QUESTIONS))
        if i != previous
    ]

    st.session_state.q_index = random.choice(candidates)
    st.session_state.round_id += 1
    st.session_state.order = random.sample(range(5), 5)
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.is_correct = False


# =====================================
# メイン画面
# =====================================

q = QUESTIONS[st.session_state.q_index]

st.title("🇪🇸 Mi Mundo Español")
st.caption("写真からスペイン語の世界を広げよう！")

col1, col2 = st.columns(2)
col1.metric("レベル", q["level"])
col2.metric("正解数", st.session_state.score)

st.subheader(q["title"])
st.image(q["photo"], use_container_width=True)


# =====================================
# クイズ
# =====================================

if not st.session_state.answered:

    st.markdown("### 写真に関係する単語を3つ選んでください")
    st.info("スペイン語だけを見て考えましょう！")

    with st.form(key=f"quiz_{st.session_state.round_id}"):

        choices = {}

        for i in st.session_state.order:
            word = q["words"][i]

            choices[i] = st.checkbox(
                word["es"],
                key=f"choice_{st.session_state.round_id}_{i}"
            )

        submitted = st.form_submit_button(
            "答え合わせ",
            use_container_width=True
        )

    if submitted:
        selected = [
            i for i, value in choices.items() if value
        ]

        if len(selected) != 3:
            st.warning("3つ選択してください。")
        else:
            correct = [
                i for i, word in enumerate(q["words"])
                if word["correct"]
            ]

            st.session_state.selected = selected
            st.session_state.is_correct = (
                set(selected) == set(correct)
            )
            st.session_state.answered = True

            if st.session_state.is_correct:
                st.session_state.score += 1

            st.rerun()


# =====================================
# 答え合わせ・マインドマップ
# =====================================

if st.session_state.answered:

    st.divider()
    st.header("📝 答え合わせ")

    if st.session_state.is_correct:
        st.success("¡Muy bien! 全問正解です！")
    else:
        st.warning("正解を確認して、覚えましょう！")

    for i in st.session_state.order:
        word = q["words"][i]

        if word["correct"]:
            st.success(f"✓ {word['es']} ＝ {word['ja']}")
        else:
            st.write(f"✕ {word['es']} ＝ {word['ja']}")

    st.divider()

    st.header("🌍 イラスト型マインドマップ")

    st.write(
        "写真に写っていない言葉も含めて、"
        "関連する単語を広げて覚えましょう。"
    )

    show_mindmap(q)

    total_words = sum(
        len(category["words"])
        for category in q["mindmap"]
    )

    st.success(
        f"今回の追加語彙は {total_words} 語です！"
    )

    st.divider()

    st.header("✍️ 書き写して覚えよう")

    st.markdown("""
    1. マインドマップを見ながらスペイン語を書く
    2. 日本語の意味を確認する
    3. 日本語を隠してスペイン語を思い出す
    4. 声に出して発音する
    """)

    if st.button(
        "次の問題へ →",
        use_container_width=True
    ):
        next_question()
        st.rerun()


st.divider()
st.caption("Mi Mundo Español | Aprende español cada día")
