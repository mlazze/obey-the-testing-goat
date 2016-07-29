from invoke import task
from threading import Thread


@task
def run(ctx, firefox=False):
    browser = "chrome"
    if firefox:
        browser = "firefox"

    ctx.run("docker run -d "
            "--net=host --name selenium "
            "selenium/standalone-{browser}-debug"
            .format(browser=browser))


@task
def runserver(ctx):
    def server():
        ctx.run("python superlists/manage.py runserver")

    threads = map(lambda x: Thread(target=x), (server,))
    # Kick off
    [x.start() for x in threads]
    # Wait for completion - maybe pending KeyboardInterrupt or similar
    [x.join() for x in threads]


@task
def migrate(ctx, makeMigrations=False):
    if makeMigrations:
        makemigrations(ctx)

    ctx.run("python superlists/manage.py migrate")


@task
def makemigrations(ctx):
    ctx.run("python superlists/manage.py makemigrations")


@task
def stop(ctx):
    ctx.run("docker kill selenium")
    ctx.run("docker rm selenium")
