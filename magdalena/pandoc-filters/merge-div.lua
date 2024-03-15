-- Lua filter to merge div with same class

-- Function to calculate length of div
function len_div(div)
    local len = 0
    for _ in pairs(div.content) do
        len = len + 1
    end

    return len
end

-- Function to check if two div have the same classes
function divs_have_same_class(div1, div2)
    local len_div1 = len_div(div1)
    local len_div2 = len_div(div2)

    if len_div1 ~= len_div2 then
        return false
    end

    for i=1,len_div1 do
        if div1.attr.classes[i] ~= div2.attr.classes[i] then
            return false
        end
    end

    return true
end

-- Function to merge blocks with the same classes
function Blocks(blocks)
    local new_blocks = {}

    local previous_div = nil

    for index, block in ipairs(blocks)
    do
        if previous_div == nil then
            if block.tag == 'Div' then
                previous_div = block
            else
                table.insert(new_blocks, block)
            end
        else
            if block.tag == 'Div' then
                if divs_have_same_class(previous_div, block) then
                    for _, value in ipairs(block.content) do
                        table.insert(previous_div.content, value)
                    end
                else
                    table.insert(new_blocks, previous_div)
                    previous_div = block    
                end
            else
                table.insert(new_blocks, previous_div)
                table.insert(new_blocks, block)

                previous_div = nil
            end
        end
    end

    -- Insert last element
    if previous_div ~= nil then
        table.insert(new_blocks, previous_div)
    end
    
    return new_blocks
end