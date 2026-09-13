import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="DESTRAVA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_destrava():
    return {"perfis": {}}

_cache = get_cache_destrava()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_laudos', 'laudos_salvos',
    'missoes_concluidas', 'missoes_ignoradas',
    'contador_travas', 'historico_promessas', 'emergencias_usadas',
    'vitorias_registradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_laudo(o_que_evita: str, trava_principal: str, conteudo: str, nivel_sabotagem: int):
    st.session_state.historico_laudos.append({
        'data':            datetime.now().strftime('%d/%m %H:%M'),
        'o_que_evita':     o_que_evita,
        'trava_principal': trava_principal,
        'conteudo':        conteudo,
        'nivel_sabotagem': nivel_sabotagem,
        'missao_status':   None,  # 'concluida' | 'ignorada' | None
    })

def registrar_trava(trava: str):
    """Conta a frequência de cada trava para o Mapa das Travas."""
    if trava not in st.session_state.contador_travas:
        st.session_state.contador_travas[trava] = 0
    st.session_state.contador_travas[trava] += 1

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':                "Login",
    'usuario':              "",
    'api_key':              "",
    'pagina':               "Home",
    'historico_laudos':     [],
    'laudos_salvos':        [],
    'missoes_concluidas':   0,
    'missoes_ignoradas':    0,
    'contador_travas':      {},
    'historico_promessas':  [],  # lista de {'data':..., 'cumpriu': bool}
    'emergencias_usadas':   0,
    'vitorias_registradas': [],  # lista de strings — vitórias que a pessoa já teve
    'debate_historico':     [],
    'debate_key':           0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def gerar_laudo_procrastinacao(o_que_evita: str, trava_selecionada: str, contexto_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um analista de procrastinação — um misto de psicólogo comportamental e perito técnico.
Sua especialidade é identificar a VERDADEIRA causa por trás da procrastinação, que quase nunca é a tarefa em si.
Usuário: {st.session_state.usuario}.

O que a pessoa está evitando: {o_que_evita}
Trava que ela identificou: {trava_selecionada}
{contexto_extra}

FORMATO OBRIGATÓRIO — siga exatamente esta estrutura:

📋 LAUDO DA PROCRASTINAÇÃO

🔍 PROBLEMA REAL DETECTADO:
[2-3 linhas. NÃO diga apenas "você está evitando X". Vá além — explique a real razão psicológica por trás
(ex: "Você não está evitando gravar o vídeo. Você está evitando a possibilidade de gravar e não ter resultado.
Seu cérebro está tentando te proteger da frustração.") Seja específico para a situação descrita.]

🎯 NÍVEL DE SABOTAGEM: [X]%
[1 linha explicando esse número — baseado na intensidade da trava e há quanto tempo isso se repete]

🔒 TRAVA PRINCIPAL: {trava_selecionada}
[1-2 linhas explicando como essa trava específica se manifesta nesse caso]

⚡ O QUE SEU CÉREBRO ESTÁ REALMENTE FAZENDO:
[1-2 linhas — explique o mecanismo de defesa psicológico em ação, de forma simples e validante, sem julgar a pessoa]

🧠 PARECER FINAL:
[1-2 frases diretas. Termine com uma frase de impacto que reframe a procrastinação como proteção, não fraqueza]

REGRAS CRÍTICAS:
- O nível de sabotagem deve ser coerente com a intensidade descrita — não invente números aleatórios
- Tom: técnico mas acolhedor — você é um analista, não um juiz
- NUNCA culpe ou envergonhe a pessoa — procrastinação é proteção, não falha de caráter
- Seja específico para a situação real descrita, não genérico
- Português do Brasil, direto"""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Estou evitando: {o_que_evita}. O que sinto: {trava_selecionada}. {contexto_extra}"},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def gerar_missao_ia(o_que_evita: str, trava: str, laudo: str) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você cria "missões mínimas" para destravar procrastinação — ações tão pequenas e ridículas de fáceis
que a resistência psicológica não consegue se ativar.

A pessoa está evitando: {o_que_evita}
Trava identificada: {trava}
Diagnóstico: {laudo[:300]}

Crie UMA missão de no máximo 3 minutos. A missão NÃO PODE ser a tarefa completa.
Ela deve ser o menor passo físico possível que abre a porta para a tarefa, sem exigir que a pessoa "termine" nada.

Exemplos do estilo esperado:
- Tarefa evitada: gravar vídeo → Missão: "Não grave o vídeo. Apenas abra a câmera e fique olhando para ela por 30 segundos. Depois feche."
- Tarefa evitada: estudar → Missão: "Não estude. Apenas abra o material e leia só o título da primeira página."
- Tarefa evitada: ligar para alguém → Missão: "Não ligue ainda. Apenas digite o número e deixe o dedo sobre o botão de chamar por 10 segundos."

FORMATO:

🎯 MISSÃO DE [X] MINUTOS

[Nome curto e direto da missão]

[Instrução passo a passo, bem específica, em 2-4 linhas. Use a fórmula "Não faça X. Apenas faça Y."]

💡 Por que isso funciona: [1 linha explicando por que esse passo mínimo contorna a trava específica]

Português do Brasil, tom direto e ligeiramente provocador (no bom sentido)."""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Crie a missão mínima para: {o_que_evita}"},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def debater_voz_interior(fala_usuario: str, historico: list) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um debatedor socrático especializado em confrontar a voz sabotadora interna de quem procrastina.
Usuário: {st.session_state.usuario}.

A pessoa vai dizer frases de autossabotagem (ex: "não vai dar certo", "sou incapaz", "vai ser ruim").
Sua função é questionar essas afirmações com perguntas diretas e lógicas, no estilo socrático —
sem dar sermão, sem ser agressivo, apenas expondo a falta de evidência por trás do medo.

REGRAS:
- Responda com 1-2 frases curtas, geralmente uma pergunta direta
- Questione: "Qual evidência você tem disso?", "Isso é um fato ou um medo?", "Já aconteceu antes ou é uma previsão?"
- Quando a pessoa admitir que não tem evidência, aponte isso com clareza mas sem ironia
- Nunca seja condescendente ou debochado
- Tom: firme, lógico, like um bom terapeuta cognitivo-comportamental
- Português do Brasil, frases curtas"""

        mensagens = [{"role": "system", "content": system}]
        for h in historico[-8:]:
            mensagens.append({"role": h["role"], "content": h["content"]})
        mensagens.append({"role": "user", "content": fala_usuario})

        response = client.chat.completions.create(
            messages=mensagens,
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def gerar_resposta_emergencia(situacao_emergencia: str) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        vitorias = st.session_state.vitorias_registradas
        total_missoes = st.session_state.missoes_concluidas
        vitorias_texto = ", ".join(vitorias[-5:]) if vitorias else "ainda não há vitórias registradas"

        system = f"""MODO EMERGÊNCIA ATIVADO. A pessoa está prestes a desistir de algo importante AGORA.
Usuário: {st.session_state.usuario}.
Total de missões já concluídas anteriormente: {total_missoes}.
Vitórias anteriores registradas: {vitorias_texto}.

Sua função AGORA é ser firme, direto e presente — como alguém que segura a pessoa pelos ombros e não deixa ela desistir.

ESTRUTURA DA RESPOSTA:

🚨 MODO EMERGÊNCIA

[1 frase curta e firme reconhecendo o momento — sem fazer terapia longa, sem fazer pergunta. Apenas presença.]

📊 LEMBRETE DOS SEUS NÚMEROS:
Você já completou {total_missoes} missão(ões) antes. Isso não é a primeira vez que você sente vontade de parar — e nas outras vezes você continuou.

🏆 SUAS VITÓRIAS ANTERIORES:
{vitorias_texto if vitorias else "Você ainda está construindo seu histórico de vitórias — essa pode ser a primeira."}

⚡ AÇÃO IMEDIATA (próximos 60 segundos):
[Uma instrução física extremamente simples e imediata — respirar, levantar, beber água, etc — seguida de voltar à tarefa por apenas mais 2 minutos]

[Termine com 1 frase curta e direta, tipo um soco no peito motivacional sem ser piegas]

Tom: firme, presente, sem julgamento, sem sermão longo. Português do Brasil."""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": situacao_emergencia or "Estou prestes a desistir agora."},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def detectar_autoengano(frase: str) -> str:
    """Analisa a frase em busca de padrões de procrastinação/racionalização."""
    padroes_suspeitos = [
        "deixar para amanhã", "depois eu faço", "mais tarde", "não tenho tempo agora",
        "vou fazer quando", "preciso me preparar mais", "ainda não é a hora",
        "vou começar segunda", "ano que vem", "mês que vem", "semana que vem",
    ]
    frase_lower = frase.lower()
    for padrao in padroes_suspeitos:
        if padrao in frase_lower:
            return padrao
    return None

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_laudos)
    concluidas = st.session_state.missoes_concluidas

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F0FDFA;border:1px solid #2DD4BF;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} laudos gerados · {concluidas} missões concluídas</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"destrava_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="destrava3"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# --- RENDERIZAÇÃO VISUAL DO LAUDO ---
def renderizar_laudo_visual(texto_laudo: str):
    percentuais = re.findall(r'(\d+)%', texto_laudo)
    nivel_sabotagem = int(percentuais[0]) if percentuais else 50

    cor = "#DC2626" if nivel_sabotagem >= 70 else ("#D97706" if nivel_sabotagem >= 40 else "#059669")

    st.markdown(f"""
    <div class="laudo-box">
        <div class="laudo-header">
            <div class="laudo-titulo">📋 LAUDO DA PROCRASTINAÇÃO</div>
            <div style="font-size:0.78em;color:#888;">Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:2.4em;font-weight:700;color:{cor};font-family:'Playfair Display',serif;">{nivel_sabotagem}%</div>
            <div style="font-size:0.9em;color:#555;">🎯 Nível de sabotagem</div>
            <div class="barra-bg" style="max-width:280px;margin:8px auto;"><div class="barra-fill" style="width:{nivel_sabotagem}%;background:{cor};"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='card'>{texto_laudo}</div>", unsafe_allow_html=True)
    return nivel_sabotagem

# ============================================================
# TELA: LOGIN
# ============================================================
if 'contador_travas' not in st.session_state: st.session_state['contador_travas'] = None
if 'debate_historico' not in st.session_state: st.session_state['debate_historico'] = []
if 'emergencias_usadas' not in st.session_state: st.session_state['emergencias_usadas'] = None
if 'historico_laudos' not in st.session_state: st.session_state['historico_laudos'] = []
if 'historico_promessas' not in st.session_state: st.session_state['historico_promessas'] = []
if 'laudos_salvos' not in st.session_state: st.session_state['laudos_salvos'] = None
if 'missoes_concluidas' not in st.session_state: st.session_state['missoes_concluidas'] = []
if 'missoes_ignoradas' not in st.session_state: st.session_state['missoes_ignoradas'] = []
if 'vitorias_registradas' not in st.session_state: st.session_state['vitorias_registradas'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 DESTRAVA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":


    # ── BOTÕES DE AÇÃO IMEDIATA — sempre visíveis no topo ──
    col_travado, col_emergencia = st.columns(2)
    with col_travado:
        if st.button("🚨 ESTOU TRAVADO", key="btn_travado_top", use_container_width=True):
            st.session_state.pagina = "Travado"
            st.rerun()
    with col_emergencia:
        st.markdown('<div class="btn-emergencia">', unsafe_allow_html=True)
        if st.button("🆘 ESTOU PRESTES A ABANDONAR", key="btn_emergencia_top", use_container_width=True):
            st.session_state.pagina = "Emergencia"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


    # TABS
    _tab_Home, _tab_Debate, _tab_Autoengano, _tab_Mapa, _tab_Salvos, _tab_Progresso = st.tabs(['🏠 Home', '💬 Debate', '⚠️ Autoengano', '📊 Mapa', '❤️ Salvos', '📈 Progresso'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_destrava")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_destrava", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}. ⚡")
            st.markdown("<span class='badge'>Pronto-socorro ativo</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="destrava3_d2"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        total_laudos = len(st.session_state.historico_laudos)
        if total_laudos == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        taxa_conclusao = round(
            st.session_state.missoes_concluidas /
            max(1, st.session_state.missoes_concluidas + st.session_state.missoes_ignoradas) * 100
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_laudos}</div><div>Travas diagnosticadas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.missoes_concluidas}</div><div>Missões concluídas ✅</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.emergencias_usadas}</div><div>Emergências superadas 🆘</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa_conclusao}%</div><div>Taxa de destravamento</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Procrastinação não é fraqueza de caráter. É o seu cérebro tentando te proteger de uma dor que talvez nem aconteça.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada botão faz")
        guia = {
            "🚨 Estou travado":      "O fluxo principal — diagnostica a trava real e te dá uma missão de 3 minutos para destravar",
            "🆘 Prestes a abandonar":"Modo emergência — quando você está quase desistindo de algo importante agora",
            "💬 Debate":             "Confronte a voz sabotadora interna com perguntas socráticas",
            "⚠️ Autoengano":         "Cole uma frase de adiamento e veja se é racionalização disfarçada",
            "📊 Mapa":               "Veja quais são seus padrões de sabotagem mais frequentes ao longo do tempo",
            "❤️ Salvos":             "Laudos que você guardou para revisar depois",
            "📈 Progresso":          "Seu histórico completo de travas e vitórias",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_laudos:
            st.markdown("### 🕐 Últimas Travas Diagnosticadas")
            for item in reversed(st.session_state.historico_laudos[-4:]):
                status = "✅" if item.get('missao_status') == 'concluida' else ("⏸️" if item.get('missao_status') == 'ignorada' else "🔵")
                st.markdown(
                    f"<div class='hist-item'>{status} <span class='badge'>{item.get('trava_principal', '')}</span> "
                    f"<span class='badge-amarelo'>{item.get('nivel_sabotagem', 0)}% sabotagem</span> "
                    f"<small style='color:#888'>{item['data']}</small><br>"
                    f"<small>{item.get('o_que_evita', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ========================
        # ESTOU TRAVADO — fluxo principal
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_destrava")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_destrava")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Debate:
        st.header("💬 Confronto da Voz Interior")
        st.markdown("Escreva o que sua voz sabotadora está te dizendo agora. A IA vai questionar essa voz com você.")

        if 'debate_key' not in st.session_state:
            st.session_state.debate_key = 0

        if st.session_state.debate_historico:
            for msg in st.session_state.debate_historico:
                if msg['role'] == 'user':
                    st.markdown(f"<div class='debate-user'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='debate-ia'><b>🧠 Destrava:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#F0FDFA;border:1px dashed #2DD4BF;border-radius:12px;padding:16px;text-align:center;color:#0F766E;">
            💬 Escreva algo como "não vai dar certo" ou "sou incapaz disso" — e veja a IA confrontar essa afirmação com você.
            </div>""", unsafe_allow_html=True)

        # Sugestões rápidas para começar
        st.markdown("**⚡ Frases comuns — clique para usar:**")
        col_s1, col_s2, col_s3 = st.columns(3)
        sugestoes_debate = ["Não vai dar certo.", "Sou incapaz disso.", "Vai ser ruim de qualquer jeito."]
        for col, sug in zip([col_s1, col_s2, col_s3], sugestoes_debate):
            if col.button(f"\"{sug}\"", key=f"sug_debate_{sug}"):
                with st.spinner("..."):
                    resposta = debater_voz_interior(sug, st.session_state.debate_historico)
                    if resposta: st.session_state['res_debate_destra1'] = str(resposta)
                st.session_state.debate_historico.append({"role": "user", "content": sug})
                st.session_state.debate_historico.append({"role": "assistant", "content": resposta})
                st.session_state.debate_key += 1
                st.rerun()

        fala = st.text_input(
            "O que a voz sabotadora está dizendo:",
            placeholder="ex: Não vai dar certo...",
            key=f"debate_input_{st.session_state.debate_key}"
        )

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 Confrontar essa voz", key="btn_confrontar_voz", use_container_width=True):
                if fala.strip():
                    with st.spinner("..."):
                        resposta = debater_voz_interior(fala, st.session_state.debate_historico)
                        if resposta: st.session_state['res_debate_destra2'] = str(resposta)
                    st.session_state.debate_historico.append({"role": "user", "content": fala})
                    st.session_state.debate_historico.append({"role": "assistant", "content": resposta})
                    st.session_state.debate_key += 1
                    st.rerun()
                else:
                    st.warning("Escreva o que a voz está dizendo antes de confrontar.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="btn_limpar_debate", use_container_width=True):
                st.session_state.debate_historico = []
                st.session_state.debate_key += 1
                st.rerun()

        # ========================
        # DETECTOR DE AUTOENGANO
        # ========================

    with _tab_Autoengano:
        st.header("⚠️ Detector de Autoengano")
        st.markdown("Cole a frase que você está pensando agora. O app verifica se é racionalização disfarçada.")

        frase_check = st.text_input("O que você está pensando em fazer (ou não fazer)?",
            placeholder="ex: Vou deixar para amanhã, hoje não dá tempo...", key="destrava2")

        if st.button("🔍 ANALISAR", key="destrava4"):
            if frase_check.strip():
                padrao = detectar_autoengano(frase_check)

                # Registra a promessa
                st.session_state.historico_promessas.append({
                    'data': datetime.now().strftime('%d/%m %H:%M'),
                    'frase': frase_check,
                    'padrao_detectado': padrao,
                    'cumpriu': None,
                })

                if padrao:
                    promessas_similares = [
                        p for p in st.session_state.historico_promessas[:-1]
                        if p['padrao_detectado'] == padrao
                    ]
                    total_similares = len(promessas_similares) + 1
                    cumpridas = sum(1 for p in promessas_similares if p['cumpriu'] is True)

                    st.markdown(f"""
                    <div class="alerta-autoengano">
                    <div style="font-size:1.1em;font-weight:700;color:#C2410C;">⚠️ Possível racionalização detectada</div>
                    <p style="margin-top:8px;">Você usou um padrão parecido com <b>"{padrao}"</b>.</p>
                    {"<p>Nas últimas <b>" + str(total_similares-1) + "</b> vezes que você disse algo parecido, apenas <b>" + str(cumpridas) + "</b> realmente viraram ação.</p>" if total_similares > 1 else "<p>Essa é a primeira vez que você registra esse padrão — vamos acompanhar se ele se repete.</p>"}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ Não detectei padrões clássicos de procrastinação nessa frase. Pode ser uma decisão genuína.")
            else:
                st.warning("Escreva a frase para analisar.")

        # Histórico de promessas para acompanhamento
        if st.session_state.historico_promessas:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 📜 Suas frases registradas — cumpriu?")
            pendentes = [p for p in st.session_state.historico_promessas if p['cumpriu'] is None]
            if pendentes:
                for i, p in enumerate(pendentes[-5:]):
                    idx_real = st.session_state.historico_promessas.index(p)
                    st.markdown(f"<div class='hist-item'>\"{p['frase']}\" <small style='color:#888'>— {p['data']}</small></div>", unsafe_allow_html=True)
                    col_sim, col_nao = st.columns(2)
                    with col_sim:
                        if st.button("✅ Cumpri", key=f"cumpriu_sim_{idx_real}"):
                            st.session_state.historico_promessas[idx_real]['cumpriu'] = True
                            st.rerun()
                    with col_nao:
                        if st.button("❌ Não cumpri", key=f"cumpriu_nao_{idx_real}"):
                            st.session_state.historico_promessas[idx_real]['cumpriu'] = False
                            st.rerun()

            respondidas = [p for p in st.session_state.historico_promessas if p['cumpriu'] is not None]
            if respondidas:
                taxa_cumprimento = round(sum(1 for p in respondidas if p['cumpriu']) / len(respondidas) * 100)
                st.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa_cumprimento}%</div><div>Taxa real de cumprimento das suas promessas</div></div>", unsafe_allow_html=True)

        # ========================
        # MAPA DAS TRAVAS
        # ========================

    with _tab_Mapa:
        st.header("📊 Mapa das Suas Travas")
        st.markdown("Os padrões de sabotagem mais frequentes que aparecem no seu histórico.")

        if not st.session_state.contador_travas:
            st.info("Ainda não há dados suficientes. Use o botão 🚨 Estou Travado algumas vezes para o mapa aparecer.")
        else:
            total_travas = sum(st.session_state.contador_travas.values())
            ranking = sorted(st.session_state.contador_travas.items(), key=lambda x: x[1], reverse=True)

            st.markdown(f"### Baseado em {total_travas} diagnóstico(s)")
            for i, (trava, count) in enumerate(ranking):
                pct = round(count / total_travas * 100)
                st.markdown(f"""
                <div class="ranking-item">
                    <div class="ranking-num">{i+1}.</div>
                    <div style="flex:1;">
                        <div style="font-weight:600;">{trava}</div>
                        <div class="barra-bg"><div class="barra-fill" style="width:{pct}%;background:#0F766E;"></div></div>
                    </div>
                    <div style="font-weight:700;color:#0F766E;font-size:1.2em;">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)

            trava_principal = ranking[0][0]
            st.markdown(f"<div class='card'>🎯 <strong>Seu maior sabotador é:</strong> {trava_principal}<br><br>Saber qual é o padrão dominante é o primeiro passo para neutralizá-lo antes que ele apareça da próxima vez.</div>", unsafe_allow_html=True)

        # ========================
        # SALVOS
        # ========================

    with _tab_Salvos:
        st.header("❤️ Laudos Salvos")

        if not st.session_state.laudos_salvos:
            st.info("Nenhum laudo salvo ainda.")
        else:
            for i, item in enumerate(reversed(st.session_state.laudos_salvos)):
                idx_real = len(st.session_state.laudos_salvos) - 1 - i
                with st.expander(f"[{item.get('trava_principal','')}] {item.get('o_que_evita','')[:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name="laudo_procrastinacao.txt", mime="text/plain", key=f"dl_salvo_{i}")
                    with col_del:
                        if st.button("🗑️", key=f"del_salvo_{i}"):
                            st.session_state.laudos_salvos.pop(idx_real)
                            st.rerun()

        # ========================
        # PROGRESSO
        # ========================

    with _tab_Progresso:
        st.header("📈 Meu Progresso")

        total = len(st.session_state.historico_laudos)
        concluidas = st.session_state.missoes_concluidas
        ignoradas = st.session_state.missoes_ignoradas
        emergencias = st.session_state.emergencias_usadas

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Travas diagnosticadas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{concluidas}</div><div>Missões concluídas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{ignoradas}</div><div>Missões adiadas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{emergencias}</div><div>Emergências enfrentadas</div></div>", unsafe_allow_html=True)

        if st.session_state.vitorias_registradas:
            st.markdown("### 🏆 Suas Vitórias Registradas")
            for v in reversed(st.session_state.vitorias_registradas[-15:]):
                st.markdown(f"<div class='hist-item'>🏆 {v}</div>", unsafe_allow_html=True)

        if st.session_state.historico_laudos:
            st.markdown("### 📜 Histórico Completo")
            historico_txt = "\n\n".join(
                f"[{l['data']}] {l['trava_principal']} — {l['o_que_evita']} ({l['nivel_sabotagem']}% sabotagem)\n{l['conteudo']}\n{'─'*40}"
                for l in st.session_state.historico_laudos
            )
            st.download_button("⬇️ Exportar histórico completo (.txt)", data=historico_txt,
                file_name="historico_destrava.txt", mime="text/plain", key="destrava1")

            for i, item in enumerate(reversed(st.session_state.historico_laudos)):
                idx_real = len(st.session_state.historico_laudos) - 1 - i
                status = "✅ Concluída" if item.get('missao_status') == 'concluida' else ("⏸️ Adiada" if item.get('missao_status') == 'ignorada' else "🔵 Pendente")
                with st.expander(f"[{item.get('trava_principal', '')}] {item.get('o_que_evita', '')[:60]} — {status} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("❤️ Salvar", key=f"sv_hist_{i}"):
                            st.session_state.laudos_salvos.append(item.copy())
                            st.success("Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_laudos.pop(idx_real)
                            st.rerun()

            if st.button("🗑️ Limpar Todo o Histórico", key="destrava5"):
                st.session_state.historico_laudos = []
                st.session_state.contador_travas = {}
                st.rerun()
        else:
            st.info("Nenhuma trava diagnosticada ainda. Use o botão 🚨 Estou Travado para começar!")

        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Destrava — O Pronto-Socorro da Procrastinação com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
        )


# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
