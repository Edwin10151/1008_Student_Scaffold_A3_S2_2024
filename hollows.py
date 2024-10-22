from __future__ import annotations

from betterbst import BetterBST
from data_structures.bst import BinarySearchTree
from data_structures.hash_table import LinearProbeTable
from data_structures.heap import MaxHeap
"""
Ensure you have read the introduction and task 1 and understand what 
is prohibited in this task.
This includes:
The ban on inbuilt sort methods .sort() or sorted() in this task.
And ensure your treasure data structure is not banned.

"""
from abc import ABC, abstractmethod
from typing import List

from config import Tiles
from treasure import Treasure, generate_treasures


class Hollow(ABC):
    """
    DO NOT MODIFY THIS CLASS
    Mystical troves of treasure that can be found in the maze
    There are two types of hollows that can be found in the maze:
    - Spooky Hollows: Each of these hollows contains unique treasures that can be found nowhere else in the maze.
    - Mystical Hollows: These hollows contain a random assortment of treasures like the spooky hollow however all mystical hollows are connected, so if you remove a treasure from one mystical hollow, it will be removed from all other mystical hollows.
    """

    # DO NOT MODIFY THIS ABSTRACT CLASS
    """
    Initialises the treasures in this hollow
    """

    def __init__(self) -> None:
        self.treasures = self.gen_treasures()
        self.restructure_hollow()

    @staticmethod
    def gen_treasures() -> List[Treasure]:
        """
        This is done here, so we can replace it later on in the auto marker.
        This method contains the logic to generate treasures for the hollows.

        Returns:
            List[Treasure]: A list of treasures that can be found in the maze
        """
        return generate_treasures()

    @abstractmethod
    def restructure_hollow(self):
        pass

    @abstractmethod
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        pass

    def __len__(self) -> int:
        """
        After the restructure_hollow method is called, the treasures attribute should be updated
        don't create an additional attribute to store the number of treasures in the hollow.
        """
        return len(self.treasures)


class SpookyHollow(Hollow):

    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(n log n), Inserting elements into the BinarySearchTree: O(n log n)
            Worst Case Complexity: O(n log n), Inserting elements into the BinarySearchTree: O(n log n)

        Complexity requirements for full marks:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        elements = [(treasure.value / treasure.weight, treasure) for treasure in self.treasures]
        self.treasure_bst = BetterBST(elements)
        
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow 
        Takes the treasure which has the greatest value / weight ratio 
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(log (n)), Finding the maximum element: O(log n), Removing the element: O(log n)
            Worst Case Complexity: O(log n) in the best case and O(n) in the worst case (if we need to traverse the entire tree, search method even in balanced tree also has O(n) complexity)

        Complexity requirements for full marks:
            Best Case Complexity: O(log(n))
            Worst Case Complexity: O(n)
            n is the number of treasures in the hollow 
        """
        optimal_treasure = None

        # Find the maximum ratio that is less than or equal to the backpack capacity
        current = self.treasure_bst.root
        while current:
            if current.item.weight <= backpack_capacity:
                optimal_treasure = current.item
                if current.right:
                    current = current.right
                else:
                    break
            else:
                current = current.left

        if optimal_treasure:
            del self.treasure_bst[optimal_treasure.value / optimal_treasure.weight]
            self.treasures = [t for t in self.treasures if t != optimal_treasure]

        return optimal_treasure

    def __str__(self) -> str:
        return Tiles.SPOOKY_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)


class MysticalHollow(Hollow):

    def restructure_hollow(self):
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task! 

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: TODO
            Worst Case Complexity: TODO

        Complexity requirements for full marks:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
            Where n is the number of treasures in the hollow
        """
        # self.treasure_heap = MaxHeap(len(self.treasures))
        # for treasure in self.treasures:
        #     ratio = treasure.value / treasure.weight
        #     self.treasure_heap.add((ratio, treasure))
        elements = [(treasure.value / treasure.weight, treasure) for treasure in self.treasures]
        self.treasure_heap = MaxHeap.heapify(elements)

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow 
        Takes the treasure which has the greatest value / weight ratio 
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: Uses the MaxHeap to retrieve the treasure with the highest value/weight ratio that can be carried.
                                If no viable treasure is found, the remaining elements are restored to the heap using heapify.
                                Updates the treasures list to remove the selected treasure.
                                Complexity: O(log n) for the best case and O(n log n) for the worst case.
            Worst Case Complexity: TODO

        Complexity requirements for full marks:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        optimal_treasure = None
        remaining_elements = []

        while len(self.treasure_heap) > 0:
            ratio, treasure = self.treasure_heap.get_max()
            if treasure.weight <= backpack_capacity:
                optimal_treasure = treasure
                break
            else:
                remaining_elements.append((ratio, treasure))

        # Restore the heap using heapify
        if remaining_elements:
            self.treasure_heap = MaxHeap.heapify(remaining_elements)

        if optimal_treasure:
            self.treasures = [t for t in self.treasures if t != optimal_treasure]
        return optimal_treasure

    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)
