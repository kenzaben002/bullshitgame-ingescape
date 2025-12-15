#!/usr/bin/env python3
# whiteboard_display_agent_v2.py
# Agent Ingescape pour afficher visuellement le jeu Bullshit sur Whiteboard

import sys
import time
import json
import ingescape as igs


class WhiteboardDisplayAgent:

    def __init__(self, agent_name, network_device, port):
        self.agent_name = agent_name
        self.network_device = network_device
        self.port = port

        # État du jeu
        self.current_pile = []  # Toutes les cartes du tas
        self.player_count = 0
        self.ia_count = 0
        self.current_value = ""
        self.last_bullshit_event = ""
        
        # Positionnement
        self.base_x = 40.0
        self.base_y = 140.0
        self.card_width = 60.0
        self.card_height = 90.0
        self.card_spacing = 75.0
        
        # Maximum de cartes à afficher horizontalement avant retour à la ligne
        self.max_cards_per_row = 0
        self.row_height = 110.0
        
        # Couleurs
        self.colors = {
            "title": "#000000",
            "value": "#e67e22",
            "card_bg": "#ffffff",
            "card_border": "#000000",
            "bullshit": "#FF0000"
        }

        # Ingescape
        igs.agent_set_name(agent_name)
        igs.definition_set_class("Display")
        igs.log_set_console(True)

        self._setup_ios()
        print(f"✅ Agent '{agent_name}' initialisé")



    def _setup_ios(self):
        # INPUTS (reçoit des données du jeu)
        igs.input_create("game_state", igs.STRING_T, None)
        igs.observe_input("game_state", self._on_game_state, None)

        igs.input_create("game_event", igs.STRING_T, None)
        igs.observe_input("game_event", self._on_game_event, None)
        
        igs.input_create("pile_info", igs.STRING_T, None)
        igs.observe_input("pile_info", self._on_pile_info, None)

    def _on_game_state(self, iop, name, vtype, value, _):
        """Reçoit l'état complet du jeu"""
        if not value:
            return

        try:
            state = json.loads(value)
            print(f"📊 Game state received: {state.get('pile_count', 0)} cards")

            # Mettre à jour les informations
            self.player_count = state.get("player_count", 0)
            self.ia_count = state.get("ia_count", 0)
            self.current_value = state.get("current_value", "")
            self._render_whiteboard()

        except Exception as e:
            print(" Erreur game_state:", e)

    def _on_game_event(self, iop, name, vtype, value, _):
        """Reçoit les événements du jeu"""
        if not value:
            return

        print(f"🎮 Événement: {value}")

        
        if "BULLSHIT" in value.upper():
            self.last_bullshit_event = value
            self._display_bullshit_event(value)

    def _on_pile_info(self, iop, name, vtype, value, _):
        """Reçoit les informations sur le tas de cartes"""
        if value:
            print(f"🗂️ Info tas: {value}")

    def _clear_whiteboard(self):
        """Efface le Whiteboard"""
        try:
           
            igs.service_call("Whiteboard", "clear", None, "")
            time.sleep(0.05)  
        except Exception as e:
            print(f" Erreur clear: {e}")

    def _add_text(self, text, x, y, color):
        """Ajoute du texte sur le Whiteboard"""
        try:
            igs.service_call(
                "Whiteboard",
                "addText",
                (str(text), float(x), float(y), str(color)),
                ""
            )
        except Exception as e:
            print(f"⚠️ Erreur addText: {e}")

    def _add_card(self, card_str, x, y):
        """Ajoute une carte (rectangle + texte) sur le Whiteboard"""
        try:
            igs.service_call(
                "Whiteboard",
                "addShape",
                (
                    "rect",
                    float(x),
                    float(y),
                    float(x + self.card_width),
                    float(y + self.card_height),
                    self.colors["card_bg"],  
                    self.colors["card_border"],  
                    2.0  
                ),
                ""
            )
            
            # 2. Texte de la carte au centre
            text_x = x + (self.card_width / 2) - 15.0
            text_y = y + (self.card_height / 2) - 10.0
            
            # Déterminer la couleur du texte en fonction de la couleur de la carte
            text_color = "#000000"  
            
            
        except Exception as e:
            print(f"Erreur add_card: {e}")

    def _render_whiteboard(self):
        """Affiche le jeu sur le Whiteboard - Version améliorée"""
        try:
            # Effacer l'écran
            self._clear_whiteboard()
            
            # Titre principal
            self._add_text("🃏 Cartes jouées ce tour", 40.0, 40.0, self.colors["title"])
            
            # Valeur annoncée
            self._add_text(f"📢 Valeur à annoncer: {self.current_value}", 
                          40.0, 80.0, self.colors["value"])
            
            # Informations joueurs
            self._add_text(f"👤 Joueur: {self.player_count} cartes", 
                          450.0, 40.0, "#3498db")
            self._add_text(f"🤖 IA: {self.ia_count} cartes", 
                          450.0, 80.0, "#e74c3c")
            
            # Si pas de cartes dans le tas, afficher un message
            if not self.current_pile:
                self._add_text("Aucune carte jouée ce tour...", 
                              40.0, 140.0, "#888888")
                return
            
        except Exception as e:
            print(f" Erreur render_whiteboard: {e}")

    def _display_bullshit_event(self, message):
        """Affiche un événement BULLSHIT sur le Whiteboard"""
        try:
            print(f"🚨 Affichage événement BULLSHIT: {message}")
            
            # Sauvegarder l'état actuel des cartes
            saved_pile = self.current_pile.copy()
            
            # Effacer et afficher le message BULLSHIT
            self._clear_whiteboard()
            
            # Message BULLSHIT en grand
            self._add_text("🚨 BULLSHIT ! 🚨", 350.0, 250.0, self.colors["bullshit"])
            
            # Extraire le message clé
            if "prend le tas" in message:
                parts = message.split("→")
                if len(parts) > 1:
                    detail = parts[1].strip()
                   
            time.sleep(3)
            
            # Restaurer l'affichage normal
            self.current_pile = saved_pile
            self._render_whiteboard()
            
        except Exception as e:
            print(f" Erreur display_bullshit_event: {e}")


    def update_pile(self, pile_cards):
        """Met à jour la liste des cartes du tas"""
        if pile_cards:
            self.current_pile = pile_cards
            self._render_whiteboard()


    def run(self):
        """Démarre l'agent d'affichage"""
        try:
            igs.start_with_device(self.network_device, self.port)
            print(f"📡 Agent '{self.agent_name}' connecté sur {self.network_device}:{self.port}")
            print("🃏 En attente des données du jeu Bullshit...")
            print("💡 Pour tester, envoyez des événements 'game_state' depuis l'agent de jeu")
            
            # Afficher un message initial
            self._clear_whiteboard()
            self._add_text("🃏 BULLSHIT DISPLAY", 300.0, 250.0, "#3498db")
            self._add_text("En attente du jeu...", 300.0, 290.0, "#e74c3c")
            
            # Boucle principale
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n Arrêt de l'agent d'affichage")
                
        except Exception as e:
            print(f" Erreur lors du démarrage: {e}")
        finally:
            try:
                igs.stop()
            except:
                pass

class TestGameAgent:
    """Agent simple pour tester l'affichage"""
    def __init__(self, name, device, port):
        self.name = name
        igs.agent_set_name(name)
        igs.definition_set_class("TestGame")
        
        # Créer un output pour envoyer des données
        igs.output_create("test_state", igs.STRING_T, None)
        
        igs.start_with_device(device, port)
        print(f" Agent de test '{name}' démarré")
    
    def send_test_state(self):
        """Envoie un état de jeu test"""
        test_state = {
            "player_count": 5,
            "ia_count": 5,
            "current_value": "A",
            "pile_cards": ["A♠", "K♥", "Q♦", "J♣", "10♠", "9♥"]
        }
        
        igs.output_set_string("test_state", json.dumps(test_state))
        print("📤 État test envoyé")



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python graphe.py NAME DEVICE PORT")
        
        # Valeurs par défaut
        agent_name = "BullshitDisplay"
        network_device = "Wi-Fi"
        port = 5670
    else:
        agent_name = sys.argv[1]
        network_device = sys.argv[2]
        port = int(sys.argv[3])
   
    agent = WhiteboardDisplayAgent(agent_name, network_device, port)
    agent.run()