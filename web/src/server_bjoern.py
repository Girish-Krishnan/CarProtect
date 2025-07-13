import bjoern
from app import create_app

if __name__ == '__main__':
    bjoern.run(create_app(), '0.0.0.0', 6000)
