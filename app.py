from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from elasticsearch import Elasticsearch, exceptions as es_exceptions

# Function to load the model and tokenizer
def load_model(model_path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        return None, None

# Function to generate text
def generate_text(input_text, tokenizer, model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForSeq2SeqLM.from_pretrained(model)
    
    # Encoding the input text
    encoded_input = tokenizer.encode_plus(input_text, return_tensors='pt', max_length=512, truncation=True)
    
    # Generating a sequence of token IDs
    output_sequences = model.generate(input_ids=encoded_input['input_ids'], max_length=512, num_return_sequences=1)
    
    # Decoding the generated sequence to text
    paraphrase = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
    
    return paraphrase

# Initialize Elasticsearch
es = None
try:
    es = Elasticsearch(["http://elasticsearch:9200"])
    # Test connection
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed!")
except Exception as e:
    print(f"Failed to connect to Elasticsearch: {e}")
# Example usage
if __name__ == '__main__':
    # Path to your local model
    model_path = "/model"  # Use the Docker internal path as defined in docker-compose.yml
    tokenizer, model = load_model(model_path)

    if tokenizer is not None and model is not None:
        # Input text to be paraphrased
        input_text = "What is the purpose of life?"
        paraphrased_text = generate_text(input_text, tokenizer, model)  # Pass tokenizer and model here

        if paraphrased_text:
            # Index the paraphrased text into Elasticsearch
            doc = {'text': input_text, 'paraphrased_text': paraphrased_text, 'timestamp': '2023-04-25'}
            try:
                res = es.index(index="qa-index", body=doc)
                print(f"Indexed document: {res['result']}")
            except es_exceptions.ElasticsearchException as e:
                print(f"Failed to index document: {e}")
    else:
        print("Model loading failed, skipping text generation and indexing.")
