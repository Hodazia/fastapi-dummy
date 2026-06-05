'''
this is a fake db for the moment,
I will upgrade to using the postgesql + sqlaclchemy in the future

----------
And i will run it on the docker with a persistent volume option,
so that even if we stop the EC2 instance and i re run the postgres image the data shall 
remain persistent, means it shall have data stored from previous sessions also,
but will that data be stored in the drive, is a question for now?
'''

users_db = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 25
    }
]