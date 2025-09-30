import os
import json
import shutil
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# Add parent directory to Python path for imports
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
sys.path.insert(0, str(parent_dir))

from database.operations import (
    init_db,
    add_chat_message,
    add_memory,
    get_chat_history,
    get_all_memories,
    get_database_stats,
)
from database.models import ChatMessage, SpellbookMemory


class MigrationConfig:
    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent.parent

        templates_dir = self.base_path / "data" / "templates"

        self.files = {
            "chat_history": templates_dir / "chat-history.json",
            "spellbook_bee": templates_dir / "the-spellbook-bee.json",
            "spellbook_template": templates_dir / "the-spellbook.json",
        }

        self.db_path = self.base_path / "data" / "kairos.db"
        self.schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
        self.backup_dir = self.base_path / "data" / "backups"

    def get_spellbook_file(self) -> Path:
        """Get the best available spellbook file."""
        if self.files["spellbook_bee"].exists():
            return self.files["spellbook_bee"]
        return self.files["spellbook_template"]

    def _read_json_file(
        self, file_path: Path, expected_type: type = list
    ) -> Optional[Any]:
        """Common JSON file reading with validation."""
        if not file_path.exists():
            print(f"⚠️ {file_path.name} not found")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, expected_type):
                print(
                    f"❌ {file_path.name} is not a valid JSON {expected_type.__name__}"
                )
                return None

            return data
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
            return None

    def create_backup(self) -> bool:
        """Create timestamped backup of original JSON files."""
        try:
            self.backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_files = []

            for file_type, file_path in self.files.items():
                if file_path.exists():
                    backup_name = f"{file_type}_{timestamp}.json"
                    backup_path = self.backup_dir / backup_name

                    shutil.copy2(file_path, backup_path)
                    backup_files.append(backup_path)
                    print(f"✅ Backed up {file_path.name} to {backup_name}")

            print(f"✅ Created {len(backup_files)} backup files in {self.backup_dir}")
            return True

        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

    def migrate_chat_history(self) -> int:
        """Migrate chat history using ChatMessage model for validation."""
        print("📚 Migrating chat history...")

        chat_data = self._read_json_file(self.files["chat_history"])
        if not chat_data:
            return 0

        migrated_count = 0
        for msg_data in chat_data:
            try:
                # Create ChatMessage model for validation
                chat_msg = ChatMessage(
                    role=msg_data.get("role", ""),
                    content=msg_data.get("content", ""),
                    timestamp=msg_data.get("timestamp", datetime.now().isoformat()),
                )

                # Validate using model
                if not chat_msg.validate():
                    print(f"⚠️ Invalid chat message: {msg_data}")
                    continue

                # Add to database
                msg_id = add_chat_message(
                    role=chat_msg.role,
                    content=chat_msg.content,
                    timestamp=chat_msg.timestamp,
                    db_path=str(self.db_path),
                )

                if msg_id:
                    migrated_count += 1
                else:
                    print(f"⚠️ Failed to migrate message: {chat_msg.content[:50]}...")

            except Exception as e:
                print(f"⚠️ Error processing message: {e}")
                continue

        print(f"✅ Migrated {migrated_count} chat messages")
        return migrated_count

    def migrate_spellbook(self) -> int:
        """Migrate spellbook using SpellbookMemory model for validation."""
        print("🧙 Migrating spellbook...")

        spellbook_file = self.get_spellbook_file()
        spellbook_data = self._read_json_file(spellbook_file)
        if not spellbook_data:
            return 0

        migrated_count = 0
        for memory_obj in spellbook_data:
            if not isinstance(memory_obj, dict):
                print(f"⚠️ Skipping invalid memory object: {memory_obj}")
                continue

            for key, value in memory_obj.items():
                try:
                    # Extract data based on format
                    if isinstance(value, dict):
                        memory_value = value.get("value", "")
                        priority = value.get("priority", 5)
                        embedding = value.get("embedding")
                    else:
                        memory_value = str(value) if value else ""
                        priority = 5
                        embedding = None

                    # Skip empty values
                    if not memory_value.strip():
                        continue

                    # Create SpellbookMemory model
                    memory = SpellbookMemory(
                        memory_key=key,
                        memory_value=memory_value,
                        priority=priority,
                        embedding=embedding,
                    )

                    # Normalize and validate using model
                    memory.normalize()
                    if not memory.validate():
                        print(f"⚠️ Invalid memory after normalization: {key}")
                        continue

                    # Add to database
                    memory_id = add_memory(
                        memory_key=memory.memory_key,
                        memory_value=memory.memory_value,
                        priority=memory.priority,
                        embedding=memory.embedding,
                        db_path=str(self.db_path),
                    )

                    if memory_id:
                        migrated_count += 1
                    else:
                        print(f"⚠️ Failed to migrate memory: {key}")

                except Exception as e:
                    print(f"⚠️ Error processing memory {key}: {e}")
                    continue

        print(f"✅ Migrated {migrated_count} spellbook memories")
        return migrated_count

    def verify_migration(self) -> bool:
        """Verify that migration was successful."""
        print("🔍 Verifying migration...")

        try:
            stats = get_database_stats(str(self.db_path))

            print("📊 Database Statistics:")
            print(f"  Chat messages: {stats.get('chat_history_count', 0)}")
            print(f"  Memories: {stats.get('spellbook_memories_count', 0)}")

            # Test data retrieval
            recent_chats = get_chat_history(5, str(self.db_path))
            memories = get_all_memories(str(self.db_path))

            print(f"✅ Verification successful:")
            print(f"  Retrieved {len(recent_chats)} recent chat messages")
            print(f"  Retrieved {len(memories)} memories")

            # Spot check: verify a few records
            if recent_chats:
                print(f"  Sample chat: {recent_chats[0]['content'][:50]}...")

            if memories:
                print(
                    f"  Sample memory: {memories[0]['memory_key']} = {memories[0]['memory_value'][:30]}..."
                )

            return True

        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False

    def run_migration(self, create_backup: bool = True) -> bool:
        """Run the complete migration process."""
        print("🚀 Starting Kairos AI Database Migration")
        print("=" * 50)

        try:
            # Step 1: Backup
            if create_backup and not self.create_backup():
                print("❌ Backup failed, aborting migration")
                return False

            # Step 2: Initialize database
            if not init_db(str(self.db_path), str(self.schema_path)):
                print("❌ Database initialization failed")
                return False

            # Step 3: Migrate data
            chat_count = self.migrate_chat_history()
            memory_count = self.migrate_spellbook()

            # Step 4: Verify
            if not self.verify_migration():
                print("❌ Migration verification failed")
                return False

            print("=" * 50)
            print("🎉 Migration completed successfully!")
            print(f"📚 Migrated {chat_count} chat messages")
            print(f"🧙 Migrated {memory_count} memories")
            print("💡 You can now use the database instead of JSON files")

            return True

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False


def main():
    """Main entry point for migration script."""
    print("🌙 Kairos AI Database Migration Tool")
    print()

    # Check if we're in the right directory
    if not Path("kairos_ai.py").exists():
        print("❌ Please run this script from the src/python directory")
        return 1

    # Ask user preferences
    print("Migration Options:")
    print("1. Use the-spellbook-bee.json (populated with your data)")
    print("2. Use the-spellbook.json (empty template)")

    choice = input("Choose spellbook version (1 or 2): ").strip()
    use_bee = choice == "1"

    backup_choice = input("Create backup of original files? (y/n): ").strip().lower()
    create_backup = backup_choice in ["y", "yes", "1", "true"]

    print()

    # Run migration
    config = MigrationConfig()
    success = config.run_migration(create_backup=create_backup)

    if success:
        print()
        print("Next Steps:")
        print("1. Update kairos-ai.py to use the database")
        print("2. Test the new database integration")
        print("3. Remove or archive old JSON files (after testing)")
    else:
        print("Migration failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
