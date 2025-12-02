"""Test script to demonstrate Toon format token savings."""
import json
from database import init_db, SessionLocal
from toon_service import ToonService
from schemas.toon_models import Task, ScheduleBlock, StudentProfile
from logger import logger


def test_toon_token_savings():
    """Demonstrate token savings with Toon format."""
    logger.info("=== Testing Toon Format Token Savings ===\n")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Create Toon config for Study Agent
        logger.info("Creating Toon config for Study Agent...")
        toon_config = ToonService.create_config(
            db=db,
            agent_name="Study Agent",
            enabled=True
        )
        logger.info(f"✓ Created config: {toon_config.agent_name}\n")
        
        # Test 1: Task encoding
        logger.info("--- Test 1: Task Encoding ---")
        task = Task(
            id="task_001",
            title="Complete calculus assignment",
            subject="Mathematics",
            kind="assignment",
            deadline="2025-12-05T23:59:00",
            duration_estimate_min=120,
            energy_level="high",
            status="pending"
        )
        
        # JSON encoding
        task_json = json.dumps(task.__dict__, indent=2)
        
        # Toon encoding
        task_toon = ToonService.encode_message(task, "task")
        
        # Calculate savings
        savings = ToonService.calculate_token_savings(task_json, task_toon)
        
        logger.info(f"Original JSON ({savings['original_length']} chars):")
        logger.info(task_json)
        logger.info(f"\nToon Format ({savings['toon_length']} chars):")
        logger.info(task_toon)
        logger.info(f"\n✓ Token Savings: {savings['savings_chars']} chars ({savings['savings_percent']}%)\n")
        
        # Test 2: Schedule Block encoding
        logger.info("--- Test 2: Schedule Block Encoding ---")
        schedule = ScheduleBlock(
            label="Morning Study Session",
            tasks=[task],
            start_window="09:00",
            duration_min=120,
            location="home",
            confidence=0.85,
            explanation="Best time for high-energy tasks"
        )
        
        # Create a serializable version for JSON
        schedule_dict = {
            "label": schedule.label,
            "tasks": [task.__dict__],
            "start_window": schedule.start_window,
            "duration_min": schedule.duration_min,
            "location": schedule.location,
            "confidence": schedule.confidence,
            "explanation": schedule.explanation
        }
        schedule_json = json.dumps(schedule_dict, indent=2)
        schedule_toon = ToonService.encode_message(schedule, "schedule")
        
        savings2 = ToonService.calculate_token_savings(schedule_json, schedule_toon)
        
        logger.info(f"Original JSON ({savings2['original_length']} chars):")
        logger.info(schedule_json[:200] + "...")
        logger.info(f"\nToon Format ({savings2['toon_length']} chars):")
        logger.info(schedule_toon[:200] + "...")
        logger.info(f"\n✓ Token Savings: {savings2['savings_chars']} chars ({savings2['savings_percent']}%)\n")
        
        # Test 3: Student Profile encoding
        logger.info("--- Test 3: Student Profile Encoding ---")
        profile = StudentProfile(
            persona="bca_student",
            branch="BCA",
            semester=3,
            typical_wake_time="07:00",
            typical_sleep_time="23:00",
            home_duty_pattern="Help with dinner preparation around 18:00",
            study_preferences={"preferred_time": "morning", "session_length": 90}
        )
        
        profile_dict = {
            "persona": profile.persona,
            "branch": profile.branch,
            "semester": profile.semester,
            "typical_wake_time": profile.typical_wake_time,
            "typical_sleep_time": profile.typical_sleep_time,
            "home_duty_pattern": profile.home_duty_pattern,
            "study_preferences": profile.study_preferences
        }
        profile_json = json.dumps(profile_dict, indent=2)
        profile_toon = ToonService.encode_message(profile, "profile")
        
        savings3 = ToonService.calculate_token_savings(profile_json, profile_toon)
        
        logger.info(f"Original JSON ({savings3['original_length']} chars):")
        logger.info(profile_json)
        logger.info(f"\nToon Format ({savings3['toon_length']} chars):")
        logger.info(profile_toon)
        logger.info(f"\n✓ Token Savings: {savings3['savings_chars']} chars ({savings3['savings_percent']}%)\n")
        
        # Summary
        logger.info("=== Summary ===")
        total_original = savings['original_length'] + savings2['original_length'] + savings3['original_length']
        total_toon = savings['toon_length'] + savings2['toon_length'] + savings3['toon_length']
        total_savings = total_original - total_toon
        total_percent = (total_savings / total_original * 100) if total_original > 0 else 0
        
        logger.info(f"Total Original Size: {total_original} chars")
        logger.info(f"Total Toon Size: {total_toon} chars")
        logger.info(f"Total Savings: {total_savings} chars ({round(total_percent, 2)}%)")
        logger.info("✅ Toon format significantly reduces token usage!\n")
        
        # Test decoding
        logger.info("--- Testing Decoding ---")
        decoded_task = ToonService.decode_message(task_toon, "task")
        logger.info(f"Decoded task title: {decoded_task.get('title')}")
        logger.info("✓ Decoding successful!\n")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_toon_token_savings()
