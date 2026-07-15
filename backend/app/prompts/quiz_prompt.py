QUIZ_PROMPT = """Generate {number_of_questions} {difficulty} MCQs using ONLY the supplied transcript.
Each question must have exactly four distinct options, one correct answer copied exactly from its options, and a brief transcript-grounded explanation.
Return JSON only: {{"questions":[{{"question":"...","options":["...","...","...","..."],"correctAnswer":"...","explanation":"..."}}]}}

Transcript:
{transcript}"""
