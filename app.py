
import random
import streamlit as st
from collections import defaultdict

# ==========================================
# Mi Mundo Español
# 写真を見て3つの単語を選ぶ自動出題アプリ
# ==========================================

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="wide"
)

# ==========================================
# 問題データ
# 新しい場面・単語を追加するだけで問題数が増える
# ==========================================

SCENES = [
    {
        "id": "cafe",
        "title": "En una cafetería",
        "ja": "カフェ",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
        "words": [
            ("la mesa", "テーブル", "Muebles"),
            ("la silla", "椅子", "Muebles"),
            ("el café", "コーヒー", "Comida y bebida"),
            ("la taza", "カップ", "Utensilios"),
            ("el vaso", "グラス", "Utensilios"),
            ("el camarero", "ウェイター", "Personas"),
            ("la camarera", "ウェイトレス", "Personas"),
            ("la cuenta", "お会計", "Compras"),
            ("el menú", "メニュー", "Compras"),
            ("el azúcar", "砂糖", "Comida y bebida"),
            ("la leche", "牛乳", "Comida y bebida"),
            ("la terraza", "テラス", "Lugares"),
            ("el restaurante", "レストラン", "Lugares"),
            ("pedir", "注文する", "Acciones"),
            ("pagar", "支払う", "Acciones"),
        ],
    },
    {
        "id": "beach",
        "title": "En la playa",
        "ja": "ビーチ",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
        "words": [
            ("el mar", "海", "Naturaleza"),
            ("la arena", "砂", "Naturaleza"),
            ("la ola", "波", "Naturaleza"),
            ("el sol", "太陽", "Tiempo"),
            ("el cielo", "空", "Tiempo"),
            ("la nube", "雲", "Tiempo"),
            ("la toalla", "タオル", "Objetos"),
            ("el bañador", "水着", "Objetos"),
            ("la sombrilla", "パラソル", "Objetos"),
            ("las gafas de sol", "サングラス", "Objetos"),
            ("el pez", "魚", "Animales"),
            ("el delfín", "イルカ", "Animales"),
            ("nadar", "泳ぐ", "Acciones"),
            ("descansar", "休む", "Acciones"),
            ("tomar el sol", "日光浴する", "Acciones"),
        ],
    },
    {
        "id": "market",
        "title": "En el mercado",
        "ja": "市場",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            ("la fruta", "果物", "Alimentos"),
            ("la verdura", "野菜", "Alimentos"),
            ("la manzana", "りんご", "Frutas"),
            ("el plátano", "バナナ", "Frutas"),
            ("la naranja", "オレンジ", "Frutas"),
            ("la zanahoria", "にんじん", "Verduras"),
            ("el tomate", "トマト", "Verduras"),
            ("la cebolla", "たまねぎ", "Verduras"),
            ("el vendedor", "販売員", "Personas"),
            ("el cliente", "お客さん", "Personas"),
            ("el precio", "価格", "Compras"),
            ("el dinero", "お金", "Compras"),
            ("la bolsa", "袋", "Objetos"),
            ("comprar", "買う", "Acciones"),
            ("vender", "売る", "Acciones"),
        ],
    },
    {
        "id": "city",
        "title": "En la ciudad",
        "ja": "街",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1200",
        "words": [
            ("la calle", "通り", "Lugares"),
            ("el edificio", "建物", "Lugares"),
            ("la plaza", "広場", "Lugares"),
            ("el parque", "公園", "Lugares"),
            ("la tienda", "店", "Compras"),
            ("el banco", "銀行", "Lugares"),
            ("el semáforo", "信号", "Transporte"),
            ("el coche", "車", "Transporte"),
            ("el autobús", "バス", "Transporte"),
            ("la bicicleta", "自転車", "Transporte"),
            ("el árbol", "木", "Naturaleza"),
            ("la farola", "街灯", "Objetos"),
            ("caminar", "歩く", "Acciones"),
            ("cruzar", "渡る", "Acciones"),
            ("buscar", "探す", "Acciones"),
        ],
    },
    {
        "id": "home",
        "title": "En casa",
        "ja": "家",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200",
        "words": [
            ("la casa", "家", "Lugares"),
            ("la habitación", "部屋", "Lugares"),
            ("la cocina", "台所", "Lugares"),
            ("el baño", "浴室・トイレ", "Lugares"),
            ("la cama", "ベッド", "Muebles"),
            ("el sofá", "ソファ", "Muebles"),
            ("la mesa", "テーブル", "Muebles"),
            ("la puerta", "ドア", "Objetos"),
            ("la ventana", "窓", "Objetos"),
            ("la lámpara", "ランプ", "Objetos"),
            ("el frigorífico", "冷蔵庫", "Electrodomésticos"),
            ("la televisión", "テレビ", "Electrodomésticos"),
            ("cocinar", "料理する", "Acciones"),
            ("limpiar", "掃除する", "Acciones"),
            ("dormir", "眠る", "Acciones"),
        ],
    },
    {
        "id": "school",
        "title": "En la escuela",
        "ja": "学校",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200",
        "words": [
            ("la escuela", "学校", "Lugares"),
            ("el aula", "教室", "Lugares"),
            ("la biblioteca", "図書館", "Lugares"),
            ("el profesor", "先生（男性）", "Personas"),
            ("la profesora", "先生（女性）", "Personas"),
            ("el estudiante", "学生", "Personas"),
            ("el libro", "本", "Objetos"),
            ("el cuaderno", "ノート", "Objetos"),
            ("el lápiz", "鉛筆", "Objetos"),
            ("el bolígrafo", "ボールペン", "Objetos"),
            ("la mochila", "リュック", "Objetos"),
            ("la pizarra", "黒板", "Objetos"),
            ("estudiar", "勉強する", "Acciones"),
            ("leer", "読む", "Acciones"),
            ("escribir", "書く", "Acciones"),
        ],
    },
]

# ==========================================
# セッション状態
# ==========================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "round_id" not in st.session_state:
    st.session_state.round_id = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected" not in st.session_state:
    st.session_state.selected = []


# ==========================================
# 自動問題生成
# ==========================================

def generate_question():

    # 既出問題と重ならない組み合わせを探す
    for _ in range(500):

        scene = random.choice(SCENES)

        correct_words = random.sample(
            scene["words"], 3
        )

        other_words = [
            word
            for other_scene in SCENES
            if other_scene["id"] != scene["id"]
            for word in other_scene["words"]
        ]

        distractors = random.sample(other_words, 2)

        choices = correct_words + distractors
        random.shuffle(choices)

        correct_set = tuple(
            sorted(word[0] for word in correct_words)
        )

        signature = (
            scene["id"],
            correct_set,
            tuple(sorted(word[0] for word in distractors))
        )

        if signature not in st.session_state.history:
            st.session_state.history.append(signature)

            return {
                "scene": scene,
                "choices": choices,
                "correct": correct_set,
            }

    # 組み合わせが尽きた場合は履歴をリセット
    st.session_state.history = []

    return generate_question()


def next_question():

    st.session_state.current_question = generate_question()
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.round_id += 1


if st.session_state.current_question is None:
    next_question()


# ==========================================
# ヘッダー
# ==========================================

st.markdown(
    "<h1 style='text-align:center;color:#245C83;'>"
    "🇪🇸 Mi Mundo Español</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "写真からスペイン語の世界を広げよう！</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

col1.metric("正解数", st.session_state.score)
col2.metric("回答数", st.session_state.total)

accuracy = (
    round(st.session_state.score / st.session_state.total * 100)
    if st.session_state.total > 0 else 0
)

col3.metric("正解率", f"{accuracy}%")

st.divider()


# ==========================================
# 現在の問題
# ==========================================

question = st.session_state.current_question
scene = question["scene"]

st.subheader(f"📷 {scene['title']}")

st.caption(
    f"テーマ：{scene['ja']}　|　レベル：{scene['level']}"
)

st.image(
    scene["photo"],
    use_container_width=True
)

# ==========================================
# 回答前
# ==========================================

if not st.session_state.answered:

    st.info(
        "写真を見て、関係するスペイン語を3つ選んでください。"
        "日本語訳は答え合わせの後に表示されます。"
    )

    with st.form(
        key=f"answer_form_{st.session_state.round_id}"
    ):

        selected = []

        for i, word in enumerate(question["choices"]):

            checked = st.checkbox(
                word[0],
                key=f"choice_{st.session_state.round_id}_{i}"
            )

            if checked:
                selected.append(word[0])

        submitted = st.form_submit_button(
            "答え合わせ",
            use_container_width=True
        )

    if submitted:

        if len(selected) != 3:

            st.warning("3つ選択してください。")

        else:

            st.session_state.selected = selected

            st.session_state.total += 1

            st.session_state.is_correct = (
                set(selected) == set(question["correct"])
            )

            if st.session_state.is_correct:
                st.session_state.score += 1

            st.session_state.answered = True

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
        st.warning("もう一度、正解を確認しましょう。")

    for word in question["choices"]:

        spanish, japanese, category = word

        if spanish in question["correct"]:
            st.success(f"✓ {spanish} ＝ {japanese}")
        else:
            st.write(f"✕ {spanish} ＝ {japanese}")

    # ======================================
    # 関連語のマインドマップ
    # ======================================

    st.divider()
    st.header("🌍 関連する単語を広げよう")

    st.write(
        f"「{scene['ja']}」に関連する単語を整理しました。"
        "写真に写っていないものも覚えましょう。"
    )

    grouped = defaultdict(list)

    for spanish, japanese, category in scene["words"]:
        grouped[category].append((spanish, japanese))

    columns = st.columns(2)

    for index, (category, words) in enumerate(grouped.items()):

        with columns[index % 2]:

            with st.container(border=True):

                st.markdown(f"**📚 {category}**")

                for spanish, japanese in words:
                    st.markdown(
                        f"- **{spanish}**　{japanese}"
                    )

    # ======================================
    # 書き写し学習
    # ======================================

    st.divider()
    st.header("✍️ 書き写して覚えよう")

    st.write(
        "スペイン語をノートに書き写して、"
        "声に出して発音してみましょう。"
    )

    st.markdown("""
    1. スペイン語を見て書き写す
    2. 日本語の意味を確認する
    3. 日本語を見てスペイン語を思い出す
    4. 声に出して発音する
    """)

    with st.expander("今回の単語を一覧で確認"):

        for spanish, japanese, category in scene["words"]:
            st.write(f"{spanish}　—　{japanese}")

    st.divider()

    if st.button(
        "次の問題へ →",
        type="primary",
        use_container_width=True
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
