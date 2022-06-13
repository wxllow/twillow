# Lua Module Development (Recommended)

Module development with Lua is very easy and the recommended way to make modules for Twillow.
However, if you can't make a module with Lua for whatever reason, you can use [Python](python.md) instead!

## Making a module

First, you need to define the class which you want to make the module in. Here you can (optionally) define a name for the module. If you do not provide a name, the file name will be used.

```lua
MagicBallModule = {
    ['name'] = '8ball' -- This is used as the command prefix
}
```

Now, we can make the `new` function for the module that will be called when the module is loaded.
This will also contain all our module's subfunctions. And then we also need a `module` function that returns our module!

```lua
function MagicBallModule.new(o) 
    local inst = {}

    return inst
end

-- Tell Twillow where the module is. Should return your module class
function module()
    return MagicBallModule
end
```

### Making commands

Now, in our module, we can make functions that will be used as commands. If you do not want a function to be recognized as a command, add an underscore to the beginning.

Our function can take any amount of arguments, or none at all. Our function should return a string that is in [TwiML format](https://www.twilio.com/docs/messaging/twiml).

Let's start off by making a simple `8ball` command in our magic 8ball module

First, we will need to add the required imports to the beginning of our lua script.

```lua
local math = require("math")
local os = require("os")
```

Also add our choices for the 8ball to pick from. You can add/remove/modify the choices as you wish at any time.

```lua
-- Choices
local magic8ball = {'yes', 'no', 'maybe', 'probably', 'probably not', 'most definitely', 'yes, definitely', 'definitely not', 'no doubt', 'i doubt it'}
```

Finally, let's make our command! Our command will not need to accept any arguments, as it doesn't actually care what the user wants to ask the 8ball.

```Lua
-- `8ball` command
function inst:magicball(arg1, arg2, arg3)
    math.randomseed(os.time())
    return '<Response><Message>🎱 ' .. magic8ball[math.random(#magic8ball)] .. '</Message></Response>'
end
```

Here is our function. It makes a random seed using the current time and then returns a response of a random choice from the magic8ball list.

Add the plugin into your `config.toml` and run Twillow to see your plugin in action! Make sure you run `8ball 8ball` and not just `8ball` for now!

### Root command

If we do not have multiple commands, or we want a command that will run when there is not a valid subcommand specified, we can simply make a function in our module named `_all` to handle this.

```lua
    -- Root command (the function that will handle any call where a subcommand is missing, should return a function; Optional)
    function inst:_all()
        return inst.magicball
    end
```

That's it! Now we have made our first module in Lua!

## Limitations

For now, there is no standardized library to use for TwiML like in Python, so you will need to manually send the TwiML.

## Finished Module

Check [modules/misc/8ball.lua](https://github.com/wxllow/twillow/blob/master/modules/misc/8ball.lua) for the latest version.

```lua
-- Magic 8ball module -- 
local math = require("math")
local os = require("os")

-- Choices
local magic8ball = {'yes', 'no', 'maybe', 'probably', 'probably not', 'most definitely', 'yes, definitely', 'definitely not', 'no doubt', 'i doubt it'}

-- Module
MagicBallModule = {
    ['name'] = '8ball' -- This is used as the command prefix
}

function MagicBallModule.new(o) 
    local inst = {}

    -- `8ball` command
    function inst:magicball(arg1, arg2, arg3)
        math.randomseed(os.time())
        return '<Response><Message>🎱 ' .. magic8ball[math.random(#magic8ball)] .. '</Message></Response>'
    end

    -- Root command (the function that will handle any call where a subcommand is missing, should return a function; Optional)
    function inst:_all()
        return inst.magicball
    end

    return inst
end

-- Tell Twillow where the module is. Should return your module class
function module()
    return MagicBallModule
end

```
