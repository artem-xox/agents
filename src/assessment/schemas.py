from dataclasses import dataclass


@dataclass
class Question:
    text: str
    expected_answer: str


@dataclass
class Verdict:
    answer: str
    is_correct: bool
    explanation: str


@dataclass
class Assessment:
    question: Question
    verdict: Verdict
