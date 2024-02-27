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

The application provides a REST API which you can write your own endpoints to.
It is setup with the intention to be run localy on your computer.
So we do not implement any authentification for the moment.
It should however be possible to adapt the work and deploy it somewhere if that is what you want.

A default frontend for the application is available.
As the frontend as well as the API is served from the same host additional requirements need to be installed.
Use the following commands to install the requirements and verify that the svelte template works.
```bash
cd front
npm install
```

Verify if both the frontend and backend run.
To start the development servers use the script
```bash
./start_server.sh
```
or alternatively look the commands up in the script and run them manually in separate terminals for a better developer experience.

# Application Structure
The structure of the application is somewhat unconventional as we decided to have the frontend (in Svelte) and the backend (with FastAPI) in the same repository.
This was a concious decision for didactic purposes and to ensure everything was in one single place but it makes the build-process a bit more elaborate.
[This article](https://phillyharper.medium.com/svelte-fastapi-hello-world-2d545b901a34)
primary inspiration for the structure.

# How to Run
* Install as described above
* the `./start_server.sh` script assumes that your virtual environment is installed in `.venv` inside the root-folder change the script such that it fits how you installed it or start the server manually
* the current implementation has some limitations which will gradually be alliviated
    * files can be "uploaded" through the web-UI (only .pdfs for now) or stored directly under `./documents/`
    * before they can be queried the script/module `similarity_search.py` needs to be run on its own
    * the script currently deletes and completly rebuilds the databases in a naiive way depending on the number and size of documents this will take a long time
    * only after building the database it is possible to use the application as all queries only use the databases.

# Additional Sources
* [Paper: Sentence-BERT](https://arxiv.org/abs/1908.10084)
* [Youtube: Sentence-BERT explained](https://www.youtube.com/watch?v=FpUzooAD-a8)
* [Stanford NLP: Datasets](https://nlp.stanford.edu/projects/snli/)