from __future__ import annotations

import json
from typing import Any, Dict, Union

from pydantic import RootModel, ValidationError, model_validator

from unity_sps_ogc_processes_api.models.metadata_one_of import MetadataOneOf
from unity_sps_ogc_processes_api.models.metadata_one_of1 import MetadataOneOf1


class Metadata(RootModel):
    root: Union[MetadataOneOf, MetadataOneOf1]

    @model_validator(mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, dict):
            try:
                return MetadataOneOf(**value)
            except ValidationError:
                try:
                    return MetadataOneOf1(**value)
                except ValidationError:
                    pass
        elif isinstance(value, (MetadataOneOf, MetadataOneOf1)):
            return value
        raise ValueError(f"Invalid type for Metadata: {type(value)}")

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Metadata:
        return cls(root=cls.validate_type(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Metadata:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        return self.root.model_dump()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)

    def __repr__(self) -> str:
        return f"Metadata({self.root!r})"
