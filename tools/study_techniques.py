"""Advanced study technique recommendations using evidence-based learning methods.

This module provides tools for:
- Spaced repetition scheduling algorithms
- Active recall practice generation
- Study technique recommendations based on learning goals
- Progress tracking and adaptation
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math
import random


class SpacedRepetitionScheduler:
    """Implements various spaced repetition algorithms for optimal learning."""

    # Common spaced repetition intervals (in days)
    ALGORITHMS = {
        'leitner': [1, 2, 4, 7, 15, 30],  # Leitner box system
        'sm2': [1, 6],  # SuperMemo 2 simplified
        'fibonacci': [1, 1, 2, 3, 5, 8, 13, 21],  # Fibonacci sequence
        'exponential': lambda n: 2 ** (n-1)  # Exponential backoff
    }

    @staticmethod
    def calculate_next_review(algorithm: str, review_count: int, last_review: datetime,
                            performance_score: float = 1.0) -> datetime:
        """
        Calculate the next review date using specified algorithm.

        Args:
            algorithm: Name of the algorithm ('leitner', 'sm2', 'fibonacci', 'exponential')
            review_count: Number of times this item has been reviewed
            last_review: DateTime of last review
            performance_score: How well the student performed (0.0 to 1.0)

        Returns:
            DateTime for next review
        """
        if algorithm not in SpacedRepetitionScheduler.ALGORITHMS:
            algorithm = 'leitner'

        if algorithm == 'exponential':
            interval_func = SpacedRepetitionScheduler.ALGORITHMS[algorithm]
            days = interval_func(review_count)
        else:
            intervals = SpacedRepetitionScheduler.ALGORITHMS[algorithm]
            index = min(review_count - 1, len(intervals) - 1)
            days = intervals[index]

        # Adjust interval based on performance
        # Better performance = longer intervals, worse performance = shorter intervals
        adjustment_factor = 0.5 + performance_score  # Range: 0.5 to 1.5
        adjusted_days = int(days * adjustment_factor)

        return last_review + timedelta(days=adjusted_days)

    @staticmethod
    def get_optimal_study_schedule(topic: str, total_sessions: int = 7,
                                 algorithm: str = 'leitner') -> List[Dict]:
        """
        Generate an optimal study schedule for a topic using spaced repetition.

        Args:
            topic: The topic to study
            total_sessions: Number of study sessions to schedule
            algorithm: Spaced repetition algorithm to use

        Returns:
            List of study sessions with dates and recommendations
        """
        sessions = []
        current_date = datetime.now()

        for i in range(total_sessions):
            session = {
                'session_number': i + 1,
                'date': current_date.strftime('%Y-%m-%d'),
                'topic': topic,
                'focus': SpacedRepetitionScheduler._get_session_focus(i + 1, total_sessions),
                'technique': SpacedRepetitionScheduler._recommend_technique(i + 1),
                'estimated_duration': SpacedRepetitionScheduler._estimate_duration(i + 1)
            }
            sessions.append(session)

            # Calculate next session date
            if i < total_sessions - 1:
                current_date = SpacedRepetitionScheduler.calculate_next_review(
                    algorithm, i + 1, current_date, 0.8  # Assume good performance
                )

        return sessions

    @staticmethod
    def _get_session_focus(session_num: int, total_sessions: int) -> str:
        """Determine the focus for each study session."""
        if session_num == 1:
            return "Initial exposure and overview"
        elif session_num <= 3:
            return "Active recall and practice"
        elif session_num <= 5:
            return "Deep understanding and connections"
        else:
            return "Mastery and long-term retention"

    @staticmethod
    def _recommend_technique(session_num: int) -> str:
        """Recommend study technique based on session number."""
        techniques = [
            "Note-taking and concept mapping",
            "Practice testing and self-quizzing",
            "Teaching the material to someone else",
            "Spaced retrieval practice",
            "Interleaved practice with related topics",
            "Elaborative interrogation",
            "Dual coding (diagrams + text)"
        ]
        return techniques[min(session_num - 1, len(techniques) - 1)]

    @staticmethod
    def _estimate_duration(session_num: int) -> str:
        """Estimate duration for each study session."""
        if session_num == 1:
            return "45-60 minutes"
        elif session_num <= 3:
            return "30-45 minutes"
        else:
            return "20-30 minutes"


class ActiveRecallGenerator:
    """Generates active recall practice questions and exercises."""

    QUESTION_TYPES = [
        "definition_recall",
        "concept_application",
        "problem_solving",
        "comparison_analysis",
        "prediction_foresight",
        "critique_evaluation"
    ]

    @staticmethod
    def generate_recall_questions(topic: str, difficulty: str = "medium",
                                count: int = 5) -> List[Dict]:
        """
        Generate active recall questions for a topic.

        Args:
            topic: The topic to generate questions for
            difficulty: 'easy', 'medium', or 'hard'
            count: Number of questions to generate

        Returns:
            List of question dictionaries
        """
        questions = []

        for i in range(count):
            question_type = random.choice(ActiveRecallGenerator.QUESTION_TYPES)

            question = {
                'id': f"q_{i+1}",
                'type': question_type,
                'difficulty': difficulty,
                'question': ActiveRecallGenerator._generate_question_text(topic, question_type, difficulty),
                'hints': ActiveRecallGenerator._generate_hints(topic, question_type),
                'estimated_time': ActiveRecallGenerator._estimate_question_time(difficulty)
            }
            questions.append(question)

        return questions

    @staticmethod
    def _generate_question_text(topic: str, question_type: str, difficulty: str) -> str:
        """Generate specific question text based on type and difficulty."""

        templates = {
            "definition_recall": {
                "easy": f"What is the basic definition of {topic}?",
                "medium": f"Explain {topic} in your own words without looking at your notes.",
                "hard": f"Compare and contrast {topic} with a closely related concept."
            },
            "concept_application": {
                "easy": f"Give a simple example of {topic} in everyday life.",
                "medium": f"How would you apply {topic} to solve a real-world problem?",
                "hard": f"Design a complex scenario where {topic} plays a crucial role."
            },
            "problem_solving": {
                "easy": f"Solve this basic problem related to {topic}.",
                "medium": f"Analyze the steps needed to solve a {topic}-related challenge.",
                "hard": f"Create and solve an original problem involving {topic}."
            },
            "comparison_analysis": {
                "easy": f"What are the main similarities between {topic} and a related concept?",
                "medium": f"Compare the advantages and disadvantages of different approaches to {topic}.",
                "hard": f"Critically analyze how {topic} differs from alternative theories or methods."
            },
            "prediction_foresight": {
                "easy": f"What might happen if {topic} is applied incorrectly?",
                "medium": f"Predict the outcomes of a scenario involving {topic}.",
                "hard": f"Forecast how {topic} might evolve or change in the future."
            },
            "critique_evaluation": {
                "easy": f"What are the strengths of {topic}?",
                "medium": f"Evaluate the effectiveness of {topic} in different contexts.",
                "hard": f"Provide a comprehensive critique of {topic}, including limitations and potential improvements."
            }
        }

        return templates.get(question_type, {}).get(difficulty, f"Explain {topic} in detail.")

    @staticmethod
    def _generate_hints(topic: str, question_type: str) -> List[str]:
        """Generate helpful hints for difficult questions."""
        hints = {
            "definition_recall": [
                f"Think about the key characteristics of {topic}",
                "Recall the main purpose or function",
                "Consider related terms or concepts"
            ],
            "concept_application": [
                "Think of real-world scenarios",
                "Consider practical examples",
                "Break down the concept into steps"
            ],
            "problem_solving": [
                "Identify the key variables involved",
                "Consider what information you need",
                "Think step-by-step through the process"
            ]
        }

        return hints.get(question_type, ["Try to recall the main ideas", "Think about examples", "Break it down into smaller parts"])

    @staticmethod
    def _estimate_question_time(difficulty: str) -> str:
        """Estimate time needed for different difficulty questions."""
        times = {
            "easy": "2-3 minutes",
            "medium": "5-7 minutes",
            "hard": "10-15 minutes"
        }
        return times.get(difficulty, "5-10 minutes")


def recommend_study_technique(goal: str, time_available: int, current_knowledge: str) -> Dict:
    """
    Recommend the best study technique based on learning goals and constraints.

    Args:
        goal: Learning goal ('memorization', 'understanding', 'application', 'analysis')
        time_available: Minutes available for study
        current_knowledge: 'beginner', 'intermediate', 'advanced'

    Returns:
        Dictionary with recommended technique and rationale
    """
    techniques = {
        "memorization": {
            "beginner": "Spaced repetition flashcards",
            "intermediate": "Active recall testing",
            "advanced": "Memory palace technique"
        },
        "understanding": {
            "beginner": "Concept mapping with explanations",
            "intermediate": "Teaching the material",
            "advanced": "Comparative analysis"
        },
        "application": {
            "beginner": "Guided practice problems",
            "intermediate": "Real-world application scenarios",
            "advanced": "Problem creation and solving"
        },
        "analysis": {
            "beginner": "Compare and contrast exercises",
            "intermediate": "Critical evaluation",
            "advanced": "Theoretical critique and synthesis"
        }
    }

    recommended = techniques.get(goal, techniques["understanding"]).get(current_knowledge, "Active recall practice")

    # Adjust based on time available
    if time_available < 15:
        recommended = "Quick active recall quiz"
    elif time_available < 30:
        recommended = "Focused practice testing"
    elif time_available > 60:
        recommended = f"{recommended} with interleaved practice"

    return {
        "technique": recommended,
        "goal": goal,
        "time_available": time_available,
        "current_knowledge": current_knowledge,
        "rationale": f"This technique is optimal for {goal} when you have {time_available} minutes and {current_knowledge} knowledge level."
    }


# Tool functions for Agno integration

def generate_spaced_study_schedule(topic: str, sessions: int = 7, algorithm: str = "leitner") -> str:
    """Generate a spaced repetition study schedule for a topic."""
    try:
        schedule = SpacedRepetitionScheduler.get_optimal_study_schedule(topic, sessions, algorithm)

        result = f"**Spaced Repetition Study Schedule for: {topic}**\n\n"
        result += f"**Algorithm:** {algorithm.title()}\n"
        result += f"**Total Sessions:** {sessions}\n\n"

        for session in schedule:
            result += f"**Session {session['session_number']}:** {session['date']}\n"
            result += f"   • Focus: {session['focus']}\n"
            result += f"   • Technique: {session['technique']}\n"
            result += f"   • Duration: {session['estimated_duration']}\n\n"

        result += "**Tips:**\n"
        result += "• Test yourself before looking at answers\n"
        result += "• Space out your practice sessions\n"
        result += "• Focus on difficult items more frequently\n"
        result += "• Review material just before you forget it\n"

        return result

    except Exception as e:
        return f"Error generating study schedule: {str(e)}"


def generate_active_recall_questions(topic: str, difficulty: str = "medium", count: int = 5) -> str:
    """Generate active recall practice questions."""
    try:
        questions = ActiveRecallGenerator.generate_recall_questions(topic, difficulty, count)

        result = f"**Active Recall Practice Questions for: {topic}**\n\n"
        result += f"**Difficulty:** {difficulty.title()}\n"
        result += f"**Questions:** {count}\n\n"

        for question in questions:
            result += f"**Question {question['id']}:** {question['question']}\n"
            result += f"   • Type: {question['type'].replace('_', ' ').title()}\n"
            result += f"   • Estimated time: {question['estimated_time']}\n"

            if question['hints']:
                result += "   • Hints:\n"
                for hint in question['hints']:
                    result += f"     - {hint}\n"

            result += "\n"

        result += "**Instructions:**\n"
        result += "• Try to answer each question without looking at your notes\n"
        result += "• Use hints only if you're truly stuck\n"
        result += "• Review correct answers and understand why you got them wrong\n"
        result += "• Repeat difficult questions in future sessions\n"

        return result

    except Exception as e:
        return f"Error generating recall questions: {str(e)}"


def recommend_study_technique_tool(goal: str, time_available: int, current_knowledge: str) -> str:
    """Recommend the best study technique for specific conditions."""
    try:
        recommendation = recommend_study_technique(goal, time_available, current_knowledge)

        result = "**🎯 Personalized Study Technique Recommendation**\n\n"
        result += f"**Recommended Technique:** {recommendation['technique']}\n\n"
        result += f"**Learning Goal:** {recommendation['goal']}\n"
        result += f"**Time Available:** {recommendation['time_available']} minutes\n"
        result += f"**Knowledge Level:** {recommendation['current_knowledge']}\n\n"
        result += f"**Why this technique:** {recommendation['rationale']}\n\n"

        # Add implementation tips
        result += "**💡 Implementation Tips:**\n"
        if "recall" in recommendation['technique'].lower():
            result += "• Test yourself before looking at answers\n"
            result += "• Use spaced repetition for better retention\n"
        elif "teaching" in recommendation['technique'].lower():
            result += "• Explain concepts as if teaching a friend\n"
            result += "• Use simple language and examples\n"
        elif "practice" in recommendation['technique'].lower():
            result += "• Start with easier problems, then progress\n"
            result += "• Review mistakes and understand solutions\n"
        elif "mapping" in recommendation['technique'].lower():
            result += "• Draw connections between concepts\n"
            result += "• Use colors and diagrams for visual learning\n"

        return result

    except Exception as e:
        return f"Error generating technique recommendation: {str(e)}"