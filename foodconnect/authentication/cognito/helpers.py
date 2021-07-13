from authentication.cognito import constants, actions

BAD_DATA_EXCEPTION = "The required parameters were not passed through in the data dictionary"


def initiate_auth(data, param_mapping=None):
    if ("username" in data and "password" in data) or ("username" in param_mapping and "password" in param_mapping):
        auth_flow = constants.USER_PASSWORD_FLOW
        username = parse_parameter(data, param_mapping, "username")
        password = parse_parameter(data, param_mapping, "password")

        return actions.initiate_auth(username, auth_flow, password)

    else:
        raise ValueError("Unsupported auth flow")


def sign_out(data, param_mapping=None):
    if "access_token" in data:
        access_token = parse_parameter(data, param_mapping, "access_token")
        return actions.sign_out(access_token)
    else:
        raise ValueError("Access token not found")


def respond_to_auth_challenge(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
        challenge_name = parse_parameter(data, param_mapping, 'challenge_name')
        responses = parse_parameter(data, param_mapping, 'responses')
        session = parse_parameter(data, param_mapping, 'session')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.respond_to_auth_challenge(username=username, challenge_name=challenge_name,
                                             responses=responses, session=session)


def sign_up(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
        password = parse_parameter(data, param_mapping, 'password')
        user_attributes= parse_parameter(data, param_mapping, 'user_attributes')
        
    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.sign_up(username, password, user_attributes)


def confirm_sign_up(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
        confirmation_code = parse_parameter(data, param_mapping, 'password')
        force_alias_creation = parse_parameter(data, param_mapping, 'force_alias_creation')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.confirm_sign_up(username, confirmation_code, force_alias_creation)


def forgot_password(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'email')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.forgot_password(username)


def confirm_forgot_password(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'email')
        new_password = parse_parameter(data, param_mapping, 'new_password')
        code = parse_parameter(data, param_mapping, 'code')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.confirm_forgot_password(username, code, new_password)


def admin_get_user(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.admin_get_user(username)


def admin_update_user_attributes(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
        user_attributes = parse_parameter(data, param_mapping, 'user_attributes')
    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.admin_update_user_attributes(username, user_attributes)


def admin_disable_user(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.admin_disable_user(username)


def admin_delete_user(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.admin_delete_user(username)

def admin_create_user(data, param_mapping=None):
    try:
        username = parse_parameter(data, param_mapping, 'username')
        user_attributes = parse_parameter(data, param_mapping, 'user_attributes')
        temporary_password = parse_parameter(data, param_mapping, 'temporary_password')

        if "suppress" in data or "suppress" in param_mapping:
            supress = parse_parameter(data, param_mapping, 'suppress')

    except Exception as ex:
        raise ValueError(BAD_DATA_EXCEPTION)

    return actions.admin_create_user(username, user_attributes, temporary_password)


def parse_parameter(data, param_mapping, param=None):
    if param_mapping is not None:
        if param in param_mapping:
            return data[param_mapping[param]]
    else:
        return data[param]
