from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        return db_obj

    def get(self, session: AsyncSession, *args, **kwargs) -> Optional[ModelType]:
        result = session.execute(
            select(self._model).filter(*args).filter_by(**kwargs)
        )
        return result.scalars().first()

    def get_multi(
        self, session: AsyncSession, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        result = session.execute(
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    def update(
        self,
        session: AsyncSession,
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db_obj: Optional[ModelType] = None,
        **kwargs
    ) -> Optional[ModelType]:
        db_obj = db_obj or self.get(session, **kwargs)
        if db_obj is not None:
            obj_data = db_obj.__dict__
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            session.commit()
        return db_obj

    def delete(
        self, session: AsyncSession, *args, db_obj: Optional[ModelType] = None, **kwargs
    ) -> ModelType:
        db_obj = db_obj or self.get(session, *args, **kwargs)
        session.delete(db_obj)
        session.commit()
        return db_obj
