-- Lua filter to remove extra div elements from the AST
function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'cite-as-heading' then
            return {}
        end

        if value == 'license-heading' then
            return {}
        end
    end

    return nil
end