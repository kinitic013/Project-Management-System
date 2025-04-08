class ActivityActions:
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    SOFT_DELETE = 'SOFT_DELETE'
    RESTORE = 'RESTORE'
    GET = 'GET'
    GET_ALL = 'GET_ALL'
    GET_FILTER = 'GET_FILTER'
    GET_CSV = 'GET_CSV'

    CHOICES = [
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (SOFT_DELETE, 'Soft Delete'),
        (RESTORE, 'Restore'),
        (GET, 'Get'),
        (GET_ALL, 'Get All'),
        (GET_FILTER, 'Get Filter'),
        (GET_CSV, 'Get CSV'),
    ]
class ModelActions:
    PROJECT = "PROJECT"
    TASK = "TASK"
    IMAGE = "IMAGE"
    USER = "USER"

    CHOICES = [
        (PROJECT, 'Project'),
        (TASK, 'Task'),
        (IMAGE, 'Image'),
        (USER, 'User'),
    ]
