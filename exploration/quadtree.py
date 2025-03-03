from typing import NamedTuple
from shapely.geometry import Polygon, box, Point


class QuadtreeError(Exception):
    """Exception used within Quadtree for unexpected cases"""


class BBox(NamedTuple):
    """Named tuple for storing bounding box data."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float


# Maximum depth of a quadtree.
# Do not subdivide nodes if depth exceeds this value.
MAX_DEPTH = 8


class Quadtree:
    """
    Class that represents a node in the quadtree.

    Each node has:
        - bounding box (bbox)
        - capacity
        - depth (first node is depth=0, children would be depth=1, etc.)
        - either children OR polygons
    """

    def __init__(self, bbox: BBox, capacity: int, depth: int = 0):
        self.bbox = bbox
        self.node = box(bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y)
        self.capacity = capacity
        self.depth = depth
        self.polygons = {}
        self.children = []

    def is_split(self) -> bool:
        """
        Check if this node in the quadtree is split.

        Returns:
            True if split, False otherwise.
        """
        if self.children and self.polygons:
            raise QuadtreeError("polygons and children on same node")
        if len(self.children) not in (4, 0):
            raise QuadtreeError("a node must always have 0 or 4 children")
        return bool(self.children)

    def __repr__(self) -> str:
        """
        Return a view of the interior of the node.

        It is not tested, feel free to modify this function however you like.
        """
        if self.is_split():
            return f"Quadtree{list(self.children)}"

        return f"Quadtree(polygons={len(self.polygons)})"

    def split(self):
        '''
        Splits node into four child nodes of equal proportion
        '''
        child_depth = self.depth + 1
        mix, miy, max, may = self.node.bounds

        # calculate midpoints
        midx = mid(mix, max)
        midy = mid(miy, may)

        # give birth to the four children
        self.children.append(Quadtree(BBox(mix, midy, midx, may),
                                      self.capacity, child_depth))
        self.children.append(Quadtree(BBox(midx, midy, max, may),
                                      self.capacity, child_depth))
        self.children.append(Quadtree(BBox(mix, miy, midx, midy),
                                      self.capacity, child_depth))
        self.children.append(Quadtree(BBox(midx, miy, max, midy),
                                      self.capacity, child_depth))

    def add_polygon(self, id: str, polygon: Polygon) -> bool:
        '''
        Adds new polygon to Quadtree node recursively, returns True if polygon
        added successfully
        '''
        # case 1: poly is not in node
        if not polygon.intersects(self.node):
            return False

        # case 2: poly is in node, node is not split
        if not self.is_split():

            # add poly if capacity not met or max recursion depth reached
            if (len(self.polygons) < self.capacity) or (self.depth >=
                                                        MAX_DEPTH):
                self.polygons[id] = polygon
                return True

            # otherwise split node into children
            self.split()

            # add polys back to newly born children
            for child in self.children:

                # move pre-existing polys
                for key, value in self.polygons.items():
                    child.add_polygon(key, value)

                # add main poly
                child.add_polygon(id, polygon)

            # empty the polygons dict
            self.polygons = {}
            return True

        # case 3: node is split, try adding polygon to each child
        for child in self.children:
            child.add_polygon(id, polygon)

    def match(self, point: Point) -> list[str]:
        '''
        Returns list of all polygons in self (or self.children) that
        contain point
        '''
        poly_ids = []

        # base case 1: if point not in node bounding box, return []
        if not self.node.contains(point):
            return poly_ids

        # base case 2: if node not split, check all polygons for point
        if not self.is_split():
            for id, poly in self.polygons.items():
                if poly.contains(point):
                    poly_ids.append(id)
            return poly_ids

        # recursive case: if node split, check children
        for child in self.children:
            poly_ids += child.match(point)
        return poly_ids


def mid(x, y):
    '''Helper: finds midpoint between two values'''
    return (x + y)/2


def quadtree_spatial_join(
    facilities: list,
    tracts: list,
) -> list[tuple[str, str]]:
    '''Performs spatial join on a list of facilities and a list of tracts'''
    # These variables should be passed in to your root quadtree.
    #
    # Bounding box of Illinois, should be used as bounds of your
    # root quadtree.
    il_bbox = BBox(-91.513079, 36.970298, -87.494756, 42.508481)
    capacity = 10
    quadtree = Quadtree(il_bbox, capacity)

    # build quadtree
    for tract in tracts:
        quadtree.add_polygon(tract.id, tract.polygon)

    # do spatial join
    lst = []
    for facility in facilities:
        point = Point(facility.longitude, facility.latitude)
        tract = quadtree.match(point)
        if len(tract) > 0:
            lst.append((facility.plantname, tract[0]))
    return lst
