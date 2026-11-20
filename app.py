
import random
import streamlit as st

st.set_page_config(
    page_title="Mi Mundo Español",
    page_icon="🇪🇸",
    layout="centered"
)

# 問題データ
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
    },
    {
        "title": "En el mercado",
        "level": "A2",
        "photo": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
        "words": [
            {"es": "la fruta", "ja": "果物", "correct": True},
            {"es": "la verdura", "ja": "野菜", "correct": True},
            {"es": "el vendedor", "ja": "店員", "correct": True},
            {"es": "el ordenador", "ja": "パソコン", "correct": False},
            {"es": "el aeropuerto", "ja": "空港", "correct": False},
        ],
    },
]

# セッション状態
if "number" not in st.session_state:
    st.session_state.number = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.question = random.randrange(len(QUESTIONS))
    st.session_state.order = random.sample(range(5), 5)

def next_question():
    previous = st.session_state.question
    candidates = [
        i for i in range(len(QUESTIONS)) if i != previous
    ]
    st.session_state.question = random.choice(candidates)
    st.session_state.order = random.sample(range(5), 5)
    st.session_state.number += 1
    st.session_state.answered = False
    st.session_state.selected = []

# 現在の問題
q = QUESTIONS[st.session_state.question]

st.title("🇪🇸 Mi Mundo Español")
st.caption("写真を見て、スペイン語の単語を覚えよう！")

st.write(
    f"**レベル：{q['level']}**　"
    f"問題数：{st.session_state.number + 1}　"
    f"正解数：{st.session_state.score}"
)

st.subheader(q["title"])

st.image(q["photo"], use_container_width=True)

st.write("写真に関係する単語を3つ選んでください。")

# 選択画面
with st.form(key=f"quiz_{st.session_state.number}"):
    choices = {}

    for i in st.session_state.order:
        word = q["words"][i]
        choices[i] = st.checkbox(
            f"{word['es']}　（{word['ja']}）",
            key=f"word_{st.session_state.number}_{i}"
        )

    submitted = st.form_submit_button("答え合わせ")

if submitted and not st.session_state.answered:
    selected = [i for i, value in choices.items() if value]

    if len(selected) != 3:
        st.warning("3つ選んでください。")
    else:
        st.session_state.selected = selected
        st.session_state.answered = True

        correct = [
            i for i, word in enumerate(q["words"])
            if word["correct"]
        ]

        if set(selected) == set(correct):
            st.session_state.score += 1
            st.session_state.is_correct = True
        else:
            st.session_state.is_correct = False

# 答え合わせ後
if st.session_state.answered:
    if st.session_state.is_correct:
        st.success("¡Muy bien! 全問正解です！")
    else:
        st.error("もう少し！正解を確認しましょう。")

    st.subheader("正解の単語")

    correct_words = [
        word for word in q["words"] if word["correct"]
    ]

    # マインドマップ風の表示
    st.markdown(
        f"### 🌍 {q['title']}"
    )

    cols = st.columns(3)

    for col, word in zip(cols, correct_words):
        with col:
            st.markdown(f"**{word['es']}**")
            st.caption(word["ja"])

    st.divider()
    st.info("単語を声に出して読んでみましょう！")

    if st.button("次の問題へ →", use_container_width=True):
        next_question()
        st.rerun()

st.divider()
st.caption("Mi Mundo Español | Aprende español cada día")
