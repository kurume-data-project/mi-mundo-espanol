
import html
import random
import streamlit as st


# ==========================================
# Mi Mundo Español
# ==========================================

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="wide"
)

# ==========================================
# 問題・語彙データ
# 各問題：6カテゴリー × 5語 = 30語
# ==========================================

QUESTIONS = [
    {
        "title": "En una cafetería",
        "level": "A1",
        "icon": "☕",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
        "words": [
            ("la mesa", "テーブル", True),
            ("la silla", "椅子", True),
            ("el café", "コーヒー", True),
            ("el avión", "飛行機", False),
            ("el hospital", "病院", False),
        ],
        "categories": [
            ("Comida y bebida", "食べ物・飲み物", "🥐", "#45A7D5", [
                ("el té", "お茶"),
                ("la leche", "牛乳"),
                ("el azúcar", "砂糖"),
                ("el agua", "水"),
                ("el zumo", "ジュース"),
            ]),
            ("Personas", "人", "🧑‍🍳", "#E6B93F", [
                ("el camarero", "ウェイター"),
                ("la camarera", "ウェイトレス"),
                ("el cliente", "お客さん"),
                ("el cocinero", "料理人"),
                ("el amigo", "友人"),
            ]),
            ("Utensilios", "食器・道具", "🍽️", "#65B879", [
                ("la taza", "カップ"),
                ("el vaso", "グラス"),
                ("la cuchara", "スプーン"),
                ("el tenedor", "フォーク"),
                ("el plato", "皿"),
            ]),
            ("Lugares", "場所", "🏠", "#D77BB3", [
                ("la cafetería", "カフェ"),
                ("la terraza", "テラス"),
                ("la cocina", "台所"),
                ("el restaurante", "レストラン"),
                ("el baño", "トイレ"),
            ]),
            ("Acciones", "行動", "💬", "#A47ACD", [
                ("pedir", "注文する"),
                ("pagar", "支払う"),
                ("desayunar", "朝食をとる"),
                ("comer", "食べる"),
                ("beber", "飲む"),
            ]),
            ("Otras palabras", "その他", "🧾", "#E58B55", [
                ("la cuenta", "お会計"),
                ("el menú", "メニュー"),
                ("el precio", "価格"),
                ("la propina", "チップ"),
                ("la mañana", "朝"),
            ]),
        ],
    },
    {
        "title": "En la playa",
        "level": "A1",
        "icon": "🏖️",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
        "words": [
            ("el mar", "海", True),
            ("la playa", "ビーチ", True),
            ("el sol", "太陽", True),
            ("el tren", "電車", False),
            ("la oficina", "オフィス", False),
        ],
        "categories": [
            ("Animales marinos", "海の生き物", "🐬", "#45A7D5", [
                ("el pez", "魚"),
                ("el delfín", "イルカ"),
                ("la tortuga", "カメ"),
                ("el tiburón", "サメ"),
                ("la medusa", "クラゲ"),
            ]),
            ("Objetos", "持ち物", "🕶️", "#E6B93F", [
                ("la toalla", "タオル"),
                ("el bañador", "水着"),
                ("las gafas de sol", "サングラス"),
                ("la sombrilla", "パラソル"),
                ("la crema solar", "日焼け止め"),
            ]),
            ("Naturaleza", "自然", "🌴", "#65B879", [
                ("la arena", "砂"),
                ("la ola", "波"),
                ("el viento", "風"),
                ("la nube", "雲"),
                ("la palmera", "ヤシの木"),
            ]),
            ("Tiempo", "天気", "🌤️", "#D77BB3", [
                ("el calor", "暑さ"),
                ("el frío", "寒さ"),
                ("el cielo", "空"),
                ("la lluvia", "雨"),
                ("la temperatura", "気温"),
            ]),
            ("Acciones", "行動", "🏊", "#A47ACD", [
                ("nadar", "泳ぐ"),
                ("bucear", "潜る"),
                ("tomar el sol", "日光浴する"),
                ("jugar", "遊ぶ"),
                ("descansar", "休む"),
            ]),
            ("Lugares y otros", "場所・その他", "⛱️", "#E58B55", [
                ("la piscina", "プール"),
                ("el paseo", "遊歩道"),
                ("el puerto", "港"),
                ("la isla", "島"),
                ("las vacaciones", "休暇"),
            ]),
        ],
    },
    {
        "title": "En el mercado",
        "level": "A2",
        "icon": "🛒",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            ("la fruta", "果物", True),
            ("la verdura", "野菜", True),
            ("el vendedor", "販売員", True),
            ("el ordenador", "パソコン", False),
            ("el aeropuerto", "空港", False),
        ],
        "categories": [
            ("Frutas", "果物", "🍎", "#45A7D5", [
                ("la manzana", "りんご"),
                ("el plátano", "バナナ"),
                ("la naranja", "オレンジ"),
                ("la fresa", "いちご"),
                ("la uva", "ぶどう"),
            ]),
            ("Verduras", "野菜", "🥕", "#E6B93F", [
                ("la cebolla", "たまねぎ"),
                ("la zanahoria", "にんじん"),
                ("el tomate", "トマト"),
                ("la patata", "じゃがいも"),
                ("el pepino", "きゅうり"),
            ]),
            ("Otros alimentos", "その他の食べ物", "🧀", "#65B879", [
                ("el queso", "チーズ"),
                ("el pan", "パン"),
                ("el arroz", "米"),
                ("el huevo", "卵"),
                ("la carne", "肉"),
            ]),
            ("Compras", "買い物", "🛍️", "#D77BB3", [
                ("el precio", "価格"),
                ("el dinero", "お金"),
                ("la bolsa", "袋"),
                ("el kilo", "キログラム"),
                ("el descuento", "割引"),
            ]),
            ("Acciones", "行動", "🤝", "#A47ACD", [
                ("comprar", "買う"),
                ("vender", "売る"),
                ("elegir", "選ぶ"),
                ("pesar", "重さを量る"),
                ("pagar", "支払う"),
            ]),
            ("Personas y lugares", "人・場所", "🏪", "#E58B55", [
                ("el vendedor", "販売員"),
                ("el cliente", "お客さん"),
                ("el mercado", "市場"),
                ("la tienda", "店"),
                ("el puesto", "売り場"),
            ]),
        ],
    },
]


# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #245C83;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        color: #777777;
        margin-top: 0;
        margin-bottom: 20px;
    }

    .instruction {
        background: #EDF5FC;
        border-left: 5px solid #398BC5;
        padding: 14px;
        border-radius: 8px;
        margin: 12px 0;
    }

    .mindmap {
        background: #FFFDF8;
        padding: 14px;
        border-radius: 18px;
        border: 1px solid #E5DFD2;
        font-family: sans-serif;
        color: #24344D;
        width: 100%;
        box-sizing: border-box;
    }

    .mind-center {
        background: #315D80;
        color: white;
        border-radius: 22px;
        padding: 15px;
        text-align: center;
        max-width: 520px;
        margin: 0 auto;
        box-shadow: 0 4px 12px #00000020;
    }

    .mind-center img {
        width: 100%;
        height: 190px;
        object-fit: cover;
        border-radius: 13px;
        display: block;
        margin-bottom: 10px;
    }

    .mind-center .emoji {
        font-size: 30px;
    }

    .mind-center .topic {
        font-size: 22px;
        font-weight: bold;
    }

    .mind-center .translation {
        font-size: 14px;
        margin-top: 4px;
    }

    .mind-connector {
        width: 4px;
        height: 28px;
        background: #A8B5C1;
        margin: 0 auto;
    }

    .branch-heading {
        text-align: center;
        color: #64748B;
        font-size: 12px;
        margin-bottom: 10px;
    }

    .branch-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }

    .branch-card {
        background: white;
        border: 1px solid #E7E4DC;
        border-top: 6px solid var(--branch-color);
        border-radius: 13px;
        padding: 12px;
        min-width: 0;
        box-sizing: border-box;
        box-shadow: 0 2px 5px #0000000A;
    }

    .branch-icon {
        font-size: 30px;
        text-align: center;
    }

    .branch-name {
        font-size: 15px;
        font-weight: bold;
        text-align: center;
        overflow-wrap: anywhere;
    }

    .branch-ja {
        font-size: 12px;
        text-align: center;
        color: #777777;
        margin-bottom: 8px;
    }

    .word-item {
        border-left: 3px solid var(--branch-color);
        background: #FAFAF8;
        border-radius: 5px;
        padding: 6px;
        margin-top: 6px;
        overflow-wrap: anywhere;
    }

    .word-es {
        font-size: 13px;
        font-weight: bold;
        color: #234C72;
    }

    .word-ja {
        font-size: 12px;
        color: #737373;
    }

    .mind-footer {
        text-align: center;
        font-size: 12px;
        color: #777777;
        padding-top: 15px;
    }

    @media (max-width: 650px) {
        .branch-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
        }

        .branch-card {
            padding: 9px;
        }

        .branch-name {
            font-size: 13px;
        }

        .word-es {
            font-size: 12px;
        }

        .word-ja {
            font-size: 11px;
        }

        .mind-center img {
            height: 150px;
        }
    }

    @media (max-width: 360px) {
        .branch-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# マインドマップ生成
# ==========================================

def show_mindmap(question):

    safe_title = html.escape(question["title"])
    safe_icon = html.escape(question["icon"])
    safe_photo = html.escape(question["photo"], quote=True)

    content = f"""
    <div class="mindmap">

        <div class="mind-center">
            <img src="{safe_photo}" alt="テーマの写真">
            <div class="emoji">{safe_icon}</div>
            <div class="topic">{safe_title}</div>
            <div class="translation">Mi mapa de vocabulario</div>
        </div>

        <div class="mind-connector"></div>
        <div class="branch-heading">
            関連する6つのカテゴリー・30語
        </div>

        <div class="branch-grid">
    """

    for category, category_ja, icon, color, words in question["categories"]:

        content += f"""
        <div class="branch-card"
             style="--branch-color:{html.escape(color)}">

            <div class="branch-icon">
                {html.escape(icon)}
            </div>

            <div class="branch-name">
                {html.escape(category)}
            </div>

            <div class="branch-ja">
                {html.escape(category_ja)}
            </div>
        """

        for spanish, japanese in words:

            content += f"""
            <div class="word-item">
                <div class="word-es">
                    {html.escape(spanish)}
                </div>
                <div class="word-ja">
                    {html.escape(japanese)}
                </div>
            </div>
            """

        content += "</div>"

    content += """
        </div>
        <div class="mind-footer">
            Aprende español paso a paso 🇪🇸
        </div>
    </div>
    """

    st.html(content)


# ==========================================
# セッション管理
# ==========================================

if "question_index" not in st.session_state:
    st.session_state.question_index = random.randrange(len(QUESTIONS))
    st.session_state.round_id = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.is_correct = False
    st.session_state.order = random.sample(range(5), 5)


def next_question():

    previous = st.session_state.question_index

    candidates = [
        i for i in range(len(QUESTIONS))
        if i != previous
    ]

    st.session_state.question_index = random.choice(candidates)
    st.session_state.round_id += 1
    st.session_state.order = random.sample(range(5), 5)
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.is_correct = False


# ==========================================
# ヘッダー
# ==========================================

st.markdown(
    '<div class="main-title">🇪🇸 Mi Mundo Español</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">写真からスペイン語の世界を広げよう！</div>',
    unsafe_allow_html=True
)

q = QUESTIONS[st.session_state.question_index]

score_col, level_col, count_col = st.columns(3)

score_col.metric("正解数", st.session_state.score)
level_col.metric("レベル", q["level"])
count_col.metric("追加語彙", "30語")


# ==========================================
# 問題画面
# ==========================================

st.divider()

st.subheader(q["title"])
st.image(q["photo"], use_container_width=True)

if not st.session_state.answered:

    st.markdown(
        '<div class="instruction">'
        '📘 写真に関係するスペイン語を3つ選んでください。'
        '<br>日本語訳は答え合わせの後に表示されます。'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form(key=f"quiz_{st.session_state.round_id}"):

        choices = {}

        for i in st.session_state.order:

            spanish = q["words"][i][0]

            choices[i] = st.checkbox(
                spanish,
                key=f"choice_{st.session_state.round_id}_{i}"
            )

        submitted = st.form_submit_button(
            "答え合わせ",
            use_container_width=True
        )

    if submitted:

        selected = [
            i for i, value in choices.items()
            if value
        ]

        if len(selected) != 3:
            st.warning("3つ選択してください。")

        else:

            correct = [
                i for i, word in enumerate(q["words"])
                if word[2]
            ]

            st.session_state.selected = selected
            st.session_state.is_correct = (
                set(selected) == set(correct)
            )
            st.session_state.answered = True

            if st.session_state.is_correct:
                st.session_state.score += 1

            st.rerun()


# ==========================================
# 答え合わせ
# ==========================================

if st.session_state.answered:

    st.divider()
    st.header("📝 答え合わせ")

    if st.session_state.is_correct:
        st.success("¡Muy bien! 全問正解です！")
    else:
        st.warning("正解を確認して、覚えましょう！")

    st.markdown("### 5つの単語")

    for i in st.session_state.order:

        spanish, japanese, is_correct = q["words"][i]

        if is_correct:
            st.success(f"✓ {spanish} ＝ {japanese}")
        else:
            st.write(f"✕ {spanish} ＝ {japanese}")

    # ======================================
    # マインドマップ
    # ======================================

    st.divider()
    st.header("🌍 Mi mapa de vocabulario")

    st.write(
        "写真に写っていないものも含めて、"
        "関連する単語を6つのカテゴリーに広げました。"
    )

    show_mindmap(q)

    st.success("30語の新しい単語を学習できます！")

    # ======================================
    # 書き写し学習
    # ======================================

    st.divider()
    st.header("✍️ 書き写して覚えよう")

    st.write(
        "マインドマップを見ながら、"
        "スペイン語をノートに書き写してみましょう。"
    )

    st.markdown("""
    1. スペイン語を見て書き写す
    2. 日本語の意味を確認する
    3. 日本語を見てスペイン語を思い出す
    4. 声に出して発音する
    """)

    with st.expander("学習した単語を一覧で確認"):

        for category, category_ja, icon, color, words in q["categories"]:

            st.markdown(f"#### {icon} {category}（{category_ja}）")

            for spanish, japanese in words:
                st.write(f"{spanish}　—　{japanese}")

    st.divider()

    if st.button(
        "次の問題へ →",
        use_container_width=True,
        type="primary"
    ):
        next_question()
        st.rerun()


# ==========================================
# フッター
# ==========================================

st.divider()

st.caption(
    "Mi Mundo Español | Aprende español cada día 🇪🇸"
)
