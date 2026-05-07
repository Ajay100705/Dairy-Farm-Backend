"""
Custom permissions for accounts app.
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_owner
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_owner


class IsWorker(permissions.BasePermission):
    """
    Permission to only allow workers.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_worker
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_worker


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission to only allow admins or owners.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_owner or request.user.is_superuser)
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners to edit, but allow read for authenticated users.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_owner


class IsFarmOwner(permissions.BasePermission):
    """
    Permission to only allow farm owners.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_owner
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the farm
        if hasattr(obj, 'farm'):
            return obj.farm.owner == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False


class IsFarmMember(permissions.BasePermission):
    """
    Permission to allow farm members (owner or worker with access).
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Owner can access their own farms
        if user.is_owner:
            if hasattr(obj, 'farm'):
                return obj.farm.owner == user
            if hasattr(obj, 'owner'):
                return obj.owner == user
        
        # Worker can access if they have membership
        if user.is_worker:
            farm_id = None
            if hasattr(obj, 'farm'):
                farm_id = obj.farm_id
            elif hasattr(obj, 'farm_id'):
                farm_id = obj.farm_id
            
            if farm_id:
                return user.farm_memberships.filter(
                    farm_id=farm_id,
                    is_active=True,
                    status='active'
                ).exists()
        
        return False


class CanManageAnimals(permissions.BasePermission):
    """
    Permission to check if user can manage animals.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        farm_id = getattr(obj, 'farm_id', None) or getattr(obj.farm, 'id', None)
        
        if not farm_id:
            return False
        
        # Owner can always manage
        if user.is_owner:
            return True
        
        # Check worker permissions
        membership = user.farm_memberships.filter(
            farm_id=farm_id,
            is_active=True,
            status='active'
        ).first()
        
        if not membership:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return membership.can_add_animals
        elif request.method in ['PUT', 'PATCH']:
            return membership.can_edit_animals
        elif request.method == 'DELETE':
            return membership.can_delete_animals
        
        return False


class CanLogProduction(permissions.BasePermission):
    """
    Permission to check if user can log production.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations, check permission
        farm_id = request.data.get('farm') or view.kwargs.get('farm_pk')
        if not farm_id:
            return False
        
        user = request.user
        if user.is_owner:
            return True
        
        membership = user.farm_memberships.filter(
            farm_id=farm_id,
            is_active=True,
            status='active'
        ).first()
        
        return membership and membership.can_log_production


class CanViewReports(permissions.BasePermission):
    """
    Permission to check if user can view reports.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        if user.is_owner:
            return True
        
        farm_id = request.query_params.get('farm') or view.kwargs.get('farm_pk')
        if not farm_id:
            return False
        
        membership = user.farm_memberships.filter(
            farm_id=farm_id,
            is_active=True,
            status='active'
        ).first()
        
        return membership and membership.can_view_reports
