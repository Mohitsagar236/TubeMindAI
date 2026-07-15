NOTES_PROMPT = """Convert ONLY the supplied YouTube transcript into student-friendly Markdown study notes.
Do not add outside information. Omit sections the transcript cannot support.

Use this structure:
# Title
## 1. Introduction
## 2. Key Concepts
## 3. Detailed Explanation
## 4. Examples
## 5. Important Points
## 6. Quick Revision
## 7. Interview Questions

Transcript:
{transcript}

Study Notes:"""
