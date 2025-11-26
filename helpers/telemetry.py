# Code was created with AI assistance.

import json
import os
from datetime import date
from asyncio import Lock
import aiofiles
import aiofiles.os

class Telemetry:
    def __init__(self, path="telemetry.json"):
        self.path = path
        self.lock = Lock()
        self.date = str(date.today())
        self.generated = 0
        self.success = 0
        self.fail = 0

    async def load(self):
        """Load telemetry from disk or create new if missing/corrupt."""
        if not os.path.exists(self.path):
            await self._write_new()
            return

        try:
            async with aiofiles.open(self.path, "r") as f:
                data = json.loads(await f.read())

            # Validate minimal expected structure
            if "date" not in data:
                raise ValueError("Invalid telemetry schema")

            self.date = data["date"]
            self.generated = data.get("generated", 0)
            self.success = data.get("success", 0)
            self.fail = data.get("fail", 0)

            # Reset if old date
            if self.date != str(date.today()):
                await self.reset()

        except Exception:
            # On corruption: recreate
            await self._write_new()

    async def _write_new(self):
        """Create a new telemetry.json with today's date and zeroed counters."""
        self.date = str(date.today())
        self.generated = 0
        self.success = 0
        self.fail = 0

        await self.save()
    
    async def reset(self):
        """Reset counters for new day."""
        self.date = str(date.today())
        self.generated = 0
        self.success = 0
        self.fail = 0
        await self.save()

    async def save(self):
        """Atomic write to avoid corruption."""
        async with self.lock:
            tmp_path = self.path + ".tmp"
            async with aiofiles.open(tmp_path, "w") as f:
                await f.write(json.dumps({
                    "date": self.date,
                    "generated": self.generated,
                    "success": self.success,
                    "fail": self.fail
                }, indent=4))

            # Replace original atomically
            await aiofiles.os.replace(tmp_path, self.path)

    # Increment methods
    async def inc_generated(self):
        await self._increment("generated")

    async def inc_success(self):
        await self._increment("success")

    async def inc_fail(self):
        await self._increment("fail")

    async def _increment(self, field):
        async with self.lock:
            # Reset if date rolled over
            if self.date != str(date.today()):
                await self.reset()

            setattr(self, field, getattr(self, field) + 1)
            await self.save()
