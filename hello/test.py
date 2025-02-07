import requests

# path = 'http://172.168.1.221:8000/'
path = 'http://172.168.1.221:8000/users/'

# headers = {
#     'Authorization': 'Bearer JWT yeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5MDg2NTU2LCJpYXQiOjE3Mzg2NTMzODcsImp0aSI6IjUwYTM0NjFhNGIwYTRkNWFhMzgxNTAyNzVlODQ3NDViIiwidXNlcl9pZCI6MX0.cS59tFTphxx_BtuQX8qAnmD4pgWjcoLP7Sg_daGOfm0',  # If using token authentication
# }

r = requests.post(path)

Please remove this file

print(r.json())
