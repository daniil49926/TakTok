import asyncio
import asyncpg
from aiohttp_server.core.settings import settings


async def _connect() -> asyncpg.Connection:
    return await asyncpg.connect(dsn=settings.PG_DSN)


async def create_tables():
    conn = await _connect()
    await conn.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS public."Profile_id_seq"
        INCREMENT 1
        START 1
        MINVALUE 1
        MAXVALUE 2147483647
        CACHE 1
        """
    )
    await conn.execute(
        f"""
        ALTER SEQUENCE public."Profile_id_seq"
            OWNER TO "{settings.PG_USER}"
        """
    )
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS public."Profile"
        (
            id integer NOT NULL DEFAULT nextval('"Profile_id_seq"'::regclass),
            name character varying COLLATE pg_catalog."default" NOT NULL,
            surname character varying COLLATE pg_catalog."default" NOT NULL,
            username character varying COLLATE pg_catalog."default" NOT NULL,
            gender integer NOT NULL,
            email character varying COLLATE pg_catalog."default" NOT NULL,
            hashed_password character varying COLLATE pg_catalog."default" NOT NULL,
            created_at timestamp without time zone,
            is_active integer NOT NULL,
            CONSTRAINT "Profile_pkey" PRIMARY KEY (id),
            CONSTRAINT "Profile_email_key" UNIQUE (email),
            CONSTRAINT "Profile_username_key" UNIQUE (username)
        )
        """
    )
    await conn.execute(
        f"""      
        ALTER TABLE IF EXISTS public."Profile"
            OWNER to "{settings.PG_USER}"
        """
    )
    await conn.close()


if __name__ == "__main__":
    asyncio.run(create_tables())
