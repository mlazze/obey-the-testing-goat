from invoke import task
from threading import Thread


@task
def runseleniumindocker(ctx, firefox=False):
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
        ctx.run("python source/manage.py runserver")

    threads = map(lambda x: Thread(target=x), (server,))
    # Kick off
    [x.start() for x in threads]
    # Wait for completion - maybe pending KeyboardInterrupt or similar
    [x.join() for x in threads]


@task
def migrate(ctx, makeMigrations=False):
    if makeMigrations:
        makemigrations(ctx)

    ctx.run("python source/manage.py migrate")


@task
def makemigrations(ctx):
    ctx.run("python source/manage.py makemigrations")


@task
def stopseleniumindocker(ctx):
    ctx.run("docker kill selenium &", warn=True)
    ctx.run("docker rm selenium", warn=True)

@task
def collectstatic(ctx):
    ctx.run("python source/manage.py collectstatic")

@task
def rungunicorn(ctx):
    ctx.run("cd source && ../virtualenv/bin/gunicorn --bind unix:/tmp/superlists-staging.skij.mooo.com.socket superlists.wsgi:application")
