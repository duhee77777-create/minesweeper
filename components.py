"""
Core game logic for Minesweeper.

This module contains pure domain logic without any pygame or pixel-level
concerns. It defines:
- CellState: the state of a single cell
- Cell: a cell positioned by (col,row) with an attached CellState
- Board: grid management, mine placement, adjacency computation, reveal/flag

The Board exposes imperative methods that the presentation layer (run.py)
can call in response to user inputs, and does not know anything about
rendering, timing, or input devices.
"""

import random
from typing import List, Tuple


class CellState:
    """Mutable state of a single cell.

    Attributes:
        is_mine: Whether this cell contains a mine.
        is_revealed: Whether the cell has been revealed to the player.
        is_flagged: Whether the player flagged this cell as a mine.
        adjacent: Number of adjacent mines in the 8 neighboring cells.
    """

    def __init__(self, is_mine: bool = False, is_revealed: bool = False, is_flagged: bool = False, adjacent: int = 0):
        self.is_mine = is_mine
        self.is_revealed = is_revealed
        self.is_flagged = is_flagged
        self.adjacent = adjacent


class Cell:
    """Logical cell positioned on the board by column and row."""

    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row
        self.state = CellState()


class Board:
    """Minesweeper board state and rules.

    Responsibilities:
    - Generate and place mines with first-click safety
    - Compute adjacency counts for every cell
    - Reveal cells (iterative flood fill when adjacent == 0)
    - Toggle flags, check win/lose conditions
    """

    def __init__(self, cols: int, rows: int, mines: int):
        self.cols = cols
        self.rows = rows
        self.num_mines = mines
        self.cells: List[Cell] = [Cell(c, r) for r in range(rows) for c in range(cols)]
        self._mines_placed = False
        self.revealed_count = 0
        self.game_over = False
        self.win = False

    def index(self, col: int, row: int) -> int:
        """Return the flat list index for (col,row)."""
        return row * self.cols + col

    def is_inbounds(self, col: int, row: int) -> bool:
        # TODO: Return True if (col,row) is inside the board bounds.
        # Boundary check: 인덱스가 보드 범위 내에 존재하는지 검증
        return 0 <= col < self.cols and 0 <= row < self.rows

    def neighbors(self, col: int, row: int) -> List[Tuple[int, int]]:
        # TODO: Return list of valid neighboring coordinates around (col,row).
        deltas = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),           (1,  0),
            (-1,  1), (0,  1), (1,  1),
        ]
        result = []
        
        # 8방향을 순회하며 보드 범위 내(valid) 좌표만 수집
        for dc, dr in deltas:
            nc, nr = col + dc, row + dr
            if self.is_inbounds(nc, nr):
                result.append((nc, nr))
        
        return result

    def place_mines(self, safe_col: int, safe_row: int) -> None:
        # TODO: Place mines randomly, guaranteeing the first click and its neighbors are safe. And Compute adjacency counts
        # 1. 지뢰 배치 제외 구역 설정: 첫 클릭 위치 + 주변 8칸
        forbidden = {(safe_col, safe_row)} | set(self.neighbors(safe_col, safe_row))
        
        # 2. 전체 좌표 중 제외 구역을 뺀 후보군(Pool) 생성
        all_positions = [(c, r) for r in range(self.rows) for c in range(self.cols)]
        pool = [p for p in all_positions if p not in forbidden]
        
        # 3. 랜덤 샘플링으로 지뢰 배치
        count = min(self.num_mines, len(pool))
        mine_locs = random.sample(pool, count)
        
        for mc, mr in mine_locs:
            idx = self.index(mc, mr)
            self.cells[idx].state.is_mine = True
            self.mines_placed = True

        # 4. 모든 셀에 대해 인접 지뢰 개수(Adjacency) 계산
        for r in range(self.rows):
            for c in range(self.cols):
                idx = self.index(c, r)
                cell = self.cells[idx]
                
                if not cell.state.is_mine:
                    mine_count = 0
                    for nc, nr in self.neighbors(c, r):
                        n_idx = self.index(nc, nr)
                        if self.cells[n_idx].state.is_mine:
                            mine_count += 1
                    cell.state.adjacent = mine_count

    def reveal(self, col: int, row: int) -> None:
        # TODO: Reveal a cell; if zero-adjacent, iteratively flood to neighbors.
        # 1. 범위 및 예외 처리
        if not self.is_inbounds(col, row):
            return

        # 2. 첫 클릭인 경우 지뢰 배치
        if not self.mines_placed:
            self.place_mines(col, row)

        idx = self.index(col, row)
        cell = self.cells[idx]

        # 3. 이미 오픈되었거나 깃발이 꽂힌 경우 무시
        if cell.state.is_revealed or cell.state.is_flagged:
            return

        # 4. 셀 오픈 처리
        cell.state.is_revealed = True

        # 5. 지뢰를 밟은 경우
        if cell.state.is_mine:
            self.game_over = True
            self._reveal_all_mines()
            return

        # 6. 주변에 지뢰가 하나도 없는 빈 땅인 경우 -> 재귀적으로 주변 오픈 
        if cell.state.adjacent == 0:
            for nc, nr in self.neighbors(col, row):
                self.reveal(nc, nr)

        # 7. 승리 조건 확인
        self._check_win()

    def toggle_flag(self, col: int, row: int) -> None:
        # TODO: Toggle a flag on a non-revealed cell.
        # 1. 좌표 유효성 검사 
        if not self.is_inbounds(col, row):
            return

        idx = self.index(col, row)
        cell = self.cells[idx]

        # 2. 이미 오픈된 셀에는 깃발 조작 불가
        if cell.state.is_revealed:
            return

        # 3. 플래그 상태 토글
        cell.state.is_flagged = not cell.state.is_flagged
        

    def flagged_count(self) -> int:
        # TODO: Return current number of flagged cells.
        pass

    def _reveal_all_mines(self) -> None:
        """Reveal all mines; called on game over."""
        for cell in self.cells:
            if cell.state.is_mine:
                cell.state.is_revealed = True

    def _check_win(self) -> None:
        """Set win=True when all non-mine cells have been revealed."""
        total_cells = self.cols * self.rows
        if self.revealed_count == total_cells - self.num_mines and not self.game_over:
            self.win = True
            for cell in self.cells:
                if not cell.state.is_revealed and not cell.state.is_mine:
                    cell.state.is_revealed = True
