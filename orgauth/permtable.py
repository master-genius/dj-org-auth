
PERM_DEFAULT_ROLE = [
    'orgadmin',
    'teacher',
]

PERM_TABLE = {
    'orgadmin' : '*',
    'teacher' : [
        'login',
        'logout',
        'orgbind',
        'addcourse',
    ]
}
