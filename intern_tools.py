import smtplib, ssl, os, imaplib, email
from email.message import EmailMessage
from email.header import decode_header
from smolagents import tool
import edgehdf5_memory 

# Initialize Memory Backend
intern_memory = edgehdf5_memory.HDF5Memory(
    path="/sandbox/agent_memory.h5", agent_id="intern-alpha", embedding_dim=384, float16=True, compression=True
)

@tool
def send_intern_email(target_address: str, subject: str, body: str) -> str:
    """Sends an email from the intern's account to a specified address."""
    sender_email, sender_password = "intern.identity@gmail.com", os.getenv("INTERN_APP_PASSWORD") 
    em = EmailMessage()
    em['From'], em['To'], em['Subject'] = sender_email, target_address, subject
    em.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(em)
        return f"Success: Email sent to {target_address}"
    except Exception as e:
        return f"Error sending email: {e}"

@tool
def check_intern_inbox(filter_sender: str = None) -> str:
    """Checks the intern's Gmail inbox for unread messages."""
    # ... (IMAP logic defined in previous iterations) ...
    return "Inbox data parsed successfully."

@tool
def save_intern_memory(content: str, entity_tag: str = "general") -> str:
    """Saves an important fact, user preference, or system state to long-term memory."""
    try:
        intern_memory.save(chunk=content, session_id=os.getenv("CURRENT_SESSION_ID", "default"), tags=[entity_tag])
        return f"Success: Committed to long-term memory ({entity_tag})."
    except Exception as e:
        return f"Memory storage failed: {e}"

@tool
def recall_intern_memory(query: str, require_exact_match: bool = False) -> str:
    """Searches the agent's long-term memory (.h5 file) for past facts or instructions."""
    try:
        semantic_weight, keyword_weight = (0.3, 0.7) if require_exact_match else (0.8, 0.2)
        results = intern_memory.hybrid_search(query=query, semantic_weight=semantic_weight, keyword_weight=keyword_weight, top_k=3)
        if not results: return "No relevant memories found."
        return f"Recalled Memories:\n" + "\n".join([f"- {res.chunk}" for res in results])
    except Exception as e:
        return f"Memory retrieval failed: {e}"

@tool
def request_human_assistance(error_summary: str, failing_code_snippet: str) -> str:
    """Halts execution and flags humans. MUST be used after two consecutive task failures."""
    alert_payload = f"INTERN HALTED.\nReason: {error_summary}\nCode:\n{failing_code_snippet}"
    send_intern_email("admin@yourdomain.com", "Intern Error: Human Intervention Required", alert_payload)
    return "Assistance requested. Entering standby mode."
