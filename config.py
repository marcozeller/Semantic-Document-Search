from os import path, getcwd


DOCUMENTS_DIRECTORY = path.join(getcwd(), 'documents')
DATABASES_DIRECTORY = path.join(getcwd(), 'databases')

model_config = {
    'model': 'all-MiniLM-L6-v2',
    'dimension': 384,
}