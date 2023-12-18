# Semantic-Document-Search
An simple interface for searching semantically similar content in a custom corpus of documents using SBERT

# Documentation and Design Ideas
[Documentation and Design Ideas](https://github.com/marcozeller/Semantic-Document-Search/tree/main/docs)

# Requirements
All the required python libraries can be installed from the `requirements.txt` file.
Optionally create a virtual environment for this project and activate it.
In case you use pip use
```bash
pip install -r requirements.txt
``` 
to install the python dependencies.

Make sure you have uvicorn installed on your system or in your environment.
```bash
pip install "uvicorn[standard]"
```
Checkout the
[fastapi documentation](https://fastapi.tiangolo.com/#installation)
for a step by step guide or if on your system other steps are required.

To start the server use the script
```bash
./start_server.sh
```
or alternatively look the commands up in the script and run them manually.

# Application Structure
The structure of the application is somewhat unconventional as we decided to have the frontend (in Svelte) and the backend (with FastAPI) in the same repository.
This was a concious decision for didactic purposes and to ensure everything was in one single place but it makes the build-process a bit more elaborate.
[This article](https://phillyharper.medium.com/svelte-fastapi-hello-world-2d545b901a34)
primary inspiration for the structure.

# Additional Sources
* [Paper: Sentence-BERT](https://arxiv.org/abs/1908.10084)
* [Youtube: Sentence-BERT explained](https://www.youtube.com/watch?v=FpUzooAD-a8)
* [Stanford NLP: Datasets](https://nlp.stanford.edu/projects/snli/)