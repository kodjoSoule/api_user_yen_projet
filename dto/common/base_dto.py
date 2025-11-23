"""DTOs communs utilisés dans toute l'application"""
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class ApiResponse:
    """DTO de base pour toutes les réponses de l'API"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[list] = None

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        result = {'success': self.success}
        if self.message is not None:
            result['message'] = self.message
        if self.data is not None:
            result['data'] = self.data
        if self.errors is not None:
            result['errors'] = self.errors
        return result


@dataclass
class ValidationError:
    """DTO pour les erreurs de validation"""
    field: str
    message: str

    def to_dict(self) -> dict:
        """Convertit le DTO en dictionnaire"""
        return {
            'field': self.field,
            'message': self.message
        }
