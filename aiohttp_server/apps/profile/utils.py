
async def get_user_by_name(conn, name):
    _sql = """
        SELECT * FROM public."Profile" pr 
            WHERE pr.username = $1
    """ # noqa
    return await conn.fetchrow(_sql, name)
