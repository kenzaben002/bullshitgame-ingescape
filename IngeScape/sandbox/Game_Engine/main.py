import sys
import tkinter as tk
import random
import ingescape as igs
import json
import time
import ctypes
from threading import Thread


VALEURS = ["A", "2", "3", "4", "5", "6", "7",
           "8", "9", "10", "J", "Q", "K"]
COULEURS = ["♠", "♥", "♦", "♣"]

class Carte:
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def __str__(self):
        return f"{self.valeur}{self.couleur}"

class Joueur:
    def __init__(self, nom, main):
        self.nom = nom
        self.main = main

    def nb_cartes(self):
        return len(self.main)

    def recevoir(self, cartes):
        self.main.extend(cartes)

class JoueurIA(Joueur):
    def jouer(self, valeur_annoncee):
        cartes_possibles = [c for c in self.main if c.valeur == valeur_annoncee]
        if cartes_possibles:
            carte = random.choice(cartes_possibles)
            self.main.remove(carte)
            annonce = valeur_annoncee
            verite = True
        else:
            carte = random.choice(self.main)
            self.main.remove(carte)
            annonce = valeur_annoncee
            verite = False
        return carte, annonce, verite

    def decide_bullshit(self, valeur, tas):
        nb_valeur = sum(1 for c in self.main if c.valeur == valeur)
        if nb_valeur == 4:
            return True
        proba = min(0.1 + len(tas) * 0.15, 0.7)
        return random.random() < proba

    def choisir_valeur(self):
        return random.choice(VALEURS)

class JeuBullshit:
    def __init__(self):
        paquet = [Carte(v, c) for v in VALEURS for c in COULEURS]
        random.shuffle(paquet)
        self.joueur = Joueur("Joueur", paquet[:5])
        self.ia = JoueurIA("IA", paquet[5:10])
        self.tas = []
        self.valeur_annoncee = random.choice(VALEURS)
        self.derniere_verite = True
        self.dernier = None

    def jouer_joueur(self, carte):
        self.joueur.main.remove(carte)
        self.tas.append(carte)
        self.derniere_verite = (carte.valeur == self.valeur_annoncee)
        self.dernier = self.joueur

    def jouer_ia(self):
        carte, annonce, verite = self.ia.jouer(self.valeur_annoncee)
        self.tas.append(carte)
        self.derniere_verite = verite
        self.dernier = self.ia
        return annonce

    def bullshit(self, accusateur):
        if self.derniere_verite:
            accusateur.recevoir(self.tas)
            perdant = accusateur.nom
            gagnant = self.dernier.nom
        else:
            self.dernier.recevoir(self.tas)
            perdant = self.dernier.nom
            gagnant = accusateur.nom
        self.tas.clear()
        return perdant, gagnant

    def victoire(self):
        if self.joueur.nb_cartes() == 0:
            return "Joueur"
        if self.ia.nb_cartes() == 0:
            return "IA"
        return None


class BullshitGUI:
    def __init__(self, root, ingescape_callback=None):
        self.root = root
        self.root.title("Bullshit – Valeur annoncée fixe")
        self.root.geometry("950x550")
        self.root.configure(bg="#2B2B2B")

        self.jeu = JeuBullshit()
        self.selection = None
        self.en_attente_valeur = False
        self.ingescape_callback = ingescape_callback  

        # UI elements
        self.info = tk.Label(root, font=("Arial", 14), fg="white", bg="#2B2B2B")
        self.info.pack(pady=5)

        self.valeur = tk.Label(root, font=("Arial Bold", 22), fg="white", bg="#2B2B2B")
        self.valeur.pack(pady=5)

        self.canvas = tk.Canvas(root, width=900, height=180, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Frame pour choisir valeur
        frame_annonce = tk.Frame(root, bg="#2B2B2B")
        frame_annonce.pack(pady=5)
        self.frame_annonce = frame_annonce
        tk.Label(frame_annonce, text="Choisir nouvelle valeur :",
                 font=("Arial", 12), fg="white", bg="#2B2B2B").pack(side=tk.LEFT, padx=(0,5))

        self.valeur_annoncee_var = tk.StringVar(value=self.jeu.valeur_annoncee)
        self.option_annonce = tk.OptionMenu(frame_annonce, self.valeur_annoncee_var, *VALEURS)
        self.option_annonce.config(width=5, font=("Arial", 12))
        self.option_annonce.pack(side=tk.LEFT)

        self.btn_valider_valeur = tk.Button(frame_annonce, text="Valider",
                                            font=("Arial", 12, "bold"),
                                            command=self.valider_nouvelle_valeur)
        self.btn_valider_valeur.pack(side=tk.LEFT, padx=10)

        # Boutons de jeu
        btn_frame = tk.Frame(root, bg="#2B2B2B")
        btn_frame.pack(pady=10)

        self.btn_jouer = tk.Button(btn_frame, text="Jouer carte", width=20,
                                   bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                   command=self.jouer)
        self.btn_jouer.pack(side=tk.LEFT, padx=10)

        self.btn_bullshit = tk.Button(btn_frame, text="BULLSHIT !", width=20,
                                      bg="#F44336", fg="white", font=("Arial", 12, "bold"),
                                      command=self.bullshit)
        self.btn_bullshit.pack(side=tk.LEFT, padx=10)

        self.stats = tk.Label(root, font=("Arial", 12), fg="white", bg="#2B2B2B")
        self.stats.pack(pady=5)

        self.frame_annonce.pack_forget()

        # Premier affichage
        self.refresh()
        self.notify_ingescape("START")  

    def afficher_main(self):
        self.canvas.delete("all")
        self.cartes_canvas = []
        x = 30
        y = 30
        for carte in self.jeu.joueur.main:
            rect = self.canvas.create_rectangle(x, y, x+60, y+100, fill="white",
                                                outline="#555", width=2, tags="carte")
            text = self.canvas.create_text(x+30, y+50, text=str(carte),
                                           font=("Arial Bold", 18), fill="#222")
            self.cartes_canvas.append((rect, carte))
            self.canvas.tag_bind(rect, "<Button-1>",
                                 lambda e, c=carte, r=rect: self.selectionner(c, r))
            self.canvas.tag_bind(text, "<Button-1>",
                                 lambda e, c=carte, r=rect: self.selectionner(c, r))
            x += 80

    def selectionner(self, carte, rect):
        if self.en_attente_valeur:
            return
        for r, _ in self.cartes_canvas:
            self.canvas.itemconfig(r, outline="#555", width=2)
        self.canvas.itemconfig(rect, outline="#FFD700", width=4)
        self.selection = carte
        self.notify_ingescape("CARD_SELECTED", str(carte))

    def jouer(self):
        if self.en_attente_valeur:
            self.info.config(text="Choisis la nouvelle valeur annoncée avant de jouer")
            return
        if not self.selection:
            self.info.config(text="Sélectionne une carte !")
            return

        self.jeu.jouer_joueur(self.selection)
        self.selection = None
        self.notify_ingescape("PLAYER_PLAYED")

        if self.jeu.ia.decide_bullshit(self.jeu.valeur_annoncee, self.jeu.tas):
            perdant, gagnant = self.jeu.bullshit(self.jeu.ia)
            self.info.config(text=f"L'IA dit BULLSHIT → {perdant} prend le tas")
            self.notify_ingescape("IA_BULLSHIT", f"{perdant} prend le tas")
            self.demander_nouvelle_valeur(gagnant)
        else:
            annonce_ia = self.jeu.jouer_ia()
            self.info.config(text=f"L'IA joue et annonce {annonce_ia}")
            self.notify_ingescape("IA_PLAYED", annonce_ia)

        self.refresh()
        self.verifier_victoire()

    def bullshit(self):
        if self.en_attente_valeur:
            self.info.config(text="Choisis la nouvelle valeur annoncée avant de jouer")
            return
        perdant, gagnant = self.jeu.bullshit(self.jeu.joueur)
        self.info.config(text=f"BULLSHIT → {perdant} prend le tas")
        self.notify_ingescape("PLAYER_BULLSHIT", f"{perdant} prend le tas")
        self.demander_nouvelle_valeur(gagnant)
        self.refresh()
        self.verifier_victoire()

    def demander_nouvelle_valeur(self, joueur_nom):
        self.en_attente_valeur = True
        self.btn_jouer.config(state="disabled")
        self.btn_bullshit.config(state="disabled")
        self.selection = None
        self.frame_annonce.pack()
        self.info.config(text=f"{joueur_nom}, choisis la nouvelle valeur annoncée")
        self.notify_ingescape("CHOOSE_NEW_VALUE", joueur_nom)

        if joueur_nom == "IA":
            self.root.after(1500, self.ia_choisit_valeur)

    def ia_choisit_valeur(self):
        nouvelle_valeur = self.jeu.ia.choisir_valeur()
        self.valeur_annoncee_var.set(nouvelle_valeur)
        self.valider_nouvelle_valeur()

    def valider_nouvelle_valeur(self):
        nouvelle_valeur = self.valeur_annoncee_var.get()
        self.jeu.valeur_annoncee = nouvelle_valeur
        self.info.config(text=f"Nouvelle valeur annoncée : {nouvelle_valeur}")
        self.frame_annonce.pack_forget()
        self.en_attente_valeur = False
        self.btn_jouer.config(state="normal")
        self.btn_bullshit.config(state="normal")
        self.notify_ingescape("NEW_VALUE_SET", nouvelle_valeur)
        self.refresh()

    def refresh(self):
        self.valeur.config(text=f"Valeur annoncée (tour): {self.jeu.valeur_annoncee}")
        last_announce = self.jeu.valeur_annoncee
        self.stats.config(
            text=f"Joueur : {self.jeu.joueur.nb_cartes()} cartes | "
                 f"IA : {self.jeu.ia.nb_cartes()} cartes | "
                 f"Tas : {len(self.jeu.tas)} cartes | "
                 f"Dernière annonce : {last_announce}"
        )
        self.afficher_main()
        self.notify_ingescape("GAME_STATE", self.get_game_state())

    def verifier_victoire(self):
        gagnant = self.jeu.victoire()
        if gagnant:
            self.info.config(text=f"🎉 {gagnant} a gagné la partie ! 🎉")
            self.btn_jouer.config(state="disabled")
            self.btn_bullshit.config(state="disabled")
            self.canvas.unbind("<Button-1>")
            self.frame_annonce.pack_forget()
            self.notify_ingescape("GAME_WON", gagnant)

    def get_game_state(self):
        """Retourne l'état du jeu au format JSON"""
        return json.dumps({
            "player_cards": [str(c) for c in self.jeu.joueur.main],
            "player_count": self.jeu.joueur.nb_cartes(),
            "ia_count": self.jeu.ia.nb_cartes(),
            "pile_count": len(self.jeu.tas),
            "current_value": self.jeu.valeur_annoncee,
            # NOTE: on garde ton code exact ici (pile_cards limité),
            # le Whiteboard lui affichera TOUT jeu.tas.
            "pile_cards": [str(c) for c in self.jeu.tas[-3:]] if self.jeu.tas else []
        })

    def notify_ingescape(self, event_type, data=""):
        """Notifie Ingescape d'un événement"""
        if self.ingescape_callback:
            self.ingescape_callback(event_type, data)


class BullshitIngescapeAgent:
    def __init__(self, agent_name="BullshitGame", network_device="lo0", port=5670):
        self.agent_name = agent_name
        self.network_device = network_device
        self.port = port
        self.gui_root = None
        self.gui = None

        # Configuration Ingescape
        igs.agent_set_name(self.agent_name)
        igs.definition_set_class("Game_Engine")
        igs.log_set_console(True)

        # Définir les Inputs/Outputs/Services
        self._setup_ingescape()

        print(f" Agent '{self.agent_name}' initialisé")

    def _setup_ingescape(self):
        """Configure Ingescape"""
        # INPUTS
        igs.input_create("start", igs.IMPULSION_T, None)
        igs.observe_input("start", self._on_start, None)

        igs.input_create("reset", igs.IMPULSION_T, None)
        igs.observe_input("reset", self._on_reset, None)

        igs.input_create("whiteboard_cmd", igs.STRING_T, None)
        igs.observe_input("whiteboard_cmd", self._on_whiteboard_cmd, None)

        # OUTPUTS
        igs.output_create("game_state", igs.STRING_T, None)
        igs.output_create("game_event", igs.STRING_T, None)
        igs.output_create("player_hand", igs.STRING_T, None)
        igs.output_create("pile_info", igs.STRING_T, None)

        # SERVICES
        igs.service_init("get_state", self._service_get_state, None)
        igs.service_reply_add("get_state", "state_reply")
        igs.service_reply_arg_add("get_state", "state_reply", "state", igs.STRING_T)

    def _on_start(self, iop_type, name, value_type, value, my_data):
        """Démarre le jeu"""
        print("🎮 Démarrage du jeu...")
        self._launch_gui()

    def _on_reset(self, iop_type, name, value_type, value, my_data):
        """Réinitialise le jeu"""
        print("🔄 Réinitialisation...")
        if self.gui_root:
            self.gui_root.destroy()
            self.gui_root = None
        self._launch_gui()

    def _on_whiteboard_cmd(self, iop_type, name, value_type, value, my_data):
        """Reçoit une commande pour le Whiteboard"""
        if value:
            print(f"📋 Commande Whiteboard: {value}")

    def _service_get_state(self, sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
        """Retourne l'état du jeu"""
        if self.gui and self.gui.jeu:
            return self.gui.get_game_state()
        return json.dumps({"status": "Game not running"})

    def _launch_gui(self):
        """Lance l'interface graphique"""
        if self.gui_root is not None:
            return

        def run_gui():
            self.gui_root = tk.Tk()
            self.gui = BullshitGUI(self.gui_root, self._ingescape_callback)

            # Première synchro Whiteboard
            self.render_whiteboard()

            self.gui_root.mainloop()
            self.gui_root = None
            self.gui = None

        gui_thread = Thread(target=run_gui, daemon=True)
        gui_thread.start()
        print("🪟 Interface jeu lancée")

    def _ingescape_callback(self, event_type, data):
        try:
            if event_type == "GAME_STATE":
                igs.output_set_string("game_state", data)

                state = json.loads(data)
                igs.output_set_string(
                    "player_hand",
                    f"{state['player_count']} cartes: {', '.join(state['player_cards'])}"
                )
                igs.output_set_string(
                    "pile_info",
                    f"Tas: {state['pile_count']} cartes"
                )

            elif event_type == "GAME_WON":
                igs.output_set_string("game_event", f"🎉 VICTOIRE: {data}")

            elif event_type in ["PLAYER_PLAYED", "IA_PLAYED", "PLAYER_BULLSHIT", "IA_BULLSHIT"]:
                igs.output_set_string("game_event", f"{event_type}: {data}")

            elif event_type == "NEW_VALUE_SET":
                igs.output_set_string("game_event", f"🔄 Nouvelle valeur: {data}")

        except Exception as e:
            print(f"Erreur callback: {e}")

  
    def render_whiteboard(self):
        if not self.gui:
            return

        jeu = self.gui.jeu

        try:
            # Effacer le whiteboard
            igs.service_call("Whiteboard", "clear", None, "")

            # Titre
            igs.service_call(
                "Whiteboard", "addText",
                ("🃏 Cartes jouées ce tour", 40.0, 40.0, "#000000"),
                ""
            )

            # Valeur annoncée
            igs.service_call(
                "Whiteboard", "addText",
                (f" Valeur : {jeu.valeur_annoncee}", 40.0, 80.0, "#e67e22"),
                ""
            )

            # Affichage des cartes du tas (TOUTES)
            x = 40.0
            y = 140.0

            for carte in jeu.tas:
                igs.service_call(
                    "Whiteboard", "addShape",
                    ("rect", x, y, 60.0, 90.0, "#ffffff", "#000000", 2),
                    ""
                )
                igs.service_call(
                    "Whiteboard", "addText",
                    (str(carte), x + 18.0, y + 55.0, "#000000"),
                    ""
                )
                x += 75.0

        except Exception as e:
            print("Whiteboard error:", e)

    def run(self):
        """Démarre l'agent"""
        try:
            igs.start_with_device(self.network_device, self.port)
            print(f" Agent '{self.agent_name}' connecté sur {self.network_device}:{self.port}")
            print("📡 En attente... (Ctrl+C pour arrêter)")

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nArrêt de l'agent")
        finally:
            igs.stop()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python bullshit_ingescape.py agent_name network_device port")
        print("Exemple: python bullshit_ingescape.py BullshitGame \"Wi-Fi\" 5670")

        try:
            devices = igs.net_devices_list()
            print("📡 Interfaces disponibles:")
            for device in devices:
                print(f"  - {device}")
        except:
            print(" Impossible de lister les interfaces")

        sys.exit(1)

    agent_name = sys.argv[1]
    network_device = sys.argv[2]
    port = int(sys.argv[3])

    agent = BullshitIngescapeAgent(agent_name, network_device, port)
    agent.run()
