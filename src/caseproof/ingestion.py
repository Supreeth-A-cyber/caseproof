import json
import logging

logger = logging.getLogger("caseproof")


def load_case(file_path):
    """
    Load an investigation case from a JSON file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            case_data = json.load(file)

        if not isinstance(case_data, dict):
            logger.error("Invalid case format: expected a JSON object.")
            return None

        logger.info("Case loaded successfully!")
        return case_data

    except FileNotFoundError:
        logger.error("Case file not found: %s", file_path)
        return None

    except json.JSONDecodeError as error:
        logger.error("Invalid JSON format: %s", error)
        return None

    except OSError as error:
        logger.error("Unable to read case file: %s", error)
        return None


def validate_case(case_data):
    """
    Check whether the case contains the required fields and data types.
    """

    if not isinstance(case_data, dict):
        logger.error("Invalid case structure: expected a dictionary.")
        return False

    required_fields = ["case_id", "case_title", "evidence", "claims"]

    for field in required_fields:
        if field not in case_data:
            logger.error("Missing required field: %s", field)
            return False

    if not isinstance(case_data["evidence"], list):
        logger.error("Invalid field: evidence must be a list.")
        return False

    if not isinstance(case_data["claims"], list):
        logger.error("Invalid field: claims must be a list.")
        return False

    logger.info("Case structure validated successfully!")
    return True