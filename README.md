Css2Sass
========

Sublime text plugin to convert CSS in the clipboard to SASS on your screen.

### Installation

To install, well, come talk to me and I'll sort it out for you. Soon it'll be in package control.

Or, if you'd like to go it alone...

###### Installing through package control

Coming soon...

###### Installing the hard way

1. Clone repository to your sublime text packages directory.
2. Follow all other instructions.

### Usage

Insert CSS from your clipboard into a .css.sass file using `"super+k+v"`. The CSS will be inserted into your file as SASS. Perfect for copying straight from Stack Overflow.

This plugin is intended to be very much a background worker. To that end, I recommend mapping `"super+v"` to the `"css_to_sass"` command in your user key bindings. 

```json
# Preferences/Key Bindings - User

[
    {
        "keys": ["super+v"], "command": "css_to_sass"
    }
]
```

From there, you can start pasting raw CSS into your .css.sass files and be amazed as pure sass goodness is pasted into your file, and all text pasted into other files will be pasted in as usual (so no worries there!)


![demo](Screenshots/Css2Sass.gif)

### Setup Issues

###### Sass Gem

You must have the sass gem installed to use this plugin. Internally, we use the `sass-convert` command, which requires the sass gem. To install the sass gem visit http://sass-lang.com/install

###### Ruby Version Managers

If you are using RVM or rbenv etc, then you will need to set the path in settings, as RVM/rbenv modify the environment path, which messes with sublimes use of the path.

To find your path you can run `echo $PATH` on the command line. Copy the result then paste it into the Css2Sass user settings file, as shown below.

```json
# Preferences/Package Settings/Css2Sass/Settings - User

{
    "path": "your/copied/path/here"
}
```

### Known Issues

None yet. If you disagree, create an issue or let me know on twitter ([@nmdowse](http://www.twitter.com/nmdowse "Nick Dowse twitter")). Most of the hard work was done by the creators and maintainers of SassBeautify, another great Sublime Text Plugin. So, thanks to them!
