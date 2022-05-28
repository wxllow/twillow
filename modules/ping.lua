PingModule = {
    ['name'] = 'ping' -- This is used as the command prefix
}

function PingModule.new(o) 
    local inst = {}
    
    function inst:ping()
        return '<Response><Message>🏓 Pong!</Message></Response>'
    end

    -- Called when no sub-commmand specified, should return another function
    function inst:_all()
        return inst.ping
    end

    return inst
end

function module()
    return PingModule
end
