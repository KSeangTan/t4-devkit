from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from attrs import converters, define, field, validators

from t4_devkit.common.converter import to_quaternion
from t4_devkit.common.validator import is_vector3, is_vector6

from ..name import SchemaName
from .base import SchemaBase
from .registry import SCHEMAS

if TYPE_CHECKING:
    from t4_devkit.typing import QuaternionLike, Vector3Like, Vector6Like


__all__ = ["EgoPose"]


@define(slots=False)
@SCHEMAS.register(SchemaName.EGO_POSE)
class EgoPose(SchemaBase):
    """A dataclass to represent schema table of `ego_pose.json`.

    Attributes:
        token (str): Unique record identifier.
        translation (Vector3Like): Coordinate system origin given as [x, y, z] in [m].
        rotation (QuaternionLike): Coordinate system orientation given as quaternion [w, x, y, z].
        timestamp (int): Unix time stamp.
        twist (Vector6Like | None): Linear and angular velocities in the local coordinate system of
            the ego vehicle (in m/s for linear and rad/s for angular), in the order of
            (vx, vy, vz, yaw_rate, pitch_rate, roll_rate).
        acceleration (Vector3Like | None): Acceleration in the local coordinate system of
            the ego vehicle (in m/s2), in the order of (ax, ay, az).
        geocoordinate (Vector3Like | None): Coordinates in the WGS 84 reference ellipsoid
            (latitude, longitude, altitude) in degrees and meters.
    """

    translation: Vector3Like = field(converter=np.array, validator=is_vector3)
    rotation: QuaternionLike = field(converter=to_quaternion)
    timestamp: int = field(validator=validators.instance_of(int))
    twist: Vector6Like | None = field(
        default=None,
        converter=converters.optional(np.array),
        validator=validators.optional(is_vector6),
    )
    acceleration: Vector3Like | None = field(
        default=None,
        converter=converters.optional(np.array),
        validator=validators.optional(is_vector3),
    )
    geocoordinate: Vector3Like | None = field(
        default=None,
        converter=converters.optional(np.array),
        validator=validators.optional(is_vector3),
    )
