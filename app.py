
import random
import streamlit as st

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="centered"
)

# ---------------------------------
# 問題・語彙データ
# ---------------------------------

QUESTIONS = [
    {
        "title": "En una cafetería",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
        "words": [
            {"es": "la mesa", "ja": "テーブル", "correct": True},
            {"es": "la silla", "ja": "椅子", "correct": True},
            {"es": "el café", "ja": "コーヒー", "correct": True},
            {"es": "el avión", "ja": "飛行機", "correct": False},
            {"es": "el hospital", "ja": "病院", "correct": False},
        ],
        "mindmap": {
            "食べ物・飲み物": [
                ("el té", "お茶"),
                ("la leche", "牛乳"),
                ("el azúcar", "砂糖"),
                ("el agua", "水"),
                ("el zumo", "ジュース"),
            ],
            "お店・人": [
                ("el camarero", "ウェイター"),
                ("la camarera", "ウェイトレス"),
                ("el cliente", "客"),
                ("la cafetería", "カフェ"),
                ("el menú", "メニュー"),
            ],
            "食器・道具": [
                ("la taza", "カップ"),
                ("el vaso", "グラス"),
                ("la cuchara", "スプーン"),
                ("el tenedor", "フォーク"),
                ("el plato", "皿"),
            ],
            "行動・その他": [
                ("pedir", "注文する"),
                ("pagar", "支払う"),
                ("la cuenta", "お会計"),
                ("desayunar", "朝食をとる"),
                ("la propina", "チップ"),
            ],
        },
    },
    {
        "title": "En la playa",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
        "words": [
            {"es": "el mar", "ja": "海", "correct": True},
            {"es": "la playa", "ja": "ビーチ", "correct": True},
            {"es": "el sol", "ja": "太陽", "correct": True},
            {"es": "el tren", "ja": "電車", "correct": False},
            {"es": "la oficina", "ja": "オフィス", "correct": False},
        ],
        "mindmap": {
            "海の生き物": [
                ("el pez", "魚"),
                ("el delfín", "イルカ"),
                ("la tortuga", "カメ"),
                ("el tiburón", "サメ"),
                ("la medusa", "クラゲ"),
            ],
            "持ち物": [
                ("la toalla", "タオル"),
                ("el bañador", "水着"),
                ("las gafas de sol", "サングラス"),
                ("la sombrilla", "ビーチパラソル"),
                ("la crema solar", "日焼け止め"),
            ],
            "自然・天気": [
                ("la arena", "砂"),
                ("la ola", "波"),
                ("el viento", "風"),
                ("la nube", "雲"),
                ("la lluvia", "雨"),
            ],
            "行動": [
                ("nadar", "泳ぐ"),
                ("bucear", "潜る"),
                ("tomar el sol", "日光浴する"),
                ("jugar", "遊ぶ"),
                ("descansar", "休む"),
            ],
        },
    },
    {
        "title": "En el mercado",
        "level": "A2",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            {"es": "la fruta", "ja": "果物", "correct": True},
            {"es": "la verdura", "ja": "野菜", "correct": True},
            {"es": "el vendedor", "ja": "店員・販売員", "correct": True},
            {"es": "el ordenador", "ja": "パソコン", "correct": False},
            {"es": "el aeropuerto", "ja": "空港", "correct": False},
        ],
        "mindmap": {
            "果物": [
                ("la manzana", "りんご"),
                ("el plátano", "バナナ"),
                ("la naranja", "オレンジ"),
                ("la fresa", "いちご"),
                ("la uva", "ぶどう"),
            ],
            "野菜": [
                ("la cebolla", "たまねぎ"),
                ("la zanahoria", "にんじん"),
                ("el tomate", "トマト"),
                ("la patata", "じゃがいも"),
                ("el pepino", "きゅうり"),
            ],
            "買い物": [
                ("el precio", "価格"),
                ("el dinero", "お金"),
                ("la bolsa", "袋"),
                ("el kilo", "キログラム"),
                ("el descuento", "割引"),
            ],
            "行動・その他": [
                ("comprar", "買う"),
                ("vender", "売る"),
                ("elegir", "選ぶ"),
                ("pesar", "重さを量る"),
                ("fresco", "新鮮な"),
            ],
        },
    },
]


# ---------------------------------
# セッション状態
# ---------------------------------

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


# ---------------------------------
# 画面表示
# ---------------------------------

q = QUESTIONS[st.session_state.q_index]

st.title("🇪🇸 Mi Mundo Español")
st.caption("写真からスペイン語の世界を広げよう！")

col1, col2 = st.columns(2)
col1.metric("レベル", q["level"])
col2.metric("正解数", st.session_state.score)

st.progress(
    (st.session_state.round_id % 10 + 1) / 10
)

st.subheader(q["title"])
st.image(q["photo"], use_container_width=True)

# ---------------------------------
# クイズ画面
# 日本語訳は表示しない
# ---------------------------------

if not st.session_state.answered:

    st.write("### 写真に関係する単語を3つ選んでください。")
    st.info("ヒント：スペイン語だけを見て考えてみましょう！")

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


# ---------------------------------
# 答え合わせ
# ---------------------------------

if st.session_state.answered:

    st.divider()
    st.subheader("答え合わせ")

    if st.session_state.is_correct:
        st.success("¡Muy bien! 全問正解です！")
    else:
        st.warning("正解を確認して、覚えましょう！")

    st.write("#### 5つの選択肢")

    for i in st.session_state.order:
        word = q["words"][i]

        if word["correct"]:
            st.success(f"✓ {word['es']} ＝ {word['ja']}")
        else:
            st.write(f"✕ {word['es']} ＝ {word['ja']}")

    st.divider()

    # ---------------------------------
    # マインドマップ
    # ---------------------------------

    st.header("🌍 スペイン語マインドマップ")
    st.subheader(q["title"])

    st.markdown(
        "**写真のテーマから、さらに語彙を広げましょう。**"
    )

    st.info(
        "ここからは写真に写っていない関連語も含みます。"
        "新しい単語をノートに書き写して覚えましょう！"
    )

    # 中心となるテーマ
    st.markdown(
        f"""
        <div style="
            background-color:#245c83;
            color:white;
            padding:16px;
            border-radius:14px;
            text-align:center;
            font-size:22px;
            font-weight:bold;
            margin:10px 0 20px 0;
        ">
        🌍 {q['title']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 正解した3単語
    st.markdown("### 📌 写真に関係する基本単語")

    cols = st.columns(3)

    for col, word in zip(
        cols,
        [w for w in q["words"] if w["correct"]]
    ):
        with col:
            st.markdown(f"**{word['es']}**")
            st.caption(word["ja"])

    st.divider()

    # 写真にない関連語をカテゴリー別に表示
    st.markdown("### 🌱 写真から広げる関連語")

    for category, words in q["mindmap"].items():

        with st.container(border=True):
            st.markdown(f"#### 🔹 {category}")

            for es, ja in words:
                st.write(f"**{es}**　—　{ja}")

    st.divider()

    st.subheader("✍️ 書き写して覚えよう")

    st.write(
        "マインドマップの単語をノートに書いてみましょう。"
    )

    st.markdown(
        """
        1. スペイン語を見ながら書く
        2. 日本語の意味を確認する
        3. 日本語を隠してスペイン語を思い出す
        4. 声に出して発音する
        """
    )

    st.success(
        f"今回の追加語彙：{sum(len(v) for v in q['mindmap'].values())}語"
    )

    if st.button(
        "次の問題へ →",
        use_container_width=True
    ):
        next_question()
        st.rerun()

st.divider()
st.caption("Mi Mundo Español | Aprende español cada día")
