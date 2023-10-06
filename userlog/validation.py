import json

def signValidate(form_data):
    fname = form_data['first_name']
    lname = form_data['last_name']
    username = form_data['username']
    email = form_data['email']
    password1 = form_data['password1']
    password2 = form_data['password2']
    error = {
        'first_name': '',
        'last_name': '',
        'username': '',
        'email': '',
        'password1': '',
        'password2': ''
    }
    # Blank validation
    if fname == '':
        error['first_name'] = 'First Name is required'
    elif lname == '':
        error['last_name'] = 'Last Name is required'
    elif username == '':
        error['username'] = 'Username is required'
    elif email == '':
        error['email'] = 'E-mail is required'
    elif password1 == '':
        error['password1'] = 'Password is required'
    elif password2 == '':
        error['password2'] = 'Confirm Password is required'
    else:
        return None
    # if there is error it returns error dictionary
    return error

# here error_msg_dict is error message we get from Form.error, error_msg is message we want to users, error_keys are key present in error_msg dictionary
def emailPasswordValidate(error_json_msg):
    error_msg_dict = json.loads(error_json_msg)
    error_msg = {'username': '', 'email':'','password2':''}
    error_msg = {
        'username': '',
        'email': '',
        'password2': '',
    }

    error_keys = ['username', 'email', 'password2']

    for key in error_keys:
        try:
            if error_msg_dict[key]:
                error_msg[key] = error_msg_dict[key][0]['message']
        except KeyError:
            pass
    return error_msg