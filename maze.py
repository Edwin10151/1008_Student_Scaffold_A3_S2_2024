from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from config import Directions, Tiles
from hollows import Hollow, MysticalHollow, SpookyHollow
from treasure import Treasure


class Position:
    def __init__(self, row: int, col: int) -> None:
        """
        Args:
            row(int): Row number in this maze cell position
            col(int): Column number in this maze cell position
        """
        self.row: int = row
        self.col: int = col

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and value.row == self.row and value.col == self.col

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass
class MazeCell:
    tile: str | Hollow
    position: Position
    visited: bool = False

    def __str__(self) -> str:
        return str(self.tile)

    def __repr__(self) -> str:
        return f"'{self.tile}'"


class Maze:
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }

    def __init__(self, start_position: Position, end_positions: List[Position], walls: List[Position], hollows: List[tuple[Hollow, Position]], rows: int, cols: int) -> None:
        """
        Constructs the maze you should never be interacting with this method.
        Please take a look at `load_maze_from_file` & `sample1`

        Args:
            start_position(Position): Starting position in the maze.
            end_positions(List[Position]): End positions in the maze.
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            rows(int): Number of rows in the maze.
            cols(int): Number of columns in the maze.

        Complexity:
            Best Case Complexity: O(_create_grid)
            Worst Case Complexity: O(_create_grid)
        """
        self.start_position: Position = start_position
        self.end_positions: List[Position] = end_positions
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[MazeCell]] = self._create_grid(walls, hollows, end_positions)

    def _create_grid(self, walls: List[Position], hollows: List[(Hollow, Position)], end_positions: List[Position]) -> List[List[MazeCell]]:
        """
        Args:
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            end_positions(List[Position]): End positions in the maze.

        Return:
            List[MazeCell]: The generated maze grid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        grid: List[List[MazeCell]] = [[MazeCell(' ', Position(i, j))
                                       for j in range(self.cols)] for i in range(self.rows)]
        grid[self.start_position.row][self.start_position.col] = MazeCell(
            Tiles.START_POSITION.value, self.start_position)
        for wall in walls:
            grid[wall.row][wall.col].tile = Tiles.WALL.value
        for hollow, pos in hollows:
            grid[pos.row][pos.col].tile = hollow
        for end_position in end_positions:
            grid[end_position.row][end_position.col].tile = Tiles.EXIT.value
        return grid

    @staticmethod
    def validate_maze_file(maze_name: str) -> None:
        """
        Mazes must have the following:
        - A start position (P)
        - At least one exit (E)
        - All rows must have the same number of columns
        - Tiles are representations can be found in config.py
        - At least one treasure

        Args:
            maze_name(str): The name of the maze.

        Raises:
            ValueError: If maze_name is invalid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            Assuming dictionary operations can be done on O(1) time.
        """
        tile_count: dict[str, int] = {}
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            cols: int = len(lines[0].strip())
            for line in lines:
                if len(line.strip()) != cols:
                    raise ValueError(f"Uneven columns in {maze_name} ensure all rows have the same number of columns")
                # Check tiles
                for tile in line.strip():
                    if tile not in tile_count:
                        tile_count[tile] = 1
                    else:
                        tile_count[tile] += 1
        if 'P' not in tile_count or 'E' not in tile_count:
            raise ValueError(f"Missing start or end position in {maze_name}")

        if tile_count['P'] > 1:
            raise ValueError(f"Multiple start positions found in {maze_name}")

        # Check we have at least one treasure
        if not (Tiles.SPOOKY_HOLLOW.value in tile_count or Tiles.MYSTICAL_HOLLOW.value in tile_count):
            raise ValueError(f"No treasures found in {maze_name}")

        valid_types: List[str] = [tile.value for tile in Tiles]
        invalid_tiles: List[str] = [tile for tile in tile_count if tile not in valid_types]
        if invalid_tiles:
            raise ValueError(f"Invalid tile(s) found in {maze_name} ({invalid_tiles})")

    @classmethod
    def load_maze_from_file(cls, maze_name: str) -> Maze:
        """
        Args:
            maze_name(str): The maze name to load the maze from.

        Return:
            Maze: The newly created maze instance.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            For small mazes we assume the lists we not need to resize.
        """
        cls.validate_maze_file(maze_name)
        end_positions, walls, hollows = [], [], []
        mystical_hollow: MysticalHollow = MysticalHollow()
        start_position: Position | None = None
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())
            for i, line in enumerate(lines):
                for j, tile in enumerate(line.strip()):
                    if tile == Tiles.START_POSITION.value:
                        start_position: Position = Position(i, j)
                    elif tile == Tiles.EXIT.value:
                        end_positions.append(Position(i, j))
                    elif tile == Tiles.WALL.value:
                        walls.append(Position(i, j))
                    elif tile == Tiles.SPOOKY_HOLLOW.value:
                        hollows.append((SpookyHollow(), Position(i, j)))
                    elif tile == Tiles.MYSTICAL_HOLLOW.value:
                        hollows.append((mystical_hollow, Position(i, j)))
        assert start_position is not None
        return Maze(start_position, end_positions, walls, hollows, rows, cols)

    def is_valid_position(self, position: Position) -> bool:
        """
        Checks if the position is within the maze and not blocked by a wall.

        Args:
            position (Position): The position to check.

        Returns:
            bool - True if the position is within the maze and not blocked by a wall.

        Complexity:
            Best Case Complexity: O(1).  
                Explanation: In the best-case scenario, the provided position is immediately found to be out of bounds. 
                This situation occurs when either the position.row is less than 0 or greater than or equal to the number of rows in the maze (self.rows), 
                or when the position.col is less than 0 or greater than or equal to the number of columns (self.cols).
            Worst Case Complexity: O(1). 
                Explanation: In the worst-case scenario, the provided position is valid, meaning it lies within the maze boundaries. 
                This condition allows the function to proceed to check the status of the corresponding cell in the grid. 
                Since `self.grid` is a list of lists, accessing an element by its indices (i.e., `self.grid[position.row][position.col]`) is a constant-time operation, O(1).
                This is because lists in Python allow for direct indexing, ensuring that retrieving any element is performed in constant time regardless of the size of the grid.
        """
        if 0 <= position.row < self.rows and 0 <= position.col < self.cols:
            cell = self.grid[position.row][position.col]
            return cell.tile != Tiles.WALL.value and not cell.visited
        return False

    def get_available_positions(self, current_position: Position) -> List[Position]:
        """
        Returns a list of all the new possible you can move to from your current position.

        Args:
            current_position (Position): Your current position.

        Returns:
            List[Position] - A list of all the new possible you can move to from your current position.

        Complexity:
            Best Case Complexity: O(1).            
                Explanation: In the best-case scenario, if the current position has no valid movements (for example, it is surrounded by walls), 
                the function will quickly evaluate each of the four possible directions but will find that none are valid. 
                Therefore, it will return an empty list immediately without performing any further checks or operations. 
                This results in a constant time complexity, O(1).
            Worst Case Complexity: O(1)
                Explanation: The function checks four possible directions (up, down, left, and right). Since the number of directions is fixed 
                and does not vary with the size of the maze, the time taken to evaluate all potential moves remains constant. 
                The method iterates through `Maze.directions.items()`, which is assumed to be constant, thus making this part of the process O(1). 
                Each direction check involves calling `is_valid_position`, which also operates in O(1) time as previously analyzed. 
                Consequently, regardless of the current position or the size of the maze, the overall complexity remains constant, O(1).
        """
        available_positions = []
        for direction, (delta_row, delta_col) in Maze.directions.items():
            new_position = Position(current_position.row + delta_row, current_position.col + delta_col)
            if self.is_valid_position(new_position):
                available_positions.append(new_position)
        return available_positions

        
    def find_way_out(self) -> List[Position] | None:
        """
        Finds a way out of the maze in some cases there may be multiple exits
        or no exits at all.

        Returns:
            List[Position]: If there is a way out of the maze, 
            the path will be made up of the coordinates starting at 
            your original starting point and ending at the exit.

            None: Unable to find a path to the exit, simply return None.

        Complexity:
            Best Case Complexity: O(1).
                Explanation: The best-case scenario occurs when the starting position is adjacent to an exit, allowing 
                the method to quickly determine the path with minimal checks, resulting in constant time complexity.

            Worst Case Complexity: O(m * n), where m is the number of rows and n is the number of columns in the maze.
                Explanation: The worst-case scenario arises from the depth-first search (DFS) traversing the entire maze.
                The DFS may need to explore all vertices (V) and edges (E) in the maze. For a grid of size m rows by n columns,
                the total number of cells (vertices) is m * n. Each cell may connect to its neighboring cells, leading to a total of 
                approximately O(m * n) for the overall complexity as the DFS explores all potential paths until it finds an exit or exhausts all options.
        """
        start: Position = self.start_position
        path = []
        if self._dfs(start, path):
            return path
        return None

    def _dfs(self, current_position: Position, path: List[Position]) -> bool:
        """
        Depth-first search to find a path to the exit.

        Args:
            current_position (Position): The current position.
            path (List[Position]): The path taken so far.

        Returns:
            bool: True if a path to the exit is found, False otherwise.

        Complexity:
            Best Case Complexity: O(1).
                Explanation: The best-case scenario occurs if the exit is found immediately from the current position,
                allowing the function to return after only a few checks, resulting in constant time complexity.

            Worst Case Complexity: O(V + E), where V is the total number of cells (vertices) and E is the total number of connections (edges) in the maze.
                Explanation: In the worst case, the DFS will potentially explore every vertex (V) and edge (E) in the maze.
                For a grid-like structure, V corresponds to the total number of cells (m * n), and E represents the connections
                between these cells. Since the DFS can explore every cell and its connections, the complexity is driven by 
                the total number of cells and their relationships, leading to O(V + E) complexity.
        """
        if not self.is_valid_position(current_position):
            return False
        # Mark the current cell as visited
        cell = self.grid[current_position.row][current_position.col]
        cell.visited = True
        path.append(current_position)
        if cell.tile == Tiles.EXIT.value:
            return True
    
        for next_position in self.get_available_positions(current_position):
            if self._dfs(next_position, path):
                return True
        # Backtrack: unmark the cell and remove it from the path
        path.pop()
        # cell.visited = False
        return False

    def take_treasures(self, path: List[MazeCell], backpack_capacity: int) -> List[Treasure] | None:
        """
        You must take the treasures in the order they appear in the path selecting treasures
        that have the highest value / weight ratio.
        Remember the total of treasures cannot exceed backpack_capacity, which means
        Individual treasures cannot exceed this value either.

        Should there be no treasures that are viable please return an empty list.

        You do not have to validate the path, it is guaranteed to be a valid path.

        Args:
            path (List[MazeCell]): The path you took to reach the exit.
            backpack_capacity (int): The maximum weight you can carry.

        Returns:
            List[Treasure] - List of the most optimal treasures.
            None - If there are no treasures to take.

        Complexity:
            Best Case Complexity: O(n log n), where n is the number of cells in the path.
                Explanation: In the best-case scenario, the path contains hollows with treasures 
                that can all be taken within the backpack capacity. Each `get_optimal_treasure` 
                call operates in O(log n) time, leading to O(n log n) overall complexity for 
                traversing the path.

            Worst Case Complexity: O(n * m * log n), where n is the number of cells in the path and m is the 
            number of treasures in the hollows.
                Explanation: This worst-case scenario occurs when each hollow contains multiple treasures,
                and none of the treasures meet the weight condition until the last one is checked. 
                For each hollow (n cells), if the `get_optimal_treasure` method requires checking all 
                treasures (m) and potentially requires O(log n) time to manage the heap, the total 
                complexity sums to O(n * m * log n).
        """
        treasures_taken = []
        remaining_capacity = backpack_capacity

        for cell in path:
            if isinstance(cell.tile, Hollow):
                hollow = cell.tile

                optimal_treasure = hollow.get_optimal_treasure(remaining_capacity)
                if optimal_treasure and optimal_treasure.weight <= remaining_capacity:
                    treasures_taken.append(optimal_treasure)
                    remaining_capacity -= optimal_treasure.weight

        return treasures_taken if treasures_taken else None

    
    def __str__(self) -> str:
        """
        Returns the grid in a human-readable format.

        Complexity:
        Best Case Complexity: O(n) where n is the number of cells in the maze.
        Worst Case Complexity: O(n) where n is the number of cells in the maze.
        """
        my_grid: str = ""
        for row in self.grid:
            my_grid += "" if my_grid == "" else "\n"
            my_grid += str(row)

        return my_grid


def sample1() -> None:
    maze = Maze.load_maze_from_file("sample.txt")
    print(maze)


def sample2() -> None:
    maze = Maze.load_maze_from_file("sample2.txt")
    print(maze)
    # Samples as to how the grid / maze cells work
    r, c = 4, 0  # row 4, col 0
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))
    r, c = 2, 3  # row 2, col 3
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))


if __name__ == "__main__":
    sample1()



