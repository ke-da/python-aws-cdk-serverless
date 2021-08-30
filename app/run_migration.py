from alembic.config import Config
from alembic import command


def handler(*_args, **_kwargs):
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == '__main__':
    handler()
