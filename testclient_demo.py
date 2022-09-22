from app import app

USER_ID = 2
test_client = app.test_client()
# response = test_client.get('/users')


# user_data = {
#     'username': 'test-user',
#     'password': 'test-user'
# }

# users_data = [
#     {'username': 'user1', 'password': '12345'},
#     {'username': 'user2', 'password': '12345'},
#     {'username': 'user3', 'password': '12345'}
# ]
#
# for user_data in users_data:
#     response = test_client.post('/users',
#                                 json=user_data,
#                                 content_type='application/json')
#
# response = test_client.post('/users',
#                        json=user_data,
#                        content_type='application/json')

response = test_client.get(f'/users/{USER_ID}')

print('json = ', response.json)
print('code = ', response.status_code)