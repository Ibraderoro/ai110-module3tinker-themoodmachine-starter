"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# ---------------------------------------------------------------------
# EXTENSION: Slang, Emojis, Sarcasm, and Ambiguity (Challenge Items)
# ---------------------------------------------------------------------

# 1. Sarcasm / Tone Shift
SAMPLE_POSTS.append("Oh great, another unexpected unhandled exception to debug on a Friday night.")
TRUE_LABELS.append("negative")

# 2. Slang + Ambiguity
SAMPLE_POSTS.append("That interview was lowkey mid no cap, but the office looks beautiful.")
TRUE_LABELS.append("mixed")

# 3. Modern Vernacular / Slang
SAMPLE_POSTS.append("Senior developer pushed the hotfix right before deployment and it was a massive W.")
TRUE_LABELS.append("positive")

# 4. Complex Emoji Combinations
SAMPLE_POSTS.append("My environment layout is completely broken, cannot even pull from origin main branch 💀🥲")
TRUE_LABELS.append("negative")

# 5. Mixed Sentiment Cancelation Layer
SAMPLE_POSTS.append("The new framework performance is incredibly fast, but the documentation is awful.")
TRUE_LABELS.append("mixed")

# 6. Neutral Calibration / Structural Baseline
SAMPLE_POSTS.append("The team seminar is scheduled to take place on Tuesday at two o'clock in room four.")
TRUE_LABELS.append("neutral")


# --- CRITICAL INTEGRITY CHECK ---
# Enforces the deterministic length alignment constraint to prevent out-of-bounds index errors later.
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"🚨 DATASET LENGTH MISMATCH: SAMPLE_POSTS ({len(SAMPLE_POSTS)}) "
    f"does not match TRUE_LABELS ({len(TRUE_LABELS)})."
)