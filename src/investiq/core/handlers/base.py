from dataclasses import dataclass

from investiq.core.commands import Command
from investiq.core.events import CanonicalEvent


@dataclass(frozen=True)
class HandlerResult:
    events: tuple[CanonicalEvent, ...] = ()
    commands: tuple[Command, ...] = ()
