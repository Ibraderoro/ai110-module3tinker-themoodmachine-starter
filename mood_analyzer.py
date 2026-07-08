# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, date

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A simple, rule based mood classifier implementing negation windows.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster O(1) lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)
        
        # Modeling Improvement: Custom strong signal vocabulary mappings
        self.negation_signals = {"not", "no", "never", "lowkey"}
        self.emoji_weights = {
            "💀": -2, "🥲": -1, "😭": -2, "😡": -2,
            "😊": 1, "😂": 1, "🔥": 2, "👑": 2
        }

    # ---------------------------------------------------------------------
    # 1. Preprocessing (Representation Layer)
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of normalized tokens the model can work with.
        """
        cleaned = text.strip().lower()
        raw_tokens = cleaned.split()
        
        cleaned_tokens = []
        for token in raw_tokens:
            # Strip outer punctuation boundaries while ensuring inline emojis survive
            stripped = token.strip(".,!?\"'()")
            if stripped:
                cleaned_tokens.append(stripped)

        return cleaned_tokens

    # ---------------------------------------------------------------------
    # 2. Scoring Logic (Scoring / Detection Layer)
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Implements modeling improvements:
          - Advanced negation look-ahead flags ("not happy" reverses score trajectory)
          - Strong emoji/slang signal multiplier adjustments
        """
        tokens = self.preprocess(text)
        score = 0
        negate_next = False

        for token in tokens:
            # Check for strong emoji/slang overrides first
            if token in self.emoji_weights:
                score += self.emoji_weights[token]
                continue

            # Check if current word trips a negation multiplier look-ahead
            if token in self.negation_signals:
                negate_next = True
                continue

            # Core Keyword Scoring Blocks
            if token in self.positive_words:
                if negate_next:
                    score -= 1  # e.g., "not happy" flips the positive word to a negative index
                    negate_next = False
                else:
                    score += 1
            elif token in self.negative_words:
                if negate_next:
                    score += 1  # e.g., "not bad" flips the negative word to a positive index
                    negate_next = False
                else:
                    score -= 1
            else:
                # Reset negation flag if a neutral filler token is hit
                negate_next = False

        return score

    # ---------------------------------------------------------------------
    # 3. Label Prediction (Decision Rule Layer)
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a deterministic mood label.

        Features enhanced state mappings for the "mixed" sentiment classification.
        """
        score = self.score_text(text)
        tokens = self.preprocess(text)

        # Modeling Improvement: Isolate mixed sentiment states
        # Checks if both explicit sentiment profiles exist but mathematically canceled each other out
        has_positive = any(t in self.positive_words or self.emoji_weights.get(t, 0) > 0 for t in tokens)
        has_negative = any(t in self.negative_words or self.emoji_weights.get(t, 0) < 0 for t in tokens)

        if score == 0 and has_positive and has_negative:
            return "mixed"
        elif score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a clear summary explaining exactly WHY the engine arrived at its label choice.
        """
        tokens = self.preprocess(text)
        score = self.score_text(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []

        for token in tokens:
            if token in self.positive_words or (token in self.emoji_weights and self.emoji_weights[token] > 0):
                positive_hits.append(token)
            if token in self.negative_words or (token in self.emoji_weights and self.emoji_weights[token] < 0):
                negative_hits.append(token)

        return (
            f"Final Score = {score} "
            f"(positive signals: {positive_hits or '[]'}, "
            f"negative signals: {negative_hits or '[]'})"
        )