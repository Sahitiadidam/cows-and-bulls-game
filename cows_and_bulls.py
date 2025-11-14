import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Cows & Bulls - Two Player", layout="wide")
st.title("🐮 Cows & Bulls — Two Player")

# --- Helper functions ---
def valid_secret(s):
    return s.isdigit() and len(s) == 4 and len(set(s)) == 4

def check_cows_bulls(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls
    bull_positions = [i+1 for i, (s, g) in enumerate(zip(secret, guess)) if s == g]
    cow_positions = [i+1 for i, g in enumerate(guess) if g in secret and g != secret[i]]
    return cows, bulls, bull_positions, cow_positions

def reset_game():
    keys = ["player1_secret", "player2_secret", "secrets_set", "turn", "winner", "history1", "history2"]
    for k in keys:
        st.session_state[k] = None
    st.session_state["turn"] = 1
    st.session_state["secrets_set"] = False
    st.session_state["history1"] = []
    st.session_state["history2"] = []
    st.session_state["winner"] = None

# --- Session state initialization ---
if "secrets_set" not in st.session_state:
    st.session_state.secrets_set = False
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "player1_secret" not in st.session_state:
    st.session_state.player1_secret = None
if "player2_secret" not in st.session_state:
    st.session_state.player2_secret = None
if "history1" not in st.session_state:
    st.session_state.history1 = []
if "history2" not in st.session_state:
    st.session_state.history2 = []
if "winner" not in st.session_state:
    st.session_state.winner = None

# --- Sidebar Dashboard ---
st.sidebar.title("📊 Dashboard")
st.sidebar.subheader("Player 1 History")
if st.session_state.history1:
    for guess, cows, bulls, bp, cp in st.session_state.history1:
        st.sidebar.write(f"{guess} → Bulls: {bulls} (pos: {bp}), Cows: {cows} (pos: {cp})")
else:
    st.sidebar.write("No guesses yet.")

st.sidebar.subheader("Player 2 History")
if st.session_state.history2:
    for guess, cows, bulls, bp, cp in st.session_state.history2:
        st.sidebar.write(f"{guess} → Bulls: {bulls} (pos: {bp}), Cows: {cows} (pos: {cp})")
else:
    st.sidebar.write("No guesses yet.")

if st.sidebar.button("🔁 Restart Game"):
    reset_game()
    st.rerun()

# --- Secret Setup ---
if not st.session_state.secrets_set:
    st.subheader("Set Secrets for Players")
    col1, col2 = st.columns(2)

    with col1:
        p1 = st.text_input("Player 1 secret (4 unique digits)", type="password", key="p1_input")
        if st.button("Set Player 1 Secret"):
            if not valid_secret(p1):
                st.error("Secret must be 4 unique digits.")
            else:
                st.session_state.player1_secret = p1
                st.success("Player 1 secret set.")

    with col2:
        p2 = st.text_input("Player 2 secret (4 unique digits)", type="password", key="p2_input")
        if st.button("Set Player 2 Secret"):
            if not valid_secret(p2):
                st.error("Secret must be 4 unique digits.")
            else:
                st.session_state.player2_secret = p2
                st.success("Player 2 secret set.")

    # Start game
    if st.session_state.player1_secret and st.session_state.player2_secret:
        if st.session_state.player1_secret == st.session_state.player2_secret:
            st.warning("Both secrets are identical — consider using different secrets.")
        if st.button("✅ Start Game"):
            st.session_state.secrets_set = True
            st.rerun()

# --- Gameplay ---
else:
    if st.session_state.winner:
        st.success(f"🎉 Player {st.session_state.winner} wins!")
        st.balloons()
    else:
        st.subheader(f"Player {st.session_state.turn}'s Turn")
        guess = st.text_input(f"Player {st.session_state.turn} enter 4-digit guess:", key=f"guess_input_{st.session_state.turn}")
        if st.button("Check Guess"):
            if not (guess.isdigit() and len(guess) == 4):
                st.warning("Enter a 4-digit numeric guess.")
            else:
                secret = st.session_state.player2_secret if st.session_state.turn == 1 else st.session_state.player1_secret
                cows, bulls, bull_pos, cow_pos = check_cows_bulls(secret, guess)
                
                # Save history
                if st.session_state.turn == 1:
                    st.session_state.history1.append((guess, cows, bulls, bull_pos, cow_pos))
                else:
                    st.session_state.history2.append((guess, cows, bulls, bull_pos, cow_pos))

                if bulls == 4:
                    st.session_state.winner = st.session_state.turn
                    st.success(f"🎉 Player {st.session_state.turn} guessed it right and wins!")
                    st.balloons()
                else:
                    st.error(f"❌ Wrong guess! Bulls: {bulls} (pos: {bull_pos}), Cows: {cows} (pos: {cow_pos})")
                    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
                    st.rerun()
