# WorkerNode
---
The worker node repository defines how workers are interacting with the  schedualer component. The communication is supported by Google pubsub, a Google API allows message publication and subscription.
## Features
- Constant listerning to job scedualer
- Parallel jobs running in threads
- Sufficiently fills up allocated resources with function jobs
## Dependency
- Docker
- Google pubsub

## Handling Secrete
- By using Google API, dFunc has to expose respricted Google API keys to worker nodes. The API keys are shared among all workers and only allows subscrition. All Google API keys will be save inside .config directory.
## Usage
Running Worker node component only reuiqres workers to run the main python function with valid json secretes.
## Furture Work
- Package worker node into a docker image. 
- Connect with a GUI to allow registered user start up with one click.