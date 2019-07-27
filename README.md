# Blender Power Sequencer Render - BPSRender #

This is a [standalone python package](https://pypi.org/project/bpsrender/) as well as a command-line program you can use to speed up rendering [VSE projects](https://docs.blender.org/manual/en/dev/editors/vse/index.html) by spawning Blender processes in background in parallel. 

It is included with the [Blender Power Sequencer add-on](https://github.com/GDquest/Blender-power-sequencer).

![](https://i.imgur.com/BndLccL.gif)


## Install ##

To install BPSRender as a standalone command line utility, use [PiPy](https://pypi.org/project/bpsrender/): `pip install [--user] bpsrender`. 

*You must have `$HOME/.local/bin` included in your `$PATH` environment variable on GNU/Linux if you're going to install the utility locally (using `--user` when executing `pip`).*


## Usage ##

To read the help, after you installed BPSRender, type `bpsrender -h` in the shell:

```
usage: bpsrender [-h] [-o OUTPUT] [-w WORKERS] [-v] [--dry-run] [-s START]
                 [-e END] [-m] [-c] [-d] [-j]
                 blendfile

Multi-process Blender VSE rendering - will attempt to create a folder called
`render` inside of the folder containing `blendfile`. Insider `render` another
folder called `parts` will be created for storing temporary files. These files
will be joined together as the last step to produce the final render which
will be stored inside `render` and it will have the same name as `blendfile`

positional arguments:
  blendfile             Blender project file to render.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder (will contain a `bpsrender` temp folder
                        forrendering parts).
  -w WORKERS, --workers WORKERS
                        Number of workers in the pool (for video rendering).
  -v, --verbose         Increase verbosity level (eg. -vvv).
  --dry-run             Run the script without actual rendering or creating
                        files and folders. For DEBUGGING purposes
  -s START, --start START
                        Start frame
  -e END, --end END     End frame
  -m, --mixdown-only    ONLY render the audio MIXDOWN
  -c, --concatenate-only
                        ONLY CONCATENATE the (already) available video chunks
  -d, --video-only      ONLY render the VIDEO (implies --concatenate-only).
  -j, --join-only       ONLY JOIN the mixdown with the video. This will
                        produce the final render
```

## External Dependencies ##

BPSRender requires

- `blender`
- `ffmpeg`

to be available in the `$PATH` environment variable in order to work. If BPSRender catches a missing dependency it throws a an error similar to this:

```
BPSRender couldn't find external dependencies:
[v] blender: /home/razvan/.local/bin/blender
[X] ffmpeg: NOT FOUND
Check if you have them properly installed and available in the PATH environemnt variable.
Exiting...
```

## Tips ##

Here are some tips about using BPSRender as a command line utility.

### Deleting the temporary folder after a successful render ###

BPSRender creates a `bpsrender/` folder next to the `blendfile` it renders. There, it stores rendered video parts, the audio soundtrack from the project, and a text file to stitch the parts together. It does not automatically delete this folder at the moment. To do so, using the GNU/Linux shell, you can use these commands:

```shell
bpsrender my_file.blend && rm -rf bpsrender
```

After the render finished successfully, this will delete the `bpsrender` folder.

### Rendering multiple projects with POSIX shells ###

You can render many projects one after the other from the terminal using the `find` command:

```shell
find . -name "*.blend" -exec bpsrender {} \;
```

## Known Issues ##

- [  ] CTRL-C interrupt leaves subprocesses running in the background
- [  ] CTRL-C interrupt doesn't clean the folders yet
