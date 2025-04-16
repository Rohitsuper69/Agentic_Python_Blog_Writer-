import spacy

class TopicAgent:
    def __init__(self, topic, tone=None):
        """
        Initializes TopicAgent with a blog topic and optional writing tone.
        Loads the spaCy NLP pipeline for English.
        """
        self.topic = topic.strip()
        self.tone = tone or "educational"
        self.nlp = spacy.load("en_core_web_sm")

    def split_and_clean(self, phrase):
        """
        Tokenizes a phrase and splits it using conjunctions (and/or).
        Filters out stopwords and non-alphabetic tokens.
        Capitalizes and groups meaningful word chunks.
        """
        doc = self.nlp(phrase)
        parts = []
        current = []
        for token in doc:
            if token.text.lower() in {"and", "or"}:
                if current:
                    parts.append(current)
                    current = []
            elif not token.is_stop and token.is_alpha:
                current.append(token.text.capitalize())
        if current:
            parts.append(current)

        # Reconstruct cleaned sub-phrases
        return [" ".join(part) for part in parts if len(part) > 0]

    def extract_subtopics(self):
        """
        Extracts noun phrases and named entities from the topic.
        Breaks them into smaller subtopics using `split_and_clean`.
        Ensures uniqueness and filters by length (≤ 5 words).
        Returns up to 5 clean subtopics or the main topic title-cased.
        """
        doc = self.nlp(self.topic)

        raw_candidates = [chunk.text for chunk in doc.noun_chunks]
        raw_candidates += [ent.text for ent in doc.ents]

        split_phrases = []
        for phrase in raw_candidates:
            split_phrases.extend(self.split_and_clean(phrase))

        # Remove duplicates and overly long phrases
        seen = set()
        final = []
        for phrase in split_phrases:
            key = phrase.lower()
            if key not in seen and len(phrase.split()) <= 5:
                seen.add(key)
                final.append(phrase)

        return final[:5] or [self.topic.title()]

    def analyze(self):
        """
        Returns a tuple: (list of subtopics, selected tone).
        """
        subtopics = self.extract_subtopics()
        return subtopics, self.tone
