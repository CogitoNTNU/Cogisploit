"""
Simple terminal chat interface for a local Qwen model.
Type your message and press enter. Type 'exit' or 'quit' to stop.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "./models/qwen2.5-3b"

print("Loading model... this may take a moment.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
print("Model loaded. Type 'exit' to quit.\n")

# Keep conversation history so the model has context across turns
conversation = []

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    if not user_input:
        continue

    conversation.append({"role": "user", "content": user_input})

    # Build the prompt using the model's chat template
    text = tokenizer.apply_chat_template(
        conversation, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
    )

    # Decode only the newly generated tokens (skip the input prompt part)
    response_ids = outputs[0][inputs["input_ids"].shape[1] :]
    response = tokenizer.decode(response_ids, skip_special_tokens=True)

    print(f"\nAssistant: {response}\n")

    conversation.append({"role": "assistant", "content": response})
