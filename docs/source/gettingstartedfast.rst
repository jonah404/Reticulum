********************
Getting Started Fast
********************

The best way to get started with the Reticulum Network Stack depends on what
you want to do. This guide will outline sensible starting paths for different
scenarios.


Try Using a Reticulum-based Program
=============================================
If you simply want to try using a program built with Reticulum, you can take
a look at `Nomad Network <https://github.com/markqvist/nomadnet>`_, which
provides a complete encrypted communications suite built with Reticulum.

.. image:: screenshots/nomadnet_3.png
    :target: _images/nomadnet_3.png

`Nomad Network <https://github.com/markqvist/nomadnet>`_ is a user-facing client
for the messaging and information-sharing protocol
`LXMF <https://github.com/markqvist/lxmf>`_, another project built with Reticulum.

You can install Nomad Network via pip:

.. code::

   # Install ...
   pip3 install nomadnet

   # ... and run
   nomadnet

**Please Note**: If this is the very first time you use pip to install a program
on your system, you might need to reboot your system for your program to become
available. If you get a "command not found" error or similar when running the
program, reboot your system and try again.


Using the Included Utilities
=============================================
Reticulum comes with a range of included utilities that make it easier to
manage your network, check connectivity and make Reticulum available to other
programs on your system.

You can use ``rnsd`` to run Reticulum as a background or foreground service,
and the ``rnstatus``, ``rnpath`` and ``rnprobe`` utilities to view and query
network status and connectivity.

To learn more about these utility programs, have a look at the
:ref:`Using Reticulum on Your System<using-main>` chapter of this manual.


Creating a Network With Reticulum
=============================================
To create a network, you will need to specify one or more *interfaces* for
Reticulum to use. This is done in the Reticulum configuration file, which by
default is located at ``~/.reticulum/config``. You can edit this file by hand,
or use the interactive ``rnsconfig`` utility. 

When Reticulum is started for the first time, it will create a default
configuration file, with one active interface. This default interface uses
your existing ethernet network (if there is one), and only allows you to
communicate with other Reticulum peers within your local broadcast domain.

To communicate further, you will have to add one or more interfaces. The default
configuration includes a number of examples, ranging from using TCP over the
internet, to LoRa and Packet Radio interfaces.

Possibly, the examples in the config file are enough to get you started. If
you want more information, you can read the :ref:`Building Networks<networks-main>`
and :ref:`Interfaces<interfaces-main>` chapters of this manual.


Bridging Over the Internet
=============================================
Reticulum currently offers two interfaces for connecting nodes over the internet: 
`TCP <https://markqvist.github.io/Reticulum/manual/interfaces.html#tcp-server-interface>`_ and `I2P <https://markqvist.github.io/Reticulum/manual/interfaces.html#i2p-interface>`_. Each interface offers a different set of features, and Reticulum 
users should carefully choose the interface which best suites their needs. 

The ``TCPServerInterface`` allows users to host a node accessible over TCP/IP. This
method is generally faster, lower latency, and more energy efficient than using ``I2PInterface``,
however it leaks considerable metadata about the server host.

Direct TCP client connections are able to see your node's IP address and may be able
to use this information to determine your location or identity. Adversaries 
inspecting your network's internet packets may be able to record packet metadata 
like time of transmission and packet size. By default TCP does not encrypt traffic,
so an adversary may be able to use packet inspection to learn that a system is running
Reticulum, and what other IP adresses connect to it. Hosting a node via TCP server also
requires a public IP address.

The ``I2PInterface`` routes messages through the `Invisible Internet Protocol 
(I2P) <https://geti2p.net/en/>`_. To properly use this interface, users must also run an I2P daemon in
parallel to ``rnsd``. For always-on nodes it is recommended to use `i2pd <https://i2pd.website/>`_ because it
generally runs more efficiently. 

By default, I2P will fully encrypt all traffic sent over the network, and 
obfuscate both the sender's and receiver's IP addresses. Running an I2P node 
will also relay other I2P user's encrypted packets, which will use extra
bandwidth and compute power, but also makes timing attacks and other forms of 
deep-packet-inspection much more difficult. Similar to RNS, I2P uses cryptographic 
public keys as destination addresses, which allows users to host nodes on non-static IPs.

In general it is recommended to use an I2P node if you are hosting your node 
publicly.

There is a experimental public testnet you can join by adding the following
interfaces to your ``.reticulum/config`` file:

.. code::

  # For connecting over TCP/IP:

  [[RNS Testnet Frankfurt]]
    type = TCPClientInterface
    interface_enabled = yes
    outgoing = True
    target_host = frankfurt.rns.unsigned.io
    target_port = 4965


  # For connecting over I2P:

  [[RNS Testnet I2P Node A]]
    type = I2PInterface
    interface_enabled = yes
    peers = ykzlw5ujbaqc2xkec4cpvgyxj257wcrmmgkuxqmqcur7cq3w3lha.b32.i2p


Develop a Program with Reticulum
===========================================
If you want to develop programs that use Reticulum, the easiest way to get
started is to install the latest release of Reticulum via pip:

.. code::

   pip3 install rns

The above command will install Reticulum and dependencies, and you will be
ready to import and use RNS in your own programs. The next step will most
likely be to look at some :ref:`Example Programs<examples-main>`.

For extended functionality, you can install optional dependencies:

.. code::

   pip3 install pyserial netifaces


Further information can be found in the :ref:`API Reference<api-main>`.


Participate in Reticulum Development
==============================================
If you want to participate in the development of Reticulum and associated
utilities, you'll want to get the latest source from GitHub. In that case,
don't use pip, but try this recipe:

.. code::

    # Install dependencies
    pip3 install cryptography pyserial netifaces

    # Clone repository
    git clone https://github.com/markqvist/Reticulum.git

    # Move into Reticulum folder and symlink library to examples folder
    cd Reticulum
    ln -s ../RNS ./Examples/

    # Run an example
    python3 Examples/Echo.py -s

    # Unless you've manually created a config file, Reticulum will do so now,
    # and immediately exit. Make any necessary changes to the file:
    nano ~/.reticulum/config

    # ... and launch the example again.
    python3 Examples/Echo.py -s

    # You can now repeat the process on another computer,
    # and run the same example with -h to get command line options.
    python3 Examples/Echo.py -h

    # Run the example in client mode to "ping" the server.
    # Replace the hash below with the actual destination hash of your server.
    python3 Examples/Echo.py 3e12fc71692f8ec47bc5

    # Have a look at another example
    python3 Examples/Filetransfer.py -h

When you have experimented with the basic examples, it's time to go read the
:ref:`Understanding Reticulum<understanding-main>` chapter.


Reticulum on ARM64
==============================================
On some architectures, including ARM64, not all dependencies have precompiled
binaries. On such systems, you will need to install ``python3-dev`` before
installing Reticulum or programs that depend on Reticulum.

.. code::

   # Install Python and development packages
   sudo apt update
   sudo apt install python3 python3-pip python3-dev

   # Install Reticulum
   python3 -m pip install rns


Reticulum on Android
==============================================
Reticulum can be used on Android in different ways. The easiest way to get
started is using the `Termux app <https://termux.com/>`_, at the time of writing
available on `F-droid <https://f-droid.org>`_.

Termux is a terminal emulator and Linux environment for Android based devices,
which includes the ability to use many different programs and libraries,
including Reticulum.

Since the Python cryptography.io module does not offer pre-built wheels for
Android, the standard one-line install of Reticulum does not work on Android,
and a few extra commands are required.

From within Termux, execute the following:

.. code::

    # First, make sure indexes and packages are up to date.
    pkg update
    pkg upgrade

    # Then install dependencies for the cryptography library.
    pkg install python build-essential openssl libffi rust

    # Make sure pip is up to date, and install the wheel module.
    pip3 install wheel pip --upgrade

    # To allow the installer to build the cryptography module,
    # we need to let it know what platform we are compiling for:
    export CARGO_BUILD_TARGET="aarch64-linux-android"

    # Start the install process for the cryptography module.
    # Depending on your device, this can take several minutes,
    # since the module must be compiled locally on your device.
    pip3 install cryptography

    # If the above installation succeeds, you can now install
    # Reticulum and any related software
    pip3 install rns

It is also possible to include Reticulum in apps compiled and distributed as
Android APKs. A detailed tutorial and example source code will be included
here at a later point.
