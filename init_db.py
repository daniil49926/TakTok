import asyncio
import asyncpg
import argparse
from aiohttp_server.core.settings import settings


async def _connect() -> asyncpg.Connection:
    return await asyncpg.connect(dsn=settings.PG_DSN)


async def create_sequence(
    name_of_sequence: str,
    open_conn: asyncpg.Connection
) -> None:
    await open_conn.execute(
        f"""
        CREATE SEQUENCE IF NOT EXISTS public."{name_of_sequence}"
        INCREMENT 1
        START 1
        MINVALUE 1
        MAXVALUE 2147483647
        CACHE 1
        """
    )


async def create_all():
    conn = await _connect()
    await create_sequence(name_of_sequence="Profile_id_seq", open_conn=conn)
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
    await create_sequence(name_of_sequence="TakVideo_id_seq", open_conn=conn)
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS public."TakVideo"
        (
            id integer NOT NULL DEFAULT nextval('"TakVideo_id_seq"'::regclass),
            title character varying(50) COLLATE pg_catalog."default" NOT NULL,
            description character varying(500) COLLATE pg_catalog."default" NOT NULL,
            file_path character varying(1000) COLLATE pg_catalog."default" NOT NULL,
            create_at timestamp without time zone,
            Profile_id integer,
            in_ban_list integer,
            CONSTRAINT "TakVideo_pkey" PRIMARY KEY (id),
            CONSTRAINT "TakVideo_Profile_id_fkey" FOREIGN KEY (Profile_id)
                REFERENCES public."Profile" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
        )
        """
    )
    await create_sequence(name_of_sequence="TakVideoLikes_id_seq", open_conn=conn)
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS public."TakVideoLikes"
        (
            id integer NOT NULL DEFAULT nextval('"TakVideoLikes_id_seq"'::regclass),
            video_id integer NOT NULL,
            user_id integer NOT NULL,
            CONSTRAINT "TakVideoLikes_pkey" PRIMARY KEY (id),
            CONSTRAINT "TakVideoLikes_video_id_fkey" FOREIGN KEY (video_id)
                REFERENCES public."TakVideo" (id) MATCH SIMPLE
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            CONSTRAINT "TakVideoLikes_user_id_fkey" FOREIGN KEY (user_id)
                REFERENCES public."Profile" (id) MATCH SIMPLE
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """
    )
    await create_sequence(name_of_sequence="Comment_id_seq", open_conn=conn)
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS public."Comment"
        (
            id integer NOT NULL DEFAULT nextval('"Comment_id_seq"'::regclass),
            video_id integer NOT NULL,
            user_id integer NOT NULL,
            comment_text character varying(500) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT "Comment_pkey" PRIMARY KEY (id),
            CONSTRAINT "Comment_video_id_fkey" FOREIGN KEY (video_id)
                REFERENCES public."TakVideo" (id) MATCH SIMPLE
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            CONSTRAINT "Comment_user_id_fkey" FOREIGN KEY (user_id)
                REFERENCES public."Profile" (id) MATCH SIMPLE
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """
    )
    await conn.close()


async def drop_all():
    conn = await _connect()
    await conn.execute(
        """
        DROP TABLE IF EXISTS public."Comment"
        """
    )
    await conn.execute(
        """
        DROP SEQUENCE IF EXISTS public."Comment_id_seq"
        """
    )
    await conn.execute(
        """
        DROP TABLE IF EXISTS public."TakVideoLikes"
        """
    )
    await conn.execute(
        """
        DROP SEQUENCE IF EXISTS public."TakVideoLikes_id_seq"
        """
    )
    await conn.execute(
        """
        DROP TABLE IF EXISTS public."TakVideo"
        """
    )
    await conn.execute(
        """
        DROP SEQUENCE IF EXISTS public."TakVideo_id_seq"
        """
    )
    await conn.execute(
        """
        DROP TABLE IF EXISTS public."Profile"
        """
    )
    await conn.execute(
        """
        DROP SEQUENCE IF EXISTS public."Profile_id_seq"
        """
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TakTok Init DB script")
    parser.add_argument(
        "--mod",
        help="Script modifier, either delete all entities - 0, or create all entities - 1.",
        default=1
    )
    args = parser.parse_args()
    coro = create_all if int(args.mod) else drop_all
    asyncio.run(coro())


