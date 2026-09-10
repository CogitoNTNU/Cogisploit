"""
Maximally visible terminal chat for a local Qwen model.
Shows: tokenization, per-token generation, top-k alternative tokens,
timing, and running token count.
"""

import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_PATH = "./models/qwen2.5-1.5b"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float32)
model.eval()
print(
    f"Model loaded. Layers: {model.config.num_hidden_layers}, "
    f"Hidden size: {model.config.hidden_size}, "
    f"Vocab size: {model.config.vocab_size}\n"
)

conversation = []


def show_tokenization(text):
    ids = tokenizer.encode(text, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(ids)
    print(f"\n[TOKENIZATION] {len(tokens)} tokens:")
    for tid, tok in zip(ids, tokens):
        print(f"    id={tid:<8} token={tok!r}")


def generate_verbose(input_ids, max_new_tokens=80, top_k=5):
    generated = input_ids
    print("\n[GENERATION] token-by-token:\n")

    for step in range(max_new_tokens):
        start = time.time()

        with torch.no_grad():
            outputs = model(generated)
            logits = outputs.logits[:, -1, :]

        probs = torch.softmax(logits, dim=-1)
        top_probs, top_ids = torch.topk(probs, top_k)

        chosen_id = top_ids[0][0].unsqueeze(0).unsqueeze(0)
        chosen_token = tokenizer.decode(chosen_id[0])

        elapsed = time.time() - start

        # Show the top-k candidates the model considered at this step
        alt_str = ", ".join(
            f"{tokenizer.decode([tid.item()])!r}:{p.item():.2f}"
            for tid, p in zip(top_ids[0], top_probs[0])
        )
        print(
            f"  step {step:>3} | chosen={chosen_token!r:<15} "
            f"| top-{top_k}=[{alt_str}] | {elapsed * 1000:.0f}ms"
        )

        generated = torch.cat([generated, chosen_id], dim=1)

        if chosen_id.item() == tokenizer.eos_token_id:
            print("  [EOS reached]")
            break

    return generated


print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        break
    if not user_input:
        continue

    show_tokenization(user_input)
    conversation.append({"role": "user", "content": user_input})

    text = tokenizer.apply_chat_template(
        conversation, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt")

    print(f"\n[INPUT] {inputs['input_ids'].shape[1]} total tokens fed to model")

    full_output = generate_verbose(inputs["input_ids"], max_new_tokens=100)

    response_ids = full_output[0][inputs["input_ids"].shape[1] :]
    response = tokenizer.decode(response_ids, skip_special_tokens=True)

    print(f"\nAssistant: {response}\n")
    print("-" * 70)

    conversation.append({"role": "assistant", "content": response})
