import yaml


def load_config(filename='config.yaml'):
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config
