import streamlit as st

st.set_page_config(page_title="Cows & Bulls - Two Player", layout="centered")

st.title("🐮 Cows & Bulls — Two Player")

# --- helper functions ---
def valid_secret(s):
    return s.isdigit() and len(s) == 4 and len(set(s)) == 4

def check_cows_bulls(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls
    
    bull_positions = [i+1 for i, (s, g) in enumerate(zip(secret, guess)) if s == g]
    cow_positions = [i+1 for i, g in enumerate(guess) if g in secret and g != secret[i]]
    
    return cows, bulls, bull_positions, cow_positions


def reset_game():
    keys = [
        "player1_secret", "player2_secret", "secrets_set", "turn",
        "winner", "history1", "history2", "guesses1", "guesses2"
    ]
    for k in keys:
        st.session_state[k] = None
    st.session_state["turn"] = 1
    st.session_state["secrets_set"] = False
    st.session_state["history1"] = []
    st.session_state["history2"] = []
    st.session_state["winner"] = None
    st.session_state["guesses1"] = 0
    st.session_state["guesses2"] = 0

# --- session state defaults ---
defaults = {
    "player1_secret": None,
    "player2_secret": None,
    "secrets_set": False,
    "turn": 1,
    "winner": None,
    "history1": [],
    "history2": [],
    "guesses1": 0,
    "guesses2": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("Enter secret numbers for Player 1 and Player 2. They will be hidden from the other player.")

# --- Secret setup stage ---
if not st.session_state.secrets_set:
    col1, col2 = st.columns(2)
    with col1:
        with st.form("p1_form"):
            p1 = st.text_input("Player 1 secret (4 unique digits)", type="password", key="p1_input")
            submit1 = st.form_submit_button("Set Player 1 Secret")
            if submit1:
                if not valid_secret(p1):
                    st.error("Player 1 secret must be 4 unique digits (0-9).")
                else:
                    st.session_state.player1_secret = p1
                    st.success("Player 1 secret set.")
    with col2:
        with st.form("p2_form"):
            p2 = st.text_input("Player 2 secret (4 unique digits)", type="password", key="p2_input")
            submit2 = st.form_submit_button("Set Player 2 Secret")
            if submit2:
                if not valid_secret(p2):
                    st.error("Player 2 secret must be 4 unique digits (0-9).")
                else:
                    st.session_state.player2_secret = p2
                    st.success("Player 2 secret set.")

    if st.session_state.player1_secret and st.session_state.player2_secret:
        if st.session_state.player1_secret == st.session_state.player2_secret:
            st.warning("Both secrets are identical — consider using different secrets.")
        if st.button("✅ Start Game"):
            st.session_state.secrets_set = True
            st.rerun()

    st.divider()
    st.info("Secrets are stored in this browser session only. Reloading page will reset the game unless you use the Restart button below.")
    if st.button("🔁 Restart/Reset"):
        reset_game()
        st.rerun()

# --- Gameplay stage ---
else:
    st.subheader(f"Player {st.session_state.turn}'s Turn")
    st.write("Hint: Bulls = correct digit in correct position. Cows = correct digit wrong position.")

    # --- Scoreboard section ---
    st.markdown("### 🧮 Scoreboard")
    col_score1, col_score2 = st.columns(2)
    with col_score1:
        st.metric("Player 1 Guesses", st.session_state.guesses1)
    with col_score2:
        st.metric("Player 2 Guesses", st.session_state.guesses2)

    # show history
    with st.expander("📚 Guess History (click to open)"):
        st.write("Player 1 guesses:")
        if st.session_state.history1:
            for g, c, b in st.session_state.history1:
                st.write(f"- {g} → Bulls: {b}, Cows: {c}")
        else:
            st.write("- No guesses yet.")
        st.write("---")
        st.write("Player 2 guesses:")
        if st.session_state.history2:
            for g, c, b in st.session_state.history2:
                st.write(f"- {g} → Bulls: {b}, Cows: {c}")
        else:
            st.write("- No guesses yet.")

    # Guess section
    with st.form("guess_form"):
        guess = st.text_input(f"Player {st.session_state.turn} enter 4-digit guess:", key=f"guess_input")
        submit_guess = st.form_submit_button("Check Guess")

        if submit_guess:
            if not (guess.isdigit() and len(guess) == 4):
                st.warning("Enter a 4-digit numeric guess.")
            else:
                if st.session_state.turn == 1:
                    secret = st.session_state.player2_secret
                else:
                    secret = st.session_state.player1_secret

                cows, bulls = check_cows_bulls(secret, guess)

                # store history
                if st.session_state.turn == 1:
                    st.session_state.history1.append((guess, cows, bulls))
                    st.session_state.guesses1 += 1
                else:
                    st.session_state.history2.append((guess, cows, bulls))
                    st.session_state.guesses2 += 1

                # --- feedback and next steps ---
                if bulls == 4:
                    st.session_state.winner = st.session_state.turn
                    st.success(f"🎉 Player {st.session_state.turn} guessed it right and wins!")
                    st.balloons()
                else:
                    st.error("❌ Wrong guess! Try again next turn.")
                    st.info(f"👉 You got {bulls} Bulls and {cows} Cows this round.")
                    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
                    st.rerun()

    st.divider()
    if st.button("🔁 Restart Game"):
        reset_game()
        st.rerun()

    if st.session_state.winner:
        st.success(f"🏆 Player {st.session_state.winner} wins the game!")
        st.info(f"Total Guesses — Player 1: {st.session_state.guesses1}, Player 2: {st.session_state.guesses2}")
