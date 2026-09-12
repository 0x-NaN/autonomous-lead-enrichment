import tiktoken
from config.settings import settings

encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def estimate_cost(input_tokens: int, output_tokens: int, model: str = "qwen2.5:7b") -> float:
    if "ollama" in model.lower() or model in ["qwen2.5:7b", "llama3", "mistral"]:
        return 0.0
    
    pricing = {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    }
    
    if model not in pricing:
        return 0.0
    
    input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
    return input_cost + output_cost