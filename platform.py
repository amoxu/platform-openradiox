import json
import os
from os.path import isdir, isfile, join
from platform import system
from platformio.managers.platform import PlatformBase
from platformio.util import get_systype

class OpenradioxPlatform(PlatformBase):
    
    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        board_config = self.board_config(board)

        default_protocol = board_config.get("upload.protocol") or "cmsis-dap"

        return PlatformBase.configure_default_packages(self, variables, targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get(
            "protocols", [])
        if "tools" not in debug:
            debug['tools'] = {}

        for link in ("cmsis-dap", "jlink", "stlink"):
            if link not in upload_protocols or link in debug['tools']:
                continue

            server_args = ["-s", "$PACKAGE_DIR/scripts"]

            if debug.get("openocd_board"):
                server_args.extend([
                    "-f", "board/%s.cfg" % debug.get("openocd_board")
                ])
            else:
                assert debug.get("openocd_target"), (
                    "Missed target configuration for %s" % board.id)
                transport = debug.get('transport',"swd")
                server_args.extend([
                    "-f", "interface/%s.cfg" % link,
                    "-c", "transport select %s" % (transport if link!="stlink" else "hla_"+transport),
                    "-f", "target/%s.cfg" % debug.get("openocd_target")
                ])
                server_args.extend(debug.get("openocd_extra_args", []))

            debug['tools'][link] = {
                "server": {
                    "package": "tool-openocd-kd32",
                    "executable": join("bin-"+ get_systype(), "openocd.exe" if system()=="Windows" else "openocd"),
                    "arguments": server_args
                }
            }
            debug['tools'][link]['onboard'] = link in debug.get("onboard_tools", [])
            debug['tools'][link]['default'] = link in debug.get("default_tools", [])

        board.manifest['debug'] = debug
        return board
