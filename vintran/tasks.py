import datetime
import logging

from vintran import app, db
from vintran.models import VintranFile


def check_expired_files():
    with app.app_context():
        files: list[VintranFile] = filter(
            lambda f: datetime.datetime.strptime(f.expiration, "%Y-%m-%d %H:%M:%S.%f")
            < datetime.datetime.now(),
            VintranFile.query.all(),
        )

        for file in files:
            logging.debug(
                f"File {file.filename} ({file.file_id}) has expired! Deleting..."
            )
            db.session.delete(file)
            db.session.commit()
