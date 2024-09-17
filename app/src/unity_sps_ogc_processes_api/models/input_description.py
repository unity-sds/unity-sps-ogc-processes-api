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

from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator

from unity_sps_ogc_processes_api.models.input_description_all_of_max_occurs import (
    InputDescriptionAllOfMaxOccurs,
)
from unity_sps_ogc_processes_api.models.metadata import Metadata
from unity_sps_ogc_processes_api.models.model_schema import ModelSchema

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class InputDescription(BaseModel):
    """
    InputDescription
    """  # noqa: E501

    title: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    keywords: Optional[List[StrictStr]] = None
    metadata: Optional[List[Metadata]] = None
    schema_: ModelSchema = Field(alias="schema")
    min_occurs: Optional[StrictInt] = Field(default=1, alias="minOccurs")
    max_occurs: Optional[StrictInt] = Field(alias="maxOccurs")
    value_passing: Optional[List[StrictStr]] = Field(default=None, alias="valuePassing")
    __properties: ClassVar[List[str]] = [
        "title",
        "description",
        "keywords",
        "metadata",
        "schema",
        "minOccurs",
        "maxOccurs",
        "valuePassing",
    ]

    @field_validator("value_passing")
    def value_passing_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        for i in value:
            if i not in ("byValue", "byReference"):
                raise ValueError("each list item must be one of ('byValue', 'byReference')")
        return value

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
        """Create an instance of InputDescription from a JSON string"""
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
        if self.schema_:
            _dict["schema"] = self.schema_.to_dict()
        # override the default output from pydantic by calling `to_dict()` of max_occurs
        if self.max_occurs:
            _dict["maxOccurs"] = self.max_occurs.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of InputDescription from a dict"""
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
                    ModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None
                ),
                "minOccurs": (obj.get("minOccurs") if obj.get("minOccurs") is not None else 1),
                "maxOccurs": (
                    InputDescriptionAllOfMaxOccurs.from_dict(obj.get("maxOccurs"))
                    if obj.get("maxOccurs") is not None
                    else None
                ),
                "valuePassing": obj.get("valuePassing"),
            }
        )
        return _obj
