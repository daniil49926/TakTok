
async def get_videos(conn):
    _sql = """
        SELECT * FROM public."TakVideo"
    """
    return await conn.fetch(_sql)
