








from typing import Tuple, Dict, Any, Callable, List, Set
from level2.dto import Task
from ..dto import DependencyConfig
from ..utils import safe_float
import collections

class DependencyMappingAgent:
    name = "DEPENDENCY_MAPPING"

    def _dfs_detect_cycle(self, node_id, graph, visited, stack) -> bool:
        visited.add(node_id)
        stack.add(node_id)
        for neigh in graph.get(node_id, []):
            if neigh not in visited:
                if self._dfs_detect_cycle(neigh, graph, visited, stack):
                    return True
            elif neigh in stack:
                return True
        stack.remove(node_id)
        return False

    def _topological_sort(self, nodes, graph):
        indeg = {n:0 for n in nodes}
        for n in nodes:
            for v in graph.get(n, []):
                indeg[v] = indeg.get(v,0) + 1
        q = collections.deque([n for n in nodes if indeg.get(n,0)==0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph.get(u, []):
                indeg[v] -= 1
                if indeg[v]==0:
                    q.append(v)
        return order

    def _longest_path_effort(self, start_id, graph, repo_fetcher, visited, memo) -> float:
        # возвращает суммарный effort на самом длинном пути из start_id
        if start_id in memo:
            return memo[start_id]
        max_child = 0.0
        for c in graph.get(start_id, []):
            if c in visited:
                continue
            visited.add(c)
            child_sum = self._longest_path_effort(c, graph, repo_fetcher, visited, memo)
            visited.remove(c)
            if child_sum > max_child:
                max_child = child_sum
        t = repo_fetcher(start_id)
        eff = safe_float(t.effort if t and getattr(t,'effort',None) is not None else (t.metadata.get("effort") if t and t.metadata else 0.0), 0.0) if repo_fetcher else 0.0
        total = eff + max_child
        memo[start_id] = total
        return total

    def score(self, task: Task, cfg: DependencyConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        """
        repo_fetcher(task_id)->Task должен возвращать Task или None. Если None -> анализ ограничен метаданными текущей задачи.
        """
        meta = task.metadata or {}
        # сбор графа: начнём от текущей задачи, рекурсивно собираем до max_depth
        graph = {}
        nodes = set()
        frontier = [(task.id, 0)]
        while frontier:
            tid, depth = frontier.pop()
            if tid in nodes:
                continue
            nodes.add(tid)
            t = repo_fetcher(tid) if repo_fetcher else None
            deps = []
            if t:
                deps = t.dependencies or []
            else:
                # если данных нет — берем метаданные текущего таска только
                if tid == task.id:
                    deps = task.dependencies or []
                else:
                    deps = []
            graph[tid] = deps
            if depth < cfg.max_depth:
                for d in deps:
                    frontier.append((d, depth+1))

        # detect cycles
        visited = set()
        has_cycle = self._dfs_detect_cycle(task.id, graph, set(), set())

        # topological order (if DAG)
        topo = self._topological_sort(list(nodes), graph) if not has_cycle else []

        # critical path approx (longest path by effort)
        critical_effort = 0.0
        critical_path_root = None
        if repo_fetcher:
            memo = {}
            for n in nodes:
                val = self._longest_path_effort(n, graph, repo_fetcher, set([n]), memo)
                if val > critical_effort:
                    critical_effort = val
                    critical_path_root = n

        details = {
            "nodes_count": len(nodes),
            "has_cycle": bool(has_cycle),
            "topological_len": len(topo),
            "critical_effort": critical_effort,
            "critical_root": critical_path_root
        }
        label = "CYCLE" if has_cycle else ("COMPLEX" if len(nodes) > 5 else "SIMPLE")
        # score: чем больше зависимостей и крит_effort — тем выше риск/сложность (0..1)
        score = min(1.0, (len(nodes) / 20.0) + (critical_effort / 100.0))
        return float(score), details, {"DEP_LABEL": label}







