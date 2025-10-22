import types
import unittest
from unittest import mock

try:
    import pandas as pd
    from pandas.testing import assert_frame_equal
except ImportError:  # pragma: no cover - pruebas se omiten si falta pandas
    pd = None  # type: ignore[assignment]
    assert_frame_equal = None  # type: ignore[assignment]
try:
    from sqlalchemy import Column, Integer, String, create_engine
    from sqlalchemy.orm import Session, declarative_base, sessionmaker
except ImportError:  # pragma: no cover - pruebas se omiten si falta SQLAlchemy
    Column = Integer = String = create_engine = None  # type: ignore[assignment]
    Session = declarative_base = sessionmaker = None  # type: ignore[assignment]

from src.utils import model_utils
from src.utils.model_utils import ModelUtils
from utils.model_utils import ModelUtils as CompatModelUtils


class ModelUtilsCompatibilityTestCase(unittest.TestCase):
    """Pruebas que validan importaciones retrocompatibles."""

    def test_legacy_import_exposes_same_class(self) -> None:
        self.assertIs(CompatModelUtils, ModelUtils)


class ModelUtilsDependencyGuardsTestCase(unittest.TestCase):
    """Pruebas que verifican los mensajes cuando faltan dependencias opcionales."""

    def test_model_to_dataframe_requires_sqlalchemy_when_missing(self) -> None:
        if model_utils.Session is not None:
            self.skipTest("SQLAlchemy está instalado en el entorno de pruebas")

        dummy_session = mock.Mock()
        dummy_model = type("DummyModel", (), {})

        with self.assertRaisesRegex(RuntimeError, "SQLAlchemy"):
            ModelUtils.model_to_dataframe(dummy_session, dummy_model)

    def test_rows_to_dataframe_requires_pandas_when_missing(self) -> None:
        if model_utils.pd is not None:
            self.skipTest("pandas está instalado en el entorno de pruebas")

        with mock.patch("src.utils.model_utils.Session", object()):
            with self.assertRaisesRegex(RuntimeError, "pandas"):
                ModelUtils.rows_to_dataframe([])

    def test_rows_to_dataframe_with_plain_dicts_without_sqlalchemy(self) -> None:
        class FakeDataFrame:
            def __init__(self, data=None, columns=None):
                self.data = list(data or [])
                self.columns = list(columns or [])

            @classmethod
            def from_records(cls, records, columns=None):
                return cls(records, columns)

        fake_pandas = types.SimpleNamespace(DataFrame=FakeDataFrame)
        rows = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]

        with mock.patch("src.utils.model_utils._require_pandas", return_value=fake_pandas), \
            mock.patch("src.utils.model_utils._require_sqlalchemy") as require_sqlalchemy:
            df = ModelUtils.rows_to_dataframe(rows, columns=["name", "age"])

        self.assertEqual(df.data, rows)
        self.assertEqual(df.columns, ["name", "age"])
        require_sqlalchemy.assert_not_called()


if declarative_base is not None and Column is not None:
    Base = declarative_base()

    class User(Base):  # type: ignore[misc]
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        age = Column(Integer, nullable=False)

else:  # pragma: no cover - las pruebas se omiten si no hay SQLAlchemy disponible
    Base = None  # type: ignore[assignment]

    class User:  # type: ignore[too-few-public-methods]
        pass


@unittest.skipIf(pd is None, "pandas es requerido para estas pruebas")
@unittest.skipIf(Session is None, "SQLAlchemy es requerido para estas pruebas")
class ModelUtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self) -> None:
        self.session: Session = self.Session()
        self.session.query(User).delete()
        self.session.add_all(
            [
                User(id=1, name="Alice", age=30),
                User(id=2, name="Bob", age=25),
                User(id=3, name="Charlie", age=35),
            ]
        )
        self.session.commit()

    def tearDown(self) -> None:
        self.session.close()

    def test_model_to_dataframe_returns_all_columns(self) -> None:
        df = ModelUtils.model_to_dataframe(
            self.session,
            User,
            order_by=[User.id],
        )

        expected = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "age": [30, 25, 35],
            }
        )
        assert_frame_equal(df.reset_index(drop=True), expected)

    def test_model_to_dataframe_applies_filters_limit_and_offset(self) -> None:
        df = ModelUtils.model_to_dataframe(
            self.session,
            User,
            filters=[User.age >= 30],
            limit=1,
            offset=1,
            order_by=[User.age.desc()],
        )

        expected = pd.DataFrame({"id": [1], "name": ["Alice"], "age": [30]})
        assert_frame_equal(df.reset_index(drop=True), expected)

    def test_model_to_dataframe_selects_specific_columns(self) -> None:
        df = ModelUtils.model_to_dataframe(
            self.session,
            User,
            columns=[User.name],
            order_by=[User.name],
        )

        expected = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
        assert_frame_equal(df.reset_index(drop=True), expected)

    def test_rows_to_dataframe_with_query_rows(self) -> None:
        rows = self.session.query(User.name, User.age).order_by(User.name).all()

        df = ModelUtils.rows_to_dataframe(rows)

        expected = pd.DataFrame(
            {
                "name": ["Alice", "Bob", "Charlie"],
                "age": [30, 25, 35],
            }
        )
        assert_frame_equal(df.reset_index(drop=True), expected)

    def test_rows_to_dataframe_empty_uses_provided_columns(self) -> None:
        df = ModelUtils.rows_to_dataframe([], columns=[User.name, User.age])

        expected = pd.DataFrame(columns=["name", "age"])
        assert_frame_equal(df, expected)


if __name__ == "__main__":
    unittest.main()
