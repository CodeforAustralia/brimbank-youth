from background_task import background

@background(schedule=5)
def print_something():
    print('Again this is a background task')