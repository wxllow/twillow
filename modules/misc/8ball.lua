-- Magic 8ball module -- 
local math = require("math")
local os = require("os")

local magic8ball = {'yes', 'no', 'maybe', 'probably', 'probably not', 'most definitely', 'yes, definitely', 'definitely not', 'no doubt', 'i doubt it'}

MagicBallModule = {
    ['name'] = '8ball' -- This is used as the command prefix
}

function MagicBallModule.new(o) 
    local inst = {}

    function inst:magicball()
        math.randomseed(os.time())
        return '<Response><Message>🎱 ' .. magic8ball[math.random(#magic8ball)] .. '</Message></Response>'
    end

    function inst:_all()
        return inst.magicball
    end

    return inst
end

function module()
    return MagicBallModule
end
