from __future__ import annotations

import json
import pprint
from typing import Any, Dict, List, Union

from pydantic import RootModel, ValidationError, model_validator

from unity_sps_ogc_processes_api.models.inline_or_ref_data1 import InlineOrRefData1


class Input(RootModel):
    root: Union[InlineOrRefData1, List[InlineOrRefData1]]

    @model_validator(mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, dict):
            try:
                return InlineOrRefData1(**value)
            except ValidationError:
                pass
        elif isinstance(value, list):
            try:
                return [InlineOrRefData1(**item) for item in value]
            except ValidationError:
                pass
        elif isinstance(value, InlineOrRefData1):
            return value
        raise ValueError(f"Invalid type for Input: {type(value)}")

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Input:
        return cls(root=cls.validate_type(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Input:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.root, list):
            return [item.model_dump() for item in self.root]
        return self.root.model_dump()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)

    def __repr__(self) -> str:
        return f"Input({self.root!r})"

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump())
