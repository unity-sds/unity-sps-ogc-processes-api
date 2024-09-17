# coding: utf-8

"""
    OGC API - Processes

    Example API Definition for OGC API - Processes

    The version of the OpenAPI document: 0.1
    Contact: info@ogc.org
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
from typing import Any, Dict, List, Union

from pydantic import RootModel, model_validator

from unity_sps_ogc_processes_api.models.bbox import Bbox
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.qualified_input_value import QualifiedInputValue


class InlineOrRefData(RootModel):
    root: Union[Bbox, List[Any], bool, float, int, str, Link, QualifiedInputValue]

    @model_validator(mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, dict):
            if all(k in value for k in ["mediaType", "encoding", "schema", "value"]):
                return QualifiedInputValue(**value)
            if "href" in value:
                return Link(**value)
            if "bbox" in value:
                return Bbox(**value)
            return value  # Handle other dict cases
        elif isinstance(value, (Bbox, Link, QualifiedInputValue, bool, int, float, str)):
            return value
        elif isinstance(value, list):
            return value
        raise ValueError(f"Invalid type for InlineOrRefData: {type(value)}")

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> InlineOrRefData:
        return cls(root=cls.validate_type(obj))

    @classmethod
    def from_json(cls, json_str: str) -> InlineOrRefData:
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.root, (Bbox, Link, QualifiedInputValue)):
            return self.root.model_dump()
        return self.root

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)

    def __repr__(self) -> str:
        return f"InlineOrRefData({self.root!r})"

    def to_str(self) -> str:
        return pprint.pformat(self.model_dump())
