# Contributing

## Development Environment

### Conda

Export the environment configuration using

```bash
micromamba env export -n magdalena > environment.yml
```

```bash
micromamba env export -n magdalena > environment.dev.yml
```

```bash
pip list --format=freeze > requirements.txt
```

```bash
pip list --format=freeze > requirements.dev.txt
```
