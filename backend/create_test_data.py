"""
Utility script to seed the database with sample Norwegian lessons and tests.

You can run it from the backend folder:
    python create_test_data.py

Or from the repository root:
    python backend/create_test_data.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List

import django


def bootstrap_django() -> None:
    """Ensure Django settings are loaded whether we run from root or backend."""
    current_dir = Path(__file__).resolve().parent
    if (current_dir / 'manage.py').exists():
        backend_dir = current_dir
    elif (current_dir.parent / 'backend' / 'manage.py').exists():
        backend_dir = current_dir.parent / 'backend'
    else:
        raise RuntimeError("Could not find Django backend (manage.py).")

    sys.path.append(str(backend_dir))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()


def seed_sample_data() -> Dict[str, int]:
    """Create sample lessons, tests, questions, and answers."""
    from apps.tests.models import Answer, Lesson, Question, Test
    from django.contrib.auth.models import User

    author, _ = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True},
    )

    sample_lessons: List[Dict] = [
        {
            "title": "Introduksjon til norsk",
            "description": "Hilsener, alfabet og grunnleggende uttrykk.",
            "level": "A1",
            "tests": [
                {
                    "title": "Hilsener og høflighet",
                    "description": "Enkle hilsener og avslutninger.",
                    "duration_minutes": 8,
                    "questions": [
                        {
                            "text": "Skriv norsk hilsen som betyr «hello».",
                            "answer": "hei",
                            "alternatives": ["hallo", "hei!"],
                        },
                        {
                            "text": "Fullfør setningen: «God ____!» (morning)",
                            "answer": "morgen",
                            "alternatives": ["mårgen"],
                        },
                        {
                            "text": "Hvordan sier du «takk» på norsk?",
                            "answer": "takk",
                            "alternatives": ["tusen takk", "takk!"],
                        },
                    ],
                }
            ],
        },
        {
            "title": "Verb i presens",
            "description": "Vanlige verb i nåtid.",
            "level": "A1",
            "tests": [
                {
                    "title": "Hverdag og bosted",
                    "description": "Fyll inn riktige verbformer i presens.",
                    "duration_minutes": 10,
                    "questions": [
                        {"text": "Fyll inn: Jeg ___ kaffe hver dag. (drikke)", "answer": "drikker"},
                        {"text": "Fyll inn: Hun ___ i Oslo. (bo)", "answer": "bor"},
                        {"text": "Fullfør setningen: Vi ___ norske. (være)", "answer": "er"},
                    ],
                }
            ],
        },
        {
            "title": "Staving og vokaler",
            "description": "Øv på æ, ø og å i vanlige ord.",
            "level": "A1",
            "tests": [
                {
                    "title": "Vokaler med tegn",
                    "description": "Fokuser på de tre norske spesialvokalene.",
                    "duration_minutes": 9,
                    "questions": [
                        {"text": "Hvilken bokstav mangler? sm_r (ord for «butter»)", "answer": "ø"},
                        {"text": "Fyll inn riktig bokstav: bl_bær (bær med blå farge)", "answer": "å"},
                        {"text": "Fullfør navnet på dyret: bj_rn (dyr i skogen)", "answer": "ø"},
                    ],
                }
            ],
        },
    ]

    counters = {"lessons": 0, "tests": 0, "questions": 0, "answers": 0}

    for lesson_data in sample_lessons:
        lesson, _ = Lesson.objects.update_or_create(
            title=lesson_data["title"],
            defaults={
                "description": lesson_data.get("description", ""),
                "level": lesson_data.get("level", "A1"),
                "created_by": author,
            },
        )
        # Ensure ownership and metadata are kept in sync for existing lessons
        lesson.description = lesson_data.get("description", "")
        lesson.level = lesson_data.get("level", "A1")
        lesson.created_by = author
        lesson.save(update_fields=["description", "level", "created_by"])
        counters["lessons"] += 1

        for test_data in lesson_data["tests"]:
            test, _ = Test.objects.update_or_create(
                lesson=lesson,
                title=test_data["title"],
                defaults={
                    "description": test_data.get("description", ""),
                    "test_type": test_data.get("test_type", "fill-in-the-blank"),
                    "duration_minutes": test_data.get("duration_minutes", 15),
                    "show_correct_answers": True,
                    "show_errors_breakdown": True,
                },
            )
            test.description = test_data.get("description", "")
            test.test_type = test_data.get("test_type", "fill-in-the-blank")
            test.duration_minutes = test_data.get("duration_minutes", 15)
            test.show_correct_answers = True
            test.show_errors_breakdown = True
            test.save(
                update_fields=[
                    "description",
                    "test_type",
                    "duration_minutes",
                    "show_correct_answers",
                    "show_errors_breakdown",
                ]
            )
            counters["tests"] += 1

            # Replace questions for this sample test to keep content clean
            test.questions.all().delete()

            for index, question_data in enumerate(test_data["questions"], start=1):
                question = Question.objects.create(
                    test=test,
                    text=question_data["text"],
                    order=index,
                    difficulty=question_data.get("difficulty", 1),
                    explanation=question_data.get("explanation", ""),
                )
                counters["questions"] += 1

                # Create the correct answer first
                Answer.objects.create(
                    question=question,
                    text=question_data["answer"],
                    is_correct=True,
                    order=1,
                    explanation=question_data.get("explanation", ""),
                )
                counters["answers"] += 1

                for offset, alt in enumerate(question_data.get("alternatives", []), start=2):
                    Answer.objects.create(
                        question=question,
                        text=alt,
                        is_correct=False,
                        order=offset,
                    )
                    counters["answers"] += 1

    return counters


def main() -> None:
    bootstrap_django()
    counters = seed_sample_data()
    print(
        f"Seeded {counters['lessons']} lessons, {counters['tests']} tests, "
        f"{counters['questions']} questions and {counters['answers']} answers."
    )


if __name__ == '__main__':
    main()
