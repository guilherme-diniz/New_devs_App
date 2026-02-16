import pytest
from decimal import Decimal
from app.services.reservations import calculate_monthly_revenue


@pytest.mark.asyncio
class TestCalculateMonthlyRevenue:
    """
    Tests run against the seeded Docker Postgres database.

    Seed data reference (relevant entries):
      - res-tz-1:  prop-001 / tenant-a, check_in 2024-02-29 23:30:00+00, amount 1250.000
                   Property timezone: Europe/Paris → check-in is 2024-03-01 00:30:00 local
      - res-dec-1: prop-001 / tenant-a, check_in 2024-03-15, amount 333.333
      - res-dec-2: prop-001 / tenant-a, check_in 2024-03-16, amount 333.333
      - res-dec-3: prop-001 / tenant-a, check_in 2024-03-17, amount 333.334
      - prop-004 / tenant-b (America/New_York): 4 reservations totaling 1776.50
    """

    async def test_march_paris_includes_timezone_boundary_reservation(self):
        """res-tz-1 is Feb 29 23:30 UTC but March 1 00:30 in Paris — should count in March."""
        result = await calculate_monthly_revenue("prop-001", "tenant-a", 3, 2024)
        # 1250.000 + 333.333 + 333.333 + 333.334 = 2250.000
        assert result == Decimal("2250.000")

    async def test_february_paris_excludes_timezone_boundary_reservation(self):
        """res-tz-1 is March in Paris — February should have nothing."""
        result = await calculate_monthly_revenue("prop-001", "tenant-a", 2, 2024)
        assert result == Decimal("0")

    async def test_month_with_no_reservations(self):
        """January 2024 has no seed data for prop-001."""
        result = await calculate_monthly_revenue("prop-001", "tenant-a", 1, 2024)
        assert result == Decimal("0")

    async def test_new_york_property_march(self):
        """prop-004 / tenant-b in America/New_York — all mid-day UTC, no boundary ambiguity."""
        result = await calculate_monthly_revenue("prop-004", "tenant-b", 3, 2024)
        # 420.00 + 560.75 + 480.25 + 315.50 = 1776.50
        assert result == Decimal("1776.500")

    async def test_tenant_isolation(self):
        """prop-001 exists for both tenants — tenant-b has no reservations for it."""
        result = await calculate_monthly_revenue("prop-001", "tenant-b", 3, 2024)
        assert result == Decimal("0")

    async def test_nonexistent_property(self):
        """A property that doesn't exist should return zero."""
        result = await calculate_monthly_revenue("prop-999", "tenant-a", 3, 2024)
        assert result == Decimal("0")
