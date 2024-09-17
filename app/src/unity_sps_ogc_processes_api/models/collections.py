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
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from unity_sps_ogc_processes_api.models.collection_info import CollectionInfo
from unity_sps_ogc_processes_api.models.link import Link

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Collections(BaseModel):
    """
    Collections
    """  # noqa: E501

    links: List[Link]
    time_stamp: Optional[datetime] = Field(default=None, alias="timeStamp")
    number_matched: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(
        default=None, alias="numberMatched"
    )
    number_returned: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(
        default=None, alias="numberReturned"
    )
    collections: List[CollectionInfo]
    __properties: ClassVar[List[str]] = [
        "links",
        "timeStamp",
        "numberMatched",
        "numberReturned",
        "collections",
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
        """Create an instance of Collections from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict["links"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in collections (list)
        _items = []
        if self.collections:
            for _item in self.collections:
                if _item:
                    _items.append(_item.to_dict())
            _dict["collections"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Collections from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "links": (
                    [Link.from_dict(_item) for _item in obj.get("links")]
                    if obj.get("links") is not None
                    else None
                ),
                "timeStamp": obj.get("timeStamp"),
                "numberMatched": obj.get("numberMatched"),
                "numberReturned": obj.get("numberReturned"),
                "collections": (
                    [CollectionInfo.from_dict(_item) for _item in obj.get("collections")]
                    if obj.get("collections") is not None
                    else None
                ),
            }
        )
        return _obj
