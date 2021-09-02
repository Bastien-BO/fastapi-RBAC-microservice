from sqlalchemy.orm import Session

"""
Add support for environment role settings
Need total refactor
"""


"""
def add_basic_permission(db: Session):
    crud = ["get", "add", "delete", "put"]
    model = ["user", "role", "permission"]
    for x in range(0, len(crud)):
        for y in range(0, len(model)):
            permission = PermissionCreate(name=crud[x] + "_" + model[y])
            user = get_permission_by_name(db=db, name=crud[x] + "_" + model[y])
            if not user:
                create_permission(db=db, permission=permission)
"""