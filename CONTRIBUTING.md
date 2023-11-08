# Contributing

## Production Environment

### Conda

Create or update the environment using

```bash
mamba create -f environment.yml
```

Export the environment configuration using

```bash
mamba env export -n magdalena > environment.yml
```

```bash
pip list --format=freeze > requirements.txt
```

## Development Environment

### Conda

Create or update the environment using

```bash
mamba create -f environment.dev.yml
```

Export the environment configuration using

```bash
mamba env export -n magdalena-dev > environment.dev.yml
```

```bash
pip list --format=freeze > requirements.dev.txt
```

## Continous Integration Test

We recommend to run the continous integration test in the Docker container.

Run

```bash
docker compose up
```

and, in another terminal, run

```bash
docker exec magdalena-magdalena-1 -- pytest .
```

## User Experience Test

We recommend to run the continous integration test in the Docker container.

Run

```bash
docker compose up
```

and open http://localhost:5000 with your web browser.
