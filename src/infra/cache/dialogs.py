import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.domain.entities import Message


class DialogCache:
    def __init__(self, cache_dir: str = "dialog_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def save_dialog(
        self, messages: List[Message], dialog_id: Optional[str] = None
    ) -> str:
        """Save a dialog to local JSON file"""
        if dialog_id is None:
            dialog_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        dialog_data = {
            "dialog_id": dialog_id,
            "created_at": datetime.now().isoformat(),
            "messages": [{"role": msg.role, "text": msg.text} for msg in messages],
        }

        file_path = self.cache_dir / f"{dialog_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)

        return dialog_id

    def load_dialog(self, dialog_id: str) -> Optional[List[Message]]:
        """Load a dialog from local JSON file"""
        file_path = self.cache_dir / f"{dialog_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                dialog_data = json.load(f)

            messages = [
                Message(role=msg["role"], text=msg["text"])
                for msg in dialog_data["messages"]
            ]

            return messages
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return None

    def list_dialogs(self) -> List[dict]:
        """List all available dialogs with metadata"""
        dialogs = []

        for file_path in self.cache_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    dialog_data = json.load(f)

                dialogs.append(
                    {
                        "dialog_id": dialog_data.get("dialog_id", file_path.stem),
                        "created_at": dialog_data.get("created_at", ""),
                        "message_count": len(dialog_data.get("messages", [])),
                        "file_path": str(file_path),
                    }
                )
            except (json.JSONDecodeError, FileNotFoundError):
                continue

        # Sort by creation date (newest first)
        dialogs.sort(key=lambda x: x["created_at"], reverse=True)
        return dialogs

    def delete_dialog(self, dialog_id: str) -> bool:
        """Delete a dialog from local storage"""
        file_path = self.cache_dir / f"{dialog_id}.json"

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def get_dialog_info(self, dialog_id: str) -> Optional[dict]:
        """Get dialog metadata without loading all messages"""
        file_path = self.cache_dir / f"{dialog_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                dialog_data = json.load(f)

            return {
                "dialog_id": dialog_data.get("dialog_id", dialog_id),
                "created_at": dialog_data.get("created_at", ""),
                "message_count": len(dialog_data.get("messages", [])),
                "file_path": str(file_path),
            }
        except (json.JSONDecodeError, FileNotFoundError):
            return None
