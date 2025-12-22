from typing import Any, Optional
import math


class PaginationParams:
    """Helper class for pagination parameters."""
    
    def __init__(self, page: int = 1, page_size: int = 20):
        self.page = max(1, page)
        self.page_size = max(1, min(page_size, 100))  # Cap at 100
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size
    
    def get_pagination_data(self, total: int) -> dict[str, Any]:
        """Generate pagination metadata."""
        total_pages = math.ceil(total / self.page_size)
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total": total,
            "total_pages": total_pages
        }
