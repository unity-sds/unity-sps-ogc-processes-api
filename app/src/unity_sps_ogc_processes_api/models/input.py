from __future__ import annotations

import json
import pprint
from typing import Any, Dict, List, Union

from pydantic import RootModel, model_validator
from unity_sps_ogc_processes_api.models.bbox1 import Bbox1
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.qualified_input_value1 import QualifiedInputValue1


class Input(RootModel):
    root: Union[
        Bbox1,
        List[Any],
        bool,
        float,
        int,
        str,
        Link,
        QualifiedInputValue1,
        List[Union[Bbox1, List[Any], bool, float, int, str, Link, QualifiedInputValue1]],
    ]

    @model_validator(mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, dict):
            if all(k in value for k in ["mediaType", "encoding", "schema", "value"]):
                return QualifiedInputValue1(**value)
            if "bbox" in value:
                return Bbox1(**value)
            if "href" in value:
                return Link(**value)
        elif isinstance(value, list):
            return [cls.validate_type(item) for item in value]
        elif isinstance(value, (bool, int, float, str, Bbox1, Link, QualifiedInputValue1)):
            return value
        elif isinstance(value, List):
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
