import os
import docker
from smolagents import CodeAgent, LiteLLMModel
from intern_tools import send_intern_email, check_intern_inbox, save_intern_memory, recall_intern_memory, request_human_assistance

# 1. Initialize the Local Docker Client (for ephemeral execution)
docker_client = docker.from_env()

def secure_docker_executor(code: str) -> str:
    """Intercepts generated Python code and runs it in the burner container."""
    try:
        container = docker_client.containers.run(
            "intern-burner-env:latest", command=["python3", "-c", code],
            remove=True, network_mode="none", mem_limit="256m", cpu_quota=50000, stdout=True, stderr=True
        )
        return container.decode('utf-8')
    except docker.errors.ContainerError as e:
        return f"Execution Error: {e.stderr.decode('utf-8')}"
    except Exception as e:
        return f"System Error: {str(e)}"

# 2. API Routing to LiteLLM Proxy (Port 4000), NOT directly to Ollama
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:7b", 
    api_base="http://localhost:4000", 
    num_ctx=8192
)

# 3. System Prompt & Guardrails
intern_system_prompt = """
You are an autonomous IT assistant operating inside a strictly isolated KVM environment. 
You write and execute Python code to solve tasks. 

CRITICAL PROTOCOLS:
1. TEST-DRIVEN ERROR HANDLING: Treat execution errors as feedback. Read the Traceback from standard error, correct the logic, and resubmit.
2. MISSING CONTEXT: If a script fails due to missing variables or paths, execute `recall_intern_memory` before attempting a rewrite.
3. THREE-STRIKE ESCALATION: If you fail a task twice consecutively, you MUST stop and execute `request_human_assistance()`.
"""

# 4. Instantiate the Agent
agent = CodeAgent(
    tools=[send_intern_email, check_intern_inbox, save_intern_memory, recall_intern_memory, request_human_assistance],
    model=model,
    system_prompt=intern_system_prompt,
    max_iterations=4, 
    add_base_tools=False,
    additional_kwargs={"executor": secure_docker_executor} # Forces code into the burner container
)

if __name__ == "__main__":
    print("Project Intern: Secure Sandbox Online.")
    # test_instruction = "..."
    # agent.run(test_instruction)
