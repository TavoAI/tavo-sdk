"""
Code Submitter for Tavo Scanner

Handles submission of code to API server for remote analysis.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncio


class CodeSubmitter:
    """Handles code submission to TavoAI API server."""

    def __init__(self, sdk_integration):
        """Initialize code submitter.

        Args:
            sdk_integration: SDK integration instance
        """
        self.sdk_integration = sdk_integration

    async def submit_file(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """Submit a single file for analysis.

        Args:
            file_path: Path to file to submit
            **kwargs: Additional submission options

        Returns:
            Submission result with ID and status
        """
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path_obj.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Read file content
        try:
            with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                code_content = f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file {file_path}: {e}")

        # Prepare submission data
        submission_data = {
            'code': code_content,
            'filename': file_path_obj.name,
            'language': self._detect_language(file_path_obj),
            'file_path': str(file_path_obj),
            **kwargs
        }

        # Submit to API
        return await self.sdk_integration.submit_code(**submission_data)

    async def submit_directory(self, dir_path: str, **kwargs) -> Dict[str, Any]:
        """Submit a directory for analysis.

        Args:
            dir_path: Path to directory to submit
            **kwargs: Additional submission options

        Returns:
            Submission result
        """
        dir_path_obj = Path(dir_path)

        if not dir_path_obj.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")

        if not dir_path_obj.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")

        # Collect all code files
        code_files = []
        for file_path in self._find_code_files(dir_path_obj):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    code_files.append({
                        'filename': file_path.name,
                        'path': str(file_path.relative_to(dir_path_obj)),
                        'content': content,
                        'language': self._detect_language(file_path)
                    })
            except Exception as e:
                # Skip files that can't be read
                continue

        if not code_files:
            raise ValueError(f"No code files found in directory: {dir_path}")

        # Submit directory as bulk operation
        return await self.sdk_integration.ai_bulk_operations.post_bulk_analysis(
            items=[
                {
                    'type': 'code_submission',
                    'data': file_data,
                    **kwargs
                }
                for file_data in code_files
            ]
        )

    async def submit_url(self, repository_url: str, **kwargs) -> Dict[str, Any]:
        """Submit a repository URL for analysis.

        Args:
            repository_url: Git repository URL
            **kwargs: Additional submission options

        Returns:
            Submission result
        """
        # For URL submissions, we'll create a scan request instead
        return await self.sdk_integration.create_scan(
            repository_url=repository_url,
            **kwargs
        )

    def _find_code_files(self, dir_path: Path, max_files: int = 100) -> List[Path]:
        """Find code files in directory."""
        code_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.clj', '.hs', '.ml', '.fs', '.vb', '.lua', '.pl', '.pm',
            '.r', '.m', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.sql',
            '.xml', '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg'
        }

        code_files = []
        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in code_extensions:
                code_files.append(file_path)
                if len(code_files) >= max_files:
                    break

        return code_files

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.clj': 'clojure',
            '.hs': 'haskell',
            '.ml': 'ocaml',
            '.fs': 'fsharp',
            '.vb': 'vb',
            '.lua': 'lua',
            '.pl': 'perl',
            '.pm': 'perl',
            '.r': 'r',
            '.m': 'matlab',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.fish': 'fish',
            '.ps1': 'powershell',
            '.sql': 'sql',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'ini'
        }

        return extension_map.get(file_path.suffix.lower(), 'unknown')

    async def get_submission_status(self, submission_id: str) -> Dict[str, Any]:
        """Get status of code submission.

        Args:
            submission_id: Submission identifier

        Returns:
            Submission status
        """
        # This would need a specific endpoint for submission status
        # For now, we'll use job status if it's a job
        try:
            return await self.sdk_integration.get_job_status(submission_id)
        except Exception:
            return {
                'id': submission_id,
                'status': 'unknown',
                'message': 'Unable to retrieve submission status'
            }


