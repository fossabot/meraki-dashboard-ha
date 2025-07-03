"""Helper utilities for Meraki Dashboard integration."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from homeassistant.core import HomeAssistant


async def batch_api_calls(
    hass: HomeAssistant,
    api_calls: list[tuple[Callable, tuple, dict]],
    max_concurrent: int = 5,
    delay_between_batches: float = 0.1,
) -> list[Any]:
    """Execute multiple API calls in batches with concurrency control.

    Args:
        hass: Home Assistant instance
        api_calls: List of tuples (function, args, kwargs)
        max_concurrent: Maximum concurrent API calls
        delay_between_batches: Delay between batches in seconds

    Returns:
        List of results in the same order as input calls
    """
    results = []

    # Process in batches
    for i in range(0, len(api_calls), max_concurrent):
        batch = api_calls[i : i + max_concurrent]
        batch_tasks = []

        for func, args, kwargs in batch:
            # Create task for each API call
            task = hass.async_add_executor_job(func, *args, **kwargs)
            batch_tasks.append(task)

        # Wait for batch to complete
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        results.extend(batch_results)

        # Add delay between batches to avoid rate limiting
        if i + max_concurrent < len(api_calls):
            await asyncio.sleep(delay_between_batches)

    return results
