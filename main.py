import tkinter as tk
from datetime import datetime
import random
import os
import subprocess
import re

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


WATCH_MAC = "D8:C2:FA:3B:3A:37"

MENSAGENS = {
    "calmo": "Mantém assim, gata.",
    "alerta": "Opa, deu animada?",
    "alto": "Respira, tá alto."
}


def ler_status_watch(mac=WATCH_MAC):
    try:
        out = subprocess.check_output(
            ["bluetoothctl", "info", mac],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=3
        )
    except Exception:
        return False, None

    conectado = "Connected: yes" in out
    bateria = None

    m_hex = re.search(r"Battery Percentage:\s*0x([0-9a-fA-F]+)", out)
    if m_hex:
        bateria = int(m_hex.group(1), 16)
    else:
        m_dec = re.search(r"Battery Percentage:\s*\d+\s*\((\d+)\)", out)
        if m_dec:
            bateria = int(m_dec.group(1))

    return conectado, bateria


class MiaGotchi:
    def __init__(self, root):
        self.root = root
        self.root.title("MiaGotchi")
        self.root.geometry("380x550")
        self.root.configure(bg="#181825")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(self.base_dir, "historico_miagotchi.log")
        self.bpm = 76
        self.modo_auto = True
        self.alerta_wpp = False
        self.no_topo = False
        self.ultimo_humor = None

        top_frame = tk.Frame(root, bg="#181825")
        top_frame.pack(fill="x", padx=16, pady=(12, 4))

        self.lbl_hora = tk.Label(
            top_frame, text="00:00:00", font=("Consolas", 12, "bold"),
            fg="#89b4fa", bg="#181825"
        )
        self.lbl_hora.pack(side="left")

        self.btn_wpp = tk.Button(
            top_frame, text="Simular WPP", command=self.toggle_wpp,
            font=("Arial", 9, "bold"), bg="#a6e3a1", fg="#11111b",
            relief="flat", padx=8, pady=2
        )
        self.btn_wpp.pack(side="right")

        self.lbl_watch = tk.Label(
            root, text="WATCH: checando...", font=("Consolas", 9, "bold"),
            fg="#bac2de", bg="#24273a", padx=8, pady=4
        )
        self.lbl_watch.pack(fill="x", padx=16, pady=(2, 4))

        self.lbl_bpm = tk.Label(
            root, text=f"{self.bpm} BPM", font=("Consolas", 26, "bold"),
            fg="#a6e3a1", bg="#181825"
        )
        self.lbl_bpm.pack(pady=(2, 2))

        self.canvas = tk.Canvas(
            root, width=210, height=210, bg="#f5f5f5",
            highlightthickness=2, highlightbackground="#45475a"
        )
        self.canvas.pack(pady=6)
        self.img_ref = None

        self.lbl_fala = tk.Label(
            root, text="", font=("Arial", 12, "bold"),
            fg="#cdd6f4", bg="#24273a", wraplength=340, justify="center",
            padx=10, pady=10
        )
        self.lbl_fala.pack(fill="x", padx=16, pady=6)

        btn_frame = tk.Frame(root, bg="#181825")
        btn_frame.pack(pady=6)

        tk.Button(
            btn_frame, text="Calmo (72)", command=lambda: self.set_bpm(72),
            bg="#313244", fg="#cdd6f4", relief="flat", padx=8, pady=4
        ).grid(row=0, column=0, padx=4)

        tk.Button(
            btn_frame, text="Animado (104)", command=lambda: self.set_bpm(104),
            bg="#313244", fg="#cdd6f4", relief="flat", padx=8, pady=4
        ).grid(row=0, column=1, padx=4)

        tk.Button(
            btn_frame, text="Alto (128)", command=lambda: self.set_bpm(128),
            bg="#313244", fg="#cdd6f4", relief="flat", padx=8, pady=4
        ).grid(row=0, column=2, padx=4)

        extra_frame = tk.Frame(root, bg="#181825")
        extra_frame.pack(pady=4)

        self.btn_auto = tk.Button(
            extra_frame, text="BPM Automático: ON", command=self.toggle_auto,
            bg="#89b4fa", fg="#11111b", font=("Arial", 9, "bold"),
            relief="flat", padx=10, pady=4
        )
        self.btn_auto.grid(row=0, column=0, padx=4)

        self.btn_topo = tk.Button(
            extra_frame, text="No Topo: OFF", command=self.toggle_topo,
            bg="#313244", fg="#cdd6f4", font=("Arial", 9, "bold"),
            relief="flat", padx=10, pady=4
        )
        self.btn_topo.grid(row=0, column=1, padx=4)

        self.atualizar_hora()
        self.atualizar_watch()
        self.atualizar_tudo()
        self.loop_bpm()

    def registrar_evento(self, evento):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{agora}] {self.bpm} BPM | {evento}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(linha)
        except Exception:
            pass

    def atualizar_hora(self):
        agora = datetime.now().strftime("%H:%M:%S")
        self.lbl_hora.config(text=f"🕒 {agora}")
        self.root.after(1000, self.atualizar_hora)

    def atualizar_watch(self):
        conectado, bateria = ler_status_watch()
        if conectado and bateria is not None:
            self.lbl_watch.config(text=f"WATCH conectado • Bateria: {bateria}%", fg="#a6e3a1")
        elif conectado:
            self.lbl_watch.config(text="WATCH conectado", fg="#a6e3a1")
        else:
            self.lbl_watch.config(text="WATCH desconectado", fg="#f38ba8")
        self.root.after(10000, self.atualizar_watch)

    def toggle_wpp(self):
        self.alerta_wpp = not self.alerta_wpp
        self.registrar_evento(f"WPP={'ON' if self.alerta_wpp else 'OFF'}")
        self.atualizar_tudo()

    def toggle_topo(self):
        self.no_topo = not self.no_topo
        self.root.attributes("-topmost", self.no_topo)
        if self.no_topo:
            self.btn_topo.config(text="No Topo: ON", bg="#cba6f7", fg="#11111b")
        else:
            self.btn_topo.config(text="No Topo: OFF", bg="#313244", fg="#cdd6f4")

    def set_bpm(self, valor):
        self.modo_auto = False
        self.btn_auto.config(text="BPM Automático: OFF", bg="#585b70", fg="#cdd6f4")
        self.bpm = valor
        self.atualizar_tudo()

    def toggle_auto(self):
        self.modo_auto = not self.modo_auto
        if self.modo_auto:
            self.btn_auto.config(text="BPM Automático: ON", bg="#89b4fa", fg="#11111b")
        else:
            self.btn_auto.config(text="BPM Automático: OFF", bg="#585b70", fg="#cdd6f4")

    def tentar_carregar_png(self, humor):
        if not HAS_PIL:
            return False
        caminho = os.path.join(self.base_dir, f"{humor}.png")
        if os.path.exists(caminho):
            img = Image.open(caminho).convert("RGBA")
            img.thumbnail((190, 190), Image.Resampling.LANCZOS)
            self.img_ref = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(105, 105, image=self.img_ref)
            return True
        return False

    def desenhar_personagem(self, humor):
        if self.tentar_carregar_png(humor):
            return

        self.canvas.delete("all")
        self.canvas.create_oval(50, 35, 160, 145, fill="#f5e0dc", outline="#cba6f7", width=3)

        if humor == "calmo":
            self.canvas.create_arc(72, 72, 96, 92, start=0, extent=180, style="arc", width=3, outline="#1e1e2e")
            self.canvas.create_arc(114, 72, 138, 92, start=0, extent=180, style="arc", width=3, outline="#1e1e2e")
            self.canvas.create_arc(86, 92, 124, 118, start=180, extent=180, style="arc", width=3, outline="#1e1e2e")
        elif humor == "alerta":
            self.canvas.create_oval(78, 74, 92, 92, fill="#1e1e2e")
            self.canvas.create_oval(118, 74, 132, 92, fill="#1e1e2e")
            self.canvas.create_oval(97, 98, 113, 114, outline="#1e1e2e", width=3)
        else:
            self.canvas.create_line(74, 72, 94, 82, width=3, fill="#1e1e2e")
            self.canvas.create_line(136, 72, 116, 82, width=3, fill="#1e1e2e")
            self.canvas.create_oval(79, 82, 91, 94, fill="#1e1e2e")
            self.canvas.create_oval(119, 82, 131, 94, fill="#1e1e2e")
            self.canvas.create_arc(88, 104, 122, 122, start=0, extent=180, style="arc", width=3, outline="#1e1e2e")

    def atualizar_tudo(self):
        self.lbl_bpm.config(text=f"{self.bpm} BPM")

        if self.bpm < 95:
            humor = "calmo"
            cor = "#a6e3a1"
        elif self.bpm <= 115:
            humor = "alerta"
            cor = "#f9e2af"
        else:
            humor = "alto"
            cor = "#f38ba8"

        if humor != self.ultimo_humor:
            self.ultimo_humor = humor
            self.registrar_evento(f"ESTADO={humor.upper()}")

        msg = MENSAGENS[humor]
        if self.alerta_wpp:
            msg = f"💬 WPP! {msg}"

        self.lbl_bpm.config(fg=cor)
        self.lbl_fala.config(text=msg, fg=cor)
        self.desenhar_personagem(humor)

    def loop_bpm(self):
        if self.modo_auto:
            self.bpm = max(55, min(145, self.bpm + random.choice([-3, -1, 0, 1, 3])))
            self.atualizar_tudo()

        delay = max(550, min(1500, int(60000 / max(45, self.bpm))))
        self.root.after(delay, self.loop_bpm)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiaGotchi(root)
    root.mainloop()
