from datetime import datetime, timezone

import pytest
from sqlmodel import Field, SQLModel

from models.common.base_models import BaseModel, TimestampMixin


class TestTimestampMixin:
    def test_timestamp_mixin_creation(self):
        class TestModel1(TimestampMixin, table=True):
            __tablename__ = "test_model_1"
            id: int = Field(primary_key=True)
            name: str = Field()

        before_creation = datetime.now(timezone.utc)
        model = TestModel1(id=1, name="test")
        after_creation = datetime.now(timezone.utc)

        assert model.created_at is not None
        assert before_creation <= model.created_at <= after_creation
        assert model.updated_at is None

    def test_timestamp_mixin_update(self):
        class TestModel2(TimestampMixin, table=True):
            __tablename__ = "test_model_2"
            id: int = Field(primary_key=True)
            name: str = Field()

        model = TestModel2(id=1, name="test")
        original_created_at = model.created_at

        model.updated_at = datetime.now(timezone.utc)

        assert model.created_at == original_created_at
        assert model.updated_at is not None

    def test_timestamp_mixin_inheritance(self):
        class TestModel3(TimestampMixin, SQLModel):
            name: str

        model = TestModel3(name="test")

        assert hasattr(model, "created_at")
        assert hasattr(model, "updated_at")
        assert model.created_at is not None
        assert model.updated_at is None


class TestBaseModel:
    def test_base_model_config(self):
        class TestModel4(BaseModel):
            name: str

        model = TestModel4(name="test")

        # Check that model_config exists and has the right settings
        assert hasattr(model, "model_config")
        assert model.model_config.get("arbitrary_types_allowed") is True

    def test_base_model_inheritance(self):
        class TestModel5(BaseModel):
            name: str
            value: int

        model = TestModel5(name="test", value=42)

        assert model.name == "test"
        assert model.value == 42
        assert hasattr(model, "model_config")

    def test_base_model_with_timestamp_mixin(self):
        class TestModel6(TimestampMixin, BaseModel):
            name: str

        model = TestModel6(name="test")

        assert hasattr(model, "created_at")
        assert hasattr(model, "updated_at")
        assert hasattr(model, "model_config")
        assert model.model_config.get("arbitrary_types_allowed") is True
