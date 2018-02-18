# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016, Niklas Hauser
# Copyright (c)      2016, Fabian Greif
# All rights reserved.

import os
import logging

from lxml import etree

from ..device_tree import DeviceTree
from .device_file import DeviceFileWriter

LOGGER = logging.getLogger("dfg.output.xml")

class DeviceMemmapWriter(DeviceFileWriter):
    """ DeviceFileWriter
    Formats a generic tree as a modm device file.
    """

    @staticmethod
    def toEtree(tree):
        assert tree.name == "memmap"

        # Add the RCA root element
        root = etree.Element("modm")
        root.set("version", "0.4.0")
        root.append(etree.Comment(" WARNING: This file is generated by the modm device file generator. Do not edit! "))
        # Format the entire tree
        device = etree.SubElement(root, tree.name)
        # Add the naming schema
        DeviceFileWriter._to_etree(tree, device)
        return root

    @staticmethod
    def format(tree):
        return etree.tostring(DeviceMemmapWriter.toEtree(tree),
                              encoding="UTF-8",
                              pretty_print=True,
                              xml_declaration=True)

    @staticmethod
    def write(tree, folder, name):
        path = os.path.join(folder, name(tree.ids) + ".xml")
        content = DeviceMemmapWriter.format(tree).decode("utf-8")

        if os.path.exists(path):
            LOGGER.warning("Overwriting file '%s'", os.path.basename(path))
        else:
            LOGGER.info("New XML file: '%s'", os.path.basename(path))
        with open(path, "w") as device_file:
            device_file.write(content)
        return path