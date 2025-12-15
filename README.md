# 🃏 Bullshit Card Game with IngeScape
**A distributed implementation of the Bullshit card game using IngeScape for multi-agent communication and real-time visualization.**

## 📋 Table of Contents
- [🎯 Features](#-features)
- [🤖 Agent Specifications](#agent-specifications)
- [📸 Screenshots](#-screenshots)
- [🚀 Quick Start](#-quick-start)
- [🎮 How to Play](#-how-to-play)
---

## 🎯 Features

### 🎲 **Core Game Features**
- Complete Bullshit card game logic
- machine opponent with bluff detection
- Tkinter-based graphical interface
- Real-time game state synchronization

### 🔗 **IngeScape Integration**
- Multi-agent distributed architecture
- Whiteboard visualization
- Real-time event broadcasting
- Service-oriented communication

### 🛠️ **Developer Features**
- Complete validation test suite
- Automated deployment scripts
- Comprehensive documentation
- Cross-platform compatibility

---
## **Agent Specifications**

### **🎮 GAME_ENGINE AGENT**
**Role**: Game controller & UI - Runs the actual game logic and Tkinter interface  
**Does**: Manages deck, player/AI turns, enforces rules, provides playable interface  
**Whiteboard relation**: Sends game state/events → Display Agent → Whiteboard visualization

### **🖥️ Graph_AGENT**  
**Role**: Visualization bridge - Shows game on Whiteboard  
**Does**: Listens to Game Engine, draws cards/stats/text on Whiteboard, highlights events  
**Whiteboard relation**: Direct control → sends "addText", "addShape", "clear" commands to Whiteboard



## 📸 Screenshots

<img width="1917" height="853" alt="image" src="https://github.com/user-attachments/assets/edb36a22-a1e4-4274-a2d3-c61d7dd39667" />

## 🚀 Quick Start

(make sure you are in the right path everytime )
# 1. Requirement

     -pip install ingescape
     -python -- version 
     
# 2. Launch the game
 open a terminal 1:

      -cd ~\IngeScape\sandbox\Game_Engine
      -python main.py game_engine {"network"} {port}
  
 open a terminal 2:
 
      -cd ~\IngeScape\sandbox\graphe
      -python main.py graphe {"network"} {port}
      
- open whitboard.exe and connect it to the same network device and port as other agents 
# 3. Open IngeScape to see the Whiteboard display
- clic on start on the Game_engine agent 
  
## 🎮 How to Play
- Each player starts with 5 cards
- Announce a card value (e.g., "Ace")
- Play a card (truthfully or bluff)
- Opponent can call "BULLSHIT!" if they suspect a bluff
- If bluff is caught, the liar takes all cards in the pile
- First to empty their hand wins!

