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
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictStr

from unity_sps_ogc_processes_api.models.metadata import Metadata
from unity_sps_ogc_processes_api.models.model_schema import ModelSchema

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class OutputDescription(BaseModel):
    """
    OutputDescription
    """  # noqa: E501

    title: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    keywords: Optional[List[StrictStr]] = None
    metadata: Optional[List[Metadata]] = None
    schema: ModelSchema = Field(alias="schema")
    __properties: ClassVar[List[str]] = [
        "title",
        "description",
        "keywords",
        "metadata",
        "schema",
    ]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of OutputDescription from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in metadata (list)
        _items = []
        if self.metadata:
            for _item in self.metadata:
                if _item:
                    _items.append(_item.to_dict())
            _dict["metadata"] = _items
        # override the default output from pydantic by calling `to_dict()` of schema
        if self.schema:
            _dict["schema"] = self.schema.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of OutputDescription from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "title": obj.get("title"),
                "description": obj.get("description"),
                "keywords": obj.get("keywords"),
                "metadata": (
                    [Metadata.from_dict(_item) for _item in obj.get("metadata")]
                    if obj.get("metadata") is not None
                    else None
                ),
                "schema": (
                    ModelSchema.from_dict(obj.get("schema"))
                    if obj.get("schema") is not None
                    else None
                ),
            }
        )
        return _obj
