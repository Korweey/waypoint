"""
waypoint_core/trail_types.py
-----------------------------
Week 8 — Hierarchy, polymorphism, mixins, and operators.

Class hierarchy:
    Trail (abstract base class)
    ├── DayHike
    │   └── GuidedDayHike
    ├── BackpackingRoute
    └── TrailRun

Mixins:
    ElevationMixin  — adds grade_percent() calculation
    RatingMixin     — adds average star rating

All concrete subclasses implement:
    estimated_time() — returns estimated hours as float
    summary()        — returns a one-line string description

Mixed Resolution Order (MRO) for GuidedDayHike:
    GuidedDayHike -> DayHike -> ElevationMixin
    -> RatingMixin -> Trail -> ABC -> object
    (verify with GuidedDayHike.__mro__)
"""

import abc
from waypoint_core.distance import Distance


# ======================================================
# Mixins (added BEFORE Trail in composed class hierarchy)
# ======================================================

class ElevationMixin:
    """
    Mixin that adds a grade_percent() method.

    Computes elevation grade as a percentage of distance.
    Requires the host class to have:
        self.elevation_gain_m  (float)
        self.distance          (Distance in km or mi)

    Usage:
        class DayHike(ElevationMixin, Trail): ...
    """

    def grade_percent(self):
        """
        Calculate the elevation grade as a percentage.

        Formula: (elevation_gain_m / distance_m) * 100
        where distance_m converts the trail distance to metres.

        Returns:
            float: Grade percentage rounded to 2 decimal places.
        """
        # Convert distance to metres
        dist = self.distance
        if dist.unit == 'km':
            distance_m = dist.magnitude * 1000
        else:
            distance_m = dist.magnitude * 1609.34

        if distance_m == 0:
            return 0.0

        return round((self.elevation_gain_m / distance_m) * 100, 2)


class RatingMixin:
    """
    Mixin that adds a star-rating system to a trail.

    Maintains a private list of ratings (1–5 stars).
    Provides add_rating() and average_rating().

    Usage:
        class DayHike(ElevationMixin, RatingMixin, Trail): ...
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the ratings list and pass remaining
        arguments up the MRO chain via super().

        Returns: None
        """
        super().__init__(*args, **kwargs)
        self._ratings = []

    def add_rating(self, stars):
        """
        Add a star rating for this trail.

        Parameters:
            stars (int) : Rating between 1 and 5 inclusive.

        Raises:
            ValueError: If stars is outside 1–5.

        Returns: None
        """
        if not (1 <= stars <= 5):
            raise ValueError(
                f"Rating must be between 1 and 5. Got: {stars}"
            )
        self._ratings.append(stars)

    def average_rating(self):
        """
        Calculate the average star rating.

        Returns:
            float: Average stars, or 0.0 if no ratings yet.
        """
        if not self._ratings:
            return 0.0
        return round(sum(self._ratings) / len(self._ratings), 2)


# ======================================================
# Abstract Base Class: Trail
# ======================================================

class Trail(abc.ABC):
    """
    Abstract base class for all trail types.

    Subclasses MUST implement:
        estimated_time() -> float  (hours)
        summary()        -> str    (one-line description)

    Instantiating Trail directly, or a subclass that is
    missing either abstract method, raises TypeError.

    Class variable:
        default_unit (str) : Platform default unit ('km'/'mi').

    Parameters:
        trail_id         (int)      : Unique identifier.
        name             (str)      : Trail name.
        distance         (Distance) : Trail length.
        elevation_gain_m (float)    : Elevation gain in metres.
        difficulty       (str)      : easy/moderate/hard/expert.
    """

    default_unit       = 'km'
    VALID_DIFFICULTIES = ('easy', 'moderate', 'hard', 'expert')

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty):
        """
        Initialise shared trail attributes.
        Called via super().__init__() from subclasses.

        Parameters:
            trail_id         (int)      : Unique trail ID.
            name             (str)      : Trail name.
            distance         (Distance) : Trail length.
            elevation_gain_m (float)    : Elevation in metres.
            difficulty       (str)      : Difficulty level.

        Raises:
            TypeError:  If distance is not a Distance instance.
            ValueError: If difficulty is invalid.

        Returns: None
        """
        if not isinstance(distance, Distance):
            raise TypeError("distance must be a Distance instance.")
        self.set_difficulty(difficulty)
        self.id               = trail_id
        self.name             = name
        self.distance         = distance
        self.elevation_gain_m = float(elevation_gain_m)

    # --------------------------------------------------
    # Abstract methods — subclasses MUST override these
    # --------------------------------------------------

    @abc.abstractmethod
    def estimated_time(self):
        """
        Return the estimated time to complete this trail
        in hours (float). Each subclass uses its own pacing.

        Returns:
            float: Estimated hours.
        """

    @abc.abstractmethod
    def summary(self):
        """
        Return a one-line string describing this trail.

        Returns:
            str: Human-readable summary.
        """

    # --------------------------------------------------
    # Difficulty — guarded setter / getter
    # --------------------------------------------------

    def set_difficulty(self, difficulty):
        """
        Set difficulty, rejecting invalid values.

        Parameters:
            difficulty (str) : easy/moderate/hard/expert.

        Raises:
            ValueError: If difficulty is invalid.

        Returns: None
        """
        difficulty = difficulty.lower().strip()
        if difficulty not in self.VALID_DIFFICULTIES:
            raise ValueError(
                f"Invalid difficulty '{difficulty}'. "
                f"Must be one of: {self.VALID_DIFFICULTIES}"
            )
        self._difficulty = difficulty

    def get_difficulty(self):
        """Return current difficulty. Returns: str"""
        return self._difficulty

    # --------------------------------------------------
    # Class methods
    # --------------------------------------------------

    @classmethod
    def set_default_unit(cls, unit):
        """
        Change the platform default unit.

        Parameters:
            unit (str) : 'km' or 'mi'.

        Raises:
            ValueError: If unit is invalid.

        Returns: None
        """
        unit = unit.lower().strip()
        if unit not in Distance.VALID_UNITS:
            raise ValueError(f"Invalid unit '{unit}'.")
        cls.default_unit = unit

    @classmethod
    def from_dict(cls, data):
        """
        Alternate constructor — build a Trail from a dict.
        Note: cls must be a concrete subclass, not Trail itself.

        Parameters:
            data (dict) : Keys: id, name, distance, unit,
                          elevation_gain_m, difficulty.

        Returns:
            Trail subclass instance.
        """
        unit     = data.get('unit', cls.default_unit)
        distance = Distance(data['distance'], unit)
        return cls(
            trail_id         = data['id'],
            name             = data['name'],
            distance         = distance,
            elevation_gain_m = data['elevation_gain_m'],
            difficulty       = data['difficulty']
        )

    # --------------------------------------------------
    # Static validators
    # --------------------------------------------------

    @staticmethod
    def is_valid_difficulty(difficulty):
        """Check difficulty without raising. Returns: bool"""
        return difficulty.lower().strip() in Trail.VALID_DIFFICULTIES

    @staticmethod
    def is_valid_unit(unit):
        """Check unit without raising. Returns: bool"""
        return unit.lower().strip() in Distance.VALID_UNITS

    # --------------------------------------------------
    # Equality by id
    # --------------------------------------------------

    def __eq__(self, other):
        """
        Two trails are equal if they share the same id.

        Parameters:
            other (object) : Object to compare.

        Returns:
            bool: True if same id.
        """
        if not isinstance(other, Trail):
            return NotImplemented
        return self.id == other.id

    # --------------------------------------------------
    # String representations
    # --------------------------------------------------

    def __str__(self):
        return (f"{self.name} [{type(self).__name__}] — "
                f"{self.distance} ({self._difficulty})")

    def __repr__(self):
        return (f"{type(self).__name__}(id={self.id!r}, "
                f"name={self.name!r}, distance={self.distance!r}, "
                f"elevation_gain_m={self.elevation_gain_m!r}, "
                f"difficulty={self._difficulty!r})")


# ======================================================
# Concrete subclasses
# ======================================================

class DayHike(ElevationMixin, RatingMixin, Trail):
    """
    A single-day hiking trail.

    Pacing: 4 km/h (or 2.5 mph) on flat terrain, adjusted
    for elevation gain at +1 hour per 600 m of gain.

    Inherits:
        ElevationMixin.grade_percent()
        RatingMixin.add_rating() / average_rating()
        Trail (all shared attributes and methods)

    MRO: DayHike -> ElevationMixin -> RatingMixin -> Trail
    """

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty):
        """
        Initialise DayHike via super() up the MRO chain.

        Parameters: (same as Trail.__init__)
        Returns: None
        """
        super().__init__(
            trail_id         = trail_id,
            name             = name,
            distance         = distance,
            elevation_gain_m = elevation_gain_m,
            difficulty       = difficulty
        )

    def estimated_time(self):
        """
        Estimate hiking time in hours.

        Formula:
            base_time = distance_km / 4.0
            elev_time = elevation_gain_m / 600.0
            total     = base_time + elev_time

        Returns:
            float: Estimated hours rounded to 2 decimal places.
        """
        dist_km   = (self.distance.magnitude
                     if self.distance.unit == 'km'
                     else self.distance.convert().magnitude)
        base_time = dist_km / 4.0
        elev_time = self.elevation_gain_m / 600.0
        return round(base_time + elev_time, 2)

    def summary(self):
        """
        One-line summary of this day hike.

        Returns:
            str: e.g. 'DayHike: Ridgeline Loop — 8.50 km, ~2.66 h'
        """
        return (f"DayHike: {self.name} — {self.distance}, "
                f"~{self.estimated_time()} h, "
                f"grade {self.grade_percent()}%")


class GuidedDayHike(DayHike):
    """
    A guided day hike — extends DayHike with a guide_name field.

    Adds one further level to the hierarchy (WP-203).
    Overrides summary() to include the guide's name.

    Inherits everything from DayHike, ElevationMixin,
    RatingMixin, and Trail.

    MRO: GuidedDayHike -> DayHike -> ElevationMixin
         -> RatingMixin -> Trail -> ABC -> object
    """

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty, guide_name):
        """
        Initialise GuidedDayHike with an extra guide_name field.

        Parameters:
            guide_name (str) : Name of the trail guide.
            (all others same as DayHike)

        Returns: None
        """
        # Call super() to handle all Trail/Mixin initialisation
        super().__init__(
            trail_id         = trail_id,
            name             = name,
            distance         = distance,
            elevation_gain_m = elevation_gain_m,
            difficulty       = difficulty
        )
        # Additional field specific to GuidedDayHike
        self.guide_name = guide_name

    def summary(self):
        """
        Override summary() to include guide name.
        Calls super().summary() and extends it.

        Returns:
            str: e.g. 'GuidedDayHike: ... | Guide: Jane Smith'
        """
        base = super().summary().replace("DayHike", "GuidedDayHike")
        return f"{base} | Guide: {self.guide_name}"


class BackpackingRoute(ElevationMixin, RatingMixin, Trail):
    """
    A multi-day backpacking route.

    Pacing: slower than day hiking — 3 km/h base pace due
    to heavy pack weight, plus +1 hour per 400 m elevation.

    Parameters:
        num_days (int) : Number of days for the route.
        (all others same as Trail)
    """

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty, num_days=1):
        """
        Initialise BackpackingRoute.

        Parameters:
            num_days (int) : Days planned for the route.
            (others same as Trail)

        Returns: None
        """
        super().__init__(
            trail_id         = trail_id,
            name             = name,
            distance         = distance,
            elevation_gain_m = elevation_gain_m,
            difficulty       = difficulty
        )
        self.num_days = num_days

    def estimated_time(self):
        """
        Estimate time in hours for the full route.

        Formula:
            base_time = distance_km / 3.0
            elev_time = elevation_gain_m / 400.0
            total     = base_time + elev_time

        Returns:
            float: Estimated hours rounded to 2 decimal places.
        """
        dist_km   = (self.distance.magnitude
                     if self.distance.unit == 'km'
                     else self.distance.convert().magnitude)
        base_time = dist_km / 3.0
        elev_time = self.elevation_gain_m / 400.0
        return round(base_time + elev_time, 2)

    def summary(self):
        """
        One-line summary of this backpacking route.

        Returns:
            str: Description including num_days.
        """
        return (f"BackpackingRoute: {self.name} — {self.distance}, "
                f"~{self.estimated_time()} h over {self.num_days} days, "
                f"grade {self.grade_percent()}%")


class TrailRun(RatingMixin, Trail):
    """
    A trail running route.

    Pacing: 10 km/h base pace (running), with +30 min per
    500 m elevation gain.

    Does NOT use ElevationMixin (runners track time, not grade).
    Overrides difficulty display — trail runners use their own
    scale: adds 'technical' as an alias for 'hard'.
    """

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty):
        """
        Initialise TrailRun.

        Parameters: (same as Trail)
        Returns: None
        """
        super().__init__(
            trail_id         = trail_id,
            name             = name,
            distance         = distance,
            elevation_gain_m = elevation_gain_m,
            difficulty       = difficulty
        )

    def estimated_time(self):
        """
        Estimate running time in hours.

        Formula:
            base_time = distance_km / 10.0
            elev_time = elevation_gain_m / 500.0 * 0.5
            total     = base_time + elev_time

        Returns:
            float: Estimated hours rounded to 2 decimal places.
        """
        dist_km   = (self.distance.magnitude
                     if self.distance.unit == 'km'
                     else self.distance.convert().magnitude)
        base_time = dist_km / 10.0
        elev_time = (self.elevation_gain_m / 500.0) * 0.5
        return round(base_time + elev_time, 2)

    def summary(self):
        """
        One-line summary of this trail run.

        Returns:
            str: Description with running-specific pacing.
        """
        return (f"TrailRun: {self.name} — {self.distance}, "
                f"~{self.estimated_time()} h "
                f"({self._difficulty})")


# ======================================================
# FakeTrail — duck-typed, inherits nothing (WP-206)
# ======================================================

class FakeTrail:
    """
    A duck-typed trail for testing the polymorphic loop.
    Inherits from nothing — just implements estimated_time()
    and summary() so it works alongside real Trail subclasses.

    Used to verify the polymorphic loop doesn't require
    isinstance checks.
    """

    def __init__(self, name):
        """
        Parameters:
            name (str) : Name for this fake trail.

        Returns: None
        """
        self.name = name

    def estimated_time(self):
        """
        Returns a fixed estimated time for testing.

        Returns:
            float: Always 1.0 hour.
        """
        return 1.0

    def summary(self):
        """
        Returns a fake summary string.

        Returns:
            str: Fixed test summary.
        """
        return f"FakeTrail: {self.name} — test only, ~1.0 h"

    def __str__(self):
        return f"FakeTrail({self.name!r})"
