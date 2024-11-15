import sys
from crew import MarketingPostsCrew
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")

def validate_inputs(inputs):
    """
    Validate that the input project description is insurance-related 
    and customer domain is not empty.
    """
    if not inputs.get('customer_domain'):
        raise ValueError("Customer Domain is required.")
    if not inputs.get('project_description'):
        raise ValueError("Project Description is required.")
    
    required_keywords = ["insurance", "life", "health", "property", "coverage", "policy", "claims"]
    description_lower = inputs['project_description'].lower()
    
    if not any(keyword in description_lower for keyword in required_keywords):
        raise ValueError("The project description must be related to the insurance industry. Please provide a valid insurance-related project.")

def run():
    """
    Run the crew with the provided inputs and store the output.
    """
    inputs = {
        'customer_domain': input("Enter Customer Domain (e.g., https://www.jubileelife.com/): "),
        'project_description': input("Enter Project Description: ")
    }
    
    try:
        validate_inputs(inputs)  # Validate user inputs
        crew_instance = MarketingPostsCrew().crew()
        
        if not crew_instance:
            raise ValueError("Failed to initialize the Crew instance.")
        
        result = crew_instance.kickoff(inputs=inputs)
        
        # Print and return the result
        print("Crew Output:", result)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'customer_domain': input("Enter Customer Domain (e.g., https://www.jubileelife.com/): "),
        'project_description': input("Enter Project Description: ")
    }
    
    try:
        validate_inputs(inputs)  # Validate user inputs
        n_iterations = int(input("Enter number of training iterations (default: 10): ") or 10)
        
        crew_instance = MarketingPostsCrew().crew()
        result = crew_instance.train(n_iterations=n_iterations, inputs=inputs)
        
        # Print and return the training result
        print("Training Completed:", result)
        return result
    except ValueError as ve:
        print(f"Input Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Determine the mode (run or train) based on script arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        train()
    else:
        run()
