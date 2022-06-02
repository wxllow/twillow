-- A "recreation" of +1 (855) 444-8888 that plays one of the snippets that were played on the number--
local math = require("math")
local os = require("os")

math.randomseed(os.time())

CMIYGLVoiceHandler = {
    ['name'] = 'cmiygl' -- This is used as the command prefix
}

function CMIYGLVoiceHandler.new(o, app) 
    local inst = {}

    local songs = {
        'MOMMATALK.mp3',
        'PASSPORT.mp3',
        'NUMBER%20NUMBER.mp3',
        'SIR%20BAUDELAIRE.mp3',
        'RISE.mp3'
    }

    function inst:call_reply(request)
        return '<Response><Play>https://raw.githubusercontent.com/Netriza/cmiygl/main/' .. songs[math.random(#songs)] .. '</Play></Response>'
    end

    return inst
end

function voice_handler()
    return CMIYGLVoiceHandler
end
