
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



class CategoryUnavailableError(DomainError):
    status_code = 404
    detail = "Category not found or inactive"
    error_code = "CATEGORY_UNAVAILABLE"



class ProductUnavailableError(DomainError):
    status_code = 404
    detail = "Product not found or inactive"
    error_code = "PRODUCT_UNAVAILABLE"



class ReviewUnavailableError(DomainError):
    status_code = 404
    detail = "Review not found or inactive"
    error_code = "REVIEW_UNAVAILABLE"



class ProductPermissionDeniedError(DomainError):
    status_code = 403
    detail = "You can only update your own products"
    error_code = "PRODUCT_PERMISSION_DENIED"



