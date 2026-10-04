import memory
import json
from transformers import AutoTokenizer

def trim_history_by_chars(history, max_chars):
    result = []
    chars = 0

    for item in history[::-1]:
        length = len(item["content"])

        if chars + length <= max_chars:
            result.append(item)
            chars += length
        else:
            break

    return result[::-1]
def build_context(history, long_memory, max_chars):

    context = []

    memory_text = "\n".join(long_memory)

    system_message = {
        "role":"system",
        "content":memory_text
    }

    context.append(system_message)

    remain = max_chars - len(memory_text)

    context.extend(
        trim_history_by_chars(history, remain)
    )

    return context
def count_context_length(context):
    total = 0

    for item in context:
        total += len(item["content"])

    return total