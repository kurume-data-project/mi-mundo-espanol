
import json
import random
import time
import urllib.error
import urllib.request
from collections import defaultdict

import streamlit as st


# ==========================================
# Mi Mundo Español
# ==========================================

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #245C83;
}
.sub-title {
    text-align: center;
    color: gray;
}
.word-card {
    padding: 12px;
    border-radius: 12px;
    background: #F1F5F9;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 問題データ
# ==========================================

SCENES = [
    {
        "id": "cafe",
        "title": "En una cafetería",
        "ja": "カフェ",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
        "words": [
            ("la mesa", "テーブル", "家具"),
            ("la silla", "椅子", "家具"),
            ("el café", "コーヒー", "飲食物"),
            ("la taza", "カップ", "道具"),
            ("el vaso", "グラス", "道具"),
            ("el camarero", "ウェイター", "人物"),
            ("la camarera", "ウェイトレス", "人物"),
            ("la cuenta", "お会計", "買い物"),
            ("el menú", "メニュー", "買い物"),
            ("el azúcar", "砂糖", "飲食物"),
            ("la leche", "牛乳", "飲食物"),
            ("la terraza", "テラス", "場所"),
            ("el restaurante", "レストラン", "場所"),
            ("pedir", "注文する", "動作"),
            ("pagar", "支払う", "動作"),
        ],
    },
    {
        "id": "beach",
        "title": "En la playa",
        "ja": "ビーチ",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
        "words": [
            ("el mar", "海", "自然"),
            ("la arena", "砂", "自然"),
            ("la ola", "波", "自然"),
            ("el sol", "太陽", "天気"),
            ("el cielo", "空", "天気"),
            ("la nube", "雲", "天気"),
            ("la toalla", "タオル", "道具"),
            ("el bañador", "水着", "道具"),
            ("la sombrilla", "パラソル", "道具"),
            ("las gafas de sol", "サングラス", "道具"),
            ("el pez", "魚", "動物"),
            ("el delfín", "イルカ", "動物"),
            ("nadar", "泳ぐ", "動作"),
            ("descansar", "休む", "動作"),
            ("tomar el sol", "日光浴する", "動作"),
        ],
    },
    {
        "id": "market",
        "title": "En el mercado",
        "ja": "市場",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            ("la fruta", "果物", "食べ物"),
            ("la verdura", "野菜", "食べ物"),
            ("la manzana", "りんご", "果物"),
            ("el plátano", "バナナ", "果物"),
            ("la naranja", "オレンジ", "果物"),
            ("la zanahoria", "にんじん", "野菜"),
            ("el tomate", "トマト", "野菜"),
            ("la cebolla", "たまねぎ", "野菜"),
            ("el vendedor", "販売員", "人物"),
            ("el cliente", "お客さん", "人物"),
            ("el precio", "価格", "買い物"),
            ("el dinero", "お金", "買い物"),
            ("la bolsa", "袋", "道具"),
            ("comprar", "買う", "動作"),
            ("vender", "売る", "動作"),
        ],
    },
    {
        "id": "city",
        "title": "En la ciudad",
        "ja": "街",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1200",
        "words": [
            ("la calle", "通り", "場所"),
            ("el edificio", "建物", "建物"),
            ("la plaza", "広場", "場所"),
            ("el parque", "公園", "場所"),
            ("la tienda", "店", "買い物"),
            ("el banco", "銀行", "建物"),
            ("el semáforo", "信号", "交通"),
            ("el coche", "車", "交通"),
            ("el autobús", "バス", "交通"),
            ("la bicicleta", "自転車", "交通"),
            ("el árbol", "木", "自然"),
            ("la farola", "街灯", "道具"),
            ("caminar", "歩く", "動作"),
            ("cruzar", "渡る", "動作"),
            ("buscar", "探す", "動作"),
        ],
    },
    {
        "id": "home",
        "title": "En casa",
        "ja": "家",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200",
        "words": [
            ("la casa", "家", "場所"),
            ("la habitación", "部屋", "場所"),
            ("la cocina", "台所", "場所"),
            ("el baño", "浴室・トイレ", "場所"),
            ("la cama", "ベッド", "家具"),
            ("el sofá", "ソファ", "家具"),
            ("la mesa", "テーブル", "家具"),
            ("la puerta", "ドア", "道具"),
            ("la ventana", "窓", "道具"),
            ("la lámpara", "ランプ", "道具"),
            ("el frigorífico", "冷蔵庫", "家電"),
            ("la televisión", "テレビ", "家電"),
            ("cocinar", "料理する", "動作"),
            ("limpiar", "掃除する", "動作"),
            ("dormir", "眠る", "動作"),
        ],
    },
    {
        "id": "school",
        "title": "En la escuela",
        "ja": "学校",
        "level": "A1",
        "photo": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200",
        "words": [
            ("la escuela", "学校", "場所"),
            ("el aula", "教室", "場所"),
            ("la biblioteca", "図書館", "場所"),
            ("el profesor", "先生（男性）", "人物"),
            ("la profesora", "先生（女性）", "人物"),
            ("el estudiante", "学生", "人物"),
            ("el libro", "本", "道具"),
            ("el cuaderno", "ノート", "道具"),
            ("el lápiz", "鉛筆", "道具"),
            ("el bolígrafo", "ボールペン", "道具"),
            ("la mochila", "リュック", "道具"),
            ("la pizarra", "黒板", "道具"),
            ("estudiar", "勉強する", "動作"),
            ("leer", "読む", "動作"),
            ("escribir", "書く", "動作"),
        ],
    },
]


# ==========================================
# セッション状態
# ==========================================

defaults = {
    "score": 0,
    "total": 0,
    "round_id": 0,
    "history": [],
    "current_question": None,
    "answered": False,
    "selected": [],
    "exploration_result": None,
    "exploration_word": "",
    "last_ai_search": 0,
    "ai_search_count": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 問題の自動生成
# ==========================================

def generate_question():

    for _ in range(500):

        scene = random.choice(SCENES)

        correct_words = random.sample(scene["words"], 3)

        other_words = [
            word
            for other_scene in SCENES
            if other_scene["id"] != scene["id"]
            for word in other_scene["words"]
        ]

        distractors = random.sample(other_words, 2)

        choices = correct_words + distractors
        random.shuffle(choices)

        signature = (
            scene["id"],
            tuple(sorted(word[0] for word in correct_words)),
            tuple(sorted(word[0] for word in distractors))
        )

        if signature not in st.session_state.history:
            st.session_state.history.append(signature)

            return {
                "scene": scene,
                "choices": choices,
                "correct": tuple(
                    sorted(word[0] for word in correct_words)
                )
            }

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
# AI単語探究機能
# ==========================================

def get_openai_key():

    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None


def explore_word(word, level):

    api_key = get_openai_key()

    if not api_key:
        raise ValueError(
            "OpenAI APIキーが設定されていません。"
            "StreamlitのSecretsを設定してください。"
        )

    prompt = f"""
あなたは日本人向けのスペイン語教師です。

学習者が入力したスペイン語について、
日本語でわかりやすく説明してください。

入力単語：{word}
学習レベル：{level}

次の条件を守ってください。

・スペイン語として正しい意味を説明する
・名詞なら男性名詞・女性名詞を明記する
・動詞なら不定詞と基本的な意味を説明する
・関連語を6カテゴリーに分けて紹介する
・各カテゴリーに2〜4語を入れる
・関連語にはスペイン語と日本語訳を付ける
・例文は自然なスペイン語にする
・例文を3つ作り、日本語訳も付ける
・学習レベルに合った簡単な文にする
・文法ポイントを2〜3個説明する
・不確かな情報を断定しない
・入力がスペイン語でない場合は、スペイン語の候補を説明する

次のJSON形式だけで回答してください。

{{
  "word": "入力された単語",
  "meaning": "日本語の意味",
  "part_of_speech": "品詞",
  "grammar": "性数や活用などの基本情報",
  "categories": [
    {{
      "name": "カテゴリー名",
      "words": [
        {{
          "spanish": "関連するスペイン語",
          "japanese": "日本語訳"
        }}
      ]
    }}
  ],
  "examples": [
    {{
      "spanish": "スペイン語の例文",
      "japanese": "日本語訳"
    }}
  ],
  "grammar_points": [
    "文法ポイント"
  ],
  "study_tip": "覚え方のヒント"
}}
"""

    payload = {
        "model": "gpt-4o-mini",
        "input": [
            {
                "role": "system",
                "content": (
                    "You are a careful Spanish language teacher. "
                    "Return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "text": {
            "format": {
                "type": "json_object"
            }
        },
        "max_output_tokens": 2200
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"AI APIエラー（HTTP {error.code}）。"
            "APIキー・利用状況・モデル設定を確認してください。"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            "AIサービスに接続できませんでした。通信環境を確認してください。"
        ) from error

    output_text = ""

    for item in result.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text += content.get("text", "")

    if not output_text:
        raise RuntimeError(
            "AIから回答を取得できませんでした。もう一度お試しください。"
        )

    try:
        return json.loads(output_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "AIの回答を読み取れませんでした。もう一度お試しください。"
        ) from error


# ==========================================
# ヘッダー・モード選択
# ==========================================

st.markdown(
    "<h1 class='main-title'>🇪🇸 Mi Mundo Español</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>スペイン語の世界を広げよう！</p>",
    unsafe_allow_html=True
)

mode = st.radio(
    "学習モード",
    [
        "📷 写真で単語を学ぶ",
        "🔎 単語を探究する"
    ],
    horizontal=True
)

st.divider()


# ==========================================
# モード① 写真で単語を学ぶ
# ==========================================

if mode == "📷 写真で単語を学ぶ":

    st.subheader("📷 写真を見て3つ選ぼう")

    col1, col2, col3 = st.columns(3)

    col1.metric("正解数", st.session_state.score)
    col2.metric("回答数", st.session_state.total)

    accuracy = (
        round(
            st.session_state.score /
            st.session_state.total * 100
        )
        if st.session_state.total > 0 else 0
    )

    col3.metric("正解率", f"{accuracy}%")

    question = st.session_state.current_question
    scene = question["scene"]

    st.subheader(scene["title"])
    st.caption(f"テーマ：{scene['ja']} | レベル：{scene['level']}")

    st.image(scene["photo"], use_container_width=True)

    if not st.session_state.answered:

        st.info(
            "写真に関係するスペイン語を3つ選んでください。"
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

    if st.session_state.answered:

        st.divider()
        st.header("📝 答え合わせ")

        if st.session_state.is_correct:
            st.success("¡Muy bien! 全問正解です！")
        else:
            st.warning("正解を確認しましょう。")

        for word in question["choices"]:

            spanish, japanese, category = word

            if spanish in question["correct"]:
                st.success(f"✓ {spanish} ＝ {japanese}")
            else:
                st.write(f"✕ {spanish} ＝ {japanese}")

        st.divider()
        st.header("🌍 関連する単語")

        grouped = defaultdict(list)

        for spanish, japanese, category in scene["words"]:
            grouped[category].append((spanish, japanese))

        columns = st.columns(2)

        for index, (category, words) in enumerate(grouped.items()):

            with columns[index % 2]:
                with st.container(border=True):
                    st.markdown(f"**📚 {category}**")

                    for spanish, japanese in words:
                        st.write(f"{spanish} — {japanese}")

        st.divider()
        st.header("✍️ 書き写して覚えよう")

        st.write(
            "スペイン語を書き写し、声に出して発音してみましょう。"
        )

        with st.expander("今回の単語を一覧で確認"):
            for spanish, japanese, category in scene["words"]:
                st.write(f"{spanish} — {japanese}")

        if st.button(
            "次の問題へ →",
            type="primary",
            use_container_width=True
        ):
            next_question()
            st.rerun()


# ==========================================
# モード② 単語を探究する
# ==========================================

elif mode == "🔎 単語を探究する":

    st.header("🔎 単語探究モード")

    st.write(
        "気になるスペイン語を入力してください。"
        "AIが関連語・例文・文法を整理します。"
    )

    level = st.selectbox(
        "学習レベル",
        ["A1", "A2", "B1"],
        index=1
    )

    with st.form("explore_form"):

        search_word = st.text_input(
            "調べたい単語",
            placeholder="例：la calle、aprovechar、arreglado"
        )

        explore_button = st.form_submit_button(
            "この単語を調べる",
            use_container_width=True
        )

    if explore_button:

        clean_word = search_word.strip()

        if not clean_word:
            st.warning("単語を入力してください。")

        elif len(clean_word) > 80:
            st.warning("入力は80文字以内にしてください。")

        elif st.session_state.ai_search_count >= 10:
            st.warning(
                "このセッションでの検索上限（10回）に達しました。"
                "時間をおいて利用してください。"
            )

        elif time.time() - st.session_state.last_ai_search < 3:
            st.warning("少し待ってから、もう一度お試しください。")

        else:

            st.session_state.last_ai_search = time.time()

            with st.spinner(
                "AIが関連語と例文を作成しています..."
            ):

                try:
                    result = explore_word(clean_word, level)

                    st.session_state.exploration_result = result
                    st.session_state.exploration_word = clean_word
                    st.session_state.ai_search_count += 1

                except Exception as error:
                    st.error(str(error))

    # 検索結果表示

    result = st.session_state.exploration_result

    if result:

        st.divider()

        st.header(f"📖 {result.get('word', '')}")

        st.subheader(result.get("meaning", ""))

        st.write(
            f"**品詞：** {result.get('part_of_speech', '')}"
        )

        st.info(result.get("grammar", ""))

        st.divider()
        st.header("🧠 関連マインドマップ")

        st.markdown(
            """
            <div style="
                background:#245C83;
                color:white;
                padding:18px;
                border-radius:16px;
                text-align:center;
                font-size:24px;
                font-weight:bold;
            ">
            中心の単語
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"### {result.get('word', '')} — {result.get('meaning', '')}"
        )

        categories = result.get("categories", [])
        columns = st.columns(2)

        for index, category in enumerate(categories):

            with columns[index % 2]:

                with st.container(border=True):

                    st.markdown(
                        f"**🌱 {category.get('name', '関連語')}**"
                    )

                    for item in category.get("words", []):

                        spanish = item.get("spanish", "")
                        japanese = item.get("japanese", "")

                        st.markdown(
                            f"- **{spanish}** — {japanese}"
                        )

        st.divider()
        st.header("💬 例文")

        for index, example in enumerate(
            result.get("examples", []), start=1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**例文 {index}**"
                )

                st.markdown(
                    f"### {example.get('spanish', '')}"
                )

                st.write(
                    example.get("japanese", "")
                )

        st.divider()
        st.header("📚 文法ポイント")

        for point in result.get("grammar_points", []):
            st.markdown(f"- {point}")

        st.divider()
        st.header("✍️ 覚え方のヒント")

        st.info(result.get("study_tip", ""))

        st.caption(
            "AIが作成した学習用の説明です。"
            "試験や重要な文章に使う場合は辞書などでも確認してください。"
        )


# ==========================================
# フッター
# ==========================================

st.divider()

st.caption(
    "Mi Mundo Español | Aprende español cada día 🇪🇸"
)
