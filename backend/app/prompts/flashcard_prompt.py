FLASHCARD_PROMPT = """Generate {number_of_cards} concise flashcards using ONLY the supplied transcript.
Return JSON only: {{"flashcards":[{{"front":"question or term","back":"answer or explanation"}}]}}

Transcript:
{transcript}"""
