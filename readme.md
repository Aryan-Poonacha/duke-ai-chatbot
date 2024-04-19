# 

[**Try the chatbot here!**](https://dukeaichat.streamlit.app/) - ask it any questions about the Duke AI Engineering program!

## Data

Data was taken from a compilation of URLs of the various Duke program websites. Scraping done with `scrape_data.py` (and some manual cleaning and webpage saving).

## Model

The base model used is the (as of April 19th, 2024) cutting-edge [Llamma-8B base model](https://huggingface.co/meta-llama/Meta-Llama-3-8B). It has undergone instruction fine-tuning to improve its instruction-following chatbot capability.

### Finetuning

#### Dataset

The dataset used for finetuning is [this](https://huggingface.co/datasets/alespalla/chatbot_instruction_prompts) instruction finetuning dataset that's a compilation of chatbot Q&A-style instruction data from multiple sources.

#### Process


### Retrieval-Augmented Generation (RAG)

The system uses Retrieval-Augmented Generation (RAG) to retrieve data from the vector database. 


## Pipeline

The architecture of the overall system consists of the following components:

1. Data ingestion pipeline - this consists of the `scrape_data` script to webscrape and save all the relevant data from the webpages we need, as well as the `vectara_upload` script to upload this data to the Vector database used for this project, Vectara. After the data is ingested by Vectara, 
2. Finetuned model hosted on HuggingFace with API call to it for inference.
3. Streamlit interface hosted on Streamlit community. Receives query -> gets RAG results from vectorized semantic search from Vectara -> queries HuggingFace finetuned model with custom prompt to get response -> displays results to user. Repeat in frontend chat interface loop.


## Evaluation

The evaulation of the fine-tuning 

Additionally, for an additional component of human evaluation, I made a brief feedback survey on Qualtrics to collect feedback from users after their interactions with the chatbot.

## Inference

Frontend interface is a [streamlit community application](https://dukeaichat.streamlit.app/) that interfaces with the relevant backend components to provide a smooth chat experience.

## References

Resources used for finding an instruction-tuned dataset:

1. https://analyticsindiamag.com/10-question-answering-datasets-to-build-robust-chatbot-systems/
2. https://huggingface.co/collections/davanstrien/top-10-instruction-tuning-datasets-650d91e11427d12e8542a21a