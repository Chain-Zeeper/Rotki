import os

from gevent import monkey  # isort:skip
monkey.patch_all()  # isort:skip
import logging
import sys
import traceback
from pathlib import Path

from rotkehlchen.errors.misc import DBSchemaError, SystemPermissionError
from rotkehlchen.logging import RotkehlchenLogsAdapter
from rotkehlchen.server import RotkehlchenServer

logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)


def setup_openssl():
    if getattr(sys, 'frozen', False) is True:
        # If running in PyInstaller bundle
        logger.debug(f'Running in a bundle {sys._MEIPASS}')
        base_path = Path(sys._MEIPASS)
        os.environ['OPENSSL_CONF'] = str(base_path / 'openssl.cnf')
    else:
        logger.debug('Running in a normal Python environment')


def main() -> None:
    try:
        setup_openssl()
        rotkehlchen_server = RotkehlchenServer()
    except (SystemPermissionError, DBSchemaError) as e:
        print(f'ERROR at initialization: {e!s}')
        sys.exit(1)
    except SystemExit as e:
        if e.code is None or e.code in (0, 2):
            # exit_code 2 is for invalid arguments
            exit_code = 0 if e.code is None else e.code
            sys.exit(exit_code)
        else:
            tb = traceback.format_exc()
            log.critical(tb)
            print(f'Failed to start rotki backend:\n{tb}')
            sys.exit(1)
    except:  # noqa: B001, E722, RUF100  # pylint: disable=bare-except
        tb = traceback.format_exc()
        log.critical(tb)
        print(f'Failed to start rotki backend:\n{tb}')
        sys.exit(1)

    rotkehlchen_server.main()


if __name__ == '__main__':
    main()
