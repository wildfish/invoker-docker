from invoke import task, run
import yaml


def docker_compose_run(ctx, cmd):
    docker_compose_file = ctx.get('docker_compose_file', 'docker-compose.yml')
    docker_cmd = ctx.get('docker_compose_cmd', 'docker-compose')

    run('{docker_cmd} {cmd}'.format(
        docker_cmd=docker_cmd,
        file_string='-f {}'.format(docker_compose_file) if docker_compose_file else '',
        cmd=cmd,
    ))


def docker_run(ctx, cmd):
    docker_cmd = ctx.get('docker_cmd', 'docker')

    run('{docker_cmd} {cmd}'.format(
        docker_cmd=docker_cmd,
        cmd=cmd,
    ))


def get_service_images(ctx, services):
    docker_compose_file = ctx.get('docker_compose_file', 'docker-compose.yml')

    with open(docker_compose_file) as f:
        docker_cfg = yaml.load(f)

        for svc in services:
            yield (svc, docker_cfg['services'][svc]['image'])


@task(help={
    'label': 'The label to use for the image',
})
def build(ctx, label=None):
    """
    Builds the docker image
    """
    managed_services = ctx['docker_managed_services']

    docker_compose_run(ctx, 'build {managed_services}'.format(
        managed_services=' '.join(managed_services),
    ))

    if label:
        for svc, image in get_service_images(ctx, managed_services):
            docker_run(ctx, 'tag {image} {image_name}:{label}'.format(
                image=image,
                image_name=image.split(':')[0],
                label=label,
            ))


@task(help={
    'build': 'Flag whether build the image before publishing',
    'label': 'The label to use for the image',
})
def push(ctx, _build=True, label=None):
    """
    Publishes the docker image to the registry
    """
    if _build:
        build(ctx, label=label)

    managed_services = ctx.get['docker_managed_services']

    if label:
        for svc, image in get_service_images(ctx, managed_services):
            docker_run(ctx, 'push {image_name}:{label}'.format(
                image_name=image.split(':')[0],
                label=label,
            ))
    else:
        docker_compose_run(ctx, 'push {}'.format(' '.join(managed_services)))


@task(help={
    'build': 'Flag whether build the image before publishing',
})
def test(ctx, _build=True):
    test_services = ctx.get('docker_compose_test_services', {'test': []})

    if _build:
        build(ctx)

    for svc, cmds in test_services.items():
        if cmds and len(cmds) > 0:
            for cmd in cmds:
                docker_compose_run(ctx, 'run --rm {} {}'.format(
                    svc,
                    cmd if cmd else '',
                ))
        else:
            docker_compose_run(ctx, 'run --rm {}'.format(svc))

