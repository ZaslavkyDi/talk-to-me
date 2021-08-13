import datetime
import re

import ulid
from sqlalchemy import TIMESTAMP, Column, MetaData, String
from sqlalchemy.orm import declarative_base, declared_attr
from stringcase import snakecase

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(
    metadata=meta
)  #: This is the class whose metadata all orm models should use


class TimeStamped:
    """
    Marker for models that have creation and update timestamps.
    Initializes the updated time to the same value as the create time
    """

    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=datetime.datetime.utcnow,
        default=lambda context: context.get_current_parameters()["created_at"],
    )


class BaseOrmModel(TimeStamped, Base):
    """
    Provides an automated table name, primary key column, created and updated timestamps
    """

    __abstract__ = True
    id = Column(String(32), primary_key=True, default=lambda: ulid.new().str)

    @declared_attr
    def __tablename__(
        cls,
    ) -> str:  # cannot use @classmethod here otherwise Alembic explodes
        """
        Provide automated table name
        :return:
        """
        return re.sub("^orm_", "", snakecase(cls.__name__))
