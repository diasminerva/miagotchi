# MiaGotchi - Monitor Biometrico (BPM) e Tamagotchi Fisico com IA

![Prototipo fisico do MiaGotchi](assets/miagotchi_hardware.jpg)

Dispositivo fisico de mesa em **ESP32-S3** + **MAX30102** que mede batimentos cardiacos (BPM) em tempo real, altera expressoes faciais, envia mensagens reativas, exibe alertas de WhatsApp e conversa por voz com IA.

## Nucleo de BPM e Mensagens

- **Calmo (< 90 BPM):** rosto tranquilo e mensagens curtas de foco (ex.: *"Mantem assim, gata."*).
- **Animado (90 - 115 BPM):** rosto alerta com avisos leves de acompanhamento.
- **Alto (> 115 BPM):** rosto preocupado com alerta de pausa e respiracao.
- **Modo Hibrido:** leitura via sensor optico MAX30102 ou simulacao (`Calmo 72`, `Animado 104`, `Alto 128`).

## Hardware

- ESP32-S3 com tela touch, microfone e alto-falante
- Sensor optico de pulso **MAX30102** (I2C)
- Case compacto e alimentacao USB-C / bateria

## Autora

Desenvolvido por **[Mia (diasminerva)](https://github.com/diasminerva)**.
