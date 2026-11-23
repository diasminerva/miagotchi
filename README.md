# 👾 MiaGotchi — Monitor Biométrico (BPM) & Tamagotchi Físico com IA

![Status](https://img.shields.io/badge/status-functional%20prototype-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Hardware](https://img.shields.io/badge/Hardware-ESP32--S3%20Touch%20LCD-orange)
![Focus](https://img.shields.io/badge/Core-BPM%20Telemetry%20%26%20Reactive%20Messages-red)

![Protótipo físico do MiaGotchi](assets/miagotchi_hardware.jpg)

O **MiaGotchi** é um dispositivo físico de mesa estilo Tamagotchi projetado para acompanhar sua **frequência cardíaca (BPM) em tempo real**, reagir ao seu ritmo biológico através de **expressões faciais ilustradas** e enviar **mensagens dinâmicas de feedback** diretamente na tela, além de integrar alertas de **WhatsApp** e **conversação por voz com Inteligência Artificial**.

Construído sobre uma placa **ESP32-S3 com tela sensível ao toque, microfone e alto-falante**, o projeto conecta telemetria biométrica, arquitetura orientada a eventos em Python e interface embarcada.

---

## 💓 Núcleo de BPM e Mensagens Reativas

| Estado | Faixa de BPM | Expressão do Avatar | Comportamento & Mensagens Enviadas |
| :--- | :--- | :--- | :--- |
| **Calmo** | `< 90 BPM` | Rosto tranquilo | Envia mensagens curtas de incentivo e foco estável (ex.: *"Mantém assim, gata."*). |
| **Animado** | `90 – 115 BPM` | Rosto alerta / atento | Detecta elevação moderada de ritmo e envia avisos leves de acompanhamento. |
| **Alto** | `> 115 BPM` | Rosto preocupado / pico | Dispara alerta visual prioritário na tela com mensagens de pausa e respiração. |

- **Alertas de WhatsApp:** notificações visuais discretas na tela sem interromper o fluxo de trabalho.
- **Histórico Biométrico:** registro contínuo de horário, BPM, estado ativo e mensagens enviadas.
- **Conversação por Voz com IA:** captura de fala pelo microfone da placa e resposta em voz alta no alto-falante integrado.

---

## 🖥️ Hardware Utilizado

- **Placa Principal:** ESP32-S3 Dual-Core 240 MHz com Display Touch LCD 2.8" (`240x320`)
- **Áudio Bidirecional:** Microfone MEMS integrado + codec de áudio com mini alto-falante
- **Controles:** Tela touch + botões táteis frontais em case compacto impresso em 3D

---

## 👩‍💻 Autora

Desenvolvido por **[Mia (diasminerva)](https://github.com/diasminerva)** — Desenvolvedora Fullstack.
