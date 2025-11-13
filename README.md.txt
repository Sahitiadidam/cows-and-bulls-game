# 🐮 Cows & Bulls — Two Player Game  

### 🎮 About the Game  
Cows & Bulls is a classic code-breaking logic game where two players compete to guess each other's secret 4-digit number.  
After each guess, players get feedback:  
- 🐂 **Bulls** — Correct digit in the correct position.  
- 🐮 **Cows** — Correct digit but in the wrong position.  

The first player to get **4 Bulls** wins the game!  

---

### 💡 Features  
✅ Two-player turn-based gameplay  
✅ Hidden secret inputs (so no peeking 👀)  
✅ Automatic turn switching  
✅ Real-time feedback for each guess  
✅ “Wrong guess” message + Bulls & Cows position hints  
✅ Scoreboard showing performance of both players  
✅ Restart option to play again instantly  
✅ Built with **Python + Streamlit**  

---

### 🚀 How to Play  
1. Each player enters a **secret 4-digit number** (all digits must be unique).  
2. Players take turns guessing each other’s secret number.  
3. After each guess, the game will show how many:
   - 🐂 **Bulls** — Correct digit in correct position  
   - 🐮 **Cows** — Correct digit in wrong position  
4. Keep guessing until one player gets **4 Bulls** — that player wins! 🎉  

---

### 🛠️ How to Run Locally  
1. Make sure you have **Python 3.9 or above** installed.  
2. Install required package:
   ```bash
   pip install streamlit
