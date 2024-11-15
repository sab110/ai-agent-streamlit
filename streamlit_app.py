# main.py

import streamlit as st
from marketing_agent.src.marketing_agent.crew import MarketingPostsCrew
from dotenv import load_dotenv
import os
import re


# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="Marketing Posts Crew", layout="centered")

# Validate inputs
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

# Clean raw output
def clean_output(raw_output):
    """
    Cleans the raw output by removing special characters.
    """
    return re.sub(r'[^\w\s.,:]', '', raw_output)

# Main function for Streamlit app
def main():
    st.title("Marketing Strategy Agent")
    st.write("Enter project details to generate marketing strategy content for insurance-related projects.")

    with st.form("input_form"):
        customer_domain = st.text_input("Customer Domain", help="E.g., https://www.jubileelife.com/")
        project_description = st.text_area("Project Description", help="Describe the project in detail.")
        verbose = st.checkbox("Verbose Mode", value=False)

        submitted = st.form_submit_button("Run Crew")

        if submitted:
            inputs = {
                "customer_domain": customer_domain,
                "project_description": project_description
            }

            try:
                # Validate inputs
                validate_inputs(inputs)
                
                # Display spinner while processing
                with st.spinner("Generating output..."):
                    # Initialize crew instance
                    crew_instance = MarketingPostsCrew().crew(verbose=verbose)
                    raw_result = crew_instance.kickoff(inputs=inputs)

                    # Extract and clean output from copy_creation_task
                    if hasattr(raw_result, "tasks_output"):
                        for task in raw_result.tasks_output:
                            if task.name == "copy_creation_task":
                                # raw_output = clean_output(task.raw)
                                st.success("Agent Output")
                                # Display the output as markdown to prevent scrolling
                                st.markdown(f"### Generated Copy\n\n{task.raw}")
                                break
                        else:
                            st.warning("No output found for 'copy_creation_task'.")
                    else:
                        st.warning("No tasks output found.")
            except ValueError as ve:
                st.error(f"Input Error: {ve}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
