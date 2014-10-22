# A Minecraft / NuPIC Mashup

## NuPIC Fall 2014 Hackathon project with Minecraft.

The `java` directory contains classes for an [Forge Mod Loader](http://www.minecraftforge.net/) Minecraft mod that writes player location over a socket. The `python` directory contains a [NuPIC](https://github.com/numenta/nupic) client that connects to the same socket and accepts the coordinates to pass them into a CoordinateEncoder.

### Dependencies

- [Forge Mod Loader](http://www.minecraftforge.net/)
- [NuPIC](https://github.com/numenta/nupic)

### Running

First, start the python process that opens a socket and waits for a connection from the Java minecraft mod.

    python python/nupic_client.py

Then, start Minecraft using the Forge Mod Loader (you can find instructions on Eclipse and IntelliJ IDEA startup [here](http://www.minecraftforge.net/wiki/Installation/Source)).