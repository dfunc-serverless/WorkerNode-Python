# WorkerNode
---
The worker node repository defines how workers are interacting with the scheduler component. The communication is supported by Google pubsub, a Google API allows message publication and subscription.
## Features
- Constantly listening to the job scheduler
- Parallel jobs running in threads
- Sufficiently fills up allocated resources with function jobs
## Dependency
- Docker
- Google pubsub

## Handling Secrete
- By using Google API, dFunc has to expose restricted Google API keys to worker nodes. The API keys are shared among all workers and only allows subscription. All Google API keys will be saved inside the .config directory.
## Usage
Running Worker node component only requires workers to run the main python function with valid JSON secrets.
## Further Work
- Package worker node into a docker image. 
- Connect with a GUI to allow registered user startup with one click.
