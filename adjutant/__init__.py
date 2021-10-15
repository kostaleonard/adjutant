"""adjutant is a package for managing ML experiments over Discord in conjunction
with WandB."""

from pkg_resources import get_distribution
from adjutant import adjutant_client

__version__ = get_distribution('adjutant-discord').version
Adjutant = adjutant_client.Adjutant
