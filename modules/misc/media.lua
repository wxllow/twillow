-- Module for sending back media from a URL -- 

MediaModule = {
    ['name'] = 'media' -- This is used as the command prefix
}

function MediaModule.new(o) 
    local inst = {}

    -- get command
    function inst:get(url)
        if not url then
            return '<Response><Message>No URL was specified!</Messgae></Response>'
        end

        return '<Response><Message>Sending media...</Message><Message><Media>' .. url .. '</Media></Message></Response>'
    end

    -- Called when no sub-commmand specified, should return another function
    function inst:_all()
        return inst.get
    end

    return inst
end

function module()
    return MediaModule
end
