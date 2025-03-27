import streamlit as st
import zxcvbn 
import re

def evaluate_password(password):
    """Evaluates password strength based on rules and zxcvbn analysis."""
   
    # Use zxcvbn for overall strength analysis
    result = zxcvbn.zxcvbn(password)
    score = result['score']  # Score from 0 (weak) to 4 (very strong)
   
    # Custom rule-based analysis
    length_score = len(password) >= 12  # Minimum 12 characters
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[@$!%*?&#^()_+<>]', password))
   
    # Calculate rule-based strength level
    complexity = sum([length_score, has_upper, has_lower, has_digit, has_special])
   
    # Convert scores to labels
    strength_levels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    strength = strength_levels[max(score, complexity - 1)]
   
    # Feedback messages
    feedback = []
    if not length_score:
        feedback.append("Use at least 12 characters.")
    if not has_upper:
        feedback.append("Include at least one uppercase letter (A-Z).")
    if not has_lower:
        feedback.append("Include at least one lowercase letter (a-z).")
    if not has_digit:
        feedback.append("Include at least one number (0-9).")
    if not has_special:
        feedback.append("Include at least one special character (@$!%*?&#^).")

    return strength, feedback

# Streamlit UI
st.title("🔒 Password Strength Meter")

password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = evaluate_password(password)
   
    # Display strength with color
    color_map = {
        "Very Weak": "red",
        "Weak": "orange",
        "Fair": "yellow",
        "Strong": "green",
        "Very Strong": "darkgreen",
    }
    st.markdown(f"**Strength:** <span style='color:{color_map[strength]}; font-weight:bold'>{strength}</span>", unsafe_allow_html=True)

    # Display feedback
    if feedback:
        st.subheader("Suggestions to Improve:")
        for tip in feedback:
            st.write(f"- {tip}")

