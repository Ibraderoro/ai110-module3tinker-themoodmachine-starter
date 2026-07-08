# Model Card: Mood Machine

This model card covers the architecture, data composition, behavioral metrics, and ethical boundaries of **The Mood Machine** project, contrasting a hand-crafted **Rule-Based Model** (`mood_analyzer.py`) with a data-driven **Machine Learning Model** (`ml_experiments.py`)[cite: 1].

---

## 1. Model Overview

**Model type:**  
I compared both models—the hand-crafted rule-based system and the trained scikit-learn machine learning system[cite: 1].

**Intended purpose:**  
The system evaluates short social media updates or text snippets and classifies them into one of four emotional categories: `positive`, `negative`, `neutral`, or `mixed`[cite: 1].

**How it works (brief):**  
*   **Rule-Based Model:** Tokenizes a raw text string, converts it to lowercase, strips common outer punctuation, and loops over the terms[cite: 1]. It increases or decreases a numeric score based on manual dictionary matches while checking a simple look-ahead flag to handle basic negations[cite: 1].
*   **ML Model:** Uses scikit-learn's `CountVectorizer` to convert text into frequency tokens (Bag-of-Words) and uses a linear classifier to automatically learn feature-to-label probability weights from our human-coded examples[cite: 1].

---

## 2. Data

**Dataset description:**  
The dataset consists of 12 short-form text items within `SAMPLE_POSTS`[cite: 1]. It includes the 6 default starter items plus 6 custom entries manually appended to test edge-case phrasings like modern internet vernacular, emojis, and irony.

**Labeling process:**  
Labels in `TRUE_LABELS` were manually specified based on true contextual human intent rather than literal word presence. Sarcastic text lines were labeled with their underlying true negative intent, while sentences containing heavily balanced, clashing sentiments were explicitly tagged as `mixed`.

**Important characteristics of your dataset:**  
*   Contains modern tech vernacular/slang (`"lowkey"`, `"mid"`, `"no cap"`, `"W"`, `"cooked"`).
*   Utilizes standalone and terminating expressive emojis as heavy sentiment anchors (`💀`, `🥲`).
*   Includes high-contrast sarcasm where the overall sentiment runs inverse to literal phrase definitions.
*   Features structured mixed-sentiment strings where positive features and negative features collide equally.

**Possible issues with the dataset:**  
Extreme data volume constraints. Because the model's entire worldview is restricted to a small 12-row sample, any word or slang token absent from the dataset carries zero pre-calculated weight, causing the systems to display extreme fragility when exposed to wider language usage[cite: 1].

---

## 3. How the Rule-Based Model Works (if used)

**Your scoring rules:**  
*   **Keyword Accumulation:** Standard positive word matches increment the score by `+1`, while negative matches decrement it by `-1`[cite: 1].
*   **Negation Intercept Window:** If a modifier token (`"not"`, `"never"`, `"no"`) is parsed, a state flag trips, flipping the mathematical trajectory of the immediate next sentiment token.
*   **Emoji Weighting:** Expressive emojis bypass text filtering and map to amplified static point values (`💀` adds `-2`, `🔥` adds `+2`) to catch visual shorthand signals.
*   **Threshold Gates:** Standard scores $>0$ yield `positive`, and scores $<0$ yield `negative`[cite: 1]. If a score resolves to exactly `0` but the underlying text contains active hits from *both* positive and negative token lists, the engine maps it to `mixed` instead of defaulting to a flat `neutral` line.

**Strengths of this approach:**  
It is completely deterministic and easy to inspect[cite: 1]. You can trace every single token pass step-by-step to see exactly which logic branches fired, allowing for straightforward code adjustments[cite: 1].

**Weaknesses of this approach:**  
Highly brittle by nature[cite: 1]. It is entirely blind to tone, subtext, or real-world situational context[cite: 1]. If a slang term is unmapped or a word is misspelled, the system drops the signal entirely.

---

## 4. How the ML Model Works (if used)

**Features used:**  
Text strings are vectorized into token frequency matrices utilizing a **Bag-of-Words configuration via `CountVectorizer`**[cite: 1].

**Training data:**  
The model trained directly on the text arrays in `SAMPLE_POSTS` matched against the indices of the `TRUE_LABELS` answer key[cite: 1].

**Training behavior:**  
The ML model achieved a perfect optimization score of **1.00 (100% accuracy) on the training dataset**[cite: 1]. However, this perfect score represents an absolute state of training memorization (overfitting); the model simply built explicit rules around the precise word frequencies of those 12 specific rows[cite: 1].

**Strengths and weaknesses:**  
*   **Strengths:** Automatically maps complex multi-word features and hidden token combinations without requiring a developer to write tedious if-else rule structures[cite: 1].
*   **Weaknesses:** Highly vulnerable to picking up spurious cues or single dominant tokens[cite: 1]. If a positive word like `"love"` is over-represented across positive training lines, its probability weight becomes massive, causing the model to misclassify any new sentence containing it, regardless of negative qualifiers[cite: 1].

---

## 5. Evaluation

**How you evaluated the model:**  
Both versions were evaluated against the 12 items in `dataset.py`[cite: 1]. The rule-based engine successfully handled adjacent negations but struggled with sarcasm[cite: 1]. The ML engine scored a 1.00 on the active dataset but immediately displayed vulnerability when exposed to unseen test phrasings[cite: 1].

**Examples of correct predictions:**  
1.  *“I am not happy about this”* $\rightarrow$ **Rule-Based Model predicted: negative**. Correct because the negation look-ahead flag successfully intercepted the token `"not"` and inverted the positive weight of `"happy"`.
2.  *“Oh great, I love getting flat tires on my way to an interview.”* $\rightarrow$ **ML Model predicted: negative**. Correct because the model observed the phrase `"oh great"` paired with a negative target label within its small training data environment, allowing it to correctly predict a negative state.

**Examples of incorrect predictions:**  
1.  *“Oh great, another unexpected unhandled exception...”* $\rightarrow$ **Rule-Based Model predicted: positive**. Failed because it extracted the literal word `"great"` from its static lookup set, missing the sarcastic, frustrating nature of a software crash[cite: 1].
2.  *“I absolutely love it when my code crashes right before a demo.”* $\rightarrow$ **ML Model predicted: positive**. Failed because the token `"love"` carried a heavy, pre-calculated statistical probability for the `positive` class based on the training samples, completely overwhelming the unseen technical words like `"crashes"` or `"demo"`[cite: 1].

---

## 6. Limitations

*   **Sarcasm Blindness:** Neither model can compute tone irony or subtext reliably; they are easily misled by individual word signals[cite: 1]. As proven by the input *“I absolutely love it when my code crashes...”*, an explicit positive word completely breaks the statistical pipeline when used sarcastically.
*   **Small Worldview Constraints:** The dataset is far too small to generalize to real-world deployment[cite: 1]. Unseen text inputs cause the system's prediction paths to fail or drift unpredictably.

---

## 7. Ethical Considerations

*   **Linguistic Style Bias:** Testing revealed that when sentiment is expressed in formal language, the system performs cleanly. However, if a user employs modern vernacular or regional slang (*"absolute fire, no cap"*), the rule-based model scores it as neutral because the tokens fall outside standard list parameters. This introduces a systematic bias where the accuracy of the system is directly linked to *who* wrote the post and their cultural background, rather than *what* they actually meant[cite: 1]. This systematically underserves informal language communities.
*   **Distress Misclassification:** Deploying this system to automatically monitor customer support or student feedback channels could result in critical expressions of frustration or distress being incorrectly classified as "positive" due to sarcastic framing (e.g., *"This is just great"*), causing critical alerts to be missed[cite: 1].

---

## 8. Ideas for Improvement

*   **Incorporate n-gram Feature Windows:** Configure the `CountVectorizer` to extract pairs and triplets of consecutive words (`ngram_range=(1, 3)`) to help the machine learning model capture multi-word negations and context phrases automatically.
*   **Deploy True Out-of-Sample Validation:** Restructure the project to use a distinct validation and testing split rather than calculating accuracy metrics purely on training data, providing a true measure of real-world generalization[cite: 1].
*   **Add an Unseen Token Fallback Engine:** Enhance the rule-based logic to handle unknown words gracefully, ensuring unmapped slang phrases do not cause the scoring metrics to fluctuate wildly[cite: 1].