# TESTE-CU

## Projeto JARVIS (ativação por voz)

Este repositório agora inclui um exemplo funcional de assistente em Python com:

- escuta contínua no microfone,
- ativação por palavra-chave (`jarvis`),
- interpretação de comando por IA (OpenAI),
- resposta falada por TTS local (`pyttsx3`) ou por voz customizada (ElevenLabs).

> Arquivos principais: `jarvis/jarvis_assistant.py`, `jarvis/requirements.txt`, `jarvis/.env.example`.

## Como rodar

1. Entre na pasta do projeto e crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r jarvis/requirements.txt
```

3. Configure as chaves:

```bash
cp jarvis/.env.example .env
# edite .env e preencha OPENAI_API_KEY
# opcional: ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID
```

4. Rode o assistente:

```bash
python jarvis/jarvis_assistant.py
```

5. Diga "jarvis" para ativar e depois faça seu comando.

## Observações importantes

- Para reproduzir uma voz "igual ao filme", use somente vozes para as quais você tem autorização legal.
- Clonagem sem permissão pode violar direitos autorais, direitos de imagem/voz e políticas de plataformas.
- Se não configurar ElevenLabs, o sistema usa voz local automática (fallback).
