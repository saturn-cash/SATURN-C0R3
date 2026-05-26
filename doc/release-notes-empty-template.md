*The release notes draft is a temporary file that can be added to by anyone. See
[/doc/developer-notes.md#release-notes](/doc/developer-notes.md#release-notes)
for the process.*

*version* Release Notes Draft
===============================

Saturn Core version *version* is now available from:

  <https://saturncore.org/bin/saturn-core-*version*/>

This release includes new features, various bug fixes and performance
improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/saturn/saturn/issues>

To receive security and update notifications, please subscribe to:

  <https://saturncore.org/en/list/announcements/join/>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes in some cases), then run the
installer (on Windows) or just copy over `/Applications/Saturn-Qt` (on macOS)
or `saturnd`/`saturn-qt` (on Linux).

Upgrading directly from a version of Saturn Core that has reached its EOL is
possible, but it might take some time if the data directory needs to be migrated. Old
wallet versions of Saturn Core are generally supported.

Compatibility
==============

Saturn Core is supported and tested on the following operating systems or newer:
Linux Kernel 3.17, macOS 14, and Windows 10 (version 1903). Saturn
Core should also work on most other Unix-like systems but is not as
frequently tested on them. It is not recommended to use Saturn Core on
unsupported systems.

Notable changes
===============

P2P and network changes
-----------------------

Updated RPCs
------------


Changes to wallet related RPCs can be found in the Wallet section below.

New RPCs
--------

Build System
------------

Updated settings
----------------


Changes to GUI or wallet related settings can be found in the GUI or Wallet section below.

New settings
------------

Tools and Utilities
-------------------

Wallet
------

GUI changes
-----------

Low-level changes
=================

RPC
---

Tests
-----

*version* change log
====================

Credits
=======

Thanks to everyone who directly contributed to this release:


As well as to everyone that helped with translations on
[Transifex](https://explore.transifex.com/saturn/saturn/).
