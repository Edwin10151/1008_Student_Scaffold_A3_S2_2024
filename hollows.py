from __future__ import annotations

from betterbst import BetterBST
from data_structures.bst import BSTInOrderIterator, BinarySearchTree
from data_structures.hash_table import LinearProbeTable
from data_structures.heap import MaxHeap
from data_structures.linked_queue import LinkedQueue
from data_structures.linked_stack import LinkedStack
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
            Best Case Complexity: O(n log n), where n is the number of treasures in the hollow
                Explanation: The method processes each treasure in the hollow to create a list of tuples containing the negative value-to-weight ratios and corresponding treasures so that we can retrieve the maximum value-to-weight ratio first after we negate it again.
                This operation takes O(n) time since every treasure must be iterated over. 
                After forming this list, the elements are inserted into a BetterBST, which, on average, has a logarithmic insertion complexity for each treasure. 
                Since there are n treasures, the overall complexity for building the BetterBST is O(n log n). Therefore, the best case complexity is O(n log n).
            Worst Case Complexity: O(n log n), where n is the number of treasures in the hollow
                Explanation: The reasoning remains the same as in the best case. Each treasure is processed exactly once to create the list, 
                and each insertion into the BetterBST takes logarithmic time. Consequently, even in the worst-case scenario, the overall complexity does not exceed O(n log n).
        
        Complexity requirements for full marks:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        elements = [(-treasure.value / treasure.weight, treasure) for treasure in self.treasures]
        self.treasures = BetterBST(elements)
        
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
            Best Case Complexity: O(log(n)), where n is the number of treasures in the hollow 
                Explanation: In the best-case scenario, the optimal treasure is found quickly during the in-order traversal of the BetterBST. 
                If the first treasure examined meets the weight requirement, it can be removed with a logarithmic time complexity operation in the binary search tree. 
                Thus, the best-case complexity is O(log n).
            Worst Case Complexity: O(n), where n is the number of treasures in the hollow 
                Explanation: The worst case occurs when all treasures must be examined during the in-order traversal before the suitable treasure is found. 
                This traversal requires visiting every node in the tree, leading to a linear complexity of O(n). Furthermore, if the optimal treasure is identified, 
                deleting it from the tree involves a logarithmic operation, which does not change the overall linear complexity in this case.


        Complexity requirements for full marks:
            Best Case Complexity: O(log(n))
            Worst Case Complexity: O(n)
            n is the number of treasures in the hollow 
        """
        optimal_treasure = None

        # Find the first treasure that meets the weight requirement
        for node in BSTInOrderIterator(self.treasures.root):
            current = node.item
            if current.weight <= backpack_capacity:
                optimal_treasure = current
                break

        # Remove the optimal treasure from the BetterBST
        if optimal_treasure:
            del self.treasures[-optimal_treasure.value / optimal_treasure.weight]
            
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
            Best Case Complexity: O(n), where n is the number of treasures in the hollow.
                Explanation: In the best-case scenario, if all treasures are processed in a straightforward manner, the time complexity remains linear. 
                The method generates a list of tuples where each tuple contains the value-to-weight ratio and the corresponding treasure. 
                The process of creating this list takes O(n) time, where n is the number of treasures. 
                The heapification step, where the list is converted into a heap, also operates in linear time relative to the number of elements.
            Worst Case Complexity: O(n), where n is the number of treasures in the hollow
                Explanation: Similarly, the worst-case complexity is also O(n) for the same reasons. 
                The method processes each treasure once, resulting in a linear time complexity regardless of the order of treasures or their attributes.

        Complexity requirements for full marks:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
            Where n is the number of treasures in the hollow
        """
        # Create a MaxHeap from the treasures
        elements = [(treasure.value / treasure.weight, treasure) for treasure in self.treasures]
        self.treasures = MaxHeap.heapify(elements)

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
            Best Case Complexity: O(log n), where n is the number of treasures in the hollow
                Explanation: The best-case scenario occurs when the first treasure with highest value/weight ratio retrieved from the heap via get_max() meets the weight requirement. 
                In this case, the method immediately identifies the optimal treasure, and only one heap operation (which is O(log n) complexity) is performed. 
                The loop exits without further checks, making the best-case complexity O(log n).
            
            Worst Case Complexity: O(n log n), where n is the number of treasures in the hollow
                Explanation: The worst-case scenario arises when none of the treasures meet the weight condition until the very last treasure is checked. 
                In this situation, the method calls get_max() for each treasure in the heap, which has a logarithmic time complexity in max heap.
                If n treasures are checked, the complexity sums to O(n log n). 
                Furthermore, if all treasures are heavier than the backpack capacity stored in LinkedQueue, they must be served from LinkedQueue and reinserted into the heap, which also contributes to the O(n log n) complexity.
                If no optimal treasure is found until the last element, the loop runs n times, resulting in O(n log n) complexity.

        Complexity requirements for full marks:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """

        optimal_treasure = None
        remaining_elements = LinkedQueue()

        # Find the optimal treasure
        while len(self.treasures) > 0:
            ratio, treasure = self.treasures.get_max()
            if treasure.weight <= backpack_capacity:
                optimal_treasure = treasure
                break
            else:
                remaining_elements.append((ratio, treasure))

        # Reinsert the remaining treasures served from LinkedQueue into the heap
        while not remaining_elements.is_empty():
            self.treasures.add(remaining_elements.serve())

        return optimal_treasure

    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)
