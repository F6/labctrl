
# std libs
import uuid
import os
# third-party libs
from passlib.context import CryptContext
# this package
from config import dump_config_to_file, load_config_from_file, UserAccessLevel, UserConfig


TEMP_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 'config-new-user.json')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
temp_config = load_config_from_file()


def validate_username(username: str) -> bool:
    """
    Validates if a username is usable
    """
    for user in temp_config.auth.users:
        if username == user.username:
            print("Username already taken, please use another username.")
            return False
    return True


def get_access_level(access_level: str) -> UserAccessLevel | None:
    """
    Validates if an access_level is defined, if so, return the enum, if not, return None.
    """
    for e in UserAccessLevel:
        if access_level == e.value:
            return e
    print("Undefined access level, please input only listed values.")
    return None


if __name__ == "__main__":
    print("Registering new user into config, Ctrl-C to cancel.")
    print("========================================================")

    print("Please input the username. The username is used to login to the system to get authentication tokens.")
    username = input("Username:").strip()
    while validate_username(username) is False:
        username = input("Username:").strip()

    print("Please input the password. Note that the password will be echoed in terminal.")
    password = input("Password:").strip()
    hashed_password = pwd_context.hash(password)

    possible_access_levels: str = ", ".join([e.value for e in UserAccessLevel])
    print("Please specify the access level of the new user, possible values are {}".format(
        possible_access_levels))
    access_level = get_access_level(input("Access Level:").strip())
    while access_level is None:
        access_level = get_access_level(input("Access Level:").strip())

    user_id = uuid.uuid4().__str__()
    new_user = UserConfig(id=user_id, username=username,
                          hashed_password=hashed_password, access_level=access_level)
    print("Registering new user with following information: ")
    print(new_user.model_dump_json(indent=4))
    ans = input("Is this OK? [y]/n")
    if ans == 'y' or ans == '':
        temp_config.auth.users.append(new_user)
        dump_config_to_file(temp_config, TEMP_CONFIG_PATH)
        print("Dumped new config to {}.".format(TEMP_CONFIG_PATH))
        print("Check if the new config is correct and rename it to config.json if everything is OK.")
    else:
        print("Aborted.")
