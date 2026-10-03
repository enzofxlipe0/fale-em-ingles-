import os
import json
import random
import string

import pygame
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import deepl

from dotenv import load_dotenv


# =========================================================
# INICIALIZAÇÃO
# =========================================================

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("English Speak")

clock = pygame.time.Clock()


# =========================================================
# FONTES
# =========================================================

fonte_titulo = pygame.font.Font(None, 72)
fonte_grande = pygame.font.Font(None, 56)
fonte_media = pygame.font.Font(None, 40)
fonte_pequena = pygame.font.Font(None, 30)


# =========================================================
# CORES
# =========================================================

FUNDO = (25, 30, 45)
BRANCO = (255, 255, 255)
CINZA = (180, 180, 180)

AZUL = (70, 130, 200)
AZUL_HOVER = (100, 180, 255)

VERDE = (80, 200, 120)
VERMELHO = (220, 80, 80)

AMARELO = (255, 220, 80)


# =========================================================
# DEEPL
# =========================================================

load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if not DEEPL_API_KEY:

    print("❌ Chave da DeepL não encontrada!")
    print()
    print("Crie um arquivo .env contendo:")
    print("DEEPL_API_KEY=sua_chave")

    pygame.quit()
    exit()


translator = deepl.DeepLClient(
    DEEPL_API_KEY
)


# =========================================================
# ÁUDIO
# =========================================================

sample_rate = 44100

os.makedirs(
    "gravações",
    exist_ok=True
)


# =========================================================
# DIFICULDADES
# =========================================================

dificuldades = {

    "Fácil": {
        "tempo": 6,
        "pontos": 10,
        "xp": 5,
        "vidas": 5,

        "palavras": [
            "casa", "gato", "cachorro", "água", "comida",
            "carro", "livro", "sol", "lua", "amigo",
            "bola", "mesa", "cadeira", "porta", "janela",
            "escola", "mãe", "pai", "irmão", "família",
            "água", "fogo", "terra", "céu", "mar",
            "árvore", "flor", "chuva", "neve", "vento",
            "dia", "noite", "homem", "mulher", "criança",
            "peixe", "pássaro", "cavalo", "casa", "rua",
            "telefone", "computador", "jogo", "filme", "música",
            "feliz", "triste", "grande", "pequeno", "rápido"
        ]
    },


    "Médio": {
        "tempo": 5,
        "pontos": 20,
        "xp": 10,
        "vidas": 4,

        "palavras": [
            "montanha", "floresta", "viagem", "cidade",
            "telefone", "jardim", "computador", "trabalho",
            "biblioteca", "hospital", "aeroporto", "estação",
            "restaurante", "mercado", "praia", "ilha",
            "ponte", "edifício", "quarto", "cozinha",
            "banheiro", "escritório", "professor", "estudante",
            "médico", "engenheiro", "motorista", "polícia",
            "dinheiro", "mochila", "relógio", "sapato",
            "camisa", "caderno", "caneta", "janela",
            "viagem", "aventura", "história", "planeta",
            "universo", "energia", "esporte", "futebol",
            "basquete", "computador", "internet", "notícia"
        ]
    },


    "Difícil": {
        "tempo": 4,
        "pontos": 30,
        "xp": 20,
        "vidas": 3,

        "palavras": [
            "tempestade",
            "conhecimento",
            "desenvolvimento",
            "experiência",
            "responsabilidade",
            "curiosidade",
            "imaginação",
            "tecnologia",
            "comunicação",
            "possibilidade",
            "determinação",
            "criatividade",
            "inteligência",
            "concentração",
            "oportunidade",
            "personalidade",
            "informação",
            "educação",
            "sociedade",
            "natureza",
            "ambiente",
            "comportamento",
            "descoberta",
            "experimento",
            "universidade",
            "astronauta",
            "engenharia",
            "programação",
            "eletricidade",
            "gravidade",
            "atmosfera",
            "temperatura",
            "velocidade",
            "distância",
            "movimento",
            "estrutura",
            "material",
            "criatura",
            "civilização",
            "exploração",
            "sobrevivência",
            "estratégia",
            "mistério",
            "fenômeno",
            "desafio",
            "competição",
            "habilidade",
            "memória"
        ]
    },


    "Extremo": {
        "tempo": 3,
        "pontos": 50,
        "xp": 35,
        "vidas": 2,

        "palavras": [
            "extraordinário",
            "incompreensível",
            "aproximadamente",
            "independentemente",
            "simultaneamente",
            "consequentemente",
            "característica",
            "conscientização",
            "responsabilização",
            "desenvolvimento",
            "desnecessariamente",
            "inquestionavelmente",
            "principalmente",
            "especificamente",
            "aprofundamento",
            "representatividade",
            "sustentabilidade",
            "biodiversidade",
            "industrialização",
            "globalização",
            "democratização",
            "experimentação",
            "interpretação",
            "investigação",
            "transformação",
            "comportamental",
            "psicológico",
            "sociológico",
            "meteorológico",
            "astronômico",
            "tecnológico",
            "cientificamente",
            "extraoficialmente",
            "involuntariamente",
            "inevitavelmente",
            "surpreendentemente",
            "aprofundadamente",
            "consequentemente",
            "desproporcionalmente"
        ]
    },


    "Impossível": {
        "tempo": 2,
        "pontos": 100,
        "xp": 60,
        "vidas": 1,

        "palavras": [
            "inconstitucionalidade",
            "otorrinolaringologista",
            "eletroencefalograma",
            "esternocleidomastóideo",
            "paralelepípedo",
            "desoxirribonucleico",
            "pneumoultramicroscopicossilicovulcanoconiótico",
            "anticonstitucionalmente",
            "hipopotomonstrosesquipedaliofobia",
            "eletrocardiograma",
            "gastroenterologista",
            "oftalmologista",
            "neuropsicofarmacologia",
            "extraordinariamente",
            "incompreensibilidade",
            "multidisciplinaridade",
            "internacionalização",
            "responsabilização",
            "descontextualização",
            "incompatibilidade",
            "indissociabilidade",
            "proporcionalidade",
            "representatividade",
            "constitucionalmente"
        ]
    }
}
# =========================================================
# XP NECESSÁRIA
# =========================================================

requisitos = {

    "Fácil": 0,
    "Médio": 30,
    "Difícil": 100,
    "Extremo": 200,
    "Impossível": 350

}


# =========================================================
# SALVAR XP
# =========================================================

ARQUIVO_XP = "progresso.json"


if os.path.exists(ARQUIVO_XP):

    try:

        with open(
            ARQUIVO_XP,
            "r",
            encoding="utf-8"
        ) as arquivo:

            progresso = json.load(arquivo)

        experiencia = progresso.get(
            "experiencia",
            0
        )

    except:

        experiencia = 0

else:

    experiencia = 0


def salvar_experiencia():

    progresso = {
        "experiencia": experiencia
    }

    with open(
        ARQUIVO_XP,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            progresso,
            arquivo,
            indent=4
        )


# =========================================================
# VARIÁVEIS DO JOGO
# =========================================================

tela = "menu"

dificuldade_atual = None

palavra_atual = ""

resposta_correta = ""

resposta_jogador = ""

resultado = ""

pontos = 0

vidas = 0

rodada = 0


# =========================================================
# DIFICULDADE DESBLOQUEADA
# =========================================================

def dificuldade_desbloqueada(nome):

    return experiencia >= requisitos[nome]


# =========================================================
# DESENHAR TEXTO
# =========================================================

def desenhar_texto(
    texto,
    fonte,
    cor,
    x,
    y
):

    imagem = fonte.render(
        texto,
        True,
        cor
    )

    screen.blit(
        imagem,
        (x, y)
    )


# =========================================================
# TEXTO CENTRALIZADO
# =========================================================

def texto_centralizado(
    texto,
    fonte,
    cor,
    y
):

    imagem = fonte.render(
        texto,
        True,
        cor
    )

    x = (
        WIDTH -
        imagem.get_width()
    ) // 2

    screen.blit(
        imagem,
        (x, y)
    )


# =========================================================
# BOTÃO
# =========================================================

def desenhar_botao(
    texto,
    x,
    y,
    largura,
    altura
):

    mouse = pygame.mouse.get_pos()

    retangulo = pygame.Rect(
        x,
        y,
        largura,
        altura
    )

    if retangulo.collidepoint(mouse):

        cor = AZUL_HOVER

    else:

        cor = AZUL


    pygame.draw.rect(
        screen,
        cor,
        retangulo,
        border_radius=15
    )


    imagem = fonte_media.render(
        texto,
        True,
        BRANCO
    )


    texto_x = (
        x +
        (largura - imagem.get_width()) // 2
    )

    texto_y = (
        y +
        (altura - imagem.get_height()) // 2
    )


    screen.blit(
        imagem,
        (texto_x, texto_y)
    )


    return retangulo


# =========================================================
# VOLTAR PARA O MENU
# =========================================================

def voltar_inicio():

    global tela
    global resultado
    global resposta_jogador

    tela = "menu"

    resultado = ""

    resposta_jogador = ""


# =========================================================
# NOVA RODADA
# =========================================================

def nova_rodada():

    global palavra_atual
    global resposta_correta
    global resposta_jogador
    global resultado
    global rodada


    rodada += 1


    palavra_atual = random.choice(
        dificuldades[
            dificuldade_atual
        ]["palavras"]
    )


    resposta_jogador = ""

    resultado = ""


    try:

        traducao = translator.translate_text(

            palavra_atual,

            source_lang="PT",

            target_lang="EN-US"

        )


        resposta_correta = (
            traducao.text
            .lower()
            .strip()
        )


    except deepl.DeepLException as e:

        print(
            "❌ Erro na DeepL:",
            e
        )

        resposta_correta = ""


# =========================================================
# LIMPAR RESPOSTA
# =========================================================

def limpar_resposta(texto):

    texto = texto.lower()

    texto = texto.strip()

    texto = texto.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    return texto


# =========================================================
# GRAVAR E RECONHECER
# =========================================================

def gravar_e_reconhecer():

    global resposta_jogador
    global resultado
    global pontos
    global vidas
    global experiencia
    global tela


    tempo = dificuldades[
        dificuldade_atual
    ]["tempo"]


    arquivo = "gravações/resposta.wav"


    print()
    print("🎙️ Gravando...")


    recording = sd.rec(

        int(
            tempo *
            sample_rate
        ),

        samplerate=sample_rate,

        channels=1,

        dtype="int16"

    )


    sd.wait()


    wav.write(

        arquivo,

        sample_rate,

        recording

    )


    print("🔎 Reconhecendo...")


    recognizer = sr.Recognizer()


    try:

        with sr.AudioFile(
            arquivo
        ) as source:

            audio = recognizer.record(
                source
            )


        resposta_jogador = (

            recognizer
            .recognize_google(
                audio,
                language="en-US"
            )
            .lower()
            .strip()

        )


    except sr.UnknownValueError:

        resposta_jogador = ""


    except sr.RequestError as e:

        print(
            "❌ Erro no reconhecimento:",
            e
        )

        resposta_jogador = ""


    except Exception as e:

        print(
            "❌ Erro:",
            e
        )

        resposta_jogador = ""


    resposta = limpar_resposta(
        resposta_jogador
    )

    correta = limpar_resposta(
        resposta_correta
    )


    # =====================================================
    # NÃO ENTENDEU
    # =====================================================

    if resposta == "":

        resultado = (
            "NAO CONSEGUI ENTENDER!"
        )

        vidas -= 1


    # =====================================================
    # ACERTO
    # =====================================================

    elif resposta == correta:

        resultado = "CORRETO!"

        pontos += dificuldades[
            dificuldade_atual
        ]["pontos"]

        experiencia += dificuldades[
            dificuldade_atual
        ]["xp"]

        salvar_experiencia()


    # =====================================================
    # ERRO
    # =====================================================

    else:

        resultado = "ERRADO!"

        vidas -= 1


    # =====================================================
    # GAME OVER
    # =====================================================

    if vidas <= 0:

        tela = "game_over"


# =========================================================
# COMEÇAR JOGO
# =========================================================

def iniciar_jogo(nome):

    global dificuldade_atual
    global pontos
    global vidas
    global rodada


    dificuldade_atual = nome

    pontos = 0

    rodada = 0

    vidas = dificuldades[
        nome
    ]["vidas"]


    nova_rodada()


# =========================================================
# LOOP PRINCIPAL
# =========================================================

rodando = True


while rodando:

    # =====================================================
    # EVENTOS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            rodando = False


        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse = event.pos


            # =================================================
            # BOTÃO INÍCIO
            # =================================================

            if tela != "menu":

                botao_inicio = pygame.Rect(
                    20,
                    20,
                    120,
                    45
                )


                if botao_inicio.collidepoint(
                    mouse
                ):

                    voltar_inicio()

                    continue


            # =================================================
            # MENU
            # =================================================

            if tela == "menu":

                botao_jogar = pygame.Rect(
                    300,
                    260,
                    300,
                    80
                )


                botao_sair = pygame.Rect(
                    300,
                    360,
                    300,
                    80
                )


                if botao_jogar.collidepoint(
                    mouse
                ):

                    tela = "dificuldade"


                if botao_sair.collidepoint(
                    mouse
                ):

                    rodando = False


            # =================================================
            # DIFICULDADE
            # =================================================

            elif tela == "dificuldade":

                nomes = [

                    "Fácil",
                    "Médio",
                    "Difícil",
                    "Extremo",
                    "Impossível"

                ]


                for i in range(
                    len(nomes)
                ):

                    y = (
                        105 +
                        i * 85
                    )


                    botao = pygame.Rect(

                        250,
                        y,
                        400,
                        65

                    )


                    if botao.collidepoint(
                        mouse
                    ):

                        nome = nomes[i]


                        if dificuldade_desbloqueada(
                            nome
                        ):

                            iniciar_jogo(
                                nome
                            )

                            tela = "jogo"


            # =================================================
            # JOGO
            # =================================================

            elif tela == "jogo":

                botao_falar = pygame.Rect(

                    300,
                    390,
                    300,
                    80

                )


                if (

                    resultado == ""

                    and

                    botao_falar.collidepoint(
                        mouse
                    )

                ):

                    gravar_e_reconhecer()


                if resultado != "":

                    botao_proxima = pygame.Rect(

                        300,
                        470,
                        300,
                        60

                    )


                    if botao_proxima.collidepoint(
                        mouse
                    ):

                        nova_rodada()


            # =================================================
            # GAME OVER
            # =================================================

            elif tela == "game_over":

                botao_novamente = pygame.Rect(

                    250,
                    330,
                    400,
                    70

                )


                botao_menu = pygame.Rect(

                    250,
                    420,
                    400,
                    70

                )


                if botao_novamente.collidepoint(
                    mouse
                ):

                    iniciar_jogo(
                        dificuldade_atual
                    )

                    tela = "jogo"


                if botao_menu.collidepoint(
                    mouse
                ):

                    tela = "menu"


    # =====================================================
    # FUNDO
    # =====================================================

    screen.fill(
        FUNDO
    )


    # =====================================================
    # BOTÃO INÍCIO
    # =====================================================

    if tela != "menu":

        desenhar_botao(

            "INICIO",

            20,
            20,
            120,
            45

        )


    # =====================================================
    # MENU
    # =====================================================

    if tela == "menu":

        texto_centralizado(

            "ENGLISH SPEAK",

            fonte_titulo,

            BRANCO,

            90

        )


        texto_centralizado(

            "Aprenda inglês falando!",

            fonte_media,

            CINZA,

            170

        )


        desenhar_texto(

            "XP: " +
            str(experiencia),

            fonte_pequena,

            AMARELO,

            30,
            30

        )


        desenhar_botao(

            "JOGAR",

            300,
            260,
            300,
            80

        )


        desenhar_botao(

            "SAIR",

            300,
            360,
            300,
            80

        )


    # =====================================================
    # DIFICULDADE
    # =====================================================

    elif tela == "dificuldade":

        texto_centralizado(

            "ESCOLHA A DIFICULDADE",

            fonte_grande,

            BRANCO,

            25

        )


        desenhar_texto(

            "XP: " +
            str(experiencia),

            fonte_pequena,

            AMARELO,

            700,
            30

        )


        nomes = [

            "Fácil",
            "Médio",
            "Difícil",
            "Extremo",
            "Impossível"

        ]


        for i in range(
            len(nomes)
        ):

            nome = nomes[i]

            y = (
                105 +
                i * 85
            )


            if dificuldade_desbloqueada(
                nome
            ):

                texto_botao = nome

            else:

                texto_botao = (

                    "BLOQUEADO - " +
                    nome +
                    " (" +
                    str(requisitos[nome]) +
                    " XP)"

                )


            desenhar_botao(

                texto_botao,

                250,
                y,
                400,
                65

            )


    # =====================================================
    # JOGO
    # =====================================================

    elif tela == "jogo":

        # -------------------------------------------------
        # INFORMAÇÕES
        # -------------------------------------------------

        desenhar_texto(

            dificuldade_atual,

            fonte_pequena,

            BRANCO,

            165,
            25

        )


        desenhar_texto(

            "Rodada " +
            str(rodada),

            fonte_pequena,

            CINZA,

            165,
            60

        )


        desenhar_texto(

            "Pontos: " +
            str(pontos),

            fonte_pequena,

            AMARELO,

            700,
            25

        )


        desenhar_texto(

            "XP: " +
            str(experiencia),

            fonte_pequena,

            AMARELO,

            700,
            60

        )


        # -------------------------------------------------
        # VIDAS
        # -------------------------------------------------

        coracoes = "❤️ " * vidas


        texto_centralizado(

            coracoes,

            fonte_media,

            VERMELHO,

            100

        )


        # -------------------------------------------------
        # PALAVRA
        # -------------------------------------------------

        texto_centralizado(

            "TRADUZA:",

            fonte_pequena,

            CINZA,

            175

        )


        texto_centralizado(

            palavra_atual.upper(),

            fonte_titulo,

            BRANCO,

            215

        )


        # -------------------------------------------------
        # ESPERANDO FALA
        # -------------------------------------------------

        if resultado == "":

            texto_centralizado(

                "Fale a tradução em inglês!",

                fonte_media,

                CINZA,

                315

            )


            desenhar_botao(

                "FALAR",

                300,
                390,
                300,
                80

            )


        # -------------------------------------------------
        # RESULTADO
        # -------------------------------------------------

        else:

            if resultado == "CORRETO!":

                cor_resultado = VERDE

            else:

                cor_resultado = VERMELHO


            texto_centralizado(

                resultado,

                fonte_grande,

                cor_resultado,

                300

            )


            texto_centralizado(

                "Você disse: " +
                resposta_jogador,

                fonte_pequena,

                CINZA,

                350

            )


            texto_centralizado(

                "Resposta: " +
                resposta_correta,

                fonte_pequena,

                VERDE,

                385

            )


            desenhar_botao(

                "PRÓXIMA",

                300,
                470,
                300,
                60

            )


    # =====================================================
    # GAME OVER
    # =====================================================

    elif tela == "game_over":

        texto_centralizado(

            "GAME OVER",

            fonte_titulo,

            VERMELHO,

            100

        )


        texto_centralizado(

            "Você ficou sem vidas!",

            fonte_media,

            BRANCO,

            190

        )


        texto_centralizado(

            "Pontos: " +
            str(pontos),

            fonte_media,

            AMARELO,

            240

        )


        texto_centralizado(

            "XP: " +
            str(experiencia),

            fonte_media,

            AMARELO,

            285

        )


        desenhar_botao(

            "JOGAR NOVAMENTE",

            250,
            360,
            400,
            70

        )


        desenhar_botao(

            "MENU",

            250,
            450,
            400,
            70

        )


    # =====================================================
    # ATUALIZAR
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# ENCERRAR
# =========================================================

pygame.quit()