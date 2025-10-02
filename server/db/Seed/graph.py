from collections import defaultdict, deque
from typing import List, Dict, Set
from sqlalchemy.orm import DeclarativeBase

# --- Step 1: Extract Dependencies from SQLAlchemy Metadata ---


def build_dependency_graph(Base: DeclarativeBase) -> Dict[str, Set[str]]:
    """
    Analyzes SQLAlchemy models from the DeclarativeBase to build a dependency graph.

    The graph is built as: {child_table_name: {parent_table_name, ...}}
    Loading order must be: Parent -> Child.
    """
    dependency_graph = defaultdict(set)

    # Base.metadata contains all Table objects created by the Declarative Base
    for table in Base.metadata.sorted_tables:
        child_table_name = table.name

        # Foreign keys define the dependencies (which tables must be loaded first)
        for constraint in table.foreign_key_constraints:
            # The 'referred_table' is the parent table (the one being referenced)
            parent_table = constraint.referred_table
            parent_table_name = parent_table.name

            # Skip self-referential foreign keys for this simple sort (unless you have seed data for them)
            if parent_table_name == child_table_name:
                continue

            # Add the dependency: Child depends on Parent
            dependency_graph[child_table_name].add(parent_table_name)

    return dependency_graph


# --- Step 2: Implement Kahn's Topological Sort Algorithm ---


def topological_sort_tables(
    all_table_names: List[str], dependencies: Dict[str, Set[str]]
) -> List[str]:
    """
    Performs a topological sort to determine the safe data loading order (Parent first).
    Uses the inverse of the dependency graph (which tables depend *on* a given table).
    """

    # 1. Build the INVERSE graph and calculate in-degrees (number of tables a table depends on)

    # Graph: {parent: {child, ...}}
    adj: Dict[str, Set[str]] = defaultdict(set)

    # In-degree: {table_name: count}
    in_degree: Dict[str, int] = {name: 0 for name in all_table_names}

    # Iterate through the original dependency map (Child -> Parent)
    for child, parents in dependencies.items():
        for parent in parents:
            # Add edge to the ADJ list for the reverse direction (Parent -> Child)
            adj[parent].add(child)

            # The child's in-degree is incremented for each parent it depends on
            in_degree[child] += 1

    # 2. Initialize queue with nodes having an in-degree of 0 (tables with no dependencies)
    queue = deque([table for table, degree in in_degree.items() if degree == 0])

    sorted_order: List[str] = []

    # 3. Process the graph
    while queue:
        # Tables with 0 dependencies are safe to load now (Parent table)
        parent_table = queue.popleft()
        sorted_order.append(parent_table)

        # For every table that depends on this parent:
        for child_table in adj[parent_table]:
            # "Remove" the dependency edge
            in_degree[child_table] -= 1

            # If the child now has 0 remaining dependencies, it's safe to load next
            if in_degree[child_table] == 0:
                queue.append(child_table)

    # 4. Check for cycles (e.g., Table A references Table B, and Table B references Table A)
    if len(sorted_order) != len(all_table_names):
        # In a seed-loading context, this is a serious error. You'd need to
        # use `use_alter=True` on one of the ForeignKeys to break the cycle.
        raise ValueError(
            "Cyclic dependency detected in database schema! Cannot determine safe loading order."
        )

    return sorted_order
