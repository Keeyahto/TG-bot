from tortoise import Tortoise

from config import config


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        # db_url='mysql://root:1234@localhost:3306/db',
        db_url=config['GENERAL']['DB_URL'],
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


# run_async is a helper function to run simple async Tortoise scripts.
