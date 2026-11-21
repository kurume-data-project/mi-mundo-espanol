import random
import hashlib
import io
import json
from datetime import date
from collections import defaultdict

import pandas as pd
import streamlit as st
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title="MimapES | Mi mapa. Mi español.", page_icon="🇪🇸", layout="wide")

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

# セッション状態
defaults = {"score":0,"total":0,"round_id":0,"history":[],"current_question":None,
            "answered":False,"selected":[],"is_correct":False}
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
st.markdown("<p class='sub-title'>スペイン語の世界を広げよう！</p>", unsafe_allow_html=True)

mode = st.radio("学習モード", [
    "📷 写真クイズで学ぶ",
    "🌱 写真からマインドマップを作る",
    "🔎 AIで単語を探究する",
    "🖼️ AIで写真を認識する",
], horizontal=True)
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

# モード② 写真アップロード＋テーマ選択＋単語マインドマップ
elif mode == "🌱 写真からマインドマップを作る":
    st.header("🌱 写真からスペイン語のマインドマップを作ろう")
    st.write("写真をアップロードし、テーマを選ぶと、関連する単語をカテゴリー別に表示します。")
    st.info("写真の内容をAIで自動認識する機能はありません。選択したテーマに登録された単語を表示します。")

    photo = st.file_uploader("写真をアップロード（JPG・PNG・WEBP）",
                             type=["jpg","jpeg","png","webp"],key="mindmap_photo")
    theme = st.selectbox("写真のテーマを選んでください",list(MINDMAP.keys()),key="mindmap_theme")
    title,groups = MINDMAP[theme]
    if photo is not None:
        st.image(photo,caption=f"アップロードした写真：{theme}",use_container_width=True)
    else:
        st.caption("写真をアップロードすると、ここに表示されます。")

    st.divider()
    st.subheader("🧠 スペイン語マインドマップ")
    st.markdown(f"<div class='center-node'>{theme}<br><span style='font-size:15px;font-weight:normal'>{title}</span></div>",
                unsafe_allow_html=True)
    cols = st.columns(2)
    rows = []
    for i,(category,words) in enumerate(groups.items()):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"**🌿 {category}**")
                for spanish,japanese in words:
                    st.markdown(f"- **{spanish}** — {japanese}")
                    rows.append({"テーマ":theme,"カテゴリー":category,
                                 "スペイン語":spanish,"日本語":japanese})
    st.divider()
    st.subheader("📥 単語をダウンロード")
    csv = pd.DataFrame(rows).to_csv(index=False,encoding="utf-8-sig")
    st.download_button("このテーマの単語をCSVで保存",data=csv,
                       file_name="mimapes_vocabulary.csv",
                       mime="text/csv",use_container_width=True)
    st.caption("単語データは学習用の基本語彙です。地域や場面によって別の表現が使われる場合があります。")

# AI共通設定：1ブラウザーセッションにつき1日5回
DAILY_LIMIT = 5
TODAY = date.today().isoformat()
if st.session_state.get("ai_usage_date") != TODAY:
    st.session_state.ai_usage_date = TODAY
    st.session_state.ai_usage_count = 0
if "ai_usage_count" not in st.session_state:
    st.session_state.ai_usage_count = 0

st.divider()
st.subheader("🤖 AI利用状況")
st.write(f"本日の利用：**{st.session_state.ai_usage_count} / {DAILY_LIMIT} 回**")
st.caption("単語探究・写真認識を合わせた回数です。同じ結果がキャッシュから表示される場合は追加課金されません。")


def get_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None
    if not api_key:
        st.error("APIキーが設定されていません。Streamlit の Settings → Secrets に OPENAI_API_KEY を設定してください。")
        return None
    return OpenAI(api_key=api_key)


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def explore_word_cached(word: str, level: str):
    client = get_openai_client()
    if client is None:
        return ""
    response = client.responses.create(
        model="gpt-6-luna",
        max_output_tokens=450,
        input=[{"role": "user", "content": (
            "あなたは日本語で説明するスペイン語教師です。"
            f"学習レベルは{level}。単語・表現「{word}」を短く説明してください。"
            "意味、品詞・性数（該当する場合）、使い方の注意1点、"
            "短い例文2つ（スペイン語と日本語訳）だけを、見出し付きで日本語で回答。"
            "推測で断定せず、スペイン（スペイン本土）で一般的な用法を優先。"
        )}]
    )
    return response.output_text


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def recognize_photo_cached(image_bytes: bytes, mime_type: str, language_level: str):
    client = get_openai_client()
    if client is None:
        return ""
    import base64
    encoded = base64.b64encode(image_bytes).decode("ascii")
    data_url = f"data:{mime_type};base64,{encoded}"
    response = client.responses.create(
        model="gpt-6-luna",
        max_output_tokens=550,
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": (
                "この写真に実際に写っているものをスペイン語学習用に説明してください。"
                f"レベルは{language_level}。写真から確認できる物・人・場所を最大8個選び、"
                "スペイン語（冠詞付き名詞）—日本語訳の一覧にしてください。"
                "最後に、写真を説明する短いスペイン語文を2文と日本語訳を付けてください。"
                "見えないものを推測して追加しないでください。回答は日本語で簡潔に。"
            )},
            {"type": "input_image", "image_url": data_url, "detail": "low"}
        ]}]
    )
    return response.output_text


def can_use_ai():
    if st.session_state.ai_usage_count >= DAILY_LIMIT:
        st.warning("本日のAI利用上限（5回）に達しました。明日また利用してください。")
        return False
    return True


if mode == "🔎 AIで単語を探究する":
    st.header("🔎 AI単語探究")
    st.write("スペイン語の単語や表現の意味・使い方・例文を確認できます。")
    word = st.text_input("調べたいスペイン語", placeholder="例：de repente")
    level = st.selectbox("学習レベル", ["A1", "A2", "B1"], index=1)
    if st.button("単語を調べる", type="primary", use_container_width=True):
        cleaned = word.strip()
        if not cleaned:
            st.warning("単語または表現を入力してください。")
        elif len(cleaned) > 80:
            st.warning("入力は80文字以内にしてください。")
        elif can_use_ai():
            with st.spinner("単語を調べています…"):
                try:
                    answer = explore_word_cached(cleaned, level)
                    if answer:
                        st.session_state.ai_usage_count += 1
                        st.markdown(answer)
                    else:
                        st.error("回答を取得できませんでした。APIキーを確認してください。")
                except Exception as e:
                    st.error(f"AIの呼び出しに失敗しました：{e}")


elif mode == "🖼️ AIで写真を認識する":
    st.header("🖼️ AI写真認識")
    st.write("写真に写っているものをAIが確認し、スペイン語の単語と例文を作ります。")
    photo_ai = st.file_uploader("写真を選択（JPG・PNG・WEBP、最大5MB）",
                                type=["jpg", "jpeg", "png", "webp"], key="ai_photo")
    level_ai = st.selectbox("学習レベル", ["A1", "A2", "B1"], index=1, key="photo_level")
    if photo_ai is not None:
        raw = photo_ai.getvalue()
        if len(raw) > 5 * 1024 * 1024:
            st.error("ファイルサイズは5MB以下にしてください。")
        else:
            st.image(raw, caption="認識する写真", use_container_width=True)
            if st.button("この写真をAIで認識する", type="primary", use_container_width=True):
                if can_use_ai():
                    try:
                        # 画像を長辺768px・JPEG品質65に縮小して送信量を抑える
                        img = Image.open(io.BytesIO(raw)).convert("RGB")
                        img.thumbnail((768, 768))
                        buf = io.BytesIO()
                        img.save(buf, format="JPEG", quality=65, optimize=True)
                        compressed = buf.getvalue()
                        digest = hashlib.sha256(compressed + level_ai.encode()).hexdigest()
                        with st.spinner("写真を確認しています…"):
                            answer = recognize_photo_cached(compressed, "image/jpeg", level_ai)
                        if answer:
                            st.session_state.ai_usage_count += 1
                            st.markdown(answer)
                        else:
                            st.error("認識結果を取得できませんでした。APIキーを確認してください。")
                    except Exception as e:
                        st.error(f"写真認識に失敗しました：{e}")
    st.caption("写真は長辺768pxに縮小し、低詳細度で送信します。写真認識は単語探究より画像入力分の費用がかかります。")

st.divider()
st.caption("MimapES | Mi mapa. Mi español. 🇪🇸")
