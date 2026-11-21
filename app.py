import random
import re
import base64, hashlib, io, json
from datetime import date
from collections import defaultdict

import pandas as pd
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="MimapES", page_icon="🇪🇸", layout="wide")

st.markdown("""
<style>
.main-title{text-align:center;color:#245C83}
.sub-title{text-align:center;color:gray}
.center-node{background:#245C83;color:white;padding:16px;border-radius:16px;
text-align:center;font-size:22px;font-weight:bold;margin:8px 0 18px}
</style>
""", unsafe_allow_html=True)

# 写真クイズの既存データ
SCENES = [
    {"id":"cafe","title":"En una cafetería","ja":"カフェ","level":"A1",
     "photo":"https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200",
     "words":[("la mesa","テーブル","家具"),("la silla","椅子","家具"),("el café","コーヒー","飲食物"),("la taza","カップ","道具"),("el vaso","グラス","道具"),("el camarero","ウェイター","人物"),("la camarera","ウェイトレス","人物"),("la cuenta","お会計","買い物"),("el menú","メニュー","買い物"),("el azúcar","砂糖","飲食物"),("la leche","牛乳","飲食物"),("la terraza","テラス","場所"),("el restaurante","レストラン","場所"),("pedir","注文する","動作"),("pagar","支払う","動作")]},
    {"id":"beach","title":"En la playa","ja":"ビーチ","level":"A1",
     "photo":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
     "words":[("el mar","海","自然"),("la arena","砂","自然"),("la ola","波","自然"),("el sol","太陽","天気"),("el cielo","空","天気"),("la nube","雲","天気"),("la toalla","タオル","道具"),("el bañador","水着","道具"),("la sombrilla","パラソル","道具"),("las gafas de sol","サングラス","道具"),("el pez","魚","動物"),("el delfín","イルカ","動物"),("nadar","泳ぐ","動作"),("descansar","休む","動作"),("tomar el sol","日光浴する","動作")]},
    {"id":"market","title":"En el mercado","ja":"市場","level":"A1",
     "photo":"https://images.unsplash.com/photo-1542838132-92c53300491e?w=1200",
     "words":[("la fruta","果物","食べ物"),("la verdura","野菜","食べ物"),("la manzana","りんご","果物"),("el plátano","バナナ","果物"),("la naranja","オレンジ","果物"),("la zanahoria","にんじん","野菜"),("el tomate","トマト","野菜"),("la cebolla","たまねぎ","野菜"),("el vendedor","販売員","人物"),("el cliente","お客さん","人物"),("el precio","価格","買い物"),("el dinero","お金","買い物"),("la bolsa","袋","道具"),("comprar","買う","動作"),("vender","売る","動作")]},
    {"id":"city","title":"En la ciudad","ja":"街","level":"A1",
     "photo":"https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1200",
     "words":[("la calle","通り","場所"),("el edificio","建物","建物"),("la plaza","広場","場所"),("el parque","公園","場所"),("la tienda","店","買い物"),("el banco","銀行","建物"),("el semáforo","信号","交通"),("el coche","車","交通"),("el autobús","バス","交通"),("la bicicleta","自転車","交通"),("el árbol","木","自然"),("la farola","街灯","道具"),("caminar","歩く","動作"),("cruzar","渡る","動作"),("buscar","探す","動作")]},
    {"id":"home","title":"En casa","ja":"家","level":"A1",
     "photo":"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200",
     "words":[("la casa","家","場所"),("la habitación","部屋","場所"),("la cocina","台所","場所"),("el baño","浴室・トイレ","場所"),("la cama","ベッド","家具"),("el sofá","ソファ","家具"),("la mesa","テーブル","家具"),("la puerta","ドア","道具"),("la ventana","窓","道具"),("la lámpara","ランプ","道具"),("el frigorífico","冷蔵庫","家電"),("la televisión","テレビ","家電"),("cocinar","料理する","動作"),("limpiar","掃除する","動作"),("dormir","眠る","動作")]},
    {"id":"school","title":"En la escuela","ja":"学校","level":"A1",
     "photo":"https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200",
     "words":[("la escuela","学校","場所"),("el aula","教室","場所"),("la biblioteca","図書館","場所"),("el profesor","先生（男性）","人物"),("la profesora","先生（女性）","人物"),("el estudiante","学生","人物"),("el libro","本","道具"),("el cuaderno","ノート","道具"),("el lápiz","鉛筆","道具"),("el bolígrafo","ボールペン","道具"),("la mochila","リュック","道具"),("la pizarra","黒板","道具"),("estudiar","勉強する","動作"),("leer","読む","動作"),("escribir","書く","動作")]}
]

# 写真アップロード機能のテーマ別語彙（固定データ。写真のAI認識はしません）
MINDMAP = {
"カフェ":("En una cafetería",{
"場所・家具":[("la cafetería","カフェ"),("la mesa","テーブル"),("la silla","椅子"),("la terraza","テラス")],
"飲み物・食べ物":[("el café","コーヒー"),("el té","紅茶"),("la leche","牛乳"),("el agua","水"),("el azúcar","砂糖"),("el bocadillo","サンドイッチ")],
"人・道具":[("el camarero","ウェイター"),("la camarera","ウェイトレス"),("la taza","カップ"),("el vaso","グラス"),("el menú","メニュー")],
"行動・会話":[("pedir","注文する"),("pagar","支払う"),("la cuenta","お会計"),("¿Qué desea?","何になさいますか？"),("Quisiera un café.","コーヒーをお願いします。")]}),
"レストラン":("En un restaurante",{
"場所・人":[("el restaurante","レストラン"),("la mesa","テーブル"),("el camarero","ウェイター"),("el cliente","客"),("la cocina","厨房")],
"料理・飲み物":[("el menú","メニュー"),("el plato","料理・皿"),("la ensalada","サラダ"),("el arroz","米・ご飯"),("el pescado","魚料理"),("la carne","肉"),("el agua","水")],
"道具":[("el tenedor","フォーク"),("el cuchillo","ナイフ"),("la cuchara","スプーン"),("el vaso","グラス"),("la servilleta","ナプキン")],
"行動・会話":[("reservar","予約する"),("pedir","注文する"),("recomendar","おすすめする"),("pagar","支払う"),("La cuenta, por favor.","お会計をお願いします。")]}),
"街・道路":("En la ciudad",{
"場所・建物":[("la calle","通り"),("la plaza","広場"),("el edificio","建物"),("el parque","公園"),("la tienda","店"),("el banco","銀行")],
"交通":[("el coche","車"),("el autobús","バス"),("el tren","電車"),("la bicicleta","自転車"),("el semáforo","信号")],
"街にあるもの":[("el árbol","木"),("la farola","街灯"),("el paso de peatones","横断歩道"),("la acera","歩道")],
"行動・会話":[("caminar","歩く"),("cruzar","渡る"),("buscar","探す"),("girar","曲がる"),("¿Dónde está ...?","…はどこですか？")]}),
"公園":("En el parque",{
"自然":[("el árbol","木"),("la flor","花"),("la hierba","草"),("el césped","芝生"),("el pájaro","鳥"),("el lago","湖")],
"場所・設備":[("el parque","公園"),("el banco","ベンチ"),("el camino","小道"),("el parque infantil","遊び場")],
"人・もの":[("el niño","男の子"),("la niña","女の子"),("el perro","犬"),("la pelota","ボール"),("la bicicleta","自転車")],
"行動":[("pasear","散歩する"),("correr","走る"),("jugar","遊ぶ"),("descansar","休む"),("dar de comer","餌をあげる")]}),
"市場・買い物":("En el mercado",{
"食べ物":[("la fruta","果物"),("la verdura","野菜"),("la manzana","りんご"),("el plátano","バナナ"),("la naranja","オレンジ"),("el tomate","トマト")],
"人・場所":[("el mercado","市場"),("el vendedor","販売員"),("el cliente","客"),("el puesto","売り場")],
"買い物":[("el precio","価格"),("el dinero","お金"),("la bolsa","袋"),("la tarjeta","カード"),("la oferta","特売")],
"行動・会話":[("comprar","買う"),("vender","売る"),("costar","値段がする"),("¿Cuánto cuesta?","いくらですか？"),("Quiero medio kilo.","500グラムください。")]}),
"自宅":("En casa",{
"部屋":[("la casa","家"),("la habitación","部屋"),("la cocina","台所"),("el baño","浴室・トイレ"),("el salón","リビング")],
"家具":[("la cama","ベッド"),("el sofá","ソファ"),("la mesa","テーブル"),("la silla","椅子"),("el armario","クローゼット")],
"道具・家電":[("la puerta","ドア"),("la ventana","窓"),("la lámpara","ランプ"),("el frigorífico","冷蔵庫"),("la lavadora","洗濯機")],
"行動":[("cocinar","料理する"),("limpiar","掃除する"),("dormir","眠る"),("ducharse","シャワーを浴びる"),("descansar","休む")]}),
"学校":("En la escuela",{
"場所":[("la escuela","学校"),("el aula","教室"),("la biblioteca","図書館"),("el gimnasio","体育館")],
"人":[("el profesor","先生（男性）"),("la profesora","先生（女性）"),("el estudiante","学生"),("el compañero","クラスメート")],
"学用品":[("el libro","本"),("el cuaderno","ノート"),("el lápiz","鉛筆"),("el bolígrafo","ボールペン"),("la mochila","リュック"),("la pizarra","黒板")],
"行動":[("estudiar","勉強する"),("leer","読む"),("escribir","書く"),("preguntar","質問する"),("aprender","学ぶ")]}),
"駅・交通":("En la estación",{
"場所":[("la estación","駅"),("el andén","ホーム"),("la entrada","入口"),("la salida","出口"),("la taquilla","切符売り場")],
"交通":[("el tren","電車"),("el metro","地下鉄"),("el autobús","バス"),("el taxi","タクシー"),("el billete","切符")],
"人・もの":[("el pasajero","乗客"),("el revisor","車掌"),("la maleta","スーツケース"),("el horario","時刻表")],
"行動・会話":[("viajar","旅行する"),("subir","乗る・上がる"),("bajar","降りる"),("¿A qué hora sale?","何時に出発しますか？"),("Un billete, por favor.","切符を1枚ください。")]}),
"海・ビーチ":("En la playa",{
"自然・天気":[("el mar","海"),("la arena","砂"),("la ola","波"),("el sol","太陽"),("el cielo","空"),("la nube","雲")],
"持ち物":[("la toalla","タオル"),("el bañador","水着"),("la sombrilla","パラソル"),("las gafas de sol","サングラス"),("la crema solar","日焼け止め")],
"生き物":[("el pez","魚"),("el delfín","イルカ"),("la gaviota","カモメ"),("la concha","貝殻")],
"行動":[("nadar","泳ぐ"),("tomar el sol","日光浴する"),("descansar","休む"),("jugar","遊ぶ"),("bucear","潜水する")]}),
"旅行・観光":("De viaje",{
"観光地":[("el museo","美術館・博物館"),("el monumento","記念碑"),("la catedral","大聖堂"),("el castillo","城"),("la playa","ビーチ")],
"移動":[("el aeropuerto","空港"),("la estación","駅"),("el avión","飛行機"),("el tren","電車"),("el mapa","地図")],
"旅行の持ち物":[("el pasaporte","パスポート"),("la maleta","スーツケース"),("la cámara","カメラ"),("la reserva","予約")],
"行動・会話":[("visitar","訪れる"),("hacer fotos","写真を撮る"),("alojarse","宿泊する"),("¿Cuánto cuesta la entrada?","入場料はいくらですか？"),("Tengo una reserva.","予約しています。")]})
}


# --- AI cost controls ---
AI_MODEL = "gpt-4o-mini"
IMAGE_MODEL = "gpt-image-2.5-flare"
DAILY_AI_LIMIT = 20
OPENAI_URL = "https://api.openai.com/v1/responses"

def api_key():
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return ""

def day_key():
    return date.today().isoformat()

def ai_allowed():
    if st.session_state.get("ai_day") != day_key():
        st.session_state.ai_day = day_key()
        st.session_state.ai_count = 0
    return st.session_state.get("ai_count", 0) < DAILY_AI_LIMIT

def ai_used():
    if st.session_state.get("ai_day") != day_key():
        st.session_state.ai_day = day_key()
        st.session_state.ai_count = 0
    st.session_state.ai_count += 1

def response_text(data):
    parts = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            parts.extend(x.get("text", "") for x in item.get("content", []) if x.get("type") == "output_text")
    return "\n".join(parts).strip()

def json_result(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

def small_jpeg(upload):
    im = Image.open(upload).convert("RGB")
    im.thumbnail((768, 768))
    b = io.BytesIO()
    im.save(b, format="JPEG", quality=65, optimize=True)
    return b.getvalue()


@st.cache_data(ttl=86400, show_spinner=False)
def mindmap_ai(jpeg, level, key):
    """写真をもとに、カテゴリー別のスペイン語学習マインドマップを作る。"""
    b64 = base64.b64encode(jpeg).decode("utf-8")
    prompt = f"""あなたは日本人向けのスペイン語教師です。画像を観察し、レベル{level}（A1またはA2）の学習者向けに、写真を中心としたスペイン語マインドマップを作成してください。A1では最も基本的な語彙と短い現在形の文を使い、A2では日常生活で使う少し幅広い語彙と簡単な表現を使ってください。B1以上の難しい語彙・文法は使わないでください。
画像に実際に写っているものを中心に、関連する場所・人・物・食べ物・自然・動作・会話表現も含めてください。見えない物を写っていると断定しないでください。
JSONだけを返し、Markdownや説明文は付けないでください。
形式:
{{"scene_es":"写真の場面を表す自然なスペイン語","scene_ja":"日本語のテーマ名","summary":"写真の短い説明","categories":[{{"name":"カテゴリー名","words":[{{"es":"スペイン語（名詞は定冠詞付き）","ja":"日本語訳","example_es":"短い例文","example_ja":"例文の日本語訳"}}]}}]}}
カテゴリーは4〜6個にしてください。重要：各カテゴリーには必ずスペイン語の単語・表現をちょうど5個ずつ入れてください（3個や4個で終わらせない）。写真に写っているものを優先し、不足する場合は写真の場面で自然に使う関連語・動作・形容詞・会話表現を補ってください。カテゴリー間で同じ単語を重複させないでください。名詞は定冠詞を付け、日本語訳は自然で正確にしてください。各単語に短い例文と日本語訳を必ず付けてください。"""
    r = requests.post(OPENAI_URL, headers={"Authorization": f"Bearer {key}"},
        json={"model": AI_MODEL, "input": [{"role": "user", "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64}", "detail": "low"}
        ]}], "max_output_tokens": 1900, "store": False}, timeout=60)
    r.raise_for_status()
    return json_result(response_text(r.json()))

@st.cache_data(ttl=86400, show_spinner=False)
def illustrated_mindmap_ai(scene_es, scene_ja, level, categories_json, key):
    """抽出済みの語彙をもとに、イラスト付き学習ポスターを生成する。"""
    categories = json.loads(categories_json)
    lines = []
    for category in categories:
        lines.append(f"【{category.get('name', 'カテゴリー')}】")
        for word in category.get("words", []):
            lines.append(f"{word.get('es', '')} — {word.get('ja', '')}")
    vocab_text = "\n".join(lines)
    prompt = f"""Create a beautiful illustrated Spanish vocabulary mind-map study poster.
Theme: {scene_es} / {scene_ja}. Learner level: {level} (CEFR A1-A2).
Style: warm hand-drawn watercolor and colored-pencil cartoon illustration, friendly educational infographic, cream paper background, colorful rounded branches and small clear illustrations related to the theme. Landscape 3:2 composition, high resolution, balanced whitespace, polished printable study poster.
Center: large theme illustration and the title '{scene_es}' with Japanese '{scene_ja}'.
Arrange the following category headings and vocabulary around the center in separate clearly separated colored panels. Reproduce every Spanish term and Japanese translation exactly as written. Keep accents and articles. Do not invent, omit, duplicate, or translate the listed text differently. Use legible simple typography. Do not add unrelated text.
{vocab_text}
Important: include all listed category headings and every vocabulary pair. Keep text large and uncluttered. Add small friendly drawings that illustrate each category, but prioritize correct readable vocabulary text."""
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": IMAGE_MODEL, "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1},
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    image_b64 = payload["data"][0].get("b64_json")
    if not image_b64:
        raise ValueError("画像データが返されませんでした。")
    return base64.b64decode(image_b64)


@st.cache_data(ttl=86400, show_spinner=False)
def word_coach_ai(words_text, level, key):
    """覚えにくい単語・混同しやすい単語の覚え方を提案する。"""
    prompt = f"""あなたは日本人向けのスペイン語教師です。
学習者のレベルは{level}（A1またはA2）です。次の単語について、覚え方と見分け方を日本語で提案してください。A1では基本的な語彙と簡単な文で、A2では日常会話で使う少し幅広い語彙と表現で説明してください。B1以上の難しい文法や語彙は避けてください。
入力された単語：{words_text}

入力が似た単語の組み合わせなら、意味・ニュアンス・使い分けを対比してください。
単語が1つなら、意味、語の成り立ち（確実な場合のみ）、覚え方、よく使う場面を説明してください。
語呂合わせは無理に作らず、正確さを優先してください。例文は自然で短いスペイン語にし、日本語訳を付けてください。
最後に理解を確認する3問のミニクイズを作ってください。
JSONだけを返し、Markdownのコードフェンスや前置きは付けないでください。
形式：
{{"title":"短いタイトル","summary":"意味・違いの要約","comparison":[{{"word":"単語","meaning":"意味","nuance":"ニュアンス・使い方","memory_tip":"覚え方"}}],
"how_to_distinguish":["見分け方1","見分け方2"],"examples":[{{"es":"スペイン語の例文","ja":"日本語訳","point":"注目ポイント"}}],
"quiz":[{{"question":"問題文","options":["選択肢A","選択肢B"],"answer":"正解","explanation":"解説"}}]}}
comparisonは1〜4項目、examplesは2〜3項目、quizは3問にしてください。"""
    r = requests.post(
        OPENAI_URL,
        headers={"Authorization": f"Bearer {key}"},
        json={"model": AI_MODEL, "input": prompt, "max_output_tokens": 1300, "store": False},
        timeout=60,
    )
    r.raise_for_status()
    return json_result(response_text(r.json()))


def usage_caption():
    if st.session_state.get("ai_day") != day_key():
        st.session_state.ai_day = day_key()
        st.session_state.ai_count = 0
    st.caption(f"本日のAI利用：{st.session_state.get('ai_count',0)}/{DAILY_AI_LIMIT}回（マインドマップ・苦手単語攻略の合計）")


# セッション状態
defaults = {"score":0,"total":0,"round_id":0,"history":[],"current_question":None,
            "answered":False,"selected":[],"is_correct":False,"ai_day":day_key(),"ai_count":0,"mindmap_result":None,"mindmap_illustration":None,"word_coach_result":None}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def generate_question():
    for _ in range(500):
        scene = random.choice(SCENES)
        correct = random.sample(scene["words"], 3)
        others = [w for s in SCENES if s["id"] != scene["id"] for w in s["words"]]
        choices = correct + random.sample(others, 2)
        random.shuffle(choices)
        signature = (scene["id"], tuple(sorted(w[0] for w in correct)),
                     tuple(sorted(w[0] for w in choices if w not in correct)))
        if signature not in st.session_state.history:
            st.session_state.history.append(signature)
            return {"scene":scene,"choices":choices,
                    "correct":tuple(sorted(w[0] for w in correct))}
    st.session_state.history = []
    return generate_question()

def next_question():
    st.session_state.current_question = generate_question()
    st.session_state.answered = False
    st.session_state.selected = []
    st.session_state.round_id += 1

if st.session_state.current_question is None:
    next_question()

st.markdown("<h1 class='main-title'>🇪🇸 MimapES</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Mi mapa. Mi español.</p>", unsafe_allow_html=True)

mode = st.radio("学習モード",
    ["📷 写真クイズで学ぶ",
     "🌱 写真からスペイン語マインドマップを作る",
     "💡 苦手単語の攻略"],
    horizontal=True)
st.divider()

# モード① 写真クイズ（元の出題・採点・復習の流れを維持）
if mode == "📷 写真クイズで学ぶ":
    st.subheader("📷 写真を見て3つ選ぼう")
    c1,c2,c3 = st.columns(3)
    c1.metric("正解数",st.session_state.score)
    c2.metric("回答数",st.session_state.total)
    accuracy = round(st.session_state.score/st.session_state.total*100) if st.session_state.total else 0
    c3.metric("正解率",f"{accuracy}%")

    q = st.session_state.current_question
    scene = q["scene"]
    st.subheader(scene["title"])
    st.caption(f"テーマ：{scene['ja']} | レベル：{scene['level']}")
    st.image(scene["photo"],use_container_width=True)

    if not st.session_state.answered:
        st.info("写真に関係するスペイン語を3つ選んでください。日本語訳は答え合わせの後に表示されます。")
        with st.form(key=f"answer_form_{st.session_state.round_id}"):
            selected = []
            for i,w in enumerate(q["choices"]):
                if st.checkbox(w[0],key=f"choice_{st.session_state.round_id}_{i}"):
                    selected.append(w[0])
            submitted = st.form_submit_button("答え合わせ",use_container_width=True)
        if submitted:
            if len(selected) != 3:
                st.warning("3つ選択してください。")
            else:
                st.session_state.selected = selected
                st.session_state.total += 1
                st.session_state.is_correct = set(selected) == set(q["correct"])
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
        for w in q["choices"]:
            if w[0] in q["correct"]:
                st.success(f"✓ {w[0]} ＝ {w[1]}")
            else:
                st.write(f"✕ {w[0]} ＝ {w[1]}")
        st.divider()
        st.header("🌍 関連する単語")
        grouped = defaultdict(list)
        for spanish,japanese,category in scene["words"]:
            grouped[category].append((spanish,japanese))
        cols = st.columns(2)
        for i,(category,words) in enumerate(grouped.items()):
            with cols[i%2]:
                with st.container(border=True):
                    st.markdown(f"**📚 {category}**")
                    for spanish,japanese in words:
                        st.write(f"{spanish} — {japanese}")
        st.divider()
        st.header("✍️ 書き写して覚えよう")
        st.write("スペイン語を書き写し、声に出して発音してみましょう。")
        with st.expander("今回の単語を一覧で確認"):
            for spanish,japanese,category in scene["words"]:
                st.write(f"{spanish} — {japanese}")
        if st.button("次の問題へ →",type="primary",use_container_width=True):
            next_question()
            st.rerun()

# モード② 写真からAIマインドマップを生成
elif mode == "🌱 写真からスペイン語マインドマップを作る":
    st.header("🌱 写真からスペイン語のマインドマップを作ろう")
    st.write("写真を1枚アップロードすると、AIが写っているものや関連表現を読み取り、カテゴリー別のスペイン語マインドマップを作ります。")

    photo = st.file_uploader("写真をアップロード（JPG・PNG・WEBP）",
                             type=["jpg", "jpeg", "png", "webp"], key="mindmap_photo")
    level = st.selectbox("スペイン語の学習レベル", ["A1", "A2"], index=1)
    usage_caption()

    if photo is not None:
        st.image(photo, caption="マインドマップにする写真", use_container_width=True)
        st.caption("画像は長辺768px・JPEG品質65に縮小してAIに送信します。")
        if st.button("✨ AIでマインドマップを作成", type="primary", use_container_width=True):
            key = api_key()
            if not key:
                st.error("APIキーが設定されていません。Streamlit SecretsにOPENAI_API_KEYを設定してください。")
            elif not ai_allowed():
                st.warning(f"本日のAI利用上限{DAILY_AI_LIMIT}回に達しました。明日また利用できます。")
            else:
                try:
                    with st.spinner("写真を見ながらスペイン語のマインドマップを作成しています..."):
                        result = mindmap_ai(small_jpeg(photo), level, key)
                    ai_used()
                    st.session_state.mindmap_result = {"level": level, "data": result}
                    st.session_state.mindmap_illustration = None
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"APIエラー {e.response.status_code}。APIキー・支払い・利用上限を確認してください。")
                except Exception as e:
                    st.error(f"マインドマップを作成できませんでした: {e}")

    saved = st.session_state.get("mindmap_result")
    if saved:
        d = saved["data"]
        st.divider()
        st.subheader(f"🧠 {d.get('scene_es', 'Mi mapa')} — {d.get('scene_ja', '')}")
        st.caption(f"学習レベル：{saved.get('level', level)}")
        if d.get("summary"):
            st.write(d["summary"])

        st.markdown("### 🎨 イラスト付きマインドマップ")
        st.write("抽出した単語を、イラスト入りの学習ポスターにします。生成した画像はPNGで保存できます。")
        if st.button("🖼️ イラスト画像を作成", type="primary", use_container_width=True):
            key = api_key()
            if not key:
                st.error("APIキーが設定されていません。")
            elif not ai_allowed():
                st.warning(f"本日のAI利用上限{DAILY_AI_LIMIT}回に達しました。明日また利用できます。")
            else:
                try:
                    categories_json = json.dumps(d.get("categories", []), ensure_ascii=False)
                    with st.spinner("単語を整理してイラスト付きポスターを描いています...（少し時間がかかります）"):
                        image_bytes = illustrated_mindmap_ai(
                            d.get("scene_es", "Mi mapa"), d.get("scene_ja", ""),
                            saved.get("level", level), categories_json, key
                        )
                    ai_used()
                    st.session_state.mindmap_illustration = image_bytes
                    st.rerun()
                except requests.HTTPError as e:
                    status = e.response.status_code if e.response is not None else "不明"
                    st.error(f"画像生成APIエラー {status}。APIの利用資格・支払い・利用上限を確認してください。")
                except Exception as e:
                    st.error(f"イラストを作成できませんでした: {e}")

        illustration = st.session_state.get("mindmap_illustration")
        if illustration:
            st.image(illustration, caption="MimapES イラスト付きマインドマップ", use_container_width=True)
            st.download_button("📥 イラストをPNGで保存", data=illustration,
                               file_name="mimapes_illustrated_mindmap.png", mime="image/png",
                               use_container_width=True)
            st.caption("※画像生成AIは文字を誤って描く場合があります。正確な単語・訳は下の一覧またはCSVでも確認してください。")

        rows = []
        categories = d.get("categories", [])
        for i, category in enumerate(categories):
            with st.container(border=True):
                st.markdown(f"### 🌿 {category.get('name', f'カテゴリー{i+1}')}")
                for word in category.get("words", []):
                    es = word.get("es", "")
                    ja = word.get("ja", "")
                    st.markdown(f"**{es}** — {ja}")
                    if word.get("example_es"):
                        st.caption(f"例：{word.get('example_es')} — {word.get('example_ja', '')}")
                    rows.append({"テーマ": d.get("scene_ja", ""), "カテゴリー": category.get("name", ""),
                                 "スペイン語": es, "日本語": ja,
                                 "例文": word.get("example_es", ""), "例文訳": word.get("example_ja", "")})
        if rows:
            csv = pd.DataFrame(rows).to_csv(index=False, encoding="utf-8-sig")
            st.download_button("📥 マインドマップの単語をCSV保存", data=csv,
                               file_name="mimapes_mindmap_vocabulary.csv", mime="text/csv",
                               use_container_width=True)
            st.caption("写真に写っているものを中心に、関連語や短い例文もまとめています。")
    elif photo is None:
        st.info("まず写真をアップロードしてください。写真に合わせてAIがマインドマップを作ります。")

# モード③ 苦手単語の攻略
elif mode == "💡 苦手単語の攻略":
    st.header("💡 苦手単語の攻略")
    st.write("どうしても覚えられない単語や、似ていて混同する単語を入力してください。AIが覚え方・見分け方・例文・ミニクイズを提案します。")
    words_text = st.text_input(
        "単語を入力（複数ある場合は「/」や「,」で区切る）",
        placeholder="例：de repente / rápidamente",
        max_chars=160,
    )
    level = st.selectbox("スペイン語の学習レベル", ["A1", "A2"], index=1, key="coach_level")
    usage_caption()
    if st.button("✨ 覚え方・見分け方を提案", type="primary", use_container_width=True):
        key = api_key()
        if not words_text.strip():
            st.warning("単語を入力してください。")
        elif not key:
            st.error("APIキーが設定されていません。Streamlit SecretsにOPENAI_API_KEYを設定してください。")
        elif not ai_allowed():
            st.warning(f"本日のAI利用上限{DAILY_AI_LIMIT}回に達しました。明日また利用できます。")
        else:
            try:
                with st.spinner("単語の違いや覚え方を考えています..."):
                    result = word_coach_ai(words_text.strip(), level, key)
                ai_used()
                st.session_state.word_coach_result = {"level": level, "input": words_text.strip(), "data": result}
                st.rerun()
            except requests.HTTPError as e:
                st.error(f"APIエラー {e.response.status_code}。APIキー・支払い・利用上限を確認してください。")
            except Exception as e:
                st.error(f"提案を作成できませんでした: {e}")

    saved_coach = st.session_state.get("word_coach_result")
    if saved_coach:
        d = saved_coach["data"]
        st.divider()
        st.subheader(d.get("title", "単語の攻略ポイント"))
        st.caption(f"入力：{saved_coach.get('input', '')}｜学習レベル：{saved_coach.get('level', level)}")
        if d.get("summary"):
            st.info(d["summary"])

        comparison = d.get("comparison", [])
        if comparison:
            st.markdown("### 🔍 意味と使い方")
            for item in comparison:
                with st.container(border=True):
                    st.markdown(f"**{item.get('word', '')}** — {item.get('meaning', '')}")
                    if item.get("nuance"):
                        st.write(item["nuance"])
                    if item.get("memory_tip"):
                        st.success(f"覚え方：{item['memory_tip']}")

        tips = d.get("how_to_distinguish", [])
        if tips:
            st.markdown("### 🧭 混同しないための見分け方")
            for tip in tips:
                st.write(f"• {tip}")

        examples = d.get("examples", [])
        if examples:
            st.markdown("### 🗣️ 例文で確認")
            for item in examples:
                st.markdown(f"**{item.get('es', '')}**")
                st.write(item.get("ja", ""))
                if item.get("point"):
                    st.caption(item["point"])

        quiz = d.get("quiz", [])
        if quiz:
            st.markdown("### 📝 ミニクイズ")
            for i, item in enumerate(quiz):
                st.write(f"**{i+1}. {item.get('question', '')}**")
                options = item.get("options", [])
                if options:
                    choice = st.radio(
                        f"回答 {i+1}",
                        options,
                        key=f"coach_quiz_{hashlib.md5((saved_coach.get('input','') + str(i)).encode()).hexdigest()}",
                        index=None,
                    )
                    if choice:
                        if choice == item.get("answer"):
                            st.success("正解！")
                        else:
                            st.warning(f"正解：{item.get('answer', '')}")
                        if item.get("explanation"):
                            st.caption(item["explanation"])

st.divider()
usage_caption()
st.caption("MimapES | Mi mapa. Mi español. 🇪🇸")
