"""
Prompt template loader and formatter.

Loads prompt templates from the prompts/ directory and formats them with variables.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path


class PromptLoader:
    """Loads and formats prompt templates from files."""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Path to prompts directory. Defaults to ./prompts relative to project root.
        """
        if prompts_dir is None:
            # Default to prompts/ in project root
            project_root = Path(__file__).parent.parent.parent
            prompts_dir = project_root / "prompts"
        
        self.prompts_dir = Path(prompts_dir)
        self._cache: Dict[str, str] = {}
    
    def load_template(self, template_name: str) -> str:
        """
        Load a prompt template from file.
        
        Args:
            template_name: Name of the template (without .txt extension)
            
        Returns:
            Raw template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # Check cache first
        if template_name in self._cache:
            return self._cache[template_name]
        
        # Load from file
        template_path = self.prompts_dir / f"{template_name}.txt"
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {template_path}\n"
                f"Available templates: {self.list_templates()}"
            )
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Cache for future use
        self._cache[template_name] = template
        return template
    
    def format_prompt(self, template_name: str, **kwargs) -> str:
        """
        Load and format a prompt template with variables.
        
        Args:
            template_name: Name of the template (without .txt extension)
            **kwargs: Variable values to substitute in the template
            
        Returns:
            Formatted prompt string
            
        Example:
            >>> loader = PromptLoader()
            >>> prompt = loader.format_prompt(
            ...     "orchestrator_summary",
            ...     student_name="Jane Doe",
            ...     interests="AI, Machine Learning",
            ...     career_data=json.dumps(career_results)
            ... )
        """
        template = self.load_template(template_name)
        
        # Handle None values gracefully
        safe_kwargs = {
            key: (value if value is not None else "N/A")
            for key, value in kwargs.items()
        }
        
        try:
            return template.format(**safe_kwargs)
        except KeyError as e:
            missing_var = str(e).strip("'")
            raise ValueError(
                f"Missing required variable '{missing_var}' for template '{template_name}'\n"
                f"Provided variables: {list(kwargs.keys())}"
            )
    
    def list_templates(self) -> list:
        """
        List all available prompt templates.
        
        Returns:
            List of template names (without .txt extension)
        """
        if not self.prompts_dir.exists():
            return []
        
        return [
            f.stem for f in self.prompts_dir.glob("*.txt")
            if f.stem != "README"
        ]
    
    def clear_cache(self):
        """Clear the template cache. Useful for development/testing."""
        self._cache.clear()


# Global singleton instance
_loader_instance: Optional[PromptLoader] = None


def get_loader() -> PromptLoader:
    """Get the global PromptLoader instance (singleton)."""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = PromptLoader()
    return _loader_instance


def load_prompt(template_name: str, **kwargs) -> str:
    """
    Convenience function to load and format a prompt template.
    
    Args:
        template_name: Name of the template (without .txt extension)
        **kwargs: Variable values to substitute in the template
        
    Returns:
        Formatted prompt string
        
    Example:
        >>> from src.services.prompt_loader import load_prompt
        >>> prompt = load_prompt(
        ...     "orchestrator_summary",
        ...     student_name="Jane Doe",
        ...     interests="AI, Machine Learning"
        ... )
    """
    loader = get_loader()
    return loader.format_prompt(template_name, **kwargs)


def reload_prompts():
    """
    Reload all prompt templates from disk.
    Useful during development when prompts are being edited.
    """
    loader = get_loader()
    loader.clear_cache()
