from invoke import Collection

from .docker import build, push

ns = Collection(
    'docker',
    build,
    push,
)
