import pytest

from p2p.chain import HeaderRequest
# TODO: can't use this exception
from eth.exceptions import ValidationError


FORWARD_0_to_5 = (0, 6, 0, False)
FORWARD_0_to_5_SKIP_1 = (0, 3, 1, False)

REVERSE_5_to_0 = (5, 6, 0, True)
REVERSE_5_to_0_SKIP_1 = (5, 3, 1, True)


@pytest.mark.parametrize(
    "params,sequence,is_match",
    (
        (FORWARD_0_to_5, tuple(), True),
        (FORWARD_0_to_5, (0, 1, 2, 3, 4, 5), True),
        (FORWARD_0_to_5, (0, 2, 4, 5), True),
        (FORWARD_0_to_5, (0, 5), True),
        (FORWARD_0_to_5, (2,), True),
        (FORWARD_0_to_5, (0,), True),
        (FORWARD_0_to_5, (5,), True),
        # skips
        (FORWARD_0_to_5_SKIP_1, tuple(), True),
        (FORWARD_0_to_5_SKIP_1, (0, 2, 4), True),
        (FORWARD_0_to_5_SKIP_1, (0, 4), True),
        (FORWARD_0_to_5_SKIP_1, (2, 4), True),
        (FORWARD_0_to_5_SKIP_1, (0, 2), True),
        (FORWARD_0_to_5_SKIP_1, (0,), True),
        (FORWARD_0_to_5_SKIP_1, (2,), True),
        (FORWARD_0_to_5_SKIP_1, (4,), True),
        # reverse
        (REVERSE_5_to_0, tuple(), True),
        (REVERSE_5_to_0, (5, 4, 3, 2, 1, 0), True),
        (REVERSE_5_to_0, (5, 4, 3), True),
        (REVERSE_5_to_0, (2, 1, 0), True),
        # duplicate value
        (FORWARD_0_to_5, (0, 0, 1, 2, 3, 4, 5), False),
        (FORWARD_0_to_5, (0, 1, 2, 2, 3, 4, 5), False),
        (FORWARD_0_to_5, (0, 1, 2, 3, 4, 5, 5), False),
        # extra value
        (FORWARD_0_to_5, (0, 1, 2, 3, 4, 5, 6), False),
        (FORWARD_0_to_5, (0, 1, 3, 5, 6), False),
        (FORWARD_0_to_5_SKIP_1, (0, 2, 4, 6), False),
        (FORWARD_0_to_5_SKIP_1, (0, 2, 3, 4), False),
        (FORWARD_0_to_5_SKIP_1, (0, 2, 3), False),
    ),
)
def test_header_request_sequence_matching(
        params,
        sequence,
        is_match):
    request = HeaderRequest(None, *params)

    if is_match:
        request.validate_sequence(sequence)
    else:
        with pytest.raises(ValidationError):
            request.validate_sequence(sequence)
