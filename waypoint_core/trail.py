"""
waypoint_core/trail.py
-----------------------
Trail and Itinerary classes for the Waypoint trail-finder.

Trail  — represents a single hiking trail with a name,
         distance, elevation gain, and difficulty rating.

Itinerary — an ordered collection of Trail objects that
            computes a total distance.
"""

from waypoint_core.distance import Distance


class Trail:
    """
    Represents a hiking trail.

    Class variable:
        default_unit (str) : Platform default unit for new
                             trails. Either 'km' or 'mi'.
                             Defaults to 'km'.

    Instance attributes:
        id             (int)      : Unique identifier.
        name           (str)      : Trail name.
        distance       (Distance) : Trail length.
        elevation_gain_m (float)  : Elevation gain in metres.
        _difficulty    (str)      : Private — access via
                                    set/get_difficulty().
    """

    # ---- Class variable: platform default unit ----
    default_unit = 'km'

    # Allowed difficulty levels
    VALID_DIFFICULTIES = ('easy', 'moderate', 'hard', 'expert')

    def __init__(self, trail_id, name, distance,
                 elevation_gain_m, difficulty):
        """
        Initialise a Trail, validating distance and difficulty.

        Parameters:
            trail_id         (int)      : Unique trail ID.
            name             (str)      : Trail name.
            distance         (Distance) : Trail length.
            elevation_gain_m (float)    : Elevation in metres.
            difficulty       (str)      : One of easy/moderate/
                                          hard/expert.

        Raises:
            ValueError: If difficulty is not in VALID_DIFFICULTIES.
            TypeError:  If distance is not a Distance instance.

        Returns: None
        """
        # Validate distance type
        if not isinstance(distance, Distance):
            raise TypeError(
                "distance must be a Distance instance."
            )

        # Validate difficulty using the class method validator
        self.set_difficulty(difficulty)

        # Set all attributes
        self.id               = trail_id
        self.name             = name
        self.distance         = distance
        self.elevation_gain_m = float(elevation_gain_m)

    # --------------------------------------------------
    # Difficulty — guarded setter / getter
    # --------------------------------------------------

    def set_difficulty(self, difficulty):
        """
        Set the difficulty, rejecting invalid values.

        Parameters:
            difficulty (str) : Must be one of
                               easy/moderate/hard/expert.

        Raises:
            ValueError: If difficulty is not valid.

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
        """
        Read the current difficulty level.

        Returns:
            str: The difficulty string.
        """
        return self._difficulty

    # --------------------------------------------------
    # Class method: change the default unit
    # --------------------------------------------------

    @classmethod
    def set_default_unit(cls, unit):
        """
        Change the platform's default distance unit.
        Affects newly created trails only.

        Parameters:
            unit (str) : 'km' or 'mi'.

        Raises:
            ValueError: If unit is not 'km' or 'mi'.

        Returns: None
        """
        unit = unit.lower().strip()
        if unit not in Distance.VALID_UNITS:
            raise ValueError(
                f"Invalid unit '{unit}'. Must be 'km' or 'mi'."
            )
        cls.default_unit = unit

    # --------------------------------------------------
    # Class method: alternate constructor from dict
    # --------------------------------------------------

    @classmethod
    def from_dict(cls, data):
        """
        Build a Trail from an API-shaped dictionary.

        Expected keys:
            'id'               (int)
            'name'             (str)
            'distance'         (float)
            'unit'             (str)   optional, defaults to
                                       cls.default_unit
            'elevation_gain_m' (float)
            'difficulty'       (str)

        Parameters:
            data (dict) : Dictionary with trail fields.

        Returns:
            Trail: A fully constructed Trail instance.

        Example:
            Trail.from_dict({
                'id': 1, 'name': 'Ridgeline Loop',
                'distance': 8.5, 'unit': 'km',
                'elevation_gain_m': 320, 'difficulty': 'hard'
            })
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
        """
        Check whether a difficulty string is valid without
        raising an exception.

        Parameters:
            difficulty (str) : Difficulty string to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        return difficulty.lower().strip() in Trail.VALID_DIFFICULTIES

    @staticmethod
    def is_valid_unit(unit):
        """
        Check whether a unit string is valid.

        Parameters:
            unit (str) : Unit string to check.

        Returns:
            bool: True if 'km' or 'mi', False otherwise.
        """
        return unit.lower().strip() in Distance.VALID_UNITS

    # --------------------------------------------------
    # Equality — two trails with same id are equal
    # (WP-104: allows de-duplication on import)
    # --------------------------------------------------

    def __eq__(self, other):
        """
        Two Trail objects are equal if they share the same id,
        regardless of any other attribute differences.

        Parameters:
            other (object) : Object to compare against.

        Returns:
            bool: True if both are Trail instances with same id.
        """
        if not isinstance(other, Trail):
            return NotImplemented
        return self.id == other.id

    # --------------------------------------------------
    # String representations (stretch goal)
    # --------------------------------------------------

    def __str__(self):
        """
        Human-readable representation of the trail.

        Returns:
            str: e.g. 'Ridgeline Loop — 8.50 km (hard)'
        """
        return (f"{self.name} — {self.distance} "
                f"({self._difficulty})")

    def __repr__(self):
        """
        Developer representation.

        Returns:
            str: e.g. "Trail(id=1, name='Ridgeline Loop', ...)"
        """
        return (f"Trail(id={self.id!r}, name={self.name!r}, "
                f"distance={self.distance!r}, "
                f"elevation_gain_m={self.elevation_gain_m!r}, "
                f"difficulty={self._difficulty!r})")


# ======================================================
# Itinerary — HAS-A list of Trail objects
# ======================================================

class Itinerary:
    """
    An ordered collection of Trail objects for a trip.

    Provides:
        add_trail()       — append a trail to the list.
        total_distance()  — sum of all trail distances,
                            returned in the platform default unit.

    Parameters: None (starts empty)
    """

    def __init__(self):
        """
        Initialise an empty Itinerary with its own private
        trail list. Adding to one Itinerary never changes
        another.

        Returns: None
        """
        # Private list — each Itinerary owns its own copy
        self._trails = []

    def add_trail(self, trail):
        """
        Append a Trail to this itinerary.

        Parameters:
            trail (Trail) : The trail to add.

        Raises:
            TypeError: If trail is not a Trail instance.

        Returns: None
        """
        if not isinstance(trail, Trail):
            raise TypeError(
                "Only Trail instances can be added to an Itinerary."
            )
        self._trails.append(trail)

    def total_distance(self):
        """
        Calculate the total distance of all trails in this
        itinerary. All distances are converted to the current
        platform default unit (Trail.default_unit) before
        summing.

        Returns:
            Distance: Total distance in the platform default unit.
                      Returns Distance(0, default_unit) for
                      an empty itinerary.
        """
        unit  = Trail.default_unit
        total = 0.0

        for trail in self._trails:
            d = trail.distance
            # Convert to default unit if needed
            if d.unit != unit:
                d = d.convert()
            total += d.magnitude

        return Distance(total, unit)

    def __str__(self):
        """
        Human-readable summary of the itinerary.

        Returns:
            str: Trail names and total distance.
        """
        if not self._trails:
            return "Itinerary: (empty)"
        trail_names = ", ".join(t.name for t in self._trails)
        return (f"Itinerary [{len(self._trails)} trails]: "
                f"{trail_names} | "
                f"Total: {self.total_distance()}")
