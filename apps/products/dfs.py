from collections import defaultdict


class CategoryDFS:
    """
    DFS traversal for the category hierarchy.
    """

    @staticmethod
    def build_tree(categories):
        """
        Build an adjacency list:

        {
            parent_id: [child_id, ...]
        }
        """

        tree = defaultdict(list)

        for category in categories:

            if category.parent_id:

                tree[category.parent_id].append(
                    category.id
                )

        return dict(tree)

    @staticmethod
    def traverse(tree, category_id):
        """
        Return all descendant category ids
        using Depth First Search.
        """

        visited = []

        stack = [category_id]

        while stack:

            current = stack.pop()

            for child in reversed(
                tree.get(current, [])
            ):

                visited.append(child)

                stack.append(child)

        return visited