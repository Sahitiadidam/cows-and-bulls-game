import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Cows & Bulls - Two Player", layout="centered")
st.title("🐮 Cows & Bulls — Two Player")

# --- Helper functions ---
def valid_secret(s):
    return s.isdigit() and len(s) == 4 and len(set(s)) == 4

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
for key in ["player1_secret", "player2_secret", "secrets_set", "turn", "winner", "history1", "history2"]:
    if key not in st.session_state:
        st.session_state[key] = None if key not in ["turn", "history1", "history2"] else (1 if key=="turn" else [])

if st.session_state.secrets_set is None:
    st.session_state.secrets_set = False
if st.session_state.turn is None:
    st.session_state.turn = 1

st.markdown("Enter secret numbers for Player 1 and Player 2. They will be hidden from the other player.")

# --- Secret setup ---
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

    # Start game button
    if st.session_state.player1_secret and st.session_state.player2_secret:
        if st.session_state.player1_secret == st.session_state.player2_secret:
            st.warning("Both secrets are identical — consider using different secrets.")
        if st.button("✅ Start Game"):
            st.session_state.secrets_set = True
            st.rerun()  # updated here

    st.divider()
    st.info("Secrets are stored in this browser session only. Reloading page will reset the game unless you use the Restart button below.")
    if st.button("🔁 Restart/Reset"):
        reset_game()
        st.rerun()  # updated here

# --- Gameplay ---
else:
    st.subheader(f"Player {st.session_state.turn}'s Turn")
    st.write("Hint: Bulls = correct digit in correct position. Cows = correct digit wrong position.")

    # Show history
    with st.expander("📚 Guess History (click to open)"):
        st.write("Player 1 guesses:")
        if st.session_state.history1:
            for g, b_count, c_count, b_pos, c_pos in st.session_state.history1:
                st.write(f"- {g} → 🐂 Bulls: {b_count} (positions: {b_pos}) | 🐮 Cows: {c_count} (positions: {c_pos})")
        else:
            st.write("- No guesses yet.")

        st.write("---")
        st.write("Player 2 guesses:")
        if st.session_state.history2:
            for g, b_count, c_count, b_pos, c_pos in st.session_state.history2:
                st.write(f"- {g} → 🐂 Bulls: {b_count} (positions: {b_pos}) | 🐮 Cows: {c_count} (positions: {c_pos})")
        else:
            st.write("- No guesses yet.")

    # Player guess form
    with st.form("guess_form"):
        guess = st.text_input(f"Player {st.session_state.turn} enter 4-digit guess:", key=f"guess_input")
        submit_guess = st.form_submit_button("Check Guess")

        if submit_guess:
            if not (guess.isdigit() and len(guess) == 4):
                st.warning("Enter a 4-digit numeric guess.")
            else:
                secret = st.session_state.player2_secret if st.session_state.turn == 1 else st.session_state.player1_secret

                # Calculate bulls and cows
                bulls = [i+1 for i, (s,g) in enumerate(zip(secret, guess)) if s == g]
                cows = [i+1 for i, g in enumerate(guess) if g in secret and g != secret[i]]
                bull_count = len(bulls)
                cow_count = len(cows)

                # Update history
                if st.session_state.turn == 1:
                    st.session_state.history1.append((guess, bull_count, cow_count, bulls, cows))
                else:
                    st.session_state.history2.append((guess, bull_count, cow_count, bulls, cows))

                # Display feedback
                if bull_count == 4:
                    st.session_state.winner = st.session_state.turn
                    st.success(f"🎉 Player {st.session_state.turn} guessed it right and wins!")
                    st.balloons()
                else:
                    st.info(f"❌ Wrong guess!\n🐂 Bulls: {bull_count} (positions: {bulls}) | 🐮 Cows: {cow_count} (positions: {cows})")
                    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
                    st.info(f"Now it's Player {st.session_state.turn}'s turn.")
                    st.rerun()  # updated here

    st.divider()
    if st.button("🔁 Restart Game"):
        reset_game()
        st.rerun()  # updated here
