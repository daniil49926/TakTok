from apps.profile.utils import get_user_by_name
from core.security.security import check_password_hash


async def validate_login(conn, form):

    username = form['username']
    password = form['password']

    if not username:
        return 'username is required', None
    if not password:
        return 'password is required', None

    user = await get_user_by_name(conn, username)

    if not user:
        return 'Invalid username', None
    if not check_password_hash(password, user[6]):
        return 'Invalid password', None

    return None, user
