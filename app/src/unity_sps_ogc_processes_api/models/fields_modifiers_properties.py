from __future__ import annotations

import json
import pprint
from typing import Any, Dict, List, Union

from pydantic import RootModel, StrictStr, model_validator


class FieldsModifiersProperties(RootModel):
    root: Union[Dict[str, StrictStr], List[StrictStr]]

    @model_validator(mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, dict):
            return {k: StrictStr(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [StrictStr(item) for item in value]
        raise ValueError(f"Invalid type for FieldsModifiersProperties: {type(value)}")

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> FieldsModifiersProperties:
        return cls(root=cls.validate_type(obj))

    @classmethod
    def from_json(cls, json_str: str) -> FieldsModifiersProperties:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        return self.root

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)

    def __repr__(self) -> str:
        return f"FieldsModifiersProperties({self.root!r})"

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump())
