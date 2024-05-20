from sqlalchemy.orm import Mapped, mapped_column

from vintran import db


class VintranFile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    mimetype: Mapped[str] = mapped_column(nullable=False)
    file_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    ipv4: Mapped[str] = mapped_column(nullable=False)
    buffer: Mapped[bytes] = mapped_column(nullable=False)
    expiration: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return (
            "VintranFile {\n"
            f"\tID - {self.id},\n"
            f"\tFilename - {self.filename},\n"
            f"\tMimetype - {self.mimetype},\n"
            f"\tFile ID - {self.file_id},\n"
            f"\tHash - {self.file_hash},\n"
            f"\tIPv4 Address - {self.file_hash},\n"
            f"\tBuffer - {self.buffer[:16]}... ({len(self.buffer) - 15} more characters)\n"
            f"\tExpiration date - {self.expiration}\n"
            "}"
        )
