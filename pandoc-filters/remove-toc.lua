function Div(element)
    if element.attr.attributes["custom-style"] == "toc 1" then
        return {}
    else
        return element
    end
end

function Header(element)
    if element.level == 1 then
        if element.attr.identifier == "contents" then
            return {}
        else
            return element
        end
    else
        return element
    end
end