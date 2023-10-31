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
