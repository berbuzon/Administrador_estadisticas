"""Herramientas de apoyo para trabajar con modelos de SQLAlchemy."""

from __future__ import annotations

from typing import Iterable, List, Mapping, Optional, Sequence, Type, TypeVar, Union

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - comportamiento dependiente del entorno
    pd = None  # type: ignore[assignment]
    _PANDAS_IMPORT_ERROR = exc
else:  # pragma: no cover - rama trivial
    _PANDAS_IMPORT_ERROR = None

try:
    from sqlalchemy.orm import Query, Session
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    from sqlalchemy.orm.decl_api import DeclarativeMeta
except ImportError as exc:  # pragma: no cover - comportamiento dependiente del entorno
    Query = Session = InstrumentedAttribute = DeclarativeMeta = None  # type: ignore[assignment]
    _SQLALCHEMY_IMPORT_ERROR = exc
else:  # pragma: no cover - rama trivial
    _SQLALCHEMY_IMPORT_ERROR = None


def _require_pandas():
    """Devuelve el módulo :mod:`pandas` o lanza un error informativo."""

    if pd is None:  # pragma: no cover - depende de si pandas está instalado
        mensaje = (
            "Se requiere tener 'pandas' instalado para utilizar ModelUtils. "
            "Instálalo con 'pip install pandas'."
        )
        raise RuntimeError(mensaje) from _PANDAS_IMPORT_ERROR
    return pd


def _require_sqlalchemy():
    """Verifica que SQLAlchemy esté disponible antes de usar ModelUtils."""

    if Session is None:  # pragma: no cover - depende de si SQLAlchemy está instalado
        mensaje = (
            "Se requiere tener 'SQLAlchemy' instalado para utilizar ModelUtils. "
            "Instálalo con 'pip install sqlalchemy'."
        )
        raise RuntimeError(mensaje) from _SQLALCHEMY_IMPORT_ERROR

if DeclarativeMeta is not None:  # pragma: no cover - depende de SQLAlchemy
    _ModelT = TypeVar("_ModelT", bound=DeclarativeMeta)
else:  # pragma: no cover - rama utilizada solo si no hay SQLAlchemy
    _ModelT = TypeVar("_ModelT", bound=Type)


class ModelUtils:
    """Utilidades estáticas para operaciones comunes sobre modelos."""

    @staticmethod
    def model_to_dataframe(
        session: Session,
        model: Type[_ModelT],
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        columns: Optional[Sequence[InstrumentedAttribute]] = None,
        filters: Optional[Sequence[object]] = None,
        order_by: Optional[Sequence[object]] = None,
    ) -> pd.DataFrame:
        """Convierte una consulta de un modelo en un :class:`pandas.DataFrame`.

        Parameters
        ----------
        session:
            Sesión SQLAlchemy desde la que se ejecutará la consulta.
        model:
            Clase del modelo mapeado que se quiere consultar.
        limit:
            Número máximo de registros a recuperar. Si es ``None`` se traen todos.
        offset:
            Cantidad de registros a omitir antes de comenzar a devolver resultados.
        columns:
            Columnas a incluir en el DataFrame. Si es ``None`` se utilizan todas las
            columnas declaradas en el modelo.
        filters:
            Condiciones adicionales que se aplicarán con ``query.filter``.
        order_by:
            Lista de columnas o expresiones para ordenar los resultados.

        Returns
        -------
        pandas.DataFrame
            DataFrame conteniendo los registros solicitados.
        """

        _require_sqlalchemy()
        pandas = _require_pandas()
        query: Query = session.query(model)
        if columns:
            query = query.with_entities(*columns)
        if filters:
            query = query.filter(*filters)
        if order_by:
            query = query.order_by(*order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        rows = query.all()
        column_names = ModelUtils._column_names(
            model=model,
            columns=columns,
            query=query,
            sample_row=rows[0] if rows else None,
        )
        if not rows:
            return pandas.DataFrame(columns=column_names)

        records = ModelUtils._rows_to_dicts(rows, column_names)
        return pandas.DataFrame.from_records(records, columns=column_names)

    @staticmethod
    def rows_to_dataframe(
        rows: Iterable[object],
        *,
        model: Optional[Type[_ModelT]] = None,
        columns: Optional[Sequence[Union[InstrumentedAttribute, str]]] = None,
    ) -> pd.DataFrame:
        """Convierte cualquier iterable de filas en un :class:`pandas.DataFrame`.

        Esta utilidad es útil cuando ya se dispone de los resultados de una consulta
        personalizada (por ejemplo, usando ``session.execute``) pero se desea mantener
        una salida consistente con :meth:`model_to_dataframe`. Cuando se trabaja con
        datos ya materializados (listas de diccionarios, tuplas nombradas, etc.) se
        puede utilizar sin tener SQLAlchemy instalado siempre que las columnas se
        proporcionen como cadenas simples.
        """

        pandas = _require_pandas()
        if model is not None or ModelUtils._columns_need_sqlalchemy(columns):
            _require_sqlalchemy()
        materialized_rows = list(rows)
        column_names = ModelUtils._column_names(
            model=model,
            columns=columns,
            sample_row=materialized_rows[0] if materialized_rows else None,
        )
        if not materialized_rows:
            return pandas.DataFrame(columns=column_names)

        records = ModelUtils._rows_to_dicts(materialized_rows, column_names)
        return pandas.DataFrame.from_records(records, columns=column_names)

    @staticmethod
    def _rows_to_dicts(
        rows: Iterable[object],
        column_names: Sequence[str],
    ) -> List[Mapping[str, object]]:
        """Convierte filas devueltas por SQLAlchemy en diccionarios sencillos."""

        dicts: List[Mapping[str, object]] = []
        for row in rows:
            if hasattr(row, "_mapping"):
                mapping = row._mapping  # SQLAlchemy Row o RowMapping
                dicts.append({name: mapping[name] for name in column_names})
            elif isinstance(row, Mapping):
                dicts.append({name: row[name] for name in column_names})
            else:
                dicts.append({name: getattr(row, name) for name in column_names})
        return dicts

    @staticmethod
    def _column_names(
        *,
        model: Optional[Type[_ModelT]] = None,
        columns: Optional[Sequence[Union[InstrumentedAttribute, str]]] = None,
        query: Optional[Query] = None,
        sample_row: Optional[object] = None,
    ) -> List[str]:
        if columns:
            names: List[str] = []
            for column in columns:
                if isinstance(column, str):
                    names.append(column)
                    continue
                key = getattr(column, "key", None)
                if key:
                    names.append(key)
                    continue
                name = getattr(column, "name", None)
                if name:
                    names.append(name)
                    continue
                names.append(str(column))
            return names

        if model is not None:
            return [attr.key for attr in model.__mapper__.column_attrs]

        if query is not None:
            names = [desc.get("name") for desc in getattr(query, "column_descriptions", [])]
            if any(names):
                return [name for name in names if name]

        if sample_row is not None:
            if hasattr(sample_row, "_mapping"):
                return list(sample_row._mapping.keys())
            if isinstance(sample_row, Mapping):
                return list(sample_row.keys())

        return []

    @staticmethod
    def _columns_need_sqlalchemy(
        columns: Optional[Sequence[Union[InstrumentedAttribute, str]]]
    ) -> bool:
        """Indica si las columnas requieren soporte de SQLAlchemy."""

        if not columns:
            return False

        for column in columns:
            if isinstance(column, str):
                continue
            if InstrumentedAttribute is not None:
                try:
                    if isinstance(column, InstrumentedAttribute):
                        return True
                except TypeError:  # pragma: no cover - InstrumentedAttribute no es un tipo
                    pass
            if hasattr(column, "key") or hasattr(column, "expression"):
                return True
        return False
