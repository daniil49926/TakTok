

async def get_user_by_name(pool, name):
    _sql = """
        SELECT * FROM public."Profile" pr 
            WHERE pr.username = $1
    """
    async with pool.acquire() as coon:
        user = await coon.fetchrow(_sql, name)
    return user
