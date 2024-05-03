import os
from elasticsearch import Elasticsearch, exceptions as es_exceptions

def read_documents(directory_path):
    """Generator to read documents from a specified directory."""
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                yield filename, file.read()

def connect_elasticsearch():
    """Function to connect to Elasticsearch and return the connection."""
    es = Elasticsearch(["http://elasticsearch:9200"])
    try:
        if not es.ping():
            raise ValueError("Connection to Elasticsearch failed!")
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")
        exit()
    return es

def index_documents(es, directory_path):
    """Function to index documents from a specified directory."""
    try:
        for filename, content in read_documents(directory_path):
            doc = {
                'filename': filename,
                'content': content,
                'timestamp': '2023-04-25',
            }
            res = es.index(index="documents-index", document=doc)
            print(f"Document Indexed from {filename}: {res['result']}")
    except es_exceptions.ElasticsearchException as e:
        print(f"Error indexing document: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """Main function to handle Elasticsearch connection and document indexing."""
    es = connect_elasticsearch()
    directory_path = 'C:/Users/yonzb/OneDrive/Documents/Ai_Projects/Partner_Local_Ai/Docker/docs'
    index_documents(es, directory_path)

if __name__ == "__main__":
    main()
