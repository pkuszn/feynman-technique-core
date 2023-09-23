import yaml
import pathlib
from copy import deepcopy

def load_config(mode="DEVELOPMENT"):
    path = pathlib.Path(__file__).parent
    try:
        match mode:
            case "PRODUCTION":
                load = None
                with open(f"{path}/config/prod.yaml") as stream:
                    try: 
                        load = yaml.safe_load(stream)
                    except yaml.YAMLError as exc:
                        print(exc) 
                return load
            case "DEVELOPMENT":
                load = None
                with open(f"{path}/config/dev.yaml") as stream:
                    try: 
                        load = yaml.safe_load(stream)
                    except yaml.YAMLError as exc:
                        print(exc)
                return load
    except ImportError:
        load = None
        with open(f"{path}/config/dev.yaml") as stream:
            try: 
                load = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return load

def mask(load, parents, names):
    for parent in parents:
        for k, v in load[parent].items():
            if len(names) > 1:
                for name in names:
                    if k == name:
                        load[parent][k] = '************'  
            else:
                if k == names:
                    load[parent][k] = '************'
    return deepcopy(load)
    