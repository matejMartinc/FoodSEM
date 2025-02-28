from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

if __name__ == '__main__':
    base_model = "meta-llama/Meta-Llama-3-8B-Instruct"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=bnb_config,
        device_map={"": 0},
        attn_implementation="eager"
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.pad_token = '<|pad|>'
    tokenizer.pad_token_id = 128255

    #Load LORA weights
    model.load_adapter("Anonymous-pre-publication/FoodSEM-LLM")
    model.config.use_cache = True
    model.eval()

    system_prompt = ""
    user_prompt = "Calculate the nutrient values per 100 grams in a recipe with these ingredients: 10 ounce candies, marshmallows, 1/4 cup butter, without salt, 6 cup cocoa, dry powder, unsweetened"

    messages = [
        {
            "role": "user",
            "content": f"{system_prompt} {user_prompt}".strip()
        }
    ]

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    #Here we have a batch of one
    tokenizer_input = [prompt]

    inputs = tokenizer(tokenizer_input, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(device)
    generated_ids = model.generate(**inputs, max_new_tokens=1024, do_sample=True)
    answers = tokenizer.batch_decode(generated_ids[:, inputs['input_ids'].shape[1]:])
    answers = [x.split('<|end_of_text|>')[0].split('<|im_end|>')[0].split('<|eot_id|>')[0]
                                .replace("<|start_header_id|>assistant", '').replace("<|end_header_id|>", '')
                                         .replace("<|start_header_id|>", '').split().strip() for x in answers]
    print(answers)