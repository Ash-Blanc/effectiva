"""Test script to demonstrate DSPy optimizer integration."""
import dspy
from agents.study_agent import create_study_agent
from config.settings import GOOGLE_API_KEY
from logger import logger
from database import init_db, SessionLocal
from optimizer_service import OptimizerService

def simple_metric(example, pred, trace=None):
    """Simple evaluation metric."""
    response = pred.response if hasattr(pred, 'response') else str(pred)
    if not response:
        return 0
    
    score = 0
    if len(response) > 20:
        score += 0.5
    
    if hasattr(example, 'user_message'):
        user_words = set(example.user_message.lower().split())
        response_words = set(response.lower().split())
        if len(user_words.intersection(response_words)) > 0:
            score += 0.5
    
    return score

def main():
    """Test DSPy optimizer integration."""
    logger.info("=== Testing DSPy Optimizer Integration ===")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Configure DSPy
        logger.info("Configuring DSPy...")
        lm = dspy.LM(model="gemini/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
        dspy.configure(lm=lm)
        
        # Create study agent
        logger.info("Creating study agent...")
        agent = create_study_agent()
        
        # Create optimizer configuration in database
        logger.info("Creating optimizer config...")
        optimizer_config = OptimizerService.create_optimizer(
            db=db,
            agent_name=agent.name,
            optimizer_type="GEPA",
            config={"max_iterations": 5}
        )
        logger.info(f"Created optimizer: {optimizer_config.name}")
        
        # Create training dataset
        trainset = [
            dspy.Example(
                context="study",
                user_message="I have a math exam tomorrow.",
                response="Let's create a study plan for your math exam."
            ).with_inputs("context", "user_message"),
        ]
        
        valset = [
            dspy.Example(
                context="study",
                user_message="I can't focus.",
                response="Try the Pomodoro technique."
            ).with_inputs("context", "user_message"),
        ]
        
        # Run optimization
        logger.info("Running optimization...")
        optimized = OptimizerService.run_optimization(
            agent=agent,
            trainset=trainset,
            valset=valset,
            metric=simple_metric,
            optimizer_type="GEPA"
        )
        
        logger.info("✅ Optimization complete!")
        logger.info(f"Optimized instructions preview: {str(optimized)[:200]}...")
        
        # Get all optimizers for this agent
        optimizers = OptimizerService.get_optimizers_for_agent(db, agent.name)
        logger.info(f"Total optimizers for {agent.name}: {len(optimizers)}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
