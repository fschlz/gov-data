import numpy as np
import logging

logger = logging.getLogger(__name__)


def calc_cagr(arr: np.array, n_years: float) -> float:
    """calculate Cumulative Annual Growth Rate (CAGR)

    Args:
        arr (np.array): array of values from which to calculate the CAGR
        n_years (float): number of periods (years)

    Raises:
        e: any Exception thrown

    Returns:
        float: CAGR
    """

    try:
        first_val = arr[0]
        last_val = arr[-1]
        cagr = (
            (last_val / first_val) ** (1 / n_years) - 1
        )
        return cagr if isinstance(cagr, float) else 0.0
    except Exception:
        logger.error("shits wrong:\n %s" % (set(arr)), exc_info=True)
        return 0.0


def calc_unit_price(arr_return: np.array, arr_amount: np.array) -> float:
    return np.sum(arr_return) / np.sum(arr_amount)
