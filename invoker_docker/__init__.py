from invoke import Collection

from .docker import build, push, test

ns = Collection(
    'docker',
    build,
    push,
    test,
)
