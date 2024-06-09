# Pub/Sub Push Subscription Project

This project demonstrates how to set up a Google Cloud Pub/Sub system with a push subscription using Terraform, and a FastAPI service that handles the push messages. The service also includes endpoints for saving and retrieving sensor data.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Terraform](https://www.terraform.io/downloads.html)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Python 3.12+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- make
- [Docker](https://docs.docker.com/engine/install/)

You also need a Google Cloud account and a project set up.

## Setup

**1. Clone the repository:**

```sh
git clone git@github.com:Georg1703/pubsub_project.git
cd pubsub_project
```

**2. Start the project:**

```sh
make start
```

At this moment service is up and running, visit **http://localhost:8000/docs** to check existing endpoints.

**3. Run the tests:**

```sh
make test
```

**4. To provision GCP environment run:**

```
terraform init

terraform plan

terraform apply
```
