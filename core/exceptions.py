
class DomainError(Exception):
    status_code: int = 400
    detail: str = "Domain error"
    error_code: str = "DOMAIN_ERROR"


class CategoryNotFoundError(DomainError):
    status_code = 404
    detail = "Category not found"
    error_code = "CATEGORY_NOT_FOUND"



class ParentCategoryNotFoundError(DomainError):
    status_code = 400
    detail = "Parent category not found"
    error_code = "PARENT_CATEGORY_NOT_FOUND"



class CategorySelfParentError(DomainError):
    status_code = 400
    detail = "Category cannot be its own parent"
    error_code = "CATEGORY_SELF_PARENT"