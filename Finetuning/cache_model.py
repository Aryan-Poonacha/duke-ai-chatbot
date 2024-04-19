import transformers
import torch
import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('HF_TOKEN')

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
  "text-generation",
  model="meta-llama/Meta-Llama-3-8B-Instruct",
  model_kwargs={"torch_dtype": torch.bfloat16},
  device="cuda",
  token=token
)