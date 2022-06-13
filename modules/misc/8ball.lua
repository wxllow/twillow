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
