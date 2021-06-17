# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from . import bs_ui
from . import bs_operators
from . import resources

bl_info = {
    "name": "Blenderstands",
    "author": "RDPolarity",
    "description": "A plugin to work with armourstands in blender",
    "blender": (2, 83, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

module_list = (
    bs_operators,
    resources,
    bs_ui
)

def register():
    print("[Blenderstands Loaded]")
    for module in module_list:
        module.register()


def unregister():
    print("[Blenderstands UnLoaded]")
    for module in module_list:
        module.unregister()

if __name__ == "__main__":
    register()