from src.assessment.schemas import Question

QUESTIONS = [
    Question(
        text="what is the weather in paris?",
        expected_answer="hot",
    ),
    Question(
        text="weather in ny now?",
        expected_answer="cold",
    ),
]
