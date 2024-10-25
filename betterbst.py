from __future__ import annotations

from typing import List, Tuple, TypeVar

from algorithms.mergesort import mergesort
from data_structures.bst import BinarySearchTree
from data_structures.linked_stack import LinkedStack
from data_structures.referential_array import ArrayR

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: List[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements list.

        As such you can assume the length of elements to be non-zero.
        The elements list will contain tuples of key, item pairs.

        First sort the elements list and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(List[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(n * log(n)), where n is the number of elements in the list.
                Explanation: The method processes each element in the list to create a sorted list using merge sort by calling '__sort_elements', which has a time complexity of O(n log n). 
                After sorting, the elements are inserted into a balanced binary search tree by calling '__build_balanced_tree', which also has a time complexity of O(n log n) for n elements. 
                Hence, O(n * log(n) + n * log(n)) is still O(n * log(n))
            Worst Case Complexity: O(n * log(n)), where n is the number of elements in the list.
                Explanation: The reasoning remains the same as in the best case. Sorting the elements using merge sort and building the balanced tree both have a time complexity of O(n log n).
        """
        super().__init__()
        new_elements: List[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            list(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(n * log(n)), where n is the number of elements in the list.
                Explanation: The method utilizes merge sort to sort the list of elements. Merge sort operates by recursively dividing the list into halves until each sublist contains a single element. 
                It then merges these sublists back together in sorted order. Merge sort has a time complexity of O(n log n) in the best case because it always performs the same number of operations regardless of the initial order of elements.
            Worst Case Complexity: O(n * log(n)), where n is the number of elements in the list.
                Explanation: Similarly, merge sort has a worst-case time complexity of O(n log n). This occurs when the merging step requires processing each element in every level of recursion. 
                Thus, the overall complexity for this method is consistently O(n log n), both in best and worst cases.
        """
        sorted_keys = mergesort(elements)
        return sorted_keys

    def __build_balanced_tree(self, elements: List[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(n * log(n)), where n is the number of elements in the list.
            Worst Case Complexity: O(n * log(n)), where n is the number of elements in the list.

        Justification:
            The method uses a recursive approach to build the tree by selecting the middle element of the current list segment as the root. 
            Although the overall operation remains linear in terms of element processing, 
            the complexity of inserting each node into the tree contributes logarithmically to the overall time, leading to a best-case scenario of O(n log n).
            In the worst case, each insertion operation into the balanced tree takes O(log(n)) time. 
            As every node must be inserted into the tree, the total time complexity becomes O(n log n), 
            as the tree may not remain perfectly balanced at all times during insertions.

        Complexity requirements for full marks:
            Best Case Complexity: O(n * log(n))
            Worst Case Complexity: O(n * log(n))
            where n is the number of elements in the list.
        """
        self._build_tree(elements, 0, len(elements) - 1)

    def _build_tree(self, elements: List[Tuple[K, I]], start: int, end: int) -> None:
        """
        Auxiliary function to build a balanced binary search tree from sorted elements.

        Args:
            elements (List[Tuple[K, I]]): The sorted elements used to build the balanced tree.
            start (int): The starting index of the segment to be processed.
            end (int): The ending index of the segment to be processed.

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n), where n is the number of elements in the list.
            Worst Case Complexity: O(n), where n is the number of elements in the list.

        Justification:
            The function selects the middle element of the current segment as the root node of the subtree, ensuring that the tree remains balanced. 
            It recursively processes the left and right segments of the array. 
            Since each element is processed exactly once to build the tree, the overall complexity is linear, O(n). 

            The recursion occurs for each element, but since we're not performing any additional logarithmic operations during each call, 
            the time complexity remains O(n) for both the best and worst cases. 
            Each recursive call simply focuses on a smaller segment of the list without additional overhead, leading to efficient linear processing.
        """
        if start > end:
            return
        mid = (start + end) // 2
        key, item = elements[mid]
        self[key] = item  # __setitem__ method from bst.py to insert elements
        self._build_tree(elements, start, mid - 1)
        self._build_tree(elements, mid + 1, end)
