import sqlalchemy
from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID

from fastapi_sqlalchemy.models.base import BASE, Session, MODEL_MAPPING
from fastapi_sqlalchemy.models.mixins import GuidMixin, TimestampMixin, DictMixin


class Country(BASE, GuidMixin, TimestampMixin):
    """
    The countries table
    """
    __tablename__ = "countries"
    __abstract__ = False

    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    code = sqlalchemy.Column(
        sqlalchemy.String(2),
        nullable=False,
        unique=True
    )

    @validates("name")
    def _set_name(
            self,
            _key: str,
            value: str
    ) -> str:
        # pylint: disable=no-self-use
        return value.capitalize()

    @classmethod
    def get_by_code(
            cls,
            session: Session,
            code: str,
    ):
        """ Lookup a Country by code
        """
        return session.query(cls).filter(cls.code == code).first()

    @property
    def identity(self) -> str:
        return str(self.id)


@event.listens_for(Country, "mapper_configured", propagate=True)
def _mapper_configured(_mapper, cls):
    if getattr(cls, "__model_mapping__", True):
        MODEL_MAPPING["Country"] = cls


class PlaceType(BASE, DictMixin, GuidMixin, TimestampMixin):
    """
    The types of place table
    """
    __tablename__ = "place_types"
    __abstract__ = False

    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    description = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False
    )

    @validates("description")
    def _set_description(
            self,
            _key: str,
            value: str
    ) -> str:
        # pylint: disable=no-self-use
        return value.capitalize()

    @classmethod
    def get_by_description(
            cls,
            session: Session,
            description: str,
    ):
        """ Lookup a PlaceType by name
        """
        return session.query(cls).filter(cls.description == description).first()

    @property
    def identity(self) -> str:
        return str(self.id)


@event.listens_for(PlaceType, "mapper_configured", propagate=True)
def _mapper_configured(_mapper, cls):
    if getattr(cls, "__model_mapping__", True):
        MODEL_MAPPING["PlaceType"] = cls


class Place(BASE, DictMixin, GuidMixin, TimestampMixin):
    """
    The places table
    """
    __tablename__ = "places"
    __abstract__ = False

    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    place_type = sqlalchemy.Column(
        UUID,
        sqlalchemy.ForeignKey("place_types.id"),
        nullable=False
    )

    @validates("name")
    def _set_name(
            self,
            _key: str,
            value: str
    ) -> str:
        # pylint: disable=no-self-use
        return value.capitalize()

    @classmethod
    def get_by_type(
            cls,
            session: Session,
            place_type: str,
    ):
        """ Lookup a Place by type
        """
        return session.query(cls).filter(cls.place_type == place_type).first()

    @property
    def identity(self) -> str:
        return str(self.id)


@event.listens_for(Place, "mapper_configured", propagate=True)
def _mapper_configured(_mapper, cls):
    if getattr(cls, "__model_mapping__", True):
        MODEL_MAPPING["Place"] = cls
