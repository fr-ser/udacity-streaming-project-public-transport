"""Used in local development (and docker) to wait until all services started"""


from shared_helpers.logging import logger
from shared_helpers.wait_until import check_faust_stream, check_ksql


if __name__ == "__main__":
    check_faust_stream()
    check_ksql()

    logger.info(f"All dependencies are there!")
