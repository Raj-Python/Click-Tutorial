import click
import os
import shutil

from .tutorial import get_lessons, list_lesson_ids, run_lesson, save_lesson_statuses

STATUS_FILE = 'status.json'

@click.group(name='tutorial')
@click.pass_context
def cli(ctx):
    """
    This runs the tutorial
    """
    ctx.obj = {'status_filename': os.path.join(
            click.get_app_dir('Click Tutorial'), STATUS_FILE)}
    ctx.obj['lessons'] = get_lessons(ctx.obj['status_filename'])


@cli.command()
@click.argument('lesson_id', type=click.Choice(list_lesson_ids()))
@click.pass_context
def lesson(ctx, lesson_id):
    """
    Run tests to check given LESSON_ID.
    """
    lessons = ctx.obj['lessons']
    lesson = lessons[lesson_id]
    if lesson['status'] == 'complete':
        click.confirm(
                "This less was already completed. Do you want to re-run?", abort=True)

    click.echo("Running tests for lesson {0} {1}...".format(lesson_id, lesson['title']))

    result = run_lesson(lesson['test_file'])
    if result:
        lessons[lesson_id]['status'] = 'complete'
        click.secho("Good job!", fg='green')
    else:
        lessons[lesson_id]['status'] = 'in-progress'
        click.secho("\nHint: {0}".format(lesson.get('hint')), fg='blue')
        click.secho("URL: {0}".format(lesson.get('url', 'n/a')), fg='blue')

    save_lesson_statuses(ctx.obj['status_filename'], lessons)

    if not result:
        ctx.exit(2)

@cli.command(name='lesson-ids')
@click.pass_context
def lesson_ids(ctx):
    """
    Output a list of all LESSON_IDs.
    """
    click.echo(','.join(sorted(ctx.obj['lessons'].keys())))

@cli.command()
@click.option('--yes', is_flag=True, help="Assume Y to confirmation prompts.")
@click.pass_context
def reset(ctx, yes):
    """
    Reset the status for all lessons (start-over)
    """

    if not yes:
        click.confirm("Are you sure you want to reset the status of all lessons (start over?)", abort=True)
    lessons = {}
    save_lesson_statuses(ctx.obj['status_filename'], lessons)
    click.echo("Tutorial reset.")


@cli.command()
@click.argument('lesson_id', type=click.Choice(list_lesson_ids()))
@click.pass_context
def solve(ctx, lesson_id):
    """
    Copy solution for LESSON_ID into place for viewing / testing.
    """
    lesson = ctx.obj['lessons'][lesson_id]
    click.echo("Copying solution for lesson {0} {1}".format(lesson_id, lesson['title']))
    source_file = os.path.join('solutions/', lesson['test_file'])
    dest_file = 'click_tutorial/cli.py'
    try:
        click.echo("copy: {0} -> {1}".format(source_file, dest_file))
        shutil.copy(source_file, dest_file)
    except IOError as e:
        click.secho(str(e), fg='red')
        ctx.exit(1)

    click.echo("You may now view the solution file at click_tutorial/cli.py\n" \
               "or run the tests for the lesson with:\n\n" \
               "tutorial lesson {0}".format(lesson_id))

@cli.command()
@click.pass_context
def status(ctx):
    """
    Show the status of the tutorial lessons.
    """
    click.secho("### Lesson Name                         status\n"
            "--------------------------------------------------", bold=True, color='white')
    for lesson_number, lesson_details in sorted(ctx.obj['lessons'].items()):
        status = lesson_details.get('status')
        if status == 'complete':
            color = 'green'
        elif status == 'in-progress':
            color = 'yellow'
        else:
            color = 'red'

        click.secho("{0} {1:35} {2}".format(
            lesson_number, lesson_details.get('title'), status), fg=color)


if __name__ == '__main__':
    cli()
