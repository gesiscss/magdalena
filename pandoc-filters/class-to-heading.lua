-- Lua filter to use HTML h3 when needed
function InsertH3Quote(element)
    return {
        pandoc.Header(3, element.content[1].content, element.attr)
    }
end

function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'references-heading' then
            return InsertH3Quote(element)
        end
    end

    return nil
end